#!/usr/bin/env python3
"""Drug Excretion article graphics (EN + BN) on the user's 7 text-free AI images.
Style: 'Drug Excretion Article Visual Style Guide' (Clinical Teal; Manrope / Inter / Noto Sans Bengali).
Usage: python3 make_exc.py OUTDIR"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
F = (H / "fonts").as_uri()
BG = (H / "bg").as_uri()
CSS = f"""
@font-face{{font-family:Man;src:url({F}/manrope-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Man;src:url({F}/manrope-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:Man;src:url({F}/manrope-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:Int;src:url({F}/inter-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:Int;src:url({F}/inter-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:Int;src:url({F}/inter-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:NB;src:url({F}/noto-sans-bengali-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:NB;src:url({F}/noto-sans-bengali-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:NB;src:url({F}/noto-sans-bengali-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
:root{{--teal:#0B3438;--cream:#F7F1E6;--amber:#D99A43;--sage:#3C8580;--char:#263638;--sand:#E8E0D3;--psage:#E9F1ED;--pamber:#FFF4E4}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;position:relative;background:var(--cream);font-family:Int,NB,sans-serif;color:var(--char)}}
body.bn{{font-family:NB,Int,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(247,241,230,.98) 0%,rgba(247,241,230,.94) 30%,rgba(247,241,230,0) 41%)}}
.panel{{position:absolute;left:72px;top:0;bottom:0;width:{{pw}}px;display:flex;flex-direction:column;justify-content:center}}
.kick{{display:flex;align-items:center;gap:12px;font-weight:600;font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:var(--sage)}}
.kick:before{{content:"";width:34px;height:4px;border-radius:2px;background:var(--amber)}}
body.bn .kick{{letter-spacing:.01em;text-transform:none;font-size:25px;font-weight:700}}
h1{{font-family:Man,sans-serif;font-weight:800;font-size:56px;line-height:1.12;color:var(--teal);margin-top:14px;letter-spacing:-.01em}}
body.bn h1{{font-family:NB;font-weight:700;font-size:50px;line-height:1.28;letter-spacing:0}}
.sub{{font-size:26px;line-height:1.45;margin-top:14px;font-weight:500}}
body.bn .sub{{font-size:29px;line-height:1.6}}
.rule{{width:64px;height:5px;border-radius:3px;background:var(--amber);margin:20px 0 4px}}
.cards{{display:flex;flex-direction:column;gap:12px;margin-top:18px}}
.card{{background:var(--psage);border:1px solid var(--sand);border-left:5px solid var(--sage);border-radius:14px;padding:13px 16px;font-size:24px;line-height:1.38}}
body.bn .card{{font-size:27px;line-height:1.5}}
.card b{{display:block;font-family:Man;font-weight:700;color:var(--teal);font-size:25px;margin-bottom:2px}}
body.bn .card b{{font-family:NB;font-size:28px}}
.card.amber{{background:var(--pamber);border-left-color:var(--amber)}}
.card.dark{{background:var(--teal);border:0;border-left:5px solid var(--amber);color:var(--cream)}}
.card.dark b{{color:var(--cream)}}
.num{{display:inline-flex;width:34px;height:34px;border-radius:50%;background:var(--amber);color:var(--teal);font-family:Man;font-weight:800;font-size:19px;align-items:center;justify-content:center;margin-right:10px;vertical-align:middle}}
.row{{display:flex;align-items:flex-start;gap:12px}}
.row .num{{flex:none;margin-top:1px}}
.tag{{display:inline-block;margin-top:16px;align-self:flex-start;background:#fff;border:1px solid var(--sand);color:var(--teal);border-radius:999px;padding:6px 16px;font-size:19px;font-weight:600}}
body.bn .tag{{font-size:21px}}
"""
def card(c):
    cls, head, body = c
    return f'<div class="card {cls}"><b>{head}</b>{body}</div>' if head else f'<div class="card {cls}">{body}</div>'
def num_card(i, head, body, cls=""):
    return f'<div class="card {cls}"><div class="row"><span class="num">{i}</span><div><b>{head}</b>{body}</div></div></div>'
def page(lang, bg, kick, title, sub="", cards="", tag="", pw=520, tsize=None):
    st = f"<style>h1{{font-size:{tsize}px}}</style>" if tsize else ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("{pw}", str(pw+40))}</style>{st}</head>
<body class="{lang}"><div class="bg" style="background-image:url({BG}/{bg}.webp)"></div><div class="veil"></div>
<div class="panel"><div class="kick">{kick}</div><h1>{title}</h1>{('<p class="sub">'+sub+'</p>') if sub else '<div class="rule"></div>'}
<div class="cards">{cards}</div>{('<span class="tag">'+tag+'</span>') if tag else ''}</div></body></html>'''

S = {}  # key -> {lang: html}
def add(key, bg, en, bn, **kw):
    S[key] = {"en": page("en", bg, **en, **kw), "bn": page("bn", bg, **bn, **kw)}

add("cover", "anatomy",
    dict(kick="Pharmacology basics", title="How medicines leave the body", sub="The kidneys are a major route. Bile and other routes also help."),
    dict(kick="ফার্মাকোলজির মূল ধারণা", title="শরীর থেকে ওষুধ কীভাবে বের হয়", sub="কিডনি একটি প্রধান পথ; পিত্ত ও অন্যান্য পথও ভূমিকা রাখে।"), pw=500)
add("nephron", "nephron",
    dict(kick="Inside the kidney", title="Inside a nephron", cards=card(("", "Glomerulus", "Blood is filtered and a filtrate forms.")) + card(("", "Tubule", "The filtrate is processed on its way to urine."))),
    dict(kick="কিডনির ভেতরে", title="নেফ্রনের ভেতরে", cards=card(("", "Glomerulus", "রক্ত ছেঁকে filtrate তৈরি হয়।")) + card(("", "Tubule", "প্রস্রাবে পৌঁছানোর পথে filtrate-এর পরিবর্তন হয়।"))), pw=500)
add("processes", "tubule",
    dict(kick="Renal handling of drugs", title="Three renal processes", cards=num_card(1, "Filtration", "Unbound drug enters the filtrate.") + num_card(2, "Secretion", "Transporters add some drugs to the tubule.") + num_card(3, "Reabsorption", "Some drug moves back into the blood."), ),
    dict(kick="কিডনিতে ওষুধের পথ", title="কিডনির তিনটি প্রক্রিয়া", cards=num_card(1, "Filtration", "protein-এ যুক্ত নয় এমন ওষুধ filtrate-এ যায়।") + num_card(2, "Secretion", "transporter কিছু ওষুধ tubule-এ যোগ করে।") + num_card(3, "Reabsorption", "কিছু ওষুধ আবার রক্তে ফিরে যায়।")), pw=500, tsize=50)
add("bile-gut", "bile",
    dict(kick="Other routes", title="Liver, bile and gut", cards=card(("", "", "The liver can send some drugs and metabolites into bile.")) + card(("", "", "Bile carries them to the intestine.")) + card(("", "", "Many then leave in the faeces."))),
    dict(kick="অন্যান্য পথ", title="যকৃৎ, পিত্ত ও অন্ত্র", cards=card(("", "", "যকৃৎ কিছু ওষুধ ও metabolite পিত্তে পাঠাতে পারে।")) + card(("", "", "পিত্ত সেগুলো অন্ত্রে নিয়ে যায়।")) + card(("", "", "অনেক ক্ষেত্রে মলের সঙ্গে বের হয়ে যায়।"))), pw=500)
add("kidney-function", "kidneys-compare",
    dict(kick="Kidney function", title="Kidney function and drug exposure", cards=card(("", "Healthy kidneys", "Clear many medicines efficiently.")) + card(("amber", "Reduced function", "Some drugs can stay longer, so a prescriber may adjust the dose.")), tag="Illustrative image, not a diagnostic image"),
    dict(kick="কিডনির কার্যক্ষমতা", title="কিডনির কার্যক্ষমতা ও ওষুধের মাত্রা", cards=card(("", "সুস্থ কিডনি", "অনেক ওষুধ সহজে বের করে।")) + card(("amber", "কার্যক্ষমতা কমলে", "কিছু ওষুধ বেশি সময় থাকতে পারে; তাই চিকিৎসক ডোজ বদলাতে পারেন।")), tag="ব্যাখ্যামূলক চিত্র, রোগনির্ণয়ের ছবি নয়"), pw=500, tsize=46)
add("ph-recirculation", "recirc",
    dict(kick="Two details", title="Urine pH and recirculation", cards=card(("dark", "Urine pH", "Changes how ionised a drug is, so reabsorption can change.")) + card(("amber", "Recirculation", "Bile, gut and blood can form a loop that prolongs exposure."))),
    dict(kick="দুটি গুরুত্বপূর্ণ বিষয়", title="প্রস্রাবের pH ও পুনঃসঞ্চালন", cards=card(("dark", "প্রস্রাবের pH", "ওষুধের ionisation বদলায়, ফলে পুনঃশোষণও বদলাতে পারে।")) + card(("amber", "পুনঃসঞ্চালন", "পিত্ত, অন্ত্র ও রক্ত মিলে একটি চক্র হতে পারে, যা ওষুধকে বেশি সময় শরীরে রাখে।"))), pw=500, tsize=48)
add("water-myth", "water",
    dict(kick="Common question", title="Does extra water flush drugs out?", cards=card(("amber", "Not reliably", "Excess water can be harmful for some people.")) + card(("", "", "Follow normal hydration advice and your prescriber’s instructions."))),
    dict(kick="সাধারণ প্রশ্ন", title="বেশি পানি কি ওষুধ বের করে দেয়?", cards=card(("amber", "নির্ভরযোগ্যভাবে নয়", "অতিরিক্ত পানি কারও কারও জন্য ক্ষতিকর হতে পারে।")) + card(("", "", "স্বাভাবিক পানি পানের নিয়ম ও চিকিৎসকের নির্দেশ মানুন।"))), pw=500, tsize=46)
add("key-takeaways", "anatomy",
    dict(kick="Drug excretion", title="Key takeaways", cards=num_card(1, "", "Excretion removes drugs and metabolites.") + num_card(2, "", "Kidneys are a major route; bile and other routes help.") + num_card(3, "", "Clearance describes the body’s capacity to remove a drug.") + num_card(4, "", "Kidney function can change drug exposure and dosing.")),
    dict(kick="ওষুধের নিঃসরণ", title="মূল কথা", cards=num_card(1, "", "Excretion শরীর থেকে ওষুধ ও metabolite বের করে।") + num_card(2, "", "কিডনি প্রধান পথ; পিত্ত ও অন্যান্য পথও ভূমিকা রাখে।") + num_card(3, "", "Clearance শরীরের ওষুধ অপসারণের সক্ষমতা বোঝায়।") + num_card(4, "", "কিডনির কার্যক্ষমতা ওষুধের মাত্রা ও ডোজে প্রভাব ফেলতে পারে।")), pw=500)

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        for key, d in S.items():
            for lang, html in d.items():
                f = H / f"_tmp_{key}_{lang}.html"; f.write_text(html, encoding="utf-8")
                pg.goto(f.as_uri()); pg.wait_for_timeout(350)
                pg.evaluate("document.fonts.ready")
                png = pg.screenshot(type="png")
                im = Image.open(io.BytesIO(png)).convert("RGB")
                name = f"excretion-{key}" + ("-bn" if lang == "bn" else "") + ".webp"
                im.save(OUT / name, quality=84, method=6)
                if key == "cover":
                    s = im.crop((0, 15, 1600, 855)).resize((1200, 630), Image.LANCZOS)
                    s.save(OUT / f"excretion-social-{lang}.jpg", quality=86, optimize=True)
                f.unlink()
        b.close()
    print("done", OUT)
