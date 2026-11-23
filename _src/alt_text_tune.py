#!/usr/bin/env python3
"""Alt-text clean-up (re-runnable), following Google's image guidance: describe what the picture shows, no keyword lists.
- Author portrait (/assets/img/sayedul-abrar.jpg): one accurate description with his name, nickname and role (EN / BN).
- Bangla alt text: the name spelling used in images, "সাইয়্যেদুল আবরার", replaces older variants.
- Short related-product thumbnails get the generic name and maker.
Skips Learning and Portfolio pages (content off-limits)."""
import re, pathlib, html
R = pathlib.Path(__file__).resolve().parent.parent
EN = "Sayedul Abrar (Abrar), pharmacist and Product Executive at Opsonin Pharma Ltd., Dhaka, Bangladesh"
BN = "সাইয়্যেদুল আবরার (Sayedul Abrar), ফার্মাসিস্ট ও Opsonin Pharma Ltd.-এর প্রোডাক্ট এক্সিকিউটিভ"
PRODUCT = {
    "/assets/img/products/finix-20-capsule-box.webp": "Finix 20 (rabeprazole sodium) pack by Opsonin Pharma",
    "/assets/img/products/finix-mups-20-tablet-box.webp": "Finix MUPS 20 (rabeprazole sodium MUPS tablet) pack by Opsonin Pharma",
    "/assets/img/products/finix-hp-pack-box.webp": "Finix HP (rabeprazole, amoxicillin, clarithromycin) combination pack by Opsonin Pharma",
}
changed = 0
for p in sorted(R.glob("**/index.html")):
    rel = p.relative_to(R).as_posix()
    if rel.startswith(("_src/", "learning/", "portfolio/", "node_modules/")):
        continue
    s = p.read_text(encoding="utf-8")
    bn = re.search(r'<html[^>]*lang="bn', s) is not None
    def fix(m):
        tag = m.group(0)
        src = re.search(r'\ssrc="([^"]+)"', tag)
        alt = re.search(r'\salt="([^"]*)"', tag)
        if not src or not alt:
            return tag
        u = src.group(1).split("?")[0]
        a = alt.group(1)
        new = a
        if u == "/assets/img/sayedul-abrar.jpg":
            new = html.escape(BN if bn else EN, quote=True)
        elif u in PRODUCT and len(html.unescape(a)) < 30:
            new = html.escape(PRODUCT[u], quote=True)
        new = new.replace("সাইদুল আব্রারের", "সাইয়্যেদুল আবরারের").replace("সাইদুল আব্রার", "সাইয়্যেদুল আবরার")
        return tag if new == a else tag.replace(f'alt="{a}"', f'alt="{new}"', 1)
    out = re.sub(r"<img\b[^>]*>", fix, s)
    if out != s:
        p.write_text(out, encoding="utf-8"); changed += 1
print("alt text: pages changed", changed)
