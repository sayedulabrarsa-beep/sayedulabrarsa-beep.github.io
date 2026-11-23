#!/usr/bin/env python3
"""Adds every content image of each indexable page to sitemap.xml as <image:image> entries (with the alt text as title).
Keeps existing entries, never removes anything, and skips logos, favicons, the author photo and srcset copies (-w750 etc.).
On the homepage it only adds images that are not article images, so article covers stay listed under their own article.
Safe to re-run; the GitHub workflows run it after every article change."""
import re, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
SKIP = re.compile(r"(logo|favicon|icon-|badge|/icons/|-w\d+\.|\.svg$)", re.I)
path = R / "sitemap.xml"
sm = path.read_text(encoding="utf-8")
added = pages = 0

def page_file(url):
    rel = url[len(SITE):].strip("/")
    f = R / rel / "index.html" if rel else R / "index.html"
    return f if f.exists() else None

def fix(m):
    global added, pages
    block = m.group(0)
    loc = re.search(r"<loc>([^<]+)</loc>", block).group(1)
    f = page_file(loc)
    if not f:
        return block
    s = f.read_text(encoding="utf-8")
    if 'name="robots" content="noindex' in s or 'http-equiv="refresh"' in s:
        return block
    have = set(re.findall(r"<image:loc>([^<]+)</image:loc>", block))
    new = []
    for tag in re.findall(r"<img\b[^>]*>", s):
        src = re.search(r'\ssrc="([^"]+)"', tag)
        if not src:
            continue
        u = src.group(1).split("?")[0]
        if not u.startswith("/assets/img/") or SKIP.search(u) or u.endswith("sayedul-abrar.jpg"):
            continue
        if loc == SITE + "/" and u.startswith("/assets/img/blog/"):
            continue
        full = SITE + u
        if full in have or not (R / u.lstrip("/")).exists():
            continue
        have.add(full)
        alt = re.search(r'\salt="([^"]*)"', tag)
        title = html.unescape(alt.group(1)).strip() if alt else ""
        new.append(f"<image:image><image:loc>{html.escape(full, quote=False)}</image:loc>" + (f"<image:title>{html.escape(title, quote=False)}</image:title>" if title else "") + "</image:image>")
    if not new:
        return block
    added += len(new); pages += 1
    return block.replace("</url>", "".join(new) + "</url>", 1)

sm = re.sub(r"<url>.*?</url>", fix, sm, flags=re.S)
path.write_text(sm, encoding="utf-8")
print(f"sitemap images: added {added} image entries on {pages} pages")
