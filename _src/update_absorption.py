#!/usr/bin/env python3
"""One-time update (13 Nov 2026) of the Drug Absorption article (EN + BN): diagrams, new molecular-transport section,
first-pass explanation, extra FAQs, specific references, FAQPage + BreadcrumbList schema, shorter descriptions, social image.
Idempotent guard: refuses to run twice."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://sayedulabrar.site"
SLUG = "drug-absorption-how-medicine-enters-bloodstream"
IMG = "/assets/img/blog/drug-absorption/"
esc = lambda x: html.escape(x, quote=True)
BN_DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

FIG = {  # key: (stem, alt EN, caption EN, alt BN, caption BN)
 "cover": ("drug-absorption-cover-16x9", "", "",
   "ওষুধের শোষণ: অন্ত্রের ভিলাই পেরিয়ে ওষুধের অণু রক্তনালিতে প্রবেশ করছে, ওপরে একটি ট্যাবলেট। লিখেছেন ফার্মাসিস্ট সাইয়্যেদুল আবরার।", "ওষুধের শোষণ: সহজ চিত্র।"),
 "journey": ("journey-of-a-swallowed-tablet-diagram",
   "Diagram of the journey of a swallowed tablet: mouth and food pipe, stomach, small intestine, portal vein, liver and then the bloodstream, with five numbered steps.",
   "The journey of a swallowed tablet, simplified.",
   "গিলে খাওয়া ট্যাবলেটের যাত্রার চিত্র: মুখ ও খাদ্যনালি, পাকস্থলী, ক্ষুদ্রান্ত্র, পোর্টাল শিরা, যকৃৎ, তারপর রক্তপ্রবাহ; পাঁচটি ধাপসহ।",
   "গিলে খাওয়া ট্যাবলেটের যাত্রা, সহজ চিত্রে।"),
 "steps": ("tablet-disintegration-dissolution-absorption-steps",
   "Three close-up panels: disintegration (a tablet breaks into particles), dissolution (particles dissolve into molecules) and absorption (molecules cross intestinal cells into a blood capillary).",
   "Disintegration, dissolution and absorption. A drug must be in solution to be absorbed.",
   "তিনটি কাছের দৃশ্য: ডিসইন্টিগ্রেশন (ট্যাবলেট কণায় ভাঙে), ডিসলিউশন (কণা গলে অণু হয়) এবং অ্যাবজর্পশন (অণু অন্ত্রের কোষ পেরিয়ে রক্তনালিতে যায়)।",
   "ডিসইন্টিগ্রেশন, ডিসলিউশন ও অ্যাবজর্পশন। দ্রবীভূত ওষুধই শোষিত হতে পারে।"),
 "zoom": ("small-intestine-villi-microvilli-absorption-close-view",
   "Zoom-in diagram of the small intestine: folds of the inner wall, a finger-like villus with blood vessels, and absorbing cells with microvilli passing medicine molecules into a blood capillary.",
   "Folds, villi and microvilli give the small intestine a very large absorbing surface.",
   "ক্ষুদ্রান্ত্রের জুম-ইন চিত্র: ভেতরের দেয়ালের ভাঁজ, রক্তনালিসহ আঙুলের মতো ভিলাস, এবং মাইক্রোভিলাইযুক্ত কোষ দিয়ে ওষুধের অণু রক্তনালিতে যাচ্ছে।",
   "ভাঁজ, ভিলাই ও মাইক্রোভিলাই ক্ষুদ্রান্ত্রে শোষণের বিশাল জায়গা তৈরি করে।"),
 "mech": ("passive-diffusion-vs-carrier-transport-cell-membrane",
   "Diagram comparing passive diffusion, where drug molecules cross the lipid cell membrane from high to low concentration, with carrier-mediated transport, where a membrane protein carries the molecule using energy.",
   "Passive diffusion and carrier-mediated transport across the cell membrane.",
   "কোষপর্দা পেরোনোর দুই উপায়ের তুলনা: প্যাসিভ ডিফিউশনে অণু বেশি থেকে কম ঘনত্বে যায়; ক্যারিয়ার পরিবহনে পর্দার প্রোটিন শক্তি খরচ করে অণু বহন করে।",
   "কোষপর্দা দিয়ে প্যাসিভ ডিফিউশন ও ক্যারিয়ার-নির্ভর পরিবহন।"),
 "firstpass": ("first-pass-metabolism-bioavailability-diagram",
   "First-pass metabolism flow chart: oral dose, gut wall, portal vein, liver, general circulation, with some drug lost at each early stage; IV gives 100% bioavailability and some sublingual medicines avoid the first pass.",
   "Why not all of an oral dose reaches the general circulation.",
   "ফার্স্ট-পাস মেটাবলিজমের প্রবাহচিত্র: মুখে খাওয়া ডোজ, অন্ত্রের দেয়াল, পোর্টাল শিরা, যকৃৎ, তারপর সাধারণ রক্তপ্রবাহ; প্রতিটি ধাপে কিছু ওষুধ কমে যায়।",
   "মুখে খাওয়া পুরো ডোজ কেন রক্তপ্রবাহে পৌঁছায় না।"),
 "factors": ("factors-affecting-drug-absorption",
   "Six factors that affect drug absorption: dosage form, food, gut conditions, drug properties, other medicines and route of administration.",
   "Six things that can change how a medicine is absorbed.",
   "ওষুধের শোষণে প্রভাব ফেলা ছয়টি বিষয়: ডোজের ধরন, খাবার, পেট ও অন্ত্রের অবস্থা, ওষুধের বৈশিষ্ট্য, অন্য ওষুধ এবং প্রয়োগের পথ।",
   "ছয়টি বিষয় যা ওষুধের শোষণ বদলে দিতে পারে।"),
 "routes": ("drug-absorption-by-route-of-administration",
   "Chart of routes of administration and absorption: IV has no absorption step; intramuscular, subcutaneous, oral and sublingual need absorption; inhaled and topical depend on the product.",
   "Absorption differs by route of administration.",
   "প্রয়োগের পথ অনুযায়ী শোষণের চার্ট: শিরায় ইনজেকশনে শোষণ লাগে না; মাংসপেশি, চামড়ার নিচে, মুখে ও জিভের নিচে শোষণ লাগে; শ্বাসে ও ত্বকে পণ্যভেদে ভিন্ন।",
   "প্রয়োগের পথভেদে শোষণ আলাদা।"),
}
def fig(k, bn, hero=False):
    stem, aen, cen, abn, cbn = FIG[k]
    src = f"{IMG}{stem}{'-bn' if bn else ''}.webp?v=1"
    alt, cap = (abn, cbn) if bn else (aen, cen)
    tip = "বড় করে দেখতে ছবিতে চাপুন।" if bn else "Tap the image to view it full size."
    load = 'fetchpriority="high"' if hero else 'loading="lazy"'
    return (f'<figure class="hero-visual"><a href="{src}" target="_blank" rel="noopener" aria-label="{esc(tip)}"><img src="{src}" alt="{esc(alt)}" width="1600" height="900" {load} decoding="async"></a>'
            f'<figcaption class="caption">{cap} {tip}</figcaption></figure>')

REFS = [
 ("https://www.ncbi.nlm.nih.gov/books/NBK557405/", "Alagga AA, Pellegrini MV, Gupta V. Drug Absorption. StatPearls (NCBI Bookshelf), updated 27 February 2024", "mechanisms of absorption, small intestine, bioavailability"),
 ("https://www.ncbi.nlm.nih.gov/books/NBK551679/", "First-Pass Effect. StatPearls (NCBI Bookshelf)", "first-pass metabolism and routes that bypass it"),
 ("https://www.ncbi.nlm.nih.gov/books/NBK557744/", "Pharmacokinetics. StatPearls (NCBI Bookshelf)", "absorption within pharmacokinetics"),
 ("https://www.msdmanuals.com/professional/clinical-pharmacology/pharmacokinetics/drug-absorption", "MSD Manual Professional Edition. Drug Absorption (reviewed August 2026)", "drugs must be in solution, passive diffusion, transporters, routes"),
 ("https://www.merckmanuals.com/professional/clinical-pharmacology/pharmacokinetics/overview-of-pharmacokinetics", "Merck Manual Professional Edition. Overview of Pharmacokinetics", "general overview"),
]
def refs_ol():
    return '<ol class="references">' + "".join(f'<li>{t}. <a href="{u}" target="_blank" rel="noopener noreferrer">{u.split("//")[1].split("/")[0]}</a> — {n}.</li>' for u, t, n in REFS) + "</ol>"

T = {
 "en": dict(
   s4=('<h2>4. How do medicine molecules cross the gut wall?</h2>'
       '<p>Dissolved molecules still have to pass through the cells that line the gut. The outer layer of each cell, the <strong>cell membrane</strong>, is made of fat-like (lipid) molecules. Medicines cross it mainly in two ways:</p>'
       '<ul><li><strong>Passive diffusion:</strong> the most common way. Molecules move from where there is more drug (the gut) to where there is less (the blood), without using energy. Fat-soluble, un-ionised molecules cross most easily.</li>'
       '<li><strong>Carrier-mediated transport:</strong> special proteins in the membrane carry certain molecules across. <em>Active</em> transport uses energy and can move a drug against its concentration gradient. These carriers can become saturated, and similar drugs can compete for them.</li></ul>'
       '<p>Some proteins work in the opposite direction. Efflux pumps such as P-glycoprotein push some drugs back into the gut, which can reduce how much is absorbed.</p>'),
   fp=('<p>Here is the route behind first-pass metabolism. Blood leaving the intestine does not go straight to the rest of the body. It first travels through the <strong>portal vein</strong> to the liver. Some of the drug can be broken down in the gut wall and the liver on this first pass, so less active drug reaches the general circulation. A medicine given into a vein skips this step, and some medicines absorbed under the tongue, such as nitroglycerin, can bypass much of it.</p>'),
   sub='<p>Medicines placed under the tongue (sublingual) are absorbed through the lining of the mouth.</p>',
   faq=[("What is passive diffusion?", "It is the most common way medicines cross cell membranes. Molecules move from an area of higher concentration to an area of lower concentration without using energy."),
        ("Why does a medicine given into a vein work differently from a tablet?", "An intravenous (IV) medicine goes straight into the bloodstream, so its bioavailability is 100% and there is no absorption or first-pass step. A tablet must dissolve, be absorbed and pass the liver first.")],
   desc="How does medicine enter the bloodstream? A pharmacist explains drug absorption with diagrams: dissolution, villi, passive diffusion, first-pass and bioavailability.",
   ogalt="Drug absorption explained: medicine molecules crossing intestinal villi and entering a blood capillary.",
   crumb="Drug Absorption"),
 "bn": dict(
   s4=('<h2>৪. ওষুধের অণু কীভাবে অন্ত্রের দেয়াল পেরোয়?</h2>'
       '<p>দ্রবীভূত অণুকে অন্ত্রের আবরণীর কোষগুলো পার হতে হয়। প্রতিটি কোষের বাইরের আবরণ বা <strong>কোষপর্দা (cell membrane)</strong> চর্বিজাতীয় (lipid) অণু দিয়ে তৈরি। ওষুধ মূলত দুইভাবে এটি পার হয়:</p>'
       '<ul><li><strong>প্যাসিভ ডিফিউশন (passive diffusion):</strong> সবচেয়ে সাধারণ পথ। যেখানে ওষুধ বেশি (অন্ত্র) সেখান থেকে যেখানে কম (রক্ত) সেদিকে অণু চলে যায়, কোনো শক্তি খরচ হয় না। চর্বিতে দ্রবণীয় ও আয়নহীন (un-ionised) অণু সবচেয়ে সহজে পেরোয়।</li>'
       '<li><strong>ক্যারিয়ার-নির্ভর পরিবহন (carrier-mediated transport):</strong> কোষপর্দার বিশেষ প্রোটিন নির্দিষ্ট অণুকে বহন করে। সক্রিয় পরিবহনে (active transport) শক্তি লাগে এবং ঘনত্বের বিপরীত দিকেও ওষুধ নিতে পারে। এই ক্যারিয়ার পূর্ণ (saturated) হয়ে যেতে পারে, আর একই ধরনের ওষুধ একে অপরের সঙ্গে প্রতিযোগিতা করতে পারে।</li></ul>'
       '<p>কিছু প্রোটিন উল্টো কাজ করে। P-glycoprotein-এর মতো efflux পাম্প কিছু ওষুধকে আবার অন্ত্রে ফেরত পাঠায়, ফলে শোষণ কমতে পারে।</p>'),
   fp=('<p>First-pass metabolism বোঝার মূল পথটি এখানে। অন্ত্র থেকে বের হওয়া রক্ত সরাসরি সারা শরীরে যায় না; আগে <strong>পোর্টাল শিরা (portal vein)</strong> দিয়ে যকৃতে (লিভার) যায়। এই প্রথম যাত্রায় অন্ত্রের দেয়াল ও যকৃতে কিছু ওষুধ ভেঙে যেতে পারে, তাই কম সক্রিয় ওষুধ সাধারণ রক্তপ্রবাহে পৌঁছায়। শিরায় দেওয়া ওষুধ এই ধাপ এড়িয়ে যায়, আর জিভের নিচে রাখা কিছু ওষুধ, যেমন নাইট্রোগ্লিসারিন, এর বড় অংশ এড়াতে পারে।</p>'),
   sub='<p>জিভের নিচে রাখা (sublingual) ওষুধ মুখের ভেতরের আবরণী দিয়ে শোষিত হয়।</p>',
   faq=[("প্যাসিভ ডিফিউশন কী?", "এটি ওষুধের কোষপর্দা পেরোনোর সবচেয়ে সাধারণ উপায়। শক্তি খরচ ছাড়াই অণু বেশি ঘনত্বের জায়গা থেকে কম ঘনত্বের দিকে চলে যায়।"),
        ("শিরায় দেওয়া ওষুধ আর ট্যাবলেট আলাদাভাবে কাজ করে কেন?", "শিরায় (IV) দেওয়া ওষুধ সরাসরি রক্তে যায়, তাই এর bioavailability ১০০% এবং শোষণ বা first-pass metabolism-এর ধাপ নেই। ট্যাবলেটকে আগে দ্রবীভূত হতে হয়, শোষিত হতে হয় এবং যকৃৎ পার হতে হয়।")],
   desc="ওষুধ কীভাবে রক্তে প্রবেশ করে? ছবি ও ডায়াগ্রামসহ সহজ বাংলায় ওষুধের শোষণ: দ্রবীভবন, ভিলাই, প্যাসিভ ডিফিউশন, first-pass metabolism ও bioavailability।",
   ogalt="ওষুধের শোষণ: অন্ত্রের ভিলাই পেরিয়ে ওষুধের অণু রক্তনালিতে প্রবেশ করছে।",
   crumb="ওষুধের শোষণ"),
}

def txt(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def update(lang):
    bn = lang == "bn"; L = T[lang]
    p = R / "blog" / (SLUG + ("-bangla" if bn else "")) / "index.html"
    s = p.read_text(encoding="utf-8")
    assert "passive-diffusion-vs-carrier" not in s, "already updated"
    url = f"{B}/blog/{SLUG}{'-bangla' if bn else ''}/"
    n = (lambda k: str(k).translate(BN_DIG)) if bn else str
    # --- renumber sections 4..7 -> 5..8 (from the highest down)
    for k in (7, 6, 5, 4):
        old, new = f"<h2>{n(k)}. ", f"<h2>{n(k+1)}. "
        assert s.count(old) == 1, (lang, old); s = s.replace(old, new)
    # --- hero (BN gets its own Bangla cover)
    figs = list(re.finditer(r'<figure class="hero-visual">.*?</figure>', s, re.S))
    assert len(figs) == 2, len(figs)
    second = figs[1].group(0)
    if bn: s = s.replace(figs[0].group(0), fig("cover", True, hero=True), 1)
    # --- replace duplicate villi figure with steps + zoom
    s = s.replace(second, fig("steps", bn) + "\n" + fig("zoom", bn), 1)
    # --- journey before section 2
    h2_2 = re.search(r"<h2>%s\. [^<]*</h2>" % re.escape(n(2)), s).group(0)
    s = s.replace(h2_2, fig("journey", bn) + "\n" + h2_2, 1)
    # --- new section 4 (molecular transport) before section 5 (bioavailability)
    h2_5 = re.search(r"<h2>%s\. [^<]*</h2>" % re.escape(n(5)), s).group(0)
    s = s.replace(h2_5, L["s4"] + "\n" + fig("mech", bn) + "\n" + h2_5, 1)
    # --- first-pass explanation + diagram before section 6 (factors)
    h2_6 = re.search(r"<h2>%s\. [^<]*</h2>" % re.escape(n(6)), s).group(0)
    s = s.replace(h2_6, L["fp"] + "\n" + fig("firstpass", bn) + "\n" + h2_6, 1)
    # --- factors diagram before section 7 (routes)
    h2_7 = re.search(r"<h2>%s\. [^<]*</h2>" % re.escape(n(7)), s).group(0)
    s = s.replace(h2_7, fig("factors", bn) + "\n" + h2_7, 1)
    # --- routes: sublingual sentence + diagram before section 8 (example)
    h2_8 = re.search(r"<h2>%s\. [^<]*</h2>" % re.escape(n(8)), s).group(0)
    s = s.replace(h2_8, L["sub"] + "\n" + fig("routes", bn) + "\n" + h2_8, 1)
    # --- extra FAQs before references heading
    ref_h2 = re.search(r"<h2>(References and further reading|তথ্যসূত্র ও আরও পড়ুন)</h2>", s).group(0)
    s = s.replace(ref_h2, "".join(f"<h3>{q}</h3><p>{a}</p>\n" for q, a in L["faq"]) + ref_h2, 1)
    # --- references
    s = re.sub(r'<ol class="references">.*?</ol>', lambda m: refs_ol(), s, count=1, flags=re.S)
    # --- collect all FAQ pairs for schema
    fsec = s[s.index('<h2 id="faq">'):s.index(ref_h2)]
    pairs = re.findall(r"<h3>(.*?)</h3><p>(.*?)</p>", fsec, re.S)
    # --- meta tags
    social = f"{B}{IMG}drug-absorption-social{'-bn' if bn else ''}.jpg"
    def meta(attr, name, val):
        nonlocal s
        pat = rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")'
        assert re.search(pat, s), name
        s = re.sub(pat, lambda x: x.group(1) + esc(val) + x.group(2), s, count=1)
    meta("name", "description", L["desc"]); meta("property", "og:image", social); meta("property", "og:image:width", "1200"); meta("property", "og:image:height", "630")
    meta("name", "twitter:image", social); meta("property", "article:modified_time", "2026-11-13") if 'article:modified_time' in s else None
    if 'property="og:description"' in s: meta("property", "og:description", L["desc"])
    if 'name="twitter:description"' in s: meta("name", "twitter:description", L["desc"])
    # --- JSON-LD
    lds = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S))
    post = None
    for m in lds:
        j = json.loads(m.group(1))
        if j.get("@type") == "BlogPosting": post = (m, j)
    m, j = post
    hero = f"{B}/assets/img/blog/how-medicines-work/absorption-how-medicine-enters-the-bloodstream.webp" if not bn else f"{B}{IMG}{FIG['cover'][0]}-bn.webp"
    j["image"] = [hero, social] + [f"{B}{IMG}{FIG[k][0]}{'-bn' if bn else ''}.webp" for k in ("journey", "steps", "zoom", "mech", "firstpass", "factors", "routes")]
    j["thumbnailUrl"] = hero; j["description"] = L["desc"]; j["dateModified"] = "2026-11-13"
    j["citation"] = [{"@type": "CreativeWork", "name": t, "url": u} for u, t, _ in REFS]
    j["about"] = [{"@type": "Thing", "name": "Drug absorption"}, {"@type": "Thing", "name": "Bioavailability"}, {"@type": "Thing", "name": "First-pass effect"}, {"@type": "Thing", "name": "Pharmacokinetics"}]
    j["audience"] = {"@type": "PeopleAudience", "audienceType": "General public and pharmacy students"}
    a = re.search(r"<article.*?</article>", s, re.S).group(0); j["wordCount"] = len(txt(a).split())
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq", "inLanguage": "bn-BD" if bn else "en-BD",
             "mainEntity": [{"@type": "Question", "name": txt(q), "acceptedAnswer": {"@type": "Answer", "text": txt(an)}} for q, an in pairs]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": B + "/"}, {"@type": "ListItem", "position": 2, "name": "Pharma Blog", "item": B + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": L["crumb"], "item": url}]}
    jd = lambda d: '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "</script>"
    new = jd(j) + ("" if '"FAQPage"' in s else jd(faqld)) + ("" if '"BreadcrumbList"' in s else jd(crumbs))
    s = s.replace(m.group(0), new, 1)
    p.write_text(s, encoding="utf-8")
    print(lang, "faq", len(pairs), "words", j["wordCount"], "desc", len(L["desc"]))

for L in ("en", "bn"): update(L)
