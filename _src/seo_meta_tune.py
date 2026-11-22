#!/usr/bin/env python3
"""One-off, re-runnable: tune <title>/meta description (+og/twitter copies) for pages with high
impressions and low CTR in Search Console (export of 22 Nov 2026). Safe to re-run (no-op once applied)."""
import re, html, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
SUF = " | Sayedul Abrar"
T = {
 "blog/expiry-date-vs-manufacturing-date-medicine": (
   "Expiry Date vs Manufacturing Date: What EXP & MFG Mean",
   "What EXP and MFG mean on a medicine pack: how to read EXP 07/2027 (good to the end of that month), the batch number, opened-medicine limits and storage."),
 "blog/expiry-date-vs-manufacturing-date-medicine-bangla": (
   "মেয়াদ শেষ হওয়ার তারিখ (EXP) ও উৎপাদনের তারিখ (MFG) দেখার নিয়ম"+SUF,
   "ঔষধ বা ওষুধের মেয়াদ শেষ হওয়ার তারিখ (EXP) ও উৎপাদনের তারিখ (MFG) কীভাবে দেখবেন? 07/2027 মানে কী, ব্যাচ নম্বর ও সংরক্ষণের নিয়ম।"),
 "blog/drug-vs-medicine-bangla": (
   "ড্রাগ ও মেডিসিনের পার্থক্য কী? ওষুধ আর ড্রাগ কি একই?"+SUF,
   "ড্রাগ আর মেডিসিন (ওষুধ) কি একই জিনিস? সহজ গল্প, উদাহরণ, তুলনামূলক টেবিল ও সাধারণ প্রশ্নের মাধ্যমে Drug vs Medicine-এর পার্থক্য জানুন।"),
 "blog/drug-vs-medicine": (
   "Drug vs Medicine: Meaning, Differences & Examples"+SUF, None),
 "blog/generic-name-vs-brand-name-bangla": (
   "জেনেরিক নাম কী? জেনেরিক ও ব্র্যান্ড নামের পার্থক্য"+SUF,
   "জেনেরিক নাম ও ব্র্যান্ড নামের পার্থক্য কী? ওষুধের জেনেরিক নাম চেনার উপায়, নাপা-প্যারাসিটামল উদাহরণ ও লেবেল পড়ার নিয়ম জানুন।"),
 "blog/generic-name-vs-brand-name": (
   None,
   "Generic name vs brand name of medicine: find the active ingredient, why Finix and Rabe share one, what MUPS means, and a 4-step label check."),
 "blog/how-to-take-iron-tablets-properly": (
   "How to Take Iron Tablets: Before or After Food?"+SUF,
   "Iron tablets: before or after food? Best timing, vitamin C, tea, coffee, dairy and calcium gaps, interactions and missed doses, with NHS and NIH sources."),
 "brands/finix-mups": (None,
   "Finix MUPS 20 mg (rabeprazole sodium MUPS tablet, Opsonin Pharma): uses, how to take it, what MUPS means and FAQs in English and Bangla."),
 "brands/finix": (None,
   "Finix 20 mg (rabeprazole sodium, Opsonin Pharma): uses, how and when to take it, side effects, interactions and FAQs in English and Bangla."),
 "brands/finix-hp": (None,
   "Finix HP (rabeprazole, amoxicillin, clarithromycin; Opsonin Pharma): pack contents, course length, side effects, penicillin allergy and FAQs."),
 "brands/malifa": (None,
   "Malifa 30 mg capsule (ferric maltol, Navana Pharmaceuticals): uses, dose, food and PPI interactions, side effects and FAQs in English and Bangla."),
}
E = lambda s: html.escape(s, quote=True).replace("&#x27;", "'")
def sub_attr(s, prop_re, old, new):
    # replace content="old" in any meta tag whose name/property matches prop_re
    def f(m):
        tag = m.group(0)
        if re.search(prop_re, tag) and ('content="%s"' % old) in tag:
            return tag.replace('content="%s"' % old, 'content="%s"' % new)
        return tag
    return re.sub(r'<meta\b[^>]*>', f, s)
n = 0
for page, (nt, nd) in T.items():
    p = R / page / "index.html"
    s0 = s = p.read_text(encoding="utf8")
    if nt:
        old = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
        new = E(nt).replace("&amp;amp;", "&amp;")
        if old != new:
            s = s.replace("<title>%s</title>" % old, "<title>%s</title>" % new, 1)
            s = sub_attr(s, r'og:title|twitter:title', old, new)
    if nd:
        old = re.search(r'<meta name="description" content="(.*?)"', s).group(1)
        new = E(nd)
        if old != new:
            s = s.replace('<meta name="description" content="%s"' % old, '<meta name="description" content="%s"' % new, 1)
            s = sub_attr(s, r'og:description|twitter:description', old, new)
    if s != s0:
        p.write_text(s, encoding="utf8"); n += 1
        t = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
        d = re.search(r'<meta name="description" content="(.*?)"', s).group(1)
        print("%-62s title %3d  desc %3d" % (page, len(html.unescape(t)), len(html.unescape(d))))
print("pages changed:", n)
