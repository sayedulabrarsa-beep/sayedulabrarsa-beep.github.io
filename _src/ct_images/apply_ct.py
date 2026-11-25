#!/usr/bin/env python3
"""Clinical Trial Phases article (EN+BN): place the 10 pictures with legends/captions written in code, update head and schema."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/clinical-trial-phases/"; V = "?v=ct-20261125"
def esc(s): return html.escape(s, quote=True)
EN = {
 "cover": ("A glowing glass staircase with a white capsule on its first step, set against a teal wall and green plant in warm light.",
           "Clinical trial phases: each step answers a different research question.", None, []),
 "questions": ("A stethoscope and teal clipboard on a wooden desk beside a white capsule and a row of glowing gold stepping stones.",
               "The emphasis changes from early safety to confirmation and post-approval follow-up, but safety remains important throughout.", "ol",
               [("Phase I", "safety, tolerability and dose"), ("Phase II", "early activity in people with the condition"), ("Phase III", "larger-scale confirmation of benefit and risk"), ("Phase IV", "planned studies after marketing authorisation")]),
 "preclinical": ("A gloved hand adjusts a microscope beside a conical flask, a red petri dish and a rack of test tubes holding teal liquid.",
                 "Laboratory and non-clinical studies come before the first human study. They cannot predict every human response.", "ul",
                 [("Non-clinical evidence", "pharmacology, toxicology and safety pharmacology"), ("Product information", "how the medicine is made and controlled"), ("A clinical protocol", "question, eligibility, dose, monitoring and rules for stopping")]),
 "phase1": ("A quiet hospital ward with made beds, bedside monitors and teal curtains, with a clipboard, pen and glass of water in the foreground.",
            "Phase I is usually the first carefully monitored exposure of people to an investigational medicine.", "ul",
            [("The questions", "how the body handles it, what dose is tolerated, what short-term effects appear"), ("PK and PD", "what the body does to the medicine, and what it does to the body"), ("Participants", "often healthy volunteers, but not in every case")]),
 "phase2": ("A gloved hand holds a blister pack of white capsules above a clipboard and stethoscope, with a treatment chair behind.",
            "Phase II generally moves into people who have the condition, looking for an early sign of activity while still studying safety.", "ul",
            [("Who takes part", "people who have the condition the medicine is meant to treat"), ("What is explored", "doses, schedules and early signs of activity"), ("Not final proof", "small studies can give uncertain estimates")]),
 "phase3": ("Rows of white medicine boxes with teal and coral stripes stretch down a bright laboratory corridor.",
            "Phase III trials usually involve larger and more varied groups of participants.", "ul",
            [("Confirm", "benefits, and further describe risks"), ("Compare", "with an appropriate control, such as standard treatment or placebo when ethically suitable"), ("Still limited", "rare or very long-term problems may not appear before approval")]),
 "regulatory": ("A teal document binder tied with a gold ribbon and red wax seal, with a glowing tick above it, beside a glass sphere, a pen and golden scales.",
                "Regulatory review looks at the whole application, not only the phase labels.", "ul",
                [("The whole package", "quality, manufacturing, non-clinical and clinical evidence, proposed use and labelling"), ("Possible outcomes", "approve for a defined use, ask for more information, require further studies, restrict or refuse"), ("A positive Phase III", "does not automatically mean approval in every country")]),
 "phase4": ("Gloved hands place a white medicine box on a pharmacy shelf of identical boxes, with a glowing lamp in the background.",
            "Phase IV studies take place after marketing authorisation. Approval is not the end of learning about a medicine.", "ul",
            [("After authorisation", "longer-term safety, broader populations and routine use"), ("Planned studies", "Phase IV is not identical with pharmacovigilance"), ("Wider system", "pharmacovigilance also uses spontaneous reports and safety databases")]),
 "safeguards": ("A glass shield with a group-of-people symbol stands on a clipboard and pen, beside a stethoscope.",
                "A well-designed trial protects people while producing evidence that can be trusted.", "ol",
                [("Independent ethics review", "of the protocol and consent materials"), ("Informed consent", "understandable information before deciding"), ("Voluntary choice", "refuse or withdraw without penalty"), ("Ongoing safety monitoring", "adverse events assessed and reported"), ("Confidentiality", "protected identity and reliable records")]),
 "key": ("White steps rise like a staircase with a capsule on the top step, beside a stethoscope in warm window light.",
         "Seven ideas to take away.", None, []),
}
BN = {
 "cover": ("উজ্জ্বল কাচের সিঁড়ির প্রথম ধাপে একটি সাদা ক্যাপসুল; পেছনে টিল রঙের দেয়াল ও সবুজ গাছ, উষ্ণ আলো।",
           "ক্লিনিক্যাল ট্রায়ালের phase: প্রতিটি ধাপ আলাদা গবেষণা-প্রশ্নের উত্তর খোঁজে।", None, []),
 "questions": ("কাঠের টেবিলে স্টেথোস্কোপ ও টিল রঙের ক্লিপবোর্ড; পাশে একটি সাদা ক্যাপসুল ও সোনালি আলোয় জ্বলজ্বলে একসারি পাথরের ধাপ।",
               "জোর বদলে যায় প্রাথমিক নিরাপত্তা থেকে নিশ্চিতকরণ ও অনুমোদন-পরবর্তী পর্যবেক্ষণে, তবে নিরাপত্তা সব ধাপেই গুরুত্বপূর্ণ।", "ol",
               [("Phase I", "নিরাপত্তা, সহনশীলতা ও ডোজ"), ("Phase II", "যাঁদের রোগটি আছে, তাঁদের মধ্যে প্রাথমিক কার্যকারিতা"), ("Phase III", "বড় পরিসরে উপকার ও ঝুঁকির নিশ্চিতকরণ"), ("Phase IV", "marketing authorisation-এর পর পরিকল্পিত গবেষণা")]),
 "preclinical": ("গ্লাভস পরা একটি হাত মাইক্রোস্কোপ ঠিক করছে; পাশে কনিক্যাল ফ্লাস্ক, লাল পেট্রি ডিশ এবং টিল রঙের তরলভরা টেস্ট টিউবের র‍্যাক।",
                 "প্রথম মানব-পরীক্ষার আগে আসে ল্যাবরেটরি ও non-clinical গবেষণা। এগুলো মানুষের সব প্রতিক্রিয়া আগে থেকে বলে দিতে পারে না।", "ul",
                 [("Non-clinical প্রমাণ", "ফার্মাকোলজি, টক্সিকোলজি ও safety pharmacology"), ("পণ্যের তথ্য", "ওষুধটি কীভাবে তৈরি ও নিয়ন্ত্রিত হয়"), ("ক্লিনিক্যাল protocol", "গবেষণা-প্রশ্ন, যোগ্যতা, ডোজ, পর্যবেক্ষণ ও থামানোর নিয়ম")]),
 "phase1": ("শান্ত হাসপাতাল-ওয়ার্ড: সাজানো বিছানা, বেডসাইড মনিটর ও টিল রঙের পর্দা; সামনে ক্লিপবোর্ড, কলম ও এক গ্লাস পানি।",
            "Phase I সাধারণত গবেষণাধীন ওষুধের সঙ্গে মানুষের প্রথম, সতর্কভাবে পর্যবেক্ষিত সংস্পর্শ।", "ul",
            [("মূল প্রশ্ন", "শরীর ওষুধটি কীভাবে সামলায়, কোন ডোজ সহনীয় এবং স্বল্পমেয়াদে কী প্রভাব দেখা যায়"), ("PK ও PD", "শরীর ওষুধের ওপর কী করে এবং ওষুধ শরীরের ওপর কী করে"), ("অংশগ্রহণকারী", "অনেক সময় সুস্থ স্বেচ্ছাসেবক, তবে সব ক্ষেত্রে নয়")]),
 "phase2": ("গ্লাভস পরা একটি হাত সাদা ক্যাপসুলের ব্লিস্টার প্যাক ধরে আছে; নিচে ক্লিপবোর্ড ও স্টেথোস্কোপ, পেছনে চিকিৎসার চেয়ার।",
            "Phase II সাধারণত যাঁদের রোগটি আছে তাঁদের মধ্যে চলে; নিরাপত্তা দেখার পাশাপাশি কার্যকারিতার প্রাথমিক সংকেত খোঁজা হয়।", "ul",
            [("কারা অংশ নেন", "ওষুধটি যে রোগের জন্য, সেই রোগ আছে এমন মানুষ"), ("কী দেখা হয়", "ডোজ, সময়সূচি ও কার্যকারিতার প্রাথমিক সংকেত"), ("চূড়ান্ত প্রমাণ নয়", "ছোট গবেষণায় অনুমান অনিশ্চিত হতে পারে")]),
 "phase3": ("উজ্জ্বল ল্যাবরেটরি-করিডরে সাদা ওষুধের বাক্সের সারি; বাক্সে টিল ও প্রবাল রঙের ডোরা।",
            "Phase III ট্রায়ালে সাধারণত বড় ও আরও বৈচিত্র্যময় অংশগ্রহণকারী-দল থাকে।", "ul",
            [("নিশ্চিত করা", "উপকার, এবং ঝুঁকির আরও বিবরণ"), ("তুলনা", "উপযুক্ত control-এর সঙ্গে, যেমন প্রচলিত চিকিৎসা বা নৈতিকভাবে উপযুক্ত হলে placebo"), ("তবু সীমিত", "বিরল বা খুব দীর্ঘমেয়াদি সমস্যা অনুমোদনের আগে ধরা নাও পড়তে পারে")]),
 "regulatory": ("সোনালি ফিতা ও লাল মোমের সিলে বাঁধা টিল রঙের নথির ফাইল, ওপরে জ্বলজ্বলে টিক-চিহ্ন; পাশে কাচের গোলক, কলম ও সোনালি দাঁড়িপাল্লা।",
                "Regulatory review শুধু phase-এর নাম নয়, সম্পূর্ণ আবেদন বিবেচনা করে।", "ul",
                [("সম্পূর্ণ তথ্যভান্ডার", "মান, উৎপাদন, non-clinical ও ক্লিনিক্যাল প্রমাণ, প্রস্তাবিত ব্যবহার ও লেবেলিং"), ("সম্ভাব্য ফল", "নির্দিষ্ট ব্যবহারের জন্য অনুমোদন, আরও তথ্য চাওয়া, আরও গবেষণা চাওয়া, সীমিত করা বা প্রত্যাখ্যান"), ("Phase III-এর ইতিবাচক ফল", "প্রতিটি দেশে স্বয়ংক্রিয়ভাবে অনুমোদন বোঝায় না")]),
 "phase4": ("গ্লাভস পরা হাত ফার্মেসির তাকে একই রকম বাক্সের সারিতে একটি সাদা ওষুধের বাক্স রাখছে; পেছনে জ্বলজ্বলে বাতি।",
            "Phase IV গবেষণা হয় marketing authorisation-এর পর। অনুমোদনে ওষুধ সম্পর্কে শেখা শেষ হয় না।", "ul",
            [("অনুমোদনের পর", "দীর্ঘমেয়াদি নিরাপত্তা, বৃহত্তর জনগোষ্ঠী ও নিয়মিত ব্যবহার"), ("পরিকল্পিত গবেষণা", "Phase IV আর pharmacovigilance হুবহু এক নয়"), ("বৃহত্তর ব্যবস্থা", "Pharmacovigilance-এ spontaneous report ও safety database-ও ব্যবহৃত হয়")]),
 "safeguards": ("একটি কাচের ঢালে একদল মানুষের প্রতীক, ঢালটি ক্লিপবোর্ড ও কলমের ওপর দাঁড়ানো; পাশে স্টেথোস্কোপ।",
                "ভালোভাবে নকশা করা ট্রায়াল মানুষকে রক্ষা করে এবং নির্ভরযোগ্য প্রমাণও তৈরি করে।", "ol",
                [("স্বাধীন ethics review", "protocol ও সম্মতিপত্রের"), ("Informed consent", "সিদ্ধান্তের আগে সহজবোধ্য তথ্য"), ("স্বেচ্ছায় সিদ্ধান্ত", "শাস্তি ছাড়াই অংশ না নেওয়া বা সরে আসা"), ("চলমান নিরাপত্তা পর্যবেক্ষণ", "adverse event মূল্যায়ন ও রিপোর্ট"), ("গোপনীয়তা", "পরিচয় সুরক্ষিত ও নির্ভরযোগ্য নথি")]),
 "key": ("সাদা ধাপগুলো সিঁড়ির মতো উঠে গেছে, সবচেয়ে ওপরের ধাপে একটি ক্যাপসুল; পাশে জানালার উষ্ণ আলোয় একটি স্টেথোস্কোপ।",
         "মনে রাখার মতো সাতটি কথা।", None, []),
}
FILES = {k: f"ct-{k}" for k in EN}
def fn(k, lang): return FILES[k] + ("" if lang == "en" else "-bn") + ".webp"
def fig(L, lang, key, lazy=True):
    alt, cap, kind, items = L[key]
    cls = "pv-fig pv-key" if key == "key" else "pv-fig"
    img = f'<img src="{IMG}{fn(key, lang)}{V}" alt="{esc(alt)}" width="1600" height="900" {"loading=\"lazy\" " if lazy else ""}decoding="async">'
    leg = ""
    if kind:
        tag = "ol" if kind == "ol" else "ul"
        leg = f'<{tag} class="pv-legend">' + "".join(f"<li><div><b>{esc(t)}</b>" + (f"<span>{esc(d)}</span>" if d else "") + "</div></li>" for t, d in items) + f"</{tag}>"
    return f'<figure class="{cls}">{img}{leg}<figcaption class="caption">{esc(cap)}</figcaption></figure>'
def after_para(h, sec, n, block):
    pos = h.index(f'<h2 id="{sec}"')
    for _ in range(n): pos = h.index("</p>", pos) + 4
    return h[:pos] + "\n" + block + h[pos:]
def process(lang):
    L = EN if lang == "en" else BN
    d = R / "blog" / ("clinical-trial-phases-explained" + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8")
    assert "pv-figures.css" not in h, "already applied"
    old = '<link rel="stylesheet" href="/assets/site-polish.css?v=sa-20261122">'; assert old in h
    h = h.replace(old, old + '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124">', 1)
    m = re.search(r'<figure class="hero-visual">.*?</figure>', h, re.S); assert m
    cap = re.search(r'<figcaption class="caption">(.*?)</figcaption>', m.group(0), re.S).group(1)
    cover = (f'<figure class="hero-visual"><a href="{IMG}{fn("cover", lang)}{V}" target="_blank" rel="noopener"><img src="{IMG}{fn("cover", lang)}{V}" alt="{esc(L["cover"][0])}" width="1600" height="900" fetchpriority="high" decoding="async"></a>'
             f'<figcaption class="caption">{cap}</figcaption></figure>')
    h = h.replace(m.group(0), cover)
    for svg, key in (("clinical-trial-phases-questions.svg", "questions"), ("clinical-trial-participant-safeguards.svg", "safeguards")):
        mm = re.search(r'<figure class="article-figure"><a href="[^"]*' + re.escape(svg) + r'".*?</figure>', h, re.S); assert mm, svg
        h = h.replace(mm.group(0), fig(L, lang, key))
    h = after_para(h, "s2", 1, fig(L, lang, "preclinical"))
    h = after_para(h, "s3", 1, fig(L, lang, "phase1"))
    h = after_para(h, "s4", 1, fig(L, lang, "phase2"))
    h = after_para(h, "s5", 1, fig(L, lang, "phase3"))
    h = after_para(h, "s6", 1, fig(L, lang, "regulatory"))
    h = after_para(h, "s7", 1, fig(L, lang, "phase4"))
    p = h.index('<h2 id="key-takeaways"'); e = h.index("</h2>", p) + 5
    h = h[:e] + "\n" + fig(L, lang, "key") + h[e:]
    soc = f"{SITE}{IMG}ct-social-{lang}.jpg{V}"
    og_alt = ("Clinical Trial Phases Explained: a glowing glass staircase with a white capsule on the first step." if lang == "en"
              else "ক্লিনিক্যাল ট্রায়ালের ধাপগুলো: উজ্জ্বল কাচের সিঁড়ির প্রথম ধাপে একটি সাদা ক্যাপসুল।")
    for pat in (r'(<meta property="og:image" content=")', r'(<meta property="og:image:secure_url" content=")', r'(<meta name="twitter:image" content=")'):
        h = re.sub(pat + r'[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:type" content=")[^"]*', r'\g<1>image/jpeg', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap_, w, hh):
        u = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": hh, "caption": cap_, "creator": CRE,
                "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    lst = [obj(f"ct-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(fn(k, lang), L[k][0], 1600, 900) for k in FILES]
    h, n = re.subn(r'"image":\[[^\]]*\]', lambda _: '"image":' + json.dumps(lst, ensure_ascii=False, separators=(",", ":")), h, count=1); assert n == 1
    left = sorted(set(re.findall(r'[^"]*\.svg', h))); print(lang, "svg left:", left)
    for mm_ in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(mm_)
    d.write_text(h, encoding="utf-8")
if __name__ == "__main__":
    for lg in ("en", "bn"): process(lg); print("ok", lg)
