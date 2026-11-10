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
  function render(dx){
    var a=A[cur],n=a.slides.length+2,h,pg=((idx+1)/n*100)+'%',num=('0'+idx).slice(-2);
    var brand='<div class="sd-brand"><span>SAYEDUL ABRAR</span><i>sayedulabrar.site</i></div>';
    if(idx===0){
      h='<div class="sd sd-cover" style="--ac:'+a.accent+'"><div class="sd-in" style="flex:0 0 auto;padding-bottom:0">'+brand+'</div><img src="'+a.image+'" alt="" style="margin-top:3cqw"><div class="sd-in" style="padding-top:0"><span class="sd-kick" style="margin-top:3.5cqw">'+esc(a.kicker.toUpperCase())+'</span><h3>'+esc(a.title)+'</h3><p class="sd-meta">A pharmacist’s summary · '+esc(a.read)+' full read</p><span class="sd-swipe"><b>→</b> Swipe through</span></div></div>';
    }else if(idx===n-1){
      h='<div class="sd sd-end" style="--ac:'+a.accent+'">'+brand+'<div style="margin:auto 0"><h3>Want the full picture?</h3><p class="sd-p">This is a short summary of “'+esc(a.title)+'”. The full article has the sources, examples and FAQs.</p><div class="sd-cta"><a class="a1" href="/blog/'+a.slug+'/">Read in English ↗</a><a class="a2" lang="bn" href="/blog/'+a.bn+'">বাংলায় পড়ুন ↗</a></div></div><p class="sd-note">General education only. It does not replace advice from your doctor or pharmacist.</p></div>';
    }else{
      var s=a.slides[idx-1];
      h='<div class="sd" style="--ac:'+a.accent+';--pg:'+pg+'">'+brand+'<span class="sd-big" aria-hidden="true">'+num+'</span><h3>'+esc(s.h)+'</h3><ul>'+s.p.map(function(t){return'<li>'+esc(t)+'</li>'}).join('')+'</ul><div class="sd-foot"><em></em><span>'+num+'</span></div></div>';
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
