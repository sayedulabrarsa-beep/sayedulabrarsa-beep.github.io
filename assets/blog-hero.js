/* Pharma Blog: two-axis 3D spherical carousel with fixed card spacing. */
(function () {
  'use strict';
  function init() {
    var stage=document.getElementById('bh-stage');
    if(!stage||stage.dataset.carouselReady==='sphere')return;
    var ring=stage.querySelector('.bh-field'),grid=document.querySelector('.pb-featured-grid');
    if(!ring||!grid)return;
    var items=Array.prototype.slice.call(grid.querySelectorAll('.pb-feature-card')).map(function(card){
      var link=card.querySelector('h3 a')||card.querySelector('a[href]');
      if(!link)return null;
      var img=card.querySelector('img'),meta=card.querySelector('.pb-card-meta');
      return {href:link.getAttribute('href'),title:(link.textContent||'').replace(/\s+/g,' ').trim(),
        img:img?(img.currentSrc||img.getAttribute('src')):'',tag:meta?meta.textContent.split('·')[0].trim():'PHARMA BLOG',
        bn:!!card.querySelector('.pb-bangla-link')};
    }).filter(function(x){return x&&x.href&&x.title;});
    if(!items.length)return;
    stage.dataset.carouselReady='sphere';ring.innerHTML='';
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
      foot.appendChild(read);foot.appendChild(lang);body.appendChild(tag);body.appendChild(title);body.appendChild(foot);
      face.appendChild(body);a.appendChild(face);ring.appendChild(a);return a;
    });

    var n=cards.length,points=[],radius=300,yaw=0,pitch=0,vyaw=0,vpitch=0;
    var dragging=false,pointer=null,sx=0,sy=0,ly=0,lt=0,syaw=0,spitch=0,moved=0,last=0,visible=true;
    var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // Fibonacci sphere: near-uniform point distribution, independent of article order.
    var golden=Math.PI*(3-Math.sqrt(5));
    for(var i=0;i<n;i++){
      var yy=1-(2*(i+.5)/n),rr=Math.sqrt(Math.max(0,1-yy*yy)),theta=golden*i;
      points.push({x:Math.cos(theta)*rr,y:yy,z:Math.sin(theta)*rr});
    }
    function measure(){
      var w=stage.clientWidth,cw=w<540?136:w<900?184:236,ch=w<540?210:w<900?264:318;
      var gap=w<540?20:w<900?28:34;
      var spacing=Math.max(cw+gap,ch+gap);
      // Surface area per article determines the sphere radius; adding an article
      // expands the sphere, preserving the same minimum neighbour spacing.
      radius=spacing*Math.sqrt(n/(4*Math.PI))*1.16;
      var heading=document.querySelector('.bh-title'),fit=heading&&heading.querySelector('.bh-fit');
      if(heading&&fit){var room=heading.clientWidth-36;if(room>20){heading.style.fontSize='100px';var fw=fit.getBoundingClientRect().width;if(fw>room)heading.style.fontSize=Math.max(28,100*room/fw*.96)+'px';else heading.style.fontSize=Math.min(innerWidth>900?168:150,100*room/fw)+'px';}}
      draw();
    }
    function rotatePoint(p){
      var cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
      var x=p.x*cy+p.z*sy,z=-p.x*sy+p.z*cy;
      var y=p.y*cp-z*sp;z=p.y*sp+z*cp;
      return {x:x,y:y,z:z};
    }
    function draw(){
      cards.forEach(function(card,i){
        var p=rotatePoint(points[i]),x=p.x*radius,y=-p.y*radius,z=p.z*radius;
        var front=Math.max(0,Math.min(1,(p.z+.02)/.28));
        var scale=.88+.12*((p.z+1)/2);
        card.style.transform='translate3d('+x.toFixed(2)+'px,'+y.toFixed(2)+'px,'+z.toFixed(2)+'px) translate(-50%,-50%) scale('+scale.toFixed(3)+')';
        card.style.opacity=String(front);
        card.style.zIndex=String(Math.round((p.z+1)*1000));
        card.style.pointerEvents=dragging||p.z<.12?'none':'auto';
        card.setAttribute('aria-hidden',p.z<.12?'true':'false');
      });
    }
    function animate(t){
      if(!last)last=t;var dt=Math.min(40,t-last)/1000;last=t;
      if(visible&&!dragging&&!reduced){
        if(Math.abs(vyaw)>.006||Math.abs(vpitch)>.006){yaw+=vyaw*dt;pitch+=vpitch*dt;var decay=Math.pow(.035,dt);vyaw*=decay;vpitch*=decay;}
        else {yaw+=.12*dt;pitch+=.035*dt;}
        draw();
      }
      requestAnimationFrame(animate);
    }
    stage.addEventListener('pointerdown',function(e){
      if(e.pointerType==='mouse'&&e.button!==0)return;
      pointer=e.pointerId;sx=ly=e.clientX;sy=e.clientY;lt=e.timeStamp;syaw=yaw;spitch=pitch;moved=0;vyaw=vpitch=0;
    });
    stage.addEventListener('pointermove',function(e){
      if(pointer!==e.pointerId)return;
      var dx=e.clientX-sx,dy=e.clientY-sy;
      if(!dragging&&(Math.abs(dx)>5||Math.abs(dy)>5)){
        dragging=true;stage.classList.add('is-drag');
        try{stage.setPointerCapture(pointer);}catch(err){}
      }
      if(!dragging)return;if(e.cancelable)e.preventDefault();
      moved=Math.max(Math.abs(dx),Math.abs(dy));
      var scale=1/Math.max(180,stage.clientWidth);
      yaw=syaw+dx*scale*2.4;
      pitch=Math.max(-1.25,Math.min(1.25,spitch+dy*scale*2.4));
      var elapsed=Math.max(1,e.timeStamp-lt);
      vyaw=(e.clientX-ly)*scale*2.4/elapsed*1000;
      vpitch=(e.clientY-(stage._lastY===undefined?e.clientY:stage._lastY))*scale*2.4/elapsed*1000;
      ly=e.clientX;stage._lastY=e.clientY;lt=e.timeStamp;draw();
    });
    function end(){
      pointer=null;stage._lastY=undefined;
      if(dragging){dragging=false;stage.classList.remove('is-drag');draw();}
    }
    stage.addEventListener('pointerup',end);stage.addEventListener('pointercancel',end);stage.addEventListener('lostpointercapture',end);
    stage.addEventListener('dragstart',function(e){e.preventDefault();});
    stage.addEventListener('click',function(e){
      if(moved>7){e.preventDefault();e.stopPropagation();moved=0;return;}
      var card=e.target.closest&&e.target.closest('.bh-card');if(!card)return;
      var i=cards.indexOf(card),p=rotatePoint(points[i]);
      if(p.z<.72){e.preventDefault();yaw+=Math.atan2(-p.x,p.z);pitch=Math.max(-1.1,Math.min(1.1,pitch+Math.asin(Math.max(-1,Math.min(1,p.y)))));draw();}
    },true);
    stage.addEventListener('keydown',function(e){
      if(e.key==='ArrowLeft')vyaw=.8;else if(e.key==='ArrowRight')vyaw=-.8;
      else if(e.key==='ArrowUp')vpitch=.55;else if(e.key==='ArrowDown')vpitch=-.55;
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-bh-turn]'),function(b){
      b.addEventListener('click',function(){vyaw=(b.dataset.bhTurn==='prev'?1:-1)*.7;});
    });
    if('IntersectionObserver'in window)new IntersectionObserver(function(es){visible=es[0].isIntersecting;},{threshold:0}).observe(stage);
    document.addEventListener('visibilitychange',function(){last=0;});
    window.addEventListener('resize',measure);
    if('ResizeObserver'in window)new ResizeObserver(measure).observe(stage);
    measure();requestAnimationFrame(animate);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();