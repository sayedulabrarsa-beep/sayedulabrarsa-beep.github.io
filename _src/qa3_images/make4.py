#!/usr/bin/env python3
"""Dosage Forms, IR/SR/EC and Routes of Administration: 18 user-supplied text-free photos -> titled 1600x900 WebP (EN+BN), share images and cards.
Reuses the layout engine of make3.py; a different palette and font family per article."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make3 as m
from PIL import Image
from playwright.sync_api import sync_playwright
R, SRC, BG, FD = m.R, m.SRC, m.BG, m.FD
ST = "_src/stability_images/fonts"; EX = "_src/excretion_images/fonts"; QQ = "_src/qaqc_images/cinematic"
LAT, BNG, face = m.LAT, m.BNG, m.face
m.ART.update({
 "df": dict(dir="dosage-forms", pre="df", fam="'DFF'", ink="#063C45", key="#0B7C8A", acc="#D6336C", hi="rgba(214,51,108,.38)", veil="#EAF6F7", pill="#063C45", bandrgb="6,60,69", gold="#9BE4EE",
   css="".join([face("DFF", 800, FD(ST, "sora-latin-800-normal.woff2"), LAT), face("DFF", 600, FD(ST, "sora-latin-600-normal.woff2"), LAT), face("DFF", 800, FD(EX, "noto-sans-bengali-bengali-700-normal.woff2"), BNG), face("DFF", 600, FD(EX, "noto-sans-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.16, 1.4), ls=".08em"),
 "sr": dict(dir="release-designs", pre="sr", fam="'SRF'", ink="#4A2208", key="#C25A0E", acc="#1E9CAD", hi="rgba(30,156,173,.38)", veil="#FFF3E6", pill="#4A2208", bandrgb="74,34,8", gold="#FFD08A",
   css="".join([face("SRF", 800, FD(QQ, "hind-siliguri-latin-700-normal.woff2"), LAT), face("SRF", 600, FD(QQ, "hind-siliguri-latin-700-normal.woff2"), LAT), face("SRF", 800, FD(QQ, "hind-siliguri-bengali-700-normal.woff2"), BNG), face("SRF", 600, FD(QQ, "hind-siliguri-bengali-500-normal.woff2"), BNG)]), lh=(1.12, 1.32), ls=".1em"),
 "rt": dict(dir="routes-of-administration", pre="rt", fam="'RTF'", ink="#3D1020", key="#B3261E", acc="#F5B83D", hi="rgba(245,184,61,.55)", veil="#FBEFEF", pill="#3D1020", bandrgb="61,16,32", gold="#FFD27A",
   css="".join([face("RTF", 800, FD(ST, "noto-serif-bengali-latin-700-normal.woff2"), LAT), face("RTF", 600, FD(ST, "noto-serif-bengali-latin-600-normal.woff2"), LAT), face("RTF", 800, FD(ST, "noto-serif-bengali-bengali-800-normal.woff2"), BNG), face("RTF", 600, FD(ST, "noto-serif-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.14, 1.36), ls=".08em"),
})
IDS = ["01c8db07", "8f240c37", "369d4962", "40a6d8af", "7c0fffe7", "43635661", "30064f0b", "cf595a17", "6f173a2a", "332cc875", "80796df6", "3882e764", "e1336df7", "4872f03c", "ad3c73e5", "df05ecdf", "6c1c1af5", "bd3d831c"]
KEYS = [("df", "cover"), ("df", "solid"), ("df", "liquid"), ("df", "topical"), ("sr", "cover"), ("sr", "checklist"), ("sr", "compare"), ("sr", "ir"), ("sr", "sr"), ("sr", "ec"), ("sr", "abbr"), ("sr", "crush"),
        ("rt", "cover"), ("rt", "oral"), ("rt", "inh"), ("rt", "inj"), ("rt", "local"), ("rt", "speed")]
M4 = dict(zip(IDS, KEYS))
L = lambda tw, y0, y1: ("L", tw, y0, y1)
m.LAY.update({("df", "cover"): L(600, 60, 840), ("df", "solid"): L(400, 50, 640), ("df", "liquid"): L(540, 60, 840), ("df", "topical"): L(450, 40, 500),
  ("sr", "cover"): L(540, 60, 840), ("sr", "checklist"): L(540, 60, 840), ("sr", "compare"): L(540, 60, 840), ("sr", "ir"): L(540, 60, 840), ("sr", "sr"): L(540, 60, 840), ("sr", "ec"): L(500, 60, 840),
  ("sr", "abbr"): L(400, 60, 840), ("sr", "crush"): L(430, 40, 500),
  ("rt", "cover"): L(520, 60, 840), ("rt", "oral"): L(380, 50, 800), ("rt", "inh"): L(420, 50, 760), ("rt", "inj"): L(380, 50, 800), ("rt", "local"): L(280, 40, 520), ("rt", "speed"): L(380, 50, 840)})
def T4(*a): return a
m.T.update({
 ("df", "cover"): (("DOSAGE FORMS", "ওষুধের ধরন (ডোজ ফর্ম)"), ("Same medicine, <i>different forms</i>", "একই ওষুধ, <i>ভিন্ন ভিন্ন রূপ</i>"), (["Solids, liquids, topicals and inhaled forms, and why the form matters"], ["কঠিন, তরল, ত্বকে ও শ্বাসে ব্যবহারের রূপ, আর রূপ কেন গুরুত্বপূর্ণ"])),
 ("df", "solid"): (("SOLID ORAL FORMS", "কঠিন রূপ"), ("Tablets, capsules <i>and more</i>", "ট্যাবলেট, ক্যাপসুল <i>ও আরও</i>"), (["Tablets and capsules", "Blisters protect each dose", "Swallow as the label says"], ["ট্যাবলেট ও ক্যাপসুল", "ব্লিস্টারে প্রতিটি ডোজ সুরক্ষিত", "লেবেলের নিয়মে গিলুন"])),
 ("df", "liquid"): (("LIQUID FORMS", "তরল রূপ"), ("Measure liquids <i>with the right device</i>", "তরল ওষুধ মাপুন <i>সঠিক মাপক দিয়ে</i>"), (["Syrups, drops and suspensions", "Use the cup or syringe supplied", "Check the label before use"], ["সিরাপ, ড্রপ ও সাসপেনশন", "সঙ্গের কাপ বা সিরিঞ্জ ব্যবহার করুন", "ব্যবহারের আগে লেবেল দেখুন"])),
 ("df", "topical"): (("TOPICAL AND INHALED", "ত্বকে ও শ্বাসে"), ("Not every medicine is <i>swallowed</i>", "সব ওষুধ <i>গিলে খেতে হয় না</i>"), (["Creams, ointments and patches", "Nasal sprays and inhalers", "Use only as directed"], ["ক্রিম, মলম ও প্যাচ", "নাকের স্প্রে ও ইনহেলার", "নির্দেশনা মেনে ব্যবহার করুন"])),
 ("sr", "cover"): (("RELEASE DESIGNS", "ওষুধ ছাড়ার নকশা"), ("How medicines <i>release</i> over time", "সময়ের সঙ্গে ওষুধ <i>কীভাবে ছাড়ে</i>"), (["Immediate, sustained and enteric-coated medicines"], ["তাৎক্ষণিক, ধীর ও এন্টেরিক-কোটেড ওষুধ"])),
 ("sr", "checklist"): (("SAFE USE CHECKLIST", "নিরাপদ ব্যবহারের তালিকা"), ("Read the label, <i>ask if unsure</i>", "লেবেল পড়ুন, <i>সন্দেহ হলে জিজ্ঞাসা করুন</i>"), (["Check the product and form", "Take at the stated time", "Ask a doctor or pharmacist"], ["পণ্য ও রূপ দেখে নিন", "লেখা সময়ে সেবন করুন", "চিকিৎসক বা ফার্মাসিস্টকে জিজ্ঞাসা করুন"])),
 ("sr", "compare"): (("KEY DIFFERENCES", "মূল পার্থক্য"), ("Three designs, <i>three release patterns</i>", "তিন নকশা, <i>তিন রকম ছাড়ার ধরন</i>"), (["IR: releases soon after swallowing", "SR: releases over a longer time", "EC: designed to release beyond the stomach"], ["IR: গিলে ফেলার পরই ছাড়ে", "SR: দীর্ঘ সময় ধরে ছাড়ে", "EC: পাকস্থলী পেরিয়ে ছাড়ার নকশা"])),
 ("sr", "ir"): (("IMMEDIATE-RELEASE (IR)", "ইমিডিয়েট-রিলিজ (IR)"), ("IR releases <i>soon after swallowing</i>", "IR গিলে ফেলার <i>অল্পক্ষণ পরেই ছাড়ে</i>"), (["Conventional design", "Dissolves in the stomach", "May need more frequent doses"], ["প্রচলিত নকশা", "পাকস্থলীতে দ্রবীভূত হয়", "ঘন ঘন ডোজ লাগতে পারে"])),
 ("sr", "sr"): (("SUSTAINED-RELEASE (SR)", "সাস্টেইনড-রিলিজ (SR)"), ("SR releases <i>gradually</i>", "SR <i>ধীরে ধীরে</i> ছাড়ে"), (["Releases over a longer time", "May need fewer doses a day", "Do not crush or chew unless told"], ["দীর্ঘ সময় ধরে ছাড়ে", "দিনে কম ডোজ লাগতে পারে", "নির্দেশ ছাড়া গুঁড়ো বা চিবাবেন না"])),
 ("sr", "ec"): (("ENTERIC-COATED (EC)", "এন্টেরিক-কোটেড (EC)"), ("A coating that <i>resists stomach acid</i>", "আবরণ যা <i>পাকস্থলীর অ্যাসিড সামলায়</i>"), (["Designed to release in the intestine", "May protect the stomach or the drug", "Swallow whole unless advised"], ["অন্ত্রে ছাড়ার নকশা", "পাকস্থলী বা ওষুধকে রক্ষা করতে পারে", "পরামর্শ ছাড়া আস্ত গিলুন"])),
 ("sr", "abbr"): (("ON THE PACK", "প্যাকে যা লেখা থাকে"), ("IR, SR, EC: <i>read the code</i>", "IR, SR, EC: <i>সংক্ষেপটি পড়ুন</i>"), (["Codes can vary by brand", "Check the pack or ask"], ["ব্র্যান্ডভেদে সংক্ষেপ ভিন্ন হতে পারে", "প্যাক দেখুন বা জিজ্ঞাসা করুন"])),
 ("sr", "crush"): (("SPLIT, CRUSH OR OPEN?", "ভাঙা, গুঁড়ো বা খোলা?"), ("Do not crush <i>unless advised</i>", "পরামর্শ ছাড়া <i>গুঁড়ো করবেন না</i>"), (["Crushing can change release", "Check the label first"], ["গুঁড়ো করলে ছাড়ার ধরন বদলাতে পারে", "আগে লেবেল দেখুন"])),
 ("rt", "cover"): (("ROUTES OF ADMINISTRATION", "ওষুধ প্রয়োগের পথ"), ("How medicine <i>enters the body</i>", "ওষুধ <i>শরীরে ঢোকে</i> কীভাবে"), (["Oral, injected, inhaled, topical and other routes"], ["মুখে, ইনজেকশনে, শ্বাসে, ত্বকে ও অন্যান্য পথ"])),
 ("rt", "oral"): (("ORAL ROUTES", "মুখের পথ"), ("Swallowed, or <i>absorbed in the mouth</i>", "গিলে খাওয়া, অথবা <i>মুখেই শোষিত</i>"), (["Swallowed medicines pass through the gut", "Under-the-tongue forms act differently"], ["গিলে খাওয়া ওষুধ পরিপাকতন্ত্র দিয়ে যায়", "জিহ্বার নিচের ওষুধ ভিন্নভাবে কাজ করে"])),
 ("rt", "inh"): (("INHALED, NASAL, TOPICAL", "শ্বাস, নাক ও ত্বক"), ("Local sites, <i>different devices</i>", "স্থানীয় প্রয়োগ, <i>ভিন্ন ডিভাইস</i>"), (["Inhalers reach the airways", "Nasal sprays act in the nose", "Creams go on the skin"], ["ইনহেলার শ্বাসনালিতে পৌঁছায়", "নাকের স্প্রে নাকে কাজ করে", "ক্রিম ত্বকে লাগানো হয়"])),
 ("rt", "inj"): (("PARENTERAL ROUTES", "ইনজেকশন ও ইনফিউশন"), ("Injections go <i>around the gut</i>", "ইনজেকশন যায় <i>পরিপাকতন্ত্র এড়িয়ে</i>"), (["Muscle injection (IM)", "Intravenous infusion (IV)", "Given by trained staff"], ["মাংসপেশিতে ইনজেকশন (IM)", "শিরায় ইনফিউশন (IV)", "প্রশিক্ষিত কর্মী দেন"])),
 ("rt", "local"): (("OTHER LOCAL ROUTES", "অন্যান্য স্থানীয় পথ"), ("Eyes, ears <i>and other sites</i>", "চোখ, কান <i>ও অন্যান্য স্থান</i>"), (["Eye drops go in the eye", "Ear drops go in the ear"], ["চোখের ড্রপ চোখে", "কানের ড্রপ কানে"])),
 ("rt", "speed"): (("ROUTE AND ONSET", "পথ ও কাজ শুরুর সময়"), ("The route can <i>change the speed</i>", "পথ বদলালে <i>গতিও বদলায়</i>"), (["Onset generally varies by route", "It also depends on the medicine", "Illustration only, not a dosing guide"], ["কাজ শুরুর সময় সাধারণত পথভেদে ভিন্ন", "ওষুধের ধরনের ওপরও নির্ভর করে", "শুধু চিত্র; ডোজের নির্দেশিকা নয়"])),
})
m.SOC.update({
 "df": (("PHARMA BLOG · MEDICINE BASICS", "PHARMA BLOG · ওষুধের মৌলিক বিষয়"), ("Different Types of Medicine <i>Dosage Forms</i>: Tablets, Capsules, Liquids and More", "ওষুধের বিভিন্ন <i>Dosage Form</i>: ট্যাবলেট, ক্যাপসুল, সিরাপ ও আরও"), ("Solids, liquids, topicals and inhaled forms", "কঠিন, তরল, ত্বকে ও শ্বাসে ব্যবহারের রূপ")),
 "sr": (("PHARMA BLOG · MEDICINE BASICS", "PHARMA BLOG · ওষুধের মৌলিক বিষয়"), ("Immediate-Release vs Sustained-Release vs <i>Enteric-Coated</i> Medicines", "Immediate-Release, Sustained-Release ও <i>Enteric-Coated</i> ওষুধের পার্থক্য"), ("How release designs differ and why crushing can be unsafe", "ছাড়ার নকশা কীভাবে আলাদা এবং গুঁড়ো করা কেন অনিরাপদ হতে পারে")),
 "rt": (("PHARMA BLOG · MEDICINE BASICS", "PHARMA BLOG · ওষুধের মৌলিক বিষয়"), ("<i>Routes</i> of Drug Administration: Oral, Injection, Inhaled and More", "ওষুধ প্রয়োগের বিভিন্ন <i>Route</i>: মুখে, ইনজেকশন, ইনহেলার ও আরও"), ("How the route affects where and how a medicine acts", "পথভেদে ওষুধ কোথায় ও কীভাবে কাজ করে")),
})
m.SOCIAL_L.update({"df": (600, 60, 780), "sr": (540, 60, 780), "rt": (520, 60, 780)})
if __name__ == "__main__":
    only = set(sys.argv[1:]); stamp = []; tmp = BG / "_t.html"
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1300); pg.screenshot(path=str(out)); pg.close()
        for iid, (a, key) in M4.items():
            if only and a not in only and f"{a}-{key}" not in only: continue
            A = m.ART[a]; out = R / "assets/img/blog" / A["dir"]; out.mkdir(parents=True, exist_ok=True); bgp = BG / f"{a}-{key}.webp"
            Image.open(SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(m.main_html(a, key, lang, bgp), 1600, 900, png)
                dst = out / (f"{A['pre']}-{key}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); stamp.append([f"/assets/img/blog/{A['dir']}/{dst.name}", "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(m.social_html(a, lang, bgp), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"{A['pre']}-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en":
                        sm.save(out / f"{A['pre']}-card.webp", "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / f"{A['pre']}-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open("/tmp/stamp_q4.json", "w")); print(len(stamp), "images")
