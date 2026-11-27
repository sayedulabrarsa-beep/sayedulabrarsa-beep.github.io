#!/usr/bin/env python3
"""Cold Chain pictures: sitemap, feed, article data, blog card and homepage stack use the new images."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_cc import EN, BN, CAP, BCAP, KEYS, SITE, IMG, fn, SLUG
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/cold-chain"
PAGES = {"en": (f"blog/{SLUG}/", EN, CAP), "bn": (f"blog/{SLUG}-bangla/", BN, BCAP)}
TITLE = {"en": "Pharmaceutical Cold Chain: How Are Temperature-Sensitive Medicines Stored and Transported?", "bn": "ফার্মাসিউটিক্যাল কোল্ড চেইন: তাপমাত্রা-সংবেদনশীল ওষুধ কীভাবে সংরক্ষণ ও পরিবহন করা হয়?"}
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, A, C) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    lm = re.search(r'<lastmod>[^<]*</lastmod>', m.group(0)).group(0)
    imgs = f"<image:image><image:loc>{SITE}{IMG}cc-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(k, lang)}</image:loc><image:title>{html.escape((C.get(k) or A[k]), quote=False)}</image:title></image:image>" for k in KEYS)
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, A, C) in PAGES.items():
    f = OUT / f"cc-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
ALT = "AI-generated photo-style image: a gloved hand lifts the lid of a white insulated shipper, with cold vapour drifting over glass vials."
OLD_ALT = ["Original vector illustration of a temperature-sensitive medicine protected inside an insulated shipper, with a logger and a route from manufacturer to patient.",
           "Original vector illustration of a temperature-sensitive medicine protected in an insulated shipper, with a digital logger and a route from manufacturer to patient."]
srcset_old = "/assets/img/blog/cold-chain/cold-chain-cover-w750.webp 750w, /assets/img/blog/cold-chain/cold-chain-cover.svg 1600w"
srcset_new = IMG + "cc-card-w750.webp 750w, " + IMG + "cc-card.webp 1200w"
def swap(t):
    t = t.replace(srcset_old, srcset_new)
    t = t.replace('width="1600" height="900" loading="lazy" style="aspect-ratio:1600/900"', 'width="1200" height="630" loading="lazy" style="aspect-ratio:1200/630"')
    t = t.replace('alt="' + OLD_ALT[1] + '" loading="lazy" width="1600" height="900">', 'alt="' + ALT + '" loading="lazy" width="1200" height="630" srcset="' + srcset_new + '" sizes="357px">')
    t = t.replace(IMG + "cold-chain-cover.svg", IMG + "cc-card.webp")
    for a in OLD_ALT: t = t.replace(a, ALT)
    return t
for rel in ("assets/articles.json", "_src/data/articles.json", "index.html", "blog/index.html"):
    p = R / rel; t = p.read_text(encoding="utf-8"); t2 = swap(t)
    if t2 != t: p.write_text(t2, encoding="utf-8"); print("updated", rel)
print("left:", [r for r in ("index.html", "blog/index.html", "assets/articles.json", "_src/data/articles.json", "blog/feed.xml", "sitemap.xml") if "cold-chain-cover" in (R / r).read_text(encoding="utf-8")])
