#!/usr/bin/env python3
"""Pharmacogenetics article: 10 user-supplied text-free photos -> 1600x900 WebP with a filled title zone (kicker, title, short points) in EN + BN, plus share/card images."""
import pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/px_images/bg"; OUT = R / "assets/img/blog/pharmacogenetics"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"cover": "03f18405", "what": "fb81af49", "same": "c9592c7b", "pathways": "25cc1186", "types": "9476ef6a",
     "prodrug": "992eb7ba", "test": "d1cbe48d", "care": "c9ede010", "bangladesh": "f753c76e", "key": "c3357aca"}
# layout: ("L", text width, title px EN, title px BN, chip px) = left column on a cream veil; ("B",) = bottom band
LAY = {"cover": ("L", 510, 68, 63, 0), "what": ("B",), "same": ("L", 430, 58, 54, 27), "pathways": ("L", 520, 62, 58, 28),
       "types": ("L", 470, 62, 58, 27), "prodrug": ("L", 420, 54, 50, 25), "test": ("B",), "care": ("L", 490, 58, 54, 27),
       "bangladesh": ("B",), "key": ("B",)}
# key: (kicker EN, BN), (title EN, BN) with <i>keyword</i>, chips (EN list, BN list)
T = {
 "cover": (("PHARMACOGENETICS", "ফার্মাকোজেনেটিক্স"),
           ("Can your <i>genes</i> change how medicines work?", "আপনার <i>জিন</i> কি ওষুধের প্রতিক্রিয়া বদলে দিতে পারে?"),
           (["Gene–drug links, clinical examples and the limits of testing"], ["জিন–ওষুধের সম্পর্ক, ক্লিনিক্যাল উদাহরণ ও পরীক্ষার সীমা"])),
 "what": (("WHAT IS IT", "এটি কী"), ("Where <i>genetics</i> meets medicine", "যেখানে <i>জেনেটিক্স</i> ও ওষুধ মেলে"),
          (["Inherited DNA differences", "A medicine-specific response", "One part of precision medicine"],
           ["উত্তরাধিকারসূত্রে পাওয়া DNA-র পার্থক্য", "নির্দিষ্ট ওষুধের প্রতিক্রিয়া", "precision medicine-এর একটি অংশ"])),
 "same": (("SAME DOSE", "একই ডোজ"), ("Same dose, <i>different response</i>", "একই ডোজ, <i>ভিন্ন প্রতিক্রিয়া</i>"),
          (["Genes are one possible reason", "Age, organs, diet and other medicines matter too"],
           ["জিন একটি সম্ভাব্য কারণ", "বয়স, অঙ্গের কার্যকারিতা, খাদ্য ও অন্য ওষুধও গুরুত্বপূর্ণ"])),
 "pathways": (("FOUR PATHWAYS", "চারটি পথ"), ("How genes <i>shape</i> a medicine's journey", "জিন কীভাবে ওষুধের যাত্রাকে <i>প্রভাবিত</i> করে"),
              (["Enzymes activate or break it down", "Transporters move it in and out", "Targets and immune proteins"],
               ["এনজাইম ওষুধ সক্রিয় করে বা ভাঙে", "ট্রান্সপোর্টার ওষুধকে ভেতরে-বাইরে নেয়", "টার্গেট ও ইমিউন প্রোটিন"])),
 "types": (("METABOLISER TYPES", "মেটাবোলাইজারের ধরন"), ("Fast, normal or <i>slow</i>?", "দ্রুত, স্বাভাবিক নাকি <i>ধীর</i>?"),
           (["Predicted function, gene by gene", "Poor to ultrarapid, depending on the gene"],
            ["জিন অনুযায়ী predicted কার্যকারিতা", "জিনভেদে poor থেকে ultrarapid"])),
 "prodrug": (("PRODRUG EXAMPLE", "প্রোড্রাগের উদাহরণ"), ("Some medicines <i>must be activated</i>", "কিছু ওষুধকে আগে <i>সক্রিয় হতে হয়</i>"),
             (["Clopidogrel involves CYP2C19", "Less enzyme activity can mean less active drug"],
              ["Clopidogrel-এ CYP2C19 ভূমিকা রাখে", "এনজাইমের কার্যকারিতা কম হলে সক্রিয় ওষুধ কম তৈরি হতে পারে"])),
 "test": (("THE TEST", "পরীক্ষা"), ("A small sample, <i>a careful reading</i>", "ছোট নমুনা, <i>সতর্ক ব্যাখ্যা</i>"),
          (["Blood, saliva or a cheek swab", "Only tested variants are reported", "Needs expert interpretation"],
           ["রক্ত, লালা বা গালের swab", "শুধু পরীক্ষিত variant-এর ফল আসে", "বিশেষজ্ঞের ব্যাখ্যা দরকার"])),
 "care": (("IN CARE", "চিকিৎসায়"), ("A result <i>informs</i>, it doesn't decide", "ফল <i>দিকনির্দেশ</i> দেয়, সিদ্ধান্ত নেয় না"),
          (["May support a different medicine, dose or monitoring", "Read with the whole patient picture"],
           ["ভিন্ন ওষুধ, ডোজ বা পর্যবেক্ষণে সহায়ক হতে পারে", "রোগীর সামগ্রিক অবস্থার সঙ্গে মিলিয়ে দেখতে হয়"])),
 "bangladesh": (("BANGLADESH", "বাংলাদেশ"), ("Ask <i>before</i> you test", "পরীক্ষার <i>আগে</i> প্রশ্ন করুন"),
                (["Which gene–drug question?", "Which variants are covered?", "Who explains the result?"],
                 ["কোন জিন–ওষুধ প্রশ্নের জন্য?", "কোন variant পরীক্ষা হচ্ছে?", "ফল কে ব্যাখ্যা করবেন?"])),
 "key": (("KEY TAKEAWAYS", "মূল কথা"), ("Genes are <i>one part</i> of care", "জিন চিকিৎসার <i>একটি অংশ</i> মাত্র"),
         (["Meaning depends on the gene and the medicine", "Testing isn't needed for every medicine", "Clinical advice still comes first"],
          ["অর্থ নির্ভর করে জিন ও ওষুধের ওপর", "প্রতিটি ওষুধের জন্য পরীক্ষা লাগে না", "চিকিৎসকের পরামর্শই আগে"])),
}
CSS = f"""<meta charset="utf-8"><style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;overflow:hidden;background:#F7F1E6}}
.s img{{position:absolute}}
</style>"""

