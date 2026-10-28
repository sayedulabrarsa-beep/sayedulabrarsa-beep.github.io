(function(){
  var root=document.documentElement;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* The site uses one fixed light theme. Drop any theme saved by older versions. */
  root.removeAttribute('data-theme');
  try{localStorage.removeItem('sa-theme')}catch(e){}

  /* Header height is used to size the first screen (70% home hero, 30% next section). */
  var hdr=document.querySelector('header');
  function setHdr(){if(hdr)root.style.setProperty('--hdr',hdr.offsetHeight+'px')}
  setHdr();addEventListener('resize',setHdr);addEventListener('load',setHdr);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(setHdr);

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
    menu.querySelectorAll('a').forEach(function(a){if(new URL(a.getAttribute('href'),location.origin).pathname==='/community/'){var li=a.closest('li');if(li)li.remove();}});
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
      /* Seamless right-to-left marquee: start at the right edge, then repeat the full menu without a blank gap. */
      var navMotionOK=!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
      var originalItems=Array.prototype.slice.call(menu.children);
      /* One real menu only: Home starts at the left, moves right-to-left, then restarts from the right.
         Do not clone links; this prevents duplicated Home-to-Portfolio navigation items. */
      if(navMotionOK&&originalItems.length){
        menu.style.willChange='transform';
        menu.style.width='max-content';
        menu.style.flexWrap='nowrap';
        menu.style.justifyContent='flex-start';
        nav.style.overflow='hidden';
        nav.style.scrollBehavior='auto';
        var navBaseWidth=0,navLastFrame=0,navOffset=0;
        function measureNavigation(){
          navBaseWidth=menu.scrollWidth;
          navOffset=0;
          menu.style.transform='translate3d(0px,0,0)';
          navLastFrame=0;
        }
        function moveNavigation(now){
          if(!navLastFrame)navLastFrame=now;
          var elapsed=Math.min(now-navLastFrame,40);navLastFrame=now;
          if(!document.hidden&&!navAutoPaused&&navBaseWidth>0){
            navOffset-=elapsed*0.035;
            /* After the single Home-to-Portfolio menu has fully exited left, restart Home at the right edge. */
            if(navOffset<=-navBaseWidth)navOffset=nav.clientWidth;
            menu.style.transform='translate3d('+navOffset+'px,0,0)';
          }
          window.requestAnimationFrame(moveNavigation);
        }
        var navAutoPaused=false;
        nav.addEventListener('pointerenter',function(){navAutoPaused=true});
        nav.addEventListener('pointerleave',function(){navAutoPaused=false});
        nav.addEventListener('focusin',function(){navAutoPaused=true});
        nav.addEventListener('focusout',function(){navAutoPaused=false});
        nav.addEventListener('touchstart',function(){navAutoPaused=true},{passive:true});
        nav.addEventListener('touchend',function(){window.setTimeout(function(){navAutoPaused=false},1600)},{passive:true});
        measureNavigation();
        window.addEventListener('resize',measureNavigation,{passive:true});
        window.requestAnimationFrame(moveNavigation);
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

  /* Requested full-screen navigation overlay, using the existing navigation links */
  (function(){
    var header=document.querySelector('header'),bar=header&&header.querySelector('.bar'),nav=header&&header.querySelector('nav'),menu=nav&&nav.querySelector('.menu');
    if(!header||!bar||!menu||document.querySelector('.site-menu-toggle'))return;
    var btn=document.createElement('button');btn.type='button';btn.className='site-menu-toggle';btn.setAttribute('aria-label','Open navigation menu');btn.setAttribute('aria-expanded','false');btn.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"></path></svg>';
    var search=bar.querySelector('.site-search-toggle');if(search&&search.parentNode===bar)search.insertAdjacentElement('afterend',btn);else bar.appendChild(btn);
    var overlay=document.createElement('div');overlay.className='site-nav-overlay';overlay.id='site-nav-overlay';overlay.setAttribute('aria-hidden','true');
    var close=document.createElement('button');close.type='button';close.className='site-nav-overlay-close';close.setAttribute('aria-label','Close navigation menu');close.innerHTML='&times;';
    var card=document.createElement('div');card.className='site-nav-card';
    var profile=document.createElement('div');profile.className='site-nav-overlay-profile';
    var img=document.createElement('img');img.src='/assets/img/sayedul-abrar.jpg';img.alt='Sayedul Abrar';img.loading='lazy';
    var h=document.createElement('h2');h.textContent="Hello, I'm Sayedul Abrar";
    var p=document.createElement('p');p.textContent='Pharmacist · Product Executive · Lifelong learner. Explore my professional journey, pharmacy articles and work.';
    profile.appendChild(img);profile.appendChild(h);profile.appendChild(p);
    var links=document.createElement('nav');links.className='site-nav-overlay-links';links.setAttribute('aria-label','Expanded navigation');
    Array.prototype.forEach.call(menu.querySelectorAll('a'),function(a){if(new URL(a.getAttribute('href'),location.origin).pathname==='/community/')return;var clone=a.cloneNode(true);clone.removeAttribute('data-icon-applied');clone.querySelectorAll('.nav-icon').forEach(function(i){i.remove()});clone.removeAttribute('style');if(a.hasAttribute('aria-current'))clone.setAttribute('aria-current','page');links.appendChild(clone)});
    var contact=document.createElement('a');contact.href='/contact/';contact.className='overlay-contact';contact.textContent='Get in touch ↗';links.appendChild(contact);
    card.appendChild(close);card.appendChild(profile);card.appendChild(links);overlay.appendChild(card);document.body.appendChild(overlay);
    function open(){overlay.classList.add('is-open');overlay.setAttribute('aria-hidden','false');document.body.classList.add('nav-overlay-open');btn.setAttribute('aria-expanded','true');btn.setAttribute('aria-label','Close navigation menu');close.focus()}
    function shut(){overlay.classList.remove('is-open');overlay.setAttribute('aria-hidden','true');document.body.classList.remove('nav-overlay-open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label','Open navigation menu');btn.focus()}
    btn.addEventListener('click',function(){overlay.classList.contains('is-open')?shut():open()});close.addEventListener('click',shut);
    overlay.addEventListener('click',function(e){if(e.target===overlay)shut()});
    overlay.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){overlay.classList.remove('is-open');overlay.setAttribute('aria-hidden','true');document.body.classList.remove('nav-overlay-open')})});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&overlay.classList.contains('is-open'))shut()});
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
