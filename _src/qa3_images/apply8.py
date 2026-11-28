#!/usr/bin/env python3
"""Pharma Industry + Generic vs Brand (live): swap in new pictures with alt/captions/SEO, share images, schema, sitemap, feed, cards."""
import re, json, html, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; V = "?v=q8-20261129"; TODAY = "2026-11-29"
AIEN, AIBN = " AI-generated photo-style illustration.", " AI-তৈরি ছবি-ধাঁচের চিত্র।"
def esc(s): return html.escape(s, quote=True)
PI_ALT = {
 "cover": ("Pharmaceutical industry in Bangladesh: a modern pharmaceutical factory at sunrise with a plain medicine box and tablet strip on a wooden table. By pharmacist Sayedul Abrar.", "বাংলাদেশের ওষুধ শিল্প: সূর্যোদয়ে আধুনিক ওষুধ কারখানা, কাঠের টেবিলে সাদা ওষুধের বাক্স ও ট্যাবলেটের স্ট্রিপ। ফার্মাসিস্ট সাইয়্যেদুল আবরার।"),
 "ind": ("What is the pharmaceutical industry? A laboratory flask, a tablet press, packed medicine boxes and a pharmacy shelf in one scene, showing research, manufacturing and supply.", "ফার্মাসিউটিক্যাল শিল্প কী? ল্যাবের ফ্লাস্ক, ট্যাবলেট প্রেস, প্যাকেটজাত ওষুধের বাক্স ও ফার্মেসির তাক একই দৃশ্যে, যা গবেষণা, উৎপাদন ও সরবরাহ বোঝায়।"),
 "journey": ("From idea to patient: five stages shown as circles on a glowing path: a microscope, a lab test tube, a checklist, a tablet production line and a pharmacy handover.", "ধারণা থেকে রোগী পর্যন্ত: উজ্জ্বল পথে পাঁচটি বৃত্তে মাইক্রোস্কোপ, পরীক্ষার টিউব, চেকলিস্ট, ট্যাবলেট উৎপাদন লাইন ও ফার্মেসিতে ওষুধ হস্তান্তর।"),
 "types": ("Types of pharmaceutical companies: four scenes, a research laboratory, a tablet press, a reactor for raw materials and a sample-testing station.", "ফার্মাসিউটিক্যাল কোম্পানির ধরন: চারটি দৃশ্য, গবেষণাগার, ট্যাবলেট প্রেস, কাঁচামালের রিঅ্যাক্টর ও নমুনা পরীক্ষার স্টেশন।"),
 "api": ("API versus finished pharmaceutical product (FPP): a glass dish of white powder on the left, a glowing arrow, and finished tablets and capsules on a tray on the right.", "API বনাম ফিনিশড ফার্মাসিউটিক্যাল প্রোডাক্ট (FPP): বাঁদিকে সাদা পাউডারের ডিশ, উজ্জ্বল তীর এবং ডানদিকে ট্রেতে তৈরি ট্যাবলেট ও ক্যাপসুল।"),
 "mfg": ("Inside a pharmaceutical manufacturing facility: a tablet press, a coating pan and a blister packing machine in a cleanroom, with staff in full protective gowns.", "ওষুধ উৎপাদন কারখানার ভেতরে: ক্লিনরুমে ট্যাবলেট প্রেস, কোটিং প্যান ও ব্লিস্টার প্যাকিং মেশিন, পুরো সুরক্ষা পোশাকে কর্মীরা।"),
 "qual": ("Quality and safety in pharma: a quality analyst in a lab coat, cap and gloves placing a sample vial into an HPLC instrument beside a batch-record binder.", "ওষুধ শিল্পে মান ও নিরাপত্তা: ল্যাব কোট, ক্যাপ ও গ্লাভসে একজন মান বিশ্লেষক HPLC যন্ত্রে নমুনা ভায়াল রাখছেন, পাশে ব্যাচ রেকর্ডের বাইন্ডার।"),
 "supply": ("Pharmaceutical supply chain in Bangladesh: a warehouse with pallets of plain boxes, a delivery van and a pharmacy counter at the far end.", "বাংলাদেশে ওষুধ সরবরাহ শৃঙ্খল: সাদা বাক্সের প্যালেটসহ গুদাম, একটি ডেলিভারি ভ্যান ও শেষ প্রান্তে ফার্মেসির কাউন্টার।"),
 "who": ("Who works in the pharmaceutical industry: five professionals seen from behind in a bright corridor, including a pharmacist, a lab scientist, a production operator, a quality analyst and a sales professional.", "ওষুধ শিল্পে কারা কাজ করেন: উজ্জ্বল করিডোরে পেছন থেকে দেখা পাঁচজন পেশাজীবী, ফার্মাসিস্ট, ল্যাব বিজ্ঞানী, উৎপাদন অপারেটর, মান বিশ্লেষক ও সেলস পেশাজীবী।"),
 "take": ("Key takeaways about the pharmaceutical industry: a tablet and a capsule with a green leaf in front of a modern factory at sunrise.", "ওষুধ শিল্পের মূল কথা: সূর্যোদয়ের আলোয় আধুনিক কারখানার সামনে একটি ট্যাবলেট, একটি ক্যাপসুল ও সবুজ পাতা।")}
