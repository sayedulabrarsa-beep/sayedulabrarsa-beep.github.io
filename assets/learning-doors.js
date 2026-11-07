(function(){
'use strict';
var host=document.getElementById('ldDoors');
var rows=[].slice.call(document.querySelectorAll('.course-row'));
if(!host||!rows.length)return;
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var MON={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
function parseDate(t){var m=/(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})/.exec(t||'');return m?new Date(+m[3],MON[m[2]],+m[1]):null}
function svg(d){return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+d+'</svg>'}
var ICONS=[
 [/^AI/,svg('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 12h4"/>')],
 [/Pharma/,svg('<g transform="rotate(-45 12 12)"><rect x="2" y="8" width="20" height="8" rx="4"/><path d="M12 8v8"/></g>')],
 [/Marketing/,svg('<path d="M3 11v3a1 1 0 001 1h2l7 4V6L6 10H4a1 1 0 00-1 1z"/><path d="M16 9a4 4 0 010 6M18.5 6.5a8 8 0 010 11"/>')],
 [/Data/,svg('<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>')],
 [/Design/,svg('<path d="M12 20l7-7-4-4-7 7v4z"/><path d="M14 8l2-2a2.1 2.1 0 013 3l-2 2"/>')],
 [/Leadership/,svg('<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.5a3 3 0 010 5.5M18 14.3c2 .8 3.5 2.8 3.5 5.2"/>')],
 [/Project/,svg('<rect x="3" y="4" width="5" height="16" rx="1.2"/><rect x="10" y="4" width="5" height="10" rx="1.2"/><rect x="17" y="4" width="4" height="13" rx="1.2"/>')],
 [/Health/,svg('<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.4A4 4 0 0119 10c0 5.6-7 10-7 10z"/>')],
 [/Sales/,svg('<path d="M3 4h2l2.2 10.2a1 1 0 001 .8h8.6a1 1 0 001-.8L20 8H6"/><circle cx="9" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/>')]
];
var DEF=svg('<path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/>');
function icon(n){for(var i=0;i<ICONS.length;i++)if(ICONS[i][0].test(n))return ICONS[i][1];return DEF}
var COLORS=[['#e39a2d','#9a5200'],['#2fa39a','#145f66'],['#7a6ff0','#403a9e'],['#e0675a','#9b2f2f'],['#4f9be0','#215a99'],['#c26ec9','#7a3a86'],['#5bb06a','#2c6d3b'],['#e0a52d','#8a6205'],['#d9706e','#8c3a52']];
var groups={},order=[];
rows.forEach(function(r){
  var c=r.getAttribute('data-category');if(!c)return;
  if(!groups[c]){groups[c]={name:c,items:[],providers:{}};order.push(c)}
  var g=groups[c],dEl=r.querySelector('.date');
  g.items.push({title:(r.querySelector('h3')||{}).textContent||'',date:parseDate(dEl&&dEl.textContent),dateText:(dEl&&dEl.textContent||'').replace(/^Learning path ·\s*/,'').replace(/^Completed\s*/,'')});
  var p=r.getAttribute('data-provider');if(p)g.providers[p]=(g.providers[p]||0)+1;
});
order.sort(function(a,b){return groups[b].items.length-groups[a].items.length});
order.forEach(function(n,i){groups[n].c=COLORS[i%COLORS.length]});
var wall=document.createElement('div');wall.className='ld-wall';wall.setAttribute('role','list');
order.forEach(function(name,i){
  var g=groups[name],n=g.items.length;
  var b=document.createElement('button');b.type='button';b.className='ld-door';b.setAttribute('role','listitem');b.setAttribute('data-cat',name);
  b.style.setProperty('--c1',g.c[0]);b.style.setProperty('--c2',g.c[1]);b.style.transitionDelay=(i*70)+'ms';
  b.setAttribute('aria-haspopup','dialog');
  b.setAttribute('aria-label','Open '+name+': '+n+(n===1?' course':' courses'));
  b.innerHTML='<span class="ld-frame"><span class="ld-room"><b>'+n+'</b><small>'+(n===1?'course':'courses')+'</small></span><span class="ld-panel"><span class="ld-num">'+String(i+1).padStart(2,'0')+'</span><span class="ld-ico">'+icon(name)+'</span><span class="ld-name"></span><span class="ld-knob" aria-hidden="true"></span></span></span><span class="ld-floor" aria-hidden="true"></span><span class="ld-cta">Click to enter<em>'+n+(n===1?' course':' courses')+'</em></span>';
  b.querySelector('.ld-name').textContent=name;
  wall.appendChild(b);
});
host.appendChild(wall);
var doors=[].slice.call(wall.children);
if('IntersectionObserver' in window&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{threshold:.15});doors.forEach(function(d){io.observe(d)})}
else doors.forEach(function(d){d.classList.add('is-in')});
var ov=document.createElement('div');ov.className='ld-overlay';ov.hidden=true;
ov.innerHTML='<div class="ld-card" role="dialog" aria-modal="true" aria-labelledby="ldTitle" tabindex="-1"><button type="button" class="ld-close" aria-label="Close card">×</button><div class="ld-loading" aria-live="polite"><span class="ld-load-label">Loading the card</span><span class="ld-bar"><i></i></span><span class="ld-pct">0%</span></div><div class="ld-content" hidden><div class="ld-head"><span class="ld-ico"></span><div><p class="ld-kick">Skill area</p><h3 id="ldTitle"></h3></div></div><div class="ld-body"><div class="ld-stats"></div><ul class="ld-list"></ul><div class="ld-actions"><button type="button" class="ld-show">Show these courses ↓</button></div></div></div></div>';
document.body.appendChild(ov);
var card=ov.querySelector('.ld-card'),loading=ov.querySelector('.ld-loading'),content=ov.querySelector('.ld-content'),bar=ov.querySelector('.ld-bar i'),pct=ov.querySelector('.ld-pct');
var last=null,timer=null,cur=null;
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
function fill(g){
  card.style.setProperty('--c1',g.c[0]);card.style.setProperty('--c2',g.c[1]);
  ov.querySelector('#ldTitle').textContent=g.name;
  ov.querySelector('.ld-head .ld-ico').innerHTML=icon(g.name);
  var n=g.items.length,dated=g.items.filter(function(x){return x.date}).sort(function(a,b){return b.date-a.date});
  var pv=Object.keys(g.providers).map(function(p){return p+' '+g.providers[p]}).join(' · ');
  ov.querySelector('.ld-stats').innerHTML='<div class="ld-stat"><b>'+n+'</b><span>'+(n===1?'course or path':'courses and paths')+'</span></div><div class="ld-stat"><b>'+Object.keys(g.providers).length+'</b><span>'+esc(pv)+'</span></div>'+(dated.length?'<div class="ld-stat"><b>'+esc(dated[0].dateText)+'</b><span>latest completion</span></div>':'');
  var ul=ov.querySelector('.ld-list');ul.innerHTML='';
  (dated.length?dated:g.items).slice(0,6).forEach(function(x){var li=document.createElement('li');var t=document.createElement('div');t.textContent=x.title;li.appendChild(t);if(x.dateText){var s=document.createElement('span');s.textContent=x.dateText;li.appendChild(s)}ul.appendChild(li)});
  if(n>6){var m=document.createElement('li');m.className='ld-more';m.textContent='+ '+(n-6)+' more in the full list';ul.appendChild(m)}
}
function finish(){loading.hidden=true;content.hidden=false;card.scrollTop=0;card.focus()}
function open(name,btn){
  cur=groups[name];last=btn;fill(cur);
  ov.hidden=false;document.body.classList.add('ld-lock');
  loading.hidden=false;content.hidden=true;clearInterval(timer);
  if(reduce){bar.style.width='100%';pct.textContent='100%';finish();return}
  var v=0;bar.style.width='0%';pct.textContent='0%';card.focus();
  timer=setInterval(function(){v=Math.min(100,v+Math.ceil(Math.random()*9)+4);bar.style.width=v+'%';pct.textContent=v+'%';if(v>=100){clearInterval(timer);setTimeout(finish,160)}},60);
}
function close(){clearInterval(timer);ov.hidden=true;document.body.classList.remove('ld-lock');if(last)last.focus()}
wall.addEventListener('click',function(e){var b=e.target.closest('.ld-door');if(b)open(b.getAttribute('data-cat'),b)});
ov.addEventListener('click',function(e){if(e.target===ov||e.target.closest('.ld-close'))close()});
document.addEventListener('keydown',function(e){
  if(ov.hidden)return;
  if(e.key==='Escape'){close();return}
  if(e.key==='Tab'){var f=[].slice.call(card.querySelectorAll('button')).filter(function(x){return x.offsetParent});if(!f.length){e.preventDefault();return}var a=document.activeElement,i=f.indexOf(a);if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&(i===f.length-1||i<0)){e.preventDefault();f[0].focus()}}
});
ov.querySelector('.ld-show').addEventListener('click',function(){
  var sel=document.getElementById('categoryFilter');
  if(sel&&cur){sel.value=cur.name;sel.dispatchEvent(new Event('change',{bubbles:true}));sel.dispatchEvent(new Event('input',{bubbles:true}))}
  close();
  var t=document.getElementById('timeline')||document.getElementById('courseSearch');
  if(t)t.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
});
})();
