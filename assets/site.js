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
  var cp=document.getElementById('copy');
  if(cp){cp.addEventListener('click',function(){
    var el=document.getElementById('mail'),b=this;
    function done(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy email'},1500)}
    function sel(){var r=document.createRange();r.selectNodeContents(el);var g=getSelection();g.removeAllRanges();g.addRange(r)}
    try{navigator.clipboard.writeText(el.textContent).then(done,sel)}catch(e){sel()}
  });}
})();
