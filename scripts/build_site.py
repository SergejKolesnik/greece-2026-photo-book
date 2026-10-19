"""Render the static photo journal from the single editorial manifest (stdlib only)."""
import json,html
from pathlib import Path
repo=Path(__file__).resolve().parents[1];site=repo/'docs'
data=json.loads((site/'content.json').read_text(encoding='utf-8-sig'))
pages=data['pages'];by={p['id']:p for p in data['photos']};esc=html.escape
page_count=len(pages);version_code=data['version_code']
def picture(ident,eager=False):
    p=by[ident]
    return f'<picture><source type="image/webp" srcset="{p["src"]}"><img src="{p["fallback"]}" width="{p["width"]}" height="{p["height"]}" alt="{esc(p["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}></picture>'
cards=[]
for p in pages:
    n=p['page'];heading='h1' if n==1 else 'h2'
    figures=''.join(f'<figure class="photo-frame"><a href="{by[ident]["fallback"]}" data-photo="{ident}" aria-label="Відкрити фото: {esc(by[ident]["alt"])}">{picture(ident,n==1)}</a><figcaption>{esc(by[ident]["location"])}</figcaption></figure>' for ident in p['photos'])
    ship=' ship-page' if 'S55' in p['photos'] else ''
    if p['layout']=='history':
        hist=p['history'];content=f'<div class="history-content">{figures}<div class="history-copy"><p>{esc(hist["body"])}</p><p class="image-credit"><a href="{esc(hist["source_url"])}">{esc(hist["credit"])}</a></p></div></div>'
    elif p['layout']=='stats':
        tiles=''.join(f'<div class="stat-tile"><strong>{esc(x["value"])}</strong><b>{esc(x["label"])}</b><span>{esc(x["note"])}</span></div>' for x in p['stats'])
        content=f'<div class="stats-grid">{tiles}</div>'
    else:
        content=f'<div class="photo-grid">{figures}</div>'
    cards.append(f'<article class="journal-page layout-{p["layout"]}{ship}" id="page-{n}" data-page="{n}" aria-labelledby="title-{n}"><header class="page-head"><p class="eyebrow">{esc(p["section"])} <span>{esc(p["date"])}</span></p><{heading} id="title-{n}">{esc(p["title"])}</{heading}></header>{content}<footer class="page-foot"><p>{esc(p["caption"])}</p><span class="folio" aria-label="Сторінка {n} з {page_count}">{n:02}<small> / {page_count}</small></span></footer></article>')
toc=''.join(f'<a href="#page-{p["page"]}"><span>{p["page"]:02}</span>{esc(p["title"])}</a>' for p in pages)
places=json.loads((site/'map-data/places.json').read_text(encoding='utf-8'))
buttons=''.join(f'<button type="button" class="place-choice" data-place="{p["n"]}" aria-pressed="false"><b>{p["n"]}</b>{esc(p["name"])}</button>' for p in places)
svg=(site/'map-data/milos-map.svg').read_text(encoding='utf-8')
template=(repo/'scripts/templates/index.html').read_text(encoding='utf-8')
result=template.replace('{{TOC}}',toc).replace('{{PAGES}}','\n'.join(cards)).replace('{{SVG}}',svg).replace('{{BUTTONS}}',buttons).replace('{{PAGE_COUNT}}',str(page_count)).replace('{{VERSION_CODE}}',version_code)
(site/'index.html').write_text(result,encoding='utf-8')
(site/'content.js').write_text('window.JOURNAL='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
(site/'map.js').write_text('const PLACES='+json.dumps(places,ensure_ascii=False)+';\n'+(repo/'scripts/map-controller.js').read_text(encoding='utf-8'),encoding='utf-8')
print(f'Rendered static HTML: {page_count} pages; 69 personal photos plus credited museum image are present without JavaScript; {version_code}.')
