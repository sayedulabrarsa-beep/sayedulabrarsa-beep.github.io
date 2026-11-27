/* Pharma Blog library: a bookshelf built from the article list on the page.
   Every article is a book; English / বাংলা switches titles, covers and links.
   Shares the language with the Featured list (window.PBX, set up by the page script). */
(function () {
  'use strict';
  function init() {
    var X = window.PBX, root = document.getElementById('pb-library');
    if (!X || !root) return;
    var shelves = document.getElementById('pbl-shelves'), catsEl = document.getElementById('pbl-cats'),
        dots = document.getElementById('pbl-dots'), count = document.getElementById('pbl-count'),
        prev = root.querySelector('.pbl-prev'), next = root.querySelector('.pbl-next'),
        q = document.getElementById('pbl-q'), form = document.getElementById('pbl-search');

    var items = X.cards.map(function (c) {
      var o = c._o || {}, h = c.querySelector('h3 a'), img = c.querySelector('.pb-card-image img'),
          bl = c.querySelector('.pb-bangla-link'), meta = c.querySelector('.pb-card-meta'),
          m = meta && meta.textContent.match(/(\d+(?:\s*[–-]\s*\d+)?)\s*MIN/i);
      var enHref = o.hh || (h && h.getAttribute('href')), enTitle = o.ht || (h ? h.textContent : ''),
          enImg = o.src || (img && img.getAttribute('src')) || '', bnHref = o.bh || (bl && bl.getAttribute('href')) || enHref;
      return {
        cat: X.catOf(c), mins: m ? m[1].replace(/\s+/g, '') + ' min' : '',
        search: ((c.dataset.search || '') + ' ' + enTitle + ' ' + (c.dataset.bnTitle || '')).toLowerCase(),
        en: { href: enHref, title: enTitle.trim(), img: enImg },
        bn: { href: bnHref, title: (c.dataset.bnTitle || enTitle).trim(), img: c.dataset.bnImg || enImg }
      };
    }).filter(function (it) { return it.en.href; });
    if (!items.length) return;

    var L = X.lang || 'en', cat = 'all', query = '', page = 1, cols = 6, per = 12;

    function short(t) { var i = t.search(/[:：]/); return i >= 10 ? t.slice(0, i) : t; }
    function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
    function filtered() {
      var s = query.trim().toLowerCase();
      return items.filter(function (it) { return (cat === 'all' || it.cat === cat) && (!s || it.search.indexOf(s) > -1); });
    }
    function setCols() {
      var w = root.clientWidth || window.innerWidth; var c = w >= 980 ? 6 : w >= 640 ? 4 : 3;
      if (c !== cols || !shelves._set) { var first = (page - 1) * per; cols = c; per = c * 2; page = Math.floor(first / per) + 1; shelves._set = true; return true; }
      return false;
    }
    function book(it, i) {
      var d = it[L], a = el('a', 'pbl-book c-' + it.cat); a.href = d.href; a.style.setProperty('--i', i);
      a.title = d.title; a.setAttribute('aria-label', d.title + (it.mins ? ' (' + it.mins + ')' : ''));
      var cv = el('span', 'pbl-cover'), t = el('span', 'pbl-title', short(d.title)); if (L === 'bn') t.lang = 'bn';
      var art = el('span', 'pbl-art'), im = document.createElement('img'); im.src = d.img; im.alt = ''; im.width = 400; im.height = 250; im.loading = 'lazy'; im.decoding = 'async'; art.appendChild(im);
      cv.appendChild(t); cv.appendChild(art); if (it.mins) cv.appendChild(el('span', 'pbl-mins', it.mins)); a.appendChild(cv); return a;
    }
    function render(animate) {
      var list = filtered(), pages = Math.max(1, Math.ceil(list.length / per));
      if (page > pages) page = pages; if (page < 1) page = 1;
      var from = (page - 1) * per, slice = list.slice(from, from + per);
      shelves.style.setProperty('--cols', cols); shelves.innerHTML = '';
      if (!slice.length) { shelves.appendChild(el('p', 'pbl-empty', 'No articles match your search. Try another word or choose All Articles.')); }
      else for (var r = 0; r < 2; r++) {
        var row = el('div', 'pbl-row'), part = slice.slice(r * cols, (r + 1) * cols);
        if (!part.length) break;
        part.forEach(function (it, k) { row.appendChild(book(it, r * cols + k)); }); shelves.appendChild(row);
      }
      if (animate) { shelves.classList.remove('is-in'); void shelves.offsetWidth; shelves.classList.add('is-in'); }
      dots.innerHTML = '';
      if (pages <= 8) for (var p = 1; p <= pages; p++) {
        var b = document.createElement('button'); b.type = 'button'; b.dataset.p = p; b.setAttribute('aria-label', 'Shelf ' + p + ' of ' + pages);
        if (p === page) b.setAttribute('aria-current', 'true'); dots.appendChild(b);
      } else dots.appendChild(el('span', 'pbl-dots-text', page + ' / ' + pages));
      prev.disabled = page <= 1; next.disabled = page >= pages;
      document.getElementById('pbl-pager').style.visibility = pages < 2 ? 'hidden' : '';
      count.textContent = list.length ? 'Showing ' + (from + 1) + '–' + (from + slice.length) + ' of ' + list.length + ' articles · ' + (L === 'bn' ? 'বাংলা' : 'English') : '0 articles';
    }
    function cats() {
      catsEl.innerHTML = '';
      var rows = [['all', 'All Articles', items.length]].concat(X.CATS.map(function (c) {
        return [c[0], c[1], items.filter(function (it) { return it.cat === c[0]; }).length];
      })).filter(function (r) { return r[2] > 0; });
      rows.forEach(function (r) {
        var li = document.createElement('li'), b = document.createElement('button'); b.type = 'button'; b.dataset.c = r[0];
        b.setAttribute('aria-pressed', r[0] === cat ? 'true' : 'false');
        b.innerHTML = '<i class="dot"></i><span></span><b></b>'; b.children[1].textContent = r[1]; b.children[2].textContent = r[2];
        li.appendChild(b); catsEl.appendChild(li);
      });
    }
    function langButtons() {
      Array.prototype.forEach.call(root.querySelectorAll('.pbl-lang button'), function (b) { b.setAttribute('aria-pressed', b.dataset.l === L ? 'true' : 'false'); });
    }

    catsEl.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return; cat = b.dataset.c; page = 1;
      Array.prototype.forEach.call(catsEl.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      render(true);
    });
    dots.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { page = +b.dataset.p; render(true); } });
    prev.addEventListener('click', function () { page--; render(true); });
    next.addEventListener('click', function () { page++; render(true); });
    form.addEventListener('submit', function (e) { e.preventDefault(); page = 1; render(true); });
    q.addEventListener('input', function () { query = q.value; page = 1; render(true); });
    root.querySelector('.pbl-lang').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (b && b.dataset.l !== L) X.setLang(b.dataset.l);
    });
    document.addEventListener('pb-lang', function (e) { L = e.detail; langButtons(); render(true); });

    var sx = 0, sy = 0;
    shelves.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    shelves.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > 60 && Math.abs(dy) < 40) { page += dx < 0 ? 1 : -1; render(true); }
    }, { passive: true });
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { if (setCols()) render(false); }, 120); });

    setCols(); cats(); langButtons(); render(false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
