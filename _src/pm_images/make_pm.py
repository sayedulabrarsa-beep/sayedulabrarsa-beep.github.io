#!/usr/bin/env python3
"""Pharmaceutical Product Management article: 12 user-supplied text-free photos -> 1600x900 WebP with title zone (kicker, title, points) in EN + BN, credit pill, plus share/card images."""
import pathlib, subprocess, sys, json
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/pm_images/bg"; OUT = R / "assets/img/blog/pharma-product-management"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"what": "0cc78cb8", "bangladesh": "a7c425db", "cover": "88b99a4e", "checklist": "57053424", "framework": "3ebaf3a6", "roles": "bac9ad9e",
     "kpi": "c94c1de9", "hcp": "115fb50a", "review": "8d57ce42", "career": "980cb023", "quality": "2c4adcac", "skills": "516efb1c"}
# L = left column on cream veil: (text width, title px EN, BN, chip px EN, BN); B = bottom band
LAY = {"cover": ("L", 520, 62, 55, 0, 0), "what": ("L", 520, 58, 52, 27, 25), "bangladesh": ("B",), "checklist": ("L", 400, 52, 47, 25, 23),
       "framework": ("L", 440, 56, 50, 26, 24), "roles": ("L", 450, 56, 50, 26, 24), "kpi": ("L", 440, 56, 50, 26, 24), "hcp": ("L", 440, 54, 48, 25, 23),
       "review": ("B",), "career": ("L", 440, 56, 50, 26, 24), "quality": ("L", 450, 56, 50, 26, 24), "skills": ("L", 440, 56, 50, 26, 24)}
