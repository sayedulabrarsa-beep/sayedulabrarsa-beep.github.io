#!/usr/bin/env python3
"""Prepare the 8 pharma-industry images (fix two typos in artwork) -> assets/img/blog/pharma-industry/*.webp"""
import json, math, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
A = "/mnt/user-data/attachments/52ad2d6e-6d6a-5c6f-8d36-51ace81f756a"; ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/blog/pharma-industry"; OUT.mkdir(parents=True, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def op(i): return Image.open(f"{A}/{i}-image.png").convert("RGB")
def fix_mfg(m):
    px = m.load(); cx, cy, R = 1257, 546, 21
    def row(y):
        yy = min(max(y, cy-13), cy+13)
        return (np.mean([px[x, yy] for x in (1238, 1239, 1240)], axis=0), np.mean([px[x, yy] for x in (1274, 1275, 1276)], axis=0))
    rows = {y: row(y) for y in range(cy-R, cy+R+1)}
    for y in range(cy-R, cy+R+1):
        hw = math.sqrt(max(R*R-(y-cy)**2, 0)); l, r = rows[y]
        for x in range(int(cx-hw), int(cx+hw)+1):
            t = (x-(cx-R))/(2*R); px[x, y] = tuple(int(l[i]*(1-t)+r[i]*t) for i in range(3))
    d = ImageDraw.Draw(m); f = ImageFont.truetype(FD+"Inter-ExtraBold.otf", 38)
    d.text((cx+1.5, cy+2.5), "6", font=f, fill=(205, 105, 12), anchor="mm"); d.text((cx, cy-0.5), "6", font=f, fill=(255, 255, 255), anchor="mm")
    return m
def fix_gmp(g):
    gp = g.load()
    for y in range(636, 670):
        l = np.mean([gp[x, y] for x in range(1291, 1296)], axis=0); r = np.mean([gp[x, y] for x in range(1329, 1333)], axis=0)
        for x in range(1298, 1327):
            t = (x-1298)/29; gp[x, y] = tuple(int(l[i]*(1-t)+r[i]*t) for i in range(3))
    ImageDraw.Draw(g).text((1300, 662), "in", font=ImageFont.truetype(FD+"Inter-SemiBold.otf", 31), fill=(14, 26, 30), anchor="ls")
    return g
SRC = {"hero": ("5eaa3b19", "pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9", None),
 "api": ("94ad4329", "api-vs-finished-pharmaceutical-product-fpp", None),
 "supply": ("ceefc4a4", "pharmaceutical-supply-chain-in-bangladesh-from-manufacturing-to-patient", None),
 "gmp": ("62fd8c8a", "gmp-quality-assurance-and-quality-control-qa-qc-explained", fix_gmp),
 "mfg": ("3b0d4174", "tablet-and-capsule-manufacturing-process-seven-steps", fix_mfg),
 "journey": ("eb00b33f", "complete-journey-of-a-medicine-research-to-post-market-monitoring", None),
 "types": ("bbe333eb", "types-of-pharmaceutical-companies-innovator-generic-api-cdmo-cro", None),
 "key": ("ea4969de", "pharmaceutical-industry-in-bangladesh-key-takeaways", None)}
meta = {}
for k, (i, name, fx) in SRC.items():
    im = op(i)
    if fx: im = fx(im)
    w = 1600; im2 = im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
    im2.save(OUT/f"{name}.webp", quality=88, method=6); meta[k] = [name+".webp", *im2.size]
    if k == "hero":
        h = round(im.width/1.905); y = (im.height-h)//2
        im.crop((0, y, im.width, y+h)).resize((1200, 630), Image.LANCZOS).save(ROOT/"assets/img/blog/pharma-industry-in-bangladesh-social.jpg", quality=90, optimize=True)
json.dump(meta, open(ROOT/"_src/pharma_images.json", "w"), indent=1); print(meta)
