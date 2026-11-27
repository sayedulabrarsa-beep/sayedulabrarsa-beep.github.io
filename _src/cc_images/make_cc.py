#!/usr/bin/env python3
"""Cold Chain article: 10 user-supplied text-free photos -> 1600x900 WebP with a bold headline zone (kicker, title, points) in EN + BN, plus share/card images."""
import pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/cc_images/bg"; OUT = R / "assets/img/blog/cold-chain"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"cover": "1055a79b", "what": "73c34ae3", "which": "c76e2e79", "why": "ba9a843f", "how": "27022cec", "key": "1b422742",
     "monitor": "79e3a85f", "excursion": "664c0a97", "bangladesh": "04b7e445", "advice": "0b7a516c"}
# (text width, title px EN, title px BN, chip px EN, chip px BN)
LAY = {"cover": (545, 64, 56, 0, 0), "what": (520, 60, 54, 28, 26), "which": (400, 52, 47, 25, 23), "why": (560, 58, 52, 28, 26),
       "how": (410, 54, 48, 25, 23), "key": (470, 58, 52, 27, 25), "monitor": (400, 52, 47, 25, 23), "excursion": (480, 62, 56, 28, 26),
       "bangladesh": (440, 50, 45, 25, 23), "advice": (450, 56, 50, 26, 24)}
T = {
 "cover": (("COLD CHAIN", "কোল্ড চেইন"),
           ("Protecting <i>temperature‑sensitive</i> medicines at every hand‑off", "তাপমাত্রা-সংবেদনশীল ওষুধ সুরক্ষিত রাখুন প্রতিটি <i>হাত-বদলে</i>"),
           (["Storage ranges, monitoring and excursion response"], ["সংরক্ষণের সীমা, পর্যবেক্ষণ ও excursion-এর পরবর্তী পদক্ষেপ"])),
 "what": (("WHAT IS IT", "এটি কী"), ("A chain of <i>controls</i>, not one refrigerator", "একটি ফ্রিজ নয়, <i>নিয়ন্ত্রণের</i> ধারা"),
          (["Manufacturer to patient", "Every hand-off matters", "Backed by stability data"],
           ["উৎপাদনকারী থেকে রোগী পর্যন্ত", "প্রতিটি হাত-বদল গুরুত্বপূর্ণ", "স্থিতিশীলতার ডেটার ওপর ভিত্তি করে"])),
 "which": (("WHICH MEDICINES", "কোন ওষুধ"), ("Not every medicine needs the <i>fridge</i>", "সব ওষুধ <i>ফ্রিজে</i> রাখতে হয় না"),
           (["Vaccines, insulin, some biologics", "Rules vary by product and stage", "Check the carton and leaflet"],
            ["ভ্যাকসিন, ইনসুলিন, কিছু বায়োলজিক", "নিয়ম পণ্য ও পর্যায়ভেদে আলাদা", "কার্টন ও লিফলেট দেখুন"])),
 "why": (("WHY IT MATTERS", "কেন গুরুত্বপূর্ণ"), ("It can look normal while <i>potency</i> has changed", "দেখতে স্বাভাবিক হলেও <i>কার্যকারিতা</i> বদলে যেতে পারে"),
         (["Heat can speed up degradation", "Freezing can damage some products", "Appearance alone can't confirm quality"],
          ["তাপ ক্ষয় ত্বরান্বিত করতে পারে", "জমে গেলে কিছু পণ্যের ক্ষতি হতে পারে", "শুধু দেখে মান নিশ্চিত করা যায় না"])),
 "how": (("HOW IT WORKS", "কীভাবে কাজ করে"), ("Transport is part of the <i>chain</i>", "পরিবহনও <i>চেইনের</i> অংশ"),
         (["Refrigerated vehicle or validated shipper", "A data logger records conditions", "Records checked at receipt"],
          ["রেফ্রিজারেটেড যান বা validated শিপার", "ডেটা লগার অবস্থা রেকর্ড করে", "গ্রহণের সময় রেকর্ড যাচাই"])),
 "key": (("KEY TAKEAWAYS", "মূল কথা"), ("Protect the <i>whole</i> journey", "পুরো <i>যাত্রা</i> সুরক্ষিত রাখুন"),
         (["Storage limits are product-specific", "Monitor, record and hold excursions", "Decisions rest on stability data"],
          ["সংরক্ষণের সীমা পণ্যভেদে আলাদা", "পর্যবেক্ষণ, রেকর্ড ও excursion আটকে রাখা", "সিদ্ধান্ত স্থিতিশীলতার ডেটার ওপর নির্ভর করে"])),
 "monitor": (("MONITORING", "পর্যবেক্ষণ"), ("A thermometer shows a moment, a <i>logger</i> the trace", "থার্মোমিটার এক মুহূর্ত দেখায়, <i>লগার</i> পুরো ধারা"),
             (["One reading vs a record over time", "Calibrate, map and review"], ["একটি রিডিং বনাম সময়ের রেকর্ড", "ক্যালিব্রেট, ম্যাপ ও রেকর্ড পর্যালোচনা"])),
 "excursion": (("EXCURSION", "এক্সকার্শন"), ("Out of range? <i>Hold</i> it first", "সীমার বাইরে? আগে <i>আটকে</i> রাখুন"),
               (["Segregate the batch", "Record the evidence", "QA and the manufacturer advise"], ["ব্যাচ আলাদা করুন", "প্রমাণ রেকর্ড করুন", "QA ও উৎপাদনকারীর পরামর্শ নিন"])),
 "bangladesh": (("BANGLADESH", "বাংলাদেশ"), ("In a warm climate, <i>records</i> and equipment matter", "উষ্ণ আবহাওয়ায় <i>রেকর্ড</i> ও যন্ত্র গুরুত্বপূর্ণ"),
                (["Model Pharmacy checks storage temperature", "Pharmacy-grade refrigerator", "The product label remains the reference"],
                 ["Model Pharmacy-তে সংরক্ষণের তাপমাত্রা যাচাই", "ফার্মেসি-গ্রেড রেফ্রিজারেটর", "পণ্যের লেবেলই মূল নির্দেশিকা"])),
 "advice": (("PRACTICAL ADVICE", "ব্যবহারিক পরামর্শ"), ("Read the <i>label</i> before you store", "সংরক্ষণের আগে <i>লেবেল</i> পড়ুন"),
            (["Don't refrigerate every injection", "Use monitored equipment and logs", "Patients: follow the carton and leaflet"],
             ["সব ইনজেকশন ফ্রিজে রাখবেন না", "মনিটরড যন্ত্র ও লগ ব্যবহার করুন", "রোগী: কার্টন ও লিফলেট অনুসরণ করুন"])),
}
MAXT = 92
CSS = f"""<meta charset="utf-8"><style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;overflow:hidden;background:#F7F1E6}}.s img{{position:absolute}}
</style>"""

