#!/usr/bin/env python3
"""Pharmacovigilance article: convert the 12 user-supplied text-free AI pictures to WebP and build share/card images."""
import pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
OUT = R / "assets/img/blog/pharmacovigilance"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"pv-cover": "840e6c42", "pv-why": "8219c572", "pv-report-types": "d449bdb1", "pv-cycle": "cc357406",
     "pv-signal": "a6d8d3eb", "pv-causality": "21891ae4", "pv-benefit-risk": "3b67a0ce", "pv-bangladesh": "3328cc04",
     "pv-report-info": "eb588f1a", "pv-industry": "92d71f94", "pv-people": "970dc3cb", "pv-takeaways": "44e0c554"}
for n, p in M.items():
    im = Image.open(SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS)
    f = OUT / f"{n}.webp"; im.save(f, "WEBP", quality=86, method=6); print(n, f.stat().st_size // 1024, "KB")
SOC = {"en": dict(kick="PHARMA BLOG · MEDICINE SAFETY", l1="Pharmacovigilance:", l2="How Are Medicines", l3="Monitored for ", key="Safety?",
                  sub="Reports, signals and the DGDA system in Bangladesh", by="By Sayedul Abrar · Pharmacist"),
       "bn": dict(kick="PHARMA BLOG · ওষুধের নিরাপত্তা", l1="ফার্মাকোভিজিল্যান্স:", l2="ওষুধের নিরাপত্তা কীভাবে", l3="", key="পর্যবেক্ষণ করা হয়?",
                  sub="রিপোর্ট, সিগন্যাল ও বাংলাদেশের DGDA ব্যবস্থা", by="ফার্মাসিস্ট সাইয়্যেদুল আবরার")}
cover = OUT / "pv-cover.webp"
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, t in SOC.items():
        fam = "Sora" if lang == "en" else "NSB"
        fs = 50 if lang == "en" else 48
        html = f"""<meta charset="utf-8"><style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;width:1200px;height:630px;overflow:hidden;background:#F7F1E6;font-family:{fam},sans-serif}}
img{{position:absolute;left:150px;top:0;width:1120px;height:630px}}
.f{{position:absolute;inset:0;background:linear-gradient(90deg,#F7F1E6 0,#F7F1E6 46%,rgba(247,241,230,0) 64%)}}
.k{{position:absolute;left:58px;top:64px;font:700 19px/1 {fam};letter-spacing:.12em;color:#17646a}}
.bar{{position:absolute;left:58px;top:92px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
.h{{position:absolute;left:58px;top:116px;width:600px;font:800 {fs}px/1.16 {fam};color:#253238}}
.h em{{font-style:normal;color:#e0583a}}
.sub{{position:absolute;left:58px;top:336px;width:440px;font:700 24px/1.4 {fam};color:#345}}
.by{{position:absolute;left:58px;bottom:50px;font:700 19px/1 {fam};color:#fff;background:#17646a;padding:13px 24px;border-radius:999px}}
</style><div class="s"><img src="{cover.as_uri()}"><div class="f"></div><div class="k">{t['kick']}</div><div class="bar"></div>
<div class="h">{t['l1']}<br>{t['l2']}<br>{t['l3']}<em>{t['key']}</em></div><div class="sub">{t['sub']}</div><div class="by">{t['by']}</div></div>"""
        hp = OUT / "_s.html"; hp.write_text(html, encoding="utf-8")
        pg = b.new_page(viewport={"width": 1200, "height": 630}); pg.goto(hp.as_uri()); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / f"_s_{lang}.png")); pg.close()
        im = Image.open(OUT / f"_s_{lang}.png").convert("RGB")
        im.save(OUT / f"pv-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
        if lang == "en":
            im.save(OUT / "pv-card.webp", "WEBP", quality=84, method=6)
            im.resize((750, 394), Image.LANCZOS).save(OUT / "pv-card-w750.webp", "WEBP", quality=82, method=6)
        (OUT / f"_s_{lang}.png").unlink()
    b.close(); (OUT / "_s.html").unlink()
