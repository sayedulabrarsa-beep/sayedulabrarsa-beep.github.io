/* Pharma Blog hero: a calm 3D ring of article cards.
   One card faces the reader with neighbours either side (at least two articles always readable);
   every few seconds the ring glides softly to the next card. Swipe/drag, arrows or keys move it;
   tap a side card to bring it forward, tap the front card to read. Cards are built from the
   article grid on the page, so every new article joins automatically. */
(function () {
  'use strict';
  function init() {
    var stage = document.getElementById('bh-stage');
    if (!stage || stage.dataset.carouselReady === 'ring') return;
    var ring = stage.querySelector('.bh-field'), grid = document.querySelector('.pb-featured-grid');
    if (!ring || !grid) return;
    var items = Array.prototype.slice.call(grid.querySelectorAll('.pb-feature-card')).map(function (card) {
      var link = card.querySelector('h3 a') || card.querySelector('a[href]');
      if (!link) return null;
      var img = card.querySelector('img'), meta = card.querySelector('.pb-card-meta');
      return { href: link.getAttribute('href'), title: (link.textContent || '').replace(/\s+/g, ' ').trim(),
        img: img ? img.getAttribute('src') : '', tag: meta ? meta.textContent.split('·')[0].trim() : 'PHARMA BLOG',
        read: meta && meta.textContent.split('·')[1] ? meta.textContent.split('·')[1].trim() : '',
        bn: !!card.querySelector('.pb-bangla-link') };
    }).filter(function (x) { return x && x.href && x.title; });
    if (!items.length) return;
    stage.dataset.carouselReady = 'ring'; ring.innerHTML = '';
    var count = document.querySelector('.bh-count-n'); if (count) count.textContent = items.length;

    var cards = items.map(function (it, i) {
      var a = document.createElement('a');
      a.className = 'bh-card'; a.href = it.href; a.draggable = false; a.setAttribute('aria-label', it.title);
      var face = document.createElement('span'); face.className = 'bh-face bh-front';
      if (it.img) { var im = document.createElement('img'); im.src = it.img; im.alt = ''; im.width = 472; im.height = 266; im.decoding = 'async'; im.draggable = false; if (i > 4) im.loading = 'lazy'; face.appendChild(im); }
      var body = document.createElement('span'); body.className = 'bh-card-body';
      var tag = document.createElement('span'); tag.className = 'bh-card-tag'; tag.textContent = it.tag + (it.read ? ' · ' + it.read : '');
      var title = document.createElement('span'); title.className = 'bh-card-title'; title.textContent = it.title;
      var foot = document.createElement('span'); foot.className = 'bh-card-foot';
      var r = document.createElement('span'); r.textContent = 'Read article ↗';
      var l = document.createElement('span'); l.textContent = it.bn ? 'English + বাংলা' : 'English';
      foot.appendChild(r); foot.appendChild(l); body.appendChild(tag); body.appendChild(title); body.appendChild(foot);
      face.appendChild(body); a.appendChild(face); ring.appendChild(a); return a;
    });

    var n = cards.length, pos = 0, target = 0, R = 700, step = 26 * Math.PI / 180, pxPerCard = 300;
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var HOLD = 3600, held = 0, hover = false, visible = true, last = 0;
    var counter = stage.querySelector('.bh-index');

    function wrap(d) { d = ((d % n) + n) % n; return d > n / 2 ? d - n : d; }
    function measure() {
      var w = stage.clientWidth, cw = cards[0].offsetWidth || 300;
      step = (w < 540 ? 34 : w < 900 ? 30 : 25) * Math.PI / 180;
      var gapK = w < 540 ? 1.04 : 1.06;                       // how far the first neighbour sits from the front card
      R = cw * gapK / Math.sin(step);
      pxPerCard = Math.sin(step) * R;
      draw();
    }
    function draw() {
      var front = ((Math.round(pos) % n) + n) % n;
      for (var i = 0; i < n; i++) {
        var d = wrap(i - pos), th = d * step, a = Math.abs(th);
        var c = cards[i];
        if (a > Math.PI * 0.58) { if (c._on !== false) { c._on = false; c.style.visibility = 'hidden'; c.style.pointerEvents = 'none'; } continue; }
        if (c._on !== true) { c._on = true; c.style.visibility = ''; }
        var x = Math.sin(th) * R, z = (Math.cos(th) - 1) * R;
        var k = Math.max(0, 1 - Math.abs(d));                   // 1 at the front, 0 one card away
        var sc = 1 + 0.06 * k;
        c.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,' + z.toFixed(1) + 'px) rotateY(' + (th * 180 / Math.PI).toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
        c.style.opacity = Math.max(0, Math.min(1, (Math.PI * 0.58 - a) / (Math.PI * 0.2))).toFixed(3);
        c.style.setProperty('--bh-dim', (0.62 + 0.38 * Math.max(k, Math.cos(Math.min(a, 1.4)) * 0.75)).toFixed(3));
        c.style.zIndex = String(1000 - Math.round(Math.abs(d) * 10));
        c.style.pointerEvents = a < Math.PI * 0.45 ? 'auto' : 'none';
        c.classList.toggle('is-front', i === front && Math.abs(d) < 0.5);
        c.tabIndex = i === front ? 0 : -1;
      }
      if (counter) counter.textContent = (front + 1) + ' / ' + n;
    }
    function frame(t) {
      if (!last) last = t;
      var dt = Math.min(50, t - last); last = t;
      if (visible && !dragging) {
        if (!reduced && !hover && !document.hidden) { held += dt; if (held >= HOLD && Math.abs(target - pos) < 0.02) { target += 1; held = 0; } }
        var diff = target - pos;
        if (Math.abs(diff) > 0.0005) { pos += diff * (1 - Math.exp(-dt / (reduced ? 60 : 210))); draw(); }
        else if (pos !== target) { pos = target; draw(); }
      }
      requestAnimationFrame(frame);
    }
    function goTo(t) { target = t; held = 0; }

    // swipe / drag: follows the finger, then settles on the nearest card
    var dragging = false, pid = null, sx = 0, sy = 0, spos = 0, moved = 0, lx = 0, lt = 0, vel = 0;
    stage.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      if (e.target.closest && e.target.closest('.bh-nav')) return;
      pid = e.pointerId; sx = lx = e.clientX; sy = e.clientY; spos = pos; moved = 0; vel = 0; lt = e.timeStamp;
    });
    stage.addEventListener('pointermove', function (e) {
      if (pid !== e.pointerId) return;
      var dx = e.clientX - sx, dy = e.clientY - sy;
      if (!dragging) {
        if (Math.abs(dy) > 8 && Math.abs(dy) > Math.abs(dx)) { pid = null; return; }   // vertical = page scroll
        if (Math.abs(dx) < 7) return;
        dragging = true; stage.classList.add('is-drag'); try { stage.setPointerCapture(pid); } catch (err) {}
      }
      moved = Math.abs(dx);
      pos = spos - dx / pxPerCard; target = pos;
      var el = Math.max(1, e.timeStamp - lt); vel = -(e.clientX - lx) / pxPerCard / el * 1000; lx = e.clientX; lt = e.timeStamp;
      draw();
    });
    function end() {
      pid = null;
      if (!dragging) return;
      dragging = false; stage.classList.remove('is-drag');
      goTo(Math.round(pos + Math.max(-2, Math.min(2, vel * 0.18))));
    }
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    stage.addEventListener('dragstart', function (e) { e.preventDefault(); });
    stage.addEventListener('click', function (e) {
      if (moved > 7) { e.preventDefault(); e.stopPropagation(); moved = 0; return; }
      var c = e.target.closest && e.target.closest('.bh-card'); if (!c) return;
      var d = wrap(cards.indexOf(c) - pos);
      if (Math.abs(d) > 0.5) { e.preventDefault(); goTo(Math.round(pos + d)); }   // side card: bring it forward
    }, true);
    stage.addEventListener('mouseenter', function () { hover = true; });
    stage.addEventListener('mouseleave', function () { hover = false; held = 0; });
    stage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(Math.round(target) - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); goTo(Math.round(target) + 1); }
    });
    Array.prototype.forEach.call(stage.querySelectorAll('[data-bh-turn]'), function (b) {
      b.addEventListener('click', function (e) { e.stopPropagation(); goTo(Math.round(target) + (b.dataset.bhTurn === 'prev' ? -1 : 1)); });
    });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: 0 }).observe(stage);
    document.addEventListener('visibilitychange', function () { last = 0; });
    window.addEventListener('resize', measure);

    // headline fills the width once fonts have loaded
    var h1 = document.querySelector('.bh-title'), fit = h1 && h1.querySelector('.bh-fit');
    function fitTitle() {
      if (!h1 || !fit) return;
      var cs = getComputedStyle(h1), room = h1.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 24;
      h1.style.fontSize = '100px'; var fw = fit.getBoundingClientRect().width;
      if (fw > 0 && room > 20) h1.style.fontSize = Math.max(28, Math.min(innerWidth > 900 ? 150 : 120, 100 * room / fw * 0.97)) + 'px';
    }
    fitTitle(); window.addEventListener('resize', fitTitle);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fitTitle(); measure(); });

    measure(); requestAnimationFrame(frame);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
