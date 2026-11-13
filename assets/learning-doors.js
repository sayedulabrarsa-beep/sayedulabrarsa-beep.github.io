(function(){
'use strict';
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
/* Dhaka clock */
var clk=document.getElementById('lpTime');
function tick(){try{clk.textContent=new Intl.DateTimeFormat('en-GB',{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:'Asia/Dhaka'}).format(new Date())}catch(e){}}
if(clk){tick();setInterval(tick,20000)}
/* sideways scroller: arrows + mouse drag (touch uses native swipe) */
function scroller(el,prev,next,stage){
  if(!el)return;
  function step(){var c=el.querySelector('.ld-door,.lp-card');return c?c.getBoundingClientRect().width+24:300}
  function edges(){var max=el.scrollWidth-el.clientWidth-2;(stage||el.parentNode).classList.toggle('at-start',el.scrollLeft<=2);(stage||el.parentNode).classList.toggle('at-end',el.scrollLeft>=max)}
  if(prev)prev.addEventListener('click',function(){el.scrollBy({left:-step(),behavior:reduce?'auto':'smooth'})});
  if(next)next.addEventListener('click',function(){el.scrollBy({left:step(),behavior:reduce?'auto':'smooth'})});
  el.addEventListener('scroll',edges,{passive:true});window.addEventListener('resize',edges);edges();
  el.addEventListener('keydown',function(e){if(e.target!==el)return;if(e.key==='ArrowRight'){e.preventDefault();el.scrollBy({left:step(),behavior:'smooth'})}if(e.key==='ArrowLeft'){e.preventDefault();el.scrollBy({left:-step(),behavior:'smooth'})}});
  var down=false,sx=0,sl=0,moved=false;
  el.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0)return;down=true;moved=false;sx=e.clientX;sl=el.scrollLeft});
  window.addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;if(!moved&&Math.abs(dx)>6){moved=true;el.classList.add('is-drag')}if(moved)el.scrollLeft=sl-dx});
  window.addEventListener('pointerup',function(){if(!down)return;down=false;if(moved){setTimeout(function(){el.classList.remove('is-drag')},0)}});
  el.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
  el.addEventListener('dragstart',function(e){e.preventDefault()});
}
var track=document.getElementById('lpTrack');
if(track){
  var stage=track.parentNode;
  scroller(track,stage.querySelector('.lp-prev'),stage.querySelector('.lp-next'),stage);
  /* door opens, light grows to fill the screen, then the area page loads */
  track.addEventListener('click',function(e){
    var a=e.target.closest('a.ld-door');
    if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    if(reduce)return;
    e.preventDefault();
    if(a.classList.contains('is-opening'))return;
    var f=a.querySelector('.ld-frame').getBoundingClientRect();
    a.classList.add('is-opening');track.classList.add('is-entering');
    var p=document.createElement('div');p.className='lp-portal';
    p.style.cssText='top:'+f.top+'px;left:'+f.left+'px;width:'+f.width+'px;height:'+f.height+'px';
    document.body.appendChild(p);
    void p.offsetWidth;
    setTimeout(function(){p.classList.add('go')},380);
    try{sessionStorage.setItem('ldEnter','1')}catch(x){}
    var href=a.href,go=function(){location.href=href};
    setTimeout(go,1250);
  });
  window.addEventListener('pageshow',function(ev){
    if(!ev.persisted)return;
    [].slice.call(document.querySelectorAll('.lp-portal')).forEach(function(n){n.remove()});
    [].slice.call(track.querySelectorAll('.is-opening')).forEach(function(n){n.classList.remove('is-opening')});
    track.classList.remove('is-entering');
  });
}
[].slice.call(document.querySelectorAll('.lp-group')).forEach(function(g){
  scroller(g.querySelector('.lp-gallery'),g.querySelector('.lp-gprev'),g.querySelector('.lp-gnext'),g.querySelector('.lp-gal-ctl'));
});
})();
/* ===== Full course record as a scroll story (month by month) ===== */
(function(){
'use strict';
var story=document.getElementById('ltStory'),src=document.getElementById('timeline');
if(!story||!src)return;
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
var MS=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
var M3={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
var rowsAll=[].slice.call(document.querySelectorAll('.course-row'));
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
function read(r){
  var dl=(r.querySelector('.date')||{}).textContent||'',m=/(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})/.exec(dl);
  var prov=r.getAttribute('data-provider');
  if(/^Coursera/.test(dl))prov='Coursera';else if(/^LinkedIn Learning/.test(dl))prov='LinkedIn Learning';
  var t=(r.querySelector('h3')||{}).textContent||'';
  return {title:t,cat:r.getAttribute('data-category')||'',prov:prov,d:m?+m[1]:null,mo:m?M3[m[2]]:null,y:m?+m[3]:null,t:m?Date.UTC(+m[3],M3[m[2]],+m[1]):null,path:/^Learning path/.test(dl)||/Professional Certificate/.test(t)};
}
var DAY=86400000;
function label(g,short){
  var a=g.last,b=g.first,ma=short?MS[a.mo].charAt(0)+MS[a.mo].slice(1).toLowerCase():MN[a.mo],mb=short?MS[b.mo].charAt(0)+MS[b.mo].slice(1).toLowerCase():MN[b.mo];
  if(a.t===b.t)return b.d+' '+mb+' '+b.y;
  if(a.mo===b.mo&&a.y===b.y)return a.d+' – '+b.d+' '+mb+' '+b.y;
  if(a.y===b.y)return a.d+' '+ma+' – '+b.d+' '+mb+' '+b.y;
  return a.d+' '+ma+' '+a.y+' – '+b.d+' '+mb+' '+b.y;
}
function build(){
  var seen={},days={},dorder=[],und=[];
  rowsAll.forEach(function(r){
    if(r.hidden)return;
    var c=read(r),k=c.title.toLowerCase()+'|'+c.prov;if(seen[k])return;seen[k]=1;
    if(c.t===null){und.push(c);return}
    if(!days[c.t]){days[c.t]={t:c.t,items:[]};dorder.push(c.t)}
    days[c.t].items.push(c);
  });
  dorder.sort(function(a,b){return b-a});
  var out=[],cur=null;
  dorder.forEach(function(t){
    var dd=days[t];
    if(cur&&cur.items.length+dd.items.length<=10&&(cur.first.t-t)<=14*DAY){cur.items=cur.items.concat(dd.items);cur.last=dd.items[0]}
    else{cur={items:dd.items.slice(),first:dd.items[0],last:dd.items[0]};out.push(cur)}
  });
  /* in each group: first = newest, last = oldest; label() wants oldest then newest */
  out.forEach(function(g){var newest=g.first,oldest=g.last;g.first=newest;g.last=oldest;g.provs={};g.items.forEach(function(c){g.provs[c.prov]=1});g.y=newest.y;g.mo=newest.mo;g.key='d'+newest.t});
  if(und.length){var u={key:'undated',y:null,mo:null,items:und,provs:{}};und.forEach(function(c){u.provs[c.prov]=1});out.push(u)}
  return out;
}
var icoSvg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>';
var rings='<svg viewBox="0 0 600 600" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1">'+[300,262,224,186,148,110,72].map(function(r){return '<circle cx="300" cy="300" r="'+r+'"/>'}).join('')+'</g><g stroke="currentColor" stroke-width="1.4">'+(function(){var o='';for(var i=0;i<48;i++){var a=i*Math.PI/24,r1=i%4===0?276:286,r2=300;o+='<line x1="'+(300+Math.cos(a)*r1)+'" y1="'+(300+Math.sin(a)*r1)+'" x2="'+(300+Math.cos(a)*r2)+'" y2="'+(300+Math.sin(a)*r2)+'"/>'}return o})()+'</g></svg>';
var digits='<span class="lt-reel">'+[0,1,2,3,4,5,6,7,8,9].map(function(d){return '<span>'+d+'</span>'}).join('')+'</span>';
var G=[],items=[],active=-1,cur,tot,bar,range,yearBox,yearText,fill,list,digitEls,ring,raf=0;
function render(){
  G=build();
  if(!G.length){story.innerHTML='';story.classList.remove('is-on');src.classList.remove('lt-off');return}
  var h='<div class="lt-rings" aria-hidden="true">'+rings+'</div><div class="wrap lt-head-m"><p class="lt-kick"><i></i>Full course record</p><h2>Every course, month by month.</h2></div><div class="wrap lt-grid"><div class="lt-left"><p class="lt-kick"><i></i>Full course record</p><h2 class="lt-h">Every course,<br>month by month.</h2>'
   +'<div class="lt-year" role="img" aria-label="Year"><span class="lt-digits">'+digits+digits+digits+digits+'</span><span class="lt-yeartext"></span></div>'
   +'<p class="lt-range"></p><div class="lt-prog"><span class="lt-pico">'+icoSvg+'</span><b class="lt-cur">01</b><span class="lt-tot"></span><span class="lt-bar"><i></i></span></div></div>'
   +'<ol class="lt-list"><li class="lt-fillwrap" aria-hidden="true"><i class="lt-fill"></i></li>'
   +G.map(function(g,i){
      var und=g.key==='undated',ttl=und?'Earlier learning':label(g),tag=und?'NO DATE ON RECORD':label(g,true).toUpperCase();
      var n=g.items.length,pv=Object.keys(g.provs).join(' · ');
      return '<li class="lt-item" data-i="'+i+'"><span class="lt-dot" aria-hidden="true"></span><p class="lt-date">'+tag+' · '+n+(n===1?' COURSE':' COURSES')+'</p><h3>'+esc(ttl)+'</h3><p class="lt-sub">'+esc(pv)+'</p><ul>'+g.items.map(function(c,j){return '<li'+(j>=8?' class="lt-more" hidden':'')+'>'+esc(c.title)+(c.path?' <em>learning path</em>':'')+'<small>'+esc(c.cat)+'</small></li>'}).join('')+'</ul>'+(n>8?'<button type="button" class="lt-toggle" aria-expanded="false">Show '+(n-8)+' more</button>':'')+'</li>';
   }).join('')+'</ol></div>';
  story.innerHTML=h;story.classList.add('is-on');src.classList.add('lt-off');
  ring=story.querySelector('.lt-rings');
  function syncRing(){
    if(!ring)return;
    var bounds=story.getBoundingClientRect();
    ring.classList.toggle('is-visible',bounds.top<window.innerHeight*.55&&bounds.bottom>window.innerHeight*.45);
  }
  syncRing();
  cur=story.querySelector('.lt-cur');tot=story.querySelector('.lt-tot');bar=story.querySelector('.lt-bar i');range=story.querySelector('.lt-range');
  yearBox=story.querySelector('.lt-year');yearText=story.querySelector('.lt-yeartext');fill=story.querySelector('.lt-fill');list=story.querySelector('.lt-list');
  digitEls=[].slice.call(story.querySelectorAll('.lt-digits .lt-reel'));items=[].slice.call(story.querySelectorAll('.lt-item'));
  tot.textContent='/ '+('0'+G.length).slice(-2);
  [].slice.call(story.querySelectorAll('.lt-toggle')).forEach(function(bt){bt.addEventListener('click',function(){var it=bt.closest('.lt-item'),open=bt.getAttribute('aria-expanded')!=='true';[].slice.call(it.querySelectorAll('.lt-more')).forEach(function(l){l.hidden=!open});bt.setAttribute('aria-expanded',String(open));bt.textContent=open?'Show fewer':'Show '+(it.querySelectorAll('.lt-more').length)+' more';setTimeout(function(){setActive(active,true)},30)})});
  active=-1;setActive(0,true);onScroll();
}
function setActive(i,force){
  if(i===active&&!force)return;active=i;var g=G[i];
  items.forEach(function(el,k){el.classList.toggle('is-active',k===i);el.classList.toggle('is-past',k<i)});
  cur.textContent=('0'+(i+1)).slice(-2);
  var n=g.items.length;
  range.textContent=(g.key==='undated'?'NO DATE ON RECORD':label(g,true).toUpperCase())+' — '+n+(n===1?' COURSE':' COURSES');
  if(g.y===null){yearBox.classList.add('is-text');yearText.textContent='Earlier'}
  else{yearBox.classList.remove('is-text');var s=String(g.y);digitEls.forEach(function(r,k){r.style.transform='translateY('+(-(+s.charAt(k))*10)+'%)'});yearBox.setAttribute('aria-label',s)}
  bar.style.width=(G.length>1?(i/(G.length-1))*100:100)+'%';
  var it=items[i],dot=it.querySelector('.lt-dot');
  fill.style.height=(it.offsetTop+dot.offsetTop+6)+'px';
}
function onScroll(){
  raf=0;if(!items.length)return;
  var line=window.innerHeight*.46,best=0,bd=1e9;
  items.forEach(function(el,k){var r=el.getBoundingClientRect(),c=r.top+Math.min(r.height,160)/2,d=Math.abs(c-line);if(r.top<line&&r.bottom>line){d=-1}if(d<bd){bd=d;best=k}});
  setActive(best);
}
/* wheel turns only with page scroll: down = clockwise, up = back, stops when scrolling stops */
var rot=0,lastSY=window.scrollY;
window.addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(onScroll);var sy=window.scrollY,dy=sy-lastSY;lastSY=sy;if(ring&&story){var rb=story.getBoundingClientRect(),vh=window.innerHeight,on=rb.top<vh*.55&&rb.bottom>vh*.45;ring.classList.toggle('is-visible',on);if(on&&!reduce){rot=(rot+dy*.12)%360;ring.style.setProperty('--lt-rot',rot.toFixed(2)+'deg')}}},{passive:true});
window.addEventListener('resize',function(){setHH();if(items.length)setActive(active,true)});
function setHH(){var h=document.querySelector('header');story.style.setProperty('--hh',(h?h.offsetHeight:0)+'px')}
setHH();
['courseSearch','categoryFilter','providerFilter'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener(id==='courseSearch'?'input':'change',function(){render()})});
render();
})();
/* ===== gentle scroll reveal for the other Learning sections ===== */
(function(){
if(!('IntersectionObserver' in window)||(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches))return;
var els=[].slice.call(document.querySelectorAll('.workshop-card,.cert-card,.rf-uni-card,.workshop-zone .section-title,.rolling-head,.rf-learn .eyebrow,.rf-learn .rf-sub,.rf-stats>*,.learning-note'));
if(!els.length)return;
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
els.forEach(function(el,i){el.classList.add('lt-rv');el.style.setProperty('--d',(i%4)*80+'ms');io.observe(el)});
})();

