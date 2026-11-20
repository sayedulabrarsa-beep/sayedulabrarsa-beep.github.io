/* Pharma Blog hero: article cards orbiting a vertical axis in a spiral (double-sided: article in
   front, patterned back behind). Built from the article grid, so new articles join automatically.
   The ring turns on its own, with page scroll, with a sideways drag/swipe, or the arrow keys. */
(function () {
  var stage = document.getElementById('bh-stage');
  if (!stage) return;

  // headline spans the hero width whichever font has loaded
  var h1 = document.querySelector('.bh-title'), fitEl = h1 && h1.querySelector('.bh-fit');
  function fit() {
    if (!fitEl) return;
    h1.style.fontSize = '100px';
    var cs = getComputedStyle(h1), w = fitEl.getBoundingClientRect().width, room = h1.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 28;
    if (w > 0) h1.style.fontSize = Math.min(window.innerWidth > 900 ? 168 : 150, Math.floor(100 * room / w * 0.95)) + 'px';
    for (var k = 0; k < 30 && fitEl.getBoundingClientRect().width > room; k++) h1.style.fontSize = (parseFloat(h1.style.fontSize) - 3) + 'px';
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', fit); setTimeout(fit, 1500); setTimeout(fit, 4000);

  var ring = stage.querySelector('.bh-field');
  var src = Array.prototype.slice.call(document.querySelectorAll('.pb-featured-grid .pb-feature-card'));
  if (!src.length) { stage.style.display = 'none'; return; }
  function txt(el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; }

  var data = [];
  src.forEach(function (c) {
    var link = c.querySelector('h3 a') || c.querySelector('a[href]'); if (!link) return;
    var img = c.querySelector('img');
    data.push({ href: link.getAttribute('href'), title: txt(link), img: img && img.getAttribute('src'),
      tag: txt(c.querySelector('.pb-card-meta')).split('·')[0].trim(), bn: !!c.querySelector('.pb-bangla-link') });
  });
  // the helix: article cards mixed with patterned tiles, wound two turns round a vertical axis
  var cn = document.querySelector('.bh-count-n'); if (cn) cn.textContent = data.length;
  var list = data.slice();
  while (list.length < 9) list = list.concat(data);
  var seq = [];
  list.forEach(function (d) { seq.push(d); });   // articles only, with open space between them

  var cards = seq.map(function (d, i) {
    var el;
    if (d) {
      el = document.createElement('a');
      el.className = 'bh-card'; el.href = d.href; el.tabIndex = -1; el.draggable = false; el.setAttribute('aria-label', d.title);
      el.innerHTML = '<span class="bh-face bh-front">' +
        (d.img ? '<img src="' + d.img + '" alt="" width="472" height="266" decoding="async">' : '') +
        '<span class="bh-card-body"><span class="bh-card-tag"></span><span class="bh-card-title"></span>' +
        '<span class="bh-card-foot"><span>Read article ↗</span><span>' + (d.bn ? 'English + বাংলা' : 'English') + '</span></span></span></span>' +
        '';
      el.querySelector('.bh-card-tag').textContent = d.tag;
      el.querySelector('.bh-card-title').textContent = d.title;
    } else {
      el = document.createElement('span');
      var t = 't' + ((i * 5 % 6) + 1);
      el.className = 'bh-card bh-tile'; el.setAttribute('aria-hidden', 'true');
      el.innerHTML = '<span class="bh-face bh-back bh-tf ' + t + '"></span><span class="bh-face bh-back ' + t + '"></span>';
    }
    ring.appendChild(el);
    return el;
  });

  var N = cards.length, TURNS = 2, step = 360 * TURNS / N, R = 430, H = 700, push = 1, rot = 0, vel = 0, auto = 10 /* deg per second */;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hovering = false, dragging = false, visible = true, last = 0;

  function measure() {
    var w = stage.clientWidth;
    /* Keep neighbouring article cards apart as the collection grows. The vertical pitch
       scales with the responsive card size; every new article is included automatically. */
    var pitch = w < 540 ? 94 : w < 900 ? 118 : 154;
    R = stage.dataset.r ? +stage.dataset.r : w < 540 ? Math.min(170, w * 0.455) : w < 900 ? Math.min(270, w * 0.36) : Math.min(520, w * 0.36);
    H = Math.max(stage.clientHeight * 1.35, N * pitch);
    push = w < 540 ? 1.15 : 1.05;
  }
  function angle(i) { return i * step + rot; }
  function facing(i) { return Math.cos(angle(i) * Math.PI / 180); }   // 1 = facing the viewer, -1 = facing away
  function render() {
    var half = H / 2, fadeZone = H * 0.16;
    for (var i = 0; i < N; i++) {
      var a = angle(i), rad = a * Math.PI / 180;
      var y = ((i * H / N + rot * H / (360 * TURNS)) % H + H) % H - half;   // cards travel downward as the helix turns
      var x = Math.sin(rad) * R, z = Math.cos(rad) * R - R * push;
      var c = cards[i];
      c.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,' + z.toFixed(1) + 'px) rotateY(' + (a % 360).toFixed(2) + 'deg)';
      var op = Math.max(0, Math.min(1, (half - Math.abs(y)) / fadeZone)) * Math.min(1, Math.abs(Math.cos(rad)) / 0.22);
      c.style.setProperty('--bh-op', op.toFixed(3));
      c.style.pointerEvents = op < 0.5 ? 'none' : '';
      var f = facing(i), b = f > 0.3 ? 1 : f > -0.2 ? 0.78 : 0.5, rev = f < 0;
      // cards seen from behind show the article itself, mirrored, a little darker
      if (c._b !== b) { c._b = b; c.style.setProperty('--bh-dim', b); }
    }
  }
  function frame(t) {
    if (!last) last = t;
    var dt = Math.min(50, t - last) / 1000; last = t;
    if (visible && !dragging) {
      if (Math.abs(vel) > 0.01) { rot += vel * dt; vel *= Math.pow(0.04, dt); }   // glide after a drag or scroll
      else if (!hovering && !reduce) rot += auto * dt;
      render();
    }
    requestAnimationFrame(frame);
  }

  // page scroll turns the ring
  var ly = window.scrollY || 0;
  window.addEventListener('scroll', function () {
    var y = window.scrollY || 0, d = y - ly; ly = y;
    if (visible) { rot += d * 0.2; vel = d * 2.4; if (reduce) render(); }
  }, { passive: true });

  // sideways drag / swipe turns it; a drag never opens a link
  var pid = null, sx = 0, sy = 0, sr = 0, moved = 0, lx = 0, lt = 0;
  stage.addEventListener('pointerdown', function (e) { if (e.button) return; pid = e.pointerId; sx = lx = e.clientX; sy = e.clientY; sr = rot; moved = 0; lt = e.timeStamp; vel = 0; });
  stage.addEventListener('pointermove', function (e) {
    if (pid !== e.pointerId) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    if (!dragging && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { dragging = true; stage.classList.add('is-drag'); try { stage.setPointerCapture(pid); } catch (err) {} }
    if (dragging) {
      moved = Math.abs(dx); rot = sr + dx * 0.22;
      var dtm = Math.max(1, e.timeStamp - lt); vel = (e.clientX - lx) * 0.22 / dtm * 1000; lx = e.clientX; lt = e.timeStamp;
      render();
    }
  });
  function end() { pid = null; if (dragging) { dragging = false; stage.classList.remove('is-drag'); } }
  stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
  stage.addEventListener('dragstart', function (e) { e.preventDefault(); });
  stage.addEventListener('pointerover', function (e) { if (e.pointerType === 'mouse') hovering = true; });
  stage.addEventListener('pointerout', function (e) { if (e.pointerType === 'mouse' && !stage.contains(e.relatedTarget)) hovering = false; });

  // a card facing away is brought to the front instead of opening
  stage.addEventListener('click', function (e) {
    if (moved > 8) { e.preventDefault(); e.stopPropagation(); moved = 0; return; }
    var a = e.target.closest && e.target.closest('.bh-card'); if (!a) return;
    var i = cards.indexOf(a);
    if (facing(i) < 0.55) {
      e.preventDefault();
      var target = -i * step, diff = ((target - rot) % 360 + 540) % 360 - 180;
      vel = diff * 3.2;                                           // eases round to this card
    }
  }, true);

  // arrows / buttons
  function nudge(dir) { vel = dir * step * 3.2; if (reduce) { rot += dir * step; render(); } }
  stage.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') nudge(1); else if (e.key === 'ArrowRight') nudge(-1); });
  Array.prototype.forEach.call(document.querySelectorAll('[data-bh-turn]'), function (b) {
    b.addEventListener('click', function () { nudge(b.getAttribute('data-bh-turn') === 'prev' ? 1 : -1); });
  });

  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0 }).observe(stage);
  document.addEventListener('visibilitychange', function () { last = 0; });
  window.addEventListener('resize', function () { fit(); measure(); render(); });

  measure(); render();
  requestAnimationFrame(frame);
})();
