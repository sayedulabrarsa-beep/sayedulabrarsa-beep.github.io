/* Heartburn / Acid reflux / GERD article: small interactions. Plain text stays in the page if this file fails. */
(function () {
  'use strict';
  var root = document.querySelector('.article-content');
  if (!root) return;
  document.documentElement.classList.add('rx-js');
  var BN = (document.documentElement.lang || '').indexOf('bn') === 0;
  function N(n) { n = String(n); return BN ? n.replace(/\d/g, function (d) { return '০১২৩৪৫৬৭৮৯'.charAt(d); }) : n; }
  function $(s, c) { return (c || root).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); }

  /* generic "one panel at a time" for chips + panels (trio, valve, warning tabs) */
  $$('[data-rx-switch]').forEach(function (wrap) {
    var chips = $$('[data-rx-chip]', wrap), panels = $$('[data-rx-panel]', wrap);
    function show(id) {
      chips.forEach(function (c) { c.setAttribute('aria-selected', c.dataset.rxChip === id ? 'true' : 'false'); c.tabIndex = c.dataset.rxChip === id ? 0 : -1; });
      panels.forEach(function (p) { p.hidden = p.dataset.rxPanel !== id; });
      wrap.setAttribute('data-state', id);
      var fig = $('.rx-valve-fig', wrap); if (fig) fig.setAttribute('data-state', id);
    }
    chips.forEach(function (c, i) {
      c.addEventListener('click', function () { show(c.dataset.rxChip); });
      c.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = (i + 1) % chips.length;
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = (i - 1 + chips.length) % chips.length;
        if (n !== null) { e.preventDefault(); chips[n].focus(); show(chips[n].dataset.rxChip); }
      });
    });
    show(chips[0].dataset.rxChip);
  });

  /* step viewer (story, habit slider) */
  $$('[data-rx-steps]').forEach(function (wrap) {
    var items = $$('[data-rx-step]', wrap), i = 0;
    var prev = $('[data-rx-prev]', wrap), next = $('[data-rx-next]', wrap), dots = $$('.rx-dot', wrap);
    var live = $('[data-rx-live]', wrap);
    function go(n, announce) {
      i = Math.max(0, Math.min(items.length - 1, n));
      items.forEach(function (el, k) { el.hidden = k !== i; });
      dots.forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === items.length - 1;
      if (live && announce) live.textContent = N(i + 1) + ' / ' + N(items.length);
    }
    if (prev) prev.addEventListener('click', function () { go(i - 1, true); });
    if (next) next.addEventListener('click', function () { go(i + 1, true); });
    dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k, true); }); });
    wrap.addEventListener('keydown', function (e) {
      if (e.target.closest && e.target.closest('input,textarea')) return;
      if (e.key === 'ArrowRight') { go(i + 1, true); } else if (e.key === 'ArrowLeft') { go(i - 1, true); }
    });
    var sx = null;
    wrap.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    wrap.addEventListener('touchend', function (e) {
      if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1), true);
    }, { passive: true });
    go(0, false);
  });

  /* trigger cards: mark the ones you notice */
  var tg = $('[data-rx-triggers]');
  if (tg) {
    var tally = $('[data-rx-tally]', tg);
    var cards = $$('.rx-trig', tg);
    var tpl0 = tg.dataset.none, tpl1 = tg.dataset.some;
    function upd() {
      var n = cards.filter(function (c) { return c.getAttribute('aria-pressed') === 'true'; }).length;
      tally.textContent = n === 0 ? tpl0 : tpl1.replace('{n}', N(n));
    }
    cards.forEach(function (c) {
      c.addEventListener('click', function () { c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); upd(); });
    });
    upd();
  }

  /* habit checklist */
  var cl = $('[data-rx-checklist]');
  if (cl) {
    var boxes = $$('input[type=checkbox]', cl), bar = $('.rx-bar i', cl.parentNode), txt = $('[data-rx-progress]', cl.parentNode);
    var t = cl.dataset.tpl;
    function pg() {
      var n = boxes.filter(function (b) { return b.checked; }).length;
      bar.style.width = (n / boxes.length * 100) + '%';
      txt.textContent = t.replace('{n}', N(n)).replace('{t}', N(boxes.length));
    }
    boxes.forEach(function (b) { b.addEventListener('change', pg); });
    pg();
  }

  /* quiz */
  var qz = $('#quiz');
  if (qz) {
    var D = qz.dataset, boxesQ = $$('.quiz', qz), score = 0, done = 0;
    var res = $('.rx-result', qz);
    boxesQ.forEach(function (box) {
      $$('button', box).forEach(function (b) {
        b.addEventListener('click', function () {
          if (box.getAttribute('data-done')) return;
          box.setAttribute('data-done', '1');
          var ok = b.dataset.correct === 'yes';
          $$('button', box).forEach(function (x) {
            x.disabled = true;
            if (x.dataset.correct === 'yes') x.classList.add('rx-right');
            else if (x === b) x.classList.add('rx-wrong');
          });
          $('.quiz-feedback', box).textContent = ok ? D.ok : D.no;
          if (ok) score++;
          done++;
          if (done === boxesQ.length && res) {
            $('[data-rx-score]', res).textContent = D.score.replace('{n}', N(score)).replace('{t}', N(boxesQ.length));
            $('[data-rx-msg]', res).textContent = score === boxesQ.length ? D.all : D.some;
            res.hidden = false;
            res.scrollIntoView({ block: 'nearest', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
          }
        });
      });
    });
    var again = $('[data-rx-again]', qz);
    if (again) again.addEventListener('click', function () {
      score = 0; done = 0; res.hidden = true;
      boxesQ.forEach(function (box) {
        box.removeAttribute('data-done');
        $$('button', box).forEach(function (x) { x.disabled = false; x.classList.remove('rx-right', 'rx-wrong'); });
        $('.quiz-feedback', box).textContent = '';
      });
      qz.scrollIntoView({ block: 'start' });
    });
  }

  /* gentle reveal on scroll */
  var rv = $$('.rx-reveal');
  if ('IntersectionObserver' in window && rv.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('rx-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
    setTimeout(function () { rv.forEach(function (el) { el.classList.add('rx-in'); }); }, 4000);
  } else { rv.forEach(function (el) { el.classList.add('rx-in'); }); }
})();
