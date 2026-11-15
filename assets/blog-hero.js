/* Pharma Blog hero: builds a drifting 3D field of cards from the article cards already on the page,
   so every new article added to the grid appears here automatically. */
(function () {
  var stage = document.getElementById('bh-stage');
  if (!stage) return;

  // size the headline so it spans the hero width whichever font has loaded
  var h1 = document.querySelector('.bh-title'), fitEl = h1 && h1.querySelector('.bh-fit');
  function fit() {
    if (!fitEl) return;
    h1.style.fontSize = '100px';
    var w = fitEl.getBoundingClientRect().width, room = h1.clientWidth - 28;
    if (w > 0) h1.style.fontSize = Math.min(150, Math.floor(100 * room / w * 0.97)) + 'px';
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', fit);
  var field = stage.querySelector('.bh-field');
  var src = Array.prototype.slice.call(document.querySelectorAll('.pb-featured-grid .pb-feature-card'));
  if (!src.length) { stage.style.display = 'none'; return; }

  function txt(el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; }
  var items = [];
  src.forEach(function (c, i) {
    var link = c.querySelector('h3 a') || c.querySelector('a[href]');
    var img = c.querySelector('img');
    if (!link) return;
    var tag = txt(c.querySelector('.pb-card-meta')).split('·')[0].trim();
    var a = document.createElement('a');
    a.className = 'bh-card'; a.href = link.getAttribute('href'); a.tabIndex = -1; a.draggable = false;
    var html = '';
    if (img) html += '<img src="' + img.getAttribute('src') + '" alt="" width="472" height="266" decoding="async"' + (i > 3 ? ' loading="lazy"' : '') + '>';
    html += '<span class="bh-card-body"><span class="bh-card-tag"></span><span class="bh-card-title"></span>' +
      '<span class="bh-card-foot"><span>Read article ↗</span><span>' + (c.querySelector('.pb-bangla-link') ? 'English + বাংলা' : 'English') + '</span></span></span>';
    a.innerHTML = html;
    a.querySelector('.bh-card-tag').textContent = tag;
    a.querySelector('.bh-card-title').textContent = txt(link);
    a.setAttribute('aria-label', txt(link));
    items.push(a);
    if (i % 2 === 1) { var t = document.createElement('span'); t.className = 'bh-tile t' + ((Math.floor(i / 2) % 6) + 1); t.setAttribute('aria-hidden', 'true'); items.push(t); }
  });

  // deterministic scatter: three depth lanes, staggered heights
  var LANES = [{ z: 90, y: -40, s: 1 }, { z: -260, y: 118, s: 1 }, { z: -150, y: -128, s: 1 }, { z: -420, y: 30, s: 1 }];
  var nodes = items.map(function (el, i) {
    var lane = el.className.indexOf('bh-tile') > -1 ? LANES[1 + (i % 3)] : LANES[i % 2 === 0 ? 0 : 2];
    var jitter = ((i * 37) % 60) - 30;
    field.appendChild(el);
    return { el: el, i: i, z: lane.z - ((i * 53) % 70), y: lane.y + jitter, hover: false };
  });

  var gap, W, offset = 0, speed = 0.022, last = 0, running = true, visible = true;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function measure() {
    var w = stage.clientWidth;
    gap = w < 540 ? 132 : w < 900 ? 168 : 205;
    W = Math.max(nodes.length * gap, w + 500);
    var k = w < 540 ? 0.62 : w < 900 ? 0.8 : 1;
    nodes.forEach(function (n) { n.yy = n.y * k; n.zz = n.z * (w < 540 ? 0.7 : 1); });
  }
  function place() {
    var half = W / 2;
    for (var j = 0; j < nodes.length; j++) {
      var n = nodes[j];
      var x = ((n.i * (W / nodes.length) + offset) % W + W) % W - half;
      var p = x / half;                                  // -1 … 1 across the belt
      var ry = -p * 38;                                  // edges turn inward
      var z = n.zz - Math.abs(p) * 120 + (n.hover ? 70 : 0);
      var edge = Math.min(1, (1 - Math.abs(p)) * 3.2);
      var isTile = n.el.tagName !== 'A';
      var depthFade = isTile ? (n.zz < -200 ? 0.5 : 0.75) : 1;
      var dim = isTile || n.hover ? 1 : n.zz < -100 ? 0.72 : 1;
      n.el.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + n.yy.toFixed(1) + 'px,' + z.toFixed(1) + 'px) rotateY(' + ry.toFixed(2) + 'deg)';
      n.el.style.opacity = (edge * (n.hover ? 1 : depthFade)).toFixed(3);
      n.el.style.zIndex = String(1000 + Math.round(z));
      if (n.dim !== dim) { n.dim = dim; n.el.style.filter = dim < 1 ? 'brightness(' + dim + ')' : ''; }
    }
  }
  function frame(t) {
    if (!last) last = t;
    var dt = Math.min(50, t - last); last = t;
    if (running && visible && !dragging) { offset -= dt * speed; place(); }
    requestAnimationFrame(frame);
  }

  // hover pauses the drift and lifts the card
  nodes.forEach(function (n) {
    if (n.el.tagName !== 'A') return;
    n.el.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { n.hover = true; running = false; place(); } });
    n.el.addEventListener('pointerleave', function () { n.hover = false; running = !reduce; place(); });
  });

  // drag / swipe sideways to browse; a drag never triggers the link
  var dragging = false, sx = 0, sy = 0, so = 0, moved = 0, pid = null;
  stage.addEventListener('pointerdown', function (e) { if (e.button) return; pid = e.pointerId; sx = e.clientX; sy = e.clientY; so = offset; moved = 0; });
  stage.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'mouse' && pid === null) {      // gentle parallax tilt
      var r = stage.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      field.style.transform = 'rotateY(' + (px * 5).toFixed(2) + 'deg) rotateX(' + (-py * 4).toFixed(2) + 'deg)';
    }
    if (pid !== e.pointerId) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    if (!dragging && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { dragging = true; stage.classList.add('is-drag'); try { stage.setPointerCapture(pid); } catch (err) {} }
    if (dragging) { moved = Math.abs(dx); offset = so + dx * 1.25; place(); }
  });
  function end() { pid = null; if (dragging) { dragging = false; stage.classList.remove('is-drag'); } }
  stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
  stage.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') field.style.transform = ''; });
  stage.addEventListener('click', function (e) { if (moved > 8) { e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
  stage.addEventListener('dragstart', function (e) { e.preventDefault(); });

  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0 }).observe(stage);
  document.addEventListener('visibilitychange', function () { last = 0; });
  window.addEventListener('resize', function () { fit(); measure(); place(); });

  measure(); place();
  if (reduce) { running = false; } else requestAnimationFrame(frame);
})();
