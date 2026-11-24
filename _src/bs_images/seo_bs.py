#!/usr/bin/env python3
"""Biosimilars pictures: sitemap, feed, article data and blog card point at the new images."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_bs import EN, BN, FILES, SITE, IMG
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/biosimilars"
PAGES = {"en": ("blog/biosimilars-explained/", EN), "bn": ("blog/biosimilars-explained-bangla/", BN)}
TITLE = {"en": "Biosimilars Explained: How Similar Are They to Original Biologic Medicines?", "bn": "বায়োসিমিলার: আসল বায়োলজিক ওষুধের সঙ্গে কতটা মিল?"}
CARD = IMG + "bs-card.webp"; CARD7 = IMG + "bs-card-w750.webp"; OLD = IMG + "biosimilars-cover.svg"
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    imgs = f"<image:image><image:loc>{SITE}{IMG}bs-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{FILES[k]}.webp</image:loc><image:title>{html.escape(L[k][1], quote=False)}</image:title></image:image>" for k in FILES)
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc><lastmod>2026-11-24</lastmod>{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"bs-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
for rel in ("assets/articles.json", "_src/data/articles.json"):
    p = R / rel
    if p.exists():
        t = p.read_text(encoding="utf-8"); t2 = t.replace(OLD, CARD)
        if t2 != t: p.write_text(t2, encoding="utf-8"); print("updated", rel)
bp = R / "blog/index.html"; b = bp.read_text(encoding="utf-8")
old = f'<img src="{OLD}" alt="Editorial illustration of a biological cell, a protein molecule and a medicine vial representing biosimilar medicines." width="1600" height="900" loading="lazy" decoding="async">'
assert old in b
b = b.replace(old, f'<img src="{CARD7}" alt="{html.escape(EN["cover"][0])}" width="1200" height="630" loading="lazy" decoding="async" srcset="{CARD7} 750w, {CARD} 1200w" sizes="357px">')
b = b.replace(SITE + OLD, f"{SITE}{IMG}bs-social-en.jpg")
assert "biosimilars-cover.svg" not in b, re.findall(r'.{40}biosimilars-cover.svg', b)
bp.write_text(b, encoding="utf-8")
print("seo done")
