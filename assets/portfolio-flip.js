(function(){
'use strict';
var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
/* ---------- flip pad ---------- */
(function(){
  var pad=document.getElementById('pf-pad');if(!pad)return;
  var data=[].map.call(document.querySelectorAll('.pf-data li'),function(li){return[li.dataset.h]});
  if(data.length<2)return;
  var top=pad.querySelector('.pf-top'),under=pad.querySelector('.pf-under'),cnt=null;
  var i=0,busy=false,hold=false,timer;
  function fill(el,p){el.querySelector('b').textContent=p[0]}
  function pad2(n){return n<10?'0'+n:''+n}
  function next(){
    if(busy)return;busy=true;
    var n=(i+1)%data.length;
    if(reduce){fill(top,data[n]);i=n;busy=false;return}
    top.classList.add('is-flip');
    setTimeout(function(){
      i=n;fill(top,data[i]);top.classList.add('no-tr');top.classList.remove('is-flip');
      void top.offsetWidth;top.classList.remove('no-tr');
      fill(under,data[(i+1)%data.length]);busy=false;
    },720);
  }
  function loop(){clearInterval(timer);timer=setInterval(function(){if(!hold&&!document.hidden)next()},2800)}
  pad.addEventListener('mouseenter',function(){hold=true});pad.addEventListener('mouseleave',function(){hold=false});
  pad.addEventListener('click',next);
  fill(under,data[1]);loop();
})();
/* ---------- handwriting words ---------- */
(function(){
  var root=document.getElementById('pwr');if(!root)return;
  var paper=root.querySelector('.pwr-paper'),body=root.querySelector('.pwr-body'),pen=root.querySelector('.pwr-pen');
  var elAr=root.querySelector('.pwr-ar'),elEn=root.querySelector('.pwr-en'),elBn=root.querySelector('.pwr-bn'),elRef=root.querySelector('.pwr-ref');
  var btnPP=root.querySelector('.pwr-pp'),num=root.querySelector('.pwr-n');
  var list=[],idx=0,run=0,paused=reduce,visible=false,tm=[];
  function later(f,ms){var t=setTimeout(f,ms);tm.push(t);return t}
  function clear(){tm.forEach(clearTimeout);tm=[]}
  function words(el,text){el.textContent='';if(!text)return[];var out=[];text.split(/\s+/).forEach(function(w,k,a){var s=document.createElement('span');s.className='w';s.textContent=w;el.appendChild(s);if(k<a.length-1)el.appendChild(document.createTextNode(' '));out.push(s)});return out}
  function penAt(span,rtl){
    var r=span.getBoundingClientRect(),p=paper.getBoundingClientRect();
    pen.style.left=((rtl?r.left:r.right)-p.left-4)+'px';pen.style.top=(r.bottom-p.top-26)+'px';
  }
  function show(k,instant){
    clear();run++;var my=run;idx=(k+list.length)%list.length;var it=list[idx];
    body.classList.remove('out');elRef.classList.remove('on');pen.classList.remove('on');
    var A=words(elAr,it.ar),E=words(elEn,it.en&&/[.!?”"]$/.test(it.en)?it.en:(it.en||'')+'.'),B=words(elBn,it.bn);
    elAr.hidden=!it.ar;
    elRef.innerHTML='';var c=document.createElement('span');c.textContent=it.ref;elRef.appendChild(c);
    if(it.note){var s=document.createElement('small');s.textContent=it.note;elRef.appendChild(s)}
    num.textContent=(idx+1)+' / '+list.length;
    var seq=[];A.forEach(function(w){seq.push([w,true,260])});E.forEach(function(w){seq.push([w,false,115])});B.forEach(function(w){seq.push([w,false,125])});
    if(instant){seq.forEach(function(s){s[0].classList.add('on')});elRef.classList.add('on');return}
    var t=500;
    seq.forEach(function(s){later(function(){if(my!==run)return;s[0].classList.add('on');pen.classList.add('on');penAt(s[0],s[1])},t);t+=s[2]});
    later(function(){pen.classList.remove('on');elRef.classList.add('on')},t+150);
    var readMs=Math.min(7000,3000+(it.en?it.en.length*18:0));
    later(function(){if(!paused)out()},t+150+readMs);
  }
  function out(){var my=run;body.classList.add('out');later(function(){if(my===run&&!paused)show(idx+1)},520)}
  function setPaused(p){paused=p;btnPP.textContent=p?'Play':'Pause';btnPP.setAttribute('aria-pressed',p?'true':'false');btnPP.setAttribute('aria-label',p?'Resume writing':'Pause writing')}
  btnPP.addEventListener('click',function(){
    if(paused){setPaused(false);show(idx)}else{setPaused(true);clear();run++;var it=list[idx];[].forEach.call(root.querySelectorAll('.w'),function(w){w.classList.add('on')});elRef.classList.add('on');pen.classList.remove('on');body.classList.remove('out')}
  });
  root.querySelector('.pwr-next').addEventListener('click',function(){show(idx+1,paused)});
  root.querySelector('.pwr-prev').addEventListener('click',function(){show(idx-1,paused)});
  function start(){
    if(list.length)return;
    fetch(root.dataset.src).then(function(r){return r.json()}).then(function(d){list=d;setPaused(reduce);show(0,reduce)}).catch(function(){
      elEn.textContent='Words could not be loaded just now.';
    });
  }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){es.forEach(function(en){
      visible=en.isIntersecting;
      if(visible&&!list.length)start();
    })},{rootMargin:'200px'}).observe(root);
  }else start();
  document.addEventListener('visibilitychange',function(){if(document.hidden){clear();run++}else if(visible&&!paused&&list.length)show(idx)});
})();
})();
