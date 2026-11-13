#!/usr/bin/env python3
"""Rebuilds the home-page "Featured from the Pharma Blog" clothesline section.
Articles listed in _src/data/blog_stacks.json are curated; every other article under /blog is discovered and added automatically from its own HTML.
A GitHub Action (.github/workflows/featured-stacks.yml) runs this on every push that touches /blog.
"""
import json, html, pathlib, re
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
e = html.escape

# ---- automatic discovery: any article in /blog that is not curated in the JSON is added from its own HTML ----
ACCENTS = ["#2f8f83", "#c4573a", "#8a5a9c", "#b8433f", "#d08a1f", "#3b7ea1", "#6f6bb0", "#a24a6b"]
def _txt(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
def _short(t, n=190):
    t = t.strip()
    if t.endswith(":"):
        k = max(t[:-1].rfind(". "), t[:-1].rfind("। "))
        t = t[:k+1] if k > 20 else t[:-1] + "."
    if len(t) <= n: return t
    cut = t[:n]; k = max(cut.rfind(". "), cut.rfind("। "))
    return (cut[:k+1] if k > 80 else cut.rsplit(" ", 1)[0] + "…").strip()
def _head(t, n=52):
    if len(t) <= n: return t
    for sep in (":", " — ", "?"):
        k = t.find(sep)
        if 12 < k <= n: return t[:k + (1 if sep == "?" else 0)]
    return t[:n].rsplit(" ", 1)[0]
def _local(src):
    src = src.split("?")[0]
    if src.startswith("https://sayedulabrar.site/"): src = src[len("https://sayedulabrar.site"):]
    return src if src.startswith("/") and (R/src.lstrip("/")).exists() else None
def discover(known):
    out = []
    for d in sorted((R/"blog").iterdir()):
        f = d/"index.html"
        if not f.is_file() or d.name.endswith("-bangla") or d.name in known: continue
        s = f.read_text(encoding="utf-8")
        if '<article class="article-content"' not in s or 'name="robots" content="noindex' in s: continue
        m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', s)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if not (m and h1): continue
        bn_dir = R/"blog"/(d.name + "-bangla")/"index.html"
        if bn_dir.is_file() and '<article class="article-content"' in bn_dir.read_text(encoding="utf-8"): bn = d.name + "-bangla"
        elif 'id="pane-bn"' in s: bn = d.name + "/#bn"
        else: bn = d.name
        og = re.search(r'og:image" content="([^"]+)"', s); oga = re.search(r'og:image:alt" content="([^"]*)"', s)
        cover = _local(og.group(1)) if og else None
        eb = re.search(r'class="eyebrow">(.*?)</p>', s); parts = [x.strip() for x in _txt(eb.group(1)).split("·")] if eb else []
        rd = re.search(r"(\d+(?:[–-]\d+)?)\s*MIN", " ".join(parts), re.I)
        kicker = next((x.title() for x in parts[1:] if "MIN" not in x.upper()), "Article")
        a0 = s.index('<article class="article-content"'); a1 = s.find('<h2 id="faq"', a0); body = s[a0:a1 if a1 > 0 else len(s)]
        hs = list(re.finditer(r"<h([23])[^>]*>(.*?)</h[23]>", body, re.S)); secs = []
        for k, h in enumerate(hs):
            seg = body[h.end(): hs[k+1].start() if k+1 < len(hs) else len(body)]
            im = re.search(r'<figure[^>]*>\s*(?:<a [^>]*>\s*)?<img src="([^"]+)" alt="([^"]*)"', seg)
            pr = re.search(r"<p>(.*?)</p>", seg, re.S)
            if im and _local(im.group(1)) and pr:
                head = re.sub(r"^(?:[0-9০-৯]+[.।]\s*|[A-Z]\s*[—-]\s*)", "", _txt(h.group(2)))
                secs.append((h.group(1), head, _short(_txt(pr.group(1))), _local(im.group(1)), html.unescape(im.group(2))))
        main = [x for x in secs if x[0] == "2"]; pick = main if len(main) >= 3 else secs
        if len(pick) > 5: pick = [pick[round(i*(len(pick)-1)/4)] for i in range(5)]
        if not pick or not cover: continue
        slides = [{"h": _head(x[1]), "p": [x[2]], "img": x[3], "alt": x[4], "r": "", "sub": "", "fit": "contain"} for x in pick]
        last = [x for x in secs][-1]
        desc = re.search(r'name="description" content="([^"]*)"', s)
        qk = re.search(r'<div class="quick">(.*?)</div>', body, re.S)
        endt = re.sub(r"^[^:]{3,25}:\s*", "", _txt(qk.group(1))) if qk else (html.unescape(desc.group(1)) if desc else slides[-1]["p"][0])
        out.append({"slug": d.name, "bn": bn, "date": m.group(1), "kicker": kicker, "title": _txt(h1.group(1)), "image": cover,
                    "alt": html.unescape(oga.group(1)) if oga else _txt(h1.group(1)), "accent": ACCENTS[len(out) % len(ACCENTS)],
                    "read": (rd.group(1) + " min") if rd else "5 min", "slides": slides,
                    "end": {"h": "KEEP READING", "t": _short(endt, 150), "img": last[3], "alt": last[4]}})
    return out
_cur = json.load(open(R/"_src/data/blog_stacks.json", encoding="utf-8"))
_auto = discover({a["slug"] for a in _cur})
for a in _auto: print("auto-added:", a["slug"], a["date"], len(a["slides"]), "slides")
data = sorted(_cur + _auto, key=lambda a: a["date"], reverse=True)
for a in data:
    assert (R/a["image"].lstrip("/")).exists(), a["image"]
    assert (R/"blog"/a["slug"]/"index.html").exists(), a["slug"]
    assert (R/"blog"/a["bn"].split("#")[0]/"index.html").exists(), a["bn"]
import statistics
def edge(path):
    im = Image.open(R/path.lstrip("/")).convert("RGB"); im.thumbnail((500, 500)); w, h = im.size; px = im.load(); t = max(2, min(w, h)//60)
    pts = [px[x, y] for x in range(w) for y in list(range(t)) + list(range(h-t, h))] + [px[x, y] for y in range(h) for x in list(range(t)) + list(range(w-t, w))]
    c = [int(statistics.median(p[i] for p in pts)) for i in range(3)]
    lum = (0.299*c[0] + 0.587*c[1] + 0.114*c[2]) / 255
    return "#%02x%02x%02x" % tuple(c), lum < 0.5
for a in data:
    for s in a["slides"] + [a["end"]]:
        s["bg"], s["dk"] = edge(s["img"])
tilt = [-1.6, 1.2, -0.8, 1.8, -1.2, 0.9, -1.9, 1.4, -0.6]
cards = ""
for i, a in enumerate(data):
    n = len(a["slides"]) + 2
    iw, ih = Image.open(R/a["image"].lstrip("/")).size
    new = '<span class="st-new">NEW</span>' if i == 0 else ""
    # small copy for the card (shown ~360px wide); full image stays as src for sharp zoom
    srcset = ""
    if iw > 900:
        sp = R/(re.sub(r"\.(webp|jpe?g|png)$", "-w750.webp", a["image"].split("?")[0], flags=re.I).lstrip("/"))
        if not sp.exists():
            im = Image.open(R/a["image"].lstrip("/")); im = im.convert("RGBA" if im.mode in ("P", "LA", "RGBA") else "RGB")
            im.resize((750, round(ih*750/iw)), Image.LANCZOS).save(sp, "WEBP", quality=82, method=6)
        srcset = f' srcset="/{sp.relative_to(R).as_posix()} 750w, {a["image"]} {iw}w" sizes="357px"'
    cards += (f'<li class="st-item" style="--tilt:{tilt[i%9]}deg;--ac:{a["accent"]}"><button class="st-stack" type="button" data-i="{i}" aria-haspopup="dialog">'
              f'<span class="st-pin" aria-hidden="true"></span><span class="st-sheet st-s2" aria-hidden="true"></span><span class="st-sheet st-s1" aria-hidden="true"></span>'
              f'<span class="st-card"><img src="{a["image"]}" alt="{e(a["alt"])}" width="{iw}" height="{ih}" loading="lazy" style="aspect-ratio:{iw}/{ih}"{srcset}>{new}'
              f'<span class="st-cap"><small>{e(a["kicker"]).upper()}</small><b>{e(a["title"])}</b><em>{e(a["read"])} full read · tap to swipe</em></span>'
              f'<span class="st-count">Summary · {n} slides</span></span></button>'
              f'<a class="st-link" href="/blog/{a["slug"]}/">Read full article ↗</a></li>')
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
section = f'''<!--stacks:start-->
  <section class="st-section" aria-labelledby="st-title">
    <div class="st-head">
      <div><p class="ed-script">Notes from my learning journey</p><h2 id="st-title">Featured from the Pharma Blog</h2></div>
      <div class="st-head-side"><p>Quick swipe-through summaries of my articles. Click a stack to flip through it, then read the full article if you want more.</p><a class="ed-arrow-link" href="/blog/">Explore all articles <span>↗</span></a></div>
    </div>
    <div class="st-line-wrap"><div class="st-line" aria-hidden="true"></div>
      <ul class="st-row" id="st-row">{cards}</ul></div>
    <p class="st-hint" aria-hidden="true">Scroll sideways for more →</p>
    <script type="application/json" id="st-data">{payload}</script>
  </section>
<!--stacks:end-->'''
p = R/"index.html"; s = p.read_text(encoding="utf-8")
if "<!--stacks:start-->" in s:
    s = re.sub(r"<!--stacks:start-->.*?<!--stacks:end-->", lambda m: section, s, flags=re.S)
else:
    a = s.index('<section class="ed-blog-section">'); b = s.index("</section>", a) + len("</section>")
    s = s[:a] + section + s[b:]
    s = s.replace('</head>', '<link rel="stylesheet" href="/assets/stacks.css?v=10"></head>', 1)
    s = s.replace('</body>', '<script src="/assets/stacks.js?v=10" defer></script></body>', 1)
p.write_text(s, encoding="utf-8"); print("ok", len(data))
