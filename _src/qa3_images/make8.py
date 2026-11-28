#!/usr/bin/env python3
"""Pharma Industry (pi) and Generic vs Brand (gb): user text-free photos -> titled 1600x900 WebP (EN+BN), share image + card."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make7 as m7
m = m7.m
from PIL import Image
from playwright.sync_api import sync_playwright
R, BG, FD, LAT, BNG, face = m.R, m.BG, m.FD, m.LAT, m.BNG, m.face
FN = "_src/qa3_images/fonts"
def art(fam, lat, bn, ink, key, acc, veil, gold, hi):
    return dict(fam=f"'{fam}'", ink=ink, key=key, acc=acc, hi=hi, veil=veil, gold=gold, css="".join([face(fam, 800, FD(FN, lat + "-800-normal.woff2"), LAT), face(fam, 700, FD(FN, lat + "-700-normal.woff2"), LAT), face(fam, 800, FD(FN, bn + "-800-normal.woff2"), BNG), face(fam, 700, FD(FN, bn + "-700-normal.woff2"), BNG)]), lh=(1.14, 1.32), ls=".06em")
ARTS = {"pi": art("PIF", "outfit-latin", "baloo-da-2-bengali", "#12294A", "#D9480F", "#F5B700", "#EEF8F7", "#FFD66B", "rgba(245,183,0,.45)"),
        "gb": art("GBF", "bricolage-grotesque-latin", "baloo-da-2-bengali", "#2B1B3D", "#E4572E", "#FFC857", "#FFF3E4", "#FFD98A", "rgba(255,200,87,.5)")}
SETS = {
 "pi": {"dir": "pharma-industry", "ids": {"0a706af3": "cover", "92bd962b": "ind", "b569bbd2": "journey", "1af55b11": "types", "871ec577": "api", "69278095": "mfg", "42a09045": "qual", "8ac07808": "supply", "ef51964e": "who", "7ebb85d6": "take"},
   "Z": {"cover": (56, 130, 650, 640, False, False), "ind": (64, 60, 1472, 270, False, True), "journey": (64, 625, 1472, 250, False, True), "types": (930, 120, 600, 660, False, False), "api": (470, 36, 660, 330, False, False),
         "mfg": (50, 140, 520, 620, False, False), "qual": (40, 70, 470, 560, False, False), "supply": (940, 100, 600, 700, False, False), "who": (64, 640, 1472, 240, False, True), "take": (56, 120, 580, 660, False, False)},
   "T": {"cover": (("PHARMA INDUSTRY · BANGLADESH", "ফার্মা শিল্প · বাংলাদেশ"), ("How does the pharmaceutical industry <i>work in Bangladesh?</i>", "বাংলাদেশে ওষুধ শিল্প <i>কীভাবে কাজ করে?</i>"), (["From research and manufacturing to the pharmacy shelf."], ["গবেষণা ও উৎপাদন থেকে ফার্মেসির তাক পর্যন্ত।"])),
   "ind": (("1 · THE INDUSTRY", "১ · শিল্প"), ("What is the <i>pharmaceutical industry?</i>", "ফার্মাসিউটিক্যাল শিল্প <i>কী?</i>"), (["Research", "Manufacturing", "Quality checks", "Supply to pharmacies"], ["গবেষণা", "উৎপাদন", "মান যাচাই", "ফার্মেসিতে সরবরাহ"])),
   "journey": (("2 · THE JOURNEY", "২ · যাত্রা"), ("From idea <i>to patient</i>", "ধারণা থেকে <i>রোগীর কাছে</i>"), (["Research", "Lab testing", "Documentation", "Manufacturing", "Pharmacy"], ["গবেষণা", "ল্যাব পরীক্ষা", "নথিপত্র", "উৎপাদন", "ফার্মেসি"])),
   "types": (("3 · COMPANY TYPES", "৩ · কোম্পানির ধরন"), ("Types of <i>pharmaceutical companies</i>", "ফার্মাসিউটিক্যাল কোম্পানির <i>ধরন</i>"), (["Research and development", "Finished-product manufacturing", "Raw materials (API)", "Testing and analysis"], ["গবেষণা ও উন্নয়ন", "চূড়ান্ত পণ্য উৎপাদন", "কাঁচামাল (API)", "পরীক্ষা ও বিশ্লেষণ"])),
   "api": (("4 · API AND FPP", "৪ · API ও FPP"), ("API <i>vs finished product</i>", "API <i>বনাম চূড়ান্ত পণ্য</i>"), (["API: the active substance", "FPP: the finished product"], ["API: সক্রিয় উপাদান", "FPP: চূড়ান্ত পণ্য"])),
   "mfg": (("FACTORY FLOOR", "কারখানার মেঝে"), ("Inside a <i>manufacturing facility</i>", "উৎপাদন কারখানার <i>ভেতরে</i>"), (["Tablet press", "Coating", "Blister packing"], ["ট্যাবলেট প্রেস", "কোটিং", "ব্লিস্টার প্যাকিং"])),
   "qual": (("5 · QUALITY", "৫ · মান"), ("Quality and <i>safety</i>", "মান ও <i>নিরাপত্তা</i>"), (["GMP: the standards", "QA: planned prevention", "QC: tests and checks"], ["GMP: মানদণ্ড", "QA: পরিকল্পিত প্রতিরোধ", "QC: পরীক্ষা ও যাচাই"])),
   "supply": (("6 · SUPPLY CHAIN", "৬ · সরবরাহ শৃঙ্খল"), ("From factory <i>to pharmacy</i>", "কারখানা থেকে <i>ফার্মেসি</i>"), (["Manufacturer", "Warehouse and distribution", "Pharmacy"], ["উৎপাদক", "গুদাম ও বিতরণ", "ফার্মেসি"])),
   "who": (("7 · THE PEOPLE", "৭ · মানুষ"), ("Who <i>works</i> in the industry?", "এই শিল্পে <i>কারা</i> কাজ করেন?"), (["Pharmacist", "Lab scientist", "Production operator", "Quality analyst", "Sales and marketing"], ["ফার্মাসিস্ট", "ল্যাব বিজ্ঞানী", "উৎপাদন অপারেটর", "মান বিশ্লেষক", "সেলস ও মার্কেটিং"])),
   "take": (("KEY TAKEAWAYS", "মূল কথা"), ("Many roles, <i>one goal</i>", "অনেক ভূমিকা, <i>একই লক্ষ্য</i>"), (["Research becomes medicines", "Quality checks protect patients", "Many roles work together"], ["গবেষণা থেকে ওষুধ তৈরি হয়", "মান যাচাই রোগীকে সুরক্ষা দেয়", "অনেক পেশা একসঙ্গে কাজ করে"]))},
   "SOC": (("PHARMA BLOG · BANGLADESH", "PHARMA BLOG · বাংলাদেশ"), ("<i>Pharmaceutical Industry</i> in Bangladesh: How Does It Work?", "বাংলাদেশে <i>ওষুধ শিল্প</i> কীভাবে কাজ করে?"), ("From research to the pharmacy shelf", "গবেষণা থেকে ফার্মেসির তাক পর্যন্ত"))},
 "gb": {"dir": "generic-brand", "ids": {"f2752e39": "cover", "ac23bdc3": "rina", "7d4413c6": "ten", "53e1c652": "generic", "1dbe835b": "secret", "e33d2689": "layers", "435b6c55": "label", "caf05ded": "tricks", "c755497c": "quiz"},
   "Z": {"cover": (40, 120, 500, 660, False, False), "rina": (56, 130, 640, 640, False, False), "ten": (40, 150, 470, 600, False, False), "generic": (56, 140, 580, 620, False, False), "secret": (40, 140, 500, 620, False, False),
         "layers": (50, 130, 520, 640, False, False), "label": (50, 140, 540, 620, False, False), "tricks": (40, 140, 470, 620, False, False), "quiz": (50, 140, 520, 620, False, False)},
   "T": {"cover": (("GENERIC VS BRAND", "জেনেরিক বনাম ব্র্যান্ড"), ("Generic name <i>vs brand name</i>", "জেনেরিক নাম <i>বনাম ব্র্যান্ড নাম</i>"), (["Read any medicine label with confidence."], ["যেকোনো ওষুধের লেবেল আত্মবিশ্বাসে পড়ুন।"])),
   "rina": (("RINA'S STORY", "রিনার গল্প"), ("Two boxes, <i>one ingredient</i>", "দুটি বাক্স, <i>একই উপাদান</i>"), (["Different brand names", "Same active ingredient", "Unsure? Ask your pharmacist"], ["ভিন্ন ব্র্যান্ড নাম", "একই সক্রিয় উপাদান", "অনিশ্চিত হলে ফার্মাসিস্টকে জিজ্ঞাসা করুন"])),
   "ten": (("THE 10-SECOND TRICK", "১০ সেকেন্ডের কৌশল"), ("Find the <i>small name</i>", "ছোট <i>নামটি</i> খুঁজুন"), (["Big name: the brand", "Small name: the generic"], ["বড় নাম: ব্র্যান্ড", "ছোট নাম: জেনেরিক"])),
   "generic": (("WHAT IS IT?", "এটা কী?"), ("What is a <i>generic name?</i>", "জেনেরিক নাম <i>কী?</i>"), (["The name of the active ingredient", "Look for it on the pack"], ["সক্রিয় উপাদানের নাম", "প্যাকের গায়ে খুঁজে দেখুন"])),
   "secret": (("THE SECRET CODE", "গোপন সংকেত"), ("The code <i>inside the name</i>", "নামের <i>ভেতরের সংকেত</i>"), (["Name endings can hint at the drug class", "Example: Rabeprazole"], ["নামের শেষাংশ ওষুধের শ্রেণির ইঙ্গিত দিতে পারে", "উদাহরণ: Rabeprazole"])),
   "layers": (("THREE LAYERS", "তিন স্তর"), ("Ingredient, brand, <i>formulation</i>", "উপাদান, ব্র্যান্ড, <i>ফর্মুলেশন</i>"), (["Ingredient: the generic name", "Brand: the company's name", "Formulation: tablet, capsule and more"], ["উপাদান: জেনেরিক নাম", "ব্র্যান্ড: কোম্পানির দেওয়া নাম", "ফর্মুলেশন: ট্যাবলেট, ক্যাপসুল ইত্যাদি"])),
   "label": (("READ THE LABEL", "লেবেল পড়ুন"), ("Read a label <i>in 4 steps</i>", "লেবেল পড়ুন <i>৪ ধাপে</i>"), (["Generic name", "Strength", "Dosage form", "Manufacturer"], ["জেনেরিক নাম", "শক্তি (মাত্রা)", "ডোজ ফর্ম", "প্রস্তুতকারক"])),
   "tricks": (("EASY TRICKS", "সহজ কৌশল"), ("Remember it <i>in 4 tricks</i>", "মনে রাখুন <i>৪টি কৌশলে</i>"), (["Ingredient", "Brand", "Strength", "Form"], ["উপাদান", "ব্র্যান্ড", "শক্তি", "ফর্ম"])),
   "quiz": (("TEST YOURSELF", "নিজেকে যাচাই করুন"), ("A quick <i>3-question quiz</i>", "দ্রুত <i>৩ প্রশ্নের কুইজ</i>"), (["Myths and facts"], ["ভুল ধারণা ও সঠিক তথ্য"]))},
   "SOC": (("PHARMA BLOG · MEDICINE BASICS", "PHARMA BLOG · ওষুধের মূল কথা"), ("<i>Generic Name</i> vs Brand Name: How to Read a Medicine Label", "<i>জেনেরিক নাম</i> বনাম ব্র্যান্ড নাম: ওষুধের লেবেল পড়ার সহজ গাইড"), ("A simple guide for everyday medicine buyers", "সাধারণ মানুষের জন্য সহজ গাইড"))},
}
def body(S, key, lang, social=False):
    b = 1 if lang == "bn" else 0; BY = m.BY[b]
    if social:
        k, t, s = S["SOC"][0][b], S["SOC"][1][b], S["SOC"][2][b]; return m7.box(lang, k, t, [], 470, 50, 760, 420, True, sub=s, by=BY, uid="a") + m7.FITJS
    kick, title, rows = S["T"][key][0][b], S["T"][key][1][b], S["T"][key][2][b]
    x, y, w, h, dark, horiz = S["Z"][key]
    if key == "cover": return m7.box(lang, kick, title, [], x, y, w, h, dark, sub=rows[0], by=BY, uid="a") + m7.FITJS
    return m7.box(lang, kick, title, rows, x, y, w, h, dark, horiz, tf=50 if horiz else 56, uid="a") + m7.FITJS
def run(name):
    S = SETS[name]; m.ART["dm"] = ARTS[name]; stamp = []; tmp = BG / "_t.html"; out = R / f"assets/img/blog/{S['dir']}"; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, o):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1500); pg.screenshot(path=str(o)); pg.close()
        for iid, key in S["ids"].items():
            bgp = BG / f"{name}-{key}.webp"; Image.open(m.SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(m7.page(lang, body(S, key, lang), 1600, 900, bgp, 0), 1600, 900, png)
                dst = out / (f"{name}-{key}" + ("" if lang == "en" else "-bn") + ".webp"); Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); stamp.append([f"/assets/img/blog/{S['dir']}/{dst.name}", "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(m7.page(lang, body(S, key, lang, True), 1600, 840, bgp, -30), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"{name}-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en": sm.save(out / f"{name}-card.webp", "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / f"{name}-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open(f"/tmp/stamp_{name}.json", "w")); print(name, len(stamp), "images")
if __name__ == "__main__":
    run(sys.argv[1])
