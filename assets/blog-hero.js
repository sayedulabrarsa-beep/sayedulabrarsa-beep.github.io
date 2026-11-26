/* Responsive circular Pharma Blog carousel. New featured articles join automatically. */
(function () {
  'use strict';
  function init() {
    var stage=document.getElementById('bh-stage');
    if(!stage||stage.dataset.carouselReady==='1')return;
    var ring=stage.querySelector('.bh-field');
    var grid=document.querySelector('.pb-featured-grid');
    if(!ring||!grid)return;
    var items=Array.prototype.slice.call(grid.querySelectorAll('.pb-feature-card')).map(function(card){
      var link=card.querySelector('h3 a')||card.querySelector('a[href]');
      if(!link)return null;
      var img=card.querySelector('img'),meta=card.querySelector('.pb-card-meta');
      return {href:link.getAttribute('href'),title:(link.textContent||'').replace(/\s+/g,' ').trim(),
        img:img?(img.currentSrc||img.getAttribute('src')):'',tag:meta?meta.textContent.split('·')[0].trim():'PHARMA BLOG',
        bn:!!card.querySelector('.pb-bangla-link')};
    }).filter(function(x){return x&&x.href&&x.title;});
    if(!items.length){stage.classList.add('bh-no-carousel');return;}
    stage.dataset.carouselReady='1';
    ring.innerHTML='';
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
      foot.appendChild(read);foot.appendChild(lang);body.appendChild(tag);body.appendChild(title);body.appendChild(foot);face.appendChild(body);a.appendChild(face);ring.appendChild(a);return a;
    });
    var n=cards.length,step=360/n,radius=500,rotation=0,velocity=0,dragging=false,pointer=null;
    var sx=0,sy=0,sr=0,lx=0,lt=0,moved=0,last=0,visible=true;
    var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function measure(){
      var w=stage.clientWidth,cw=w<540?136:w<900?184:236,gap=w<540?18:w<900?26:30;
      radius=Math.max((cw+gap)/2,(cw+gap)/(2*Math.sin(Math.PI/n)));
      var heading=document.querySelector('.bh-title'),fit=heading&&heading.querySelector('.bh-fit');
      if(heading&&fit){var room=heading.clientWidth-36;if(room>20){heading.style.fontSize='100px';var fw=fit.getBoundingClientRect().width;if(fw>room)heading.style.fontSize=Math.max(28,100*room/fw*.96)+'px';else heading.style.fontSize=Math.min(innerWidth>900?168:150,100*room/fw)+'px';}}
      draw();
    }
    function angle(i){return i*step+rotation;}
    function draw(){
      cards.forEach(function(card,i){
        var a=angle(i),rad=a*Math.PI/180,f=Math.cos(rad),x=Math.sin(rad)*radius,z=(Math.cos(rad)-1)*radius;
        card.style.transform='translate3d('+x.toFixed(2)+'px,0,'+z.toFixed(2)+'px) rotateY('+a.toFixed(2)+'deg)';
        card.style.setProperty('--bh-op',Math.max(.12,Math.min(1,(f+.18)/.42)).toFixed(3));
        card.style.zIndex=String(Math.round((f+1)*1000));card.style.pointerEvents=dragging||f<-.05?'none':'auto';
        card.setAttribute('aria-hidden',f<-.05?'true':'false');
      });
    }
    function tick(t){
      if(!last)last=t;var dt=Math.min(40,t-last)/1000;last=t;
      if(visible&&!dragging&&!reduced){if(Math.abs(velocity)>.015){rotation+=velocity*dt;velocity*=Math.pow(.035,dt);}else rotation+=5.5*dt;draw();}
      requestAnimationFrame(tick);
    }
    stage.addEventListener('pointerdown',function(e){
      if(e.pointerType==='mouse'&&e.button!==0)return;
      pointer=e.pointerId;sx=lx=e.clientX;sy=e.clientY;sr=rotation;lt=e.timeStamp;moved=0;velocity=0;
    });
    stage.addEventListener('pointermove',function(e){
      if(pointer!==e.pointerId)return;var dx=e.clientX-sx,dy=e.clientY-sy;
      if(!dragging&&Math.abs(dx)>6&&Math.abs(dx)>Math.abs(dy)*1.08){dragging=true;stage.classList.add('is-drag');try{stage.setPointerCapture(pointer);}catch(err){}}
      if(!dragging)return;if(e.cancelable)e.preventDefault();moved=Math.abs(dx);
      var scale=180/(Math.PI*radius);rotation=sr+dx*scale;
      var elapsed=Math.max(1,e.timeStamp-lt);velocity=(e.clientX-lx)*scale/elapsed*1000;lx=e.clientX;lt=e.timeStamp;draw();
    });
    function end(){pointer=null;if(dragging){dragging=false;stage.classList.remove('is-drag');draw();}}
    stage.addEventListener('pointerup',end);stage.addEventListener('pointercancel',end);stage.addEventListener('lostpointercapture',end);
    stage.addEventListener('dragstart',function(e){e.preventDefault();});
    stage.addEventListener('click',function(e){
      if(moved>7){e.preventDefault();e.stopPropagation();moved=0;return;}
      var card=e.target.closest&&e.target.closest('.bh-card');if(!card)return;var i=cards.indexOf(card);
      if(Math.cos(angle(i)*Math.PI/180)<.72){e.preventDefault();var diff=((-i*step-rotation+540)%360)-180;velocity=diff*2.4;}
    },true);
    stage.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();velocity=(e.key==='ArrowLeft'?1:-1)*Math.min(34,step*2.5);}});
    Array.prototype.forEach.call(document.querySelectorAll('[data-bh-turn]'),function(b){b.addEventListener('click',function(){velocity=(b.dataset.bhTurn==='prev'?1:-1)*Math.min(34,step*2.5);});});
    if('IntersectionObserver'in window)new IntersectionObserver(function(es){visible=es[0].isIntersecting;},{threshold:0}).observe(stage);
    document.addEventListener('visibilitychange',function(){last=0;});window.addEventListener('resize',measure);
    if('ResizeObserver'in window)new ResizeObserver(measure).observe(stage);
    measure();requestAnimationFrame(tick);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();