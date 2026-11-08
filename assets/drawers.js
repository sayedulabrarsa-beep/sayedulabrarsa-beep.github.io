(function(){
  var b=document.getElementById('mdr-all');if(!b)return;
  var ds=[].slice.call(document.querySelectorAll('.mdr'));
  b.addEventListener('click',function(){
    var on=b.getAttribute('aria-pressed')!=='true';
    ds.forEach(function(d,i){setTimeout(function(){d.open=on;},i*110);});
    b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?'Close all drawers':'Open all drawers';
  });
})();
