#!/usr/bin/env python3
"""Pharmacogenetics article (EN+BN): place the 10 photos with captions, update head tags and schema. The three bilingual SVG diagrams stay."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/pharmacogenetics/"; V = "?v=px-20261126"
SLUG = "pharmacogenetics-how-genes-affect-medicine-response"
def esc(s): return html.escape(s, quote=True)
KEYS = ["cover", "what", "same", "pathways", "types", "prodrug", "test", "care", "bangladesh", "key"]
EN = {
 "cover": "AI-generated photo-style image: a scientist's gloved hands hold a clear sample tube in front of a DNA sequencing machine with teal lights.",
 "what": "AI-generated photo-style image: a laboratory scientist in a mask and safety glasses holds up a small sample vial beside a screen showing a DNA helix.",
 "same": "AI-generated photo-style image: three open hands of different ages, each holding one identical white tablet.",
 "pathways": "AI-generated photo-style image: a brass padlock with one key in the lock and two other keys beside it, used as a metaphor for enzymes and medicines.",
 "types": "AI-generated photo-style image: three glasses of water with an effervescent tablet at different stages of dissolving, from fully dissolved to barely started.",
 "prodrug": "AI-generated photo-style image: a closed magnolia bud and an open flower on the same branch, with dew drops, as a metaphor for a medicine becoming active.",
 "test": "AI-generated photo-style image: gloved hands hold a clear collection tube with a cheek swab; a second tube lies on a tray in front of a DNA model.",
 "care": "AI-generated photo-style image: a hand lifts one of four fanned blister packs of tablets in yellow, pink, blue and white on a pharmacy counter.",
 "bangladesh": "AI-generated photo-style image: a pharmacist serving a customer through the lit front of a neighbourhood pharmacy on a Dhaka street at dusk, with rickshaws in the street.",
 "key": "AI-generated photo-style image: a doctor shows a patient coloured bars on a tablet during a calm consultation in a bright clinic.",
}
CAP = {
 "cover": "Genes can influence a medicine's journey and effect, but they are only one part of the clinical picture.",
 "what": "Pharmacogenetics connects pharmacology with genetics. The result is one part of precision medicine, not a replacement for clinical assessment.",
 "same": "Two people can take the same labelled dose and still differ in drug levels, benefit or side effects. Genes are one possible reason; age, organ function, diet, other medicines and adherence also matter.",
 "pathways": "Enzymes, transporters, drug targets and immune-related proteins are four ways genetic variation can influence a medicine. The lock and keys are only a metaphor.",
 "types": "Illustration only: tablets dissolving at different speeds stand for different predicted enzyme activity. Categories vary by gene, and a “poor” result does not always mean a stronger drug effect.",
 "prodrug": "A bud and an open flower illustrate activation. Clopidogrel is a prodrug, so reduced CYP2C19 function can mean less active metabolite. A clinician interprets this; never stop or change an antiplatelet medicine on your own.",
 "test": "A sample is usually blood, saliva or a cheek swab. A report should state which genes and variants were tested; not detecting a variant does not prove that every other variant is absent.",
 "care": "Illustration only. A result may support a different medicine, dose or monitoring in selected situations, and a clinician or pharmacist reads it with the whole patient context.",
 "bangladesh": "Ask the treating clinician and the laboratory these questions before any test. This article does not claim that a particular test is routinely available across Bangladesh.",
 "key": "Illustration only: genetic information is one part of care, discussed together with a clinician.",
}
BN = {
 "cover": "AI-তৈরি ফটো-ধাঁচের ছবি: গ্লাভস পরা হাতে স্বচ্ছ একটি নমুনার টিউব, পেছনে টিল আলোর DNA সিকোয়েন্সিং মেশিন।",
 "what": "AI-তৈরি ফটো-ধাঁচের ছবি: মাস্ক ও সেফটি চশমা পরা একজন ল্যাব-বিজ্ঞানী ছোট একটি নমুনার ভায়াল তুলে ধরেছেন; পাশের পর্দায় DNA হেলিক্স।",
 "same": "AI-তৈরি ফটো-ধাঁচের ছবি: ভিন্ন বয়সের তিনটি খোলা হাত, প্রতিটিতে একই রকম একটি সাদা ট্যাবলেট।",
 "pathways": "AI-তৈরি ফটো-ধাঁচের ছবি: পিতলের একটি তালায় একটি চাবি লাগানো, পাশে আরও দুটি চাবি; এনজাইম ও ওষুধের রূপক।",
 "types": "AI-তৈরি ফটো-ধাঁচের ছবি: তিন গ্লাস পানিতে ফিজি ট্যাবলেট ভিন্ন ভিন্ন পর্যায়ে গুলছে, পুরো গোলা থেকে সবে শুরু পর্যন্ত।",
 "prodrug": "AI-তৈরি ফটো-ধাঁচের ছবি: একই ডালে একটি বন্ধ ম্যাগনোলিয়া কুঁড়ি ও একটি ফোটা ফুল, শিশিরবিন্দুসহ; ওষুধ সক্রিয় হওয়ার রূপক।",
 "test": "AI-তৈরি ফটো-ধাঁচের ছবি: গ্লাভস পরা হাতে গালের swab-সহ স্বচ্ছ সংগ্রহ-টিউব; ট্রেতে আরেকটি টিউব, পেছনে DNA মডেল।",
 "care": "AI-তৈরি ফটো-ধাঁচের ছবি: ফার্মেসির কাউন্টারে হলুদ, গোলাপি, নীল ও সাদা ট্যাবলেটের চারটি ব্লিস্টার প্যাক সাজানো; একটি হাত একটি প্যাক তুলছে।",
 "bangladesh": "AI-তৈরি ফটো-ধাঁচের ছবি: ঢাকার সন্ধ্যার রাস্তায় পাড়ার এক ফার্মেসির আলোকিত সামনের কাচ দিয়ে ফার্মাসিস্ট ক্রেতাকে সেবা দিচ্ছেন; রাস্তায় রিকশা।",
 "key": "AI-তৈরি ফটো-ধাঁচের ছবি: উজ্জ্বল ক্লিনিকে শান্ত পরামর্শের সময় চিকিৎসক রোগীকে ট্যাবলেটে রঙিন বার দেখাচ্ছেন।",
}
BCAP = {
 "cover": "জিন ওষুধের যাত্রা ও প্রভাবে ভূমিকা রাখতে পারে, তবে এটি ক্লিনিক্যাল ছবির একটি অংশ মাত্র।",
 "what": "ফার্মাকোজেনেটিক্স ফার্মাকোলজি ও জেনেটিক্সকে যুক্ত করে। এর ফল precision medicine-এর একটি অংশ; ক্লিনিক্যাল মূল্যায়নের বিকল্প নয়।",
 "same": "দুজন মানুষ একই লেবেলের ডোজ নিলেও রক্তে ওষুধের মাত্রা, উপকার বা পার্শ্বপ্রতিক্রিয়া আলাদা হতে পারে। জিন একটি সম্ভাব্য কারণ; বয়স, অঙ্গের কার্যকারিতা, খাদ্য, অন্য ওষুধ ও নিয়মিত সেবনও গুরুত্বপূর্ণ।",
 "pathways": "এনজাইম, ট্রান্সপোর্টার, ওষুধের টার্গেট ও ইমিউন-সংক্রান্ত প্রোটিন—এই চারভাবে জেনেটিক পার্থক্য ওষুধকে প্রভাবিত করতে পারে। তালা ও চাবি শুধু একটি রূপক।",
 "types": "শুধু উদাহরণ: ভিন্ন গতিতে গুলে যাওয়া ট্যাবলেট ভিন্ন predicted এনজাইম-কার্যকারিতার প্রতীক। ধরন জিনভেদে আলাদা, আর “poor” ফলের অর্থ সবসময় ওষুধের প্রভাব বেশি—এমন নয়।",
 "prodrug": "কুঁড়ি ও ফোটা ফুল সক্রিয় হওয়ার ধারণা বোঝায়। Clopidogrel একটি prodrug, তাই CYP2C19-এর কার্যকারিতা কম হলে সক্রিয় metabolite কম তৈরি হতে পারে। এর ব্যাখ্যা চিকিৎসকের কাজ; নিজে থেকে antiplatelet ওষুধ বন্ধ বা বদলাবেন না।",
 "test": "নমুনা সাধারণত রক্ত, লালা বা গালের swab। রিপোর্টে কোন জিন ও variant পরীক্ষা হয়েছে তা থাকা উচিত; কোনো variant না পাওয়া মানে অন্য সব variant নেই—এমন প্রমাণ নয়।",
 "care": "শুধু উদাহরণ। কিছু ক্ষেত্রে ফল ভিন্ন ওষুধ, ডোজ বা পর্যবেক্ষণে সহায়ক হতে পারে; চিকিৎসক বা ফার্মাসিস্ট রোগীর সামগ্রিক অবস্থার সঙ্গে মিলিয়ে তা ব্যাখ্যা করেন।",
 "bangladesh": "যেকোনো পরীক্ষার আগে চিকিৎসক ও ল্যাবরেটরিকে এই প্রশ্নগুলো করুন। এই লেখা দাবি করে না যে নির্দিষ্ট কোনো পরীক্ষা বাংলাদেশে সর্বত্র নিয়মিত পাওয়া যায়।",
 "key": "শুধু উদাহরণ: জেনেটিক তথ্য চিকিৎসার একটি অংশ, যা চিকিৎসকের সঙ্গে আলোচনা করে বোঝা উচিত।",
}
def fn(k, lang): return f"px-{k}" + ("" if lang == "en" else "-bn") + ".webp"
def fig(lang, key, lazy=True):
    A, C = (EN, CAP) if lang == "en" else (BN, BCAP)
    u = f"{IMG}{fn(key, lang)}{V}"
    cls = "pv-fig pv-key" if key == "key" else "pv-fig"
    return (f'<figure class="{cls}"><a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{esc(A[key])}" width="1600" height="900" '
            f'{"loading=\"lazy\" " if lazy else ""}decoding="async"></a><figcaption class="caption">{esc(C[key])}</figcaption></figure>')
def after_para(h, sec, n, block):
    pos = h.index(f'<h2 id="{sec}"')
    for _ in range(n): pos = h.index("</p>", pos) + 4
    return h[:pos] + "\n" + block + h[pos:]
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
    cover = (f'<figure class="hero-visual"><a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{esc(A["cover"])}" width="1600" height="900" fetchpriority="high" decoding="async"></a>'
             f'<figcaption>{cap}</figcaption></figure>')
    h = h.replace(m.group(0), cover)
    h = after_para(h, "s1", 3, fig(lang, "same"))
    h = after_para(h, "s1", 1, fig(lang, "what"))
    h = after_para(h, "s2", 1, fig(lang, "pathways"))
    h = after_para(h, "s3", 2, fig(lang, "types"))
    p = h.index('<h2 id="s4"'); p = h.index("<h3>", p); pos = h.index("</p>", p) + 4
    h = h[:pos] + "\n" + fig(lang, "prodrug") + h[pos:]
    h = after_para(h, "s5", 1, fig(lang, "test"))
    h = after_para(h, "s6", 1, fig(lang, "care"))
    h = after_para(h, "s7", 1, fig(lang, "bangladesh"))
    p = h.index('<h2 id="takeaways"'); e = h.index("</h2>", p) + 5
    h = h[:e] + "\n" + fig(lang, "key") + h[e:]
    soc = f"{SITE}{IMG}px-social-{lang}.jpg{V}"
    og_alt = ("Pharmacogenetics: gloved hands holding a sample tube in front of a DNA sequencing machine (AI-generated photo-style image)." if lang == "en"
              else "ফার্মাকোজেনেটিক্স: DNA সিকোয়েন্সিং মেশিনের সামনে নমুনার টিউব হাতে (AI-তৈরি ফটো-ধাঁচের ছবি)।")
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
        keep = [o for o in j["image"] if o["contentUrl"].endswith(".svg") and "pgx-cover" not in o["contentUrl"]]
        j["image"] = [obj(f"px-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(fn(k, lang), A[k], 1600, 900) for k in KEYS] + keep
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
    for mm_ in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(mm_)
    print(lang, "svg refs left:", sorted(set(re.findall(r'[^"]*\.svg', h))))
    d.write_text(h, encoding="utf-8")
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg); print("ok", lg)
