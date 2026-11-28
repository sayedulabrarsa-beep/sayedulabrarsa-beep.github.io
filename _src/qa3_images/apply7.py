#!/usr/bin/env python3
"""Drug vs Medicine (live): swap in the 10 new pictures (hero + 9 figures) with alt/caption/SEO, share image, schema, sitemap, feed, card."""
import re, json, html, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; D = "/assets/img/blog/drug-vs-medicine/"; V = "?v=q7-20261128"
def fn(k, lang): return f"dm-{k}" + ("" if lang == "en" else "-bn") + ".webp"
OLD = {"what-is-a-drug-active-pharmaceutical-ingredient": "drug", "what-is-a-medicine-prepared-product-tablet-capsule-syrup": "medicine", "remember-drug-vs-medicine-in-10-seconds-substance-prepared-product": "remember",
       "drug-vs-medicine-key-differences-at-a-glance": "diff", "rabeprazole-finix-finix-mups-real-world-example": "rabe", "from-drug-to-medicine-the-journey-formulation-manufacturing-quality-check": "every",
       "what-is-pharmacology-pharmacokinetics-pharmacodynamics": "pharm", "why-drug-vs-medicine-knowledge-matters-safe-rational-use": "why", "drug-vs-medicine-key-takeaways": "takeaways"}
ORDER = ["cover", "drug", "medicine", "diff", "remember", "rabe", "every", "pharm", "why", "takeaways"]
AIEN, AIBN = " AI-generated photo-style illustration.", " AI-তৈরি ছবি-ধাঁচের চিত্র।"
ALT = {
 "cover": ("Drug vs Medicine: a dish of white powder, a glowing arrow and a finished medicine pack with tablet strip, tablet and capsule, showing the active substance becoming a prepared product.",
           "Drug vs Medicine: সাদা পাউডারের ডিশ, উজ্জ্বল তীর এবং প্রস্তুত ওষুধের প্যাক, ট্যাবলেটের স্ট্রিপ, ট্যাবলেট ও ক্যাপসুল, যা সক্রিয় পদার্থ থেকে প্রস্তুত পণ্য হওয়ার ধারণা দেখায়।"),
 "drug": ("What is a drug? A lab spatula adds white powder to a glass flask beside a molecule graphic, illustrating a drug as an active substance (API).",
          "Drug কী? ল্যাবের স্প্যাচুলা দিয়ে কাচের ফ্লাস্কে সাদা পাউডার দেওয়া হচ্ছে, পাশে অণুর গ্রাফিক, যা সক্রিয় পদার্থ (API) হিসেবে Drug বোঝায়।"),
 "medicine": ("What is a medicine? A syrup bottle, cream tube, tablet strip, tablet and capsule, showing prepared products with a drug in a specific form.",
              "Medicine কী? সিরাপের বোতল, ক্রিমের টিউব, ট্যাবলেটের স্ট্রিপ, ট্যাবলেট ও ক্যাপসুল, যা নির্দিষ্ট ফর্মে Drug ধারণকারী প্রস্তুত পণ্য বোঝায়।"),
 "diff": ("Key difference between a drug and a medicine: a flask with powder on one side and a packaged strip and box on the other, active substance versus prepared product.",
          "Drug ও Medicine-এর মূল পার্থক্য: একদিকে পাউডারসহ ফ্লাস্ক, অন্যদিকে প্যাকেটজাত স্ট্রিপ ও বাক্স, অর্থাৎ সক্রিয় পদার্থ বনাম প্রস্তুত পণ্য।"),
 "remember": ("Remember it in 10 seconds: an open capsule with powder beside a tablet. S is for Substance (the drug), P is for Prepared Product (the medicine).",
              "১০ সেকেন্ডে মনে রাখুন: খোলা ক্যাপসুল থেকে পাউডার ও পাশে ট্যাবলেট। S মানে Substance (Drug), P মানে Prepared Product (Medicine)।"),
 "rabe": ("Example only: a plain medicine box and tablet strip beside a glowing stomach. Rabeprazole is the active ingredient (drug); Finix and Finix MUPS are brand-name medicines containing it.",
          "শুধু উদাহরণ: একটি সাদা ওষুধের বাক্স ও ট্যাবলেটের স্ট্রিপের পাশে উজ্জ্বল পাকস্থলী। Rabeprazole হলো সক্রিয় উপাদান (Drug); Finix ও Finix MUPS হলো এটি ধারণকারী ব্র্যান্ড নামের Medicine।"),
 "every": ("Is every drug a medicine? Glass jars of white powder beside a tablet strip: a drug can remain a raw substance until it is prepared and approved as a medicine.",
           "প্রতিটি Drug কি Medicine? সাদা পাউডারের কাচের জার ও ট্যাবলেটের স্ট্রিপ: প্রস্তুত ও অনুমোদিত না হওয়া পর্যন্ত Drug কাঁচামাল পদার্থ হিসেবেই থাকতে পারে।"),
 "pharm": ("What is pharmacology? A translucent human body with a glowing path from mouth to stomach and a receptor close-up, showing what the body does to a drug (PK) and what the drug does to the body (PD).",
           "Pharmacology কী? স্বচ্ছ মানবদেহে মুখ থেকে পাকস্থলী পর্যন্ত উজ্জ্বল পথ ও রিসেপ্টরের ক্লোজ-আপ, যা শরীর Drug-এর সঙ্গে কী করে (PK) এবং Drug শরীরে কী করে (PD) বোঝায়।"),
 "why": ("Why it matters: a pharmacist's hands holding a plain medicine box and its information leaflet, a reminder to use clear terms for safer medicine use.",
         "কেন গুরুত্বপূর্ণ: একজন ফার্মাসিস্টের হাতে সাদা ওষুধের বাক্স ও তথ্যপত্র, যা নিরাপদ ওষুধ ব্যবহারে স্পষ্ট শব্দ ব্যবহারের কথা মনে করায়।"),
 "takeaways": ("Key takeaways: a spilled capsule, a tablet strip and a mortar. A drug is the active substance, a medicine is the prepared product; related but not the same.",
               "মূল কথা: ছড়ানো ক্যাপসুল, ট্যাবলেটের স্ট্রিপ ও মর্টার। Drug হলো সক্রিয় পদার্থ, Medicine হলো প্রস্তুত পণ্য; সম্পর্কিত কিন্তু এক নয়।")}
