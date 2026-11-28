#!/usr/bin/env python3
"""Upgrade the 30 Nov - 5 Dec calendar pages (already on main, text approved by the user in PRs #27, #34, #35)
with their own cover, 2 code-drawn diagrams, a key-takeaways picture, 1200x630 share image, BreadcrumbList,
ImageObject list, series navigation and related reading. Text is left as it is, except the Bangla H2 headings
(English words replaced with Bangla, English kept in brackets) and over-long descriptions.
Usage: python3 _src/nextweek/upgrade.py <key>   (dosage | release | paracetamol | routes). Pages stay noindex."""
import sys, re, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from nw_pages import ARTICLES
SITE = "https://sayedulabrar.site"
E = lambda s: html.escape(s, quote=True)
BND = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
V = "nw-20261128"

def fig(src, alt, cap, n, bn, cover=False):
    if cover:
        return (f'<figure class="hero-visual"><a href="{src}?v={V}" target="_blank" rel="noopener"><img src="{src}?v={V}" alt="{E(alt)}" width="1600" height="900" fetchpriority="high" decoding="async"></a>'
                f'<figcaption class="caption">{cap}</figcaption></figure>')
    return (f'<figure class="article-figure"><a href="{src}?v={V}" target="_blank" rel="noopener"><img src="{src}?v={V}" alt="{E(alt)}" width="1600" height="900" loading="lazy" decoding="async"></a>'
            f'<figcaption>{"চিত্র" if bn else "Figure"} {str(n).translate(BND) if bn else n} · {cap}</figcaption></figure>')

