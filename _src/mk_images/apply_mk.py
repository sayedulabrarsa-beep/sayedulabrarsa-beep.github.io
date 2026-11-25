#!/usr/bin/env python3
"""Pharmaceutical Marketing Strategy (EN+BN): place the 10 pictures with legends, update head/schema, sitemap, feed, data files."""
import re, json, html, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/pharma-marketing-strategy/"; V = "?v=mk-20261125"
def esc(s): return html.escape(s, quote=True)
EN = {
 "cover": ("A teal glass staircase with a plain white medicine box and stethoscope on the steps and golden scales on top, in front of a Dhaka-style skyline at sunset.",
           "Pharmaceutical marketing strategy in Bangladesh: a practical framework with ethics at its centre.", None, []),
 "context": ("A golden compass and a teal relief map of Bangladesh on a desk, with a white capsule, notebook and pen.",
             "Sector-level indicators help with context; they do not replace a current category or brand audit.", "ul",
             [("Differences to respect", "therapeutic areas, care settings, geography, affordability, distribution and information needs"), ("Sector data", "useful context, not a substitute for a current category or brand-level audit"), ("Start with data", "current and clearly defined, not assumptions about every prescriber or patient")]),
 "research": ("A magnifying glass over a bar chart on a white board, with teal and coral map pins, a clipboard and a cup of tea on a desk.",
              "Build a fact base before choosing a campaign, and record the source, period and limits of each input.", "ul",
              [("Category", "value, volume, growth and seasonality on one consistent market definition"), ("Competition", "molecules, dosage forms, packs, approved claims and availability"), ("Care pathway", "clinical context and access barriers, without unnecessary patient data"), ("Internal readiness", "quality, regulatory status, supply, pricing and field capability"), ("External environment", "policy, guidelines and public-health priorities")]),
 "segmentation": ("Five glass cubes in teal, green, gold, coral and steel blue on a pharmacy counter, with shelves of plain white boxes and a stethoscope behind.",
                  "Illustrative segmentation dimensions. Use only relevant, lawful and necessary information.", "ul",
                  [("Therapeutic", "clinical need, treatment context, evidence gap"), ("Professional", "specialty or setting, information need, access preference"), ("Market", "geography, availability, affordability")]),
 "positioning": ("Papers, a teal folder and a stethoscope drop into a glass funnel that ends in a single glowing white capsule.",
                 "Evidence and a real healthcare need should come before the message.", "ol",
                 [("Product evidence", ""), ("Healthcare need", ""), ("Supportable value", ""), ("Approved message", "")]),
 "channels": ("A tablet, laptop and phone with blank screens are joined by glowing gold lines to a gold and teal compass, beside a notebook, pen and white capsule.",
              "A channel should serve the information need, not be chosen only because it is fashionable or easy to count.", "ul",
              [("Objectives", "a baseline, target, owner and time period for each"), ("Channels", "matched to information need, evidence type and applicable rules"), ("Quality", "evaluate reach and quality, not only impressions or activity volume")]),
 "plan": ("Five wooden figures stand in a glowing ring around a white capsule, in front of a blank desk calendar with teal and coral headers and stacks of sticky notes.",
          "Involve medical, regulatory, quality, sales, supply, finance and procurement teams early.", "ul",
          [("For every activity", "objective, audience, message, evidence, channel, owner, budget and timeline"), ("Involve early", "medical, regulatory, quality, sales, supply, finance and procurement"), ("Check readiness", "approvals, training, stock and a named owner")]),
 "scorecard": ("A glass panel with four dial gauges in teal, coral, gold and steel blue stands on a teal base, beside a stethoscope, capsule, clipboard with a ticked checklist and pen.",
               "Choose a small set of indicators that answer the strategy’s key questions.", "ul",
               [("Business", "growth, share, forecast"), ("Access", "availability, distribution"), ("Engagement", "reach, relevance, learning"), ("Quality and compliance", "approved claims, review")]),
 "ethics": ("A glass shield with a scales symbol stands on a bound stack of documents tied with a gold ribbon, beside a stethoscope and pen.",
            "Ethical promotion is part of strategy, not a final checklist.", "ul",
            [("Current, approved information", "use approved product information and materials"), ("No exaggeration", "do not overstate benefits, omit material risks or imply unsupported superiority"), ("Scientific exchange stays distinct", "from inducements or prescribing pressure"), ("Necessary data only", "collect only professional information that is needed")]),
 "mistakes": ("A coral tile with a cross and a teal tile with a tick stand behind a notebook with a ticked checklist, a stethoscope and a white capsule.",
              "Most strategic mistakes start with skipping the healthcare need or the evidence.", "ul",
              [("Campaign before need", "starting with an idea before defining the healthcare need"), ("Sales data without context", "market definition, period or denominator unchecked"), ("Activity is not engagement", "counting activities instead of meaningful professional engagement"), ("Claims beyond the evidence", "stronger than the evidence or approved product information")]),
}
BN = {
 "cover": ("সবুজ-নীল কাচের সিঁড়ির ধাপে একটি সাদা ওষুধের বাক্স ও স্টেথোস্কোপ, ওপরে সোনালি দাঁড়িপাল্লা; পেছনে সূর্যাস্তের আলোয় ঢাকার মতো শহরের আকাশরেখা।",
           "বাংলাদেশে ফার্মাসিউটিক্যাল মার্কেটিং কৌশল: নৈতিকতাকে কেন্দ্রে রেখে বাস্তবসম্মত কাঠামো।", None, []),
 "context": ("টেবিলে সোনালি কম্পাস ও বাংলাদেশের সবুজ-নীল ত্রিমাত্রিক মানচিত্র; পাশে একটি সাদা ক্যাপসুল, নোটবুক ও কলম।",
             "সেক্টর-পর্যায়ের সূচক প্রেক্ষাপট বোঝাতে সাহায্য করে; হালনাগাদ category বা brand audit-এর বিকল্প নয়।", "ul",
             [("যে পার্থক্য মাথায় রাখতে হবে", "থেরাপিউটিক ক্ষেত্র, চিকিৎসাসেবার পরিবেশ, ভৌগোলিক অবস্থান, সামর্থ্য, বিতরণ ও তথ্যের প্রয়োজন"), ("সেক্টর-তথ্য", "প্রেক্ষাপটের জন্য উপকারী, কিন্তু হালনাগাদ category বা brand audit-এর বিকল্প নয়"), ("তথ্য দিয়ে শুরু", "হালনাগাদ ও স্পষ্টভাবে সংজ্ঞায়িত; প্রতিটি চিকিৎসক বা রোগী কী চান তা ধরে নেওয়া নয়")]),
 "research": ("সাদা বোর্ডের বার চার্টের ওপর ম্যাগনিফাইং গ্লাস; টেবিলে সবুজ-নীল ও প্রবাল রঙের ম্যাপ পিন, ক্লিপবোর্ড ও এক কাপ চা।",
              "campaign বেছে নেওয়ার আগে তথ্যভিত্তি তৈরি করুন এবং প্রতিটি তথ্যের উৎস, সময়কাল ও সীমাবদ্ধতা লিখে রাখুন।", "ul",
              [("Category", "একই market definition ধরে value, volume, growth ও seasonality"), ("প্রতিযোগিতা", "molecule, dosage form, pack, অনুমোদিত claim ও প্রাপ্যতা"), ("Care pathway", "অপ্রয়োজনীয় রোগীর তথ্য ছাড়া ক্লিনিক্যাল প্রেক্ষাপট ও সেবা পাওয়ার বাধা"), ("অভ্যন্তরীণ প্রস্তুতি", "মান, নিয়ন্ত্রক অবস্থা, সরবরাহ, মূল্য ও field সক্ষমতা"), ("বাহ্যিক পরিবেশ", "নীতি, guideline ও জনস্বাস্থ্যের অগ্রাধিকার")]),
 "segmentation": ("ফার্মেসি কাউন্টারে সবুজ-নীল, সবুজ, সোনালি, প্রবাল ও ইস্পাত-নীল রঙের পাঁচটি কাচের ঘনক; পেছনে সাদা বাক্সের তাক ও স্টেথোস্কোপ।",
                  "Segmentation-এর উদাহরণ। শুধু প্রাসঙ্গিক, আইনসম্মত ও প্রয়োজনীয় তথ্য ব্যবহার করুন।", "ul",
                  [("থেরাপিউটিক", "ক্লিনিক্যাল প্রয়োজন, চিকিৎসার প্রেক্ষাপট, evidence gap"), ("পেশাগত", "বিশেষত্ব বা কর্মক্ষেত্র, তথ্যের প্রয়োজন, প্রাপ্তির পছন্দ"), ("বাজার", "ভৌগোলিক অবস্থান, প্রাপ্যতা, সামর্থ্য")]),
 "positioning": ("কাগজ, সবুজ-নীল ফোল্ডার ও স্টেথোস্কোপ একটি কাচের ফানেলে পড়ছে, নিচে একটি জ্বলজ্বলে সাদা ক্যাপসুল।",
                 "Message তৈরির আগে evidence এবং বাস্তব healthcare need নিশ্চিত করুন।", "ol",
                 [("পণ্যের evidence", ""), ("Healthcare need", ""), ("গ্রহণযোগ্য value", ""), ("অনুমোদিত message", "")]),
 "channels": ("ফাঁকা পর্দার ট্যাবলেট, ল্যাপটপ ও ফোন সোনালি রেখায় সোনালি-সবুজ কম্পাসের সঙ্গে যুক্ত; পাশে নোটবুক, কলম ও সাদা ক্যাপসুল।",
              "Channel যেন তথ্যের প্রয়োজন মেটায়; শুধু জনপ্রিয় বা গোনা সহজ বলে বাছাই করা ঠিক নয়।", "ul",
              [("লক্ষ্য", "প্রতিটির জন্য baseline, target, দায়িত্বপ্রাপ্ত ব্যক্তি ও সময়সীমা"), ("Channel", "তথ্যের প্রয়োজন, প্রমাণের ধরন ও প্রযোজ্য নিয়ম অনুযায়ী বাছাই"), ("মান", "শুধু impression বা কাজের সংখ্যা নয়, reach ও মানও মূল্যায়ন করুন")]),
 "plan": ("ফাঁকা ডেস্ক ক্যালেন্ডার ও রঙিন স্টিকি নোটের সামনে একটি সাদা ক্যাপসুল ঘিরে জ্বলজ্বলে বৃত্তে পাঁচটি কাঠের মানুষের মূর্তি।",
          "Medical, regulatory, quality, sales, supply, finance ও procurement দলকে আগেভাগে যুক্ত করুন।", "ul",
          [("প্রতিটি কার্যক্রমের জন্য", "লক্ষ্য, audience, message, evidence, channel, দায়িত্বশীল, বাজেট ও সময়সূচি"), ("আগেভাগে যুক্ত করুন", "medical, regulatory, quality, sales, supply, finance ও procurement"), ("প্রস্তুতি যাচাই", "অনুমোদন, প্রশিক্ষণ, মজুত ও নির্দিষ্ট দায়িত্বশীল")]),
 "scorecard": ("সবুজ-নীল ভিত্তির ওপর কাচের ফলকে সবুজ-নীল, প্রবাল, সোনালি ও ইস্পাত-নীল রঙের চারটি ডায়াল; সামনে স্টেথোস্কোপ, ক্যাপসুল, টিক-দেওয়া চেকলিস্টসহ ক্লিপবোর্ড ও কলম।",
               "কৌশলের গুরুত্বপূর্ণ প্রশ্নগুলোর উত্তর দেয়—এমন অল্প কয়েকটি সূচক বেছে নিন।", "ul",
               [("ব্যবসায়িক ফল", "প্রবৃদ্ধি, শেয়ার, পূর্বাভাস"), ("প্রাপ্যতা", "সহজলভ্যতা, বিতরণ"), ("সম্পৃক্ততা", "reach, প্রাসঙ্গিকতা, শেখা"), ("মান ও compliance", "অনুমোদিত claim, review")]),
 "ethics": ("সোনালি ফিতায় বাঁধা কাগজের স্তূপের ওপর দাঁড়িপাল্লা-চিহ্নসহ কাচের ঢাল; পাশে স্টেথোস্কোপ ও কলম।",
            "নৈতিক প্রচার কৌশলেরই অংশ, শেষে যোগ করা চেকলিস্ট নয়।", "ul",
            [("হালনাগাদ, অনুমোদিত তথ্য", "অনুমোদিত পণ্য-তথ্য ও উপকরণ ব্যবহার করুন"), ("অতিরঞ্জন নয়", "উপকার বাড়িয়ে বলা, গুরুত্বপূর্ণ ঝুঁকি বাদ দেওয়া বা অসমর্থিত শ্রেষ্ঠত্বের ইঙ্গিত দেওয়া যাবে না"), ("বৈজ্ঞানিক আলোচনা আলাদা", "প্রলোভন বা prescribing-এর চাপ থেকে"), ("শুধু প্রয়োজনীয় তথ্য", "যে পেশাগত তথ্য দরকার, কেবল সেটুকু সংগ্রহ করুন")]),
 "mistakes": ("সামনে চেকলিস্টসহ নোটবুক, স্টেথোস্কোপ ও সাদা ক্যাপসুল; পেছনে ক্রস-চিহ্নের প্রবাল টাইল ও টিক-চিহ্নের সবুজ-নীল টাইল।",
              "বেশিরভাগ কৌশলগত ভুল শুরু হয় স্বাস্থ্যসেবার প্রয়োজন বা evidence উপেক্ষা করা থেকে।", "ul",
              [("প্রয়োজনের আগে campaign", "স্বাস্থ্যসেবার প্রয়োজন ঠিক করার আগে ধারণা দিয়ে শুরু"), ("প্রেক্ষাপট ছাড়া sales data", "market definition, সময়কাল বা denominator যাচাই না করা"), ("কাজের সংখ্যা মানেই সম্পৃক্ততা নয়", "অর্থবহ পেশাগত সম্পৃক্ততার বদলে কার্যক্রম গোনা"), ("Evidence-এর বেশি claim", "প্রমাণ বা অনুমোদিত পণ্য-তথ্যের চেয়ে জোরালো দাবি")]),
}
def fn(k, lang): return f"mk-{k}" + ("" if lang == "en" else "-bn") + ".webp"
def fig(L, lang, key, lazy=True):
    alt, cap, kind, items = L[key]
    img = f'<img src="{IMG}{fn(key, lang)}{V}" alt="{esc(alt)}" width="1600" height="900" {"loading=\"lazy\" " if lazy else ""}decoding="async">'
    leg = ""
    if kind:
        leg = f'<{kind} class="pv-legend">' + "".join(f"<li><div><b>{esc(t)}</b>" + (f"<span>{esc(d)}</span>" if d else "") + "</div></li>" for t, d in items) + f"</{kind}>"
    return f'<figure class="pv-fig">{img}{leg}<figcaption class="caption">{esc(cap)}</figcaption></figure>'