PI_NEW_CAP = {"ind": ("The pharmaceutical industry links research, manufacturing, quality checks and supply to pharmacies.", "ফার্মাসিউটিক্যাল শিল্প গবেষণা, উৎপাদন, মান যাচাই ও ফার্মেসিতে সরবরাহকে যুক্ত করে।"),
              "who": ("Many professional roles work together in the pharmaceutical industry.", "ওষুধ শিল্পে অনেক পেশাজীবী একসঙ্গে কাজ করেন।")}
GB_ALT = {
 "cover": ("Generic name vs brand name: four plain medicine boxes in different colours beside a tablet strip and tablets on a pharmacy counter. By pharmacist Sayedul Abrar.", "জেনেরিক নাম বনাম ব্র্যান্ড নাম: ফার্মেসির কাউন্টারে ভিন্ন রঙের চারটি সাদা ওষুধের বাক্স, পাশে ট্যাবলেটের স্ট্রিপ ও ট্যাবলেট। ফার্মাসিস্ট সাইয়্যেদুল আবরার।"),
 "ten": ("The 10-second trick: a stopwatch showing 10 seconds beside a tablet strip, tablets and capsules, a reminder to find the small generic name on the box.", "১০ সেকেন্ডের কৌশল: ট্যাবলেটের স্ট্রিপ, ট্যাবলেট ও ক্যাপসুলের পাশে ১০ সেকেন্ড দেখানো স্টপওয়াচ, বাক্সে ছোট জেনেরিক নামটি খুঁজে নেওয়ার স্মারক।"),
 "rina": ("Rina's two boxes: a young woman at a pharmacy holding two different medicine boxes, one with a teal band and one with an orange band, and comparing them.", "রিনার দুই বাক্স: ফার্মেসিতে এক তরুণী হাতে দুটি আলাদা ওষুধের বাক্স, একটিতে সবুজ-নীল ও অন্যটিতে কমলা ব্যান্ড, তুলনা করে দেখছেন।"),
 "generic": ("What is a generic name? A glass dish of white powder with a molecule model, tablets and a capsule, pointing to the active ingredient behind a medicine.", "জেনেরিক নাম কী? সাদা পাউডারের কাচের ডিশ, অণুর মডেল, ট্যাবলেট ও ক্যাপসুল, যা ওষুধের পেছনের সক্রিয় উপাদান বোঝায়।"),
 "secret": ("The secret code in medicine names: a magnifying glass over a plain medicine box showing a molecule structure, beside tablet strips and tablets.", "ওষুধের নামের গোপন সংকেত: সাদা ওষুধের বাক্সের ওপর ম্যাগনিফাইং গ্লাসে অণুর গঠন, পাশে ট্যাবলেটের স্ট্রিপ ও ট্যাবলেট।"),
 "layers": ("Three layers of a medicine: a molecule on top, white powder in the middle, and finished medicine boxes, strips and capsules at the bottom.", "ওষুধের তিন স্তর: ওপরে অণু, মাঝখানে সাদা পাউডার, নিচে তৈরি ওষুধের বাক্স, স্ট্রিপ ও ক্যাপসুল।"),
 "label": ("Read the label in 4 steps: a pharmacist's hands pointing to the information panel of a medicine box with icons, a QR code and a barcode.", "৪ ধাপে লেবেল পড়ুন: একজন ফার্মাসিস্টের হাত ওষুধের বাক্সের তথ্য প্যানেল দেখাচ্ছে, যেখানে আইকন, QR কোড ও বারকোড আছে।"),
 "tricks": ("Easy tricks to remember: a thoughtful man with a glowing idea bulb and three sticky notes, a flask, a capsule and a price tag, beside two medicine boxes.", "মনে রাখার সহজ কৌশল: ভাবনায় মগ্ন একজন পুরুষ, উজ্জ্বল আইডিয়া বাল্ব ও তিনটি স্টিকি নোটে ফ্লাস্ক, ক্যাপসুল ও দামের ট্যাগ, পাশে দুটি ওষুধের বাক্স।"),
 "quiz": ("Test yourself: a clipboard checklist with a question mark, a red cross and a green tick bubble, beside medicine boxes and tablets.", "নিজেকে যাচাই করুন: প্রশ্নচিহ্নসহ চেকলিস্ট ক্লিপবোর্ড, লাল ক্রস ও সবুজ টিক চিহ্ন, পাশে ওষুধের বাক্স ও ট্যাবলেট।")}
