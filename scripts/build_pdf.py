"""Build the PDF edition from the same page and photo manifest as the site."""
from pathlib import Path
import json, os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor

repo=Path(__file__).resolve().parents[1];site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8-sig'))
fontdir=Path(os.environ.get('JOURNAL_FONT_DIR','C:/Windows/Fonts'))
pdfmetrics.registerFont(TTFont('Body',str(fontdir/'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(fontdir/'segoeuib.ttf')))
pdfmetrics.registerFont(TTFont('Serif',str(fontdir/'georgia.ttf')))
by={p['id']:p for p in data['photos']};version=data['version_code'];count=len(data['pages'])
c=canvas.Canvas(str(site/'greece-2026.pdf'),pagesize=(540,840),pageCompression=1,invariant=1)
c.setTitle(f'Греція 2026 — редакція {version}')
c.setAuthor('Греція 2026');c.setSubject(f'{count} сторінок · 69 особистих фото · 1 музейне зображення · {version}')
def text(x,y,s,font,size,color):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def frame(ident,x,y,w,h,crop=False,label=True):
    photo=by[ident];labelheight=15 if label else 0;ih=h-labelheight
    c.setFillColor(HexColor('#14212d'));c.rect(x,y+labelheight,w,ih,fill=1,stroke=0)
    factor=(max if crop else min)(w/photo['width'],ih/photo['height'])
    dw,dh=photo['width']*factor,photo['height']*factor
    c.saveState();path=c.beginPath();path.rect(x,y+labelheight,w,ih);c.clipPath(path,stroke=0,fill=0)
    c.drawImage(str(site/photo['fallback']),x+(w-dw)/2,y+labelheight+(ih-dh)/2,width=dw,height=dh)
    c.restoreState()
    if label:text(x,y+2,photo['location'],'Body',8,'#aeb8ba')
def footer(page,caption,top):
    c.setStrokeColor(HexColor('#c96a4b'));c.setLineWidth(2);c.line(26,91,514,91)
    lines=simpleSplit(caption,'Serif',13,420)
    for i,line in enumerate(lines[:2]):text(26,66-i*18,line,'Serif',13,'#f5f1e8')
    text(370,43,version,'Bold',7,'#aeb8ba')
    c.setFillColor(HexColor('#d58a68'));c.setFont('Body',10);c.drawRightString(514,43,f'{page:02} / {count}')
for page in data['pages']:
    n=page['page'];layout=page['layout'];ids=page['photos']
    c.setFillColor(HexColor('#101923'));c.rect(0,0,540,840,fill=1,stroke=0)
    text(26,799,page['section'].upper(),'Bold',9,'#dc8e6a')
    c.setFont('Body',9);c.setFillColor(HexColor('#aeb8ba'));c.drawRightString(514,799,page['date'])
    size=50 if n==1 else 27;title_lines=simpleSplit(page['title'],'Serif',size,488);top=760
    for line in title_lines:text(26,top,line,'Serif',size,'#f5f1e8');top-=size*1.12
    gallerytop=top+size*.15-15;bottom=110;height=gallerytop-bottom;gap=12
    if layout=='cover':frame(ids[0],26,bottom,488,height,True,False)
    elif 'S55' in ids:frame('S55',26,bottom,488,height,False,True)
    elif layout=='history':
        hist=page['history'];leftw=187;frame(ids[0],26,bottom,leftw,height,False,False)
        x=228;y=gallerytop-10
        for para in hist['body'].split('. '):
            lines=simpleSplit(para.strip(), 'Body',12,286)
            for line in lines:text(x,y,line,'Body',12,'#f5f1e8');y-=18
            y-=8
        credit=simpleSplit(hist['credit'],'Body',8,286)
        for line in credit:text(x,y,line,'Body',8,'#aeb8ba');y-=12
        text(x,y-7,'Wikimedia Commons · сторінка зображення','Body',7,'#d9a184')
        c.linkURL(hist['source_url'],(x,y-10,x+220,y+4),relative=0)
    elif layout=='stats':
        stats=page['stats'];cols=2;gapx=10;gapy=10;tilew=(488-gapx)/2;tileh=min(112,(height-(len(stats)//2)*gapy)/(len(stats)//2+1))
        for i,item in enumerate(stats):
            col=i%2;row=i//2;x=26+col*(tilew+gapx);y=gallerytop-(row+1)*tileh-row*gapy
            c.setFillColor(HexColor('#172532'));c.roundRect(x,y,tilew,tileh,5,fill=1,stroke=0)
            text(x+12,y+tileh-28,item['value'],'Serif',22,'#dc8e6a')
            text(x+12,y+tileh-48,item['label'],'Bold',9,'#f5f1e8')
            for j,line in enumerate(simpleSplit(item['note'],'Body',7.5,tilew-24)[:2]):text(x+12,y+tileh-64-j*11,line,'Body',7.5,'#aeb8ba')
    elif layout=='solo':frame(ids[0],26,bottom,488,height,True,True)
    elif layout=='pair':
        hh=(height-gap)/2;frame(ids[0],26,bottom+hh+gap,488,hh);frame(ids[1],26,bottom,488,hh)
    elif layout=='triptych':
        lower=(height-gap)/2.25;upper=lower*1.25;ww=(488-gap)/2
        frame(ids[0],26,bottom+lower+gap,488,upper)
        frame(ids[1],26,bottom,ww,lower,True);frame(ids[2],26+ww+gap,bottom,ww,lower,True)
    elif layout=='photo-story':
        ww=(488-gap)*.48;right=488-ww-gap;hh=(height-gap)/2
        frame(ids[0],26,bottom,ww,height,False)
        frame(ids[1],26+ww+gap,bottom+hh+gap,right,hh,False)
        frame(ids[2],26+ww+gap,bottom,right,hh,False)
    elif layout=='quartet':
        hh=(height-gap)/2;ww=(488-gap)/2
        for i,ident in enumerate(ids):frame(ident,26+(i%2)*(ww+gap),bottom+(1-i//2)*(hh+gap),ww,hh,True)
    else:raise ValueError(f'Unsupported layout on page {n}: {layout}')
    footer(n,page['caption'],gallerytop);c.showPage()
c.save()
print(f'PDF: {count} pages; 69 personal photos; version {version}')
