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
/* D: Lenis smooth scroll on the homepage only */
if(window.Lenis){
  ['#st-row','.ed-world-viewport','.home-logo-strip','.st-modal','[role="dialog"]'].forEach(function(s){[].forEach.call(document.querySelectorAll(s),function(el){el.setAttribute('data-lenis-prevent','')})});
  var lenis=new Lenis({lerp:.1,wheelMultiplier:1,smoothWheel:true,anchors:{offset:-76}});
  window.__lenis=lenis;
  (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now());
}
})();
