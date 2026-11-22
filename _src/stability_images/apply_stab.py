#!/usr/bin/env python3
"""Put the 8 new stability figures into the EN + BN article pages, add the Key takeaways section,
and tighten the SEO head (title, description, share image, schema, sitemap). Re-runnable."""
import json, pathlib, re, html

R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"
IMG = "/assets/img/blog/stability/"
SLUG = "medicine-stability-testing-how-shelf-life-is-established"
V = "?v=1"

ORDER = ["cover", "study", "tests", "pack", "climate", "shelf", "storage", "key"]
FILES = {"cover": "stability-cover", "study": "stability-study-design", "tests": "stability-quality-tests",
         "pack": "stability-packaging", "climate": "stability-bangladesh-climate", "shelf": "stability-shelf-life",
         "storage": "stability-patient-storage", "key": "stability-key-takeaways"}

TXT = {
 "en": {
  "alt": {
   "cover": "Illustration of a glass stability chamber holding amber bottles, vials and blister packs inside a glowing clock ring, for medicine stability testing.",
   "study": "Three glowing lanes carrying sample bottles for accelerated, intermediate and long-term stability studies with illustrative temperature and humidity conditions.",
   "tests": "Six glass pedestals showing stability tests: physical properties, assay and impurities, dissolution, moisture, pH and microbial limits.",
   "pack": "A glass dome protecting a blister pack, amber bottle, white bottle with desiccant and carton from heat and moisture, showing why packaging is part of a stability study.",
   "climate": "Illustration of a pharmaceutical warehouse and delivery truck under monsoon rain and strong sun, showing hot and humid storage conditions in Bangladesh.",
   "shelf": "Illustrative stability trend curve falling towards an acceptance limit, beside a medicine pack with an hourglass marking the printed expiry date.",
   "storage": "Hands placing a medicine box on a cool, dry shelf, with two warning panels showing direct sun and a steamy bathroom to avoid.",
   "key": "Five glowing pillars for temperature, humidity, time, packaging and evidence around a small stability chamber, summarising the key takeaways."},
  "cap": {
   "cover": "A stability chamber keeps samples under defined conditions so changes can be measured over time. Illustration prepared for this article.",
   "study": "The study arms answer different questions. Conditions shown are illustrative ICH Q1A(R2) general-case examples; they depend on the product, storage label and target market.",
   "tests": "The programme follows attributes that may change and matter to product quality, safety or performance. The test panel depends on the dosage form.",
   "pack": "Study the medicine in the container-closure system proposed for marketing, including protective secondary packaging when relevant.",
   "climate": "Heat and humidity during storage, transport and distribution are why climate matters. Illustration only; it does not show a regulatory requirement.",
   "shelf": "Shelf life is a decision based on the full stability data package, not a date selected separately from the evidence. The curve is illustrative, not real data.",
   "storage": "Follow the storage instructions on the pack, and avoid heat, direct sunlight and damp rooms such as bathrooms.",
   "key": "The five points to remember about stability testing and shelf life."},
  "h2_key": "9. Key takeaways",
  "key_items": [
   "Stability testing follows medicine quality over time under defined temperature, humidity, light and packaging conditions.",
   "Long-term data are the main basis for a finished medicine's shelf life; accelerated data support the assessment.",
   "Studies should use the proposed marketed container-closure system or a justified equivalent.",
   "Representative batches and planned time points show whether quality stays within specification.",
   "Shelf life is a decision from the whole data package. Store the medicine as the pack says."],
  "title": "Medicine Stability Testing: How Shelf Life Is Set | Sayedul Abrar",
  "ogtitle": "Medicine Stability Testing: How Shelf Life Is Set",
  "desc": "Medicine stability testing explained: long-term, accelerated and ongoing studies, packaging, shelf life and expiry dates, with Bangladesh context.",
  "ogalt": "Medicine Stability Testing: a glowing glass stability chamber with medicine bottles, vials and blister packs inside a clock ring.",
  "after_h2": {"climate": "6. Bangladesh: climate and regulatory context", "storage": "8. What should patients understand?"},
  "faq_h": "Frequently asked questions",
 },
 "bn": {
  "alt": {
   "cover": "ওষুধের stability testing: জ্বলজ্বলে ঘড়ির বলয়ের ভেতরে কাচের stability chamber, যেখানে অ্যাম্বার বোতল, ভায়াল ও ব্লিস্টার প্যাক রাখা আছে।",
   "study": "Accelerated, intermediate ও long-term stability study-র জন্য নমুনা বোতল বহনকারী তিনটি আলোকিত লেন, সঙ্গে উদাহরণস্বরূপ তাপমাত্রা ও আর্দ্রতার শর্ত।",
   "tests": "Stability test-এর ছয়টি ধাপ: ভৌত বৈশিষ্ট্য, assay ও impurity, dissolution, আর্দ্রতা, pH এবং microbial limit।",
   "pack": "কাচের গম্বুজ ব্লিস্টার প্যাক, অ্যাম্বার বোতল, desiccant-সহ সাদা বোতল ও কার্টনকে তাপ ও আর্দ্রতা থেকে রক্ষা করছে—packaging কেন study-র অংশ তা বোঝাতে।",
   "climate": "মৌসুমি বৃষ্টি ও কড়া রোদের নিচে ওষুধের গুদাম ও ডেলিভারি ট্রাক—বাংলাদেশের গরম ও আর্দ্র সংরক্ষণ পরিবেশের চিত্র।",
   "shelf": "গ্রহণযোগ্য সীমার দিকে নামতে থাকা উদাহরণ-রেখা এবং expiry date বোঝাতে বালিঘড়িসহ ওষুধের প্যাক।",
   "storage": "ঠান্ডা ও শুকনো তাকে ওষুধের বাক্স রাখছে দুটি হাত; পাশে সরাসরি রোদ ও স্যাঁতসেঁতে বাথরুমের দুটি সতর্কতা-প্যানেল।",
   "key": "তাপমাত্রা, আর্দ্রতা, সময়, packaging ও প্রমাণ—পাঁচটি আলোকিত স্তম্ভ ও মাঝখানে ছোট stability chamber; মূল কথার সারসংক্ষেপ।"},
  "cap": {
   "cover": "নির্দিষ্ট পরিবেশে নমুনা রেখে সময়ের সঙ্গে পরিবর্তন মাপতে stability chamber ব্যবহার করা হয়। এই নিবন্ধের জন্য তৈরি চিত্র।",
   "study": "তিন ধরনের study আলাদা প্রশ্নের উত্তর দেয়। দেখানো শর্তগুলো ICH Q1A(R2)-এর সাধারণ উদাহরণ; পণ্য, storage label ও target market অনুযায়ী শর্ত বেছে নিতে হয়।",
   "tests": "সময়ের সঙ্গে যে quality attribute বদলাতে পারে এবং পণ্যের মান, নিরাপত্তা বা কার্যকারিতার জন্য গুরুত্বপূর্ণ—সেগুলো পর্যবেক্ষণ করা হয়। পরীক্ষার তালিকা dosage form-এর ওপর নির্ভর করে।",
   "pack": "বাজারজাত করার container-closure system-এ বা বৈজ্ঞানিকভাবে যুক্তিযুক্ত সমতুল্য packaging-এ study করা উচিত।",
   "climate": "সংরক্ষণ, পরিবহন ও বিতরণের সময় গরম ও আর্দ্রতার কারণেই জলবায়ু গুরুত্বপূর্ণ। এটি শুধু চিত্র; কোনো নিয়ন্ত্রক শর্ত নয়।",
   "shelf": "Shelf life হলো সম্পূর্ণ stability data package-এর ভিত্তিতে নেওয়া quality decision; প্রমাণ থেকে আলাদা করে বেছে নেওয়া কোনো তারিখ নয়। রেখাটি উদাহরণ, প্রকৃত data নয়।",
   "storage": "প্যাকের storage নির্দেশনা মানুন এবং গরম, সরাসরি রোদ ও বাথরুমের মতো স্যাঁতসেঁতে ঘর এড়িয়ে চলুন।",
   "key": "Stability testing ও shelf life সম্পর্কে মনে রাখার পাঁচটি বিষয়।"},
  "h2_key": "৯. মূল কথা",
  "key_items": [
   "Stability testing হলো নির্দিষ্ট তাপমাত্রা, আর্দ্রতা, আলো ও packaging-এর মধ্যে সময়ের সঙ্গে ওষুধের মান কীভাবে বদলায় তা পর্যবেক্ষণ।",
   "Long-term data-ই finished medicine-এর shelf life-এর প্রধান ভিত্তি; accelerated data মূল্যায়নকে সমর্থন করে।",
   "Study করতে হবে বাজারজাত করার container-closure system-এ বা যুক্তিযুক্ত সমতুল্য packaging-এ।",
   "প্রতিনিধিত্বশীল batch ও পরিকল্পিত time point দেখায় মান specification-এর মধ্যে থাকছে কি না।",
   "Shelf life হলো সম্পূর্ণ data package থেকে নেওয়া সিদ্ধান্ত। প্যাকে যেভাবে লেখা, সেভাবেই ওষুধ রাখুন।"],
  "title": "ওষুধের স্থায়িত্ব পরীক্ষা: মেয়াদ কীভাবে নির্ধারিত হয় | Sayedul Abrar",
  "ogtitle": "ওষুধের স্থায়িত্ব পরীক্ষা: মেয়াদ কীভাবে নির্ধারিত হয়",
  "desc": None,   # keep the existing Bangla description
  "ogalt": "ওষুধের স্থায়িত্ব পরীক্ষা: ঘড়ির বলয়ের ভেতরে ওষুধের বোতল, ভায়াল ও ব্লিস্টার প্যাকসহ কাচের stability chamber।",
  "after_h2": {"climate": "৬. বাংলাদেশ: climate ও regulatory context", "storage": "৮. রোগীদের কী জানা দরকার?"},
  "faq_h": "সাধারণ প্রশ্নোত্তর",
 },
}


