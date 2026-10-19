'use strict';
const DATA=window.JOURNAL;
const photoById=new Map(DATA.photos.map(p=>[p.id,p]));
const readingOrder=DATA.pages.flatMap(p=>p.photos);
const dialog=document.querySelector('#viewer'),viewImage=document.querySelector('#view-img'),stage=document.querySelector('.viewer-stage');
let current=0,scale=1,startX=null,pinch=null,hadPinch=false;
function showPhoto(index){
  current=(index+readingOrder.length)%readingOrder.length;
  const photo=photoById.get(readingOrder[current]);
  viewImage.src=photo.src;viewImage.alt=photo.alt;
  viewImage.onerror=()=>{viewImage.onerror=null;viewImage.src=photo.fallback};
  document.querySelector('#view-caption').textContent=`${current+1} / ${readingOrder.length} · ${photo.alt}`;
  scale=1;viewImage.style.transform='scale(1)';
  if(!dialog.open){dialog.showModal();document.body.classList.add('viewer-open')}
}
document.querySelectorAll('a[data-photo]').forEach(a=>a.addEventListener('click',event=>{
  if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  event.preventDefault();showPhoto(readingOrder.indexOf(a.dataset.photo));
}));
document.querySelector('.viewer-close').onclick=()=>dialog.close();
document.querySelector('.viewer-prev').onclick=()=>showPhoto(current-1);
document.querySelector('.viewer-next').onclick=()=>showPhoto(current+1);
dialog.addEventListener('close',()=>document.body.classList.remove('viewer-open'));
document.addEventListener('keydown',event=>{if(!dialog.open)return;if(event.key==='ArrowLeft')showPhoto(current-1);if(event.key==='ArrowRight')showPhoto(current+1)});
stage.addEventListener('wheel',event=>{event.preventDefault();scale=Math.max(1,Math.min(4,scale+(event.deltaY<0?.2:-.2)));viewImage.style.transform=`scale(${scale})`},{passive:false});
stage.addEventListener('touchstart',event=>{
  if(event.touches.length===1){startX=event.touches[0].clientX;hadPinch=false}
  if(event.touches.length===2){hadPinch=true;pinch=Math.hypot(event.touches[0].clientX-event.touches[1].clientX,event.touches[0].clientY-event.touches[1].clientY)}
},{passive:true});
stage.addEventListener('touchmove',event=>{
  if(event.touches.length!==2)return;event.preventDefault();
  const distance=Math.hypot(event.touches[0].clientX-event.touches[1].clientX,event.touches[0].clientY-event.touches[1].clientY);
  if(pinch)scale=Math.max(1,Math.min(4,scale+(distance-pinch)/180));pinch=distance;viewImage.style.transform=`scale(${scale})`;
},{passive:false});
stage.addEventListener('touchend',event=>{pinch=null;if(hadPinch||startX===null||scale!==1)return;const dx=event.changedTouches[0].clientX-startX;if(Math.abs(dx)>55)showPhoto(current+(dx<0?1:-1));startX=null});
document.querySelectorAll('.photo-frame img').forEach(img=>{
  function fallback(){img.closest('picture').querySelectorAll('source').forEach(s=>s.remove());img.removeEventListener('error',fallback);const item=photoById.get(img.closest('a').dataset.photo);img.src=item.fallback}
  img.addEventListener('error',fallback);if(img.complete&&img.naturalWidth===0)fallback();
});
document.querySelectorAll('.contents-links a').forEach(a=>a.addEventListener('click',()=>document.querySelector('.contents').removeAttribute('open')));
if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting)document.querySelector('.reading-progress').textContent=`${String(entry.target.dataset.page).padStart(2,'0')} / ${DATA.pages.length}`}),{rootMargin:'-10% 0px -35% 0px',threshold:.25});
  document.querySelectorAll('.journal-page').forEach(p=>observer.observe(p));
}
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
