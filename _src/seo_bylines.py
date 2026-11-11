#!/usr/bin/env python3
"""Adds a visible byline (author link + dates) to articles that lack one. Idempotent."""
import re, pathlib, datetime
R = pathlib.Path(__file__).resolve().parent.parent
SL = ["expiry-date-vs-manufacturing-date-medicine","generic-name-vs-brand-name","glucosamine-alzheimers-nature-metabolism-study","heartburn-vs-acid-reflux-vs-gerd","what-is-the-pharmaceutical-industry"]
BD = str.maketrans("0123456789","০১২৩৪৫৬৭৮৯")
BM = ["জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন","জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"]
def en(d): d = datetime.date.fromisoformat(d); return f"{d.day} {d.strftime('%B %Y')}"
def bn(d): d = datetime.date.fromisoformat(d); return f"{d.day} {BM[d.month-1]} {d.year}".translate(BD)
CSS = '<style id="byline-css">.byline-seo{margin:14px 0 18px;font-size:13px;color:#52625d;line-height:1.6}.byline-seo a{color:#126b56;font-weight:700;text-decoration:none;border-bottom:1px solid #126b5655}.byline-seo time{white-space:nowrap}</style>'
for slug in SL:
    for suffix, lang in (("", "en"), ("-bangla", "bn")):
        p = R/"blog"/(slug+suffix)/"index.html"
        if not p.exists(): continue
        s = p.read_text(encoding="utf-8")
        if "byline-seo" in s: continue
        pub = re.search(r'datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)', s).group(1); mod = re.search(r'dateModified"\s*:\s*"(\d{4}-\d\d-\d\d)', s).group(1)
        if lang == "en":
            t = f'By <a href="/about/" rel="author">Sayedul Abrar</a>, pharmacist · Published <time datetime="{pub}">{en(pub)}</time>' + (f' · Updated <time datetime="{mod}">{en(mod)}</time>' if mod != pub else "")
        else:
            t = f'লেখক: <a href="/about/" rel="author">সায়েদুল আবরার</a>, ফার্মাসিস্ট · প্রকাশ: <time datetime="{pub}">{bn(pub)}</time>' + (f' · হালনাগাদ: <time datetime="{mod}">{bn(mod)}</time>' if mod != pub else "")
        a = s.index("<article"); f = s.index("</figure>", a) + len("</figure>")
        s = s[:f] + f'<p class="byline-seo">{t}</p>' + s[f:]
        s = s.replace("</head>", CSS + "</head>", 1)
        p.write_text(s, encoding="utf-8"); print("byline", p.parent.name)
