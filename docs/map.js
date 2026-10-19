(() => {
  const places = [
    {n:1,name:'Адамас',date:'9–10 жовтня',day:'10',x:44,y:58,note:'Прибуття на Мілос, порт, перший ранок і вечірнє світло.'},
    {n:2,name:'Палеохорі',date:'11 жовтня',day:'11',x:70,y:77,note:'Південний берег: червоні схили й відкрита лінія моря.'},
    {n:3,name:'Проватас',date:'11 жовтня',day:'11',x:40,y:79,note:'Південний берег: бухта й спокійний перехід між локаціями.'},
    {n:4,name:'Фіріплака',date:'11 жовтня',day:'11',x:48,y:74,note:'Південний берег: довга пляжна лінія та кольорові скелі.'},
    {n:5,name:'Плака / Кастро',date:'12 жовтня',day:'12',x:30,y:50,note:'Вечірній підйом над островом і захід сонця.'},
    {n:6,name:'Кліма',date:'12 жовтня',day:'12',x:28,y:55,note:'Човнові гаражі над морем; поруч — пам’ять про античний Мілос.'},
    {n:7,name:'Поллонія',date:'13 жовтня',day:'13',x:76,y:22,note:'Східне узбережжя, рибальський ритм і відкритий горизонт.'},
    {n:8,name:'Мандракія',date:'14 жовтня',day:'14',x:67,y:33,note:'Човни, кольорові двері й повільний ритм північного берега.'},
    {n:9,name:'Саракініко',date:'14 жовтня',day:'14',x:57,y:36,note:'Білі вулканічні скелі, ландшафт і вода; маршрутних ліній немає.'}
  ];
  const markers = document.querySelector('#map-markers');
  const details = document.querySelector('#map-details');
  const filter = document.querySelector('#map-day-filter');
  if (!markers || !details || !filter) return;

  if (new URLSearchParams(location.search).get('map') === '1') {
    document.querySelectorAll('body > *:not(.real-map)').forEach(el => el.style.display = 'none');
    document.body.style.padding = '0';
    document.querySelector('.real-map').style.margin = '0 auto';
  }
  const showDetails = (items) => {
    details.innerHTML = items.map(p => `<article class="map-detail-card"><div class="map-detail-number">${p.n}</div><div><h3>${p.name}</h3><p class="map-detail-meta">${p.date}</p><p>${p.note}</p></div></article>`).join('');
  };
  const draw = () => {
    const selected = filter.value;
    const visible = places.filter(p => selected === 'all' || p.day === selected);
    markers.innerHTML = '';
    const clustered = selected === 'all' || selected === '12';
    visible.forEach(p => {
      if (clustered && p.n === 6) return;
      const isCluster = clustered && p.n === 5;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = isCluster ? 'map-pin map-cluster' : 'map-pin';
      btn.style.left = `${p.x}%`; btn.style.top = `${p.y}%`;
      btn.setAttribute('aria-label', isCluster ? 'Маркери 5 і 6: Плака / Кастро та Кліма' : `${p.n}. ${p.name}`);
      btn.textContent = isCluster ? '5·6' : p.n;
      btn.addEventListener('click', () => showDetails(isCluster ? places.filter(x => x.n === 5 || x.n === 6) : [p]));
      markers.appendChild(btn);
    });
    if (!visible.length) details.innerHTML = '<p class="map-details-empty">Для цього дня підтверджених точок у редакційній хронології немає.</p>';
  };
  filter.addEventListener('change', draw);
  draw();
})();
