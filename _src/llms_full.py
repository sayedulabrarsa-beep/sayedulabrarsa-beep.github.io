#!/usr/bin/env python3
"""Writes /llms-full.txt: plain-text copy of the profile and every Pharma Blog article, for AI assistants.
Run from anywhere: python3 _src/llms_full.py"""
import re, html, pathlib, json
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://sayedulabrar.site"
def text(fragment):
    f = re.sub(r"<(script|style|nav|figure|svg)\b.*?</\1>", " ", fragment, flags=re.S)
    f = re.sub(r"<h([1-3])[^>]*>", lambda m: "\n\n" + "#" * (int(m.group(1)) + 1) + " ", f)
    f = re.sub(r"</h[1-3]>", "\n", f)
    f = re.sub(r"<li[^>]*>", "\n- ", f)
    f = re.sub(r"<(p|div|tr|details|summary|section|br)[^>]*>", "\n", f)
    f = re.sub(r"<t[dh][^>]*>", " | ", f)
    f = html.unescape(re.sub(r"<[^>]+>", "", f))
    f = re.sub(r"[ \t]+", " ", f)
    f = re.sub(r"\n\s*\n\s*\n+", "\n\n", f)
    return "\n".join(l.strip() for l in f.splitlines()).strip()
def meta(s, name):
    m = re.search(r'<meta (?:name|property)="%s" content="([^"]*)"' % re.escape(name), s)
    return html.unescape(m.group(1)) if m else ""
out = ["# Sayedul Abrar (সাইয়্যেদুল আবরার) — full text for AI assistants",
       f"Source: {B}/ · Short index: {B}/llms.txt",
       "Sayedul Abrar, also known as Abrar, is a pharmacist (A Grade Pharmacist, Bangladesh) and Product Executive in the Product Management Department of Opsonin Pharma Ltd., Dhaka, Bangladesh, and a Bachelor of Pharmacy graduate of Daffodil International University. He writes the Pharma Blog on sayedulabrar.site: pharmacist-written patient education in English and Bangla.",
       "This is an independent personal website, not an official site of any pharmaceutical company. Articles are general education, not personal medical advice.", ""]
about = (R / "about/index.html").read_text(encoding="utf-8")
m = re.search(r"<main\b.*?</main>", about, re.S)
out += ["## About Sayedul Abrar", f"URL: {B}/about/", text(m.group(0)) if m else "", ""]
arts = []
for p in sorted((R / "blog").glob("*/index.html")):
    s = p.read_text(encoding="utf-8")
    if "<article" not in s or 'content="noindex' in s: continue
    d = re.search(r'article:published_time" content="([^"]+)"', s)
    arts.append((d.group(1) if d else "", p.parent.name, s))
arts.sort(key=lambda a: (a[0], a[1]), reverse=True)
out.append("## Pharma Blog articles (newest first)\n")
for date, slug, s in arts:
    t = re.sub(r"\s*\|\s*Sayedul Abrar\s*$", "", html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1))).strip()
    lang = "Bangla" if slug.endswith("-bangla") else "English"
    a = re.search(r"<article\b.*?</article>", s, re.S)
    body = text(a.group(0)) if a else ""
    body = re.split(r"\n#+ (?:Sayedul Abrar|Continue learning|আরও পড়ুন)\n", body)[0]
    out += [f"### {t}", f"URL: {B}/blog/{slug}/ · Language: {lang} · Published: {date} · Author: Sayedul Abrar, pharmacist",
            f"Summary: {meta(s, 'description')}", "", body, "", "---", ""]
(R / "llms-full.txt").write_text("\n".join(out), encoding="utf-8")
print("llms-full.txt", len(arts), "articles", (R / "llms-full.txt").stat().st_size, "bytes")