def main_html(key, lang, bgpath):
    b = 0 if lang == "en" else 1
    fam = "Sora" if lang == "en" else "NSB"
    kick, title, chips = T[key][0][b], T[key][1][b], T[key][2][b]
    lay = LAY[key]; lh = 1.14 if lang == "en" else 1.34; ls = ".12em" if lang == "en" else "0"
    base = f"""<style>.s{{width:1600px;height:900px;font-family:{fam},sans-serif}}.s img{{left:0;top:0;width:1600px;height:900px}}</style>"""
    if lay[0] == "L":
        _, tw, fe, fb, cp = lay; fs = fe if lang == "en" else fb
        if key == "cover":
            ch = f'<div class="sub">{chips[0]}</div><div class="by">{"By Sayedul Abrar · Pharmacist" if lang=="en" else "ফার্মাসিস্ট সাইয়্যেদুল আবরার"}</div>'
        else:
            ch = '<div class="ch">' + "".join(f'<div class="c">{c}</div>' for c in chips) + "</div>"
        veil = tw + 64
        return CSS + base + f"""<style>.v{{position:absolute;left:0;top:0;width:{veil+160}px;height:900px;background:linear-gradient(90deg,#F7F1E6 0,rgba(247,241,230,.97) {veil}px,rgba(247,241,230,0) 100%)}}
.t{{position:absolute;left:64px;top:0;width:{tw}px;height:900px;display:flex;flex-direction:column;justify-content:center}}
.k{{font:700 25px/1 {fam};letter-spacing:{ls};color:#17646a}}.bar{{width:96px;height:7px;border-radius:4px;background:#e0583a;margin:18px 0 26px}}
.h{{font:800 {fs}px/{lh} {fam};color:#253238}}.h i{{font-style:normal;color:#e0583a}}
.ch{{margin-top:32px;display:flex;flex-direction:column;gap:14px}}.c{{background:#fff;border-left:7px solid #17646a;border-radius:10px;padding:14px 20px;font:700 {cp}px/1.38 {fam};color:#253238;box-shadow:0 4px 14px rgba(23,100,106,.12)}}
.sub{{margin-top:26px;font:700 28px/1.45 {fam};color:#345}}.by{{margin-top:30px;align-self:flex-start;font:700 24px/1 {fam};color:#fff;background:#17646a;padding:16px 30px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="v"></div><div class="t"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div>{ch}</div></div>"""
    fs = 62 if lang == "en" else 57
    cp = 27 if lang == "en" else 26
    return CSS + base + f"""<style>.bd{{position:absolute;left:0;bottom:0;width:1600px;height:330px;background:linear-gradient(180deg,rgba(18,62,66,0) 0,rgba(18,62,66,.93) 40px,rgba(18,62,66,.96) 100%)}}
.l{{position:absolute;left:64px;bottom:44px;width:780px}}.k{{font:700 24px/1 {fam};letter-spacing:{ls};color:#ffcf8a}}.bar{{width:84px;height:6px;border-radius:3px;background:#ff8a63;margin:14px 0 18px}}
.h{{font:800 {fs}px/{lh} {fam};color:#fff}}.h i{{font-style:normal;color:#ffb48f}}
.r{{position:absolute;right:64px;bottom:44px;width:640px;display:flex;flex-direction:column;gap:12px}}.c{{background:rgba(255,255,255,.95);border-left:7px solid #e0583a;border-radius:10px;padding:12px 18px;font:700 {cp}px/1.35 {fam};color:#253238}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="bd"></div><div class="l"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div></div>
<div class="r">{"".join(f'<div class="c">{c}</div>' for c in chips)}</div></div>"""