GB_CAP = {"ten": ("The 10-second trick: find the small generic name on the box.", "১০ সেকেন্ডের কৌশল: বাক্সে ছোট জেনেরিক নামটি খুঁজুন।"), "secret": ("Look closer: a generic name carries clues about the ingredient.", "আরও কাছ থেকে দেখুন: জেনেরিক নামে উপাদানের সূত্র থাকে।"), "quiz": ("Ready for the quiz? Test what you learned.", "কুইজের জন্য প্রস্তুত? যা শিখলেন যাচাই করে নিন।")}
GB_OLD = {"generic-vs-brand-same-ingredient-two-medicine-boxes-pharmacist": "cover", "four-parts-of-medicine-box-generic-name-strength-dosage-form-manufacturer": "ten", "rina-two-medicine-boxes-same-ingredient-different-brand": "rina",
          "active-ingredient-forms-powder-capsule-pellets-magnifier": "generic", "secret-code-in-medicine-names-generic-name-guide": "secret", "three-layers-generic-name-brand-name-formulation-finix-rabeprazole": "layers",
          "four-step-medicine-pack-check-generic-name-strength-dosage-form-manufacturer": "label", "remember-generic-vs-brand-in-4-tricks": "tricks", "medicine-safety-quiz-reward-badges": "quiz"}
PI_OLD = {"pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9": "cover", "complete-journey-of-a-medicine-research-to-post-market-monitoring": "journey", "types-of-pharmaceutical-companies-innovator-generic-api-cdmo-cro": "types",
          "api-vs-finished-pharmaceutical-product-fpp": "api", "tablet-and-capsule-manufacturing-process-seven-steps": "mfg", "gmp-quality-assurance-and-quality-control-qa-qc-explained": "qual",
          "pharmaceutical-supply-chain-in-bangladesh-from-manufacturing-to-patient": "supply", "pharmaceutical-industry-in-bangladesh-key-takeaways": "take"}
def io(u): return {"@type": "ImageObject", "contentUrl": u, "url": u, "creator": {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}, "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/", "license": SITE + "/sayedul-abrar-logo/#copyright"}
def seo(h, pre, D, lang, keys, ogalt):
    b = lang != "en"; soc = f"{SITE}{D}{pre}-social-{lang}.jpg{V}"
    h = re.sub(r'(<meta property="og:image" content=")[^"]*"', rf'\g<1>{soc}"', h); h = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', rf'\g<1>{soc}"', h)
    for p in ('<meta property="og:image:alt" content="', '<meta name="twitter:image:alt" content="'):
        if p in h: h = re.sub(re.escape(p) + r'[^"]*"', lambda m: p + esc(ogalt) + '"', h)
        else: h = h.replace(p.replace(' content="', ''), p.replace(' content="', ''), 1)
    if 'name="twitter:image:alt"' not in h: h = re.sub(r'(<meta name="twitter:image" content="[^"]*">)', lambda m: m.group(1) + f'<meta name="twitter:image:alt" content="{esc(ogalt)}">', h, count=1)
    if 'og:image:alt' not in h: h = re.sub(r'(<meta property="og:image" content="[^"]*">)', lambda m: m.group(1) + f'<meta property="og:image:alt" content="{esc(ogalt)}">', h, count=1)
    if 'og:image:secure_url' not in h: h = h.replace('<meta property="og:image:alt"', f'<meta property="og:image:secure_url" content="{soc}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt"', 1) if 'og:image:width' not in h else h.replace('<meta property="og:image:alt"', f'<meta property="og:image:secure_url" content="{soc}"><meta property="og:image:alt"', 1)
    def ld(m):
        j = json.loads(m.group(1))
        if j.get("@type") != "BlogPosting": return m.group(0)
        j["image"] = [io(f"{SITE}{D}{pre}-social-{lang}.jpg")] + [io(f"{SITE}{D}{pre}-{k}{'' if lang=='en' else '-bn'}.webp") for k in keys]
        j["thumbnailUrl"] = f"{SITE}{D}{pre}-card.webp"; j["dateModified"] = TODAY
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, h, flags=re.S)
def w750(pre, D, k):
    for lang in ("en", "bn"):
        s = "" if lang == "en" else "-bn"; im = Image.open(R / f"assets{D[7:]}{pre}-{k}{s}.webp"); im.resize((750, 422), Image.LANCZOS).save(R / f"assets{D[7:]}{pre}-{k}{s}-w750.webp", "WEBP", quality=82, method=6)
