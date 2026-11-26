#!/usr/bin/env python3
"""Pharmacogenetics pictures: sitemap, feed, article data, blog card and homepage stack use the new images."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_px import EN, BN, CAP, BCAP, KEYS, SITE, IMG, fn, SLUG
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/pharmacogenetics"
PAGES = {"en": (f"blog/{SLUG}/", EN, CAP), "bn": (f"blog/{SLUG}-bangla/", BN, BCAP)}
TITLE = {"en": "Pharmacogenetics: Can Your Genes Change How Medicines Work?", "bn": "ফার্মাকোজেনেটিক্স: আপনার জিন কি ওষুধের প্রতিক্রিয়া বদলে দিতে পারে?"}
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, A, C) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    lm = re.search(r'<lastmod>[^<]*</lastmod>', m.group(0)).group(0)
    imgs = f"<image:image><image:loc>{SITE}{IMG}px-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(k, lang)}</image:loc><image:title>{html.escape(C[k], quote=False)}</image:title></image:image>" for k in KEYS)
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, A, C) in PAGES.items():
    f = OUT / f"px-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
OLD = IMG + "pgx-cover.svg"; ALT = "AI-generated photo-style image: gloved hands holding a clear sample tube in front of a DNA sequencing machine."
def swap(t):
    t = t.replace(OLD, IMG + "px-card.webp")
    for a in ("Original vector artwork showing a DNA double helix beside a medicine capsule, representing how genes can influence medicine response.",
              "Original vector artwork showing a DNA double helix and medicine capsule to represent pharmacogenetics."):
        t = t.replace(a, ALT)
    return t
for rel in ("assets/articles.json", "_src/data/articles.json", "index.html", "blog/index.html"):
    p = R / rel
    if p.exists():
        t = p.read_text(encoding="utf-8"); t2 = swap(t)
        if t2 != t: p.write_text(t2, encoding="utf-8"); print("updated", rel)
print("left:", [r for r in ("index.html", "blog/index.html", "assets/articles.json", "_src/data/articles.json", "blog/feed.xml") if "pgx-cover" in (R / r).read_text(encoding="utf-8")])
