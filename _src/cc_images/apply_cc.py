#!/usr/bin/env python3
"""Cold Chain article (EN+BN): place the 10 photos with captions, update head tags and schema. The four SVG diagrams stay."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/cold-chain/"; V = "?v=cc-20261127"
SLUG = "pharmaceutical-cold-chain-medicines-storage-transport"
def esc(s): return html.escape(s, quote=True)
KEYS = ["cover", "what", "which", "why", "how", "monitor", "excursion", "bangladesh", "advice", "key"]
EN = {
 "cover": "AI-generated photo-style image: a gloved hand lifts the lid of a white insulated shipper, with cold vapour drifting over five glass vials with blue caps in a foam tray.",
 "what": "AI-generated photo-style image: an aisle in a pharmaceutical cold-storage room with shelves of plain white cartons, a frosted door and cold mist on the floor.",
 "which": "AI-generated photo-style image: a wooden tray holding a pen injector, a glass vial, a prefilled syringe and an ampoule, surrounded by ice crystals.",
 "why": "AI-generated photo-style image: two identical glass vials side by side, one with clear liquid and frost droplets, the other with cloudy liquid and white clumps.",
 "how": "AI-generated photo-style image: a worker in a navy jacket and blue gloves slides a white insulated box onto a trolley beside a white refrigerated van with open rear doors at dusk.",
 "monitor": "AI-generated photo-style image: a small white digital temperature data logger with a green light, taped to a carton inside an insulated box beside a glass vial and frozen gel packs.",
 "excursion": "AI-generated photo-style image: gloved hands attach a blank tag to a carton wrapped in yellow tape on a metal storage shelf.",
 "bangladesh": "AI-generated photo-style image: a pharmacist in a white coat places a box in a glass-door medicine refrigerator inside a pharmacy, with rickshaws on a rainy street at dusk outside.",
 "advice": "AI-generated photo-style image: hands place a plain white medicine box on a refrigerator shelf beside a glass of water and a folded cloth.",
 "key": "AI-generated photo-style image: an open insulated shipper with frozen blue gel packs around a foam tray holding six glass vials.",
}
CAP = {
 "what": "A cold chain links the manufacturer, warehouse, transport provider, distributor, pharmacy or hospital and patient. A cold room is only one link.",
 "which": "Illustration only: the items shown are generic. Which medicines need temperature control depends on the product and stage of use, so follow the carton, leaflet and manufacturer instructions.",
 "why": "Illustration only. A product may look normal even when its potency has changed, so appearance alone cannot confirm quality.",
 "how": "Active refrigerated systems or validated passive shippers protect the load in transport, and a suitable data logger records conditions.",
 "monitor": "A thermometer shows one moment; a digital data logger records temperature over time. Calibration and record review make the readings dependable.",
 "excursion": "Illustration only: an affected batch is held and segregated so it cannot be supplied or used accidentally, until a documented decision is made.",
 "bangladesh": "Illustration only. DGDA's 2024 Model Pharmacy guideline includes checks on preserving temperature-sensitive medicines and monitoring storage temperature. It does not mean every medicine needs 2–8°C.",
 "advice": "Illustration only: follow the product's storage statement, and do not refrigerate a medicine unless its instructions say so.",
 "key": "Illustration only: a validated shipper with conditioned coolant protects products in transit, but storage limits remain product-specific.",
}
BN = {
 "cover": "AI-তৈরি ফটো-ধাঁচের ছবি: গ্লাভস পরা হাতে সাদা ইনসুলেটেড শিপারের ঢাকনা তোলা হচ্ছে; ফোম ট্রেতে নীল ঢাকনার পাঁচটি কাচের ভায়ালের ওপর ঠান্ডা বাষ্প।",
 "what": "AI-তৈরি ফটো-ধাঁচের ছবি: ফার্মাসিউটিক্যাল কোল্ড-স্টোরেজ রুমের করিডরে সাদা কার্টনভরা তাক, কুয়াশাচ্ছন্ন কাচের দরজা ও মেঝেতে ঠান্ডা কুয়াশা।",
 "which": "AI-তৈরি ফটো-ধাঁচের ছবি: কাঠের ট্রেতে একটি পেন ইনজেক্টর, কাচের ভায়াল, প্রিফিলড সিরিঞ্জ ও অ্যাম্পুল; চারপাশে বরফের কণা।",
 "why": "AI-তৈরি ফটো-ধাঁচের ছবি: পাশাপাশি দুটি একই রকম কাচের ভায়াল; একটিতে স্বচ্ছ তরল ও হিমের ফোঁটা, অন্যটিতে ঘোলা তরল ও সাদা দলা।",
 "how": "AI-তৈরি ফটো-ধাঁচের ছবি: গোধূলিতে খোলা পেছনের দরজাসহ সাদা রেফ্রিজারেটেড ভ্যানের পাশে নেভি জ্যাকেট ও নীল গ্লাভস পরা একজন কর্মী ট্রলিতে সাদা ইনসুলেটেড বাক্স তুলছেন।",
 "monitor": "AI-তৈরি ফটো-ধাঁচের ছবি: ইনসুলেটেড বাক্সের ভেতরে কার্টনের ওপর টেপ দিয়ে লাগানো সবুজ বাতিসহ ছোট সাদা ডিজিটাল তাপমাত্রা ডেটা লগার; পাশে কাচের ভায়াল ও জমাট জেল প্যাক।",
 "excursion": "AI-তৈরি ফটো-ধাঁচের ছবি: ধাতব তাকে হলুদ টেপে মোড়ানো কার্টনে গ্লাভস পরা হাতে ফাঁকা একটি ট্যাগ লাগানো হচ্ছে।",
 "bangladesh": "AI-তৈরি ফটো-ধাঁচের ছবি: সাদা কোট পরা ফার্মাসিস্ট ফার্মেসির কাচের দরজার ওষুধ-রেফ্রিজারেটরে একটি বাক্স রাখছেন; বাইরে গোধূলির বৃষ্টিভেজা রাস্তায় রিকশা।",
 "advice": "AI-তৈরি ফটো-ধাঁচের ছবি: রেফ্রিজারেটরের তাকে এক গ্লাস পানি ও ভাঁজ করা কাপড়ের পাশে সাদা একটি ওষুধের বাক্স রাখা হচ্ছে।",
 "key": "AI-তৈরি ফটো-ধাঁচের ছবি: খোলা ইনসুলেটেড শিপারে জমাট নীল জেল প্যাকে ঘেরা ফোম ট্রেতে ছয়টি কাচের ভায়াল।",
}
BCAP = {
 "what": "কোল্ড চেইন উৎপাদনকারী, ওয়্যারহাউস, পরিবহনকারী, ডিস্ট্রিবিউটর, ফার্মেসি বা হাসপাতাল এবং রোগীকে যুক্ত করে। কোল্ড রুম এর একটি ধাপ মাত্র।",
 "which": "শুধু উদাহরণ: ছবির জিনিসগুলো সাধারণ চিত্র। কোন ওষুধে তাপমাত্রা নিয়ন্ত্রণ দরকার তা পণ্য ও ব্যবহারের ধাপের ওপর নির্ভর করে; তাই কার্টন, লিফলেট ও উৎপাদনকারীর নির্দেশনা অনুসরণ করুন।",
 "why": "শুধু উদাহরণ। কার্যকারিতা বদলে গেলেও পণ্য দেখতে স্বাভাবিক থাকতে পারে, তাই শুধু দেখে মান নিশ্চিত করা যায় না।",
 "how": "পরিবহনে active রেফ্রিজারেটেড ব্যবস্থা বা validated passive শিপার পণ্য রক্ষা করে, আর উপযুক্ত ডেটা লগার অবস্থা রেকর্ড করে।",
 "monitor": "থার্মোমিটার এক মুহূর্তের তাপমাত্রা দেখায়; ডিজিটাল ডেটা লগার সময়ের সঙ্গে তাপমাত্রা রেকর্ড করে। ক্যালিব্রেশন ও রেকর্ড পর্যালোচনা রিডিংকে নির্ভরযোগ্য করে।",
 "excursion": "শুধু উদাহরণ: প্রভাবিত ব্যাচ আটকে ও আলাদা করে রাখা হয়, যাতে নথিভুক্ত সিদ্ধান্ত না হওয়া পর্যন্ত ভুলে সরবরাহ বা ব্যবহার না হয়।",
 "bangladesh": "শুধু উদাহরণ। DGDA-র ২০২৪ সালের Model Pharmacy নির্দেশিকায় তাপমাত্রা-সংবেদনশীল ওষুধ সংরক্ষণ ও সংরক্ষণ-তাপমাত্রা পর্যবেক্ষণের যাচাই আছে। এর অর্থ এই নয় যে প্রতিটি ওষুধ ২–৮°C-এ রাখতে হবে।",
 "advice": "শুধু উদাহরণ: পণ্যের সংরক্ষণ-নির্দেশনা অনুসরণ করুন; নির্দেশনায় না থাকলে ওষুধ রেফ্রিজারেটরে রাখবেন না।",
 "key": "শুধু উদাহরণ: validated শিপার ও কন্ডিশন্ড coolant পরিবহনে পণ্য রক্ষা করে, তবে সংরক্ষণের সীমা পণ্যভেদে আলাদা।",
}
def fn(k, lang): return f"cc-{k}" + ("" if lang == "en" else "-bn") + ".webp"
def fig(lang, key):
    A, C = (EN, CAP) if lang == "en" else (BN, BCAP)
    u = f"{IMG}{fn(key, lang)}{V}"
    cls = "pv-fig pv-key" if key == "key" else "pv-fig"
    return (f'<figure class="{cls}"><a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{esc(A[key])}" width="1600" height="900" loading="lazy" decoding="async"></a>'
            f'<figcaption class="caption">{esc(C[key])}</figcaption></figure>')
def after_para(h, sec, n, block):
    pos = h.index(f'<h2 id="{sec}"')
    for _ in range(n): pos = h.index("</p>", pos) + 4
    return h[:pos] + "\n" + block + h[pos:]
def after_h2(h, sec, block):
    p = h.index(f'<h2 id="{sec}"'); e = h.index("</h2>", p) + 5
    return h[:e] + "\n" + block + h[e:]
def process(lang):
    A = EN if lang == "en" else BN
    d = R / "blog" / (SLUG + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8")
    assert "pv-figures.css" not in h, "already applied"
    old = re.search(r'<link rel="stylesheet" href="/assets/site-polish\.css\?v=[^"]*">', h).group(0)
    h = h.replace(old, old + '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124">', 1)
    m = re.search(r'<figure class="hero-visual">.*?</figure>', h, re.S); assert m
    cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', m.group(0), re.S).group(1)
    u = f"{IMG}{fn('cover', lang)}{V}"
    h = h.replace(m.group(0), f'<figure class="hero-visual"><a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{esc(A["cover"])}" width="1600" height="900" fetchpriority="high" decoding="async"></a><figcaption>{cap}</figcaption></figure>')
    for key, sec in (("what", "what-is-cold-chain"), ("which", "which-medicines"), ("why", "why-temperature-matters"), ("how", "how-chain-works"),
                     ("monitor", "monitoring"), ("excursion", "excursion"), ("bangladesh", "bangladesh")):
        h = after_para(h, sec, 1, fig(lang, key))
    h = after_h2(h, "practical-advice", fig(lang, "advice"))
    h = after_h2(h, "key-takeaways", fig(lang, "key"))
    soc = f"{SITE}{IMG}cc-social-{lang}.jpg{V}"
    og_alt = ("Pharmaceutical cold chain: a gloved hand opens an insulated shipper holding glass vials (AI-generated photo-style image)." if lang == "en"
              else "ফার্মাসিউটিক্যাল কোল্ড চেইন: গ্লাভস পরা হাতে কাচের ভায়ালসহ ইনসুলেটেড শিপার খোলা হচ্ছে (AI-তৈরি ফটো-ধাঁচের ছবি)।")
    for pat in (r'(<meta property="og:image" content=")', r'(<meta property="og:image:secure_url" content=")', r'(<meta name="twitter:image" content=")'):
        h = re.sub(pat + r'[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:type" content=")[^"]*', r'\g<1>image/jpeg', h)
    h = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r'\g<1>1200', h)
    h = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r'\g<1>630', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap_, w, hh):
        u_ = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u_, "url": u_, "width": w, "height": hh, "caption": cap_, "creator": CRE,
                "creditText": "Sayedul Abrar (sayedulabrar.site)", "copyrightNotice": "© 2026 Sayedul Abrar. All rights reserved.", "acquireLicensePage": SITE + "/contact/"}
    def fix(m_):
        j = json.loads(m_.group(1))
        if j.get("@type") != "BlogPosting": return m_.group(0)
        keep = [o for o in j["image"] if o["contentUrl"].endswith(".svg") and "cold-chain-cover" not in o["contentUrl"]]
        j["image"] = [obj(f"cc-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(fn(k, lang), A[k], 1600, 900) for k in KEYS] + keep
        j["thumbnailUrl"] = SITE + IMG + "cc-card.webp"
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
    for mm_ in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(mm_)
    print(lang, "refs left to old cover:", h.count("cold-chain-cover"))
    d.write_text(h, encoding="utf-8")
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg); print("ok", lg)