# ---------- Pharma industry ----------
PI = "pi"; PD = "/assets/img/blog/pharma-industry/"; PKEYS = ["cover", "ind", "journey", "types", "api", "mfg", "qual", "supply", "who", "take"]; w750(PI, PD, "cover")
def pi_url(k, lang, w=False): return f"{PD}pi-{k}{'' if lang=='en' else '-bn'}{'-w750' if w else ''}.webp{V}"
def pi_page(lang):
    p = R / f"blog/what-is-the-pharmaceutical-industry{'' if lang=='en' else '-bangla'}/index.html"; h = p.read_text(encoding="utf-8"); b = lang != "en"
    def fig(m):
        s = m.group(0); name = re.search(r"pharma-industry/([^\"]+?)\.webp", s).group(1); k = PI_OLD[name]
        ai = AIEN if not b else AIBN
        s = re.sub(r'src="[^"]*"', f'src="{pi_url(k, lang)}"', s, count=1); s = re.sub(r'alt="[^"]*"', f'alt="{esc(PI_ALT[k][b])}"', s, count=1)
        s = re.sub(r'width="\d+" height="\d+"', 'width="1600" height="900"', s, count=1)
        if k == "cover": s = re.sub(r'srcset="[^"]*"', f'srcset="{pi_url(k, lang, True)} 750w, {pi_url(k, lang)} 1600w"', s, count=1)
        if "<figcaption" in s: s = re.sub(r"</figcaption>", ai + "</figcaption>", s, count=1)
        else: s = s.replace("</figure>", f'<figcaption class="caption">{PI_ALT[k][b].split(". By")[0].split(".")[0]}.{ai}</figcaption></figure>') if False else s
        return s
    h, n = re.subn(r'<figure class="hero-visual">.*?</figure>', fig, h, flags=re.S); assert n == 8, n
    def newfig(k): return f'<figure class="hero-visual"><img src="{pi_url(k, lang)}" alt="{esc(PI_ALT[k][b])}" width="1600" height="900" loading="lazy" decoding="async"><figcaption class="caption">{PI_NEW_CAP[k][b]}{AIEN if not b else AIBN}</figcaption></figure>'
    i = h.find('<div class="lang-pane"') if False else h.find("<h2", h.find("</figure>"))  # first h2 after hero
    j = h.find("</p>", i) + 4; h = h[:j] + newfig("ind") + h[j:]
    i = h.find('<section id="roles">'); assert i > 0; j = h.find("</p>", i) + 4; h = h[:j] + newfig("who") + h[j:]
    og = PI_ALT["cover"][b].split(" By pharmacist")[0].split(" ফার্মাসিস্ট সাইয়্যেদুল")[0]
    h = seo(h, PI, PD, lang, PKEYS, og); p.write_text(h, encoding="utf-8")
for l in ("en", "bn"): pi_page(l)
# ---------- Generic vs brand ----------
GB = "gb"; GD = "/assets/img/blog/generic-brand/"; GKEYS = ["cover", "ten", "rina", "generic", "secret", "layers", "label", "tricks", "quiz"]; w750(GB, GD, "cover")
def gb_url(k, lang): return f"{GD}gb-{k}{'' if lang=='en' else '-bn'}.webp{V}"
def gb_page(slug, lang):
    p = R / f"blog/{slug}/index.html"; h = p.read_text(encoding="utf-8"); cnt = 0
    def fig(m):
        nonlocal cnt; s = m.group(0); mm = re.search(r"generic-brand/([^\"]+?)\.webp", s)
        if not mm or mm.group(1) not in GB_OLD: return s
        k = GB_OLD[mm.group(1)]; cnt += 1; s = s.replace('class="gb-fig narrow"', 'class="gb-fig"')
        def im(x):
            t = x.group(0); l = "en" if 'class="lang-en"' in t else "bn"
            t = re.sub(r'src="[^"]*"', f'src="{gb_url(k, l)}"', t, count=1); t = re.sub(r'alt="[^"]*"', f'alt="{esc(GB_ALT[k][l == "bn"])}"', t, count=1)
            return re.sub(r'width="\d+" height="\d+"', 'width="1600" height="900"', t, count=1)
        s = re.sub(r"<img [^>]*>", im, s)
        def cap(x):
            c = x.group(0); l = "en" if 'lang-en' in c[:30] else "bn"; txt = re.search(r">(.*?)</span>", c, re.S).group(1)
            if k in GB_CAP: txt = GB_CAP[k][l == "bn"]
            return c[:c.find(">") + 1] + txt + (AIEN if l == "en" else AIBN) + "</span>"
        return re.sub(r"<figcaption>.*?</figcaption>", lambda y: re.sub(r'<span class="lang-(?:en|bn)"[^>]*>.*?</span>', cap, y.group(0), flags=re.S), s, flags=re.S)
    h = re.sub(r'<figure class="gb-fig[^"]*">.*?</figure>', fig, h, flags=re.S); assert cnt == 9, cnt
    lang = "en" if slug.endswith("name") else "bn"; og = GB_ALT["cover"][lang == "bn"].split(" By pharmacist")[0].split(" ফার্মাসিস্ট সাইয়্যেদুল")[0]
    h = seo(h, GB, GD, lang, GKEYS, og); p.write_text(h, encoding="utf-8")
