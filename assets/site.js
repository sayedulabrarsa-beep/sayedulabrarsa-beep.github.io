(function(){
  var root=document.documentElement;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* light / dark button */
  var tg=document.getElementById('tgl');
  if(tg){tg.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
    var nx=cur==='dark'?'light':'dark';root.setAttribute('data-theme',nx);
    try{localStorage.setItem('sa-theme',nx)}catch(e){}});}

  /* phone menu row: scroll so the current page link is in view */
  var cur=document.querySelector('.menu a[aria-current="page"]');
  if(cur){var nv=cur.closest('nav');
    if(nv&&nv.scrollWidth>nv.clientWidth){nv.scrollLeft=Math.max(0,cur.offsetLeft-(nv.clientWidth-cur.offsetWidth)/2)}}

  /* sliding strips. data-dir="right" (default) moves left to right; speed in px per second */
  function loop(track,speed,after){
    var base=[].slice.call(track.children);
    if(!base.length)return;
    var box=track.parentNode;
    var guard=0;
    function width(){return track.scrollWidth}
    while(width()<box.clientWidth*1.2&&guard<8){
      base.forEach(function(n){var c=n.cloneNode(true);track.appendChild(c)});guard++}
    var half=[].slice.call(track.children);
    half.forEach(function(n){var c=n.cloneNode(true);track.appendChild(c)});
    [].slice.call(track.children).forEach(function(n,k,a){
      if(k>=base.length){
        n.setAttribute('aria-hidden','true');
        [].slice.call(n.querySelectorAll('img')).forEach(function(im){im.setAttribute('alt','')});
        [].slice.call(n.querySelectorAll('a')).forEach(function(l){l.setAttribute('tabindex','-1')});
      }
    });
    function setDur(){
      var w=track.scrollWidth/2;
      track.style.setProperty('--dur',Math.max(20,Math.round(w/speed))+'s');
      if(box.getAttribute('data-dir')==='left'){track.style.animationDirection='reverse'}
    }
    setDur();
    [].slice.call(track.querySelectorAll('img')).forEach(function(im){if(!im.complete)im.addEventListener('load',setDur)});
  }
  if(!reduce){
    var t=document.getElementById('track');
    if(t){loop(t,55)}
    [].slice.call(document.querySelectorAll('.strip-track')).forEach(function(el){loop(el,45)});
  }

  /* brand portfolio carousel */
  var brandTrack=document.getElementById('brandMarquee');
  if(brandTrack){
    [].slice.call(document.querySelectorAll('[data-scroll]')).forEach(function(btn){
      btn.addEventListener('click',function(){
        var direction=btn.getAttribute('data-scroll')==='right'?1:-1;
        brandTrack.scrollBy({left:direction*Math.max(240,brandTrack.clientWidth*.75),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
      });
    });
    var paused=false;
    brandTrack.addEventListener('mouseenter',function(){paused=true});
    brandTrack.addEventListener('mouseleave',function(){paused=false});
    brandTrack.addEventListener('focusin',function(){paused=true});
    brandTrack.addEventListener('focusout',function(){paused=false});
    if(!reduce){
      var last=0;
      function moveBrands(now){
        if(!last)last=now;
        var dt=Math.min(now-last,40);last=now;
        if(!paused && !document.hidden && brandTrack.scrollWidth>brandTrack.clientWidth){
          brandTrack.scrollLeft+=dt*.025;
          if(brandTrack.scrollLeft+brandTrack.clientWidth>=brandTrack.scrollWidth-2)brandTrack.scrollLeft=0;
        }
        requestAnimationFrame(moveBrands);
      }
      requestAnimationFrame(moveBrands);
    }
  }

  /* Centered personal header, icon navigation, continuously moving swipeable menu and site search */
  (function(){
    var header=document.querySelector('header'),bar=header&&header.querySelector('.bar'),nav=header&&header.querySelector('nav'),menu=nav&&nav.querySelector('.menu');
    if(!bar||!nav||!menu)return;
    var logo=bar.querySelector('.logo'),theme=bar.querySelector('.tgl');
    if(!bar.querySelector('.site-search-toggle')){
      var searchBtn=document.createElement('button');searchBtn.type='button';searchBtn.className='site-search-toggle';searchBtn.setAttribute('aria-label','Open site search');searchBtn.setAttribute('aria-expanded','false');
      searchBtn.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.6"></circle><path d="m16 16 5 5"></path></svg>';
      bar.insertBefore(searchBtn,logo||bar.firstChild);
      var form=document.createElement('form');form.className='site-search-form';form.setAttribute('role','search');form.hidden=true;
      form.innerHTML='<label class="visually-hidden" for="site-search-input">Search this website</label><input id="site-search-input" type="search" placeholder="Search Sayedul Abrar…" autocomplete="off"><button type="submit">Search</button>';
      bar.appendChild(form);
      searchBtn.addEventListener('click',function(){var open=form.hidden;form.hidden=!open;searchBtn.setAttribute('aria-expanded',String(open));if(open)form.querySelector('input').focus()});
      form.addEventListener('submit',function(e){e.preventDefault();var q=form.querySelector('input').value.trim();if(q)location.href='/search/?q='+encodeURIComponent(q)});
    }
    if(logo)logo.setAttribute('aria-label','Sayedul Abrar home');
    var icons={
      '/':'<path d="m3 10 9-7 9 7"></path><path d="M5 9v11h14V9M9 20v-6h6v6"></path>',
      '/about/':'<circle cx="12" cy="8" r="4"></circle><path d="M4 21a8 8 0 0 1 16 0"></path>',
      '/experience/':'<rect x="3" y="7" width="18" height="13" rx="2"></rect><path d="M8 7V4h8v3M3 12h18M10 12v2h4v-2"></path>',
      '/achievements/':'<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM7 6H4v2a4 4 0 0 0 4 4M17 6h3v2a4 4 0 0 1-4 4"></path>',
      '/education/':'<path d="m2 9 10-5 10 5-10 5zM6 11v5c4 3 8 3 12 0v-5M22 9v6"></path>',
      '/learning/':'<path d="M4 5.5A3.5 3.5 0 0 1 7.5 2H20v17H7.5A3.5 3.5 0 0 0 4 22zM4 5.5V22M8 6h8M8 10h8"></path>',
      '/publications/':'<path d="M6 3h9l4 4v14H6zM15 3v5h4M9 12h7M9 16h7"></path>',
      '/community/':'<circle cx="9" cy="8" r="3"></circle><circle cx="17" cy="9" r="2.5"></circle><path d="M2 20a7 7 0 0 1 14 0M15 15a5 5 0 0 1 7 5"></path>',
      '/blog/':'<path d="M4 4h16v16H4zM8 8h8M8 12h8M8 16h5"></path>',
      '/vlog/':'<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="m10 9 5 3-5 3z"></path>',
      '/contact/':'<rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="m4 7 8 6 8-6"></path>',
      '/portfolio/':'<rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M7 8h10M7 12h10M7 16h6"></path>'
    };
    Array.prototype.forEach.call(menu.querySelectorAll('a'),function(a){
      if(a.dataset.iconApplied)return;
      var path=new URL(a.getAttribute('href'),location.origin).pathname;
      var shape=icons[path];if(!shape)return;
      var svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');svg.classList.add('nav-icon');svg.innerHTML=shape;
      a.insertBefore(svg,a.firstChild);a.dataset.iconApplied='true';
    });
    if(!menu.dataset.marqueeReady){
      menu.dataset.marqueeReady='true';
      var originals=Array.prototype.slice.call(menu.children),baseWidth=0,pausedUntil=0,last=0;
      originals.forEach(function(li){li.dataset.originalNav='true'});
      originals.forEach(function(li){var copy=li.cloneNode(true);copy.setAttribute('aria-hidden','true');copy.querySelectorAll('a,button').forEach(function(el){el.setAttribute('tabindex','-1')});menu.appendChild(copy)});
      function measure(){baseWidth=0;originals.forEach(function(li){baseWidth+=li.getBoundingClientRect().width});nav.scrollLeft=0;}
      measure();window.addEventListener('resize',measure,{passive:true});
      function pause(){pausedUntil=performance.now()+4500}
      nav.addEventListener('touchstart',pause,{passive:true});nav.addEventListener('wheel',pause,{passive:true});nav.addEventListener('pointerdown',pause,{passive:true});nav.addEventListener('keydown',pause);
      if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
        function animate(now){if(!last)last=now;var dt=Math.min(40,now-last);last=now;
          if(!document.hidden&&now>pausedUntil&&baseWidth>nav.clientWidth+5){nav.scrollLeft+=dt*.045;if(nav.scrollLeft>=baseWidth)nav.scrollLeft=0}
          requestAnimationFrame(animate)}
        requestAnimationFrame(animate);
      }
    }
  })();

  /* copy email */
  var cp=document.getElementById('copy');
  if(cp){cp.addEventListener('click',function(){
    var el=document.getElementById('mail'),b=this;
    function done(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy email'},1500)}
    function sel(){var r=document.createRange();r.selectNodeContents(el);var g=getSelection();g.removeAllRanges();g.addRange(r)}
    try{navigator.clipboard.writeText(el.textContent).then(done,sel)}catch(e){sel()}
  });}
})();