def fig(lang, key, first=False):
    t = TXT[lang]
    f = FILES[key] + ("" if lang == "en" else "-bn") + ".webp"
    url = IMG + f + V
    a = html.escape(t["alt"][key], quote=True)
    c = html.escape(t["cap"][key])
    extra = 'fetchpriority="high" decoding="async"' if first else 'loading="lazy" decoding="async"'
    return (f'<figure class="hero-visual"><a href="{url}" target="_blank" rel="noopener"><img src="{url}" alt="{a}" '
            f'width="1600" height="900" {extra}></a><figcaption class="caption">{c}</figcaption></figure>')


def page(lang):
    suffix = "" if lang == "en" else "-bangla"
    p = R / "blog" / (SLUG + suffix) / "index.html"
    s = p.read_text(encoding="utf-8")
    t = TXT[lang]
    soc = f"{SITE}{IMG}stability-social-{lang}.jpg{V}"

    # ---- 1. figures: replace the 5 old ones in order, then insert the 3 new ones
    old = list(re.finditer(r'<figure class="hero-visual">.*?</figure>', s, re.S))
    assert len(old) in (5, 7, 8), len(old)
    if len(old) == 5:
        mapping = ["cover", "study", "tests", "pack", "shelf"]
        out, last = [], 0
        for m, k in zip(old, mapping):
            out.append(s[last:m.start()]); out.append(fig(lang, k, first=(k == "cover"))); last = m.end()
        out.append(s[last:]); s = "".join(out)
        for k, h in t["after_h2"].items():
            m = re.search(r'<h2>' + re.escape(h) + r'</h2>', s)
            assert m, h
            s = s[:m.end()] + fig(lang, k) + s[m.end():]
        items = "".join(f"<li>{html.escape(x)}</li>" for x in t["key_items"])
        block = (f'<h2>{t["h2_key"]}</h2>{fig(lang, "key")}'
                 f'<div class="takeaways"><ul>{items}</ul></div>\n')
        m = re.search(r'<h2 id="faq">', s)
        s = s[:m.start()] + block + s[m.start():]

    # ---- 2. head: title, description, share image
    s = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"], quote=False)}</title>', s, 1, re.S)
    if t["desc"]:
        d = html.escape(t["desc"], quote=True)
        s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s, 1)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s, 1)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s, 1)
    og = html.escape(t["ogtitle"], quote=True)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + og + m.group(2), s, 1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + og + m.group(2), s, 1)
    alt = html.escape(t["ogalt"], quote=True)
    s = re.sub(r'<meta property="og:image"[^>]*>\s*<meta property="og:image:type"[^>]*>\s*<meta property="og:image:width"[^>]*>\s*'
               r'<meta property="og:image:height"[^>]*>\s*<meta property="og:image:alt"[^>]*>',
               f'<meta property="og:image" content="{soc}"><meta property="og:image:secure_url" content="{soc}">'
               f'<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200">'
               f'<meta property="og:image:height" content="630"><meta property="og:image:alt" content="{alt}">', s, 1, re.S)
    s = re.sub(r'<meta name="twitter:image"[^>]*>\s*<meta name="twitter:image:alt"[^>]*>',
               f'<meta name="twitter:image" content="{soc}"><meta name="twitter:image:alt" content="{alt}">', s, 1, re.S)

    # ---- 3. schema
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    d = json.loads(m.group(1))
    assert d["@type"] == "BlogPosting"
    suf = "" if lang == "en" else "-bn"
    d["image"] = [f"{SITE}{IMG}{FILES[k]}{suf}.webp{V}" for k in ORDER]
    d["thumbnailUrl"] = f"{SITE}{IMG}{FILES['cover']}{suf}.webp{V}"
    d["headline"] = t["ogtitle"] if lang == "en" else d["headline"]
    if t["desc"]:
        d["description"] = t["desc"]
    d["dateModified"] = "2026-11-22"
    d.setdefault("isAccessibleForFree", True)
    kw = re.search(r'<meta name="keywords" content="([^"]*)"', s)
    if kw:
        d["keywords"] = [x.strip() for x in kw.group(1).split(",") if x.strip()]
    art = s[s.find("<article"):s.find("</article>")]
    d["wordCount"] = len(re.sub(r"<[^>]+>", " ", art).split())
    refs = re.findall(r'<ol class="references">(.*?)</ol>', art, re.S)
    if refs:
        d["citation"] = [{"@type": "WebPage", "url": u} for u in re.findall(r'href="(https?://[^"]+)"', refs[0])]
    new = json.dumps(d, ensure_ascii=False, separators=(", ", ": "))
    s = s[:m.start(1)] + new + s[m.end(1):]
    p.write_text(s, encoding="utf-8")
    return p, d


def sitemap():
    p = R / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    for lang in ("en", "bn"):
        suffix = "" if lang == "en" else "-bangla"
        loc = f"{SITE}/blog/{SLUG}{suffix}/"
        suf = "" if lang == "en" else "-bn"
        imgs = "".join(
            f"<image:image><image:loc>{SITE}{IMG}{FILES[k]}{suf}.webp{V}</image:loc>"
            f"<image:title>{html.escape(TXT[lang]['alt'][k], quote=False)}</image:title></image:image>" for k in ORDER)
        pat = re.compile(r'(<url><loc>' + re.escape(loc) + r'</loc><lastmod>)[^<]*(</lastmod>).*?(</url>)', re.S)
        assert pat.search(s), loc
        s = pat.sub(lambda m: m.group(1) + "2026-11-22" + m.group(2) + imgs + m.group(3), s, 1)
    p.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    for lang in ("en", "bn"):
        pth, d = page(lang)
        print(pth.relative_to(R), "figures", len(d["image"]), "words", d["wordCount"])
    sitemap()
    print("sitemap updated")
