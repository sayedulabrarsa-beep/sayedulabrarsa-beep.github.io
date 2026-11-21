#!/usr/bin/env python3
"""Builds the EN + BN pages for a pharmacokinetics-series article from a content module in this folder.
Usage: python3 _src/kinetics_articles/build_k.py halflife
Pages are written with robots noindex; _src/apply_editorial_calendar.py releases them at 8 PM on their calendar date."""
import sys, json, html, importlib, pathlib
H = pathlib.Path(__file__).resolve().parent
ROOT = H.parent.parent
sys.path.insert(0, str(H))
A = importlib.import_module(sys.argv[1])
SITE = "https://sayedulabrar.site"
E = lambda s: html.escape(s, quote=True)
BND = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

HEAD_STYLE = """<style>.article-content{max-width:900px!important;line-height:1.82}.article-content h2{margin:34px 0 10px}.article-content p{margin:12px 0}.article-content .lang-switch{display:flex;gap:8px;margin:18px 0 24px}.article-content .lang-switch a{min-height:44px;display:inline-flex;align-items:center;justify-content:center;border:1px solid #cbd9dc;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:600}.article-content .lang-switch .active{background:#17656a;color:white}.article-content .hero-visual{background:linear-gradient(135deg,#eaf4f1,#fff5e8);border-radius:18px;padding:12px;margin:22px 0}.article-content .hero-visual img{display:block;width:100%;height:auto;border-radius:12px}.article-content .quick,.article-content .takeaways{padding:18px 20px;background:#edf6f3;border-left:4px solid #287c73;border-radius:12px;margin:20px 0}.article-content .author-card{display:flex;gap:16px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:18px;margin:30px 0}.article-content .author-card img{width:76px;height:76px;border-radius:50%;object-fit:cover}@media(max-width:600px){.article-content .author-card{align-items:flex-start}}
.article-content table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.96em}.article-content th,.article-content td{border:1px solid #d6e2df;padding:10px 12px;text-align:left;vertical-align:top}.article-content th{background:#edf6f3;color:#174F52}.article-content .table-wrap{overflow-x:auto}
.article-content .note{padding:14px 18px;background:#fff7ec;border-left:4px solid #E98250;border-radius:12px;margin:18px 0}
.article-content .series-nav{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:30px 0}.article-content .series-nav a{display:block;border:1px solid #d6e2df;border-radius:14px;padding:14px 16px;text-decoration:none;background:#fbfdfc}.article-content .series-nav small{display:block;color:#526D82;font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:.78em}.article-content .series-nav b{display:block;color:#174F52;line-height:1.35;margin-top:4px}.article-content .series-nav .next{text-align:right}.article-content .series-hub{grid-column:1/-1;text-align:center}@media(max-width:600px){.article-content .series-nav{grid-template-columns:1fr}.article-content .series-nav .next{text-align:left}}
.article-content .series-list{counter-reset:s;list-style:none;padding:0;margin:20px 0;display:grid;gap:12px}.article-content .series-list li{counter-increment:s;display:flex;gap:14px;align-items:flex-start;border:1px solid #d6e2df;border-radius:14px;padding:14px 16px;background:#fbfdfc}.article-content .series-list li:before{content:counter(s);flex:none;width:38px;height:38px;border-radius:50%;background:#174F52;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center}.article-content .series-list li.later:before{background:#E98250}html[lang=bn] .article-content ol:not(.series-list){list-style-type:bengali}.article-content .series-list b{display:block;color:#174F52}.article-content .series-list span{display:block;color:#253238;margin-top:2px}</style>"""