def run(key):
    A = ARTICLES[key]
    for lang in ("en", "bn"):
        bn = lang == "bn"
        L = A[lang]
        slug = A["slug"] + ("-bangla" if bn else "")
        p = ROOT / "blog" / slug / "index.html"
        t = p.read_text(encoding="utf-8")
        url = f"{SITE}/blog/{slug}/"
        img = lambda n: f"/assets/img/blog/{A['dir']}/{n}{'-bn' if bn else ''}.webp"
        social = f"{SITE}/assets/img/blog/{A['dir']}/{A['prefix']}-social-{lang}.jpg"

        # 1. cover: replace the borrowed hero figure
        t, k = re.subn(r'<figure class="hero-visual">.*?</figure>', lambda m: fig(img(A["cover"]), L["cover_alt"], L["cover_cap"], 0, bn, True), t, count=1, flags=re.S)
        if k == 0:  # no hero figure yet: place the cover after the language switch (or at the top of the article)
            m = re.search(r'<nav class="lang-switch".*?</nav>', t, re.S) or re.search(r'<article class="article-content">', t)
            t = t[:m.end()] + fig(img(A["cover"]), L["cover_alt"], L["cover_cap"], 0, bn, True) + t[m.end():]
        # 2. section figures: insert before the H2 that follows section n
        art_start = t.find('<article class="article-content">')
        objs = [(img(A["cover"]), L["cover_alt"], L["cover_cap"])]
        n = 0
        for name, after, (alt, cap) in zip(A["figs"], L["at"], L["figs"]):
            n += 1
            h2s = [m for m in re.finditer(r'<h2[ >]', t) if m.start() > art_start]
            pos = h2s[after].start()  # h2s[after] is the heading after section number `after`
            t = t[:pos] + fig(img(name), alt, cap, n, bn) + t[pos:]
            objs.append((img(name), alt, cap))
        # 3. description
        if L.get("description"):
            assert len(L["description"]) <= 160, (key, lang, len(L["description"]))
            for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
                t = re.sub(pat, lambda m: m.group(1) + E(L["description"]) + m.group(2), t, count=1)
        d = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
        assert len(html.unescape(d)) <= 160, (key, lang, len(html.unescape(d)))
        # 4. Bangla headings
        for old, new in L.get("h2", []):
            assert old in t, (key, lang, old)
            t = t.replace(f">{old}</h2>", f">{new}</h2>").replace(f">{old}</a>", f">{new}</a>")
        # 5. share image + alt
        for prop in ("og:image", "og:image:secure_url"):
            if f'property="{prop}"' in t:
                t = re.sub(rf'(<meta property="{prop}" content=")[^"]*(")', lambda m: m.group(1) + social + m.group(2), t, count=1)
        if 'og:image:secure_url' not in t:
            t = t.replace('<meta property="og:image" ', f'<meta property="og:image:secure_url" content="{social}"><meta property="og:image" ', 1)
        t = re.sub(r'<meta property="og:image:(type|width|height)" content="[^"]*">', "", t)
        t = t.replace('<meta property="og:image" ', '<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image" ', 1)
        t = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', lambda m: m.group(1) + social + m.group(2), t, count=1)
        t = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', lambda m: m.group(1) + E(L["cover_alt"]) + m.group(2), t, count=1)
        if 'name="twitter:image:alt"' in t:
            t = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*(")', lambda m: m.group(1) + E(L["cover_alt"]) + m.group(2), t, count=1)
        else:
            t = t.replace('<meta name="twitter:image" ', f'<meta name="twitter:image:alt" content="{E(L["cover_alt"])}"><meta name="twitter:image" ', 1)
        # 6. BlogPosting image list + BreadcrumbList
        image_objects = [social] + [{"@type": "ImageObject", "contentUrl": SITE + u, "url": SITE + u, "name": cap, "caption": cap, "description": alt,
                                     "width": 1600, "height": 900, "inLanguage": "bn-BD" if bn else "en-BD", "encodingFormat": "image/webp",
                                     "creator": {"@type": "Person", "name": "Sayedul Abrar", "url": f"{SITE}/about/"},
                                     "creditText": "Sayedul Abrar", "copyrightNotice": "© 2026 Sayedul Abrar"} for u, alt, cap in objs]
        def fix_ld(m):
            o = json.loads(m.group(1))
            if o.get("@type") == "BlogPosting":
                o["image"] = image_objects
                o["thumbnailUrl"] = social
            return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"
        t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, t, flags=re.S)
        if '"BreadcrumbList"' not in t:
            h1 = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1))).strip()
            crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Pharma Blog", "item": f"{SITE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
            t = t.replace("</head>", '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False, separators=(",", ":")) + "</script></head>", 1)
        # 7. figure CSS (same rules as the kinetics builder)
        if 'id="fig-fit"' not in t:
            t = t.replace("</head>", '<style id="fig-fit">.article-figure{margin:28px 0}.article-figure a{display:block}.article-figure img,.hero-visual img{display:block;width:100%;height:auto;border-radius:14px}.article-figure figcaption{font-size:14px;color:#526D82;margin-top:8px}'
                          '.article-content .series-nav{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:30px 0}.article-content .series-nav a{display:block;border:1px solid #d6e2df;border-radius:14px;padding:14px 16px;text-decoration:none;background:#fbfdfc}.article-content .series-nav small{display:block;color:#526D82;font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:.78em}.article-content .series-nav b{display:block;color:#174F52;line-height:1.35;margin-top:4px}.article-content .series-nav .next{text-align:right}.article-content .series-hub{grid-column:1/-1;text-align:center}@media(max-width:600px){.article-content .series-nav{grid-template-columns:1fr}.article-content .series-nav .next{text-align:left}}</style></head>', 1)
        # 8. series nav + related reading, placed before the References heading
        ref_h = re.search(r'<h2[^>]*>(References|তথ্যসূত্র)[^<]*</h2>', t)
        block = ""
        sn = L.get("series")
        if sn and "series-nav" not in t:
            block += '<nav class="series-nav" aria-label="' + ("সিরিজের অন্য লেখা" if bn else "More in this series") + '">'
            block += (f'<a class="prev" href="{sn["prev"][0]}"><small>{"আগের লেখা" if bn else "Previous in series"}</small><b>← {sn["prev"][1]}</b></a>' if sn.get("prev") else "<span></span>")
            if sn.get("next"):
                block += f'<a class="next" href="{sn["next"][0]}"><small>{"সিরিজের পরের লেখা" if bn else "Next in series"}</small><b>{sn["next"][1]} →</b></a>'
            if sn.get("hub"):
                block += f'<a class="series-hub" href="{sn["hub"][0]}"><small>{"পুরো সিরিজ" if bn else "Full series"}</small><b>{sn["hub"][1]}</b></a>'
            block += "</nav>"
        if L.get("related") and not re.search(r'<h2[^>]*>(Related reading|আরও পড়ুন)</h2>', t):
            block += f'<h2>{"আরও পড়ুন" if bn else "Related reading"}</h2><ul>' + "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in L["related"]) + "</ul>"
        if block:
            t = t[:ref_h.start()] + block + t[ref_h.start():]
        t = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,nofollow">', t, count=1)
        p.write_text(t, encoding="utf-8")
        print(p.relative_to(ROOT), "figures:", n + 1, "desc:", len(html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))))

if __name__ == "__main__":
    for k in sys.argv[1:]:
        run(k)