/* skill-by-skill hanging lines: arrows, mouse drag, reveal */
(function(){
  var parts=[].slice.call(document.querySelectorAll('.hg-part'));if(!parts.length)return;
  [].slice.call(document.querySelectorAll('.hg-rail')).forEach(function(part){
    var tr=part.querySelector('.hg-track'),pv=part.querySelector('.hg-prev'),nx=part.querySelector('.hg-next');if(!tr)return;
    function upd(){var max=tr.scrollWidth-tr.clientWidth-2;if(pv)pv.disabled=tr.scrollLeft<=2;if(nx)nx.disabled=tr.scrollLeft>=max}
    function go(d){tr.scrollBy({left:d*Math.max(260,tr.clientWidth*.72),behavior:'smooth'})}
    if(pv)pv.addEventListener('click',function(){go(-1)});if(nx)nx.addEventListener('click',function(){go(1)});
    tr.addEventListener('scroll',function(){window.requestAnimationFrame(upd)},{passive:true});window.addEventListener('resize',upd);upd();
    tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){go(1);e.preventDefault()}else if(e.key==='ArrowLeft'){go(-1);e.preventDefault()}});
    var down=false,sx=0,sl=0,moved=false;
    tr.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0)return;down=true;moved=false;sx=e.clientX;sl=tr.scrollLeft});
    window.addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;if(!moved&&Math.abs(dx)>6){moved=true;tr.classList.add('is-drag')}if(moved)tr.scrollLeft=sl-dx});
    window.addEventListener('pointerup',function(){if(!down)return;down=false;tr.classList.remove('is-drag');window.setTimeout(upd,60)});
  });
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
  parts.forEach(function(p){p.classList.add('hg-rv');io.observe(p)});
})();

