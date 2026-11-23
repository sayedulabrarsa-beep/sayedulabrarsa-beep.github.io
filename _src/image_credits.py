#!/usr/bin/env python3
"""Adds Google image-metadata (ImageObject JSON-LD: creator, creditText, copyrightNotice, license, acquireLicensePage)
for Sayedul Abrar's own images on every indexable page, in one <script id="image-credits"> block per page.
- Covers article graphics (/assets/img/blog/) and his personal photos (Mirinja Valley, Chapainawabganj, personal moments).
- Images that show him also get "about" -> the site's Person entity, so image search links them to his profile.
- Skips company logos, product pack photos and other third-party images, Learning/Portfolio pages and noindex pages,
  and images already described with copyrightNotice in the page's own schema.
Re-runnable: the block is replaced each time. The release workflows run it after every article change."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
PERSON = {"@id": SITE + "/#person"}
OWN = re.compile(r"^/assets/img/(blog/|mirinja-valley/|chapainawabganj/|personal-moments/)")
SKIP = re.compile(r"(logo|favicon|badge|/icons/|-w\d+\.)", re.I)
NAME = re.compile(r"(Sayedul Abrar|সাইয়্যেদুল আবরার|সাইদুল আব্রার|সাইয়েদুল আবরার)")
BLOCK = re.compile(r'<script type="application/ld\+json" id="image-credits">.*?</script>', re.S)
changed = total = 0
for p in sorted(R.glob("**/index.html")):
    rel = p.relative_to(R).as_posix()
    if rel.startswith(("_src/", "learning/", "portfolio/", "node_modules/")):
        continue
    s = p.read_text(encoding="utf-8")
    if re.search(r'name="robots" content="[^"]*noindex', s) or 'http-equiv="refresh"' in s:
        continue
    base = BLOCK.sub("", s)
    ld = " ".join(re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', base, re.S))
    items, seen = [], set()
    for tag in re.findall(r"<img\b[^>]*>", base):
        m = re.search(r'\ssrc="([^"]+)"', tag)
        if not m:
            continue
        u = m.group(1).split("?")[0]
        if not OWN.match(u) or SKIP.search(u) or u.endswith(".svg") or u in seen:
            continue
        if not (R / u.lstrip("/")).exists():
            continue
        if u in ld and "copyrightNotice" in ld:
            continue
        seen.add(u)
        alt = re.search(r'\salt="([^"]*)"', tag)
        alt = html.unescape(alt.group(1)).strip() if alt else ""
        o = {"@type": "ImageObject", "contentUrl": SITE + u, "url": SITE + u,
             "creator": {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"},
             "creditText": "Sayedul Abrar (sayedulabrar.site)",
             "copyrightNotice": "© 2026 Sayedul Abrar",
             "license": SITE + "/sayedul-abrar-logo/#copyright",
             "acquireLicensePage": SITE + "/contact/"}
        if alt:
            o["name"] = alt[:150]
            o["description"] = alt
        if NAME.search(alt) and not u.startswith("/assets/img/blog/"):
            o["about"] = PERSON
        items.append(o)
    new = base
    if items:
        block = '<script type="application/ld+json" id="image-credits">' + json.dumps(
            {"@context": "https://schema.org", "@graph": items}, ensure_ascii=False, separators=(",", ":")) + "</script>"
        new = base.replace("</head>", block + "</head>", 1)
        total += len(items)
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"image credits: {total} images on {changed} changed pages")
