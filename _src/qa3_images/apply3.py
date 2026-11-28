#!/usr/bin/env python3
"""Place the 18 pictures in Regulatory Inspections, OOS Results and Paracetamol Safety (EN+BN): hero/figures, og/twitter, BlogPosting images, pv-figures.css."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; V = "?v=q3-20261128"
def esc(s): return html.escape(s, quote=True)
AI_EN = " AI-generated photo-style illustration."; AI_BN = " AI-তৈরি ছবি-ধাঁচের চিত্র।"
ART = {
 "ri": dict(slug="pharmaceutical-regulatory-inspections-what-inspectors-check", dir="regulatory-inspections", pre="ri", order=["cover", "what", "types", "check", "during", "capa"],
   secs={"meaning": "what", "risk": "types", "scope": "check", "process": "during", "findings": "capa"}),
 "oos": dict(slug="out-of-specification-oos-results-pharma-investigation", dir="oos-investigation", pre="oos", order=["cover", "terms", "causes", "investigation", "retest", "decision"],
   secs={"oos-oot-deviation": "terms", "why-oos-happens": "causes", "investigation": "investigation", "retesting-resampling": "retest", "batch-disposition": "decision"}),
 "pc": dict(slug="paracetamol-safety-and-proper-use", dir="paracetamol-safety", pre="pc", order=["cover", "label", "double", "children", "liver", "help"],
   idx={1: "label", 2: "double", 3: "children", 5: "liver", 7: "help"}),
}
EN = {
 ("ri", "cover"): ("Two pharmaceutical regulatory inspectors in white coats, hairnets and shoe covers walk through a clean production corridor beside tablet-manufacturing equipment.", "Pharmaceutical regulatory inspections: inspectors check whether real practice, premises and records match approved requirements."),
 ("ri", "what"): ("A pharmaceutical inspector in gloves and a mask ticks a blank checklist beside a stainless-steel tablet press during a regulatory inspection.", "A regulatory inspection is a structured check of premises, people and records against requirements, based on evidence."),
 ("ri", "types"): ("A quality professional reviews a facility floor plan, a report and a performance chart at a desk while planning a risk-based pharmaceutical inspection.", "Risk-based planning directs inspection effort to the sites and products where the risk to patients is higher."),
 ("ri", "check"): ("A pharmaceutical quality inspector in gloves reviews batch-record binders and papers at a laboratory bench with glassware and pipettes.", "Inspectors compare batch records, equipment, laboratory data and the quality system with what actually happens on site."),
 ("ri", "during"): ("Inspectors and company staff in white coats and hairnets discuss documents and binders around a stainless-steel table in front of a production area.", "During a visit: an opening meeting, a site walk-through, document review and a closing meeting with feedback."),
 ("ri", "capa"): ("A quality manager ticks items on a checklist with a green pen while a colleague watches, with warehouse racks behind, during inspection finding follow-up.", "Good CAPA fixes the root cause of an inspection finding, not only the finding, and tracks every action to closure."),
 ("oos", "cover"): ("A quality-control analyst in a lab coat, gloves and safety glasses reads a printed result beside an HPLC system while investigating an out-of-specification (OOS) result.", "An out-of-specification (OOS) result starts an investigation: check the laboratory first, document every step and decide on evidence."),
 ("oos", "terms"): ("Three sealed laboratory sample vials in a rack, the middle one containing pink liquid, with glassware and a microscope behind, illustrating OOS, OOT and deviation.", "OOS fails the specification, OOT is an unusual trend and a deviation departs from an approved procedure: three different terms."),
 ("oos", "causes"): ("A gloved hand pipettes blue liquid into a volumetric flask beside an analytical balance and a notebook in a pharmaceutical quality-control laboratory.", "An OOS result may come from an analyst or method error, an instrument or sample issue, or a real problem with the batch."),
 ("oos", "investigation"): ("Three laboratory colleagues in white coats review a record binder and a notebook beside an HPLC instrument during an OOS laboratory investigation.", "An OOS investigation starts with the laboratory phase, reviews records and data, and extends to production only when needed."),
 ("oos", "retest"): ("An analyst pipettes a sample into vials in a rack next to two labelled sample bottles and a retest and resample checklist.", "Retesting and resampling must follow the written procedure for a documented reason, never to test into compliance."),
 ("oos", "decision"): ("A quality professional writes on a clipboard beside a laptop showing a tick-list while sample bottles stand on the laboratory bench during batch disposition.", "The quality unit decides the batch disposition from complete evidence, then root cause and CAPA prevent repeats."),
 ("pc", "cover"): ("Paracetamol tablets and capsules beside a clear glass vial, test tubes and a microscope on a laboratory bench, introducing paracetamol safety.", "Paracetamol safety: read the label, stay within the labelled limit, take care with children and know when to seek help."),
 ("pc", "label"): ("A person holds a paracetamol 500 mg medicine box and points to its label, with a glass of water and a blister strip on the table.", "Read the label of every pack: active ingredient and strength, the dose and interval stated, and the daily limit it gives."),
 ("pc", "double"): ("A brown paracetamol bottle, a cold and flu box and a fever relief box under a magnifying glass with a warning triangle, showing hidden paracetamol.", "Many cold, flu and fever products contain paracetamol, so check every label and add up all sources to avoid double dosing."),
 ("pc", "children"): ("A mother and her young son listen to a smiling doctor who holds a bottle of children's liquid medicine beside a measuring cup and an oral syringe.", "Children need extra care with paracetamol: use a product made for children, measure with the supplied device and follow the label or professional advice."),
 ("pc", "liver"): ("An X-ray style body figure with a glowing liver and intestines beside an open bottle with paracetamol tablets spilling onto a table.", "Taking too much paracetamol can harm the liver; stay within the labelled limit and ask first if you have a liver condition."),
 ("pc", "help"): ("A man holding his abdomen in discomfort explains his symptoms to a doctor who notes them on a clipboard in a clinic.", "Seek urgent help for a possible paracetamol overdose, and ask a doctor or pharmacist if fever or pain continues."),
}
BN = {
 ("ri", "cover"): ("সাদা কোট, হেয়ারনেট ও জুতার কভার পরা দুজন ফার্মাসিউটিক্যাল রেগুলেটরি ইন্সপেক্টর ট্যাবলেট তৈরির যন্ত্রের পাশে পরিচ্ছন্ন উৎপাদন করিডরে হাঁটছেন।", "ফার্মাসিউটিক্যাল রেগুলেটরি ইন্সপেকশনে পরিদর্শকেরা দেখেন বাস্তব কাজ, প্রাঙ্গণ ও নথি অনুমোদিত প্রয়োজনের সঙ্গে মিলছে কি না।"),
 ("ri", "what"): ("গ্লাভস ও মাস্ক পরা একজন ফার্মাসিউটিক্যাল ইন্সপেক্টর রেগুলেটরি ইন্সপেকশনের সময় স্টেইনলেস-স্টিল ট্যাবলেট প্রেসের পাশে একটি ফাঁকা চেকলিস্টে টিক দিচ্ছেন।", "রেগুলেটরি ইন্সপেকশন হলো প্রাঙ্গণ, মানুষ ও নথিকে প্রয়োজনীয় মানের সঙ্গে প্রমাণের ভিত্তিতে মিলিয়ে দেখার কাঠামোবদ্ধ যাচাই।"),
 ("ri", "types"): ("ঝুঁকিভিত্তিক ফার্মাসিউটিক্যাল ইন্সপেকশনের পরিকল্পনার সময় একজন কোয়ালিটি পেশাজীবী ডেস্কে কারখানার ফ্লোর প্ল্যান, একটি প্রতিবেদন ও একটি চার্ট দেখছেন।", "ঝুঁকিভিত্তিক পরিকল্পনায় ইন্সপেকশনের মনোযোগ যায় সেই সাইট ও পণ্যে, যেখানে রোগীর জন্য ঝুঁকি বেশি।"),
 ("ri", "check"): ("গ্লাভস পরা একজন ফার্মাসিউটিক্যাল কোয়ালিটি ইন্সপেক্টর কাচের সরঞ্জাম ও পিপেটসহ ল্যাবরেটরির টেবিলে ব্যাচ রেকর্ডের বাইন্ডার ও কাগজ দেখছেন।", "ইন্সপেক্টররা ব্যাচ রেকর্ড, যন্ত্রপাতি, ল্যাবরেটরির ডেটা ও মান ব্যবস্থাকে সাইটে বাস্তবে যা ঘটে তার সঙ্গে মেলান।"),
 ("ri", "during"): ("সাদা কোট ও হেয়ারনেট পরা ইন্সপেক্টর ও কোম্পানির কর্মীরা উৎপাদন এলাকার সামনে স্টেইনলেস-স্টিলের টেবিলে নথি ও বাইন্ডার নিয়ে আলোচনা করছেন।", "পরিদর্শনের সময়: শুরুর সভা, সাইট ঘুরে দেখা, নথি পর্যালোচনা এবং মতামতসহ শেষ সভা।"),
 ("ri", "capa"): ("ইন্সপেকশনের পর্যবেক্ষণ অনুসরণের সময় পেছনে গুদামের তাকসহ একজন কোয়ালিটি ম্যানেজার সবুজ কলমে চেকলিস্টে টিক দিচ্ছেন, পাশে একজন সহকর্মী দেখছেন।", "ভালো CAPA শুধু পর্যবেক্ষণ নয়, তার মূল কারণ ঠিক করে এবং প্রতিটি পদক্ষেপ শেষ পর্যন্ত অনুসরণ করে।"),
 ("oos", "cover"): ("আউট-অব-স্পেসিফিকেশন (OOS) ফলাফল তদন্তের সময় ল্যাব কোট, গ্লাভস ও সেফটি গগলস পরা একজন কোয়ালিটি-কন্ট্রোল বিশ্লেষক HPLC যন্ত্রের পাশে মুদ্রিত ফলাফল পড়ছেন।", "OOS ফলাফল তদন্তের শুরু: আগে ল্যাবরেটরি যাচাই করুন, প্রতিটি ধাপ লিপিবদ্ধ করুন এবং প্রমাণের ভিত্তিতে সিদ্ধান্ত নিন।"),
 ("oos", "terms"): ("র‍্যাকে রাখা তিনটি সিল করা ল্যাব নমুনা-শিশি, মাঝেরটিতে গোলাপি তরল; পেছনে কাচের সরঞ্জাম ও মাইক্রোস্কোপ; OOS, OOT ও deviation বোঝাতে।", "OOS মানে স্পেসিফিকেশনে ব্যর্থ, OOT মানে অস্বাভাবিক প্রবণতা এবং deviation মানে অনুমোদিত পদ্ধতি থেকে বিচ্যুতি: তিনটি আলাদা শব্দ।"),
 ("oos", "causes"): ("ফার্মাসিউটিক্যাল কোয়ালিটি-কন্ট্রোল ল্যাবরেটরিতে বিশ্লেষণ-নিক্তি ও নোটবুকের পাশে গ্লাভস পরা হাত ভলিউমেট্রিক ফ্লাস্কে নীল তরল পিপেট করছে।", "OOS ফলাফলের কারণ হতে পারে বিশ্লেষক বা পদ্ধতির ত্রুটি, যন্ত্র বা নমুনার সমস্যা, অথবা ব্যাচেরই প্রকৃত সমস্যা।"),
 ("oos", "investigation"): ("OOS ল্যাবরেটরি তদন্তের সময় HPLC যন্ত্রের পাশে সাদা কোট পরা তিনজন সহকর্মী রেকর্ড বাইন্ডার ও নোটবুক দেখছেন।", "OOS তদন্ত শুরু হয় ল্যাবরেটরি পর্যায় দিয়ে, রেকর্ড ও ডেটা পর্যালোচনা করে এবং প্রয়োজন হলে উৎপাদন পর্যন্ত বিস্তৃত হয়।"),
 ("oos", "retest"): ("একজন বিশ্লেষক র‍্যাকের শিশিতে নমুনা পিপেট করছেন; পাশে দুটি লেবেল-করা নমুনার বোতল এবং পুনঃপরীক্ষা ও পুনঃনমুনার চেকলিস্ট।", "পুনঃপরীক্ষা ও পুনঃনমুনা হবে লিখিত পদ্ধতি মেনে, নথিবদ্ধ কারণে; শুধু পাস করানোর জন্য নয়।"),
 ("oos", "decision"): ("ব্যাচ নিষ্পত্তির সময় একজন কোয়ালিটি পেশাজীবী ক্লিপবোর্ডে লিখছেন; পাশে টিক-তালিকা দেখানো ল্যাপটপ ও ল্যাব বেঞ্চে নমুনার বোতল।", "সম্পূর্ণ প্রমাণ দেখে কোয়ালিটি ইউনিট ব্যাচের সিদ্ধান্ত নেয়; এরপর মূল কারণ ও CAPA পুনরাবৃত্তি রোধ করে।"),
 ("pc", "cover"): ("ল্যাবরেটরি বেঞ্চে স্বচ্ছ কাচের শিশি, টেস্ট টিউব ও মাইক্রোস্কোপের পাশে প্যারাসিটামল ট্যাবলেট ও ক্যাপসুল; প্যারাসিটামল নিরাপত্তার ভূমিকা।", "প্যারাসিটামল নিরাপত্তা: লেবেল পড়ুন, লেবেলের সীমার মধ্যে থাকুন, শিশুদের বেলায় বাড়তি সতর্ক হোন এবং কখন সাহায্য নেবেন তা জানুন।"),
 ("pc", "label"): ("একজন প্যারাসিটামল ৫০০ মি.গ্রা. ওষুধের বাক্স ধরে তার লেবেল দেখাচ্ছেন; টেবিলে এক গ্লাস পানি ও একটি ব্লিস্টার স্ট্রিপ।", "প্রতিটি প্যাকের লেবেল পড়ুন: সক্রিয় উপাদান ও শক্তি, লেখা ডোজ ও বিরতি এবং উল্লেখিত দৈনিক সীমা।"),
 ("pc", "double"): ("বাদামি প্যারাসিটামল বোতল, ঠান্ডা-ফ্লুর বাক্স ও জ্বর-উপশমের বাক্স; সতর্কতা-ত্রিভুজসহ ম্যাগনিফাইং গ্লাসে লুকানো প্যারাসিটামল দেখানো হচ্ছে।", "অনেক ঠান্ডা, ফ্লু ও জ্বরের ওষুধে প্যারাসিটামল থাকে; তাই প্রতিটি লেবেল দেখুন এবং সব উৎস মিলিয়ে হিসাব রাখুন, যাতে দ্বিগুণ ডোজ না হয়।"),
 ("pc", "children"): ("একজন মা ও তাঁর ছোট ছেলে হাসিমুখ চিকিৎসকের কথা শুনছে; চিকিৎসকের হাতে শিশুদের তরল ওষুধের বোতল, পাশে মাপার কাপ ও ওরাল সিরিঞ্জ।", "প্যারাসিটামলে শিশুদের জন্য বাড়তি সতর্কতা: শিশুদের জন্য নির্ধারিত পণ্য নিন, সঙ্গের মাপক দিয়ে মাপুন এবং লেবেল বা পেশাদারের পরামর্শ মানুন।"),
 ("pc", "liver"): ("এক্স-রে ধাঁচের শরীরের চিত্রে জ্বলজ্বলে লিভার ও অন্ত্র; পাশে খোলা বোতল থেকে টেবিলে ছড়িয়ে পড়া প্যারাসিটামল ট্যাবলেট।", "বেশি প্যারাসিটামল খেলে লিভারের ক্ষতি হতে পারে; লেবেলের সীমার মধ্যে থাকুন এবং লিভারের সমস্যা থাকলে আগে জিজ্ঞাসা করুন।"),
 ("pc", "help"): ("পেট চেপে ধরা অস্বস্তিতে থাকা একজন পুরুষ চিকিৎসকের কাছে উপসর্গ বলছেন, চিকিৎসক ক্লিপবোর্ডে লিখছেন।", "প্যারাসিটামল ওভারডোজের সন্দেহ হলে জরুরি সাহায্য নিন; জ্বর বা ব্যথা কমতে না চাইলে চিকিৎসক বা ফার্মাসিস্টকে জিজ্ঞাসা করুন।"),
}
def fn(a, k, lang): return f"{ART[a]['pre']}-{k}" + ("" if lang == "en" else "-bn") + ".webp"
def fig(a, k, lang, cover=False):
    L = EN if lang == "en" else BN; alt, cap = L[(a, k)]; ai = AI_EN if lang == "en" else AI_BN
    base = f"/assets/img/blog/{ART[a]['dir']}/"
    ex = 'fetchpriority="high" decoding="async"' if cover else 'loading="lazy" decoding="async"'
    return f'<figure class="pv-fig"><img src="{base}{fn(a, k, lang)}{V}" alt="{esc(alt)}" width="1600" height="900" {ex}><figcaption class="caption">{esc(cap + ai)}</figcaption></figure>'
def after_first_block(h, start, block):
    m = re.compile(r"</p>|</table></div>|</ul>").search(h, start); assert m
    return h[:m.end()] + block + h[m.end():]
def process(a, lang):
    A = ART[a]; d = R / "blog" / (A["slug"] + ("" if lang == "en" else "-bangla")) / "index.html"; h = d.read_text(encoding="utf-8")
    assert "q3-20261128" not in h
    h = h.replace("</head>", '<link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261124"></head>', 1)
    for k in A["order"][1:]:  # body figures, built later in reverse position order to keep indexes valid
        pass
    jobs = []
    if "secs" in A:
        for sid, k in A["secs"].items():
            m = re.search(r'<h2[^>]*id="' + re.escape(sid) + r'"[^>]*>.*?</h2>', h, re.S); assert m, sid; jobs.append((m.end(), k))
    else:
        h2 = [m.end() for m in re.finditer(r"<h2[^>]*>.*?</h2>", h, re.S)]
        for i, k in A["idx"].items(): jobs.append((h2[i], k))
    for pos, k in sorted(jobs, reverse=True): h = after_first_block(h, pos, fig(a, k, lang))
    cover = fig(a, "cover", lang, cover=True)
    if a == "pc":
        m = re.search(r'<div class="quick">.*?</div>', h, re.S); assert m; h = h[:m.end()] + cover + h[m.end():]
    else:
        m = re.search(r'<figure class="hero-visual">.*?</figure>', h, re.S); assert m
        h = h[:m.start()] + cover.replace('class="pv-fig"', 'class="hero-visual"') + h[m.end():]
    soc = f"{SITE}/assets/img/blog/{A['dir']}/{A['pre']}-social-{lang}.jpg{V}"; oa = esc((EN if lang == "en" else BN)[(a, "cover")][0])
    h = re.sub(r'<meta property="og:image(?::[a-z_]+)?" content="[^"]*">\s*', "", h)
    h = re.sub(r'<meta name="twitter:image(?::alt)?" content="[^"]*">\s*', "", h)
    og = (f'<meta property="og:image" content="{soc}"><meta property="og:image:secure_url" content="{soc}"><meta property="og:image:type" content="image/jpeg">'
          f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{oa}">')
    tw = f'<meta name="twitter:image" content="{soc}"><meta name="twitter:image:alt" content="{oa}">'
    m = re.search(r'<meta property="og:url"[^>]*>', h); assert m; h = h[:m.end()] + og + h[m.end():]
    h = re.sub(r'<meta name="twitter:card" content="[^"]*">', '<meta name="twitter:card" content="summary_large_image">' + tw, h, count=1)
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap, w, hh):
        u = f"{SITE}/assets/img/blog/{A['dir']}/{name}"
        return {"@type": "ImageObject", "contentUrl": u, "url": u, "width": w, "height": hh, "caption": cap, "creator": CRE, "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    L = EN if lang == "en" else BN
    lst = [obj(f"{A['pre']}-social-{lang}.jpg", L[(a, "cover")][0], 1200, 630)] + [obj(fn(a, k, lang), L[(a, k)][0], 1600, 900) for k in A["order"]]
    thumb = f"{SITE}/assets/img/blog/{A['dir']}/{A['pre']}-card.webp"
    def fix(m):
        j = json.loads(m.group(1)); nodes = j["@graph"] if "@graph" in j else [j]
        for n in nodes:
            if n.get("@type") == "BlogPosting":
                old = n.get("image"); extra = [o for o in (old if isinstance(old, list) else []) if isinstance(o, dict) and not str(o.get("url", "")).endswith(("cover.svg",))]
                n["image"] = lst + extra; n["thumbnailUrl"] = thumb
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(\{(?:(?!</script>).)*"@type":\s*"BlogPosting"(?:(?!</script>).)*)</script>', fix, h, count=1, flags=re.S)
    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(x)
    d.write_text(h, encoding="utf-8"); print(a, lang, "figs", h.count('class="pv-fig"') + h.count('class="hero-visual"'))
if __name__ == "__main__":
    import sys
    for a in (sys.argv[1:] or ART):
        for lg in ("en", "bn"): process(a, lg)
