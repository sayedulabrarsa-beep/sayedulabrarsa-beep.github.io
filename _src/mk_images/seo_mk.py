#!/usr/bin/env python3
"""Pharmaceutical Marketing Strategy pictures: sitemap, feed, article data, blog card and stack data point at the new images."""
import re, json, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_mk import EN, BN, SITE, IMG, fn
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/pharma-marketing-strategy"
PAGES = {"en": ("blog/pharmaceutical-marketing-strategy-bangladesh/", EN), "bn": ("blog/pharmaceutical-marketing-strategy-bangladesh-bangla/", BN)}
TITLE = {"en": "Pharmaceutical Marketing Strategy in Bangladesh: A Practical, Ethical Framework", "bn": "বাংলাদেশে ফার্মাসিউটিক্যাল মার্কেটিং কৌশল: বাস্তবসম্মত ও নৈতিক পরিকল্পনা"}
OLD = IMG + "marketing-strategy-cover.svg"; OLD7 = IMG + "marketing-strategy-cover-w750.webp"; CARD = IMG + "mk-card.webp"; CARD7 = IMG + "mk-card-w750.webp"
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"; m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    lm = re.search(r'<lastmod>[^<]*</lastmod>', m.group(0)).group(0)
    imgs = f"<image:image><image:loc>{SITE}{IMG}mk-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(k, lang)}</image:loc><image:title>{html.escape(L[k][1], quote=False)}</image:title></image:image>" for k in L)
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"mk-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>(?:(?!</item>).)*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
ALT = EN["cover"][0]
def swap(t):
    t = re.sub(r'("inLanguage":"(bn|en)","image":")' + re.escape(SITE + OLD), lambda m: m.group(1) + f"{SITE}{IMG}mk-social-{m.group(2)}.jpg", t)
    return t.replace(OLD7, CARD7).replace(OLD, CARD)
for rel in ("assets/articles.json", "_src/data/articles.json", "blog/index.html"):
    p = R / rel; t = p.read_text(encoding="utf-8"); t2 = swap(t)
    if t2 != t: p.write_text(t2, encoding="utf-8"); print("updated", rel)
# curated homepage stack entry
bp = R / "_src/data/blog_stacks.json"; d = json.loads(bp.read_text(encoding="utf-8"))
e = [x for x in d if x["slug"] == "pharmaceutical-marketing-strategy-bangladesh"][0]
e["image"] = IMG + "mk-social-en.jpg"; e["alt"] = ALT
newimg = {"Start with market insight": ("research", EN), "Segment around real needs": ("segmentation", EN), "Position with evidence": ("positioning", EN), "Measure more than sales": ("scorecard", EN)}
for s in e["slides"]:
    k, L = newimg[s["h"]]; s["img"] = IMG + fn(k, "en"); s["alt"] = L[k][0]
e["end"]["img"] = IMG + fn("ethics", "en"); e["end"]["alt"] = EN["ethics"][0]
bp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
