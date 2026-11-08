(function(){
  var cab=document.getElementById('cab');if(!cab)return;
  var dlgs=[].slice.call(document.querySelectorAll('.cab-dlg'));
  var dws=[].slice.call(cab.querySelectorAll('.dw'));
  var allBtn=document.getElementById('cab-all');
  var cur=-1,lastBtn=null;

  /* ---- drawers ---- */
  function setOpen(dw,on){
    dw.classList.toggle('is-open',on);
    dw.querySelector('.dw-toggle').setAttribute('aria-expanded',on?'true':'false');
    dw.querySelector('.dw-view').tabIndex=on?0:-1;
    var cta=dw.querySelector('.dw-cta'),t=dw.querySelector('.dw-cta-t');
    cta.tabIndex=on?-1:0;
    cta.setAttribute('aria-hidden',on?'true':'false');
    if(t)t.textContent='Open to see my portfolio';
  }
  dws.forEach(function(dw){setOpen(dw,false);});
  function syncAll(){
    var all=dws.every(function(d){return d.classList.contains('is-open');});
    if(allBtn){allBtn.setAttribute('aria-pressed',all?'true':'false');allBtn.textContent=all?'Close all drawers':'Open all drawers';}
  }
  cab.addEventListener('click',function(ev){
    var dw=ev.target.closest('.dw');if(!dw)return;
    if(ev.target.closest('.dw-x')){setOpen(dw,false);var tg=dw.querySelector('.dw-toggle');if(tg)tg.focus({preventScroll:true});syncAll();return;}
    if(ev.target.closest('.dw-view')){lastBtn=dw.querySelector('.dw-view');show(dws.indexOf(dw));return;}
    if(ev.target.closest('.dw-toggle')||ev.target.closest('.dw-cta')||ev.target.closest('.dw-front')){
      var open=dw.classList.contains('is-open');
      if(!open){
        setOpen(dw,true);syncAll();
        setTimeout(function(){var v=dw.querySelector('.dw-view');if(v)v.focus({preventScroll:true});},650);
      }else if(ev.target.closest('.dw-toggle')){setOpen(dw,false);syncAll();}
    }
  });
  if(allBtn)allBtn.addEventListener('click',function(){
    var on=allBtn.getAttribute('aria-pressed')!=='true';
    dws.forEach(function(d,i){setTimeout(function(){setOpen(d,on);syncAll();},i*140);});
  });

  /* ---- detail dialog ---- */
  function show(i){
    var d=dlgs[i];if(!d)return;cur=i;
    if(typeof d.showModal==='function'){if(!d.open)d.showModal();}else{d.setAttribute('open','');}
    document.documentElement.style.overflow='hidden';
    var s=d.querySelector('.cab-dlg-side'),m=d.querySelector('.cab-dlg-main');
    if(s)s.scrollTop=0;if(m)m.scrollTop=0;
  }
  function hide(d){if(d.open&&typeof d.close==='function')d.close();else d.removeAttribute('open');}
  function go(step){
    if(cur<0)return;var from=cur,n=(from+step+dlgs.length)%dlgs.length;
    if(dws[n])setOpen(dws[n],true);syncAll();
    hide(dlgs[from]);show(n);
  }
  dlgs.forEach(function(d){
    d.addEventListener('click',function(ev){
      if(ev.target===d){hide(d);return;}
      if(ev.target.closest('[data-cab-close]'))hide(d);
      else if(ev.target.closest('[data-cab-prev]'))go(-1);
      else if(ev.target.closest('[data-cab-next]'))go(1);
    });
    d.addEventListener('close',function(){
      setTimeout(function(){
        if(!dlgs.some(function(x){return x.open;})){
          document.documentElement.style.overflow='';cur=-1;
          if(lastBtn)try{lastBtn.focus({preventScroll:true});}catch(e){}
        }
      },0);
    });
    d.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowLeft')go(-1);else if(ev.key==='ArrowRight')go(1);
    });
  });
})();

/* partner-wall tabs */
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.pw-tabs [role=tab]'));if(!tabs.length)return;
  var wall=document.querySelector('.pw2');wall.classList.add('pw-js');
  function sel(t){tabs.forEach(function(x){
    var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;
    var p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!on;});}
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){sel(t);});
    t.addEventListener('keydown',function(ev){
      var n=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(!n)return;
      var x=tabs[(i+n+tabs.length)%tabs.length];sel(x);x.focus();});
  });
  sel(tabs[0]);
})();
/* quotes, one by one */
(function(){
  var card=document.getElementById('pq');if(!card)return;
  var sl=[].slice.call(card.querySelectorAll('.pq-s')),dots=[].slice.call(card.querySelectorAll('.pq-dots button'));
  var cur=0,timer=null,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(n){
    n=(n+sl.length)%sl.length;
    sl.forEach(function(s,i){s.hidden=i!==n;s.classList.toggle('is-on',i===n);});
    dots.forEach(function(d,i){if(i===n)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
    cur=n;
  }
  function play(){stop();if(reduce)return;timer=setInterval(function(){show(cur+1);},8000);}
  function stop(){if(timer){clearInterval(timer);timer=null;}}
  card.querySelector('.pq-prev').addEventListener('click',function(){show(cur-1);play();});
  card.querySelector('.pq-next').addEventListener('click',function(){show(cur+1);play();});
  dots.forEach(function(d,i){d.addEventListener('click',function(){show(i);play();});});
  card.addEventListener('mouseenter',stop);card.addEventListener('mouseleave',play);
  card.addEventListener('focusin',stop);card.addEventListener('focusout',play);
  play();
})();
