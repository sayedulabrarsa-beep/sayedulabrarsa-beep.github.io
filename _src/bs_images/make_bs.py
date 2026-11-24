#!/usr/bin/env python3
"""Biosimilars article: convert the 10 user-supplied text-free pictures to WebP and build share/card images."""
import pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
OUT = R / "assets/img/blog/biosimilars"
FONTS = (R / "_src/stability_images/fonts").as_uri()
M = {"bs-cover": "e5df0df3", "bs-production": "c50edfbe", "bs-approval": "87c47d08", "bs-takeaways": "d23e7aa7", "bs-cell": "13b253da",
     "bs-biosimilar": "c03bb451", "bs-bangladesh": "2feeb069", "bs-switching": "721d1584", "bs-generic": "e2dd9313", "bs-clinic": "da27deb8"}
for n, p in M.items():
    im = Image.open(SRC / f"{p}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS)
    f = OUT / f"{n}.webp"; im.save(f, "WEBP", quality=86, method=6); print(n, f.stat().st_size // 1024, "KB")
SOC = {"en": dict(kick="PHARMA BLOG · BIOLOGIC MEDICINES", l1="Biosimilars", l2="Explained: How Similar", l3="to the Original ", key="Biologic?",
                  sub="Not a copy. Highly similar, carefully compared.", by="By Sayedul Abrar · Pharmacist"),
       "bn": dict(kick="PHARMA BLOG · বায়োলজিক ওষুধ", l1="বায়োসিমিলার:", l2="আসল বায়োলজিক ওষুধের", l3="সঙ্গে কতটা ", key="মিল?",
                  sub="হুবহু কপি নয়; অত্যন্ত সদৃশ ও যত্নে তুলনা করা।", by="ফার্মাসিস্ট সাইয়্যেদুল আবরার")}
img = OUT / "bs-takeaways.webp"
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, t in SOC.items():
        fam = "Sora" if lang == "en" else "NSB"; fs = 43 if lang == "en" else 45
        html = f"""<meta charset="utf-8"><style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;width:1200px;height:630px;overflow:hidden;background:#F7F1E6;font-family:{fam},sans-serif}}
img{{position:absolute;left:0;top:-10px;width:1200px;height:675px}}
.k{{position:absolute;left:58px;top:50px;font:700 18px/1 {fam};letter-spacing:.12em;color:#17646a}}
.bar{{position:absolute;left:58px;top:78px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
.h{{position:absolute;left:58px;top:98px;width:640px;font:800 {fs}px/1.15 {fam};color:#253238}}
.h em{{font-style:normal;color:#e0583a}}
.sub{{position:absolute;left:58px;top:276px;width:620px;font:700 20px/1.4 {fam};color:#345}}
.by{{position:absolute;left:58px;top:326px;font:700 18px/1 {fam};color:#fff;background:#17646a;padding:12px 22px;border-radius:999px}}
</style><div class="s"><img src="{img.as_uri()}"><div class="k">{t['kick']}</div><div class="bar"></div>
<div class="h">{t['l1']}<br>{t['l2']}<br>{t['l3']}<em>{t['key']}</em></div><div class="sub">{t['sub']}</div><div class="by">{t['by']}</div></div>"""
        hp = OUT / "_s.html"; hp.write_text(html, encoding="utf-8")
        pg = b.new_page(viewport={"width": 1200, "height": 630}); pg.goto(hp.as_uri()); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / f"_s_{lang}.png")); pg.close()
        im = Image.open(OUT / f"_s_{lang}.png").convert("RGB")
        im.save(OUT / f"bs-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
        if lang == "en":
            im.save(OUT / "bs-card.webp", "WEBP", quality=84, method=6)
            im.resize((750, 394), Image.LANCZOS).save(OUT / "bs-card-w750.webp", "WEBP", quality=82, method=6)
        (OUT / f"_s_{lang}.png").unlink()
    b.close(); (OUT / "_s.html").unlink()
