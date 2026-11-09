
function openLightbox(img) {
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  lightboxImg.src = img.src;
  lightboxImg.alt = img.alt;
  lightbox.classList.add('active');
}

function closeLightbox() {
  const lightbox = document.getElementById('lightbox');
  lightbox.classList.remove('active');
}

document.getElementById('lightbox').addEventListener('click', function(e) {
  if (e.target === this) {
    closeLightbox();
  }
});

// --- мобильное меню: закрытие по клику на пункт и вне меню ---
function toggleNav(e){
  if(e) e.stopPropagation();
  document.getElementById('navlinks').classList.toggle('open');
}
document.addEventListener('click', function(e){
  var nav = document.getElementById('navlinks');
  var burger = document.querySelector('.burger');
  if(!nav || !nav.classList.contains('open')) return;
  // клик по ссылке внутри меню -> закрыть
  if(e.target.closest('#navlinks a')){ nav.classList.remove('open'); return; }
  // клик вне меню и не по бургеру -> закрыть
  if(!nav.contains(e.target) && e.target!==burger){ nav.classList.remove('open'); }
});


(function(){
  try{
    if(localStorage.getItem('lf_age_ok')==='1') return;
  }catch(e){}
  var g=document.getElementById('age-gate');
  if(g){g.classList.remove('hidden');document.body.style.overflow='hidden';}
})();
function ageConfirm(){
  try{localStorage.setItem('lf_age_ok','1');}catch(e){}
  var g=document.getElementById('age-gate');
  if(g){g.classList.add('hidden');document.body.style.overflow='';}
}
function ageDeny(){
  window.location.href='https://maps.app.goo.gl/pfJ5txVBgmuriNQh9';
}


(function(){var lb=document.getElementById("posterLB");if(!lb)return;var c=lb.querySelector(".poster-lb-close");var im=lb.querySelector(".poster-lb-img");function O(u){im.src=u;lb.classList.add("open");lb.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";}window.__lfOpen=O;function o(el){var p=el.getAttribute("data-poster");if(p){O(p);}else{lb.classList.add("open");lb.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";}}function x(){lb.classList.remove("open");lb.setAttribute("aria-hidden","true");document.body.style.overflow="";}document.querySelectorAll("[data-poster]").forEach(function(el){el.addEventListener("click",function(){o(el);});el.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();o(el);}});});c.addEventListener("click",x);lb.addEventListener("click",function(e){if(e.target===lb)x();});document.addEventListener("keydown",function(e){if(e.key==="Escape")x();});})();


(function(){var nav=document.getElementById("menuNav");if(nav){nav.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){var d=document.getElementById(a.getAttribute("data-cat"));if(d)d.open=true;});});if("IntersectionObserver" in window){var ob=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){nav.querySelectorAll("a").forEach(function(x){x.classList.toggle("active",x.getAttribute("data-cat")===e.target.id);});}});},{rootMargin:"-110px 0px -72% 0px"});document.querySelectorAll(".menu-cat").forEach(function(d){ob.observe(d);});}}var now=new Date();now.setHours(0,0,0,0);var pl=document.querySelector(".past-list");document.querySelectorAll(".upcoming .uc, .upcoming .evt-banner").forEach(function(el){var dn=el.querySelector(".uc-date");if(!dn||!pl)return;var mm=dn.textContent.trim().match(/(\d{2})\.(\d{2})/);if(!mm)return;var d=new Date(now.getFullYear(),+mm[2]-1,+mm[1]);d.setHours(0,0,0,0);if(d<now){el.style.display="none";var pp=el.getAttribute("data-poster")||"";var nm=pp?"<div class=\"past-name past-link\" data-poster=\""+pp+"\" role=\"button\" tabindex=\"0\">LOST PARTY</div>":"<div class=\"past-name\">LOST PARTY</div>";var it=document.createElement("div");it.className="past-item";it.innerHTML="<div class=\"past-date\">"+mm[1]+"."+mm[2]+"</div><div class=\"past-info\">"+nm+"<div class=\"past-desc\">LEX MIRA \u00b7 SH\u00d8GUN</div></div>";var ln=it.querySelector(".past-link");if(ln&&window.__lfOpen)ln.addEventListener("click",function(){window.__lfOpen(pp);});pl.insertBefore(it,pl.firstChild);}});})();

