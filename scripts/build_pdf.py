from pathlib import Path
import json, shutil
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from PIL import Image

repo=Path(__file__).resolve().parents[1]; site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Journal','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('JournalBold','C:/Windows/Fonts/arialbd.ttf'))
out=site/'greece-2026.pdf'; c=canvas.Canvas(str(out),pagesize=(540,840))
c.setTitle('Греція 2026');c.setAuthor('Греція 2026');c.setSubject('28 сторінок · 69 фотографій · 8–17 жовтня 2026')
for page in data['pages']:
    c.setFillColor(HexColor('#0d1117'));c.rect(0,0,540,840,fill=1,stroke=0)
    c.setFillColor(HexColor('#e8a23a'));c.setFont('JournalBold',9);c.drawString(30,805,f"ГРЕЦІЯ 2026  /  {page['page']:02} — 28")
    title=page['title'] if page['page']!=1 else 'Греція 2026'
    c.setFillColor(HexColor('#eef2f5'));c.setFont('JournalBold',24)
    title_lines=simpleSplit(title,'JournalBold',24,480)
    y=766
    for line in title_lines:c.drawString(30,y,line);y-=29
    caption=page['caption']
    if page['page']==1:caption='8–17 жовтня 2026 · Афіни та Мілос. '+caption
    c.setFillColor(HexColor('#adb8c3'));c.setFont('Journal',11)
    for line in simpleSplit(caption,'Journal',11,480):c.drawString(30,y-5,line);y-=16
    y-=25
    ids=page['photos']; n=len(ids)
    if not n:
        c.setFillColor(HexColor('#e8a23a'));c.rect(30,365,70,2,fill=1,stroke=0)
        text='Афіни → Мілос → берег → пором.' if page['page']==2 else 'Море вже чекає.'
        c.setFont('JournalBold',20);c.drawString(30,330,text)
    else:
        slot=(y-48-(n-1)*12)/n
        for ident in ids:
            photo=next(p for p in data['photos'] if p['id']==ident)
            path=site/photo['fallback']
            iw,ih=photo['width'],photo['height'];factor=min(480/iw,slot/ih)
            w,h=iw*factor,ih*factor
            c.drawImage(str(path),30+(480-w)/2,y-slot+(slot-h)/2,width=w,height=h)
            y-=slot+12
    c.setFont('Journal',8);c.setFillColor(HexColor('#9ca9b5'));c.drawString(30,22,'Афіни · Мілос · 8–17 жовтня 2026');c.drawRightString(510,22,str(page['page']))
    c.showPage()
c.save()
outputs=repo/'outputs';outputs.mkdir(exist_ok=True)
shutil.copy2(out,outputs/'greece-2026.pdf')
print(out, out.stat().st_size)

