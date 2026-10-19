const PLACES=[{"n": 1, "name": "Адамас", "node": 287555072, "date": "9–17 жовтня", "note": "Порт, вечірні повернення й початок дороги додому.", "lon": 24.4472119, "lat": 36.726262, "source": "https://www.openstreetmap.org/node/287555072", "x": 498.426, "y": 270.613, "labelX": 513.426, "labelY": 300.613}, {"n": 2, "name": "Палеохорі", "node": 1839036912, "date": "11, 13 і 16 жовтня", "note": "Кольорові породи південного берега. Повернулися за деталями, а потім — попрощатися.", "lon": 24.5177401, "lat": 36.6761335, "source": "https://www.openstreetmap.org/node/1839036912", "x": 730.322, "y": 476.209, "labelX": 761.322, "labelY": 504.209}, {"n": 3, "name": "Проватас", "node": 1839034323, "date": "12 жовтня", "note": "Відкрита бухта й довга смуга прибою.", "lon": 24.4464817, "lat": 36.6706924, "source": "https://www.openstreetmap.org/node/1839034323", "x": 496.025, "y": 498.525, "labelX": 471.025, "labelY": 528.525}, {"n": 4, "name": "Фіріплака", "lon": 24.4655, "lat": 36.6653, "date": "11 жовтня", "note": "Бірюзова вода під світлими скелями.", "source": "selected photo cluster VI184/194/201", "x": 558.557, "y": 520.642, "labelX": 584.557, "labelY": 562.642}, {"n": 5, "name": "Плака / Кастро", "node": 2928336197, "date": "10 жовтня", "note": "Білі вулиці й захід сонця над островом.", "lon": 24.4217785, "lat": 36.7457433, "source": "https://www.openstreetmap.org/node/2928336197", "x": 414.801, "y": 190.713, "labelX": 379.801, "labelY": 164.713}, {"n": 6, "name": "Кліма", "node": 1832731828, "date": "12 жовтня", "note": "Над узбережжям Кліми — античний театр і кам’яні деталі.", "lon": 24.4202219, "lat": 36.7352417, "source": "https://www.openstreetmap.org/node/1832731828", "x": 409.683, "y": 233.784, "labelX": 364.683, "labelY": 239.784}, {"n": 7, "name": "Поллонія", "node": 287555071, "date": "14 жовтня", "note": "Північно-східний берег, білі будинки й море з характером.", "lon": 24.5261626, "lat": 36.7626404, "source": "https://www.openstreetmap.org/node/287555071", "x": 758.015, "y": 121.412, "labelX": 795.015, "labelY": 107.412}, {"n": 8, "name": "Мандракія", "node": 1841078177, "date": "14 жовтня", "note": "Маленька бухта з кольоровими дверима човнових гаражів.", "lon": 24.4462174, "lat": 36.7500176, "source": "https://www.openstreetmap.org/node/1841078177", "x": 495.156, "y": 173.183, "labelX": 490.156, "labelY": 136.183}, {"n": 9, "name": "Саракініко", "lon": 24.455, "lat": 36.7461, "date": "10, 14 і 16 жовтня", "note": "Перша зустріч, повернення до білих скель і останній погляд перед від’їздом.", "source": "selected photo cluster VI421/428/432/434", "x": 524.033, "y": 189.25, "labelX": 559.033, "labelY": 177.25}];
let mapZoom=1;
const mapSvg=document.querySelector('#milos-map');
const details=document.querySelector('#map-details');
function selectPlace(number){
 const place=PLACES.find(p=>p.n===Number(number));if(!place)return;
 document.querySelectorAll('[data-place]').forEach(el=>el.setAttribute('aria-pressed',String(Number(el.dataset.place)===place.n)));
 const heading=document.createElement('h3');heading.textContent=`${place.n}. ${place.name}`;
 const date=document.createElement('p');date.className='place-date';date.textContent=place.date;
 const note=document.createElement('p');note.textContent=place.note;
 details.replaceChildren(heading,date,note);
}
document.querySelectorAll('[data-place]').forEach(el=>{
 el.addEventListener('click',()=>selectPlace(el.dataset.place));
 if(el.tagName.toLowerCase()==='g')el.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectPlace(el.dataset.place)}});
});
function drawZoom(){
 const width=900/mapZoom,height=680/mapZoom;
 const centerX=mapZoom===1?450:565,centerY=mapZoom===1?340:340;
 mapSvg.setAttribute('viewBox',`${centerX-width/2} ${centerY-height/2} ${width} ${height}`);
 document.querySelector('#map-zoom-in').disabled=mapZoom>=2.25;
 document.querySelector('#map-zoom-out').disabled=mapZoom<=1;
}
document.querySelector('#map-zoom-in').onclick=()=>{mapZoom=Math.min(2.25,mapZoom*1.5);drawZoom()};
document.querySelector('#map-zoom-out').onclick=()=>{mapZoom=Math.max(1,mapZoom/1.5);drawZoom()};
document.querySelector('#map-reset').onclick=()=>{mapZoom=1;drawZoom()};
drawZoom();
if(new URLSearchParams(location.search).get('map')==='1'){
 document.querySelector('.reader-bar').hidden=true;document.querySelector('#journal').hidden=true;document.querySelector('.site-footer').hidden=true;
 document.querySelector('#island').style.marginTop='24px';
}
