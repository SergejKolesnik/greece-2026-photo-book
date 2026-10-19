const CACHE='greece-editorial-30-v3';
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('greece-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);
  if(event.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.endsWith('.pdf'))return;
  event.respondWith(fetch(event.request).then(async response=>{
    if(response.ok){try{const cache=await caches.open(CACHE);await cache.put(event.request,response.clone());const keys=await cache.keys();if(keys.length>190)await cache.delete(keys[0])}catch{}}
    return response;
  }).catch(()=>caches.match(event.request).then(response=>response||new Response('Немає з’єднання',{status:503}))));
});
