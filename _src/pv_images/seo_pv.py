#!/usr/bin/env python3
"""Pharmacovigilance pictures: sitemap, feed, article data and blog card now point at the new images."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_pv import EN, BN, FILES, SITE, IMG
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/pharmacovigilance"
PAGES = {"en": ("blog/pharmacovigilance-medicine-safety-monitoring/", EN), "bn": ("blog/pharmacovigilance-medicine-safety-monitoring-bangla/", BN)}
TITLE = {"en": "Pharmacovigilance: How Are Medicines Monitored for Safety?", "bn": "ফার্মাকোভিজিল্যান্স: ওষুধের নিরাপত্তা কীভাবে পর্যবেক্ষণ করা হয়?"}
CARD = IMG + "pv-card.webp"; CARD7 = IMG + "pv-card-w750.webp"
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    imgs = f"<image:image><image:loc>{SITE}{IMG}pv-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{FILES[k]}.webp</image:loc><image:title>{html.escape(L[k][1], quote=False)}</image:title></image:image>" for k in FILES)
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc><lastmod>2026-11-23</lastmod>{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"pv-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
OLD = IMG + "pharmacovigilance-cover.svg"
for rel in ("assets/articles.json", "_src/data/articles.json"):
    p = R / rel; t = p.read_text(encoding="utf-8"); t2 = t.replace(OLD, CARD); assert t2 != t, rel; p.write_text(t2, encoding="utf-8")
bp = R / "blog/index.html"; b = bp.read_text(encoding="utf-8")
old = f'<img src="{OLD}" alt="Symbolic illustration of medicine packs, a safety shield and connected pharmacovigilance reporting nodes." width="1600" height="900" loading="lazy" decoding="async">'
assert old in b
b = b.replace(old, f'<img src="{CARD7}" alt="{html.escape(EN["cover"][0])}" width="1200" height="630" loading="lazy" decoding="async" srcset="{CARD7} 750w, {CARD} 1200w" sizes="357px">')
b = b.replace(SITE + OLD, f"{SITE}{IMG}pv-social-en.jpg")
assert "pharmacovigilance-cover.svg" not in b
bp.write_text(b, encoding="utf-8")
print("seo done")
