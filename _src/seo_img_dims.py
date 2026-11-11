#!/usr/bin/env python3
"""Adds width/height attributes (intrinsic size) to local raster <img> tags missing them, to reduce layout shift."""
import re, sys, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
pages = sys.argv[1:]
tot = 0
for rel in pages:
    p = R/rel; s = p.read_text(encoding="utf-8"); n = 0
    def fix(m):
        global tot
        tag = m.group(0)
        if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag): return tag
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if not src or not src.group(1).startswith(("/assets/", "/img/", "assets/")): return tag
        f = R/src.group(1).lstrip("/")
        if not f.exists() or f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"): return tag
        w, h = Image.open(f).size
        tag = re.sub(r'\s*(width|height)="[^"]*"', "", tag)
        tot += 1
        return tag.replace("<img", f'<img width="{w}" height="{h}"', 1)
    s2 = re.sub(r"<img\b[^>]*>", fix, s)
    if s2 != s: p.write_text(s2, encoding="utf-8")
print("dims added", tot)
