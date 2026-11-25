#!/usr/bin/env python3
"""Clinical Trial Phases article: 10 user-supplied text-free pictures -> 1600x900 WebP with a title written in code (EN + BN), plus share/card images."""
import pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/ct_images/bg"; OUT = R / "assets/img/blog/clinical-trial-phases"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"cover": "f22a2d16", "questions": "54c30558", "preclinical": "846232a6", "phase1": "b7f051c2", "phase2": "fe904dcb",
     "phase3": "97503d4c", "regulatory": "dd9312b5", "phase4": "6937c802", "safeguards": "794852e6", "key": "3f9d184a"}
# (kicker, title with <i>keyword</i>) per language
T = {
 "cover": (("CLINICAL RESEARCH", "ক্লিনিক্যাল গবেষণা"), ("Clinical trial phases, <i>step by step</i>", "ক্লিনিক্যাল ট্রায়ালের <i>ধাপগুলো</i> এক নজরে"),
           ("From first-in-human to post-marketing", "মানুষের ওপর প্রথম পরীক্ষা থেকে বাজার-পরবর্তী পর্যবেক্ষণ")),
 "questions": (("THE BIG IDEA", "মূল ধারণা"), ("Each phase asks <i>a different question</i>", "প্রতিটি phase <i>আলাদা প্রশ্নের</i> উত্তর খোঁজে"), None),
 "preclinical": (("BEFORE PHASE I", "Phase I-এর আগে"), ("Laboratory evidence <i>comes first</i>", "প্রথমে আসে <i>ল্যাবরেটরির প্রমাণ</i>"), None),
 "phase1": (("PHASE I", "PHASE I"), ("First-in-human: <i>safety and dose</i>", "প্রথমবার মানুষে: <i>নিরাপত্তা ও ডোজ</i>"), None),
 "phase2": (("PHASE II", "PHASE II"), ("Early evidence <i>in patients</i>", "রোগীদের মধ্যে <i>প্রাথমিক প্রমাণ</i>"), None),
 "phase3": (("PHASE III", "PHASE III"), ("Confirmation <i>at larger scale</i>", "বড় পরিসরে <i>নিশ্চিতকরণ</i>"), None),
 "regulatory": (("REGULATORY REVIEW", "REGULATORY REVIEW"), ("A <i>separate decision</i> by the regulator", "নিয়ন্ত্রক সংস্থার <i>আলাদা সিদ্ধান্ত</i>"), None),
 "phase4": (("PHASE IV", "PHASE IV"), ("Learning continues <i>after authorisation</i>", "অনুমোদনের পরও <i>শেখা চলতে থাকে</i>"), None),
 "safeguards": (("PARTICIPANT PROTECTION", "অংশগ্রহণকারীর সুরক্ষা"), ("Protecting <i>the people</i> who take part", "যাঁরা অংশ নেন, তাঁদের <i>সুরক্ষা</i>"), None),
 "key": (("REMEMBER", "মনে রাখুন"), ("Key <i>takeaways</i>", "মূল <i>কথা</i>"), None),
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
i{{font-style:normal;color:#e0583a}}
</style>"""

def main_html(key, lang, bgpath):
    b = 0 if lang == "en" else 1
    fam = "Sora" if lang == "en" else "NSB"
    kick, title, sub = T[key][0][b], T[key][1][b], (T[key][2][b] if T[key][2] else "")
    fs = (58 if key != "cover" else 62) if lang == "en" else (56 if key != "cover" else 58)
    lh = 1.14 if lang == "en" else 1.32
    subh = f'<div class="sub">{sub}</div>' if sub else ""
    by = ""
    if key == "cover":
        by = f'<div class="by">{"By Sayedul Abrar · Pharmacist" if lang=="en" else "ফার্মাসিস্ট সাইয়্যেদুল আবরার"}</div>'
    return CSS + f"""<style>.s{{width:1600px;height:900px;font-family:{fam},sans-serif}}.s img{{left:0;top:0;width:1600px;height:900px}}
.t{{position:absolute;left:72px;top:0;width:470px;height:900px;display:flex;flex-direction:column;justify-content:center}}
.k{{font:700 21px/1 {fam};letter-spacing:{'.12em' if lang=='en' else '0'};color:#17646a}}.bar{{width:84px;height:6px;border-radius:3px;background:#e0583a;margin:16px 0 22px}}
.h{{font:800 {fs}px/{lh} {fam};color:#253238}}.sub{{margin-top:22px;font:700 24px/1.45 {fam};color:#345}}
.by{{margin-top:28px;align-self:flex-start;font:700 21px/1 {fam};color:#fff;background:#17646a;padding:14px 26px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="t"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div>{subh}{by}</div></div>"""

def social_html(lang, bgpath):
    fam = "Sora" if lang == "en" else "NSB"
    kick = "PHARMA BLOG · CLINICAL RESEARCH" if lang == "en" else "PHARMA BLOG · ক্লিনিক্যাল গবেষণা"
    if lang == "en":
        h = "Clinical Trial<br>Phases <i>Explained</i>"; sub = "From first-in-human to post-marketing"; by = "By Sayedul Abrar · Pharmacist"; fs = 44; lh = 1.15
    else:
        h = "ক্লিনিক্যাল ট্রায়ালের<br><i>ধাপগুলো</i> সহজ ভাষায়"; sub = "প্রথম মানব-পরীক্ষা থেকে বাজার-পরবর্তী পর্যবেক্ষণ"; by = "ফার্মাসিস্ট সাইয়্যেদুল আবরার"; fs = 42; lh = 1.3
    return CSS + f"""<style>.s{{width:1200px;height:630px;font-family:{fam},sans-serif}}.s img{{left:80px;top:0;width:1120px;height:630px}}
.fade{{position:absolute;left:0;top:0;width:620px;height:630px;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 62%,rgba(247,241,230,0) 100%)}}
.k{{position:absolute;left:58px;top:56px;font:700 18px/1 {fam};letter-spacing:{'.1em' if lang=='en' else '0'};color:#17646a}}.bar{{position:absolute;left:58px;top:84px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
.h{{position:absolute;left:58px;top:108px;width:520px;font:800 {fs}px/{lh} {fam};color:#253238}}
.sub{{position:absolute;left:58px;top:{256 if lang=='en' else 276}px;width:420px;font:700 20px/1.45 {fam};color:#345}}
.by{{position:absolute;left:58px;top:{340 if lang=='en' else 360}px;font:700 18px/1 {fam};color:#fff;background:#17646a;padding:12px 22px;border-radius:999px}}</style>
<div class="s"><img src="{bgpath.as_uri()}"><div class="fade"></div><div class="k">{kick}</div><div class="bar"></div><div class="h">{h}</div><div class="sub">{sub}</div><div class="by">{by}</div></div>"""

if __name__ == "__main__":
    for k, p in M.items():
        f = BG / f"ct-{k}.webp"
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
                png = BG / "_o.png"; shot(main_html(k, lang, BG / f"ct-{k}.webp"), 1600, 900, png)
                dst = OUT / (f"ct-{k}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); print(dst.name, dst.stat().st_size // 1024, "KB")
        for lang in ("en", "bn"):
            png = BG / "_o.png"; shot(social_html(lang, BG / "ct-cover.webp"), 1200, 630, png)
            im = Image.open(png).convert("RGB")
            im.save(OUT / f"ct-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            if lang == "en":
                im.save(OUT / "ct-card.webp", "WEBP", quality=84, method=6)
                im.resize((750, 394), Image.LANCZOS).save(OUT / "ct-card-w750.webp", "WEBP", quality=82, method=6)
        b.close()
    for x in (tmp, BG / "_o.png"):
        x.unlink(missing_ok=True)
