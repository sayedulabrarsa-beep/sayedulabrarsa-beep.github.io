#!/usr/bin/env python3
"""Drug Excretion article graphics (EN + BN), cinematic house style, on the user's 7 text-free AI images.
Palette/fonts: 'Drug Excretion Article Visual Style Guide' (Clinical Teal; Manrope / Inter / Noto Sans Bengali).
Usage: python3 make_exc.py OUTDIR"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
F = (H / "fonts").as_uri(); BG = (H / "bg").as_uri()
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
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(247,241,230,.98) 0%,rgba(247,241,230,.95) 31%,rgba(247,241,230,0) 42%)}}
.panel{{position:absolute;left:72px;top:0;bottom:58px;width:var(--pw,560px);display:flex;flex-direction:column;justify-content:center}}
.kick{{display:flex;align-items:center;gap:12px;font-weight:600;font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:var(--sage)}}
.kick:before{{content:"";width:40px;height:4px;border-radius:2px;background:var(--amber)}}
body.bn .kick{{letter-spacing:.02em;text-transform:none;font-size:27px;font-weight:700}}
h1{{font-family:Man,sans-serif;font-weight:800;font-size:var(--ts,76px);line-height:1.08;letter-spacing:-.01em;margin-top:14px;color:var(--teal)}}
body.bn h1{{font-family:NB;font-weight:700;font-size:var(--tb,64px);line-height:1.25;letter-spacing:0}}
h1 .box{{display:inline-block;background:var(--teal);color:var(--cream);padding:0 .2em;border-radius:12px;box-shadow:0 0 0 3px rgba(217,154,67,.9) inset}}
h1 .hl{{background:linear-gradient(transparent 58%,rgba(217,154,67,.95) 58%,rgba(217,154,67,.95) 92%,transparent 92%);padding:0 .06em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
h1 .amb{{color:var(--amber)}}
.sub{{font-size:28px;line-height:1.42;margin-top:16px;font-weight:500;color:var(--char)}}
body.bn .sub{{font-size:30px;line-height:1.55}}
.cards{{display:flex;flex-direction:column;gap:12px;margin-top:20px}}
.card{{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.94);border-left:6px solid var(--amber);border-radius:14px;padding:12px 16px;box-shadow:0 6px 18px rgba(11,52,56,.10)}}
.card .t{{font-size:23px;line-height:1.36}}
body.bn .card .t{{font-size:26px;line-height:1.5}}
.card .t b{{display:block;font-family:Man;font-weight:800;font-size:26px;line-height:1.2;color:var(--teal);margin-bottom:2px}}
body.bn .card .t b{{font-family:NB;font-size:29px;font-weight:700}}
.card.dark{{background:var(--teal);color:var(--cream)}}.card.dark .t b{{color:var(--cream)}}
.card.pa{{background:var(--pamber)}}
.card.sg{{background:var(--psage);border-left-color:var(--sage)}}
.badge{{flex:none;width:42px;height:42px;border-radius:12px;background:var(--teal);color:var(--cream);font-family:Man,NB;font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center;margin-top:2px}}
body.bn .badge{{font-family:NB;font-weight:700}}
.card.dark .badge{{background:var(--amber);color:var(--teal)}}
.mk{{position:absolute;width:50px;height:50px;margin:-25px 0 0 -25px;border-radius:50%;background:var(--teal);color:var(--cream);font-family:Man,NB;font-weight:800;font-size:25px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff,0 0 0 10px rgba(217,154,67,.75),0 10px 24px rgba(0,0,0,.35)}}
.call{{position:absolute;background:#fff;border-radius:14px;padding:11px 16px;box-shadow:0 10px 26px rgba(11,52,56,.28);border-left:6px solid var(--teal);max-width:310px}}
.call b{{display:block;font-family:Man;font-weight:800;font-size:23px;line-height:1.15;color:var(--teal)}}
body.bn .call b{{font-family:NB;font-weight:700;font-size:26px;line-height:1.3}}
.call span{{display:block;font-size:19px;line-height:1.35;margin-top:3px}}
body.bn .call span{{font-size:22px}}
svg.ld{{position:absolute;inset:0;pointer-events:none}}
.ai{{position:absolute;right:30px;bottom:70px;background:rgba(247,241,230,.92);color:var(--char);font-size:15px;font-weight:500;padding:4px 12px;border-radius:999px}}
body.bn .ai{{font-size:17px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:54px;display:flex;justify-content:space-between;align-items:center;padding:0 72px;font-size:17px;color:#3C5558;background:rgba(247,241,230,.96)}}
body.bn .foot{{font-size:19px}}
.foot b{{color:var(--teal);font-weight:600}}
"""
SRC = {"en": "Sources: Goodman &amp; Gilman; StatPearls; Merck Manual", "bn": "সূত্র: Goodman &amp; Gilman; StatPearls; Merck Manual"}
AUTH = {"en": "<b>Sayedul Abrar, Pharmacist</b> · sayedulabrar.site", "bn": "<b>সাইয়্যেদুল আবরার, ফার্মাসিস্ট</b> · sayedulabrar.site"}
AIT = {"en": "AI-generated illustration", "bn": "AI-তৈরি চিত্র"}
def card(head, body, cls="", n=None):
    b = f'<span class="badge">{n}</span>' if n else ""
    h = f"<b>{head}</b>" if head else ""
    return f'<div class="card {cls}">{b}<div class="t">{h}{body}</div></div>'
