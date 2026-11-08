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
