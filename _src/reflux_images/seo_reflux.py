#!/usr/bin/env python3
"""SEO follow-ups for the heartburn/GERD pictures: card images, schema images, sitemap, feed, card, article lists."""
import re, json, pathlib, sys, html
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_reflux import EN, BN, SITE, IMG
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/reflux"
PAGES = {"en": ("blog/heartburn-vs-acid-reflux-vs-gerd/", EN), "bn": ("blog/heartburn-vs-acid-reflux-vs-gerd-bangla/", BN)}
CARD = IMG + "reflux-card.webp"; CARD7 = IMG + "reflux-card-w750.webp"

# 1) card images
hero = Image.open(OUT / "hero.webp").convert("RGB")
hero.resize((1200, 675), Image.LANCZOS).save(OUT / "reflux-card.webp", "WEBP", quality=84, method=6)
hero.resize((750, 422), Image.LANCZOS).save(OUT / "reflux-card-w750.webp", "WEBP", quality=82, method=6)

def img_list(L, lang):
    first = ("reflux-social-%s.jpg" % lang, L["og_alt"], 1200, 630)
    rest = [(k, v, 1600, 900) if not k.startswith("story") else (k, v, 1200, 1200) for k, v in L["sm"].items()]
    return [first] + rest

CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
def obj(name, cap, w, h):
    u = SITE + IMG + name
    return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": h, "caption": cap, "creator": CRE,
            "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}

# 2) page schema
for lang, (path, L) in PAGES.items():
    p = R / path / "index.html"; h = p.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "Article".*?)</script>', h, re.S)
    d = json.loads(m.group(1))
    d["image"] = [obj(*t) for t in img_list(L, lang)]
    d["dateModified"] = "2026-11-23"
    new = json.dumps(d, ensure_ascii=False)
    h = h[:m.start(1)] + new + h[m.end(1):]
    p.write_text(h, encoding="utf-8")

# 3) sitemap
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"
    m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S)
    imgs = "".join(f"<image:image><image:loc>{SITE}{IMG}{n}</image:loc><image:title>{html.escape(c, quote=False)}</image:title></image:image>" for n, c, _, _ in img_list(L, lang))
    imgs += f"<image:image><image:loc>{SITE}/assets/img/sayedul-abrar.jpg</image:loc></image:image>"
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc><lastmod>2026-11-23</lastmod>{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")

# 4) feed enclosures
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"reflux-social-{lang}.jpg"
    url = f"{SITE}{IMG}{f.name}"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>.*?<enclosure url=")[^"]*(" type="image/jpeg" length=")\d+(")', re.S)
    fd, n = pat.subn(lambda m: m.group(1) + url + m.group(2) + str(f.stat().st_size) + m.group(3), fd, count=1)
    assert n == 1, lang
fp.write_text(fd, encoding="utf-8")

# 5) article data + stacks + blog card
for rel in ("assets/articles.json", "_src/data/articles.json", "_src/data/blog_stacks.json"):
    p = R / rel; t = p.read_text(encoding="utf-8")
    t2 = t.replace("/assets/img/blog/heartburn-gerd-index-card.webp", CARD)
    assert t2 != t, rel
    p.write_text(t2, encoding="utf-8")
bp = R / "blog/index.html"; b = bp.read_text(encoding="utf-8")
old = re.search(r'<img src="/assets/img/blog/heartburn-gerd-index-card-w750\.webp" alt="[^"]*" width="1600" height="900" loading="lazy" srcset="[^"]*" sizes="357px">', b)
assert old
b = b.replace(old.group(0), f'<img src="{CARD7}" alt="{html.escape(EN["sm"]["hero.webp"])}" width="1200" height="675" loading="lazy" srcset="{CARD7} 750w, {CARD} 1200w" sizes="357px">')
b = b.replace(SITE + "/assets/img/blog/heartburn-gerd-hero.jpg", f"{SITE}{IMG}reflux-social-en.jpg")
bp.write_text(b, encoding="utf-8")
print("seo done")
