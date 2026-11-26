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
  // One horizontal circular orbit. Every article occupies a fixed arc-length slot,
  // so adding articles expands the orbit instead of squeezing existing cards together.
  var cn = document.querySelector('.bh-count-n'); if (cn) cn.textContent = data.length;
  var cards = data.map(function (d) {
    var el = document.createElement('a');
    el.className = 'bh-card'; el.href = d.href; el.tabIndex = -1; el.draggable = false; el.setAttribute('aria-label', d.title);
    el.innerHTML = '<span class="bh-face bh-front">' +
      (d.img ? '<img src="' + d.img + '" alt="" width="472" height="266" decoding="async">' : '') +
      '<span class="bh-card-body"><span class="bh-card-tag"></span><span class="bh-card-title"></span>' +
      '<span class="bh-card-foot"><span>Read article ↗</span><span>' + (d.bn ? 'English + বাংলা' : 'English') + '</span></span></span></span>';
    el.querySelector('.bh-card-tag').textContent = d.tag;
    el.querySelector('.bh-card-title').textContent = d.title;
    ring.appendChild(el);
    return el;
  });

  var N = cards.length, step = 360 / N, R = 900, rot = 0, vel = 0, auto = 8;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hovering = false, dragging = false, visible = true, last = 0;

  function measure() {
    var w = stage.clientWidth;
    var cardW = w < 540 ? 136 : w < 900 ? 184 : 236;
    var gap = w < 540 ? 28 : 36;
    // Circumference = article count × (card width + fixed gap).
    R = Math.max(1, N * (cardW + gap) / (2 * Math.PI));
  }
  function angle(i) { return i * step + rot; }
  function facing(i) { return Math.cos(angle(i) * Math.PI / 180); }
  function render() {
    for (var i = 0; i < N; i++) {
      var a = angle(i), rad = a * Math.PI / 180;
      // A true circular orbit around the vertical axis; no vertical helix or stacking.
      var x = Math.sin(rad) * R;
      var z = Math.cos(rad) * R - R;
      var c = cards[i], f = Math.cos(rad);
      c.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,' + z.toFixed(1) + 'px) rotateY(' + a.toFixed(2) + 'deg)';
      var op = Math.max(0, Math.min(1, (f + 0.12) / 0.32));
      c.style.setProperty('--bh-op', op.toFixed(3));
      c.style.pointerEvents = (op < 0.28 || dragging) ? 'none' : '';
      c.setAttribute('aria-hidden', op < 0.28 ? 'true' : 'false');
    }
  }
  function frame(t) {
    if (!last) last = t;
    var dt = Math.min(50, t - last) / 1000; last = t;
    if (visible && !dragging) {
      if (Math.abs(vel) > 0.01) { rot += vel * dt; vel *= Math.pow(0.04, dt); }
      else if (!hovering && !reduce) rot += auto * dt;
      render();
    }
    requestAnimationFrame(frame);
  }

  // Pause while the user explores; resume the gentle circular motion afterwards.
  stage.addEventListener('pointerover', function (e) { if (e.pointerType === 'mouse') hovering = true; });
  stage.addEventListener('pointerout', function (e) { if (e.pointerType === 'mouse' && !stage.contains(e.relatedTarget)) hovering = false; });

  // Horizontal swipe/drag follows the orbit's arc length, keeping the gesture predictable.
  var pid = null, sx = 0, sy = 0, sr = 0, moved = 0, lx = 0, lt = 0;
  stage.addEventListener('pointerdown', function (e) {
    if (e.button !== undefined && e.button !== 0) return;
    pid = e.pointerId; sx = lx = e.clientX; sy = e.clientY; sr = rot; moved = 0; lt = e.timeStamp; vel = 0;
  });
  stage.addEventListener('pointermove', function (e) {
    if (pid !== e.pointerId) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    if (!dragging && Math.abs(dx) > 7 && Math.abs(dx) > Math.abs(dy) * 1.05) {
      dragging = true; stage.classList.add('is-drag');
      try { stage.setPointerCapture(pid); } catch (err) {}
    }
    if (dragging) {
      if (e.cancelable) e.preventDefault();
      moved = Math.abs(dx);
      var degreesPerPixel = 180 / (Math.PI * R);
      rot = sr + dx * degreesPerPixel;
      var dtm = Math.max(1, e.timeStamp - lt);
      vel = (e.clientX - lx) * degreesPerPixel / dtm * 1000;
      lx = e.clientX; lt = e.timeStamp; render();
    }
  });
  function end() {
    pid = null;
    if (dragging) { dragging = false; stage.classList.remove('is-drag'); render(); }
  }
  stage.addEventListener('pointerup', end);
  stage.addEventListener('pointercancel', end);
  stage.addEventListener('lostpointercapture', end);
  stage.addEventListener('dragstart', function (e) { e.preventDefault(); });

  // Tap a visible card to open it; tap a side card to bring it smoothly to the front.
  stage.addEventListener('click', function (e) {
    if (moved > 7) { e.preventDefault(); e.stopPropagation(); moved = 0; return; }
    var a = e.target.closest && e.target.closest('.bh-card'); if (!a) return;
    var i = cards.indexOf(a);
    if (facing(i) < 0.72) {
      e.preventDefault();
      var target = -i * step;
      var diff = ((target - rot) % 360 + 540) % 360 - 180;
      vel = diff * 2.8;
    }
  }, true);

  function nudge(dir) { vel = dir * Math.min(42, step * 2.8); if (reduce) { rot += dir * step; render(); } }
  stage.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') nudge(1);
    else if (e.key === 'ArrowRight') nudge(-1);
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-bh-turn]'), function (b) {
    b.addEventListener('click', function () { nudge(b.getAttribute('data-bh-turn') === 'prev' ? 1 : -1); });
  });

  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0 }).observe(stage);
  document.addEventListener('visibilitychange', function () { last = 0; });
  window.addEventListener('resize', function () { fit(); measure(); render(); });
  measure(); render(); requestAnimationFrame(frame);
})();