ICONS = """<link rel="icon" href="/favicon.ico?v=sa-logo-20261114" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/assets/icons/favicon-48x48.png?v=sa-logo-20261114"><link rel="icon" type="image/png" sizes="96x96" href="/assets/icons/favicon-96x96.png?v=sa-logo-20261114"><link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png?v=sa-logo-20261114"><link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png?v=sa-logo-20261114"><link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png?v=sa-logo-20261114"><link rel="manifest" href="/site.webmanifest?v=sa-logo-20261114"><style id="logo-mark-css">.logo-mark{display:inline-block;width:1.3em;height:1.3em;border-radius:50%;vertical-align:-.28em;margin-right:.38em;box-shadow:0 0 0 1px rgba(194,140,30,.35)}@media (max-width:420px){.logo-mark{width:1.15em;height:1.15em}}</style>"""

def build(lang):
    bn = lang == "bn"
    d = A.BN if bn else A.EN
    slug = A.SLUG + ("-bangla" if bn else "")
    url = f"{SITE}/blog/{slug}/"
    en_url, bn_url = f"{SITE}/blog/{A.SLUG}/", f"{SITE}/blog/{A.SLUG}-bangla/"
    img = lambda n: f"/assets/img/blog/{A.IMGDIR}/{n}{'-bn' if bn else ''}.webp"
    social = f"{SITE}/assets/img/blog/{A.IMGDIR}/{A.PREFIX}-social-{lang}.jpg"
    assert len(d["description"]) <= 160, (lang, len(d["description"]))
    figs = [img(A.COVER)] + [img(f[0]) for s in d["sections"] for f in ([s["fig"]] if s.get("fig") else [])]
    blog = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": d["title"], "description": d["description"],
            "inLanguage": "bn-BD" if bn else "en-BD", "datePublished": A.DATE, "dateModified": A.DATE,
            "image": [social] + [SITE + f for f in figs],
            "author": {"@type": "Person", "name": "Sayedul Abrar", "url": f"{SITE}/about/"},
            "publisher": {"@type": "Person", "name": "Sayedul Abrar", "url": f"{SITE}/"},
            "mainEntityOfPage": url, "isAccessibleForFree": True, "keywords": d["keywords"]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Pharma Blog", "item": f"{SITE}/blog/"},
        {"@type": "ListItem", "position": 3, "name": d["title"], "item": url}]}
    J = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"
    extra_ld = "".join(J(x(lang)) for x in getattr(A, "EXTRA_LD", []))
    head = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{E(d["title"])} | Sayedul Abrar</title><meta name="description" content="{E(d["description"])}"><meta name="author" content="Sayedul Abrar">'
            f'<meta name="robots" content="noindex,nofollow"><link rel="canonical" href="{url}">'
            f'<link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="bn" href="{bn_url}"><link rel="alternate" hreflang="x-default" href="{en_url}">'
            f'<meta property="og:type" content="article"><meta property="og:locale" content="{"bn_BD" if bn else "en_US"}"><meta property="og:site_name" content="Sayedul Abrar">'
            f'<meta property="og:title" content="{E(d["title"])}"><meta property="og:description" content="{E(d["description"])}"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{social}"><meta property="og:image:secure_url" content="{social}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{E(d["cover_alt"])}">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(d["title"])}"><meta name="twitter:description" content="{E(d["description"])}"><meta name="twitter:image" content="{social}"><meta name="twitter:image:alt" content="{E(d["cover_alt"])}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="/assets/style.css?v=pb-next-20261112"><link rel="stylesheet" href="/assets/nav-pill.css?v=stable-nav-20261120"><link rel="stylesheet" href="/assets/site-polish.css">'
            + HEAD_STYLE + J(blog) + J(faq) + f'<meta property="article:published_time" content="{A.DATE}T20:00:00+06:00">' + J(crumbs) + extra_ld +
            '<style id="fig-fit">.article-figure{margin:28px 0}.article-figure a{display:block}.article-figure img,.hero-visual img{display:block;width:100%;height:auto;border-radius:14px}.article-figure figcaption{font-size:14px;color:#526D82;margin-top:8px}</style>'
            + ICONS + '</head>')
    nav = ('<body><a class="skip" href="#main">Skip to content</a><header><div class="wrap bar"><a class="logo" href="/"><img class="logo-mark" src="/assets/img/sayedul-abrar-logo-badge-96.webp" srcset="/assets/img/sayedul-abrar-logo-badge-96.webp 1x, /assets/img/sayedul-abrar-logo-badge-192.webp 2x" alt="Sayedul Abrar SA logo" width="34" height="34" decoding="async">Sayedul Abrar</a>'
           '<nav aria-label="Main"><ul class="menu" id="menu"><li><a href="/">Home</a></li><li><a href="/about/">About</a></li><li><a href="/blog/" aria-current="page">Pharma Blog</a></li><li><a href="/contact/">Contact</a></li></ul></nav></div></header>')
    day = int(A.DATE[8:]); months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    bnmonths = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
    mi = int(A.DATE[5:7]) - 1
    datestr = f"{str(day).translate(BND)} {bnmonths[mi]} ২০২৬" if bn else f"{day} {months[mi]} 2026"
    body = (f'<main id="main"><section class="page-head"><div class="wrap"><p class="eyebrow">{d["eyebrow"]}</p><h1>{E(d["h1"])}</h1><p>{d["lead"]}</p></div></section>'
            f'<section class="wrap"><article class="article-content"><nav class="lang-switch" aria-label="Language">'
            f'<a{" class=\"active\"" if not bn else ""} href="/blog/{A.SLUG}/" lang="en">English</a><a{" class=\"active\"" if bn else ""} href="/blog/{A.SLUG}-bangla/" lang="bn">বাংলা</a></nav>'
            f'<figure class="hero-visual"><a href="{img(A.COVER)}?v=1" target="_blank" rel="noopener"><img src="{img(A.COVER)}?v=1" alt="{E(d["cover_alt"])}" width="1600" height="900" fetchpriority="high" decoding="async"></a><figcaption class="caption">{d["cover_caption"]}</figcaption></figure>'
            f'<p class="byline-seo">{"লিখেছেন" if bn else "By"} <a href="/about/" rel="author">{"সাইয়্যেদুল আবরার" if bn else "Sayedul Abrar"}</a>, {"ফার্মাসিস্ট" if bn else "pharmacist"} · <time datetime="{A.DATE}">{datestr}</time></p>'
            f'<div class="quick"><strong>{"সহজভাবে:" if bn else "In simple terms:"}</strong> {d["quick"]}</div>')
    n = 0
    for s in d["sections"]:
        body += f'<h2{" id=" + chr(34) + s["id"] + chr(34) if s.get("id") else ""}>{s["h2"]}</h2>{s["html"]}'
        if s.get("fig"):
            n += 1; f = s["fig"]
            body += (f'<figure class="article-figure"><a href="{img(f[0])}?v=1" target="_blank" rel="noopener"><img src="{img(f[0])}?v=1" alt="{E(f[1])}" width="1600" height="900" loading="lazy" decoding="async"></a>'
                     f'<figcaption>{"চিত্র" if bn else "Figure"} {str(n).translate(BND) if bn else n} · {f[2]}</figcaption></figure>')
        if s.get("after"):
            body += s["after"]
    if d.get("takeaways"):
        body += '<div class="takeaways"><ul>' + "".join(f"<li>{t}</li>" for t in d["takeaways"]) + "</ul></div>"
    body += f'<h2 id="faq">{"সাধারণ প্রশ্ন" if bn else "Frequently asked questions"}</h2>' + "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in d["faqs"])
    sn = d.get("series", {})
    if sn:
        body += '<nav class="series-nav" aria-label="' + ("সিরিজের অন্য লেখা" if bn else "More in this series") + '">'
        if sn.get("prev"):
            body += f'<a class="prev" href="{sn["prev"][0]}"><small>{"আগের লেখা" if bn else "Previous in series"}</small><b>← {sn["prev"][1]}</b></a>'
        else:
            body += "<span></span>"
        if sn.get("next"):
            body += f'<a class="next" href="{sn["next"][0]}"><small>{"সিরিজের পরের লেখা" if bn else "Next in series"}</small><b>{sn["next"][1]} →</b></a>'
        if sn.get("hub"):
            body += f'<a class="series-hub" href="{sn["hub"][0]}"><small>{"পুরো সিরিজ" if bn else "Full series"}</small><b>{sn["hub"][1]}</b></a>'
        body += "</nav>"
    if d.get("related"):
        body += f'<h2>{"আরও পড়ুন" if bn else "Related reading"}</h2><ul>' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in d["related"]) + "</ul>"
    body += f'<h2>{"তথ্যসূত্র ও আরও পড়ুন" if bn else "References and further reading"}</h2><ol>' + "".join(
        f'<li>{t}. <a href="{u}" target="_blank" rel="noopener noreferrer">{E(u.split("/")[2].replace("www.", ""))}</a></li>' for t, u in A.REFS) + "</ol>"
    body += (f'<div class="disclaimer"><strong>{"শিক্ষামূলক সতর্কতা:" if bn else "Educational disclaimer:"}</strong> '
             + ("এই লেখা সাধারণ শেখার জন্য, ব্যক্তিগত চিকিৎসা পরামর্শ নয়। চিকিৎসক বা ফার্মাসিস্টের সাথে কথা না বলে কোনো ওষুধ বা ডোজ পরিবর্তন করবেন না। জরুরি অবস্থায় দ্রুত চিকিৎসা নিন।" if bn else
                "This article is for general learning and is not personal medical advice. Do not change a medicine or dose without talking to a doctor or pharmacist. In an emergency, get medical help quickly.")
             + "</div>")
    body += ('<section class="author-card" aria-label="Author information"><img src="/assets/img/sayedul-abrar.jpg" alt="Sayedul Abrar, pharmacist" width="76" height="76" loading="lazy"><div>'
             f'<h2>{"সাইয়্যেদুল আবরার" if bn else "Sayedul Abrar"}</h2><p><strong>A Grade Pharmacist · Registration Code: A-22040</strong></p>'
             f'<p>{"প্রোডাক্ট এক্সিকিউটিভ, প্রোডাক্ট ম্যানেজমেন্ট ডিপার্টমেন্ট (PMD) · Opsonin Pharma Ltd." if bn else "Product Executive, Product Management Department (PMD) · Opsonin Pharma Ltd."}</p>'
             f'<p><a href="/about/">{"লেখকের প্রোফাইল" if bn else "View author profile"}</a> · <a href="https://www.linkedin.com/in/sayedulabrar" target="_blank" rel="noopener noreferrer">LinkedIn</a></p></div></section></article></section>')
    more = ("<!--more-articles--><nav class=\"more-articles\" aria-label=\"" + ("ফার্মা ব্লগ থেকে আরও পড়ুন" if bn else "More from the Pharma Blog") + f"\" lang=\"{lang}\"><h2>"
            + ("ফার্মা ব্লগ থেকে আরও পড়ুন" if bn else "More from the Pharma Blog") + "</h2><ul>"
            + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in d["related"][:3]) + "</ul></nav><!--/more-articles--></main>")
    foot = ('<footer><div class="wrap"><p>© 2026 Sayedul Abrar. All rights reserved.</p><p><a href="/blog/">Pharma Blog</a> · <a href="/about/">About</a></p></div></footer>'
            '<script src="/assets/site.js?v=stable-nav-20261120" defer></script><script src="/assets/site-polish.js" defer></script><script src="/assets/blog-related.js?v=ae8-20261117" defer></script></body></html>')
    out = ROOT / "blog" / slug / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + nav + body + more + foot, encoding="utf-8")
    print(out.relative_to(ROOT), len(d["description"]), "chars desc")

for lang in ("en", "bn"):
    build(lang)
