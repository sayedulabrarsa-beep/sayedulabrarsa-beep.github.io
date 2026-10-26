(function(){
  var burger=document.getElementById('burger'),menu=document.getElementById('menu');
  if(burger&&menu){burger.addEventListener('click',function(){var o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});}
  var root=document.documentElement;
  var tg=document.getElementById('tgl');
  if(tg){tg.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
    var nx=cur==='dark'?'light':'dark';root.setAttribute('data-theme',nx);
    try{localStorage.setItem('sa-theme',nx)}catch(e){}});}
  var tr=document.getElementById('track');
  if(tr&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    var base=[].slice.call(tr.children);
    for(var r=0;r<3;r++)base.forEach(function(n){tr.appendChild(n.cloneNode(true))});
    [].slice.call(tr.children).forEach(function(n){tr.appendChild(n.cloneNode(true))});
    [].slice.call(tr.querySelectorAll('img')).forEach(function(im,k,a){if(k>=a.length/2){im.setAttribute('alt','');im.setAttribute('aria-hidden','true')}});
  }

  var brandTrack=document.getElementById('brandMarquee');
  if(brandTrack){
    [].slice.call(document.querySelectorAll('[data-scroll]')).forEach(function(btn){
      btn.addEventListener('click',function(){
        var direction=btn.getAttribute('data-scroll')==='right'?1:-1;
        brandTrack.scrollBy({left:direction*Math.max(240,brandTrack.clientWidth*.75),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
      });
    });
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
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
  var cp=document.getElementById('copy');
  if(cp){cp.addEventListener('click',function(){
    var el=document.getElementById('mail'),b=this;
    function done(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy email'},1500)}
    function sel(){var r=document.createRange();r.selectNodeContents(el);var g=getSelection();g.removeAllRanges();g.addRange(r)}
    try{navigator.clipboard.writeText(el.textContent).then(done,sel)}catch(e){sel()}
  });}
})();
