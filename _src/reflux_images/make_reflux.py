#!/usr/bin/env python3
"""Heartburn/GERD article: convert the 25 user-supplied AI pictures to web sizes, patch the
English-only '3 hours' text on the clock picture for Bangla, and build 1200x630 share images."""
import pathlib, cv2, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
OUT = R / "assets/img/blog/reflux"
FONTS = (R / "_src/stability_images/fonts").as_uri()
OUT.mkdir(parents=True, exist_ok=True)

# name -> (attachment prefix, size)   W = 1600x900, S = 1200x1200, T = 1200x800
M = {
 "hero": ("e3025880", "W"), "valve": ("4d85f8b3", "W"),
 "story-1-late-dinner": ("d0489f25", "S"), "story-2-lighter-routine": ("8cb36598", "S"),
 "story-3-warning-signs": ("9ea7dbeb", "S"), "story-4-doctor-visit": ("91e4add6", "S"),
 "trigger-spicy": ("1de98adc", "T"), "trigger-late-dinner": ("d157b4a3", "T"),
 "trigger-fried": ("c5aa29a5", "T"), "trigger-fizzy": ("ae6649a3", "S"),
 "trigger-tea-coffee": ("035b1883", "T"), "trigger-chocolate": ("6195c2dd", "T"),
 "habit-smaller-meal": ("b183fa99", "W"), "habit-upright": ("85fd2508", "W"),
 "habit-raised-bed": ("94676ec6", "W"), "habit-activity": ("ec34dfd7", "W"),
 "habit-loose-clothing": ("2734963d", "W"), "habit-three-hours": ("32dd3398", "W"),
 "warning-green": ("a6ca223c", "W"), "warning-amber": ("b0d2ab96", "W"), "warning-red": ("d6f34777", "W"),
 "doctor": ("d54a1fb0", "W"), "myth-vs-fact": ("f0a2f97e", "W"), "quiz-check": ("1b859699", "W"),
 "key-takeaways": ("9ce2525a", "W"),
}
SZ = {"W": (1600, 900), "S": (1200, 1200), "T": (1200, 800)}

def load(prefix):
    return Image.open(SRC / f"{prefix}-image.png").convert("RGB")

def save(im, name, size):
    im = im.resize(size, Image.LANCZOS)
    p = OUT / f"{name}.webp"
    im.save(p, "WEBP", quality=86, method=6)
    return p.stat().st_size // 1024

def clock_bn():
    """Remove '3 hours' from the clock picture and write the Bangla words in code."""
    im = cv2.imread(str(SRC / "32dd3398-image.png"))
    h, w = im.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    mask[272:428, 585:810] = 255
    clean = cv2.inpaint(im, mask, 12, cv2.INPAINT_NS)
    clean = cv2.GaussianBlur(clean, (0, 0), 0.6)
    keep = cv2.inpaint(im, mask, 12, cv2.INPAINT_NS)
    soft = cv2.GaussianBlur(mask, (0, 0), 3)[..., None] / 255.0
    clean = (im * (1 - soft) + clean * soft).astype(np.uint8)
    tmp = OUT / "_clock_clean.png"
    cv2.imwrite(str(tmp), clean)
    html = f"""<style>
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF}}
html,body{{margin:0}}.s{{position:relative;width:{w}px;height:{h}px;overflow:hidden}}
img{{position:absolute;inset:0;width:100%;height:100%}}
.t{{position:absolute;left:590px;width:212px;top:278px;text-align:center;color:#17646a;font:800 108px/1 NSB;}}
.u{{position:absolute;left:590px;width:212px;top:372px;text-align:center;color:#17646a;font:800 50px/1 NSB;}}
</style><div class="s"><img src="{tmp.as_uri()}"><div class="t">৩</div><div class="u">ঘণ্টা</div></div>"""
    hp = OUT / "_clock.html"; hp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(hp.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(OUT / "_clock_bn.png")); b.close()
    im2 = Image.open(OUT / "_clock_bn.png").convert("RGB")
    print("habit-three-hours-bn", save(im2, "habit-three-hours-bn", (1600, 900)), "KB")
    for f in ("_clock_clean.png", "_clock.html", "_clock_bn.png"):
        (OUT / f).unlink()

SOC = {
 "en": dict(kick="PHARMA BLOG · DIGESTIVE HEALTH", l1="Heartburn vs", l2="Acid Reflux", l3="vs ", key="GERD",
            sub="Symptoms, triggers and when to see a doctor", by="By Sayedul Abrar · Pharmacist"),
 "bn": dict(kick="PHARMA BLOG · হজম স্বাস্থ্য", l1="বুক জ্বালাপোড়া,", l2="অ্যাসিড রিফ্লাক্স", l3="ও ", key="GERD",
            sub="লক্ষণ, কারণ ও কখন ডাক্তার দেখাবেন", by="ফার্মাসিস্ট সাইয়্যেদুল আবরার"),
}

def social():
    hero = OUT / "hero.webp"
    with sync_playwright() as p:
        b = p.chromium.launch()
        for lang, t in SOC.items():
            fam = "Sora" if lang == "en" else "NSB"
            html = f"""<style>
@font-face{{font-family:Sora;font-weight:700;src:url({FONTS}/sora-latin-700-normal.woff2)}}
@font-face{{font-family:Sora;font-weight:800;src:url({FONTS}/sora-latin-800-normal.woff2)}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:700;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}}
@font-face{{font-family:NSB;font-weight:800;src:url({FONTS}/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
html,body{{margin:0}}.s{{position:relative;width:1200px;height:630px;overflow:hidden;font-family:{fam},sans-serif}}
img{{position:absolute;left:0;top:-22px;width:1200px;height:675px}}
.k{{position:absolute;left:58px;top:64px;font:700 19px/1 {fam};letter-spacing:.14em;color:#17646a}}
.h{{position:absolute;left:58px;top:112px;width:560px;font:800 {54 if lang=='en' else 50}px/1.12 {fam};color:#253238}}
.h em{{font-style:normal;color:#e0583a}}
.sub{{position:absolute;left:58px;top:340px;width:430px;font:700 {24 if lang=='en' else 25}px/1.4 {fam};color:#345;}}
.by{{position:absolute;left:58px;bottom:50px;font:700 19px/1 {fam};color:#fff;background:#17646a;padding:13px 24px;border-radius:999px}}
.bar{{position:absolute;left:58px;top:92px;width:74px;height:5px;border-radius:3px;background:#e0583a}}
</style><div class="s"><img src="{hero.as_uri()}"><div class="k">{t['kick']}</div><div class="bar"></div>
<div class="h">{t['l1']}<br>{t['l2']}<br>{t['l3']}<em>{t['key']}</em></div><div class="sub">{t['sub']}</div><div class="by">{t['by']}</div></div>"""
            hp = OUT / "_s.html"; hp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": 1200, "height": 630}); pg.goto(hp.as_uri()); pg.wait_for_timeout(600)
            pg.screenshot(path=str(OUT / f"_s_{lang}.png")); pg.close()
            im = Image.open(OUT / f"_s_{lang}.png").convert("RGB")
            im.save(OUT / f"reflux-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
            print("social", lang, (OUT / f"reflux-social-{lang}.jpg").stat().st_size // 1024, "KB")
            (OUT / f"_s_{lang}.png").unlink()
        b.close(); (OUT / "_s.html").unlink()

if __name__ == "__main__":
    for name, (pre, k) in M.items():
        print(name, save(load(pre), name, SZ[k]), "KB")
    clock_bn()
    social()
