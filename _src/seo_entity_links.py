#!/usr/bin/env python3
"""One-off/idempotent: link every article's author/publisher to the site Person entity (@id),
add isPartOf WebSite, add a BreadcrumbList where missing, add the RSS <link rel=alternate>,
and make the first article image the high-priority LCP image."""
import json, re, pathlib, html
R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"; PID = SITE + "/#person"
FEED = '<link rel="alternate" type="application/rss+xml" title="Pharma Blog | Sayedul Abrar" href="/blog/feed.xml">'
AUTH = {"@type": "Person", "@id": PID, "name": "Sayedul Abrar", "url": SITE + "/about/"}
n = 0
for p in sorted(list((R/"blog").glob("*/index.html")) + list((R/"vlog").glob("*/index.html"))):
    s = p.read_text(encoding="utf-8"); o = s
    sec = p.parent.parent.name; slug = p.parent.name; url = f"{SITE}/{sec}/{slug}/"
    has_bc = '"BreadcrumbList"' in s
    def fix(m):
        try: j = json.loads(m.group(2))
        except Exception: return m.group(0)
        if not isinstance(j, dict) or j.get("@type") not in ("Article", "BlogPosting"): return m.group(0)
        j["author"] = AUTH; j["publisher"] = {"@type": "Person", "@id": PID, "name": "Sayedul Abrar", "url": SITE + "/"}
        j["isPartOf"] = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Sayedul Abrar"}
        j.setdefault("@id", url + "#article")
        j.setdefault("mainEntityOfPage", {"@type": "WebPage", "@id": url})
        return m.group(1) + json.dumps(j, ensure_ascii=False) + m.group(3)
    s = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', fix, s, flags=re.S)
    if not has_bc:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        name = html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else slug
        hub = ("Pharma Blog", SITE + "/blog/") if sec == "blog" else ("Daily Vlog", SITE + "/vlog/")
        bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": hub[0], "item": hub[1]},
            {"@type": "ListItem", "position": 3, "name": name[:110], "item": url}]}
        s = s.replace("</head>", '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + "</script>\n</head>", 1)
    if sec == "blog" and "application/rss+xml" not in s:
        s = s.replace("</head>", FEED + "\n</head>", 1)
    # first image inside the article = LCP candidate: load eagerly with high priority
    a = s.find("<article"); 
    if a > -1:
        m = re.compile(r"<img\b[^>]*>").search(s, a)
        if m:
            t = m.group(0); t2 = re.sub(r'\s+loading="lazy"', "", t)
            if "fetchpriority" not in t2: t2 = t2.replace("<img", '<img fetchpriority="high"', 1)
            s = s[:m.start()] + t2 + s[m.end():]
    if s != o: p.write_text(s, encoding="utf-8"); n += 1
# feed link on blog hub and homepage
for rel in ["blog/index.html", "index.html"]:
    p = R/rel; s = p.read_text(encoding="utf-8")
    if "application/rss+xml" not in s: p.write_text(s.replace("</head>", FEED + "\n</head>", 1), encoding="utf-8"); n += 1
print("pages changed", n)