T = {
 "cover": (("PRODUCT MANAGEMENT", "প্রোডাক্ট ম্যানেজমেন্ট"),
           ("From <i>market insight</i> to brand growth", "বাজারের সংকেত থেকে <i>ব্র্যান্ডের প্রবৃদ্ধি</i>"),
           (["Roles, planning, ethical engagement and KPIs in Bangladesh"], ["বাংলাদেশে কাজ, পরিকল্পনা, নৈতিক যোগাযোগ ও KPI"])),
 "what": (("WHAT IT IS", "এটি কী"), ("A brand is built by <i>more than promotion</i>", "ব্র্যান্ড গড়ে ওঠে <i>প্রচারের চেয়ে বেশি</i> কিছুতে"),
          (["Healthcare need and market data", "Positioning and availability", "Ethical, measurable execution"],
           ["স্বাস্থ্যসেবার প্রয়োজন ও বাজারের তথ্য", "positioning ও প্রাপ্যতা", "নৈতিক, পরিমাপযোগ্য বাস্তবায়ন"])),
 "bangladesh": (("WHY BANGLADESH", "কেন বাংলাদেশ"), ("Many brands, <i>one molecule</i>", "অনেক ব্র্যান্ড, <i>একই উপাদান</i>"),
                (["Differentiate on credible evidence", "Availability and service matter", "Compliance is part of the brand"],
                 ["বিশ্বাসযোগ্য evidence-এ পার্থক্য গড়ুন", "প্রাপ্যতা ও সেবা গুরুত্বপূর্ণ", "compliance ব্র্যান্ডেরই অংশ"])),
 "roles": (("CORE RESPONSIBILITIES", "প্রধান দায়িত্ব"), ("Five tools, <i>one brand plan</i>", "পাঁচটি উপকরণ, <i>একটি ব্র্যান্ড পরিকল্পনা</i>"),
           (["Clinical understanding", "Numbers and budgets", "Digital and field tools", "Records and review"],
            ["ক্লিনিক্যাল বোঝাপড়া", "সংখ্যা ও বাজেট", "ডিজিটাল ও field উপকরণ", "রেকর্ড ও review"])),
 "framework": (("SIX-STEP FRAMEWORK", "ছয় ধাপের কাঠামো"), ("Plan the brand <i>step by step</i>", "ব্র্যান্ড পরিকল্পনা <i>ধাপে ধাপে</i>"),
               (["Insight, then positioning", "Objectives, then plan", "Execute, measure, improve"],
                ["আগে insight, তারপর positioning", "আগে লক্ষ্য, তারপর পরিকল্পনা", "বাস্তবায়ন, পরিমাপ, উন্নয়ন"])),
 "checklist": (("ONE-PAGE CHECKLIST", "এক পাতার চেকলিস্ট"), ("Check the plan <i>before</i> you act", "কাজের <i>আগেই</i> পরিকল্পনা যাচাই"),
               (["Objective and audience", "Evidence and approvals", "Owner and timeline"],
                ["লক্ষ্য ও audience", "evidence ও অনুমোদন", "দায়িত্বশীল ও সময়সূচি"])),
 "hcp": (("ETHICAL ENGAGEMENT", "নৈতিক যোগাযোগ"), ("Respect for the <i>doctor's time</i> and judgement", "চিকিৎসকের <i>সময় ও বিবেচনার</i> প্রতি শ্রদ্ধা"),
         (["Approved, current information", "Professional data only", "Science, not inducements"],
          ["অনুমোদিত, হালনাগাদ তথ্য", "শুধু পেশাগত তথ্য", "বিজ্ঞান, প্রলোভন নয়"])),
 "kpi": (("KPIs", "KPI"), ("Measure <i>more than sales</i>", "বিক্রির চেয়ে <i>বেশি কিছু</i> মাপুন"),
         (["Growth and market share", "Availability and access", "Engagement quality and compliance"],
          ["প্রবৃদ্ধি ও market share", "প্রাপ্যতা ও সহজলভ্যতা", "সম্পৃক্ততার মান ও compliance"])),
 "skills": (("SKILLS", "দক্ষতা"), ("A toolkit that <i>combines</i> science and business", "বিজ্ঞান ও ব্যবসাকে <i>মেলানো</i> উপকরণ"),
            (["Scientific knowledge", "Data analysis", "Communication and planning"],
             ["বৈজ্ঞানিক জ্ঞান", "ডেটা বিশ্লেষণ", "যোগাযোগ ও পরিকল্পনা"])),
 "quality": (("REGULATION AND QUALITY", "নিয়ম ও মান"), ("A great brand starts with a <i>quality</i> product", "ভালো ব্র্যান্ডের শুরু <i>মানসম্মত</i> পণ্যে"),
             (["Follow approved information", "Respect GMP and supply quality", "No claim beyond evidence"],
              ["অনুমোদিত তথ্য মেনে চলুন", "GMP ও সরবরাহের মান মানুন", "evidence-এর বেশি claim নয়"])),
 "career": (("FROM PHARMACY TO PMD", "ফার্মেসি থেকে PMD"), ("Your pharmacy degree is <i>a strong start</i>", "ফার্মেসির ডিগ্রি <i>একটি শক্ত শুরু</i>"),
            (["Add marketing and data skills", "Learn how the market works", "Build communication habits"],
             ["marketing ও ডেটা দক্ষতা যোগ করুন", "বাজার কীভাবে চলে শিখুন", "যোগাযোগের অভ্যাস গড়ুন"])),
 "review": (("MONTHLY PMD REVIEW", "মাসিক PMD review"), ("Review, decide, <i>improve</i>", "পর্যালোচনা, সিদ্ধান্ত, <i>উন্নয়ন</i>"),
            (["Share the data", "Agree actions and owners", "Check results next month"],
             ["ডেটা সবার সঙ্গে ভাগ করুন", "কাজ ও দায়িত্বশীল ঠিক করুন", "পরের মাসে ফল দেখুন"])),
}
CSS = f"""<meta charset="utf-8"><style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;overflow:hidden;background:#F7F1E6}}.s img{{position:absolute}}
</style>"""
MAXT = 92
def main_html(key, lang, bgpath):
    b = 0 if lang == "en" else 1; fam = "Sora" if lang == "en" else "NSB"
    kick, title, chips = T[key][0][b], T[key][1][b], T[key][2][b]
    lay = LAY[key]; lh = 1.14 if lang == "en" else 1.34; ls = ".12em" if lang == "en" else "0"
    base = f"<style>:root{{--s:1}}.s{{width:1600px;height:900px;font-family:{fam},sans-serif}}.s img{{left:0;top:0;width:1600px;height:900px}}</style>"
    if lay[0] == "L":
        _, tw, fe, fb, ce, cb = lay; fs = fe if lang == "en" else fb; cp = ce if lang == "en" else cb
        if key == "cover":
            ch = f'<div class="sub">{chips[0]}</div><div class="by">{"By Sayedul Abrar · Pharmacist" if lang=="en" else "ফার্মাসিস্ট সাইয়্যেদুল আবরার"}</div>'
        else:
            ch = '<div class="ch">' + "".join(f'<div class="c">{c}</div>' for c in chips) + "</div>"
        veil = tw + 64; kfs = 25 if lang == "en" else 31
        return CSS + base + f"""<style>.v{{position:absolute;left:0;top:0;width:{veil+150}px;height:900px;background:linear-gradient(90deg,#F7F1E6 0,rgba(247,241,230,.97) {veil}px,rgba(247,241,230,0) 100%)}}
.t{{position:absolute;left:64px;top:0;width:{tw}px;height:900px;display:flex;flex-direction:column;justify-content:center}}.in{{display:flex;flex-direction:column}}
.k{{font:800 calc(var(--s)*{kfs}px)/1.1 {fam};letter-spacing:{ls};color:#174F52}}.bar{{width:calc(var(--s)*104px);height:calc(var(--s)*8px);border-radius:4px;background:#D8A84E;margin:calc(var(--s)*18px) 0 calc(var(--s)*26px)}}
.h{{font:800 calc(var(--s)*{fs}px)/{lh} {fam};color:#253238}}.h i{{font-style:normal;color:#174F52;box-shadow:inset 0 -.32em 0 rgba(216,168,78,.55)}}
.ch{{margin-top:calc(var(--s)*32px);display:flex;flex-direction:column;gap:calc(var(--s)*14px)}}.c{{background:#fff;border-left:calc(var(--s)*8px) solid #174F52;border-bottom:calc(var(--s)*4px) solid #D8A84E;border-radius:10px;padding:calc(var(--s)*14px) calc(var(--s)*20px);font:700 calc(var(--s)*{cp}px)/1.38 {fam};color:#253238;box-shadow:0 4px 14px rgba(23,79,82,.12)}}
.sub{{margin-top:calc(var(--s)*26px);font:700 calc(var(--s)*28px)/1.45 {fam};color:#253238}}.by{{margin-top:calc(var(--s)*30px);align-self:flex-start;white-space:nowrap;font:700 calc(var(--s)*24px)/1 {fam};color:#fff;background:#253238;padding:calc(var(--s)*16px) calc(var(--s)*30px);border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="v"></div><div class="t"><div class="in" id="in"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div>{ch}</div></div></div>
<script>document.fonts.ready.then(function(){{var r=document.documentElement,e=document.getElementById("in"),best=1;for(var s=1;s<=2.6;s+=0.02){{r.style.setProperty("--s",s);if(e.getBoundingClientRect().height>715||e.scrollWidth>{tw}+2||{fs}*s>{MAXT})break;best=s}}r.style.setProperty("--s",best)}});</script>"""
    fs = 62 if lang == "en" else 68; cp = 27 if lang == "en" else 29; kf = 24 if lang == "en" else 30
    return CSS + base + f"""<style>.bd{{position:absolute;left:0;bottom:0;width:1600px;height:330px;background:linear-gradient(180deg,rgba(37,50,56,0) 0,rgba(37,50,56,.93) 40px,rgba(37,50,56,.96) 100%)}}
.l{{position:absolute;left:64px;bottom:44px;width:780px}}.k{{font:700 {kf}px/1 {fam};letter-spacing:{ls};color:#F2CF86}}.bar{{width:84px;height:6px;border-radius:3px;background:#D8A84E;margin:14px 0 18px}}
.h{{font:800 {fs}px/{lh} {fam};color:#fff}}.h i{{font-style:normal;color:#F2CF86}}
.r{{position:absolute;right:64px;bottom:44px;width:640px;display:flex;flex-direction:column;gap:12px}}.c{{background:rgba(255,255,255,.96);border-left:7px solid #174F52;border-bottom:3px solid #D8A84E;border-radius:10px;padding:12px 18px;font:700 {cp}px/1.35 {fam};color:#253238}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="bd"></div><div class="l"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div></div>
<div class="r">{"".join(f'<div class="c">{c}</div>' for c in chips)}</div></div>"""
def social_html(lang, bgpath):
    fam = "Sora" if lang == "en" else "NSB"
    kick = "PHARMA BLOG · PRODUCT MANAGEMENT" if lang == "en" else "PHARMA BLOG · প্রোডাক্ট ম্যানেজমেন্ট"
    if lang == "en":
        h = "Pharmaceutical<br>Product Management<br>in <i>Bangladesh</i>"; sub = "From market insight to brand growth"; by = "By Sayedul Abrar · Pharmacist"; fs = 40; lh = 1.16
    else:
        h = "ফার্মাসিউটিক্যাল<br>প্রোডাক্ট ম্যানেজমেন্ট:<br><i>কাজ, কৌশল ও দায়িত্ব</i>"; sub = "বাজারের সংকেত থেকে ব্র্যান্ডের প্রবৃদ্ধি"; by = "ফার্মাসিস্ট সাইয়্যেদুল আবরার"; fs = 37; lh = 1.3
    return CSS + f"""<style>.s{{width:1200px;height:630px;font-family:{fam},sans-serif}}.s img{{left:60px;top:0;width:1120px;height:630px}}
.fade{{position:absolute;left:0;top:0;width:640px;height:630px;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 66%,rgba(247,241,230,0) 100%)}}
.k{{position:absolute;left:52px;top:56px;font:700 17px/1 {fam};letter-spacing:{'.09em' if lang=='en' else '0'};color:#174F52}}.bar{{position:absolute;left:52px;top:84px;width:74px;height:5px;border-radius:3px;background:#D8A84E}}
.h{{position:absolute;left:52px;top:108px;width:560px;font:800 {fs}px/{lh} {fam};color:#253238}}.h i{{font-style:normal;color:#174F52;box-shadow:inset 0 -.3em 0 rgba(216,168,78,.55)}}
.sub{{position:absolute;left:52px;top:{318 if lang=='en' else 328}px;width:480px;font:700 20px/1.45 {fam};color:#345}}
.by{{position:absolute;left:52px;top:{392 if lang=='en' else 396}px;font:700 18px/1 {fam};color:#fff;background:#253238;padding:12px 22px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="fade"></div><div class="k">{kick}</div><div class="bar"></div><div class="h">{h}</div><div class="sub">{sub}</div><div class="by">{by}</div></div>"""
if __name__ == "__main__":
    for k, p in M.items():
        Image.open(SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(BG / f"pm-{k}.webp", "WEBP", quality=92, method=6)
    tmp = BG / "_t.html"; made = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1200); pg.screenshot(path=str(out)); pg.close()
        for k in M:
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(main_html(k, lang, BG / f"pm-{k}.webp"), 1600, 900, png)
                dst = OUT / (f"pm-{k}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); made.append(["/assets/img/blog/pharma-product-management/" + dst.name, "tr" if k in ("bangladesh", "review") else "br"])
        for lang in ("en", "bn"):
            png = BG / "_o.png"; shot(social_html(lang, BG / "pm-cover.webp"), 1200, 630, png)
            im = Image.open(png).convert("RGB"); im.save(OUT / f"pm-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            if lang == "en":
                im.save(OUT / "pm-card.webp", "WEBP", quality=84, method=6); im.resize((750, 394), Image.LANCZOS).save(OUT / "pm-card-w750.webp", "WEBP", quality=82, method=6)
        b.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(made, open("/tmp/stamp_pm.json", "w"))
