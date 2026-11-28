#!/usr/bin/env python3
"""Product Management pictures: sitemap images, feed enclosures, article data, blog card + Blog JSON-LD images, homepage stack data."""
import re, json, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_pm import EN, BN, SITE, IMG, V, fn
R = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = R / "assets/img/blog/pharma-product-management"
SLUG = "pharmaceutical-product-management-bangladesh"
PAGES = {"en": (f"blog/{SLUG}/", EN), "bn": (f"blog/{SLUG}-bangla/", BN)}
TITLE = {"en": "Pharmaceutical Product Management in Bangladesh: From Market Insight to Brand Growth", "bn": "বাংলাদেশে ফার্মাসিউটিক্যাল প্রোডাক্ট ম্যানেজমেন্ট: কাজ, কৌশল ও দায়িত্ব"}
ORDER = ["cover", "what", "bangladesh", "roles", "framework", "checklist", "hcp", "kpi", "skills", "quality", "career", "review"]
# sitemap
sp = R / "sitemap.xml"; sm = sp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    loc = f"{SITE}/{path}"; m = re.search(r'<url><loc>' + re.escape(loc) + r'</loc>.*?</url>', sm, re.S); assert m
    lm = re.search(r'<lastmod>[^<]*</lastmod>', m.group(0)).group(0).replace("2026-11-26", "2026-11-28")
    imgs = f"<image:image><image:loc>{SITE}{IMG}pm-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang], quote=False)}</image:title></image:image>"
    imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(k, lang)}</image:loc><image:title>{html.escape(L[k][1].split(' AI-')[0], quote=False)}</image:title></image:image>" for k in ORDER)
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
sp.write_text(sm, encoding="utf-8")
# feed
fp = R / "blog/feed.xml"; fd = fp.read_text(encoding="utf-8")
for lang, (path, L) in PAGES.items():
    f = OUT / f"pm-social-{lang}.jpg"
    pat = re.compile(r'(<link>' + re.escape(f"{SITE}/{path}") + r'</link>(?:(?!</item>).)*?</description>)(\s*</item>)', re.S)
    enc = f'\n      <enclosure url="{SITE}{IMG}{f.name}" type="image/jpeg" length="{f.stat().st_size}" />'
    fd, n = pat.subn(lambda m: m.group(1) + enc + m.group(2), fd, count=1); assert n == 1, lang
fp.write_text(fd, encoding="utf-8")
# article data (card image)
CARD = IMG + "pm-card.webp"
ap = R / "assets/articles.json"; a = json.loads(ap.read_text(encoding="utf-8"))
for x in a:
    if x.get("slug") == SLUG: x["img"] = CARD
ap.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sp2 = R / "_src/data/articles.json"; d = json.loads(sp2.read_text(encoding="utf-8"))
d[SLUG] = {"tag_en": "Pharmaceutical Marketing", "tag_bn": "ফার্মাসিউটিক্যাল মার্কেটিং", "title_en": "Pharmaceutical Product Management in Bangladesh", "title_bn": TITLE["bn"],
           "desc_en": "A practical guide to market analysis, brand strategy, product lifecycle, ethical doctor engagement and KPIs.",
           "desc_bn": "বাজার বিশ্লেষণ, ব্র্যান্ড কৌশল, নৈতিক চিকিৎসক-যোগাযোগ ও KPI-সহ প্রোডাক্ট ম্যানেজমেন্টের ব্যবহারিক গাইড।", "img": CARD}
sp2.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
# blog index: JSON-LD images + card
bp = R / "blog/index.html"; b = bp.read_text(encoding="utf-8")
for lang in ("en", "bn"):
    u = f"{SITE}/blog/{SLUG}{'' if lang == 'en' else '-bangla'}/"
    b, n = re.subn(r'("url":"' + re.escape(u) + r'","datePublished":"[^"]*","dateModified":")[^"]*(","inLanguage":"' + lang + r'","image":")"', lambda m: m.group(1) + "2026-11-28" + m.group(2) + f"{SITE}{IMG}pm-social-{lang}.jpg{V}\"", b, count=1); assert n == 1, lang
