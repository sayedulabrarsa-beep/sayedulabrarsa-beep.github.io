#!/usr/bin/env python3
"""Drug vs Medicine (dm): 10 user text-free photos -> titled 1600x900 WebP (EN+BN) with the text zone in a different place per picture, share image + card."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make3 as m
from PIL import Image
from playwright.sync_api import sync_playwright
R, BG, FD, LAT, BNG, face = m.R, m.BG, m.FD, m.LAT, m.BNG, m.face
FN = "_src/qa3_images/fonts"
m.ART["dm"] = dict(dir="drug-vs-medicine", pre="dm", fam="'DMF'", ink="#0E3B43", key="#C2185B", acc="#FFB300", hi="rgba(255,179,0,.45)", veil="#FFF6EA", pill="#0E3B43", bandrgb="14,59,67", gold="#FFD66B",
  css="".join([face("DMF", 800, FD(FN, "lexend-latin-800-normal.woff2"), LAT), face("DMF", 600, FD(FN, "lexend-latin-600-normal.woff2"), LAT), face("DMF", 800, FD(FN, "anek-bangla-bengali-800-normal.woff2"), BNG), face("DMF", 600, FD(FN, "anek-bangla-bengali-600-normal.woff2"), BNG)]), lh=(1.14, 1.3), ls=".06em")
IDS = {"328bb7ab": "cover", "1703ea44": "drug", "a638cdcf": "medicine", "1d2efec1": "diff", "02ed8b74": "remember", "76dc77de": "rabe", "b842fa29": "every", "7a913f8f": "pharm", "fa0be925": "why", "3e3548f4": "takeaways"}
# key: (x, y, w, h, dark, horizontal chips)
Z = {"cover": (470, 60, 640, 460, True, False), "drug": (985, 140, 545, 560, True, False), "medicine": (56, 150, 480, 600, False, False), "diff": (64, 36, 1472, 270, False, True),
     "rabe": (64, 640, 1472, 230, True, True), "every": (1010, 120, 520, 640, False, False), "pharm": (56, 130, 480, 640, False, False), "why": (50, 520, 610, 340, False, False), "takeaways": (1010, 110, 530, 680, False, False)}
T = {
 "cover": (("DRUG VS MEDICINE", "DRUG VS MEDICINE"), ("Drug or medicine: <i>what is the difference?</i>", "Drug নাকি Medicine: <i>পার্থক্য কী?</i>"), (["A drug is the active substance; a medicine is the prepared product."], ["Drug হলো সক্রিয় পদার্থ; Medicine হলো প্রস্তুত পণ্য।"])),
 "drug": (("1 · THE DRUG", "১ · DRUG"), ("A <i>drug</i> is the active substance", "<i>Drug</i> হলো সক্রিয় পদার্থ"), (["Often called the API", "Acts on the body"], ["প্রায়ই API নামে পরিচিত", "শরীরে প্রভাব ফেলে"])),
 "medicine": (("2 · THE MEDICINE", "২ · MEDICINE"), ("A <i>medicine</i> is the prepared product", "<i>Medicine</i> হলো প্রস্তুত পণ্য"), (["Drug + dose + form", "Tablet, capsule, syrup, cream"], ["Drug + মাত্রা + ফর্ম", "Tablet, Capsule, Syrup, Cream"])),
 "diff": (("KEY DIFFERENCES", "মূল পার্থক্য"), ("Substance <i>vs</i> product", "পদার্থ <i>বনাম</i> পণ্য"), (["Drug: the active substance", "Medicine: the usable product", "The terms can overlap by context"], ["Drug: সক্রিয় পদার্থ", "Medicine: ব্যবহারযোগ্য পণ্য", "প্রসঙ্গভেদে শব্দ দুটি মিলে যায়"])),
 "rabe": (("A REAL EXAMPLE", "একটি বাস্তব উদাহরণ"), ("One drug, <i>more than one medicine</i>", "একটি Drug, <i>একাধিক Medicine</i>"), (["Rabeprazole: the active ingredient (drug)", "Finix: a brand-name medicine", "Finix MUPS: a brand-name medicine"], ["Rabeprazole: সক্রিয় উপাদান (Drug)", "Finix: ব্র্যান্ড নামের Medicine", "Finix MUPS: ব্র্যান্ড নামের Medicine"])),
 "every": (("IS EVERY DRUG A MEDICINE?", "প্রতিটি DRUG কি MEDICINE?"), ("Not <i>every drug</i> becomes a medicine", "প্রতিটি <i>Drug</i> Medicine হয় না"), (["A drug can stay a raw substance", "It becomes a medicine once prepared and approved for use"], ["Drug কাঁচামাল পদার্থ হিসেবেও থাকতে পারে", "প্রস্তুত ও ব্যবহারের অনুমোদন পেলে Medicine হয়"])),
 "pharm": (("PHARMACOLOGY", "ফার্মাকোলজি"), ("Pharmacology: <i>PK and PD</i>", "Pharmacology: <i>PK এবং PD</i>"), (["PK: what the body does to the drug", "PD: what the drug does to the body"], ["PK: শরীর Drug-এর সঙ্গে কী করে", "PD: Drug শরীরে কী করে"])),
 "why": (("WHY IT MATTERS", "কেন গুরুত্বপূর্ণ"), ("Clear words, <i>safer use</i>", "স্পষ্ট শব্দ, <i>নিরাপদ ব্যবহার</i>"), (["The right medicine at the right dose", "Fewer mix-ups"], ["সঠিক Medicine, সঠিক মাত্রা", "বিভ্রান্তি কম"])),
 "takeaways": (("KEY TAKEAWAYS", "মূল কথা"), ("Related, <i>but not the same</i>", "সম্পর্কিত, <i>তবে এক নয়</i>"), (["Drug: the active substance", "Medicine: the prepared product", "Rabeprazole is the drug; Finix is a medicine"], ["Drug: সক্রিয় পদার্থ", "Medicine: প্রস্তুত পণ্য", "Rabeprazole হলো Drug; Finix হলো Medicine"])),
}
T["remember"] = (("REMEMBER IT IN 10 SECONDS", "১০ সেকেন্ডে মনে রাখুন"), ("", ""), ([], []))
SOC = (("PHARMA BLOG · PHARMACOLOGY BASICS", "PHARMA BLOG · ফার্মাকোলজির মূল কথা"), ("<i>Drug</i> vs Medicine: What Is the Difference?", "<i>Drug</i> বনাম Medicine: পার্থক্য কী?"), ("Meaning, examples and FAQs", "অর্থ, উদাহরণ ও সাধারণ প্রশ্ন"))
def box(lang, kick, title, rows, x, y, w, h, dark=False, horiz=False, sub=None, by=None, tf=56, uid="b", kicker_only=False):
    A = m.ART["dm"]; bn = lang == "bn"; fam = A["fam"]; lh = A["lh"][1 if bn else 0]; ls = "0" if bn else A["ls"]
    ink = "#fff" if dark else A["ink"]; key = A["gold"] if dark else A["key"]; vc = "10,52,62" if dark else "255,246,234"; va = ".74" if dark else ".84"
    kf = 22 if not bn else 27; tf = tf if not bn else tf - 4; cf = 25 if not bn else 24; maxt = 126 if not bn else 112
    ch = "" if not rows or sub else '<div class="ch">' + "".join(f'<div class="c">{c}</div>' for c in rows) + "</div>"
    sb = f'<div class="sub">{sub}</div>' if sub else ""; bb = f'<div class="by">{by}</div>' if by else ""
    ttl = f'<div class="h">{title}</div>' if title else ""
    kk = f'<div class="k">{kick}</div><div class="bar"></div>' if kick else ""
    css = (f"<style>.v{uid}{{position:absolute;left:{x-26}px;top:{y-22}px;width:{w+52}px;height:{h+44}px;border-radius:30px;background:rgba({vc},{va});box-shadow:0 0 46px 30px rgba({vc},{va})}}"
           f".t{uid}{{position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;flex-direction:column;justify-content:center}}.in{uid}{{display:flex;flex-direction:column}}"
           f".t{uid} .k{{font:800 calc(var(--s)*{kf}px)/1.12 {fam};letter-spacing:{ls};color:{key}}}.t{uid} .bar{{width:calc(var(--s)*110px);height:calc(var(--s)*9px);border-radius:5px;background:{A['acc']};margin:calc(var(--s)*14px) 0 calc(var(--s)*18px)}}"
           f".t{uid} .h{{font:800 calc(var(--s)*{tf}px)/{lh} {fam};color:{ink}}}.t{uid} .h i{{font-style:normal;color:{key};box-shadow:inset 0 -.3em 0 {A['hi']}}}"
           f".t{uid} .ch{{margin-top:calc(var(--s)*22px);display:flex;flex-direction:{'row' if horiz else 'column'};flex-wrap:wrap;gap:calc(var(--s)*12px)}}.t{uid} .c{{background:#fff;border-left:calc(var(--s)*9px) solid {A['key']};border-bottom:calc(var(--s)*4px) solid {A['acc']};border-radius:10px;padding:calc(var(--s)*11px) calc(var(--s)*18px);font:700 calc(var(--s)*{cf}px)/1.34 {fam};color:{A['ink']};box-shadow:0 4px 14px rgba(0,0,0,.14)}}"
           f".t{uid} .sub{{margin-top:calc(var(--s)*18px);font:600 calc(var(--s)*{cf+2}px)/1.4 {fam};color:{ink}}}.t{uid} .by{{margin-top:calc(var(--s)*20px);align-self:flex-start;white-space:nowrap;font:700 calc(var(--s)*{cf-1}px)/1 {fam};color:{A['ink']};background:#fff;padding:calc(var(--s)*13px) calc(var(--s)*24px);border-radius:999px}}</style>")
    js = (f"<script>(window.FIT=window.FIT||[]).push(function(){{var e=document.getElementById('in{uid}');var best=1,r=document.documentElement;for(var s=1;s<=3.4;s+=0.02){{r.style.setProperty('--s',s);if(e.getBoundingClientRect().height>{h}||e.scrollWidth>{w}+2||{tf}*s>{maxt}||{cf}*s>46)break;best=s}}return best}});</script>")
    return css + f'<div class="v{uid}"></div><div class="t{uid}"><div class="in{uid}" id="in{uid}">{kk}{ttl}{sb}{ch}{bb}</div></div>' + js
FITJS = "<script>document.fonts.ready.then(function(){var r=document.documentElement,f=window.FIT||[],m=9;f.forEach(function(g){var b=g();m=Math.min(m,b)});r.style.setProperty('--s',m)})</script>"
def body(key, lang, social=False):
    b = 1 if lang == "bn" else 0; kick, title, rows = T[key][0][b], T[key][1][b], T[key][2][b]; BY = m.BY[b]
    if social:
        k, t, s = SOC[0][b], SOC[1][b], SOC[2][b]; return box(lang, k, t, [], 470, 50, 760, 420, True, sub=s, by=BY, uid="a") + FITJS
    x, y, w, h, dark, horiz = Z.get(key, (0,) * 6)
    if key == "cover": return box(lang, kick, title, [], x, y, w, h, True, sub=rows[0], by=BY, uid="a") + FITJS
    if key == "remember":
        return (box(lang, kick, "<i>S</i> and <i>P</i>" if b == 0 else "<i>S</i> এবং <i>P</i>", [], 56, 40, 470, 230, True, uid="a") +
                box(lang, None, None, (["S = Substance: the drug", "P = Prepared Product: the medicine"], ["S = Substance: Drug", "P = Prepared Product: Medicine"])[b], 1000, 700, 540, 170, True, uid="b") + FITJS)
    return box(lang, kick, title, rows, x, y, w, h, dark, horiz, tf=50 if horiz else 56, uid="a") + FITJS
def page(lang, inner, W, H, bgp, shift):
    A = m.ART["dm"]
    return (f"<meta charset='utf-8'><style>{A['css']}html,body{{margin:0}}.s{{position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{A['veil']};font-family:{A['fam']},sans-serif}}.s>img{{position:absolute;left:0;top:{shift}px;width:1600px;height:900px}}:root{{--s:1}}</style><div class='s'><img src='{bgp.as_uri()}'>{inner}</div>")
if __name__ == "__main__":
    stamp = []; tmp = BG / "_t.html"
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1500); pg.screenshot(path=str(out)); pg.close()
        out = R / "assets/img/blog/drug-vs-medicine"
        for iid, key in IDS.items():
            bgp = BG / f"dm-{key}.webp"; Image.open(m.SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(page(lang, body(key, lang), 1600, 900, bgp, 0), 1600, 900, png)
                dst = out / (f"dm-{key}" + ("" if lang == "en" else "-bn") + ".webp"); Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); stamp.append([f"/assets/img/blog/drug-vs-medicine/{dst.name}", "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(page(lang, body(key, lang, True), 1600, 840, bgp, -30), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"dm-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en": sm.save(out / "dm-card.webp", "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / "dm-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open("/tmp/stamp_q7.json", "w")); print(len(stamp), "images")