CAP_EN = {"every": "Not every drug becomes a medicine."}; CAP_BN = {"every": "প্রতিটি Drug Medicine হয় না।"}
TITLE = ("Drug vs Medicine: What Is the Difference?", "Drug বনাম Medicine: পার্থক্য কী?")
OGALT = ("Drug vs Medicine: a drug is the active substance and a medicine is the prepared product", "Drug বনাম Medicine: Drug হলো সক্রিয় পদার্থ, Medicine হলো প্রস্তুত পণ্য")
for lang in ("en", "bn"):  # 750px hero
    im = Image.open(R / f"assets/img/blog/drug-vs-medicine/{fn('cover', lang)}"); im.resize((750, 422), Image.LANCZOS).save(R / f"assets/img/blog/drug-vs-medicine/dm-cover{'' if lang=='en' else '-bn'}-w750.webp", "WEBP", quality=82, method=6)
def url(k, lang, w750=False): return D + fn(k, lang).replace(".webp", "-w750.webp" if w750 else ".webp") + V
def fig(old, k, lang):
    cap = re.search(r"<figcaption>(.*?)</figcaption>", old, re.S).group(1)
    cap = (CAP_EN if lang == "en" else CAP_BN).get(k, cap)
    return f'<figure class="gb-fig"><img src="{url(k, lang)}" width="1600" height="900" alt="{html.escape(ALT[k][lang != "en"], quote=True)}" loading="lazy" decoding="async"><figcaption>{cap}{AIEN if lang == "en" else AIBN}</figcaption></figure>'
