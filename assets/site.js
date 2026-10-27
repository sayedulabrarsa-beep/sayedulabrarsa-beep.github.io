(function(){
  var root=document.documentElement;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Apply saved theme consistently on every page and viewport. */
  var tg=document.getElementById('tgl');
  function applyTheme(theme){
    if(theme!=='light'&&theme!=='dark')return;
    root.setAttribute('data-theme',theme);
    if(tg){
      tg.textContent=theme==='dark'?'☾':'☼';
      tg.setAttribute('aria-label',theme==='dark'?'Switch to light mode':'Switch to dark mode');
      tg.setAttribute('title',theme==='dark'?'Switch to light mode':'Switch to dark mode');
    }
  }
  var initialTheme='';
  try{initialTheme=localStorage.getItem('sa-theme')||''}catch(e){}
  if(initialTheme!=='light'&&initialTheme!=='dark'){
    initialTheme=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  }
  applyTheme(initialTheme);
  if(tg){tg.addEventListener('click',function(){
    var current=root.getAttribute('data-theme')||initialTheme;
    var next=current==='dark'?'light':'dark';
    applyTheme(next);
    try{localStorage.setItem('sa-theme',next)}catch(e){}
  });}

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
    if(!menu.dataset.navStableReady){
      menu.dataset.navStableReady='true';
      /* Keep one real, swipeable row. Move gently right-to-left, pause for people,
         and never clone links or interfere with manual scrolling and taps. */
      var active=menu.querySelector('a[aria-current="page"]');
      function revealActive(){
        if(!active)return;
        var navRect=nav.getBoundingClientRect(),linkRect=active.getBoundingClientRect();
        if(linkRect.left<navRect.left||linkRect.right>navRect.right){
          nav.scrollLeft+=linkRect.left-navRect.left-(nav.clientWidth-linkRect.width)/2;
        }
      }
      requestAnimationFrame(revealActive);
      window.addEventListener('load',revealActive,{once:true});
      if(document.fonts&&document.fonts.ready){document.fonts.ready.then(revealActive).catch(function(){});}
      /* Preserve the user's scroll position on resize instead of returning to Home. */
      var previousWidth=window.innerWidth;
      window.addEventListener('resize',function(){
        if(Math.abs(window.innerWidth-previousWidth)>80){previousWidth=window.innerWidth;}
      },{passive:true});
      var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var navPaused=false,navLast=0;
      nav.addEventListener('pointerenter',function(){navPaused=true});
      nav.addEventListener('pointerleave',function(){navPaused=false});
      nav.addEventListener('focusin',function(){navPaused=true});
      nav.addEventListener('focusout',function(){navPaused=false});
      nav.addEventListener('touchstart',function(){navPaused=true},{passive:true});
      nav.addEventListener('touchend',function(){window.setTimeout(function(){navPaused=false},1400)},{passive:true});
      if(!reduced){
        function scrollMenu(now){
          if(!navLast)navLast=now;
          var dt=Math.min(now-navLast,40);navLast=now;
          if(!navPaused&&!document.hidden&&nav.scrollWidth>nav.clientWidth){
            nav.scrollLeft+=dt*.012;
            if(nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-2)nav.scrollLeft=0;
          }
          requestAnimationFrame(scrollMenu);
        }
        requestAnimationFrame(scrollMenu);
      }
    }
  })();

  /* On narrow screens place the focus icons after the quote/details row.
     Restore the original parent on wider screens so desktop layout remains intact. */
  (function(){
    var mq=window.matchMedia('(max-width: 700px)');
    var shell=document.querySelector('.hero-redesign .hero-shell');
    var copy=shell&&shell.querySelector('.hero-copy');
    var pillars=copy&&copy.querySelector('.hero-pillars');
    var detail=shell&&shell.querySelector('.hero-details');
    if(!shell||!copy||!pillars||!detail)return;
    function arrange(){
      if(mq.matches){
        if(pillars.parentElement!==shell)shell.appendChild(pillars);
      }else{
        if(pillars.parentElement!==copy)copy.appendChild(pillars);
      }
    }
    arrange();
    if(mq.addEventListener)mq.addEventListener('change',arrange);
    else if(mq.addListener)mq.addListener(arrange);
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