gb_page("generic-name-vs-brand-name", "en"); gb_page("generic-name-vs-brand-name-bangla", "bn")
# ---------- sitemap / feed / data / cards / home ----------
CFG = [("what-is-the-pharmaceutical-industry", PI, PD, PI_ALT, PKEYS), ("generic-name-vs-brand-name", GB, GD, GB_ALT, GKEYS)]
sm = (R / "sitemap.xml").read_text(encoding="utf-8"); fd = (R / "blog/feed.xml").read_text(encoding="utf-8")
for slug, pre, D, ALT, keys in CFG:
    for lang in ("en", "bn"):
        loc = f"{SITE}/blog/{slug}{'' if lang=='en' else '-bangla'}/"; m = re.search(r"<url><loc>" + re.escape(loc) + r"</loc>.*?</url>", sm, re.S); assert m, loc
        lm = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{TODAY}</lastmod>", re.search(r"<lastmod>[^<]*</lastmod>", m.group(0)).group(0))
        t = lambda k: html.escape(ALT[k][lang != "en"].split(":")[0].split("?")[0], quote=False)
        im = f"<image:image><image:loc>{SITE}{D}{pre}-social-{lang}.jpg</image:loc><image:title>{t('cover')}</image:title></image:image>" + "".join(f"<image:image><image:loc>{SITE}{D}{pre}-{k}{'' if lang=='en' else '-bn'}.webp</image:loc><image:title>{t(k)}</image:title></image:image>" for k in keys)
        sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{im}</url>" + sm[m.end():]
        f = R / f"assets{D[7:]}{pre}-social-{lang}.jpg"
        fd, n = re.subn(r'(<link>' + re.escape(loc) + r'</link>(?:(?!</item>).)*?)<enclosure[^>]*/>', lambda mm: mm.group(1) + f'<enclosure url="{SITE}{D}{f.name}" type="image/jpeg" length="{f.stat().st_size}" />', fd, count=1, flags=re.S)
        if n != 1: print("WARN feed", loc)
(R / "sitemap.xml").write_text(sm, encoding="utf-8"); (R / "blog/feed.xml").write_text(fd, encoding="utf-8")
for fp in ("assets/articles.json", "_src/data/articles.json"):
    t = (R / fp).read_text(encoding="utf-8")
    for slug, pre, D, ALT, keys in CFG:
        t = re.sub(r'("slug": "' + slug + r'".*?"img": ")[^"]*"', lambda m: m.group(1) + f"{D}{pre}-card.webp\"", t, count=1, flags=re.S)
    (R / fp).write_text(t, encoding="utf-8")
for fp in ("index.html", "blog/index.html"):
    t = (R / fp).read_text(encoding="utf-8")
    for slug, pre, D, ALT, keys in CFG:
        for m in set(re.findall(re.escape(D) + r"[a-z0-9-]*thumbnail[a-z0-9-]*\.webp", t)):
            if (pre == PI and "thumbnail-16x9" in m) or (pre == GB and "same-ingredient" not in m and "which-name" in m or "generic-vs-brand" in m and "thumbnail" in m): t = t.replace(m, f"{D}{pre}-cover{'-w750' if '-w750' in m else ''}.webp")
        t = t.replace(f"{SITE}/assets/img/blog/pharma-industry-in-bangladesh-social.jpg", f"{SITE}{PD}pi-social-en.jpg")
    (R / fp).write_text(t, encoding="utf-8")
print("ok")
