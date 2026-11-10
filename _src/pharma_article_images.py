#!/usr/bin/env python3
"""Replace Pexels stock photos with the user's 8 images in the EN + BN 'pharmaceutical industry' pages; SEO + schema.
Source = git HEAD version (idempotent as long as HEAD still has the stock photos); falls back to working copy if already converted."""
import re, json, html, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/pharma-industry/"
M = json.load(open(ROOT/"_src/pharma_images.json"))
SOCIAL = BASE + "/assets/img/blog/pharma-industry-in-bangladesh-social.jpg"
T = {  # key: (alt_en, cap_en, alt_bn, cap_bn, name_en)
"hero": ("Pharmaceutical industry in Bangladesh, how medicines reach you: a scientist in a laboratory, a tablet production line, a warehouse with a forklift, a delivery truck and a pharmacist handing medicine to a patient. By pharmacist Sayedul Abrar.",
  "From laboratory to pharmacy shelf: an illustration of how medicines reach patients.",
  "বাংলাদেশের ওষুধ শিল্প, ওষুধ কীভাবে আপনার কাছে পৌঁছায়: গবেষণাগারে বিজ্ঞানী, ট্যাবলেট উৎপাদন লাইন, ফর্কলিফটসহ গুদাম, ডেলিভারি ট্রাক এবং রোগীর হাতে ওষুধ তুলে দিচ্ছেন একজন ফার্মাসিস্ট। ফার্মাসিস্ট সায়েদুল আবরার।",
  "গবেষণাগার থেকে ফার্মেসির তাক পর্যন্ত: ওষুধ কীভাবে রোগীর কাছে পৌঁছায় তার একটি চিত্র।", "Pharmaceutical Industry in Bangladesh: How Medicines Reach You"),
"journey": ("The complete journey of a medicine in seven stages: research and discovery, preclinical research, clinical research, regulatory review, manufacturing, distribution and post-market monitoring.",
  "A simplified overview. Not every medicine follows exactly the same route; generic and biological medicines differ.",
  "একটি ওষুধের পূর্ণ যাত্রা সাতটি ধাপে: গবেষণা ও আবিষ্কার, প্রিক্লিনিকাল গবেষণা, ক্লিনিকাল গবেষণা, নিয়ন্ত্রক পর্যালোচনা, উৎপাদন, বিতরণ এবং বাজারজাতের পর পর্যবেক্ষণ।",
  "সরল সারসংক্ষেপ। সব ওষুধ হুবহু একই পথে যায় না; জেনেরিক ও বায়োলজিক্যাল ওষুধের পথ আলাদা।", "The complete journey of a medicine, from research to post-market monitoring"),
"types": ("Seven types of pharmaceutical companies: innovator or research-based, generic medicine manufacturer, branded-generic company, API manufacturer, biopharmaceutical company, CDMO and CRO.",
  "These categories can overlap; one company may do several of these things.",
  "ফার্মাসিউটিক্যাল কোম্পানির সাত ধরন: উদ্ভাবক বা গবেষণাভিত্তিক, জেনেরিক ওষুধ প্রস্তুতকারক, ব্র্যান্ডেড-জেনেরিক কোম্পানি, API প্রস্তুতকারক, বায়োফার্মাসিউটিক্যাল কোম্পানি, CDMO ও CRO।",
  "এই ধরনগুলো একটির সঙ্গে আরেকটি মিলে যেতে পারে; একটি কোম্পানি একসঙ্গে একাধিক কাজ করতে পারে।", "Types of pharmaceutical companies: innovator, generic, API, CDMO and CRO"),
"api": ("API versus finished pharmaceutical product (FPP): the API is the active substance, usually a bulk powder or crystal; the FPP is the final ready-to-use medicine made by formulating the API with excipients, then packaging and quality testing it.",
  "In short: the API is the key ingredient, and the finished pharmaceutical product is the complete medicine.",
  "API বনাম ফিনিশড ফার্মাসিউটিক্যাল প্রোডাক্ট (FPP): API হলো সক্রিয় উপাদান, সাধারণত বাল্ক পাউডার বা ক্রিস্টাল; FPP হলো API-কে এক্সসিপিয়েন্টের সঙ্গে ফর্মুলেট করে, প্যাকেজ ও মান পরীক্ষা করে তৈরি ব্যবহারের উপযোগী ওষুধ।",
  "সংক্ষেপে: API হলো মূল উপাদান, আর FPP হলো পূর্ণাঙ্গ ওষুধ।", "API vs finished pharmaceutical product (FPP)"),
"mfg": ("Seven steps of tablet and capsule manufacturing: raw materials (API and excipients), dispensing and weighing, blending, formulation by compression or encapsulation, optional coating, quality control and packaging.",
  "A simplified sequence. Steps vary by dosage form and product; not every tablet uses every step.",
  "ট্যাবলেট ও ক্যাপসুল উৎপাদনের সাতটি ধাপ: কাঁচামাল (API ও এক্সসিপিয়েন্ট), ডিসপেন্সিং ও ওজন, মিশ্রণ, কম্প্রেশন বা এনক্যাপসুলেশনে ফর্মুলেশন, ঐচ্ছিক কোটিং, মান নিয়ন্ত্রণ ও প্যাকেজিং।",
  "সরল ক্রম। ধাপগুলো ওষুধের ধরন ও পণ্যভেদে আলাদা হয়; প্রতিটি ট্যাবলেটে সব ধাপ লাগে না।", "Tablet and capsule manufacturing process in seven steps"),
"gmp": ("GMP, quality assurance and quality control compared: GMP is a set of standards for consistent production; QA is a system of planned activities across the whole process; QC is the set of tests and checks on raw materials, in-process products and the final product.",
  "GMP, QA and QC protect different parts of medicine quality.",
  "GMP, কোয়ালিটি অ্যাসিউরেন্স ও কোয়ালিটি কন্ট্রোলের তুলনা: GMP হলো ধারাবাহিক উৎপাদনের মানদণ্ড; QA হলো পুরো প্রক্রিয়া জুড়ে পরিকল্পিত কার্যক্রমের ব্যবস্থা; QC হলো কাঁচামাল, প্রক্রিয়াধীন পণ্য ও চূড়ান্ত পণ্যের পরীক্ষা ও যাচাই।",
  "GMP, QA ও QC ওষুধের মানের ভিন্ন ভিন্ন অংশ রক্ষা করে।", "GMP, QA and QC: the quality framework behind medicines"),
"supply": ("Pharmaceutical supply chain in Bangladesh in five steps: manufacturing at the pharmaceutical plant, the company central warehouse, distribution through depots and distributors, retail pharmacy, and the patient.",
  "A simplified illustration. Actual channels, licences and storage requirements depend on the product and current Bangladesh regulations.",
  "বাংলাদেশে ওষুধ সরবরাহ শৃঙ্খলের পাঁচ ধাপ: ওষুধ কারখানায় উৎপাদন, কোম্পানির কেন্দ্রীয় গুদাম, ডিপো ও পরিবেশকের মাধ্যমে বিতরণ, খুচরা ফার্মেসি এবং রোগী।",
  "সরল চিত্র। প্রকৃত বিতরণ পথ, লাইসেন্স ও সংরক্ষণের শর্ত পণ্য ও বর্তমান বাংলাদেশি বিধিমালার ওপর নির্ভর করে।", "The pharmaceutical supply chain in Bangladesh, from manufacturing to the patient"),
"key": ("Key takeaways about the pharmaceutical industry in Bangladesh: it develops and manufactures medicines, follows standards such as GMP with QA and QC, uses a supply chain from factory to warehouse, distributor and pharmacy, provides branded and generic medicines, and is a key healthcare sector.",
  "A summary illustration. For sector figures, see the BIDA profile cited in the references.",
  "বাংলাদেশের ওষুধ শিল্পের মূল কথা: ওষুধ উন্নয়ন ও উৎপাদন, GMP-সহ QA ও QC মানদণ্ড অনুসরণ, কারখানা থেকে গুদাম, পরিবেশক ও ফার্মেসি পর্যন্ত সরবরাহ শৃঙ্খল, ব্র্যান্ডেড ও জেনেরিক ওষুধ সরবরাহ এবং একটি গুরুত্বপূর্ণ স্বাস্থ্যখাত।",
  "সারসংক্ষেপ চিত্র। খাতসংক্রান্ত সংখ্যার জন্য তথ্যসূত্রে দেওয়া BIDA প্রোফাইল দেখুন।", "Key takeaways: the pharmaceutical industry in Bangladesh")}
