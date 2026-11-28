#!/usr/bin/env python3
"""How to read a medicine label (lb): 10 user pictures. 5 Finix label pictures already carry their own text and are used as they are ("N" layout); 5 text-free photos get titles. Reuses make3/make5."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make3 as m
import make5 as m5
from PIL import Image
from playwright.sync_api import sync_playwright
R, BG, FD, LAT, BNG, face = m.R, m.BG, m.FD, m.LAT, m.BNG, m.face
FN = "_src/qa3_images/fonts"
m.ART["lb"] = dict(dir="medicine-label", pre="lb", fam="'LBF'", ink="#2B3A12", key="#4E7D1E", acc="#F57C00", hi="rgba(245,124,0,.42)", veil="#FBF4E4", pill="#2B3A12", bandrgb="43,58,18", gold="#FFD27A",
  css="".join([face("LBF", 800, FD(FN, "rubik-latin-800-normal.woff2"), LAT), face("LBF", 600, FD(FN, "rubik-latin-600-normal.woff2"), LAT), face("LBF", 800, FD(FN, "noto-sans-bengali-bengali-800-normal.woff2"), BNG), face("LBF", 600, FD(FN, "noto-sans-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.12, 1.34), ls=".08em")
IDS = {"65b25680": "cover", "36512531": "which", "765afb4b": "brand", "b8ccbd8e": "strength", "845982e6": "dirs", "4e4f431c": "warn", "bb7f0c1c": "dates", "6dc034ff": "storage", "5f09d0de": "checklist", "e544a770": "takeaways"}
L = lambda tw, y0, y1: ("L", tw, y0, y1); N = ("N",)
m.LAY.update({("lb", "cover"): L(560, 60, 840), ("lb", "which"): L(520, 60, 840), ("lb", "dirs"): L(520, 60, 840), ("lb", "checklist"): L(520, 60, 840), ("lb", "takeaways"): L(520, 60, 840),
  ("lb", "brand"): N, ("lb", "strength"): N, ("lb", "warn"): N, ("lb", "dates"): N, ("lb", "storage"): N})
m.T.update({
 ("lb", "cover"): (("MEDICINE LABEL", "ওষুধের লেবেল"), ("Read the label <i>before you take it</i>", "ওষুধ খাওয়ার আগে <i>লেবেল পড়ুন</i>"), (["Name, strength, directions, warnings, dates and storage on a medicine pack"], ["ওষুধের প্যাকে নাম, শক্তি, নির্দেশনা, সতর্কতা, তারিখ ও সংরক্ষণ"])),
 ("lb", "which"): (("KNOW YOUR LABEL", "লেবেল চিনুন"), ("Which <i>label</i> are you reading?", "আপনি কোন <i>লেবেল</i> পড়ছেন?"), (["Outer carton", "Strip or bottle", "Leaflet"], ["বাইরের কার্টন", "স্ট্রিপ বা বোতল", "লিফলেট"])),
 ("lb", "dirs"): (("DIRECTIONS", "নির্দেশনা"), ("How much, how often, <i>how long</i>", "কতটুকু, কতবার, <i>কতদিন</i>"), (["Follow the prescriber's directions", "Ask if anything is unclear"], ["চিকিৎসকের নির্দেশ মেনে চলুন", "অস্পষ্ট হলে জিজ্ঞাসা করুন"])),
 ("lb", "checklist"): (("QUICK CHECK", "দ্রুত যাচাই"), ("A simple <i>label checklist</i>", "লেবেলের সহজ <i>চেকলিস্ট</i>"), (["Name and strength", "Directions and warnings", "MFG, EXP and batch", "Storage and pack"], ["নাম ও শক্তি", "নির্দেশনা ও সতর্কতা", "MFG, EXP ও ব্যাচ", "সংরক্ষণ ও প্যাক"])),
 ("lb", "takeaways"): (("KEY TAKEAWAYS", "মূল কথা"), ("Read it, <i>check it</i>, ask if unsure", "পড়ুন, <i>মিলিয়ে দেখুন</i>, সন্দেহে জিজ্ঞাসা করুন"), (["Check name, strength and directions", "Check dates, batch and storage", "Ask a pharmacist when in doubt"], ["নাম, শক্তি ও নির্দেশনা দেখুন", "তারিখ, ব্যাচ ও সংরক্ষণ দেখুন", "সন্দেহ হলে ফার্মাসিস্টকে জিজ্ঞাসা করুন"])),
})
m.SOC["lb"] = (("PHARMA BLOG · MEDICINE SAFETY", "PHARMA BLOG · ওষুধের নিরাপত্তা"), ("How to Read a <i>Medicine Label</i>", "<i>ওষুধের লেবেল</i> কীভাবে পড়বেন"), ("Name, strength, directions, warnings, dates and storage", "নাম, শক্তি, নির্দেশনা, সতর্কতা, তারিখ ও সংরক্ষণ"))
m.SOCIAL_L["lb"] = (520, 60, 780)
if __name__ == "__main__":
    stamp = []; tmp = BG / "_t.html"
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1300); pg.screenshot(path=str(out)); pg.close()
        A = m.ART["lb"]; out = R / "assets/img/blog" / A["dir"]; out.mkdir(parents=True, exist_ok=True)
        for iid, key in IDS.items():
            bgp = BG / f"lb-{key}.webp"
            Image.open(m.SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                dst = out / (f"lb-{key}" + ("" if lang == "en" else "-bn") + ".webp")
                if key in ("brand", "strength", "warn", "dates", "storage"):
                    Image.open(bgp).convert("RGB").save(dst, "WEBP", quality=88, method=6)  # as supplied, English text baked in
                else:
                    png = BG / "_o.png"; shot(m5.main_html("lb", key, lang, bgp), 1600, 900, png); Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6)
                stamp.append([f"/assets/img/blog/{A['dir']}/{dst.name}", "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(m5.social_html("lb", lang, bgp), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"lb-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en": sm.save(out / "lb-card.webp", "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / "lb-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open("/tmp/stamp_q6.json", "w")); print(len(stamp), "images")
