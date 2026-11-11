#!/usr/bin/env python3
"""ProfilePage JSON-LD on /about/ and sitemap <lastmod> from each page's real last git commit date."""
import re, json, subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent.parent; B = "https://sayedulabrar.site"
p = R/"about/index.html"; s = p.read_text(encoding="utf-8")
if '"ProfilePage"' not in s:
    person = next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S) if json.loads(x).get("@type") == "Person")
    prof = {"@context": "https://schema.org", "@type": "ProfilePage", "@id": B+"/about/#profile", "url": B+"/about/", "name": "About Sayedul Abrar, pharmacist", "inLanguage": "en", "dateModified": "2026-11-11T00:00:00+06:00", "mainEntity": person}
    s = s.replace("</head>", '<script type="application/ld+json">' + json.dumps(prof, ensure_ascii=False) + "</script></head>", 1); p.write_text(s, encoding="utf-8"); print("profilepage added")
def last(path):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)], cwd=R, capture_output=True, text=True).stdout.strip()
    return out or None
sm = R/"sitemap.xml"; x = sm.read_text(encoding="utf-8"); n = 0
def fix(m):
    global n
    loc = m.group(1); rel = loc.replace(B, "").strip("/")
    f = R/(rel+"/index.html" if rel else "index.html")
    if not f.exists(): f = R/rel
    d = last(f.relative_to(R)) if f.exists() and f.is_file() else None
    if d and d != m.group(2): n += 1; return m.group(0).replace(m.group(2), d)
    return m.group(0)
x = re.sub(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", fix, x); sm.write_text(x, encoding="utf-8"); print("lastmod updated", n)
