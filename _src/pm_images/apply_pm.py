#!/usr/bin/env python3
"""Pharmaceutical Product Management (EN+BN): place 12 pictures with captions, add og/twitter image tags and BlogPosting images."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/pharma-product-management/"; V = "?v=pm-20261128"
def esc(s): return html.escape(s, quote=True)
EN = {
 "cover": ("A pharmacist in a white coat looks out of a glass office window at a Dhaka-style skyline at sunset, with a tablet, a plain white medicine box and a blister pack on the desk.",
           "Pharmaceutical product management in Bangladesh connects healthcare need, market insight, quality, ethics and measurable execution. AI-generated photo-style illustration."),
 "what": ("A white medicine box, blister pack, amber bottle, brass compass and a closed notebook arranged on a wooden desk in warm window light.",
          "A brand is built by more than promotion: healthcare need, market data, positioning, availability and ethical execution. AI-generated photo-style illustration."),
 "bangladesh": ("A pharmacist in a white coat shows a plain white medicine box to a customer across a glass counter in a Bangladeshi pharmacy with shelves of boxes behind.",
                "Where many brands share the same molecule, differentiation has to come from credible evidence, availability and service. AI-generated photo-style illustration."),
 "roles": ("A stethoscope, calculator, tablet with a blank screen, blister pack and a notebook with a pen laid out on a wooden desk.",
           "Core responsibilities combine clinical understanding, numbers, digital and field tools, and good records. AI-generated photo-style illustration."),
 "framework": ("A man in smart casual clothes carrying a folder walks up wide sunlit stone steps toward a glass office building.",
               "A six-step brand plan moves from insight to positioning, objectives, planning, execution and review. AI-generated photo-style illustration."),
 "checklist": ("A clipboard with five ticked checklist lines stands on a desk beside books, a pen, a laptop and a blister pack.",
               "Check the one-page brand plan for objective, evidence, approvals, owner and timeline before acting. AI-generated photo-style illustration."),
 "hcp": ("A doctor in a white coat and a medical representative with a closed folder talk calmly across a desk in a bright clinic office.",
         "Ethical engagement respects the doctor’s time and judgement and uses approved, current information. AI-generated photo-style illustration."),
 "kpi": ("A man looks at a monitor showing a line chart, bar chart and donut chart without labels, with a cup of tea and a notebook on the desk.",
         "Choose KPIs that go beyond sales: growth, availability, engagement quality and compliance. AI-generated photo-style illustration."),
 "skills": ("An open leather work bag on a desk holds a microscope, laptop, headphones, notebook and pen.",
            "A product manager’s toolkit combines scientific knowledge, data analysis, communication and planning. AI-generated photo-style illustration."),
 "quality": ("A quality inspector in a hairnet, mask and gloves examines a tablet above a tray of white tablets in a pharmaceutical production area.",
             "Regulation and product quality come first: follow approved information, respect GMP and avoid claims beyond the evidence. AI-generated photo-style illustration."),
 "career": ("A pharmacist in a white coat holding a folder stands between a pharmacy shelf of plain boxes and a bright glass office doorway.",
            "A pharmacy degree is a strong start for product management when it is combined with marketing and data skills. AI-generated photo-style illustration."),
 "review": ("A presenter in a teal jacket explains charts on a wall screen to three colleagues seated at a table with laptops.",
            "A monthly PMD review shares the data, agrees actions and owners, and checks results the next month. AI-generated photo-style illustration."),
}
BN = {
 "cover": ("সাদা কোট পরা একজন ফার্মাসিস্ট কাচের অফিস-জানালা দিয়ে সূর্যাস্তের আলোয় ঢাকার মতো শহরের আকাশরেখা দেখছেন; টেবিলে ট্যাবলেট, সাদা ওষুধের বাক্স ও ব্লিস্টার প্যাক।",
           "বাংলাদেশে ফার্মাসিউটিক্যাল প্রোডাক্ট ম্যানেজমেন্ট স্বাস্থ্যসেবার প্রয়োজন, বাজারের তথ্য, মান, নৈতিকতা ও পরিমাপযোগ্য বাস্তবায়নকে যুক্ত করে। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "what": ("কাঠের টেবিলে জানালার নরম আলোয় সাজানো সাদা ওষুধের বাক্স, ব্লিস্টার প্যাক, বাদামি বোতল, পিতলের কম্পাস ও বন্ধ নোটবুক।",
          "ব্র্যান্ড শুধু প্রচারে গড়ে ওঠে না: স্বাস্থ্যসেবার প্রয়োজন, বাজারের তথ্য, positioning, প্রাপ্যতা ও নৈতিক বাস্তবায়ন একসঙ্গে লাগে। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "bangladesh": ("বাংলাদেশের একটি ফার্মেসিতে কাচের কাউন্টারের ওপারে সাদা কোট পরা ফার্মাসিস্ট ক্রেতাকে একটি সাদা ওষুধের বাক্স দেখাচ্ছেন; পেছনে বাক্সের তাক।",
                "একই উপাদানের অনেক ব্র্যান্ড থাকলে পার্থক্য গড়তে হয় বিশ্বাসযোগ্য evidence, প্রাপ্যতা ও সেবা দিয়ে। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "roles": ("কাঠের টেবিলে স্টেথোস্কোপ, ক্যালকুলেটর, ফাঁকা পর্দার ট্যাবলেট, ব্লিস্টার প্যাক এবং কলমসহ নোটবুক।",
           "প্রধান দায়িত্বে মেলে ক্লিনিক্যাল বোঝাপড়া, সংখ্যা, ডিজিটাল ও field উপকরণ এবং ভালো রেকর্ড। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "framework": ("ফোল্ডার হাতে স্মার্ট ক্যাজুয়াল পোশাকের একজন রোদ-ঝলমলে চওড়া পাথরের সিঁড়ি বেয়ে কাচের অফিস ভবনের দিকে উঠছেন।",
               "ছয় ধাপের ব্র্যান্ড পরিকল্পনা এগোয় insight, positioning, লক্ষ্য, পরিকল্পনা, বাস্তবায়ন ও review ধরে। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "checklist": ("টেবিলে বই, কলম, ল্যাপটপ ও ব্লিস্টার প্যাকের পাশে পাঁচটি টিক-দেওয়া লাইনসহ একটি ক্লিপবোর্ড।",
               "কাজ শুরুর আগে এক পাতার পরিকল্পনায় লক্ষ্য, evidence, অনুমোদন, দায়িত্বশীল ও সময়সূচি যাচাই করুন। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "hcp": ("উজ্জ্বল ক্লিনিক-কক্ষে ডেস্কের দুই পাশে সাদা কোট পরা একজন চিকিৎসক ও বন্ধ ফোল্ডার হাতে একজন মেডিকেল রিপ্রেজেন্টেটিভ শান্তভাবে কথা বলছেন।",
         "নৈতিক যোগাযোগে চিকিৎসকের সময় ও বিবেচনাকে সম্মান করা হয় এবং অনুমোদিত, হালনাগাদ তথ্য ব্যবহার করা হয়। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "kpi": ("একজন মনিটরে লেবেলহীন লাইন চার্ট, বার চার্ট ও ডোনাট চার্ট দেখছেন; টেবিলে এক কাপ চা ও নোটবুক।",
         "বিক্রির বাইরেও KPI বেছে নিন: প্রবৃদ্ধি, প্রাপ্যতা, সম্পৃক্ততার মান ও compliance। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "skills": ("টেবিলে খোলা চামড়ার কাজের ব্যাগে মাইক্রোস্কোপ, ল্যাপটপ, হেডফোন, নোটবুক ও কলম।",
            "প্রোডাক্ট ম্যানেজারের উপকরণে মেলে বৈজ্ঞানিক জ্ঞান, ডেটা বিশ্লেষণ, যোগাযোগ ও পরিকল্পনা। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "quality": ("হেয়ারনেট, মাস্ক ও গ্লাভস পরা একজন কোয়ালিটি পরিদর্শক ওষুধ উৎপাদন এলাকায় সাদা ট্যাবলেটের ট্রের ওপরে একটি ট্যাবলেট পরীক্ষা করছেন।",
             "নিয়ম ও মান আগে: অনুমোদিত তথ্য মানুন, GMP-কে সম্মান করুন এবং evidence-এর বেশি claim করবেন না। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "career": ("ফোল্ডার হাতে সাদা কোট পরা একজন ফার্মাসিস্ট সাদা বাক্সের ফার্মেসি-তাক ও উজ্জ্বল কাচের অফিস-দরজার মাঝখানে দাঁড়িয়ে আছেন।",
            "marketing ও ডেটা দক্ষতা যোগ করলে ফার্মেসির ডিগ্রি প্রোডাক্ট ম্যানেজমেন্টের জন্য শক্ত শুরু। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
 "review": ("টিল-রঙের জ্যাকেট পরা একজন উপস্থাপক দেয়ালের পর্দায় চার্ট বুঝিয়ে দিচ্ছেন; টেবিলে ল্যাপটপসহ তিনজন সহকর্মী বসে।",
            "মাসিক PMD review-তে ডেটা ভাগ করা হয়, কাজ ও দায়িত্বশীল ঠিক হয় এবং পরের মাসে ফল দেখা হয়। AI-তৈরি ছবি-ধাঁচের চিত্র।"),
}
def fn(k, lang): return f"pm-{k}" + ("" if lang == "en" else "-bn") + ".webp"
def fig(L, lang, key, lazy=True):
    alt, cap = L[key]
    img = f'<img src="{IMG}{fn(key, lang)}{V}" alt="{esc(alt)}" width="1600" height="900" {"loading=\"lazy\" " if lazy else ""}decoding="async">'
    return f'<figure class="pv-fig">{img}<figcaption class="caption">{esc(cap)}</figcaption></figure>'
def after_para(h, sec, block):
    pos = h.index(f'<section id="{sec}">'); pos = h.index("</p>", pos) + 4
    return h[:pos] + block + h[pos:]
def after_h3(h, text, block):
    pos = h.index(f"<h3>{text}</h3>") + len(f"<h3>{text}</h3>"); return h[:pos] + block + h[pos:]
H3 = {"en": ("A simple monthly PMD review cycle", "A practical one-page brand-plan checklist"), "bn": ("একটি সহজ মাসিক PMD review cycle", "এক পাতার brand-plan checklist")}
def process(lang):
    L = EN if lang == "en" else BN
    d = R / "blog" / ("pharmaceutical-product-management-bangladesh" + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8"); assert "pv-figures.css" not in h
    css = '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124"><style>.pm-wrap .pv-fig{margin:26px 0;padding:clamp(10px,2.2vw,18px);border-radius:20px;background:linear-gradient(135deg,#eaf4f1,#fff5e8);border:1px solid #d6e6e3}.pm-wrap .pv-fig img{display:block;width:100%;height:auto;border-radius:14px;aspect-ratio:16/9;object-fit:cover}.pm-wrap .pv-fig .caption{margin:12px 4px 0;font-size:14px;line-height:1.55;color:#41545b}</style>'
    h = h.replace("</head>", css + "</head>", 1)
    for sec, key in (("what", "what"), ("bd", "bangladesh"), ("work", "roles"), ("framework", "framework"), ("ethics", "hcp"), ("kpi", "kpi"), ("skills", "skills"), ("regulation", "quality"), ("career", "career")):
        h = after_para(h, sec, fig(L, lang, key))
    h = after_h3(h, H3[lang][0], fig(L, lang, "review")); h = after_h3(h, H3[lang][1], fig(L, lang, "checklist"))
    cover = fig(L, lang, "cover", lazy=False).replace('decoding="async"', 'fetchpriority="high" decoding="async"')
    assert '</div><section class="pm-summary">' in h
    h = h.replace('</div><section class="pm-summary">', "</div>" + cover + '<section class="pm-summary">', 1)
    soc = f"{SITE}{IMG}pm-social-{lang}.jpg{V}"; og_alt = L["cover"][0]
    tags = (f'<meta property="og:image" content="{soc}"><meta property="og:image:secure_url" content="{soc}"><meta property="og:image:type" content="image/jpeg">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(og_alt)}">')
    h = h.replace('<meta property="og:locale"', tags + '<meta property="og:locale"', 1)
    h = h.replace('<meta name="twitter:card" content="summary">', '<meta name="twitter:card" content="summary_large_image">', 1)
    h = re.sub(r'(<meta name="twitter:description" content="[^"]*">)', r'\1' + f'<meta name="twitter:image" content="{soc}"><meta name="twitter:image:alt" content="{esc(og_alt)}">', h, 1)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap_, w, hh):
        u = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": hh, "caption": cap_, "creator": CRE,
                "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    order = ["cover", "what", "bangladesh", "roles", "framework", "checklist", "hcp", "kpi", "skills", "quality", "career", "review"]
    lst = [obj(f"pm-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(fn(k, lang), L[k][0], 1600, 900) for k in order]
    thumb = f"{SITE}{IMG}pm-card.webp"
    h, n = re.subn(r'("inLanguage":"(?:en|bn)",)("datePublished")', lambda m: m.group(1) + '"image":' + json.dumps(lst, ensure_ascii=False, separators=(",", ":")) + ',"thumbnailUrl":"' + thumb + '",' + m.group(2), h, count=1); assert n == 1
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(m)
    # order check
    pos = [h.index(IMG + fn(k, lang)) for k in ["cover", "what", "bangladesh", "roles", "framework", "kpi", "skills", "quality", "career"]]
    assert pos == sorted(pos), pos
    d.write_text(h, encoding="utf-8"); print(lang, "ok", h.count("<figure class=\"pv-fig\">"))
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg)
