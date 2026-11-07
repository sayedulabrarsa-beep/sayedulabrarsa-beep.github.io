(function(){
'use strict';
var host=document.getElementById('ldDoors');
var rows=[].slice.call(document.querySelectorAll('.course-row'));
if(!host||!rows.length)return;
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var MON={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
function parseDate(t){var m=/(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})/.exec(t||'');return m?new Date(+m[3],MON[m[2]],+m[1]):null}
var groups={},order=[];
rows.forEach(function(r){
  var c=r.getAttribute('data-category');if(!c)return;
  if(!groups[c]){groups[c]={name:c,items:[],providers:{}};order.push(c)}
  var g=groups[c],dEl=r.querySelector('.date');
  g.items.push({title:(r.querySelector('h3')||{}).textContent||'',date:parseDate(dEl&&dEl.textContent),dateText:(dEl&&dEl.textContent||'').replace(/^Learning path ·\s*/,'')});
  var p=r.getAttribute('data-provider');if(p)g.providers[p]=(g.providers[p]||0)+1;
});
order.sort(function(a,b){return groups[b].items.length-groups[a].items.length});
var wall=document.createElement('div');wall.className='ld-wall';wall.setAttribute('role','list');
order.forEach(function(name,i){
  var g=groups[name],n=g.items.length;
  var b=document.createElement('button');b.type='button';b.className='ld-door';b.setAttribute('role','listitem');b.setAttribute('data-cat',name);
  b.setAttribute('aria-haspopup','dialog');
  b.setAttribute('aria-label','Open '+name+': '+n+(n===1?' course':' courses'));
  b.innerHTML='<span class="ld-frame"><span class="ld-panel"><span class="ld-num">'+String(i+1).padStart(2,'0')+'</span><span class="ld-name"></span><span class="ld-count"></span><span class="ld-knob" aria-hidden="true"></span></span><span class="ld-light" aria-hidden="true"></span></span><span class="ld-cta">Click to enter</span>';
  b.querySelector('.ld-name').textContent=name;
  b.querySelector('.ld-count').textContent=n+(n===1?' course':' courses');
  wall.appendChild(b);
});
host.appendChild(wall);
var ov=document.createElement('div');ov.className='ld-overlay';ov.hidden=true;
ov.innerHTML='<div class="ld-card" role="dialog" aria-modal="true" aria-labelledby="ldTitle" tabindex="-1"><button type="button" class="ld-close" aria-label="Close card">×</button><div class="ld-loading" aria-live="polite"><span class="ld-load-label">Loading the card</span><span class="ld-bar"><i></i></span><span class="ld-pct">0%</span></div><div class="ld-content" hidden><p class="ld-kick">Skill area</p><h3 id="ldTitle"></h3><p class="ld-meta"></p><ul class="ld-list"></ul><div class="ld-actions"><button type="button" class="ld-show">Show these courses ↓</button></div></div></div>';
document.body.appendChild(ov);
var card=ov.querySelector('.ld-card'),loading=ov.querySelector('.ld-loading'),content=ov.querySelector('.ld-content'),bar=ov.querySelector('.ld-bar i'),pct=ov.querySelector('.ld-pct');
var last=null,timer=null,cur=null;
function fill(g){
  ov.querySelector('#ldTitle').textContent=g.name;
  var n=g.items.length,prov=Object.keys(g.providers).map(function(p){return p+' ('+g.providers[p]+')'}).join(' · ');
  var dated=g.items.filter(function(x){return x.date}).sort(function(a,b){return b.date-a.date});
  ov.querySelector('.ld-meta').textContent=n+(n===1?' completed course or path':' completed courses and paths')+' · '+prov+(dated.length?' · latest: '+dated[0].dateText.replace(/^Completed\s*/,''):'');
  var ul=ov.querySelector('.ld-list');ul.innerHTML='';
  (dated.length?dated:g.items).slice(0,6).forEach(function(x){var li=document.createElement('li');li.textContent=x.title;ul.appendChild(li)});
  if(n>6){var m=document.createElement('li');m.className='ld-more';m.textContent='+ '+(n-6)+' more in the full list';ul.appendChild(m)}
}
function finish(){loading.hidden=true;content.hidden=false;ov.classList.add('is-ready');card.focus()}
function open(name,btn){
  cur=groups[name];last=btn;fill(cur);
  ov.hidden=false;document.body.classList.add('ld-lock');ov.classList.remove('is-ready');
  loading.hidden=false;content.hidden=true;
  var done=function(){finish()};
  clearInterval(timer);
  if(reduce){bar.style.width='100%';pct.textContent='100%';done();card.focus();return}
  var v=0;bar.style.width='0%';pct.textContent='0%';card.focus();
  timer=setInterval(function(){v=Math.min(100,v+Math.ceil(Math.random()*9)+4);bar.style.width=v+'%';pct.textContent=v+'%';if(v>=100){clearInterval(timer);setTimeout(done,160)}},60);
}
function close(){clearInterval(timer);ov.hidden=true;document.body.classList.remove('ld-lock');if(last)last.focus()}
wall.addEventListener('click',function(e){var b=e.target.closest('.ld-door');if(b)open(b.getAttribute('data-cat'),b)});
ov.addEventListener('click',function(e){if(e.target===ov||e.target.closest('.ld-close'))close()});
document.addEventListener('keydown',function(e){
  if(ov.hidden)return;
  if(e.key==='Escape'){close();return}
  if(e.key==='Tab'){var f=[].slice.call(card.querySelectorAll('button')).filter(function(x){return x.offsetParent});if(!f.length){e.preventDefault();return}var a=document.activeElement,i=f.indexOf(a);if(e.shiftKey&&(i<=0)){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&(i===f.length-1||i<0)){e.preventDefault();f[0].focus()}}
});
ov.querySelector('.ld-show').addEventListener('click',function(){
  var sel=document.getElementById('categoryFilter');
  if(sel&&cur){sel.value=cur.name;sel.dispatchEvent(new Event('change',{bubbles:true}));sel.dispatchEvent(new Event('input',{bubbles:true}))}
  close();
  var t=document.getElementById('timeline')||document.getElementById('courseSearch');
  if(t)t.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
});
})();
