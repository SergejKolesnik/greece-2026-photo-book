'use strict';
const data=window.JOURNAL;
const journal=document.querySelector('#journal'),toc=document.querySelector('#toc');
const all=data.photos;
let current=0,scale=1,startX=0,pinch=null;
data.pages.filter(p=>p.page!==1).forEach(p=>{
  const sec=document.createElement('section');sec.className='chapter';sec.id=`page-${p.page}`;
  const head=document.createElement('div');head.className='chapter-head';
  const title=document.createElement('h2');title.textContent=p.title;
  const number=document.createElement('span');number.className='chapter-date';number.textContent=`${String(p.page).padStart(2,'0')} / 28 · ${p.section}`;
  head.append(title,number);sec.append(head);
  const caption=document.createElement('p');caption.className='lead';caption.textContent=p.caption;sec.append(caption);
  const gallery=document.createElement('div');gallery.className='gallery';
  p.photos.forEach(id=>{
    const item=all.find(x=>x.id===id),figure=document.createElement('figure');figure.className='card';
    const button=document.createElement('button');button.className='photo-button';button.type='button';button.setAttribute('aria-label',`Відкрити фото: ${p.title}`);
    const img=document.createElement('img');img.src=item.src;img.alt=p.title;img.loading='lazy';img.decoding='async';img.width=item.width;img.height=item.height;
    img.onerror=()=>{img.onerror=null;img.src=item.fallback};button.append(img);button.onclick=()=>{current=all.findIndex(x=>x.id===id);show()};figure.append(button);gallery.append(figure);
  });sec.append(gallery);journal.append(sec);
  if(p.page===2||data.pages[p.page-2].section!==p.section){const a=document.createElement('a');a.href=`#${sec.id}`;a.textContent=p.section;toc.append(a)}
});
const viewer=document.querySelector('#viewer'),viewImg=document.querySelector('#view-img'),zoom=document.querySelector('.zoom');
function show(){const x=all[current];viewImg.src=x.src;viewImg.onerror=()=>{viewImg.onerror=null;viewImg.src=x.fallback};const page=data.pages.find(p=>p.photos.includes(x.id));viewImg.alt=page.title;document.querySelector('#view-caption').textContent=`${current+1} / 69 · ${page.title}`;if(!viewer.open)viewer.showModal();scale=1;viewImg.style.transform='scale(1)'}
function move(delta){current=(current+delta+all.length)%all.length;show()}
document.querySelector('.close').onclick=()=>viewer.close();document.querySelector('.prev').onclick=()=>move(-1);document.querySelector('.next').onclick=()=>move(1);
document.querySelector('.start').onclick=()=>journal.scrollIntoView();document.querySelector('#theme').onclick=()=>document.body.classList.toggle('light');
zoom.addEventListener('wheel',e=>{e.preventDefault();scale=Math.max(1,Math.min(4,scale+(e.deltaY<0?.25:-.25)));viewImg.style.transform=`scale(${scale})`},{passive:false});
zoom.addEventListener('touchstart',e=>{if(e.touches.length===1)startX=e.touches[0].clientX;if(e.touches.length===2){pinch=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY)}},{passive:true});
zoom.addEventListener('touchmove',e=>{if(e.touches.length!==2)return;e.preventDefault();const dist=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);if(pinch)scale=Math.max(1,Math.min(4,scale+(dist-pinch)/180));pinch=dist;viewImg.style.transform=`scale(${scale})`},{passive:false});
zoom.addEventListener('touchend',e=>{if(pinch){pinch=null;return}if(scale===1&&e.changedTouches.length===1){const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>55)move(dx<0?1:-1)}});
document.addEventListener('keydown',e=>{if(!viewer.open)return;if(e.key==='ArrowLeft')move(-1);if(e.key==='ArrowRight')move(1)});
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
