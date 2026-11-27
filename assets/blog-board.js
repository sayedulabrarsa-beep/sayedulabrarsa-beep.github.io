/* Pharma Blog article board. Reads the article grid on the page, so new articles appear automatically.
   - cards are grouped topic by topic; when there are more than fit, the board changes set every 20 s
   - drag a card into the tray (or press Enter on it) to see what the article covers
   - double-click / double-tap a card for the full article in a reader overlay */
(function () {
  var tray = document.getElementById('ab-tray');
  if (!tray) return;
  var pinsEl = tray.querySelector('.ab-pins'), slot = tray.querySelector('.ab-slot'), topicsEl = tray.querySelector('.ab-topics'),
      pageEl = tray.querySelector('.ab-page'), bar = tray.querySelector('.ab-bar i'), detail = tray.querySelector('.ab-detail');
  function txt(el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; }

  var COLORS = ['#116b57', '#c9483b', '#b8862b', '#7a5aa6', '#2f7f9c', '#a35a2a', '#4f7a3a', '#9c3f6b'];
  var topicColor = {}, data = [];
  Array.prototype.forEach.call(document.querySelectorAll('.pb-featured-grid .pb-feature-card'), function (c) {
    var link = c.querySelector('h3 a') || c.querySelector('a[href]'); if (!link) return;
    var img = c.querySelector('img'), bn = c.querySelector('.pb-bangla-link'), ps = c.querySelectorAll('.pb-card-copy > p');
    var desc = '', bnDesc = '';
    Array.prototype.forEach.call(ps, function (p) {
      if (p.classList.contains('pb-card-meta')) return;
      if (p.classList.contains('pb-bangla')) bnDesc = txt(p); else if (!desc) desc = txt(p);
    });
    var meta = txt(c.querySelector('.pb-card-meta')).split('·');
    var title = txt(link), short = title.split(/[:?]/)[0].trim();
    if (short.length > 30) short = short.split(' ').slice(0, 4).join(' ');
    var tag = (meta[0] || 'Article').trim();
    if (window.PBX) { var cc = window.PBX.CATS.filter(function (x) { return x[0] === window.PBX.catOf(c); })[0]; if (cc) tag = cc[1].toUpperCase(); }   // merge look-alike labels into the six topics
    if (!(tag in topicColor)) topicColor[tag] = COLORS[Object.keys(topicColor).length % COLORS.length];
    data.push({ href: link.getAttribute('href'), bn: bn && bn.getAttribute('href'), title: title, short: short, img: img && img.getAttribute('src'),
      tag: tag, read: (meta[1] || '').trim(), desc: desc, bnDesc: bnDesc });
  });
  if (!data.length) { tray.parentNode.style.display = 'none'; return; }
  // topic by topic: keep each topic's articles together, topics in order of first appearance
  var all = data.slice();
  var order = Object.keys(topicColor);
  data.sort(function (a, b) { return order.indexOf(a.tag) - order.indexOf(b.tag); });

  // one board per topic; each topic has its own colours. A topic with many articles spans several boards.
  var THEMES = [
    ['#e3d0b6', '#d9c2a3', '#b99f7d'], ['#cfdcc9', '#bccfb4', '#7f9c78'], ['#efd3c8', '#e4bfb1', '#b98676'],
    ['#cfe0e6', '#b9d0d9', '#6f98a8'], ['#ddd3e8', '#cbbfdc', '#8f7fae'], ['#f0e2b4', '#e5d197', '#b49a4c'], ['#e2c4b0', '#d4ae96', '#a07658']];
  var LAY = {
    d: { 1: [[36, 44, -4]], 2: [[25, 42, -6], [49, 47, 5]], 3: [[19, 38, -6], [40, 49, 4], [61, 37, -3]],
         n: [[15, 28, -7], [35, 40, 5], [56, 27, -4], [17, 56, 4], [39, 62, -3], [60, 55, 5]] },
    t: { 1: [[40, 36, -4]], 2: [[27, 33, -6], [66, 37, 5]], 3: [[20, 29, -6], [52, 34, 5], [82, 29, -3]],
         n: [[18, 23, -6], [48, 27, 5], [78, 22, -4], [22, 45, 4], [52, 48, -5], [80, 44, 3]] },
    m: { 1: [[50, 37, -4]], 2: [[29, 33, -6], [71, 39, 5]], 3: [[25, 28, -6], [73, 31, 5], [47, 48, -3]],
         n: [[22, 25, -6], [72, 28, 5], [46, 42, -3], [22, 57, 4], [74, 58, -5]] } };
  function lay() { var w = tray.clientWidth; return LAY[w < 540 ? 'm' : w < 900 ? 't' : 'd']; }

  var groups = {}; order.forEach(function (t) { groups[t] = []; });
  data.forEach(function (d) { groups[d.tag].push(d); });
  var boards = [];
  function makeBoards() {
    var per = lay().n.length; boards = [];
    var allParts = Math.ceil(all.length / per);                       // first: every article, a few at a time
    for (var a = 0; a < allParts; a++) boards.push({ tag: 'ALL ARTICLES', ti: -1, items: all.slice(a * per, a * per + per), part: a + 1, parts: allParts });
    order.forEach(function (t, ti) {                                  // then: topic by topic
      var g = groups[t], parts = Math.ceil(g.length / per);
      for (var k = 0; k < parts; k++) boards.push({ tag: t, ti: ti, items: g.slice(k * per, k * per + per), part: k + 1, parts: parts });
    });
  }

  var page = 0, pages = 1, pins = [], picked = null, busy = false, elapsed = 0, PERIOD = 20000, z = 10;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var titleEl = tray.querySelector('.ab-title');
  function nice(t) { return t.charAt(0) + t.slice(1).toLowerCase(); }

  // topic tabs
  topicsEl.innerHTML = '';
  topicColor['ALL ARTICLES'] = '#2b2219';
  var tabs = ['ALL ARTICLES'].concat(order).map(function (t, ti) {
    var li = document.createElement('li'), b = document.createElement('button');
    b.type = 'button'; b.textContent = nice(t) + ' (' + (t === 'ALL ARTICLES' ? all.length : groups[t].length) + ')'; li.style.setProperty('--tc', topicColor[t]);
    b.addEventListener('click', function () { if (picked) close(); for (var i = 0; i < boards.length; i++) if (boards[i].tag === t) { page = i; build(true); return; } });
    li.appendChild(b); topicsEl.appendChild(li); return li;
  });

  function build(animate) {
    makeBoards(); pages = boards.length; if (page >= pages) page = 0;
    var bd = boards[page], L = lay(), sp = bd.items.length <= 3 ? L[bd.items.length] : L.n, set = bd.items, old = pins;
    var th = bd.ti < 0 ? ['#ead9c0', '#dcc6a6', '#b99f7d'] : THEMES[(bd.ti + 1) % THEMES.length];
    tray.style.setProperty('--ab-bg', th[0]); tray.style.setProperty('--ab-bg2', th[1]); tray.style.setProperty('--ab-edge', th[2]);
    tray.style.setProperty('--ab-tc', topicColor[bd.tag]);
    titleEl.innerHTML = ''; nice(bd.tag).split(' ').forEach(function (w, i, arr) { titleEl.appendChild(document.createTextNode(w)); if (i < arr.length - 1) titleEl.appendChild(document.createElement('br')); });
    tabs.forEach(function (li, i) { li.classList.toggle('is-on', (['ALL ARTICLES'].concat(order))[i] === bd.tag); });
    old.forEach(function (p) { p.el.classList.add('is-out'); setTimeout(function () { p.el.remove(); }, 450); });
    pins = set.map(function (d, i) {
      var el = document.createElement('div');
      el.className = 'ab-pin' + (animate ? ' is-in' : ''); el.tabIndex = 0; el.setAttribute('role', 'button');
      el.setAttribute('aria-label', d.title + '. Press Enter for a summary, or double-click for the full article.');
      el.style.left = sp[i][0] + '%'; el.style.top = sp[i][1] + '%'; el.style.setProperty('--r', sp[i][2] + 'deg'); el.style.zIndex = String(++z);
      el.innerHTML = '<span class="ab-tape"></span><span class="ab-photo">' + (d.img ? '<img src="' + d.img + '" alt="" loading="lazy" decoding="async" width="300" height="300">' : '') + '</span><span class="ab-cap"></span>';
      el.querySelector('.ab-tape').textContent = d.tag; el.querySelector('.ab-tape').style.setProperty('--tc', topicColor[d.tag]);
      el.querySelector('.ab-cap').textContent = d.short;
      pinsEl.appendChild(el);
      var pin = { el: el, d: d, x: 0, y: 0, r: sp[i][2] };
      wire(pin);
      if (animate) setTimeout(function () { el.classList.remove('is-in'); }, 80 + i * 70);
      return pin;
    });
    pageEl.textContent = (bd.ti < 0 ? 'All articles' : 'Topic ' + (bd.ti + 1) + ' of ' + order.length) + (bd.parts > 1 ? ' · ' + bd.part + '/' + bd.parts : '');
    Array.prototype.forEach.call(tray.querySelectorAll('.ab-status button, .ab-bar'), function (b) { b.style.display = pages > 1 ? '' : 'none'; });
    elapsed = 0;
  }
  function go(dir) { if (picked || pages < 2) return; page = (page + dir + pages) % pages; build(true); }

  function setPos(pin) { pin.el.style.setProperty('--x', pin.x + 'px'); pin.el.style.setProperty('--y', pin.y + 'px'); pin.el.style.setProperty('--r', pin.r + 'deg'); }
  function overSlot(pin) {
    var a = pin.el.getBoundingClientRect(), b = slot.getBoundingClientRect(), cx = a.left + a.width / 2, cy = a.top + a.height / 2;
    return cx > b.left - 20 && cx < b.right + 20 && cy > b.top - 20 && cy < b.bottom + 20;
  }
  function wire(pin) {
    var el = pin.el, pid = null, sx, sy, ox, oy, drag = false, lastTap = 0;
    var pickTap = 0;
    el.addEventListener('pointerdown', function (e) {
      if (picked === pin) { if (e.timeStamp - pickTap < 400) { pickTap = 0; close(); } else pickTap = e.timeStamp; return; }
      if (e.button || picked) return;
      pid = e.pointerId; sx = e.clientX; sy = e.clientY; ox = pin.x; oy = pin.y; drag = false; el.style.zIndex = String(++z);
      try { el.setPointerCapture(pid); } catch (err) {}
    });
    el.addEventListener('pointermove', function (e) {
      if (pid !== e.pointerId) return;
      var dx = e.clientX - sx, dy = e.clientY - sy;
      if (!drag && Math.abs(dx) + Math.abs(dy) > 7) { drag = true; busy = true; el.classList.add('is-drag'); }
      if (drag) { pin.x = ox + dx; pin.y = oy + dy; setPos(pin); slot.classList.toggle('is-hot', overSlot(pin)); }
    });
    function up(e) {
      if (pid !== e.pointerId) return; pid = null;
      if (drag) {
        drag = false; busy = false; el.classList.remove('is-drag'); slot.classList.remove('is-hot');
        if (overSlot(pin)) open(pin);
        else {                                                     // stay where dropped, but inside the tray
          var t = tray.getBoundingClientRect(), a = el.getBoundingClientRect();
          if (a.left < t.left + 8) pin.x += t.left + 8 - a.left; if (a.right > t.right - 8) pin.x -= a.right - t.right + 8;
          if (a.top < t.top + 8) pin.y += t.top + 8 - a.top; if (a.bottom > t.bottom - 8) pin.y -= a.bottom - t.bottom + 8;
          setPos(pin);
        }
        return;
      }
      var now = e.timeStamp;                                       // double-tap / double-click → full article
      if (now - lastTap < 380) { lastTap = 0; reader(pin.d, false); } else lastTap = now;
    }
    el.addEventListener('pointerup', up);
    el.addEventListener('pointercancel', function (e) { if (pid === e.pointerId) { pid = null; drag = false; busy = false; el.classList.remove('is-drag'); slot.classList.remove('is-hot'); } });
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (e.shiftKey) reader(pin.d, false); else open(pin); } });
    el.addEventListener('dragstart', function (e) { e.preventDefault(); });
  }

  // summary view: the card sits in the tray slot and the board shows what the article covers
  function open(pin) {
    if (picked) return; picked = pin; pin.home = { x: pin.x, y: pin.y, r: pin.r };
    var a = pin.el.getBoundingClientRect(), b = slot.getBoundingClientRect();
    var k = Math.min(1, (b.width - 22) / pin.el.offsetWidth, (b.height - 22) / pin.el.offsetHeight);
    pin.x += b.left + b.width / 2 - (a.left + a.width / 2); pin.y += b.top + b.height / 2 - (a.top + a.height / 2); pin.r = -2;
    pin.el.style.setProperty('--s', k); setPos(pin); pin.el.classList.add('is-picked');
    var d = pin.d;
    detail.querySelector('.ab-d-img').innerHTML = d.img ? '<img src="' + d.img + '" alt="">' : '';
    detail.querySelector('.ab-d-tag').textContent = 'Topic: ' + nice(d.tag) + (d.read ? ' · ' + d.read.toLowerCase() : '');
    detail.querySelector('.ab-d-h').textContent = d.title;
    detail.querySelector('.ab-d-en').textContent = d.desc;
    var bnp = detail.querySelector('.ab-d-bn'); bnp.textContent = d.bnDesc; bnp.style.display = d.bnDesc ? '' : 'none';
    detail.querySelector('.ab-d-big').textContent = d.short;
    var en = detail.querySelector('[data-ab="en"]'), bn = detail.querySelector('[data-ab="bn"]');
    en.href = d.href; if (d.bn) { bn.href = d.bn; bn.style.display = ''; } else bn.style.display = 'none';
    glimpse(d);
    tray.classList.add('is-open'); slot.firstElementChild.style.visibility = 'hidden';
    setTimeout(function () { detail.querySelector('.ab-close').focus({ preventScroll: true }); }, 60);
  }

  // a short glimpse of the article: its opening answer and the sections inside it
  var gCache = {};
  function glimpse(d) {
    var box = detail.querySelector('.ab-d-glimpse'), want = d.href;
    box.hidden = true; box.querySelector('.ab-g-lead').textContent = ''; box.querySelector('.ab-g-list').innerHTML = '';
    function show(g) {
      if (!picked || picked.d.href !== want || !g) return;
      box.querySelector('.ab-g-lead').textContent = g.lead;
      box.querySelector('.ab-g-lead-wrap').hidden = !g.lead;
      var ol = box.querySelector('.ab-g-list');
      g.secs.forEach(function (sx) { var li = document.createElement('li'), a = document.createElement('a'); a.href = want + (sx.id ? '#' + sx.id : ''); a.textContent = sx.t; li.appendChild(a); ol.appendChild(li); });
      box.querySelector('.ab-g-secs').hidden = !g.secs.length;
      box.hidden = !(g.lead || g.secs.length);
    }
    if (gCache[want]) return show(gCache[want]);
    if (!window.fetch || !window.DOMParser) return;
    fetch(want).then(function (r) { return r.ok ? r.text() : ''; }).then(function (html) {
      if (!html) return;
      var doc = new DOMParser().parseFromString(html, 'text/html'), art = doc.querySelector('article.article-content') || doc.querySelector('article') || doc.body;
      function t(el) { var en = el.querySelector('.lang-en'); return txt(en || el); }
      var secs = [];
      Array.prototype.forEach.call(art.querySelectorAll('h2'), function (h) { if (secs.length < 6 && !h.closest('nav, aside, .ae-band')) secs.push({ t: t(h), id: h.id || (h.closest('[id]') && h.closest('[id]') !== art ? h.closest('[id]').id : '') }); });
      var lead = '';
      Array.prototype.some.call(art.querySelectorAll('p'), function (p) {
        if (p.classList.contains('lang-bn') || p.hidden || p.closest('nav, header, figure, aside, .article-meta')) return false;
        var x = t(p); if (x.length < 70 || /^category:/i.test(x)) return false;
        lead = x.length > 260 ? x.slice(0, 257).replace(/\s+\S*$/, '') + '…' : x; return true;
      });
      gCache[want] = { lead: lead, secs: secs }; show(gCache[want]);
    }).catch(function () {});
  }

  function close() {
    if (!picked) return; var pin = picked; picked = null;
    pin.x = pin.home.x; pin.y = pin.home.y; pin.r = pin.home.r; pin.el.style.removeProperty('--s'); setPos(pin);
    pin.el.classList.remove('is-picked'); tray.classList.remove('is-open'); slot.firstElementChild.style.visibility = '';
    if (overSlot(pin)) { pin.x = 0; pin.y = 0; setPos(pin); }
    elapsed = 0;
  }
  detail.querySelector('.ab-close').addEventListener('click', close);
  detail.querySelector('[data-ab="back"]').addEventListener('click', close);
  detail.addEventListener('dblclick', function (e) { if (!e.target.closest('a,button')) close(); });
  detail.querySelector('[data-ab="full"]').addEventListener('click', function () { if (picked) reader(picked.d, false); });

  // full-view reader
  var rd = document.createElement('div'); rd.className = 'ab-reader'; rd.setAttribute('role', 'dialog'); rd.setAttribute('aria-modal', 'true'); rd.setAttribute('aria-label', 'Article reader');
  rd.innerHTML = '<div class="ab-r-bar"><b></b><button type="button" data-l="en">English</button><button type="button" data-l="bn">বাংলা</button><a class="ab-r-new" target="_blank" rel="noopener">Open page ↗</a><button type="button" class="ab-r-x" aria-label="Close reader">Close ✕</button></div><iframe title="Article" loading="lazy"></iframe>';
  document.body.appendChild(rd);
  var rFrame = rd.querySelector('iframe'), rCur = null;
  function reader(d, bn) {
    rCur = d; var url = bn && d.bn ? d.bn : d.href;
    rd.querySelector('b').textContent = d.title; rd.querySelector('.ab-r-new').href = url; rFrame.src = url;
    rd.querySelector('[data-l="bn"]').style.display = d.bn ? '' : 'none';
    rd.querySelector('[data-l="en"]').classList.toggle('is-on', !bn); rd.querySelector('[data-l="bn"]').classList.toggle('is-on', !!bn);
    rd.classList.add('is-on'); document.documentElement.classList.add('ab-lock');
    rd.querySelector('.ab-r-x').focus({ preventScroll: true });
  }
  function readerOff() { rd.classList.remove('is-on'); document.documentElement.classList.remove('ab-lock'); rFrame.src = 'about:blank'; rCur = null; elapsed = 0; }
  rd.querySelector('.ab-r-x').addEventListener('click', readerOff);
  rd.querySelector('[data-l="en"]').addEventListener('click', function () { if (rCur) reader(rCur, false); });
  rd.querySelector('[data-l="bn"]').addEventListener('click', function () { if (rCur) reader(rCur, true); });
  rd.addEventListener('click', function (e) { if (e.target === rd) readerOff(); });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (rCur) readerOff(); else if (picked) close(); });

  // every 20 s the board shows the next set (paused while someone is using it)
  var visible = false, hover = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0.25 }).observe(tray); else visible = true;
  tray.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') hover = true; });
  tray.addEventListener('pointerleave', function () { hover = false; });
  setInterval(function () {
    if (pages < 2 || !visible || busy || picked || rCur || hover || document.hidden) { if (bar) bar.style.width = (elapsed / PERIOD * 100) + '%'; return; }
    elapsed += 250; if (bar) bar.style.width = Math.min(100, elapsed / PERIOD * 100) + '%';
    if (elapsed >= PERIOD) go(1);
  }, 250);
  Array.prototype.forEach.call(tray.querySelectorAll('[data-ab-go]'), function (b) { b.addEventListener('click', function () { go(b.getAttribute('data-ab-go') === 'prev' ? -1 : 1); }); });

  var lastW = tray.clientWidth, rt;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { var nw = tray.clientWidth; if ((nw < 540) !== (lastW < 540) || (nw < 900) !== (lastW < 900)) { close(); build(false); } lastW = tray.clientWidth; }, 200); });

  build(false);
})();
