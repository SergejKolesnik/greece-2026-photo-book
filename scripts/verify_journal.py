"""Check editorial completeness, duplicate assets, image decoding and SVG topology.

Optional: --url https://.../ checks the actual deployed files without authentication.
"""
import argparse,csv,hashlib,json,concurrent.futures,urllib.request,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
repo=Path(__file__).resolve().parents[1];site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8-sig'))
photos={p['id']:p for p in data['photos']};pages=data['pages']
assert len(pages)==28 and [p['page'] for p in pages]==list(range(1,29))
flat=[ident for p in pages for ident in p['photos']]
assert len(flat)==69 and set(flat)=={f'S{i:02}' for i in range(1,70)} and len(set(flat))==69
assert all(p['photos'] and p['caption'] and p['date'] and p['location'] for p in pages)
assert [photos[x]['date'] for p in pages[1:] for x in p['photos']]==sorted(photos[x]['date'] for p in pages[1:] for x in p['photos'])
assert pages[-2]['photos']==['S64','S65','S66'] and pages[-1]['photos']==['S67','S68','S69']
hashes=[]
for p in photos.values():
    for key in ['src','fallback']:
        file=site/p[key];assert file.exists(),file
        with Image.open(file) as image:assert image.size==(p['width'],p['height']) and not image.getexif();image.verify()
    hashes.append(hashlib.sha256((site/p['fallback']).read_bytes()).hexdigest())
assert len(set(hashes))==69
class JournalParser(HTMLParser):
    def __init__(self):super().__init__();self.articles=[];self.current=None;self.imgs=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and 'data-page' in a:self.current={'page':int(a['data-page']),'photos':[]};self.articles.append(self.current)
        if tag=='a' and 'data-photo' in a:self.current['photos'].append(a['data-photo'])
        if tag=='img':self.imgs.append(a)
        assert tag!='iframe','Reader must use the self-hosted SVG, not an independent map iframe'
    def handle_endtag(self,tag):
        if tag=='article':self.current=None
    def handle_data(self,data):self.text.append(data)
parser=JournalParser();parser.feed((site/'index.html').read_text(encoding='utf-8-sig'))
assert parser.articles==[{'page':p['page'],'photos':p['photos']} for p in pages]
reader=' '.join(parser.text).lower()
assert not any(term in reader for term in ['gps','одометр','трек','маршрутних даних'])
svg=ET.fromstring((site/'map-data/milos-map.svg').read_text(encoding='utf-8'))
scene=next(el for el in svg if el.attrib.get('class')=='map-scene')
assert len([el for el in scene if el.attrib.get('class')=='island-coast'])==1
pins=[el for el in scene if el.attrib.get('class')=='map-pin'];assert len(pins)==9
assert {int(el.attrib['data-place']) for el in pins}==set(range(1,10))
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
    remote=f'OK: {len(paths)} HTTPS resources and deployed manifest'
    report=list(csv.DictReader((repo/'PAGE_AUDIT.csv').open(encoding='utf-8-sig')))
    for row in report:row['public_loading']='OK: WebP + JPEG, HTTPS 200, exact size'
    with (repo/'PAGE_AUDIT.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=report[0].keys());w.writeheader();w.writerows(report)
print(json.dumps({'pages':28,'photos':69,'empty_pages':0,'duplicates':0,'chronology':'OK (cover excluded)','image_decoding':'138/138 OK','static_html':'69/69 images','map':'9 pins and coastline share SVG scene','public':remote},ensure_ascii=True))
