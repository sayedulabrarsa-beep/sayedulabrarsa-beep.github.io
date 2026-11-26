/* Pharma Blog: seamless, right-moving infinite article carousel.
   Every card uses a fixed width + gap; new articles join the same loop. */
(function(){
 'use strict';
 function init(){
  var stage=document.getElementById('bh-stage');
  if(!stage||stage.dataset.carouselReady==='infinite')return;
  var track=stage.querySelector('.bh-field'),grid=document.querySelector('.pb-featured-grid');
  if(!track||!grid)return;
  var items=Array.prototype.slice.call(grid.querySelectorAll('.pb-feature-card')).map(function(card){
   var link=card.querySelector('h3 a')||card.querySelector('a[href]');
   if(!link)return null;
   var img=card.querySelector('img'),meta=card.querySelector('.pb-card-meta');
   return {href:link.getAttribute('href'),title:(link.textContent||'').replace(/\s+/g,' ').trim(),
    img:img?(img.currentSrc||img.getAttribute('src')):'',tag:meta?meta.textContent.split('·')[0].trim():'PHARMA BLOG',
    bn:!!card.querySelector('.pb-bangla-link')};
  }).filter(function(x){return x&&x.href&&x.title;});
  if(!items.length)return;
  stage.dataset.carouselReady='infinite';track.innerHTML='';
  var count=document.querySelector('.bh-count-n');if(count)count.textContent=items.length;
  var cards=items.map(function(item){
   var a=document.createElement('a');a.className='bh-card';a.href=item.href;a.draggable=false;a.setAttribute('aria-label',item.title);
   var face=document.createElement('span');face.className='bh-face bh-front';
   if(item.img){var image=document.createElement('img');image.src=item.img;image.alt='';image.width=472;image.height=266;image.decoding='async';image.draggable=false;face.appendChild(image);}
   var body=document.createElement('span');body.className='bh-card-body';
   var tag=document.createElement('span');tag.className='bh-card-tag';tag.textContent=item.tag;
   var title=document.createElement('span');title.className='bh-card-title';title.textContent=item.title;
   var foot=document.createElement('span');foot.className='bh-card-foot';
   var read=document.createElement('span');read.textContent='Read article ↗';
   var lang=document.createElement('span');lang.textContent=item.bn?'English + বাংলা':'English';
   foot.appendChild(read);foot.appendChild(lang);body.appendChild(tag);body.appendChild(title);body.appendChild(foot);face.appendChild(body);a.appendChild(face);track.appendChild(a);return a;
  });
  var n=cards.length,width=stage.clientWidth,cardW=220,cardH=300,gap=28,pitch=248,loop=0,offset=0,speed=28;
  var dragging=false,pointer=null,startX=0,lastX=0,lastTime=0,moved=0,lastFrame=0,visible=true,velocity=0;
  var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function measure(){
   width=stage.clientWidth;
   cardW=width<540?Math.min(158,Math.max(132,(width-54)/2)):width<900?190:236;
   cardH=width<540?236:width<900?276:320;
   gap=width<540?18:width<900?24:30;
   pitch=cardW+gap;loop=n*pitch;
   cards.forEach(function(card){
    card.style.width=cardW+'px';card.style.height=cardH+'px';
    card.style.marginTop=(-cardH/2)+'px';card.style.marginLeft='0';
   });
   render();
  }
  function render(){
   cards.forEach(function(card,i){
    var x=((i*pitch+offset)%loop+loop)%loop;
    // Keep one copy of each card in the visible viewport; loop wrap is seamless.
    card.style.transform='translate3d('+Math.round(x)+'px,0,0)';
    card.style.opacity='1';card.style.visibility='visible';card.style.zIndex='2';
    card.style.pointerEvents=dragging?'none':'auto';card.setAttribute('aria-hidden','false');
   });
  }
  function animate(t){
   if(!lastFrame)lastFrame=t;var dt=Math.min(40,t-lastFrame)/1000;lastFrame=t;
   if(visible&&!dragging&&!reduced){
    if(Math.abs(velocity)>.1){offset+=velocity*dt;velocity*=Math.pow(.035,dt);}
    else offset+=speed*dt;
    offset=((offset%loop)+loop)%loop;render();
   }
   requestAnimationFrame(animate);
  }
  stage.addEventListener('pointerdown',function(e){
   if(e.pointerType==='mouse'&&e.button!==0)return;
   pointer=e.pointerId;startX=lastX=e.clientX;lastTime=e.timeStamp;moved=0;velocity=0;
  });
  stage.addEventListener('pointermove',function(e){
   if(pointer!==e.pointerId)return;
   var dx=e.clientX-startX;
   if(e.pointerType==='touch'&&!dragging&&Math.abs(dx)<7)return;
   if(!dragging&&Math.abs(dx)>6){
    dragging=true;stage.classList.add('is-drag');
    try{stage.setPointerCapture(pointer);}catch(err){}
   }
   if(!dragging)return;
   if(e.pointerType!=='touch'&&e.cancelable)e.preventDefault();
   moved=Math.abs(dx);offset+=e.clientX-lastX;
   var elapsed=Math.max(1,e.timeStamp-lastTime);
   velocity=(e.clientX-lastX)/elapsed*1000;
   lastX=e.clientX;lastTime=e.timeStamp;
   offset=((offset%loop)+loop)%loop;render();
  });
  function end(){
   pointer=null;
   if(dragging){dragging=false;stage.classList.remove('is-drag');render();}
  }
  stage.addEventListener('pointerup',end);stage.addEventListener('pointercancel',end);stage.addEventListener('lostpointercapture',end);
  stage.addEventListener('dragstart',function(e){e.preventDefault();});
  stage.addEventListener('click',function(e){
   if(moved>7){e.preventDefault();e.stopPropagation();moved=0;}
  },true);
  stage.addEventListener('keydown',function(e){
   if(e.key==='ArrowRight'){offset+=pitch;render();}
   else if(e.key==='ArrowLeft'){offset-=pitch;render();}
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-bh-turn]'),function(b){
   b.addEventListener('click',function(){offset+=(b.dataset.bhTurn==='prev'?-pitch:pitch);offset=((offset%loop)+loop)%loop;render();});
  });
  if('IntersectionObserver'in window)new IntersectionObserver(function(es){visible=es[0].isIntersecting;},{threshold:0}).observe(stage);
  document.addEventListener('visibilitychange',function(){lastFrame=0;});
  window.addEventListener('resize',measure);
  if('ResizeObserver'in window)new ResizeObserver(measure).observe(stage);
  measure();requestAnimationFrame(animate);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();