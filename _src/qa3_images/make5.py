#!/usr/bin/env python3
"""Drug Interactions (di) and Side Effects vs ADRs (se): 12 user-supplied text-free photos -> titled 1600x900 WebP (EN+BN), share images and cards. Reuses make3's engine."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make3 as m
from PIL import Image
from playwright.sync_api import sync_playwright
R, BG, FD = m.R, m.BG, m.FD
FN = "_src/qa3_images/fonts"; ST = "_src/stability_images/fonts"; EX = "_src/excretion_images/fonts"; QQ = "_src/qaqc_images/cinematic"
LAT, BNG, face = m.LAT, m.BNG, m.face
m.ART.update({
 "di": dict(dir="drug-interactions", pre="di", fam="'DIF'", ink="#3D1450", key="#8E24AA", acc="#FFB300", hi="rgba(255,179,0,.5)", veil="#F8EEFA", pill="#3D1450", bandrgb="61,20,80", gold="#FFD66B",
   css="".join([face("DIF", 800, FD(FN, "oswald-latin-700-normal.woff2"), LAT), face("DIF", 600, FD(FN, "oswald-latin-500-normal.woff2"), LAT), face("DIF", 800, FD(ST, "noto-serif-bengali-bengali-800-normal.woff2"), BNG), face("DIF", 600, FD(ST, "noto-serif-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.1, 1.36), ls=".1em"),
 "se": dict(dir="side-effects-adr", pre="se", fam="'SEF'", ink="#1F2A37", key="#C62828", acc="#00ACC1", hi="rgba(0,172,193,.38)", veil="#F6F1EF", pill="#1F2A37", bandrgb="31,42,55", gold="#7FE3F0",
   css="".join([face("SEF", 800, FD(FN, "montserrat-latin-800-normal.woff2"), LAT), face("SEF", 600, FD(FN, "montserrat-latin-600-normal.woff2"), LAT), face("SEF", 800, FD(QQ, "hind-siliguri-bengali-700-normal.woff2"), BNG), face("SEF", 600, FD(QQ, "hind-siliguri-bengali-500-normal.woff2"), BNG)]), lh=(1.16, 1.32), ls=".06em"),
})
IDS = ["05be4e58", "393d658c", "a5a2f003", "24bf64ac", "657b4874", "2fa2b912", "869ecd3b", "89dae893", "a809fe1a", "9c7718c3", "fbf7f6c3", "aae7b816"]
KEYS = [("di", "cover"), ("di", "outcome"), ("di", "mech"), ("di", "types"), ("di", "checklist"), ("di", "list"),
        ("se", "cover"), ("se", "se"), ("se", "adr"), ("se", "vs"), ("se", "warn"), ("se", "report")]
M5 = dict(zip(IDS, KEYS)); L = lambda tw, y0, y1: ("L", tw, y0, y1)
m.LAY.update({("di", "cover"): L(500, 60, 840), ("di", "outcome"): L(380, 50, 840), ("di", "mech"): L(150, 40, 860), ("di", "types"): L(360, 50, 840), ("di", "checklist"): L(340, 60, 840), ("di", "list"): L(400, 50, 640),
  ("se", "cover"): L(330, 40, 470), ("se", "se"): L(270, 40, 860), ("se", "adr"): L(250, 40, 860), ("se", "vs"): ("N",), ("se", "warn"): L(380, 30, 350), ("se", "report"): L(250, 40, 660)})
m.T.update({
 ("di", "cover"): (("DRUG INTERACTIONS", "ওষুধের ইন্টারঅ্যাকশন"), ("One medicine can <i>affect another</i>", "এক ওষুধ আরেক ওষুধকে <i>প্রভাবিত করতে পারে</i>"), (["Medicines, food, herbs and health conditions, and how to lower the risk"], ["ওষুধ, খাবার, ভেষজ ও স্বাস্থ্য-অবস্থা, আর ঝুঁকি কমানোর উপায়"])),
 ("di", "mech"): (("TWO MECHANISMS", "দুটি প্রক্রিয়া"), ("Two ways <i>to interact</i>", "মিথস্ক্রিয়ার <i>দুই পথ</i>"), ([], [])),
 ("di", "types"): (("COMMON TYPES", "সাধারণ ধরন"), ("Medicines, food, herbs <i>and conditions</i>", "ওষুধ, খাবার, ভেষজ <i>ও স্বাস্থ্য-অবস্থা</i>"), (["Drug with drug", "Drug with food or drink"], ["ওষুধের সঙ্গে ওষুধ", "ওষুধের সঙ্গে খাবার বা পানীয়"])),
 ("di", "outcome"): (("NOT ALWAYS HARMFUL", "সবসময় ক্ষতিকর নয়"), ("Some are <i>minor</i>, some need care", "কিছু <i>সামান্য</i>, কিছুতে সতর্কতা দরকার"), (["The result depends on the medicines", "Ask before combining"], ["ফল নির্ভর করে কোন ওষুধ মিলছে তার ওপর", "মেশানোর আগে জিজ্ঞাসা করুন"])),
 ("di", "checklist"): (("LOWER THE RISK", "ঝুঁকি কমান"), ("Tell your <i>doctor and pharmacist</i> everything", "চিকিৎসক ও ফার্মাসিস্টকে <i>সব জানান</i>"), (["Share every medicine you take", "Read the label and leaflet"], ["যা যা ওষুধ খান সব জানান", "লেবেল ও লিফলেট পড়ুন"])),
 ("di", "list"): (("KEEP A LIST", "তালিকা রাখুন"), ("My <i>medicine list</i>", "আমার <i>ওষুধের তালিকা</i>"), (["Prescription and OTC medicines", "Herbal products and supplements", "Drug allergies, if any"], ["প্রেসক্রিপশন ও OTC ওষুধ", "ভেষজ পণ্য ও সাপ্লিমেন্ট", "ওষুধে অ্যালার্জি থাকলে তা"])),
 ("se", "cover"): (("SIDE EFFECTS VS ADRs", "সাইড ইফেক্ট ও ADR"), ("Weigh <i>benefit and risk</i>", "উপকার ও ঝুঁকি <i>মিলিয়ে দেখুন</i>"), (["Side effects and adverse drug reactions: what differs"], ["সাইড ইফেক্ট ও অ্যাডভার্স ড্রাগ রিঅ্যাকশনের পার্থক্য"])),
 ("se", "se"): (("SIDE EFFECTS", "সাইড ইফেক্ট"), ("Often <i>mild</i> and predictable", "প্রায়ই <i>সামান্য</i> ও প্রত্যাশিত"), ([], [])),
 ("se", "adr"): (("ADVERSE REACTION", "অ্যাডভার্স রিঅ্যাকশন"), ("Some reactions <i>need prompt care</i>", "কিছু প্রতিক্রিয়ায় <i>দ্রুত সেবা দরকার</i>"), ([], [])),
 ("se", "vs"): (("SIDE EFFECT OR ALLERGY?", "সাইড ইফেক্ট নাকি অ্যালার্জি?"), ("Not every reaction is <i>an allergy</i>", "সব প্রতিক্রিয়াই <i>অ্যালার্জি নয়</i>"), ([], [])),
 ("se", "warn"): (("WARNING SIGNS", "সতর্ক লক্ষণ"), ("Severe signs need <i>urgent help</i>", "গুরুতর লক্ষণে <i>জরুরি সাহায্য নিন</i>"), ([], [])),
 ("se", "report"): (("REPORTING", "রিপোর্ট করা"), ("Report <i>suspected reactions</i>", "সন্দেহজনক প্রতিক্রিয়া <i>রিপোর্ট করুন</i>"), ([], [])),
})
m.SOC.update({
 "di": (("PHARMA BLOG · MEDICINE SAFETY", "PHARMA BLOG · ওষুধের নিরাপত্তা"), ("Drug <i>Interactions</i>: Why Can One Medicine Affect Another?", "Drug <i>Interaction</i>: একটি ওষুধ অন্য ওষুধকে কীভাবে প্রভাবিত করে?"), ("Types, mechanisms and how to lower the risk", "ধরন, প্রক্রিয়া ও ঝুঁকি কমানোর উপায়")),
 "se": (("PHARMA BLOG · MEDICINE SAFETY", "PHARMA BLOG · ওষুধের নিরাপত্তা"), ("<i>Side Effects</i> vs Adverse Drug Reactions: What Is the Difference?", "<i>Side Effect</i> ও Adverse Drug Reaction: পার্থক্য কী?"), ("Warning signs, when to seek help and how to report", "সতর্ক লক্ষণ, কখন সাহায্য নেবেন ও কীভাবে রিপোর্ট করবেন")),
})
m.SOCIAL_L.update({"di": (500, 60, 780)})
def top_block(a, lang, kick, title):
    A = m.ART[a]; bn = lang == "bn"; fam = A["fam"]; lh = A["lh"][1 if bn else 0]; ls = "0" if bn else A["ls"]; tf = 50 if not bn else 46; kf = 22 if not bn else 25; hmax = 120
    css = (f"<style>.tb{{position:absolute;left:0;top:0;width:1600px;height:{hmax+30}px;background:linear-gradient(180deg,{A['veil']}fa 0,{A['veil']}f0 {hmax-10}px,{A['veil']}00 100%)}}.tt{{position:absolute;left:64px;top:16px;width:1100px}}"
           f".k{{font:800 calc(var(--s)*{kf}px)/1.1 {fam};letter-spacing:{ls};color:{A['key']}}}.h{{margin-top:calc(var(--s)*8px);font:800 calc(var(--s)*{tf}px)/{lh} {fam};color:{A['ink']}}}.h i{{font-style:normal;color:{A['key']};box-shadow:inset 0 -.3em 0 {A['hi']}}}</style>")
    js = (f"<script>document.fonts.ready.then(function(){{var r=document.documentElement,e=document.getElementById('tt'),best=1;for(var s=1;s<=3;s+=0.02){{r.style.setProperty('--s',s);if(e.getBoundingClientRect().height>{hmax-14}||e.scrollWidth>1102)break;best=s}}r.style.setProperty('--s',best)}});</script>")
    return css + f'<div class="tb"></div><div class="tt" id="tt"><div class="k">{kick}</div><div class="h">{title}</div></div>' + js
_main = m.main_html
def main_html(a, key, lang, bgp):
    if m.LAY[(a, key)][0] == "N": return m.page(a, lang, "", 1600, 900, bgp, 0)  # picture carries its own labels
    if (a, key) == ("se", "cover"):
        b = 1 if lang == "bn" else 0; kick, title, rows = m.T[(a, key)][0][b], m.T[(a, key)][1][b], m.T[(a, key)][2][b]
        return m.page(a, lang, m.left_block(a, lang, kick, title, [], 330, 40, 470, sub=rows[0], by=None), 1600, 900, bgp, 0)
    if m.LAY[(a, key)][0] == "T":
        b = 1 if lang == "bn" else 0; kick, title = m.T[(a, key)][0][b], m.T[(a, key)][1][b]
        return m.page(a, lang, top_block(a, lang, kick, title), 1600, 900, bgp, 0)
    return _main(a, key, lang, bgp)
_soc = m.social_html
def social_html(a, lang, bgp):
    if a == "se":
        b = 1 if lang == "bn" else 0; kick, title, sub = m.SOC[a][0][b], m.SOC[a][1][b], m.SOC[a][2][b]
        r = f'<div class="r" style="width:520px"><div class="sub">{sub}</div><div class="by">{m.BY[b]}</div></div>'
        return m.page(a, lang, m.band_block(a, lang, kick, title, [], 840, 440, right_html=r, left_w=860, right_w=520), 1600, 840, bgp, -30)
    return _soc(a, lang, bgp)
if __name__ == "__main__":
    only = set(sys.argv[1:]); stamp = []; tmp = BG / "_t.html"
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1300); pg.screenshot(path=str(out)); pg.close()
        for iid, (a, key) in M5.items():
            if only and a not in only and f"{a}-{key}" not in only: continue
            A = m.ART[a]; out = R / "assets/img/blog" / A["dir"]; out.mkdir(parents=True, exist_ok=True); bgp = BG / f"{a}-{key}.webp"
            Image.open(m.SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS).save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(main_html(a, key, lang, bgp), 1600, 900, png)
                dst = out / (f"{A['pre']}-{key}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6); stamp.append([f"/assets/img/blog/{A['dir']}/{dst.name}", "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(social_html(a, lang, bgp), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"{A['pre']}-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en":
                        sm.save(out / f"{A['pre']}-card.webp", "WEBP" if False else "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / f"{A['pre']}-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open("/tmp/stamp_q5.json", "w")); print(len(stamp), "images")
