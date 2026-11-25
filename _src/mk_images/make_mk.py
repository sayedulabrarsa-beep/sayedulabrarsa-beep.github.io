#!/usr/bin/env python3
"""Pharmaceutical Marketing Strategy article: 10 user-supplied text-free pictures -> 1600x900 WebP with titles written in code (EN + BN), plus share/card images. Reuses the Clinical Trial overlay engine."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "ct_images"))
import make_ct as ct
from PIL import Image
from playwright.sync_api import sync_playwright
R = ct.R
ct.SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/mk_images/bg"; OUT = R / "assets/img/blog/pharma-marketing-strategy"
ct.BG = BG; ct.OUT = OUT
ct.M = {"cover": "0edf8bc1", "context": "6f69eb2e", "research": "1adaf708", "segmentation": "8183fed1", "positioning": "af638429",
        "channels": "8d11ac7d", "plan": "c8a92626", "scorecard": "6fffbf5c", "ethics": "670fad61", "mistakes": "de3b190b"}
ct.T = {
 "cover": (("PHARMA MARKETING", "ফার্মা মার্কেটিং"), ("Pharmaceutical Marketing <i>Strategy</i> in Bangladesh", "বাংলাদেশে ফার্মাসিউটিক্যাল <i>মার্কেটিং কৌশল</i>"),
           ("A practical, ethical framework", "বাস্তবসম্মত ও নৈতিক পরিকল্পনা")),
 "context": (("WHY BANGLADESH", "কেন বাংলাদেশ"), ("A <i>market-specific</i> approach", "<i>বাজার-নির্দিষ্ট</i> দৃষ্টিভঙ্গি"), None),
 "research": (("MARKET ANALYSIS", "বাজার বিশ্লেষণ"), ("Start with <i>market analysis</i>", "শুরু হোক <i>বাজার বিশ্লেষণ</i> দিয়ে"), None),
 "segmentation": (("SEGMENTATION", "SEGMENTATION"), ("Segment around <i>relevant needs</i>", "<i>প্রাসঙ্গিক প্রয়োজন</i> ধরে segmentation"), None),
 "positioning": (("POSITIONING", "POSITIONING"), ("Position on <i>evidence</i>, not slogans", "slogan নয়, <i>evidence</i> থেকে positioning"), None),
 "channels": (("OBJECTIVES AND CHANNELS", "লক্ষ্য ও CHANNEL"), ("Clear objectives, <i>chosen channels</i>", "স্পষ্ট লক্ষ্য, <i>বিবেচিত channel</i>"), None),
 "plan": (("THE PLAN", "পরিকল্পনা"), ("One <i>coordinated</i> plan", "একটি <i>সমন্বিত</i> পরিকল্পনা"), None),
 "scorecard": (("MEASUREMENT", "পরিমাপ"), ("Measure more <i>than sales</i>", "বিক্রির চেয়ে <i>বেশি কিছু</i> পরিমাপ করুন"), None),
 "ethics": (("ETHICS AND REGULATION", "নৈতিকতা ও নিয়ন্ত্রণ"), ("Ethics is <i>part of strategy</i>", "নৈতিকতা <i>কৌশলেরই অংশ</i>"), None),
 "mistakes": (("AVOID THESE", "এড়িয়ে চলুন"), ("Common <i>strategic mistakes</i>", "সাধারণ <i>কৌশলগত ভুল</i>"), None),
}
ct.FONTS = (R / "_src/stability_images/fonts").as_uri()
def social_html(lang, bgpath):
    fam = "Sora" if lang == "en" else "NSB"
    kick = "PHARMA BLOG · MARKETING" if lang == "en" else "PHARMA BLOG · মার্কেটিং"
    if lang == "en":
        h = "Pharmaceutical Marketing<br><i>Strategy</i> in Bangladesh"; sub = "A practical, ethical framework"; by = "By Sayedul Abrar · Pharmacist"; fs = 39; lh = 1.15
    else:
        h = "ফার্মাসিউটিক্যাল<br><i>মার্কেটিং কৌশল</i>"; sub = "বাংলাদেশের জন্য বাস্তবসম্মত ও নৈতিক পরিকল্পনা"; by = "ফার্মাসিস্ট সাইয়্যেদুল আবরার"; fs = 42; lh = 1.3
    return ct.CSS + f"""<style>.s{{width:1200px;height:630px;font-family:{fam},sans-serif}}.s img{{left:80px;top:0;width:1120px;height:630px}}
.fade{{position:absolute;left:0;top:0;width:620px;height:630px;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 62%,rgba(247,241,230,0) 100%)}}
.k{{position:absolute;left:58px;top:56px;font:700 17px/1 {fam};letter-spacing:{'.1em' if lang=='en' else '0'};color:#17646a}}.bar{{position:absolute;left:58px;top:84px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
.h{{position:absolute;left:58px;top:108px;width:540px;font:800 {fs}px/{lh} {fam};color:#253238}}
.sub{{position:absolute;left:58px;top:{236 if lang=='en' else 256}px;width:420px;font:700 20px/1.45 {fam};color:#345}}
.by{{position:absolute;left:58px;top:{320 if lang=='en' else 350}px;font:700 18px/1 {fam};color:#fff;background:#17646a;padding:12px 22px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="fade"></div><div class="k">{kick}</div><div class="bar"></div><div class="h">{h}</div><div class="sub">{sub}</div><div class="by">{by}</div></div>"""
if __name__ == "__main__":
    for k, p in ct.M.items():
        Image.open(ct.SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(BG / f"mk-{k}.webp", "WEBP", quality=92, method=6)
    tmp = BG / "_t.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(out)); pg.close()
        for k in ct.M:
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(ct.main_html(k, lang, BG / f"mk-{k}.webp"), 1600, 900, png)
                dst = OUT / (f"mk-{k}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); print(dst.name, dst.stat().st_size // 1024, "KB")
        for lang in ("en", "bn"):
            png = BG / "_o.png"; shot(social_html(lang, BG / "mk-cover.webp"), 1200, 630, png)
            im = Image.open(png).convert("RGB"); im.save(OUT / f"mk-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            if lang == "en":
                im.save(OUT / "mk-card.webp", "WEBP", quality=84, method=6); im.resize((750, 394), Image.LANCZOS).save(OUT / "mk-card-w750.webp", "WEBP", quality=82, method=6)
        b.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
