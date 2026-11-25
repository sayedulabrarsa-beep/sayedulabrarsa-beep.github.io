#!/usr/bin/env python3
"""Clinical Trial Phases pictures: sitemap, feed, article data, blog card and homepage stack point at the new images."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_ct import EN, BN, FILES, SITE, IMG, fn
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/clinical-trial-phases"
PAGES = {"en": ("blog/clinical-trial-phases-explained/", EN), "bn": ("blog/clinical-trial-phases-explained-bangla/", BN)}
TITLE = {"en": "Clinical Trial Phases Explained: From First-in-Human to Post-Marketing", "bn": "ক্লিনিক্যাল ট্রায়ালের ধাপগুলো সহজ ভাষায়"}
OLDS = IMG + "clinical-trial-phases-social.svg"; OLD7 = IMG + "clinical-trial-phases-social-w750.webp"
CARD = IMG + "ct-card.webp"; CARD7 = IMG + "ct-card-w750.webp"
ALT = EN["cover"][0]
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    lm = re.search(r'<lastmod>[^<]*</lastmod>', m.group(0)).group(0)
    imgs = f"<image:image><image:loc>{SITE}{IMG}ct-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(k, lang)}</image:loc><image:title>{html.escape(L[k][1], quote=False)}</image:title></image:image>" for k in FILES)
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"ct-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type=")[^"]*(" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + f"{SITE}{IMG}{f.name}" + m.group(2) + "image/jpeg" + m.group(3) + str(f.stat().st_size) + m.group(4), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
def swap(t):
    t = re.sub(r'("inLanguage":"(bn|en)","image":")' + re.escape(SITE + OLDS), lambda m: m.group(1) + f"{SITE}{IMG}ct-social-{m.group(2)}.jpg", t)
    t = t.replace(OLD7, CARD7).replace(OLDS, CARD)
    for a in ("Clinical trial phases: safety, early signal, confirmation and post-marketing follow-up.",
              "Original four-stage clinical trial phases diagram showing Phase I safety, Phase II early activity, Phase III confirmation and Phase IV follow-up."):
        t = t.replace(a, html.escape(ALT, quote=True) if "<" in t[:1] or False else ALT)
    return t
for rel in ("assets/articles.json", "_src/data/articles.json", "index.html", "blog/index.html"):
    p = R / rel
    if p.exists():
        t = p.read_text(encoding="utf-8"); t2 = swap(t)
        if t2 != t: p.write_text(t2, encoding="utf-8"); print("updated", rel)
bad = [r for r in ("index.html", "blog/index.html", "assets/articles.json", "_src/data/articles.json", "blog/feed.xml") if "clinical-trial-phases-social" in (R / r).read_text(encoding="utf-8")]
print("left:", bad)
