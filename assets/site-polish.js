/* Site polish (not loaded on Learning or Portfolio): article reading progress, inner-page section reveals. */
(function(){
'use strict';
var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
/* reading progress bar on blog articles */
var art=document.querySelector('article.article-content');
if(art){
  var bar=document.createElement('div');bar.className='sp-progress';bar.setAttribute('aria-hidden','true');bar.innerHTML='<i></i>';document.body.appendChild(bar);
  var fill=bar.firstChild,tick=0;
  function upd(){tick=0;var r=art.getBoundingClientRect(),total=r.height-innerHeight*.6,done=-r.top+innerHeight*.2;var p=total>0?Math.max(0,Math.min(1,done/total)):0;fill.style.transform='scaleX('+p.toFixed(4)+')'}
  addEventListener('scroll',function(){if(!tick){tick=1;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd();
}
/* soft reveals on About, Achievements and Education */
if(reduce||!('IntersectionObserver' in window))return;
var path=location.pathname.replace(/index\.html$/,'');
if(!/^\/(about|achievements|education)\/$/.test(path))return;
var secs=[].slice.call(document.querySelectorAll('main > section')).slice(1);
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('sp-in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -10% 0px',threshold:.06});
secs.forEach(function(s){var r=s.getBoundingClientRect();if(r.top<innerHeight*.9)return;s.classList.add('sp-rv');io.observe(s)});
})();