def social_html(lang, bgpath):
    fam = "Sora" if lang == "en" else "NSB"
    kick = "PHARMA BLOG · PHARMACOLOGY & GENETICS" if lang == "en" else "PHARMA BLOG · ফার্মাকোলজি ও জেনেটিক্স"
    if lang == "en":
        h = "Pharmacogenetics:<br>Can Your <i>Genes</i> Change<br>How Medicines Work?"; sub = "Gene–drug links and the limits of testing"; by = "By Sayedul Abrar · Pharmacist"; fs = 40; lh = 1.16
    else:
        h = "ফার্মাকোজেনেটিক্স:<br>আপনার <i>জিন</i> কি ওষুধের<br>প্রতিক্রিয়া বদলে দিতে পারে?"; sub = "জিন–ওষুধের সম্পর্ক ও পরীক্ষার সীমা"; by = "ফার্মাসিস্ট সাইয়্যেদুল আবরার"; fs = 37; lh = 1.32
    return CSS + f"""<style>.s{{width:1200px;height:630px;font-family:{fam},sans-serif}}.s img{{left:60px;top:0;width:1120px;height:630px}}
.fade{{position:absolute;left:0;top:0;width:640px;height:630px;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 66%,rgba(247,241,230,0) 100%)}}
.k{{position:absolute;left:52px;top:46px;font:700 17px/1 {fam};letter-spacing:{'.09em' if lang=='en' else '0'};color:#17646a}}.bar{{position:absolute;left:52px;top:74px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
.h{{position:absolute;left:52px;top:98px;width:560px;font:800 {fs}px/{lh} {fam};color:#253238}}.h i{{font-style:normal;color:#e0583a}}
.sub{{position:absolute;left:52px;top:{300 if lang=='en' else 318}px;width:480px;font:700 20px/1.45 {fam};color:#345}}
.by{{position:absolute;left:52px;top:{372 if lang=='en' else 392}px;font:700 18px/1 {fam};color:#fff;background:#17646a;padding:12px 22px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="fade"></div><div class="k">{kick}</div><div class="bar"></div><div class="h">{h}</div><div class="sub">{sub}</div><div class="by">{by}</div></div>"""

if __name__ == "__main__":
    for k, p in M.items():
        f = BG / f"px-{k}.webp"
        Image.open(SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(f, "WEBP", quality=92, method=6)
    tmp = BG / "_t.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(500)
            pg.screenshot(path=str(out)); pg.close()
        for k in M:
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(main_html(k, lang, BG / f"px-{k}.webp"), 1600, 900, png)
                dst = OUT / (f"px-{k}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); print(dst.name, dst.stat().st_size // 1024, "KB")
        for lang in ("en", "bn"):
            png = BG / "_o.png"; shot(social_html(lang, BG / "px-cover.webp"), 1200, 630, png)
            im = Image.open(png).convert("RGB")
            im.save(OUT / f"px-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            if lang == "en":
                im.save(OUT / "px-card.webp", "WEBP", quality=84, method=6)
                im.resize((750, 394), Image.LANCZOS).save(OUT / "px-card-w750.webp", "WEBP", quality=82, method=6)
        b.close()
    for x in (tmp, BG / "_o.png"):
        x.unlink(missing_ok=True)