def after_para(h, sec, block):
    pos = h.index(f'<section id="{sec}">'); pos = h.index("</p>", pos) + 4
    return h[:pos] + block + h[pos:]
def process(lang):
    L = EN if lang == "en" else BN
    d = R / "blog" / ("pharmaceutical-marketing-strategy-bangladesh" + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8"); assert "pv-figures.css" not in h
    h = h.replace("</head>", '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124"><style>.pm-wrap>.pv-fig{margin:0 0 26px;padding:clamp(10px,2.2vw,18px);border-radius:20px;background:linear-gradient(135deg,#eaf4f1,#fff5e8);border:1px solid #d6e6e3}.pm-wrap>.pv-fig img{display:block;width:100%;height:auto;border-radius:14px;aspect-ratio:16/9;object-fit:cover}.pm-wrap>.pv-fig .caption{margin:12px 4px 0;font-size:14px;color:#41545b}</style></head>', 1)
    for svg, key in (("segmentation-framework", "segmentation"), ("positioning-evidence-funnel", "positioning"), ("marketing-scorecard", "scorecard")):
        mm = re.search(r'<figure><img src="[^"]*' + svg + r'\.svg".*?</figure>', h, re.S); assert mm, svg
        h = h.replace(mm.group(0), fig(L, lang, key))
    h = after_para(h, "context", fig(L, lang, "context")); h = after_para(h, "research", fig(L, lang, "research"))
    h = after_para(h, "objectives", fig(L, lang, "channels")); h = after_para(h, "execution", fig(L, lang, "plan"))
    h = after_para(h, "ethics", fig(L, lang, "ethics")); h = after_para(h, "mistakes", "") if False else h
    p = h.index('<section id="mistakes">'); e = h.index("</h2>", p) + 5; h = h[:e] + fig(L, lang, "mistakes") + h[e:]
    cover = fig(L, lang, "cover", lazy=False).replace('decoding="async"', 'fetchpriority="high" decoding="async"')
    h = h.replace("</header><section class=\"pm-summary\">", "</header>" + cover + '<section class="pm-summary">', 1); assert cover in h
    soc = f"{SITE}{IMG}mk-social-{lang}.jpg{V}"
    og_alt = ("Pharmaceutical marketing strategy in Bangladesh: a teal staircase with a medicine box, stethoscope and golden scales." if lang == "en"
              else "বাংলাদেশে ফার্মাসিউটিক্যাল মার্কেটিং কৌশল: সিঁড়ির ধাপে ওষুধের বাক্স, স্টেথোস্কোপ ও সোনালি দাঁড়িপাল্লা।")
    for pat in (r'(<meta property="og:image" content=")', r'(<meta property="og:image:secure_url" content=")', r'(<meta name="twitter:image" content=")'):
        h = re.sub(pat + r'[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    if 'og:image:type' not in h:
        h = h.replace('<meta property="og:image:alt"', '<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt"', 1)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap_, w, hh):
        u = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": hh, "caption": cap_, "creator": CRE,
                "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    lst = [obj(f"mk-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(fn(k, lang), L[k][0], 1600, 900) for k in L]
    h, n = re.subn(r'"image":"[^"]*marketing-strategy-cover\.svg"', lambda _: '"image":' + json.dumps(lst, ensure_ascii=False, separators=(",", ":")), h, count=1); assert n == 1
    print(lang, "svg left:", sorted(set(re.findall(r'[^"]*\.svg', h))))
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(m)
    d.write_text(h, encoding="utf-8")
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg); print("ok", lg)