def page(lang):
    p = R / f"blog/drug-vs-medicine{'' if lang=='en' else '-bangla'}/index.html"; h = p.read_text(encoding="utf-8"); b = lang != "en"
    h = re.sub(r'<img class="article-image"[^>]*>(?:<p class="image-caption">.*?</p>)?', "", h, flags=re.S)
    def hero(m):
        s = m.group(0); cap = re.search(r"<figcaption>(.*?)</figcaption>", s, re.S).group(1)
        i = f'<img class="article-hero" src="{url("cover", lang)}" alt="{html.escape(ALT["cover"][b], quote=True)}" title="{html.escape(TITLE[b], quote=True)}" width="1600" height="900" fetchpriority="high" decoding="async" srcset="{url("cover", lang, True)} 750w, {url("cover", lang)} 1600w" sizes="357px">'
        return f'<figure class="hero-figure">{i}<figcaption>{cap}{AIEN if not b else AIBN}</figcaption></figure>'
    h, n = re.subn(r'<figure class="hero-figure">.*?</figure>', hero, h, count=1, flags=re.S); assert n == 1
    cnt = 0
    def rf(m):
        nonlocal cnt; old = m.group(0); name = re.search(r"/drug-vs-medicine/([^\"]+?)\.webp", old).group(1); cnt += 1; return fig(old, OLD[name], lang)
    h = re.sub(r'<figure class="gb-fig">.*?</figure>', rf, h, flags=re.S); assert cnt == 9, cnt
    soc = f"{SITE}{D}dm-social-{lang}.jpg{V}"
    h = re.sub(r'(<meta property="og:image" content=")[^"]*"', rf'\g<1>{soc}"', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', lambda m: m.group(1) + html.escape(OGALT[b], quote=True) + '"', h)
    h = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', rf'\g<1>{soc}"', h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*"', lambda m: m.group(1) + html.escape(OGALT[b], quote=True) + '"', h)
    if 'og:image:secure_url' not in h: h = h.replace('<meta property="og:image:alt"', f'<meta property="og:image:secure_url" content="{soc}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt"', 1)
    def ld(m):
        j = json.loads(m.group(1))
        if j.get("@type") != "BlogPosting": return m.group(0)
        def io(u): return {"@type": "ImageObject", "contentUrl": u, "url": u, "creator": {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}, "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/", "license": SITE + "/sayedul-abrar-logo/#copyright"}
        j["image"] = [io(f"{SITE}{D}dm-social-{lang}.jpg")] + [io(SITE + D + fn(k, lang)) for k in ORDER]
        j["thumbnailUrl"] = f"{SITE}{D}dm-card.webp"; j["dateModified"] = "2026-11-28"
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, h, flags=re.S)
    assert "unsplash" not in h
    p.write_text(h, encoding="utf-8")
for l in ("en", "bn"): page(l)
sm = (R / "sitemap.xml").read_text(encoding="utf-8")
for lang in ("en", "bn"):
    loc = f"{SITE}/blog/drug-vs-medicine{'' if lang=='en' else '-bangla'}/"; m = re.search(r"<url><loc>" + re.escape(loc) + r"</loc>.*?</url>", sm, re.S); lm = re.search(r"<lastmod>[^<]*</lastmod>", m.group(0)).group(0).replace("2026-11-27", "2026-11-28")
    im = f"<image:image><image:loc>{SITE}{D}dm-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[lang != 'en'], quote=False)}</image:title></image:image>" + "".join(f"<image:image><image:loc>{SITE}{D}{fn(k, lang)}</image:loc><image:title>{html.escape(ALT[k][lang != 'en'].split(':')[0].split('?')[0], quote=False)}</image:title></image:image>" for k in ORDER)
    sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{im}</url>" + sm[m.end():]
(R / "sitemap.xml").write_text(sm, encoding="utf-8")
fd = (R / "blog/feed.xml").read_text(encoding="utf-8")
for lang in ("en", "bn"):
    loc = f"{SITE}/blog/drug-vs-medicine{'' if lang=='en' else '-bangla'}/"; f = R / f"assets/img/blog/drug-vs-medicine/dm-social-{lang}.jpg"
    fd, n = re.subn(r'(<link>' + re.escape(loc) + r'</link>(?:(?!</item>).)*?)<enclosure[^>]*/>', lambda mm: mm.group(1) + f'<enclosure url="{SITE}{D}{f.name}" type="image/jpeg" length="{f.stat().st_size}" />', fd, count=1, flags=re.S); assert n == 1
(R / "blog/feed.xml").write_text(fd, encoding="utf-8")
for fp, isd in (("assets/articles.json", False), ("_src/data/articles.json", True)):
    j = json.loads((R / fp).read_text(encoding="utf-8"))
    if isd: j["drug-vs-medicine"]["img"] = D + "dm-card.webp"
    else:
        for x in j:
            if x.get("slug") == "drug-vs-medicine": x["img"] = D + "dm-card.webp"
    (R / fp).write_text(json.dumps(j, ensure_ascii=False, indent=2 if True else None) + "\n", encoding="utf-8")
b = (R / "blog/index.html").read_text(encoding="utf-8")
i = b.find('<a href="/blog/drug-vs-medicine/" class="pb-card-image">'); s = b.rfind("<article", 0, i); e = b.find("</article>", i); c = b[s:e]
c = re.sub(r'data-bn-img="[^"]*"', f'data-bn-img="{D}dm-social-bn.jpg{V}"', c)
c = re.sub(r'<img src="[^"]*"[^>]*>', f'<img src="{D}dm-card-w750.webp{V}" alt="{html.escape(ALT["cover"][0], quote=True)}" width="1200" height="630" loading="lazy" srcset="{D}dm-card-w750.webp{V} 750w, {D}dm-card.webp{V} 1200w" sizes="357px">', c, count=1)
(R / "blog/index.html").write_text(b[:s] + c + b[e:], encoding="utf-8"); print("ok")
