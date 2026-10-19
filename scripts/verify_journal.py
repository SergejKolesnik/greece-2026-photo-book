"""Check the v3 editorial pages, image attribution, decoding and SVG topology.

Optional: --url https://.../ checks every deployed resource and the public manifest.
"""
import argparse,csv,hashlib,json,concurrent.futures,urllib.request,xml.etree.ElementTree as ET,re
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
repo=Path(__file__).resolve().parents[1];site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8-sig'))
photos={p['id']:p for p in data['photos']};pages=data['pages'];version=data['version_code']
assert version=='GR26-20261019-V05' and len(pages)==30 and [p['page'] for p in pages]==list(range(1,31))
flat=[ident for p in pages for ident in p['photos']]
personal=[ident for ident in flat if ident.startswith(('S','C'))]
selected=[ident for ident in personal if ident.startswith('S')]
assert len(personal)==69 and len(set(personal))==69
assert len(selected)==65 and len(set(selected))==65
assert set(selected)=={f'S{i:02}' for i in range(1,70)}-{'S01','S05','S14','S18'}
assert {ident for ident in personal if ident.startswith('C')}=={'C01','C02','C03','C04'}
assert flat.count('VENUS')==1 and photos['VENUS']['role']=='museum-image'
assert all(p['caption'] and p['date'] and p['location'] for p in pages)
assert all(p['photos'] for p in pages if p['layout'] not in ['stats'])
assert pages[14]['layout']=='history' and pages[14]['photos']==['VENUS']
assert pages[27]['layout']=='stats' and pages[27]['photos']==[]
assert pages[5]['layout']=='photo-story' and pages[24]['photos']==['S55']
travel=[ident for p in pages[1:] if p['layout'] not in ['history','stats'] for ident in p['photos']]
assert [photos[x]['date'] for x in travel]==sorted(photos[x]['date'] for x in travel)
assert pages[-2]['photos']==['S64','S65','S66','S67'] and pages[-1]['photos']==['S68','S69']
assert photos['S55']['width']>photos['S55']['height']
hashes=[]
for p in photos.values():
    for key in ['src','fallback']:
        file=site/p[key];assert file.exists(),file
        with Image.open(file) as image:assert image.size==(p['width'],p['height']);image.verify()
    if p['id'].startswith(('S','C')):
        with Image.open(site/p['fallback']) as image:assert not image.getexif()
        hashes.append(hashlib.sha256((site/p['fallback']).read_bytes()).hexdigest())
assert len(set(hashes))==73
manifest=list(csv.DictReader((repo/'SELECTION_MANIFEST.csv').open(encoding='utf-8-sig')))
cover=next(row for row in manifest if row['id']=='S12')
assert photos['S12']['sha256']==cover['source_sha256']
class JournalParser(HTMLParser):
    def __init__(self):super().__init__();self.articles=[];self.current=None;self.imgs=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and 'data-page' in a:self.current={'page':int(a['data-page']),'photos':[]};self.articles.append(self.current)
        if tag=='a' and 'data-photo' in a:self.current['photos'].append(a['data-photo'])
        if tag=='img' and a.get('src'):self.imgs.append(a)
        assert tag!='iframe','Reader must use the self-hosted SVG, not an independent map iframe'
    def handle_endtag(self,tag):
        if tag=='article':self.current=None
    def handle_data(self,data):self.text.append(data)
parser=JournalParser();parser.feed((site/'index.html').read_text(encoding='utf-8-sig'))
assert parser.articles==[{'page':p['page'],'photos':p['photos']} for p in pages]
assert len(parser.imgs)==70 and version in (site/'index.html').read_text(encoding='utf-8-sig')
reader=' '.join(parser.text).lower().replace(data['pages'][27]['stats_note'].lower(),'')
assert not any(term in reader for term in ['gps','одометр','трек','маршрутних даних'])
pdf=PdfReader(site/'greece-2026.pdf');assert len(pdf.pages)==30
pdftext=[p.extract_text() or '' for p in pdf.pages]
assert all(version in s for s in pdftext)
assert 'Венера' in pdftext[14] and 'Греція 2026 у цифрах' in pdftext[27]
assert 'S55' in pages[24]['photos'] and 'object-fit:cover' not in (site/'styles.css').read_text(encoding='utf-8-sig').split('.ship-page')[1].split('}',1)[0]
html_source=(site/'index.html').read_text(encoding='utf-8-sig')
svg=ET.fromstring(re.search(r'(<svg\b.*?</svg>)',html_source).group(1))
scene=next(el for el in svg if el.attrib.get('class')=='map-scene')
assert len([el for el in scene if el.attrib.get('class')=='island-coast'])==1
pins=[el for el in scene if el.attrib.get('class')=='map-pin'];assert len(pins)==12
assert {int(el.attrib['data-place']) for el in pins}==set(range(1,13))
coast=json.loads((site/'map-data/milos-coastline.geojson').read_text(encoding='utf-8'))
ring=coast['features'][0]['geometry']['coordinates'][0];assert ring[0]==ring[-1] and len(ring)>1000
args=argparse.ArgumentParser();args.add_argument('--url');opts=args.parse_args()
remote='not checked'
if opts.url:
    base=opts.url.rstrip('/')+'/'
    paths=['','content.json','content.js','app.js','map.js','styles.css','sw.js','greece-2026.pdf','map-data/milos-map.svg','map-data/places.json','map-data/milos-coastline.geojson']+[p[k] for p in photos.values() for k in ['src','fallback']]
    def check(path):
        with urllib.request.urlopen(urllib.request.Request(base+path,method='HEAD'),timeout=35) as r:
            assert r.status==200,(path,r.status)
            expected=(site/(path or 'index.html')).stat().st_size
            assert int(r.headers['Content-Length'])==expected,(path,r.headers['Content-Length'],expected)
        return path
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:list(pool.map(check,paths))
    with urllib.request.urlopen(base+'content.json',timeout=30) as r:assert json.load(r)==data,'Remote editorial manifest differs'
    remote=f'OK: {len(paths)} resources and matching remote manifest'
print(json.dumps({'version':version,'pages':30,'personal_photos':69,'approved_new_candidates':4,'museum_images':1,'pdf_pages':len(pdf.pages),'pdf_version_code':'30/30 OK','unassigned_replaced_photos':['S01','S05','S14','S18'],'personal_duplicates':0,'chronology':'OK (cover and inserted history/stat pages excluded)','image_decoding':'148/148 OK','static_html':'70/70 visual images','cover_origin_hash':'OK','ship_original':'full aspect ratio retained','map':'12 accessible map callouts and coastline share one SVG scene','public':remote},ensure_ascii=True))
