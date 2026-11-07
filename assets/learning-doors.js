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
