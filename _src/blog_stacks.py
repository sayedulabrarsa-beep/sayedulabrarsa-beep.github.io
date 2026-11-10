#!/usr/bin/env python3
"""Rebuilds the home-page 'Featured from the Pharma Blog' clothesline section from _src/data/blog_stacks.json.
To add a new article: append an entry to the JSON (newest date sorts first), then run this script."""
import json, html, pathlib, re
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
data = sorted(json.load(open(R/"_src/data/blog_stacks.json", encoding="utf-8")), key=lambda a: a["date"], reverse=True)
e = html.escape
for a in data:
    assert (R/a["image"].lstrip("/")).exists(), a["image"]
    assert (R/"blog"/a["slug"]/"index.html").exists(), a["slug"]
    assert (R/"blog"/a["bn"].split("#")[0]/"index.html").exists(), a["bn"]
tilt = [-1.6, 1.2, -0.8, 1.8, -1.2, 0.9, -1.9, 1.4, -0.6]
cards = ""
for i, a in enumerate(data):
    n = len(a["slides"]) + 2
    iw, ih = Image.open(R/a["image"].lstrip("/")).size
    new = '<span class="st-new">NEW</span>' if i == 0 else ""
    cards += (f'<li class="st-item" style="--tilt:{tilt[i%9]}deg;--ac:{a["accent"]}"><button class="st-stack" type="button" data-i="{i}" aria-haspopup="dialog" aria-label="Open summary: {e(a["title"])} ({n} slides)">'
              f'<span class="st-pin" aria-hidden="true"></span><span class="st-sheet st-s2" aria-hidden="true"></span><span class="st-sheet st-s1" aria-hidden="true"></span>'
              f'<span class="st-card"><img src="{a["image"]}" alt="{e(a["alt"])}" width="{iw}" height="{ih}" loading="lazy" style="aspect-ratio:{iw}/{ih}">{new}'
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
    s = s.replace('</head>', '<link rel="stylesheet" href="/assets/stacks.css?v=8"></head>', 1)
    s = s.replace('</body>', '<script src="/assets/stacks.js?v=8" defer></script></body>', 1)
p.write_text(s, encoding="utf-8"); print("ok", len(data))