(function(){var b=document.getElementById("peMore"),o=document.getElementById("peOlder");if(!b||!o)return;b.addEventListener("click",function(){o.classList.add("pe-open");b.style.display="none";});})();
(function(){function t(n,p){try{if(typeof gtag==='function')gtag('event',n,p||{});}catch(e){}}document.querySelectorAll('a[href*="resmio.com"]').forEach(function(a){a.addEventListener('click',function(){t('reserve_click',{location:(a.className||'link').trim()});});});document.querySelectorAll('a[href="#finder"]').forEach(function(a){a.addEventListener('click',function(){t('finder_open',{source:(a.className||'link').trim()});});});document.querySelectorAll('[data-poster]').forEach(function(el){el.addEventListener('click',function(){t('poster_open',{poster:el.getAttribute('data-poster')});});});})();
(function(){try{var p=location.pathname;var onCS=/^\/cs(\/|$)/.test(p),onDE=/^\/de(\/|$)/.test(p),onUA=/^\/ua(\/|$)/.test(p);var L=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']).map(function(s){return(s||'').toLowerCase();});var wDE=L.some(function(l){return l.indexOf('de')===0;}),wCS=L.some(function(l){return l.indexOf('cs')===0||l.indexOf('cz')===0;}),wUK=L.some(function(l){return l.indexOf('uk')===0;});var t=null;if(wUK&&!onUA)t={h:'/ua/',x:'🇺🇦 Переглянути цю сторінку українською →',k:'uk'};else if(wDE&&!onDE)t={h:'/de/',x:'🇩🇪 Diese Seite auf Deutsch anzeigen →',k:'de'};else if(wCS&&!onCS)t={h:'/cs/',x:'🇨🇿 Zobrazit tuto stránku česky →',k:'cs'};if(!t)return;try{if(localStorage.getItem('lf-lh-'+t.k)==='1')return;}catch(e){}var b=document.createElement('div');b.id='lf-lang-bar';var a=document.createElement('a');a.href=t.h;a.textContent=t.x;var c=document.createElement('button');c.className='lf-x';c.setAttribute('aria-label','Close');c.textContent='×';c.onclick=function(){b.parentNode&&b.parentNode.removeChild(b);try{localStorage.setItem('lf-lh-'+t.k,'1');}catch(e){}};b.appendChild(a);b.appendChild(c);document.body.insertBefore(b,document.body.firstChild);}catch(e){}})();
/* open-now status (v1.29). Hours: Su-Tu 18-00, We-Th 17-01, Fr-Sa 17-03 (Europe/Prague) */
(function(){try{
var el=document.getElementById('scStatus');if(!el)return;
var H={0:[18,24],1:[18,24],2:[18,24],3:[17,25],4:[17,25],5:[17,27],6:[17,27]};
var L=(document.documentElement.lang||'en').slice(0,2);
var T={en:{o:'Open now · till ',s:'Closing soon · till ',c:'Closed · opens ',t:'today ',m:'tomorrow '},
cs:{o:'Otevřeno · do ',s:'Brzy zavíráme · do ',c:'Zavřeno · otevíráme ',t:'dnes v ',m:'zítra v '},
de:{o:'Jetzt geöffnet · bis ',s:'Schließt bald · bis ',c:'Geschlossen · öffnet ',t:'heute ',m:'morgen '},
uk:{o:'Відчинено · до ',s:'Скоро зачиняємось · до ',c:'Зачинено · відчиняємось ',t:'сьогодні о ',m:'завтра о '}}[L]||null;
if(!T)T={o:'Open now · till ',s:'Closing soon · till ',c:'Closed · opens ',t:'today ',m:'tomorrow '};
function hh(h){h=h%24;return(h<10?'0':'')+h+':00';}
function upd(){
 var p=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Prague',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date());
 var g={};p.forEach(function(x){g[x.type]=x.value;});
 var d=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(g.weekday),t=(+g.hour%24)+(+g.minute)/60;
 var y=(d+6)%7,cls,txt,cl=null;
 if(t<H[y][1]-24){cl=H[y][1];}            /* after midnight, still yesterday's shift */
 else if(t>=H[d][0]){cl=H[d][1];}
 if(cl!==null){var left=(cl>=24&&t<H[d][0]?cl-24:cl)-t;cls=left<=1?'soon':'open';txt=(left<=1?T.s:T.o)+hh(cl);}
 else{cls='closed';txt=T.c+(t<H[d][0]?T.t+hh(H[d][0]):T.m+hh(H[(d+1)%7][0]));}
 el.className='sc-status on '+cls;el.innerHTML='<i></i>';el.appendChild(document.createTextNode(txt));
}
upd();setInterval(upd,60000);
}catch(e){}})();
