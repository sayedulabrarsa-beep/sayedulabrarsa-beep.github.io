#!/usr/bin/env python3
"""Biosimilars article (EN+BN): place the 10 pictures with legends/captions written in code, add Key takeaways, update head/schema."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/biosimilars/"
def esc(s): return html.escape(s, quote=True)
EN = {
 "cover": ("Two almost identical antibody protein models stand either side of a medicine vial on a round podium, joined by a glowing ring, with a teal and gold shield behind.",
           "Biosimilars: biological manufacturing, quality comparison and use in healthcare.", None, []),
 "cell": ("A living cell with a nucleus sends a stream of small particles towards a large Y-shaped antibody molecule, with a small white tablet in front for size comparison.",
          "Biological medicines come from living cells. Their molecules are large and complex compared with a tablet.", "ul",
          [("Made in living cells", "bacteria, yeast or mammalian cells"), ("Large and complex", "far bigger than a typical tablet molecule"), ("Process matters", "manufacturing conditions shape the final product")]),
 "similar": ("Two nearly identical medicine vials with slightly different cap shades sit on a gold balance scale, with a magnifying glass between them showing two almost matching antibody molecules.",
             "A biosimilar is compared closely with its reference product. Small natural differences can exist.", "ul",
             [("Reference product", "the biological medicine already approved"), ("Biosimilar", "highly similar, compared head to head"), ("The test", "no clinically meaningful differences in quality, safety and effectiveness")]),
 "generic": ("Split picture. Left: a small ball-and-stick molecule beside a white tablet. Right: a very large, intricate antibody molecule beside a medicine vial.",
             "A conventional generic is usually a small-molecule copy. A biosimilar is a large biological medicine, highly similar but not an exact copy.", "two",
             [("Conventional generic", "usually a small chemical molecule with the same active ingredient"), ("Biosimilar", "a large, complex biological molecule, highly similar to the reference")]),
 "production": ("A scientist in a hair cover, mask and gloves checks a clipboard beside a bioreactor full of glowing cells, which connects through three filter columns to a sealed medicine vial.",
                "From cells to vial: the product is grown, harvested, purified, formulated and filled under controlled conditions.", "ol",
                [("Grow", "cells make the biological substance"), ("Purify", "filters remove unwanted material"), ("Fill", "the product is formulated and filled into vials"), ("Check", "quality is controlled and compared with the reference product")]),
 "approval": ("A lab scene with a screen comparing two antibody models, a microscope and test tubes, and below them a checklist, a group of people and a gold approval seal with a tick.",
              "Evidence is built step by step. Regulators weigh all of it together.", "ol",
              [("Lab comparison", "structure, purity and potency"), ("Function tests", "does it work in the same way?"), ("Clinical evidence when needed", "tailored to the product"), ("Regulator decision", "all evidence considered together")]),
 "switching": ("A patient with a bandage on his arm sits beside a pharmacist with a clipboard and a doctor, with two vials and a curved arrow between them under a teal shield with a tick.",
               "Switching between a reference product and a biosimilar is a clinical decision, made with the treating team.", "ul",
               [("Monitoring continues", "immune reactions and safety are followed after approval"), ("Do not switch alone", "talk to your clinician or pharmacist first"), ("Rules differ", "interchangeability depends on the country and regulator")]),
 "bd": ("A smiling pharmacist holds a medicine vial beside a refrigerator of vials marked with a snowflake, with a green map shape of Bangladesh and a small stack of gold coins and bars behind.",
        "In Bangladesh, check official DGDA information, follow storage instructions and ask about access. This picture is a symbol, not a price guide.", "ul",
        [("Cold storage", "many biologics need refrigeration; follow the pack instructions"), ("DGDA status", "check official DGDA information for a product's registration"), ("Cost and access", "matter in real life; this article gives no prices")]),
 "clinic": ("A doctor with a stethoscope talks with a patient across a desk with a vial and clipboard, and a teal and gold shield with a glowing light bulb floats between them.",
            "The best next step is a conversation with your treating clinician or pharmacist.", "ul",
            [("Ask about the product and plan", ""), ("Ask about schedule and storage", ""), ("Ask about follow-up", ""), ("Never start, stop or switch alone", "")]),
 "key": ("Six steps rise like a staircase to a shield with a cross: a cell with an antibody, a molecule model, a microscope, a balance scale, a family and the shield.",
         "Six ideas to take away.", "ol",
         [("Made by living cells", "complex molecules from living systems"), ("Not a simple copy", "highly similar, not an exact molecular copy"), ("Compared in the lab", "analytical and functional comparison comes first"),
          ("Weighed on all the evidence", "tailored clinical data where needed"), ("Used with monitoring", "immunogenicity, quality and clinician guidance matter"), ("Safe use rests on evidence", "not on similar names or ingredients")]),
}
BN = {
 "cover": ("প্রায় একই রকম দেখতে দুটি অ্যান্টিবডি প্রোটিনের মডেল একটি গোল মঞ্চে ওষুধের ভায়ালের দুই পাশে, মাঝে আলোকিত বলয়; পেছনে টিল-সোনালি ঢাল।",
           "বায়োসিমিলার: জীববৈজ্ঞানিক উৎপাদন, গুণগত তুলনা ও চিকিৎসায় ব্যবহারের ধারণা।", None, []),
 "cell": ("নিউক্লিয়াসসহ একটি জীবন্ত কোষ থেকে ছোট কণার ধারা একটি বড় Y-আকৃতির অ্যান্টিবডি অণুর দিকে যাচ্ছে; সামনে আকার তুলনার জন্য একটি ছোট সাদা ট্যাবলেট।",
          "বায়োলজিক ওষুধ জীবন্ত কোষ থেকে আসে। ট্যাবলেটের অণুর তুলনায় এর অণু বড় ও জটিল।", "ul",
          [("জীবন্ত কোষে তৈরি", "ব্যাকটেরিয়া, ইস্ট বা স্তন্যপায়ী প্রাণীর কোষ"), ("বড় ও জটিল", "সাধারণ ট্যাবলেটের অণুর চেয়ে অনেক বড়"), ("প্রক্রিয়াই গুরুত্বপূর্ণ", "উৎপাদনের পরিবেশ চূড়ান্ত পণ্যকে প্রভাবিত করে")]),
 "similar": ("সামান্য ভিন্ন রঙের ঢাকনাসহ প্রায় একই রকম দুটি ওষুধের ভায়াল সোনালি দাঁড়িপাল্লায়; মাঝখানে ম্যাগনিফাইং গ্লাসে প্রায় মিলে যাওয়া দুটি অ্যান্টিবডি অণু।",
             "বায়োসিমিলারকে তার Reference Product-এর সঙ্গে খুঁটিয়ে তুলনা করা হয়। স্বাভাবিক ছোট পার্থক্য থাকতে পারে।", "ul",
             [("Reference Product", "আগে থেকে অনুমোদিত বায়োলজিক ওষুধ"), ("বায়োসিমিলার", "অত্যন্ত সদৃশ; সরাসরি তুলনা করা হয়"), ("পরীক্ষা", "মান, নিরাপত্তা ও কার্যকারিতায় চিকিৎসাগতভাবে অর্থপূর্ণ কোনো পার্থক্য নেই")]),
 "generic": ("দুই ভাগের ছবি। বাঁয়ে: সাদা ট্যাবলেটের পাশে ছোট বল-ও-স্টিক অণু। ডানে: ওষুধের ভায়ালের পাশে অনেক বড় ও জটিল অ্যান্টিবডি অণু।",
             "প্রচলিত জেনেরিক সাধারণত ছোট অণুর কপি। বায়োসিমিলার বড় বায়োলজিক ওষুধ—অত্যন্ত সদৃশ, কিন্তু হুবহু কপি নয়।", "two",
             [("প্রচলিত জেনেরিক", "সাধারণত একই সক্রিয় উপাদানসহ ছোট রাসায়নিক অণু"), ("বায়োসিমিলার", "বড় ও জটিল জীববৈজ্ঞানিক অণু; Reference Product-এর সঙ্গে অত্যন্ত সদৃশ")]),
 "production": ("হেয়ার ক্যাপ, মাস্ক ও গ্লাভস পরা একজন বিজ্ঞানী ক্লিপবোর্ড দেখছেন; পাশে জ্বলজ্বলে কোষভরা বায়োরিঅ্যাক্টর, যা তিনটি ফিল্টার-কলামের মধ্য দিয়ে সিল করা ওষুধের ভায়ালে যুক্ত।",
                "কোষ থেকে ভায়াল পর্যন্ত: নিয়ন্ত্রিত পরিবেশে পণ্য জন্মানো, সংগ্রহ, বিশুদ্ধ করা, ফর্মুলেশন ও ভরা হয়।", "ol",
                [("জন্মানো", "কোষ জীববৈজ্ঞানিক উপাদান তৈরি করে"), ("বিশুদ্ধ করা", "ফিল্টার অবাঞ্ছিত উপাদান সরায়"), ("ভরা", "ফর্মুলেশন করে ভায়ালে ভরা হয়"), ("পরীক্ষা", "মান নিয়ন্ত্রণ ও Reference Product-এর সঙ্গে তুলনা")]),
 "approval": ("ল্যাবের দৃশ্য: পর্দায় দুটি অ্যান্টিবডি মডেলের তুলনা, মাইক্রোস্কোপ ও টেস্ট টিউব; নিচে চেকলিস্ট, একদল মানুষ এবং টিক চিহ্নসহ সোনালি অনুমোদন-সিল।",
              "প্রমাণ ধাপে ধাপে গড়ে ওঠে। নিয়ন্ত্রক সংস্থা সব প্রমাণ একসঙ্গে বিবেচনা করে।", "ol",
              [("ল্যাব তুলনা", "গঠন, বিশুদ্ধতা ও শক্তি"), ("কার্যকারিতা পরীক্ষা", "একই ভাবে কাজ করে কি না"), ("প্রয়োজনে ক্লিনিক্যাল প্রমাণ", "পণ্য অনুযায়ী সাজানো"), ("নিয়ন্ত্রকের সিদ্ধান্ত", "সব প্রমাণ একসঙ্গে বিবেচিত")]),
 "switching": ("হাতে ব্যান্ডেজ লাগানো একজন রোগী ক্লিপবোর্ডহাতে ফার্মাসিস্ট ও একজন ডাক্তারের পাশে; মাঝে টিক চিহ্নসহ টিল ঢালের নিচে দুটি ভায়াল ও একটি বাঁকা তীর।",
               "Reference Product ও বায়োসিমিলারের মধ্যে বদল একটি চিকিৎসাগত সিদ্ধান্ত, যা চিকিৎসা-দলের সঙ্গে নিতে হয়।", "ul",
               [("পর্যবেক্ষণ চলতে থাকে", "অনুমোদনের পরও ইমিউন প্রতিক্রিয়া ও নিরাপত্তা দেখা হয়"), ("নিজে বদলাবেন না", "আগে চিকিৎসক বা ফার্মাসিস্টের সঙ্গে কথা বলুন"), ("নিয়ম ভিন্ন হতে পারে", "interchangeability দেশ ও নিয়ন্ত্রক সংস্থার ওপর নির্ভর করে")]),
 "bd": ("হাসিমুখে একজন ফার্মাসিস্ট ওষুধের ভায়াল ধরে আছেন; পাশে তুষারকণা-চিহ্নযুক্ত ভায়ালভরা ফ্রিজ, পেছনে বাংলাদেশের সবুজ মানচিত্রের আকার এবং সোনালি মুদ্রা ও বার।",
        "বাংলাদেশে DGDA-র অফিসিয়াল তথ্য দেখুন, সংরক্ষণের নির্দেশনা মানুন এবং প্রাপ্যতা সম্পর্কে জিজ্ঞাসা করুন। ছবিটি প্রতীক, মূল্যতালিকা নয়।", "ul",
        [("ঠান্ডায় সংরক্ষণ", "অনেক বায়োলজিক ওষুধ ফ্রিজে রাখতে হয়; প্যাকের নির্দেশনা মানুন"), ("DGDA-র অবস্থা", "পণ্যের নিবন্ধন DGDA-র অফিসিয়াল তথ্যে দেখুন"), ("খরচ ও প্রাপ্যতা", "বাস্তবে গুরুত্বপূর্ণ; এই লেখায় কোনো দাম দেওয়া হয়নি")]),
 "clinic": ("স্টেথোস্কোপ গলায় একজন ডাক্তার ডেস্কের ওপারে রোগীর সঙ্গে কথা বলছেন; ডেস্কে ভায়াল ও ক্লিপবোর্ড, মাঝে উজ্জ্বল বাল্বসহ টিল-সোনালি ঢাল ভাসছে।",
            "পরবর্তী সেরা ধাপ হলো আপনার চিকিৎসক বা ফার্মাসিস্টের সঙ্গে কথা বলা।", "ul",
            [("পণ্য ও চিকিৎসা-পরিকল্পনা জিজ্ঞাসা করুন", ""), ("সময়সূচি ও সংরক্ষণ জিজ্ঞাসা করুন", ""), ("ফলো-আপ সম্পর্কে জিজ্ঞাসা করুন", ""), ("নিজে শুরু, বন্ধ বা বদল করবেন না", "")]),
 "key": ("ছয় ধাপের সিঁড়ি ওপরে উঠে ক্রস-চিহ্নযুক্ত ঢালে শেষ: অ্যান্টিবডিসহ কোষ, অণুর মডেল, মাইক্রোস্কোপ, দাঁড়িপাল্লা, পরিবার ও ঢাল।",
         "মনে রাখার মতো ছয়টি কথা।", "ol",
         [("জীবন্ত কোষে তৈরি", "জীবন্ত ব্যবস্থা থেকে আসা জটিল অণু"), ("সাধারণ কপি নয়", "অত্যন্ত সদৃশ, হুবহু আণবিক কপি নয়"), ("ল্যাবে তুলনা", "আগে বিশ্লেষণাত্মক ও কার্যকারিতা তুলনা"),
          ("সব প্রমাণ মিলিয়ে বিচার", "প্রয়োজনে পণ্য অনুযায়ী ক্লিনিক্যাল তথ্য"), ("পর্যবেক্ষণসহ ব্যবহার", "ইমিউনোজেনিসিটি, মান ও চিকিৎসকের নির্দেশনা গুরুত্বপূর্ণ"), ("নিরাপদ ব্যবহার প্রমাণের ওপর", "নামের বা উপাদানের মিলের ওপর নয়")]),
}
FILES = {"cover": "bs-cover", "cell": "bs-cell", "similar": "bs-biosimilar", "generic": "bs-generic", "production": "bs-production", "approval": "bs-approval",
         "switching": "bs-switching", "bd": "bs-bangladesh", "clinic": "bs-clinic", "key": "bs-takeaways"}

def fig(L, key, lazy=True):
    alt, cap, kind, items = L[key]
    cls = "pv-fig pv-key" if key == "key" else "pv-fig"
    img = f'<img src="{IMG}{FILES[key]}.webp" alt="{esc(alt)}" width="1600" height="900" {"loading=\"lazy\" " if lazy else ""}decoding="async">'
    leg = ""
    if kind:
        tag = "ol" if kind == "ol" else "ul"
        c = "pv-legend" + (" pv-two" if kind == "two" else "")
        leg = f'<{tag} class="{c}">' + "".join(f"<li><div><b>{esc(t)}</b>" + (f"<span>{esc(d)}</span>" if d else "") + "</div></li>" for t, d in items) + f"</{tag}>"
    return f'<figure class="{cls}">{img}{leg}<figcaption class="caption">{esc(cap)}</figcaption></figure>'

def after_para(h, sec, n, block):
    pos = h.index(f'<h2 id="{sec}"')
    for _ in range(n): pos = h.index("</p>", pos) + 4
    return h[:pos] + "\n" + block + h[pos:]

def process(lang):
    L = EN if lang == "en" else BN
    d = R / "blog" / ("biosimilars-explained" + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8")
    assert "pv-figures.css" not in h, "already applied"
    old = '<link rel="stylesheet" href="/assets/site-polish.css?v=sa-20261122">'; assert old in h
    h = h.replace(old, old + '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124">', 1)
    m = re.search(r'<figure class="hero-visual">.*?</figure>', h, re.S); assert m
    cap = re.search(r'<figcaption class="caption">(.*?)</figcaption>', m.group(0), re.S).group(1)
    cover = (f'<figure class="hero-visual"><a href="{IMG}bs-cover.webp" target="_blank" rel="noopener"><img src="{IMG}bs-cover.webp" alt="{esc(L["cover"][0])}" width="1600" height="900" fetchpriority="high" decoding="async"></a>'
             f'<figcaption class="caption">{cap}</figcaption></figure>')
    h = h.replace(m.group(0), cover)
    h = after_para(h, "s1", 1, fig(L, "cell"))
    h = after_para(h, "s2", 2, fig(L, "similar"))
    h = after_para(h, "s3", 1, fig(L, "generic"))
    h = after_para(h, "s4", 1, fig(L, "production"))
    h = after_para(h, "s5", 1, fig(L, "approval"))
    h = after_para(h, "s6", 3, fig(L, "switching"))
    h = after_para(h, "s7", 1, fig(L, "bd"))
    # s8: clinic picture right after the heading, key takeaways section after the list
    p = h.index('<h2 id="s8"'); e = h.index("</h2>", p) + 5
    h = h[:e] + "\n" + fig(L, "clinic") + h[e:]
    title = "Key takeaways" if lang == "en" else "মূল কথাগুলো"
    f = h.index('<h2 id="faq"')
    h = h[:f] + f'<h2 id="key-takeaways">{title}</h2>\n' + fig(L, "key") + "\n" + h[f:]
    s8 = "What to remember" if lang == "en" else "মনে রাখার বিষয়"
    anchor = '<li><a href="#faq">'; assert anchor in h
    h = h.replace(anchor, f'<li><a href="#s8">{s8}</a></li><li><a href="#key-takeaways">{title}</a></li>' + anchor, 1)
    soc = f"{SITE}{IMG}bs-social-{lang}.jpg"
    og_alt = ("Biosimilars Explained: a staircase of six steps from a living cell and antibody to a protective shield." if lang == "en"
              else "বায়োসিমিলার: জীবন্ত কোষ ও অ্যান্টিবডি থেকে সুরক্ষা-ঢাল পর্যন্ত ছয় ধাপের সিঁড়ি।")
    for pat in (r'(<meta property="og:image" content=")', r'(<meta property="og:image:secure_url" content=")', r'(<meta name="twitter:image" content=")'):
        h = re.sub(pat + r'[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:type" content=")[^"]*', r'\g<1>image/jpeg', h)
    h = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r'\g<1>1200', h)
    h = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r'\g<1>630', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap_, w, hh):
        u = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": hh, "caption": cap_, "creator": CRE,
                "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    lst = [obj(f"bs-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(FILES[k] + ".webp", L[k][0], 1600, 900) for k in FILES]
    h, n = re.subn(r'"image":\[[^\]]*\]', lambda _: '"image":' + json.dumps(lst, ensure_ascii=False, separators=(",", ":")), h, count=1); assert n == 1
    assert ".svg" not in h, re.findall(r'[^"]{0,60}\.svg', h)[:3]
    for mm_ in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(mm_)
    d.write_text(h, encoding="utf-8")
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg); print("ok", lg)