def mk(n, x, y): return f'<div class="mk" style="left:{x}px;top:{y}px">{n}</div>'
def call(x, y, head, body="", w=None):
    st = f"left:{x}px;top:{y}px" + (f";max-width:{w}px" if w else "")
    return f'<div class="call" style="{st}"><b>{head}</b>' + (f"<span>{body}</span>" if body else "") + "</div>"
def line(x1, y1, x2, y2): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/><circle cx="{x2}" cy="{y2}" r="30" fill="none" stroke="#fff" stroke-width="4"/>'
def page(lang, d):
    lines = d.get("lines", "")
    ov = d.get("ov", "")
    s = f"--ts:{d.get('ts',76)}px;--tb:{d.get('tb',64)}px;--pw:{d.get('pw',560)}px"
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{lang}" style="{s}">
<div class="bg" style="background-image:url({BG}/{d['bg']}.webp)"></div><div class="veil"></div>
<svg class="ld" width="1600" height="900">{lines}</svg>{ov}
<div class="panel"><div class="kick">{d['kick']}</div><h1>{d['title']}</h1>{('<p class="sub">'+d['sub']+'</p>') if d.get('sub') else ''}<div class="cards">{d.get('cards','')}</div></div>
<div class="ai">{AIT[lang]}</div><div class="foot"><span>{SRC[lang]}</span><span>{AUTH[lang]}</span></div></body></html>'''

S = {}
def add(key, en, bn, geo=None, both=None):
    S[key] = {"en": page("en", {**(geo or {}), **en}), "bn": page("bn", {**(geo or {}), **bn})}

# cover
add("cover",
 dict(bg="anatomy", kick="Drug excretion", title='HOW MEDICINES <span class="box">LEAVE</span> THE BODY', sub="Kidneys, bile and other routes explained in simple words.", ts=88, tb=60,
      ov=call(1260, 60, "Kidneys", "Filter the blood", 250) + call(1330, 690, "Bladder", "Stores urine", 250),
      lines=line(1380, 125, 1395, 275) + line(1330, 725, 1210, 690)),
 dict(bg="anatomy", kick="ওষুধের নিঃসরণ", title='শরীর থেকে ওষুধ কীভাবে <span class="box">বের হয়</span>', sub="কিডনি, পিত্ত ও অন্যান্য পথ সহজ ভাষায়।", tb=68,
      ov=call(1260, 60, "কিডনি", "রক্ত ছেঁকে নেয়", 250) + call(1330, 690, "মূত্রথলি", "প্রস্রাব জমা রাখে", 250),
      lines=line(1380, 125, 1395, 275) + line(1330, 725, 1210, 690)))
# nephron
add("nephron",
 dict(bg="nephron", kick="Why it matters", title='INSIDE A <span class="hl">NEPHRON</span>', sub="The kidney’s filtering unit turns blood into urine.", ts=100,
      ov=call(1130, 60, "Glomerulus", "Blood is filtered here", 300) + call(1190, 690, "Tubule", "Filtrate is processed", 300),
      lines=line(1190, 120, 905, 330) + line(1250, 700, 1090, 610)),
 dict(bg="nephron", kick="কেন গুরুত্বপূর্ণ", title='<span class="hl">নেফ্রনের</span> ভেতরে', sub="কিডনির ছাঁকনি একক রক্ত থেকে প্রস্রাব তৈরি করে।", tb=84,
      ov=call(1130, 60, "Glomerulus", "এখানে রক্ত ছাঁকা হয়", 300) + call(1190, 690, "Tubule", "filtrate-এর প্রক্রিয়া চলে", 300),
      lines=line(1190, 120, 905, 330) + line(1250, 700, 1090, 610)))
# processes
add("processes",
 dict(bg="tubule", kick="Renal handling", title='THREE <span class="box">RENAL</span> PROCESSES', ts=76, pw=500,
      cards=card("Filtration", "Unbound drug enters the filtrate.", n=1) + card("Secretion", "Transporters add some drugs to the tubule.", n=2) + card("Reabsorption", "Some drug moves back into the blood.", n=3),
      ov=mk(1, 820, 520) + mk(2, 1160, 520) + mk(3, 1420, 215)),
 dict(bg="tubule", kick="কিডনিতে ওষুধের পথ", title='কিডনির তিনটি <span class="box">প্রক্রিয়া</span>', tb=64, pw=500,
      cards=card("Filtration", "protein-এ যুক্ত নয় এমন ওষুধ filtrate-এ যায়।", n=1) + card("Secretion", "transporter কিছু ওষুধ tubule-এ যোগ করে।", n=2) + card("Reabsorption", "কিছু ওষুধ আবার রক্তে ফিরে যায়।", n=3),
      ov=mk(1, 820, 520) + mk(2, 1160, 520) + mk(3, 1420, 215)))
# bile-gut
add("bile-gut",
 dict(bg="bile", kick="Other routes", title='LIVER, <span class="hl">BILE</span> AND GUT', ts=84,
      cards=card("", "The liver sends some drugs and metabolites into bile.", n=1) + card("", "Bile carries them to the intestine.", n=2) + card("", "Many then leave in the faeces.", n=3),
      ov=mk(1, 1180, 290) + mk(2, 1140, 500) + mk(3, 1090, 700)),
 dict(bg="bile", kick="অন্যান্য পথ", title='যকৃৎ, <span class="hl">পিত্ত</span> ও অন্ত্র', tb=76,
      cards=card("", "যকৃৎ কিছু ওষুধ ও metabolite পিত্তে পাঠায়।", n=1) + card("", "পিত্ত সেগুলো অন্ত্রে নিয়ে যায়।", n=2) + card("", "অনেক ক্ষেত্রে মলের সঙ্গে বের হয়ে যায়।", n=3),
      ov=mk(1, 1180, 290) + mk(2, 1140, 500) + mk(3, 1090, 700)))
# kidney function
add("kidney-function",
 dict(bg="kidneys-compare", kick="Illustration only", title='KIDNEY FUNCTION AND <span class="hl">DRUG LEVELS</span>', ts=62,
      cards=card("Healthy kidneys", "Clear many medicines efficiently.", n=1) + card("Reduced function", "Some drugs stay longer, so a prescriber may adjust the dose.", "pa", n=2),
      ov=mk(1, 1000, 560) + mk(2, 1440, 540)),
 dict(bg="kidneys-compare", kick="ব্যাখ্যামূলক চিত্র", title='কিডনির কার্যক্ষমতা ও <span class="hl">ওষুধের মাত্রা</span>', tb=58,
      cards=card("সুস্থ কিডনি", "অনেক ওষুধ সহজে বের করে।", n=1) + card("কার্যক্ষমতা কমলে", "কিছু ওষুধ বেশি সময় থাকে; তাই চিকিৎসক ডোজ বদলাতে পারেন।", "pa", n=2),
      ov=mk(1, 1000, 560) + mk(2, 1440, 540)))
# pH + recirculation
add("ph-recirculation",
 dict(bg="recirc", kick="Two details", title='URINE pH AND <span class="box">RECIRCULATION</span>', ts=54,
      cards=card("Urine pH", "Changes how ionised a drug is, so reabsorption can change.", "dark", n=1) + card("Recirculation", "Bile, gut and blood can form a loop that prolongs exposure.", "pa", n=2),
      ov=mk(1, 1420, 215) + mk(2, 1370, 660)),
 dict(bg="recirc", kick="দুটি গুরুত্বপূর্ণ বিষয়", title='প্রস্রাবের pH ও <span class="box">পুনঃসঞ্চালন</span>', tb=62,
      cards=card("প্রস্রাবের pH", "ওষুধের ionisation বদলায়, ফলে পুনঃশোষণও বদলাতে পারে।", "dark", n=1) + card("পুনঃসঞ্চালন", "পিত্ত, অন্ত্র ও রক্ত মিলে একটি চক্র হতে পারে, যা ওষুধকে বেশি সময় রাখে।", "pa", n=2),
      ov=mk(1, 1420, 215) + mk(2, 1370, 660)))
# water
add("water-myth",
 dict(bg="water", kick="Common question", title='DOES EXTRA WATER <span class="hl">FLUSH</span> DRUGS OUT?', ts=58,
      cards=card("Not reliably", "Excess water can be harmful for some people.", "pa") + card("", "Follow normal hydration advice and your prescriber’s instructions.")),
 dict(bg="water", kick="সাধারণ প্রশ্ন", title='বেশি পানি কি ওষুধ <span class="hl">বের করে</span> দেয়?', tb=58,
      cards=card("নির্ভরযোগ্যভাবে নয়", "অতিরিক্ত পানি কারও কারও জন্য ক্ষতিকর হতে পারে।", "pa") + card("", "স্বাভাবিক পানি পানের নিয়ম ও চিকিৎসকের নির্দেশ মানুন।")))
# takeaways
add("key-takeaways",
 dict(bg="anatomy", kick="Drug excretion", title='<span class="box">KEY</span> TAKEAWAYS', ts=96,
      cards=card("", "Excretion removes drugs and metabolites.", n=1) + card("", "Kidneys are a major route; bile and other routes help.", n=2) + card("", "Clearance is the body’s capacity to remove a drug.", n=3) + card("", "Kidney function can change drug exposure and dosing.", n=4)),
 dict(bg="anatomy", kick="ওষুধের নিঃসরণ", title='<span class="box">মূল</span> কথা', tb=88,
      cards=card("", "Excretion শরীর থেকে ওষুধ ও metabolite বের করে।", n=1) + card("", "কিডনি প্রধান পথ; পিত্ত ও অন্যান্য পথও ভূমিকা রাখে।", n=2) + card("", "Clearance শরীরের ওষুধ অপসারণের সক্ষমতা।", n=3) + card("", "কিডনির কার্যক্ষমতা ওষুধের মাত্রা ও ডোজে প্রভাব ফেলতে পারে।", n=4)))

if __name__ == "__main__":
    only = sys.argv[2:] or list(S)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1600, "height": 900})
        for key in only:
            for lang, html in S[key].items():
                f = H / f"_tmp_{key}_{lang}.html"; f.write_text(html, encoding="utf-8")
                pg.goto(f.as_uri()); pg.wait_for_timeout(400)
                im = Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB")
                im.save(OUT / (f"excretion-{key}" + ("-bn" if lang == "bn" else "") + ".webp"), quality=84, method=6)
                if key == "cover":
                    im.crop((0, 15, 1600, 855)).resize((1200, 630), Image.LANCZOS).save(OUT / f"excretion-social-{lang}.jpg", quality=86, optimize=True)
                f.unlink()
        b.close()
    print("done", OUT)
