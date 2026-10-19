"""Build the same 28 editorial pages as the static site. Requires Pillow/reportlab."""
from pathlib import Path
import json,os
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
by={p['id']:p for p in data['photos']}
c=canvas.Canvas(str(site/'greece-2026.pdf'),pagesize=(540,840),pageCompression=1,invariant=1)
c.setTitle('Греція 2026 — камінь, море, дорога');c.setAuthor('Греція 2026');c.setSubject('28 сторінок · 69 фотографій · редакційна версія 2')
def text(x,y,s,font,size,color):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def frame(ident,x,y,w,h,crop=False,label=True):
    photo=by[ident];labelheight=15 if label else 0;ih=h-labelheight
    c.setFillColor(HexColor('#14212d'));c.rect(x,y+labelheight,w,ih,fill=1,stroke=0)
    factor=(max if crop else min)(w/photo['width'],ih/photo['height'])
    dw,dh=photo['width']*factor,photo['height']*factor
    c.saveState();path=c.beginPath();path.rect(x,y+labelheight,w,ih);c.clipPath(path,stroke=0,fill=0)
    # Match the reader's framing; the original files remain available in the viewer.
    position=.2 if ident=='S43' else (.3 if ident=='S42' else .5)
    c.drawImage(str(site/photo['fallback']),x+(w-dw)*position,y+labelheight+(ih-dh)/2,width=dw,height=dh)
    c.restoreState()
    if label:text(x,y+2,photo['location'],'Body',8,'#aeb8ba')
for page in data['pages']:
    n=page['page'];c.setFillColor(HexColor('#101923'));c.rect(0,0,540,840,fill=1,stroke=0)
    text(26,799,page['section'].upper(),'Bold',9,'#dc8e6a')
    c.setFont('Body',9);c.setFillColor(HexColor('#aeb8ba'));c.drawRightString(514,799,page['date'])
    size=50 if n==1 else 27;title_lines=simpleSplit(page['title'],'Serif',size,488);top=760
    for line in title_lines:text(26,top,line,'Serif',size,'#f5f1e8');top-=size*1.12
    gallerytop=top+size*.15-15;bottom=110;height=gallerytop-bottom;gap=12
    ids=page['photos'];layout=page['layout']
    if layout in ['cover','solo']:frame(ids[0],26,bottom,488,height,True,layout!='cover')
    elif layout=='pair':
        hh=(height-gap)/2
        frame(ids[0],26,bottom+hh+gap,488,hh);frame(ids[1],26,bottom,488,hh)
    elif layout=='triptych':
        lower=(height-gap)/2.25;upper=lower*1.25;ww=(488-gap)/2
        frame(ids[0],26,bottom+lower+gap,488,upper)
        frame(ids[1],26,bottom,ww,lower,True);frame(ids[2],26+ww+gap,bottom,ww,lower,True)
    elif layout=='quartet':
        hh=(height-gap)/2;ww=(488-gap)/2
        for i,ident in enumerate(ids):frame(ident,26+(i%2)*(ww+gap),bottom+(1-i//2)*(hh+gap),ww,hh,True)
    c.setStrokeColor(HexColor('#c96a4b'));c.setLineWidth(2);c.line(26,91,514,91)
    caption_lines=simpleSplit(page['caption'],'Serif',13,420)
    for i,line in enumerate(caption_lines):text(26,66-i*18,line,'Serif',13,'#f5f1e8')
    text(467,42,f'{n:02} / 28','Body',10,'#d58a68');c.showPage()
c.save();print('PDF:',len(data['pages']),'pages;',len(data['photos']),'photos')