def main_html(key, lang, bgpath):
    b = 0 if lang == "en" else 1; fam = "Sora" if lang == "en" else "NSB"
    kick, title, chips = T[key][0][b], T[key][1][b], T[key][2][b]
    tw, fe, fb, ce, cb = LAY[key]; fs = fe if lang == "en" else fb; cp = ce if lang == "en" else cb
    lh = 1.14 if lang == "en" else 1.34; ls = ".12em" if lang == "en" else "0"
    if key == "cover":
        ch = f'<div class="sub">{chips[0]}</div><div class="by">{"By Sayedul Abrar · Pharmacist" if lang=="en" else "ফার্মাসিস্ট সাইয়্যেদুল আবরার"}</div>'
    else:
        ch = '<div class="ch">' + "".join(f'<div class="c">{c}</div>' for c in chips) + "</div>"
    veil = tw + 64
    kfs = 25 if lang == "en" else 31
    return CSS + f"""<style>:root{{--s:1}}.s{{width:1600px;height:900px;font-family:{fam},sans-serif}}.s img{{left:0;top:0;width:1600px;height:900px}}
.v{{position:absolute;left:0;top:0;width:{veil+150}px;height:900px;background:linear-gradient(90deg,#F7F1E6 0,rgba(247,241,230,.97) {veil}px,rgba(247,241,230,0) 100%)}}
.t{{position:absolute;left:64px;top:0;width:{tw}px;height:900px;display:flex;flex-direction:column;justify-content:center}}
.in{{display:flex;flex-direction:column}}
.k{{font:800 calc(var(--s)*{kfs}px)/1.1 {fam};letter-spacing:{ls};color:#526D82}}.bar{{width:calc(var(--s)*104px);height:calc(var(--s)*8px);border-radius:4px;background:#E98250;margin:calc(var(--s)*18px) 0 calc(var(--s)*26px)}}
.h{{font:800 calc(var(--s)*{fs}px)/{lh} {fam};color:#174F52}}.h i{{font-style:normal;color:#d9532f}}
.ch{{margin-top:calc(var(--s)*32px);display:flex;flex-direction:column;gap:calc(var(--s)*14px)}}.c{{background:#DCEBE7;border-left:calc(var(--s)*8px) solid #526D82;border-radius:10px;padding:calc(var(--s)*14px) calc(var(--s)*20px);font:700 calc(var(--s)*{cp}px)/1.38 {fam};color:#1f2e33}}
.sub{{margin-top:calc(var(--s)*26px);font:700 calc(var(--s)*28px)/1.45 {fam};color:#253238}}.by{{margin-top:calc(var(--s)*30px);align-self:flex-start;white-space:nowrap;font:700 calc(var(--s)*24px)/1 {fam};color:#fff;background:#174F52;padding:calc(var(--s)*16px) calc(var(--s)*30px);border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="v"></div><div class="t"><div class="in" id="in"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div>{ch}</div></div></div>
<script>document.fonts.ready.then(function(){{var r=document.documentElement,e=document.getElementById("in"),best=1;for(var s=1;s<=2.6;s+=0.02){{r.style.setProperty("--s",s);if(e.getBoundingClientRect().height>715||e.scrollWidth>{tw}+2||{fs}*s>{MAXT})break;best=s}}r.style.setProperty("--s",best)}});</script>"""

