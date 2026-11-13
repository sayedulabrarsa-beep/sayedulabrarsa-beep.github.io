/* Homepage motion: section reveals, magnetic buttons, Lenis smooth scroll (desktop wheel only; touch stays native). */
(function(){
'use strict';
var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
if(reduce)return;
/* B: reveal home sections once as they come into view */
var sel=['.ed-intro-band .ed-band-copy','.ed-intro-band .ed-focus-list','.home-logo-belt-heading','.st-head','.ed-recognition-photo','.ed-recognition-copy','.ed-education-copy','.ed-education-visual','.ed-final-cta','.ed-world-heading'];
var els=[];sel.forEach(function(s){[].forEach.call(document.querySelectorAll(s),function(el){el.classList.add('hm-rv');els.push(el)})});
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('hm-in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -12% 0px',threshold:.08});
  els.forEach(function(el){io.observe(el)});
  setTimeout(function(){els.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)el.classList.add('hm-in')})},60);
}else els.forEach(function(el){el.classList.add('hm-in')});
/* C: magnetic pull on desktop pointers */
var fine=false;try{fine=matchMedia('(hover:hover) and (pointer:fine)').matches}catch(e){}
if(fine){[].forEach.call(document.querySelectorAll('.ed-btn,.ed-pills a,.ed-text-link'),function(b){
  b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect(),x=e.clientX-(r.left+r.width/2),y=e.clientY-(r.top+r.height/2);b.style.translate=(x*.22).toFixed(1)+'px '+(y*.32).toFixed(1)+'px'});
  b.addEventListener('pointerleave',function(){b.style.translate=''});
})}
/* F: floating shapes in the hero collage */
(function(){var c=document.querySelector('.ed-collage');if(!c||c.querySelector('.hm-float'))return;
var w=document.createElement('div');w.className='hm-float';w.setAttribute('aria-hidden','true');
w.innerHTML='<svg class="hm-f1" viewBox="0 0 60 24" style="--r:-28deg;--d:10s"><rect x="1" y="1" width="58" height="22" rx="11"/><path d="M30 1v22"/></svg>'
+'<svg class="hm-f2" viewBox="0 0 30 30" style="--d:8s;--x:-6px"><circle cx="15" cy="15" r="13"/><path d="M5 15h20"/></svg>'
+'<svg class="hm-f3" viewBox="0 0 46 46" style="--d:12s;--y:12px"><path d="M23 3l17 10v20L23 43 6 33V13z"/><circle cx="23" cy="23" r="5"/></svg>'
+'<svg class="hm-f4" viewBox="0 0 26 26" style="--d:7s;--x:8px"><path d="M13 3v20M3 13h20"/></svg>'
+'<svg class="hm-f5" viewBox="0 0 22 22" style="--d:11s"><circle cx="11" cy="11" r="9"/></svg>';
c.insertBefore(w,c.firstChild)})();
/* D: Lenis smooth scroll on the homepage only */
if(window.Lenis){
  ['#st-row','.ed-world-viewport','.home-logo-strip','.st-modal','[role="dialog"]'].forEach(function(s){[].forEach.call(document.querySelectorAll(s),function(el){el.setAttribute('data-lenis-prevent','')})});
  var lenis=new Lenis({lerp:.1,wheelMultiplier:1,smoothWheel:true,anchors:{offset:-76}});
  window.__lenis=lenis;
  (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now());
}
})();
