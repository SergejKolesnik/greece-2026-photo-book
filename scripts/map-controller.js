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