def fig(k, bn, first=False):
    f, w, h = M[k]; a = T[k][2 if bn else 0]; c = T[k][3 if bn else 1]
    load = 'fetchpriority="high" decoding="async"' if first else 'loading="lazy" decoding="async"'
    return f'<figure class="hero-visual"><img src="{IMG}{f}" alt="{html.escape(a, quote=True)}" width="{w}" height="{h}" {load}><figcaption class="caption">{c}</figcaption></figure>'
def src(rel):
    r = subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT, capture_output=True, text=True)
    t = r.stdout if r.returncode == 0 and "images.pexels.com" in r.stdout else (ROOT/rel).read_text(encoding="utf-8")
    return t
FIG = re.compile(r'<figure class="hero-visual">.*?</figure>', re.S)
def process(slug, bn):
    rel = f"blog/{slug}/index.html"; s = src(rel); url = f"{BASE}/blog/{slug}/"
    figs = list(FIG.finditer(s)); assert len(figs) == 5, len(figs)
    new = [fig("hero", bn, True), fig("journey", bn), fig("mfg", bn), fig("gmp", bn), None]
    # build from the end so positions stay valid
    for m, n in reversed(list(zip(figs, new))):
        s = s[:m.start()] + (n or "") + s[m.end():]
    # companies image (end of companies section)
    i = s.index('<section id="factory"'); k = s.rindex("</section>", 0, i); s = s[:k] + fig("types", bn) + "\n" + s[k:]
    # API vs FPP before 2nd h3 inside factory section
    i = s.index('<section id="factory"'); j = s.index('<section id="quality"')
    h3 = [m.start() for m in re.finditer(r"<h3>", s[i:j])]; p = i + h3[1]; s = s[:p] + fig("api", bn) + "\n" + s[p:]
    # supply chain before last h3 of bangladesh section
    i = s.index('<section id="bangladesh"'); j = s.index('<section id="roles"')
    h3 = [m.start() for m in re.finditer(r"<h3>", s[i:j])]; p = i + h3[-1]; s = s[:p] + fig("supply", bn) + "\n" + s[p:]
    # key takeaways image after takeaways box
    i = s.index('class="takeaways"'); j = s.index("</div>", i) + 6; s = s[:j] + "\n" + fig("key", bn) + s[j:]
    # head meta
    alt_og = T["hero"][2 if bn else 0]
    def meta(attr, name, val):
        nonlocal s
        pat = rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")'
        assert re.search(pat, s), name
        s = re.sub(pat, lambda m: m.group(1) + html.escape(val, quote=True) + m.group(2), s, 1)
    meta("property", "og:image", SOCIAL); meta("property", "og:image:type", "image/jpeg"); meta("property", "og:image:width", "1200"); meta("property", "og:image:height", "630")
    meta("property", "og:image:alt", alt_og[:200]); meta("name", "twitter:image", SOCIAL); meta("name", "twitter:image:alt", alt_og[:200])
    kw_en = ", Bangladesh pharma industry, how medicines are made in Bangladesh, API vs finished pharmaceutical product, GMP QA QC difference, pharmaceutical supply chain Bangladesh, types of pharmaceutical companies, pharmacist Sayedul Abrar"
    kw_bn = ", ওষুধ কীভাবে তৈরি হয়, API ও FPP এর পার্থক্য, GMP QA QC পার্থক্য, বাংলাদেশে ওষুধ সরবরাহ শৃঙ্খল, ফার্মাসিস্ট সায়েদুল আবরার, Sayedul Abrar pharmacist"
    s = re.sub(r'(<meta name="keywords" content="[^"]*)(")', lambda m: m.group(1) + html.escape(kw_bn if bn else kw_en, quote=True) + m.group(2), s, 1)
    # JSON-LD
    mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S); d = json.loads(mm.group(1))
    def imo(u, w, h, name, desc, rep=False):
        return {"@type": "ImageObject", "@id": BASE + u + "#image", "url": BASE + u, "contentUrl": BASE + u, "name": name, "description": desc, "caption": desc,
                "width": w, "height": h, "encodingFormat": "image/webp", "inLanguage": "bn" if bn else "en", "creditText": "Sayedul Abrar",
                "copyrightNotice": "© 2026 Sayedul Abrar", "acquireLicensePage": BASE + "/about/", "representativeOfPage": rep,
                "creator": {"@type": "Person", "name": "Sayedul Abrar", "url": BASE + "/about/"}}
    imgs = [SOCIAL]
    for k in ("hero", "journey", "types", "api", "mfg", "gmp", "supply", "key"):
        f, w, h = M[k]; imgs.append(imo(IMG + f, w, h, T[k][4], T[k][2 if bn else 0], k == "hero"))
    d["image"] = imgs; d["thumbnailUrl"] = BASE + IMG + M["hero"][0]; d["isAccessibleForFree"] = True
    d["audience"] = {"@type": "PeopleAudience", "audienceType": "General public, pharmacy students and healthcare professionals"}
    d["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".quick", "h1"]}
    d["about"] = [{"@type": "Thing", "name": "Pharmaceutical industry in Bangladesh"}, {"@type": "Thing", "name": "Active pharmaceutical ingredient (API)"},
                  {"@type": "Thing", "name": "Good Manufacturing Practice (GMP)"}, {"@type": "GovernmentOrganization", "name": "Directorate General of Drug Administration (DGDA), Bangladesh"}]
    refs = re.search(r'<section class="references".*?</section>', s, re.S)
    if refs: d["citation"] = [{"@type": "WebPage", "name": html.unescape(re.sub(r"<[^>]+>", "", a[1])).strip(), "url": a[0]} for a in re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', refs.group(0), re.S)]
    d["wordCount"] = len(re.sub(r"<[^>]+>", " ", s[s.index("<article"):s.index("</article>")]).split())
    s = s[:mm.start(1)] + json.dumps(d, ensure_ascii=False) + s[mm.end(1):]
    # extra css: keep frame but no stretch
    (ROOT/rel).write_text(s, encoding="utf-8"); return len(s)
print(process("what-is-the-pharmaceutical-industry", False), process("what-is-the-pharmaceutical-industry-bangla", True))
