(function(){
  var d=document.getElementById('st-data'),row=document.getElementById('st-row');
  if(!d||!row)return;
  var A;try{A=JSON.parse(d.textContent)}catch(e){return}
  var v,stage,cnt,prev,next,ttl,cur=0,idx=0,last=null,sx=null;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function slides(a){var n=a.slides.length+2;return {n:n}}
  function build(){
    v=document.createElement('div');v.className='sv';v.setAttribute('role','dialog');v.setAttribute('aria-modal','true');v.setAttribute('aria-label','Article summary');
    v.innerHTML='<div class="sv-top"><div><b id="sv-t"></b><span id="sv-c"></span></div><button class="sv-btn sv-x" type="button" aria-label="Close">✕</button></div>'+
      '<button class="sv-btn sv-prev" type="button" aria-label="Previous slide">←</button><div class="sv-stage" id="sv-s" aria-live="polite"></div><button class="sv-btn sv-next" type="button" aria-label="Next slide">→</button>';
    document.body.appendChild(v);
    stage=v.querySelector('#sv-s');cnt=v.querySelector('#sv-c');ttl=v.querySelector('#sv-t');prev=v.querySelector('.sv-prev');next=v.querySelector('.sv-next');
    v.querySelector('.sv-x').onclick=close;prev.onclick=function(){go(-1)};next.onclick=function(){go(1)};
    v.addEventListener('click',function(e){if(e.target===v)close()});
    v.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    v.addEventListener('touchend',function(e){if(sx==null)return;var dx=e.changedTouches[0].clientX-sx;sx=null;if(Math.abs(dx)>45)go(dx<0?1:-1)});
    document.addEventListener('keydown',function(e){if(!v.classList.contains('on'))return;
      if(e.key==='Escape')close();else if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1);
      else if(e.key==='Tab'){var f=v.querySelectorAll('button:not([disabled]),a[href]');if(!f.length)return;var a=f[0],b=f[f.length-1];
        if(e.shiftKey&&document.activeElement===a){e.preventDefault();b.focus()}else if(!e.shiftKey&&document.activeElement===b){e.preventDefault();a.focus()}}});
  }
  function tint(s){return s.dk?'--bg:'+s.bg+';--fg:#fff;--fg2:#ece6df;--mut:#b9b4ac;':'--bg:'+s.bg+';--fg:#172f2b;--fg2:#26332f;--mut:#5f6b66;'}
  function render(dx){
    var a=A[cur],n=a.slides.length+2,h,pg=((idx+1)/n*100)+'%',num=('0'+idx).slice(-2);
    var brand='<div class="sd-brand"><span>SAYEDUL ABRAR</span><i>sayedulabrar.site</i></div>';
    if(idx===0){
      h='<div class="sd sd-cover" style="--ac:'+a.accent+'"><img class="sd-bg" src="'+a.image+'" alt="">'+brand+'<div class="sd-ctitle"><span class="sd-kick">'+esc(a.kicker.toUpperCase())+'</span><h3>'+esc(a.title)+'</h3><p class="sd-meta">A pharmacist’s summary · '+esc(a.read)+' full read</p></div><div class="sd-swipe"><b>→</b> Swipe through</div><div class="sd-foot"><em style="--pg:'+pg+'"></em><span>01</span></div></div>';
    }else if(idx===n-1){
      var e=a.end;
      h='<div class="sd sd-end" style="'+tint(e)+'--ac:'+a.accent+'">'+brand+'<h3 class="sd-endh">'+esc(e.h)+'</h3><p class="sd-p">'+esc(e.t)+'</p><div class="sd-pic"><img src="'+e.img+'" alt="'+esc(e.alt)+'"></div><div class="sd-cta"><a class="a1" href="/blog/'+a.slug+'/">Read the full article ↗</a><a class="a2" lang="bn" href="/blog/'+a.bn+'">বাংলায় পড়ুন ↗</a></div><p class="sd-note">General education only. It does not replace advice from your doctor or pharmacist.</p></div>';
    }else{
      var s=a.slides[idx-1];
      h='<div class="sd" style="'+tint(s)+'--ac:'+a.accent+';--pg:'+pg+'">'+brand+'<span class="sd-big" aria-hidden="true">'+num+'</span><h3>'+esc(s.h)+'</h3>'+(s.sub?'<p class="sd-sub">'+esc(s.sub)+'</p>':'')+'<ul>'+s.p.map(function(t){return'<li>'+esc(t)+'</li>'}).join('')+'</ul>'+(s.r?'<p class="sd-res">'+esc(s.r)+'</p>':'')+'<div class="sd-pic'+(s.fit==='contain'?' sd-contain':'')+'"><img src="'+s.img+'" alt="'+esc(s.alt)+'"></div><div class="sd-foot"><em style="--pg:'+pg+'"></em><span>'+num+'</span></div></div>';
    }
    stage.style.setProperty('--dx',(dx||14)+'px');stage.innerHTML=h;
    ttl.textContent=a.kicker;cnt.textContent=(idx+1)+' / '+n;
    prev.disabled=idx===0;next.disabled=idx===n-1;
  }
  function go(s){var n=A[cur].slides.length+2,t=idx+s;if(t<0||t>=n)return;idx=t;render(s*14)}
  function open(i,btn){if(!v)build();cur=i;idx=0;last=btn;render();v.classList.add('on');document.documentElement.style.overflow='hidden';v.querySelector('.sv-x').focus()}
  function close(){v.classList.remove('on');document.documentElement.style.overflow='';if(last)last.focus()}
  row.addEventListener('click',function(e){var b=e.target.closest('.st-stack');if(b)open(+b.dataset.i,b)});
})();
/* Featured row: endless auto-drift, drag/swipe/scroll to take over, arrows + pause (stops for reduced-motion) */
(function(){
  var row=document.getElementById('st-row');if(!row)return;
  var items=[].slice.call(row.children);if(items.length<3)return;
  var wrap=row.parentNode,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function clone(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');c.setAttribute('data-clone','1');[].forEach.call(c.querySelectorAll('button,a'),function(x){x.tabIndex=-1});return c}
  var before=document.createDocumentFragment(),after=document.createDocumentFragment();
  items.forEach(function(li){before.appendChild(clone(li));after.appendChild(clone(li))});
  row.insertBefore(before,row.firstChild);row.appendChild(after);
  row.classList.add('st-live');
  var A,W,lo,paused=false,userPause=false,idle=0,vis=true,raf=0,last=0,drag=null,speed=0.035;
  function measure(){var f=items[0],cs=getComputedStyle(row);A=f.offsetLeft;W=row.children[items.length*2].offsetLeft-f.offsetLeft;lo=A-parseFloat(cs.paddingLeft||0)}
  function norm(){var s=row.scrollLeft;if(s>=lo+W)row.scrollLeft=s-W;else if(s<lo)row.scrollLeft=s+W}
  function start(){measure();row.scrollLeft=lo}
  var hold=function(ms){idle=performance.now()+(ms||2600)};
  /* sub-pixel drift: scrollLeft rounds on some browsers, so accumulate */
  var acc=0;function tick(t){raf=requestAnimationFrame(tick);var dt=Math.min(40,t-(last||t));last=t;var v=document.querySelector('.sv.on');
    if(!reduce&&!userPause&&!drag&&vis&&!v&&t>idle&&!document.hidden){acc+=speed*dt;if(acc>=1){var n=Math.floor(acc);row.scrollLeft+=n;acc-=n}}norm()}
  ['pointerenter','focusin'].forEach(function(e){row.addEventListener(e,function(ev){if(ev.type==='pointerenter'&&ev.pointerType!=='mouse')return;hold(1e9)})});
  ['pointerleave','focusout'].forEach(function(e){row.addEventListener(e,function(ev){if(ev.type==='pointerleave'&&ev.pointerType!=='mouse')return;hold(1200)})});
  row.addEventListener('touchstart',function(){hold(3500)},{passive:true});row.addEventListener('touchmove',function(){hold(3500)},{passive:true});
  row.addEventListener('wheel',function(){hold(3000)},{passive:true});
  row.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){hold(4000)}});
  /* mouse drag to scroll */
  row.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0)return;drag={x:e.clientX,s:row.scrollLeft,m:false}});
  window.addEventListener('pointermove',function(e){if(!drag)return;var dx=e.clientX-drag.x;if(Math.abs(dx)>5)drag.m=true;if(drag.m){row.scrollLeft=drag.s-dx;row.classList.add('st-drag')}});
  window.addEventListener('pointerup',function(){if(!drag)return;var m=drag.m;drag=null;row.classList.remove('st-drag');hold(2500);if(m){row._moved=1;setTimeout(function(){row._moved=0},60)}});
  row.addEventListener('click',function(e){if(row._moved){e.stopPropagation();e.preventDefault()}},true);
  /* controls */
  var ctl=document.createElement('div');ctl.className='st-ctl';
  ctl.innerHTML='<button type="button" class="st-cb" data-d="-1" aria-label="Previous articles">←</button><button type="button" class="st-cb st-pp" aria-label="Pause auto-scroll" aria-pressed="false">❚❚</button><button type="button" class="st-cb" data-d="1" aria-label="Next articles">→</button>';
  wrap.parentNode.insertBefore(ctl,wrap.nextSibling);
  function step(d){var w=(items[0].getBoundingClientRect().width||300)+34;hold(4000);row.scrollTo({left:row.scrollLeft+d*w*1.5,behavior:reduce?'auto':'smooth'})}
  ctl.addEventListener('click',function(e){var b=e.target.closest('.st-cb');if(!b)return;if(b.dataset.d){step(+b.dataset.d)}else{userPause=!userPause;b.setAttribute('aria-pressed',userPause);b.textContent=userPause?'▶':'❚❚';b.setAttribute('aria-label',userPause?'Play auto-scroll':'Pause auto-scroll')}});
  if(reduce){var p=ctl.querySelector('.st-pp');userPause=true;p.setAttribute('aria-pressed','true');p.textContent='▶';p.setAttribute('aria-label','Play auto-scroll')}
  if('IntersectionObserver' in window)new IntersectionObserver(function(en){vis=en[0].isIntersecting},{threshold:.05}).observe(row);
  var hint=document.querySelector('.st-hint');if(hint)hint.textContent='Moves on its own. Swipe, drag or scroll sideways any time →';
  function init(){start();hold(1200);if(!raf)raf=requestAnimationFrame(tick)}
  if(document.readyState==='complete')init();else window.addEventListener('load',init);
  window.addEventListener('resize',function(){var r=(row.scrollLeft-lo)/W;measure();row.scrollLeft=lo+r*W});
})();
