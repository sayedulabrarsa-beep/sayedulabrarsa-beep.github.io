#!/usr/bin/env python3
"""Regenerates machine-readable discovery files from the articles under /blog:
   - blog/feed.xml       RSS 2.0 feed of every article (English and Bangla)
   - llms.txt            the block between <!--articles:start--> and <!--articles:end-->
   - blog/index.html     the Blog JSON-LD block (id="blog-jsonld") listing every article
Safe to run repeatedly; the GitHub Action runs it on every push to blog/**."""
import json, re, pathlib, html
from email.utils import format_datetime
from datetime import datetime, timezone
R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
PERSON = SITE + "/#person"


def meta(s, attr, name):
    m = re.search(r'<meta\s+%s="%s"\s+content="([^"]*)"' % (attr, re.escape(name)), s)
    return html.unescape(m.group(1)) if m else ""


def articles():
    out = []
    for p in sorted((R / "blog").glob("*/index.html")):
        s = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in s or "noindex" in s[:3000]:
            continue
        slug = p.parent.name
        url = f"{SITE}/blog/{slug}/"
        title = meta(s, "property", "og:title") or re.sub(r"\s*\|.*$", "", re.search(r"<title>(.*?)</title>", s, re.S).group(1))
        title = re.sub(r"\s*\|\s*Sayedul Abrar\s*$", "", html.unescape(title)).strip()
        desc = meta(s, "name", "description")
        img = meta(s, "property", "og:image")
        lang = re.search(r'<html[^>]*lang="([^"]+)"', s).group(1)
        pub = mod = None
        for b in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            try:
                j = json.loads(b)
            except Exception:
                continue
            for x in (j.get("@graph", [j]) if isinstance(j, dict) else j):
                if isinstance(x, dict) and x.get("datePublished"):
                    pub = pub or x["datePublished"]; mod = mod or x.get("dateModified")
        if not pub:
            t = re.search(r'<time[^>]*datetime="([^"]+)"', s)
            pub = t.group(1) if t else "2026-01-01"
        out.append(dict(slug=slug, url=url, title=title, desc=desc, img=img, lang=lang, pub=pub[:10], mod=(mod or pub)[:10]))
    out.sort(key=lambda a: (a["pub"], a["slug"]), reverse=True)
    return out


def rfc822(d):
    return format_datetime(datetime.strptime(d, "%Y-%m-%d").replace(hour=6, tzinfo=timezone.utc))


def write_feed(arts):
    e = html.escape
    items = []
    for a in arts:
        f = R / a["img"].replace(SITE + "/", "") if a["img"].startswith(SITE + "/") else None
        size = f.stat().st_size if f and f.exists() else 0
        kind = "webp" if a["img"].endswith(".webp") else "png" if a["img"].endswith(".png") else "jpeg"
        enc = f'\n      <enclosure url="{e(a["img"])}" type="image/{kind}" length="{size}"/>' if size else ""
        items.append(f"""    <item>
      <title>{e(a['title'])}</title>
      <link>{a['url']}</link>
      <guid isPermaLink="true">{a['url']}</guid>
      <pubDate>{rfc822(a['pub'])}</pubDate>
      <dc:creator>Sayedul Abrar</dc:creator>
      <dc:language>{e(a['lang'])}</dc:language>
      <description>{e(a['desc'])}</description>{enc}
    </item>""")
    last = max(a["mod"] for a in arts)
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Pharma Blog | Sayedul Abrar</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Pharmacist-written educational articles in English and Bangla on medicines, pharmacology and the pharmaceutical industry in Bangladesh, by Sayedul Abrar.</description>
    <language>en</language>
    <lastBuildDate>{rfc822(last)}</lastBuildDate>
    <image><url>{SITE}/assets/img/og-image.png</url><title>Pharma Blog | Sayedul Abrar</title><link>{SITE}/blog/</link></image>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (R / "blog" / "feed.xml").write_text(feed, encoding="utf-8")


def write_llms(arts):
    p = R / "llms.txt"; s = p.read_text(encoding="utf-8")
    lines = ["<!--articles:start-->", "Pharma Blog articles (newest first; each is educational, not medical advice):"]
    for a in arts:
        tag = "বাংলা" if a["lang"].startswith("bn") else "English"
        lines.append(f"- {a['title']} — {tag} ({a['pub']}): {a['url']}")
        if a["desc"]:
            lines.append(f"  Summary: {a['desc']}")
    lines.append("Feed: " + SITE + "/blog/feed.xml")
    lines.append("<!--articles:end-->")
    block = "\n".join(lines)
    if "<!--articles:start-->" in s:
        s = re.sub(r"<!--articles:start-->.*?<!--articles:end-->", lambda m: block, s, flags=re.S)
    else:
        s = s.rstrip() + "\n\n" + block + "\n"
    p.write_text(s, encoding="utf-8")


def write_blog_jsonld(arts):
    p = R / "blog" / "index.html"; s = p.read_text(encoding="utf-8")
    data = {
        "@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog",
        "url": SITE + "/blog/", "name": "Pharma Blog by Sayedul Abrar", "inLanguage": ["en", "bn"],
        "author": {"@id": PERSON}, "publisher": {"@id": PERSON},
        "isPartOf": {"@id": SITE + "/#website"},
        "blogPost": [{"@type": "BlogPosting", "@id": a["url"] + "#article", "headline": a["title"][:110], "url": a["url"],
                      "datePublished": a["pub"], "dateModified": a["mod"], "inLanguage": a["lang"],
                      "image": a["img"], "author": {"@type": "Person", "@id": PERSON, "name": "Sayedul Abrar", "url": SITE + "/about/"}} for a in arts],
    }
    tag = '<script type="application/ld+json" id="blog-jsonld">' + json.dumps(data, ensure_ascii=False) + "</script>"
    if 'id="blog-jsonld"' in s:
        s = re.sub(r'<script type="application/ld\+json" id="blog-jsonld">.*?</script>', lambda m: tag, s, flags=re.S)
    else:
        s = s.replace("</head>", tag + "\n</head>", 1)
    p.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    a = articles()
    write_feed(a); write_llms(a); write_blog_jsonld(a)
    print("articles:", len(a))