/* hanging lines react to scrolling: page scroll and sideways scroll push the cards like wind */
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var parts=[].slice.call(document.querySelectorAll('.hg-part'));if(!parts.length)return;
  var st=new Map(),vis=new Set(),lastY=window.scrollY,run=false,lt=0;
  parts.forEach(function(p){st.set(p,{a:0,v:0});var tr=p.querySelectorAll('.hg-track'),lx=[];
    tr.forEach(function(t,i){lx[i]=t.scrollLeft;t.addEventListener('scroll',function(){var d=t.scrollLeft-lx[i];lx[i]=t.scrollLeft;st.get(p).v+=Math.max(-90,Math.min(90,-d))*.22;kick()},{passive:true})})});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)})},{rootMargin:'120px 0px'});parts.forEach(function(p){io.observe(p)})}else parts.forEach(function(p){vis.add(p)});
  function prog(){var h=window.innerHeight;vis.forEach(function(p){var r=p.getBoundingClientRect();p.style.setProperty('--pg',Math.max(0,Math.min(1,(h-r.top)/(h+r.height))).toFixed(3))})}
  window.addEventListener('scroll',function(){var d=window.scrollY-lastY;lastY=window.scrollY;var imp=Math.max(-90,Math.min(90,d))*.3;vis.forEach(function(p){st.get(p).v+=imp});prog();kick()},{passive:true});
  function kick(){if(!run){run=true;lt=0;requestAnimationFrame(tick)}}
  function tick(t){var dt=lt?Math.min(.033,(t-lt)/1000):.016;lt=t;var busy=false;
    st.forEach(function(s,p){if(Math.abs(s.a)<.01&&Math.abs(s.v)<.05){if(s.a){s.a=0;s.v=0;p.style.setProperty('--sw','0')}return}
      s.v+=(-38*s.a-3.2*s.v)*dt;s.a+=s.v*dt;s.a=Math.max(-9,Math.min(9,s.a));p.style.setProperty('--sw',s.a.toFixed(2));busy=true});
    if(busy)requestAnimationFrame(tick);else run=false}
  prog();
})();