def social_html(lang, bgpath):
    fam = "Sora" if lang == "en" else "NSB"
    if lang == "en":
        kick = "PHARMA BLOG · PHARMACEUTICAL QUALITY"; h = "Pharmaceutical<br><i>Cold Chain</i>:<br>Stored and Transported"; sub = "How temperature-sensitive medicines are protected"; by = "By Sayedul Abrar · Pharmacist"; fs = 44; lh = 1.16
    else:
        kick = "PHARMA BLOG · ফার্মাসিউটিক্যাল কোয়ালিটি"; h = "ফার্মাসিউটিক্যাল<br><i>কোল্ড চেইন</i>:<br>সংরক্ষণ ও পরিবহন"; sub = "তাপমাত্রা-সংবেদনশীল ওষুধ কীভাবে সুরক্ষিত থাকে"; by = "ফার্মাসিস্ট সাইয়্যেদুল আবরার"; fs = 40; lh = 1.32
    return CSS + f"""<style>.s{{width:1200px;height:630px;font-family:{fam},sans-serif}}.s img{{left:60px;top:0;width:1120px;height:630px}}
.fade{{position:absolute;left:0;top:0;width:640px;height:630px;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 66%,rgba(247,241,230,0) 100%)}}
.k{{position:absolute;left:52px;top:98px;font:800 17px/1 {fam};letter-spacing:{'.09em' if lang=='en' else '0'};color:#526D82}}.bar{{position:absolute;left:52px;top:126px;width:74px;height:5px;border-radius:3px;background:#E98250}}
.h{{position:absolute;left:52px;top:150px;width:560px;font:800 {fs}px/{lh} {fam};color:#174F52}}.h i{{font-style:normal;color:#d9532f}}
.sub{{position:absolute;left:52px;top:{340 if lang=='en' else 332}px;width:480px;font:700 20px/1.45 {fam};color:#253238}}
.by{{position:absolute;left:52px;top:{420 if lang=='en' else 410}px;font:700 18px/1 {fam};color:#fff;background:#174F52;padding:12px 22px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="fade"></div><div class="k">{kick}</div><div class="bar"></div><div class="h">{h}</div><div class="sub">{sub}</div><div class="by">{by}</div></div>"""

if __name__ == "__main__":
    for k, p in M.items():
        Image.open(SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(BG / f"cc-{k}.webp", "WEBP", quality=92, method=6)
    tmp = BG / "_t.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1200)
            pg.screenshot(path=str(out)); pg.close()
        for k in M:
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(main_html(k, lang, BG / f"cc-{k}.webp"), 1600, 900, png)
                dst = OUT / (f"cc-{k}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); print(dst.name, dst.stat().st_size // 1024, "KB")
        for lang in ("en", "bn"):
            png = BG / "_o.png"; shot(social_html(lang, BG / "cc-cover.webp"), 1200, 630, png)
            im = Image.open(png).convert("RGB"); im.save(OUT / f"cc-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            if lang == "en":
                im.save(OUT / "cc-card.webp", "WEBP", quality=84, method=6)
                im.resize((750, 394), Image.LANCZOS).save(OUT / "cc-card-w750.webp", "WEBP", quality=82, method=6)
        b.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
