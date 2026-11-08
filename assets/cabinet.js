(function(){
  var cab=document.getElementById('cab');if(!cab)return;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dlgs=[].slice.call(document.querySelectorAll('.cab-dlg'));
  var cur=-1,lastBtn=null;

  /* doors: closed until the cabinet scrolls into view, then swing open */
  cab.classList.add('cab-js');
  function openDoors(){
    if(cab.classList.contains('is-open'))return;
    cab.classList.add('is-open');
    setTimeout(function(){cab.classList.add('cab-ready');},reduce?0:2400);
  }
  if(reduce||!('IntersectionObserver' in window)){openDoors();}
  else{
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){openDoors();io.disconnect();}});},{threshold:.35});
    io.observe(cab);
    setTimeout(openDoors,6000);
  }

  function show(i){
    var d=dlgs[i];if(!d)return;cur=i;
    if(typeof d.showModal==='function'){if(!d.open)d.showModal();}else{d.setAttribute('open','');}
    document.documentElement.style.overflow='hidden';
    var s=d.querySelector('.cab-dlg-side'),m=d.querySelector('.cab-dlg-main');
    if(s)s.scrollTop=0;if(m)m.scrollTop=0;
  }
  function hide(d){
    if(d.open&&typeof d.close==='function')d.close();else d.removeAttribute('open');
  }
  function go(step){
    var from=cur;if(from<0)return;
    var n=(from+step+dlgs.length)%dlgs.length;
    hide(dlgs[from]);show(n);
  }

  cab.addEventListener('click',function(ev){
    var b=ev.target.closest('[data-cab-open]');if(!b)return;
    lastBtn=b;show(dlgs.indexOf(document.getElementById(b.getAttribute('data-cab-open'))));
  });
  dlgs.forEach(function(d){
    d.addEventListener('click',function(ev){
      if(ev.target===d){hide(d);return;}
      if(ev.target.closest('[data-cab-close]'))hide(d);
      else if(ev.target.closest('[data-cab-prev]'))go(-1);
      else if(ev.target.closest('[data-cab-next]'))go(1);
    });
    d.addEventListener('close',function(){
      /* a plain close (not prev/next) releases the page scroll and returns focus */
      setTimeout(function(){
        if(!dlgs.some(function(x){return x.open;})){
          document.documentElement.style.overflow='';cur=-1;
          if(lastBtn)try{lastBtn.focus({preventScroll:true});}catch(e){}
        }
      },0);
    });
    d.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowLeft'){go(-1);}else if(ev.key==='ArrowRight'){go(1);}
    });
  });
})();