if f'href="/blog/{SLUG}/" class="pb-card-image"' not in b:
    card = (f'<article class="pb-feature-card" data-topics="pharmaceutical marketing product management medicine bangla" data-search="pharmaceutical product management Bangladesh product manager brand planning KPIs ethical HCP engagement doctor profiling PMD pharmacy career {html.escape(TITLE["bn"])} প্রোডাক্ট ম্যানেজমেন্ট ফার্মা ব্র্যান্ড" '
            f'data-bn-title="বাংলাদেশে ফার্মাসিউটিক্যাল প্রোডাক্ট ম্যানেজমেন্ট" data-bn-img="{IMG}pm-social-bn.jpg{V}"><a href="/blog/{SLUG}/" class="pb-card-image">'
            f'<img src="{IMG}pm-card-w750.webp" alt="{html.escape(EN["cover"][0], quote=True)}" width="1200" height="630" loading="lazy" decoding="async" srcset="{IMG}pm-card-w750.webp 750w, {IMG}pm-card.webp 1200w" sizes="357px"><span class="pb-image-label">NEW · PRODUCT MANAGEMENT</span></a>'
            f'<div class="pb-card-copy"><p class="pb-card-meta">PHARMACEUTICAL MARKETING <span>·</span> 10 MIN READ</p><h3><a href="/blog/{SLUG}/">{TITLE["en"]}</a></h3>'
            f'<p>A practical guide to pharmaceutical product management in Bangladesh: market analysis, brand strategy, product lifecycle, ethical doctor engagement, cross-functional work and KPIs.</p>'
            f'<p class="pb-bangla" lang="bn">বাংলাদেশের ওষুধ শিল্পে প্রোডাক্ট ম্যানেজমেন্ট কীভাবে কাজ করে? বাজার বিশ্লেষণ, ব্র্যান্ড কৌশল, নৈতিক HCP engagement ও KPI সহজভাবে জানুন।</p>'
            f'<a class="pb-read-link" href="/blog/{SLUG}/">Read in English ↗</a><a class="pb-bangla-link" href="/blog/{SLUG}-bangla/">বাংলায় পড়ুন ↗</a></div></article>')
    m = re.search(r'<article class="pb-feature-card"(?:(?!</article>).)*pharmaceutical-marketing-strategy-bangladesh/(?:(?!</article>).)*</article>', b, re.S); assert m
    b = b[:m.end()] + card + b[m.end():]
n = len(re.findall(r'<article class="pb-feature-card"', b))
b = re.sub(r'(<p id="pb-card-count" role="status">)\d+( articles)', lambda m: f"{m.group(1)}{n}{m.group(2)}", b)
bp.write_text(b, encoding="utf-8"); print("cards", n)
# homepage stack (curated entry)
stp = R / "_src/data/blog_stacks.json"; st = json.loads(stp.read_text(encoding="utf-8"))
st = [x for x in st if x["slug"] != SLUG]
def sl(h, p, k, r): return {"h": h, "p": [p], "img": IMG + fn(k, "en"), "alt": EN[k][0], "r": r, "sub": "", "fit": "contain"}
st.append({"slug": SLUG, "bn": SLUG + "-bangla", "date": "2026-11-24", "kicker": "Pharmaceutical Marketing", "title": TITLE["en"], "image": IMG + "pm-social-en.jpg", "alt": EN["cover"][0], "accent": "#2f8f83", "read": "10 min",
           "slides": [sl("More than promotion", "Product management connects healthcare need, market data, positioning, availability and ethical execution.", "what", "A brand is built by more than promotion."),
                      sl("Plan in six steps", "Move from insight to positioning, objectives, planning, execution and review.", "framework", "Plan the brand step by step."),
                      sl("Engage ethically", "Use approved, current information and respect the doctor’s time and judgement.", "hcp", "Science, not inducements."),
                      sl("Measure beyond sales", "Track growth, availability, engagement quality and compliance together.", "kpi", "Choose KPIs that answer the strategy’s questions.")],
           "end": {"h": "KEY TAKEAWAY", "t": "A strong pharmaceutical brand combines market insight, quality, ethical engagement and measurable follow-through.", "img": IMG + fn("review", "en"), "alt": EN["review"][0]}})
stp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("done")
