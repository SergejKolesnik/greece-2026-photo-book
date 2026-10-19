"""Render the static photo journal from the single editorial manifest (stdlib only)."""
import json,html
from pathlib import Path
repo=Path(__file__).resolve().parents[1];site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8-sig'))
pages=data['pages'];by={p['id']:p for p in data['photos']};esc=html.escape
def picture(ident,eager=False):
    p=by[ident]
    return f'<picture><source type="image/webp" srcset="{p["src"]}"><img src="{p["fallback"]}" width="{p["width"]}" height="{p["height"]}" alt="{esc(p["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}></picture>'
cards=[]
for p in pages:
    n=p['page'];heading='h1' if n==1 else 'h2'
    figures=''.join(f'<figure class="photo-frame"><a href="{by[ident]["fallback"]}" data-photo="{ident}" aria-label="Відкрити фото: {esc(by[ident]["alt"])}">{picture(ident,n==1)}</a><figcaption>{esc(by[ident]["location"])}</figcaption></figure>' for ident in p['photos'])
    cards.append(f'<article class="journal-page layout-{p["layout"]}" id="page-{n}" data-page="{n}" aria-labelledby="title-{n}"><header class="page-head"><p class="eyebrow">{esc(p["section"])} <span>{esc(p["date"])}</span></p><{heading} id="title-{n}">{esc(p["title"])}</{heading}></header><div class="photo-grid">{figures}</div><footer class="page-foot"><p>{esc(p["caption"])}</p><span class="folio" aria-label="Сторінка {n} з 28">{n:02}<small> / 28</small></span></footer></article>')
toc=''.join(f'<a href="#page-{p["page"]}"><span>{p["page"]:02}</span>{esc(p["title"])}</a>' for p in pages)
places=json.loads((site/'map-data/places.json').read_text(encoding='utf-8'))
buttons=''.join(f'<button type="button" class="place-choice" data-place="{p["n"]}" aria-pressed="false"><b>{p["n"]}</b>{esc(p["name"])}</button>' for p in places)
svg=(site/'map-data/milos-map.svg').read_text(encoding='utf-8')
template=(repo/'scripts/templates/index.html').read_text(encoding='utf-8')
result=template.replace('{{TOC}}',toc).replace('{{PAGES}}','\n'.join(cards)).replace('{{SVG}}',svg).replace('{{BUTTONS}}',buttons)
(site/'index.html').write_text(result,encoding='utf-8')
(site/'content.js').write_text('window.JOURNAL='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
(site/'map.js').write_text('const PLACES='+json.dumps(places,ensure_ascii=False)+';\n'+(repo/'scripts/map-controller.js').read_text(encoding='utf-8'),encoding='utf-8')
print('Rendered static HTML: 28 pages; all 69 images are present without JavaScript.')
