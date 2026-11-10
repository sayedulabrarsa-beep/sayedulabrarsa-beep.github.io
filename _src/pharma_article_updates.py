#!/usr/bin/env python3
"""One-time content/SEO improvements for the pharma-industry article pair (idempotent via marker)."""
import re, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent; BASE = "https://sayedulabrar.site"
EN = dict(slug="what-is-the-pharmaceutical-industry", faq_n=10,
 bd_old="methodology in mind.</p>", bd_new=" The same profile also refers to 213 active companies and puts annual API imports at about USD 1.3 billion; like the other figures, these carry no year on the page.</p>",
 br_old="evidence and correct use matter.</p>", br_new=' To go deeper, read my article on <a href="/blog/generic-name-vs-brand-name/">generic name vs brand name</a>.</p>',
 faqs=[("11. How much of Bangladesh's medicine demand is met by local manufacturers?", "According to the BIDA sector profile, local manufacturers meet about 98% of the country's medicine demand. The page gives no year or methodology, so treat it as a profile figure rather than a live statistic."),
  ("12. Does Bangladesh make its own APIs?", "Only a small share. BIDA's profile says Bangladesh imports over 85% of its API needs, and it describes a 200-acre BSCIC API Park at Munshiganj as helping to build domestic API production. Making finished tablets locally is different from making the API locally."),
  ("13. What is a branded-generic medicine?", 'A medicine sold under a company-selected brand name whose active ingredient is a well-known generic substance, such as paracetamol. The brand identifies the product and the generic name identifies the ingredient. See <a href="/blog/generic-name-vs-brand-name/">Generic Name vs Brand Name</a>.')],
 card='<a class="related-card" href="/blog/when-to-take-ppi-before-meals/"><strong>When to Take a PPI</strong><span>A practical example of reading a medicine label and leaflet.</span></a>')
BN = dict(slug="what-is-the-pharmaceutical-industry-bangla", faq_n=10,
 bd_old="পদ্ধতি বিবেচনা করে বুঝতে হবে।</p>", bd_new=" একই প্রোফাইলে ২১৩টি সক্রিয় কোম্পানির কথা এবং বছরে প্রায় ১.৩ বিলিয়ন মার্কিন ডলারের API আমদানির কথা আছে; অন্য সংখ্যাগুলোর মতো এগুলোর সালও পেজে দেওয়া নেই।</p>",
 br_old="মান ও প্রমাণ গুরুত্বপূর্ণ।</p>", br_new=' আরও জানতে পড়ুন <a href="/blog/generic-name-vs-brand-name/">জেনেরিক নাম ও ব্র্যান্ড নামের পার্থক্য</a> লেখাটি।</p>',
 faqs=[("১১. বাংলাদেশের ওষুধের চাহিদার কত অংশ স্থানীয় উৎপাদকরা পূরণ করে?", "BIDA-এর সেক্টর প্রোফাইল অনুযায়ী দেশের ওষুধের চাহিদার প্রায় ৯৮% স্থানীয় উৎপাদকরা পূরণ করে। পেজে কোনো সাল বা পদ্ধতি দেওয়া নেই, তাই এটিকে লাইভ পরিসংখ্যান না ভেবে প্রোফাইলের তথ্য হিসেবে দেখুন।"),
  ("১২. বাংলাদেশ কি নিজের API নিজে তৈরি করে?", "অল্প অংশ। BIDA-এর প্রোফাইল বলছে প্রয়োজনীয় API-এর ৮৫%-এর বেশি আমদানি করতে হয়, আর মুন্সীগঞ্জে BSCIC-র ২০০ একরের API পার্ক দেশীয় API উৎপাদন গড়ে তুলতে সাহায্য করছে বলে বর্ণনা আছে। দেশে ট্যাবলেট তৈরি করা আর দেশে API তৈরি করা এক নয়।"),
  ("১৩. ব্র্যান্ডেড-জেনেরিক ওষুধ কী?", 'কোম্পানির দেওয়া ব্র্যান্ড নামে বাজারজাত করা সেই ওষুধ, যার সক্রিয় উপাদান প্যারাসিটামলের মতো পরিচিত জেনেরিক উপাদান। ব্র্যান্ড নাম পণ্যকে চেনায়, জেনেরিক নাম উপাদানকে। দেখুন <a href="/blog/generic-name-vs-brand-name/">জেনেরিক নাম ও ব্র্যান্ড নামের পার্থক্য</a>।')],
 card='<a class="related-card" href="/blog/when-to-take-ppi-before-meals/#bn"><strong>When to Take a PPI</strong><span>ওষুধের লেবেল ও লিফলেট পড়ার একটি বাস্তব উদাহরণ।</span></a>')
def run(c):
    p = ROOT/f"blog/{c['slug']}/index.html"; s = p.read_text(encoding="utf-8")
    if "<!--upd1-->" in s: return "skip"
    for a, b in ((c["bd_old"], c["bd_new"]), (c["br_old"], c["br_new"])):
        assert s.count(a) == 1, a; s = s.replace(a, a[:-4] + b)
    add = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>\n" for q, a in c["faqs"])
    i = s.index('id="faq"'); j = s.index("</section>", i); s = s[:j] + add + s[j:]
    k = s.index('<a class="related-card" href="/blog/expiry-date'); s = s[:k] + c["card"] + s[k:]
    # FAQPage JSON-LD from page details
    sec = s[s.index('id="faq"'):s.index("</section>", s.index('id="faq"'))]
    qa = [{"@type": "Question", "name": re.sub(r"^[0-9০-৯]+[.।]\s*", "", html.unescape(re.sub(r"<[^>]+>", "", q))).strip(),
           "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a)).strip()}} for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", sec, re.S)]
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "bn" if "bangla" in c["slug"] else "en", "mainEntity": qa}
    s = s.replace("</head>", '<!--upd1--><script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + "</script></head>", 1)
    p.write_text(s, encoding="utf-8"); return len(qa)
print(run(EN), run(BN))
