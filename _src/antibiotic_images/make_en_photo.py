#!/usr/bin/env python3
"""Bangla photo-style infographics: Hugging Face (Z-Image Turbo) background photo + Bangla text set in code."""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
NAME = "Sayedul Abrar"
BY = f"By {NAME}, Pharmacist"
CSS = f"""
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anton;src:url({U}/anton-latin-400-normal.woff2)}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-800-normal.woff2);font-weight:800;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-700-normal.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;font-family:Poppins,HS,sans-serif;color:#173d43;position:relative;background:#f7f4ee}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:right center}}
.fade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(250,248,243,.97) 0%,rgba(250,248,243,.94) var(--a,46%),rgba(250,248,243,0) var(--b,66%))}}
.col{{position:absolute;left:72px;top:54px;bottom:96px;width:var(--w,900px);display:flex;flex-direction:column}}
.kick{{font-size:21px;font-weight:600;color:#2f8f83;letter-spacing:.14em;text-transform:uppercase}}
h1{{font-size:50px;line-height:1.18;font-weight:700;margin-top:2px}}
.list{{display:flex;flex-direction:column;gap:16px;margin-top:22px;flex:1;justify-content:center}}
.row{{display:flex;gap:20px;align-items:center;background:rgba(255,255,255,.88);border:1px solid #e3eeec;border-radius:22px;padding:18px 24px;box-shadow:0 10px 26px rgba(23,61,67,.08)}}
.n{{width:52px;height:52px;border-radius:50%;background:#17656a;color:#fff;font-weight:700;font-size:28px;display:flex;align-items:center;justify-content:center;flex:none}}
.t{{font-size:28px;font-weight:700;line-height:1.25}}
.p{{font-size:22px;line-height:1.45;color:#3f5a63}}
.note{{margin-top:16px;font-size:26px;font-weight:700;border-radius:16px;padding:14px 22px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:62px;display:flex;justify-content:space-between;align-items:center;padding:0 72px;font-size:20px;color:#5b6f75;background:rgba(250,248,243,.92);border-top:1px solid #e2ebe8}}
.foot b{{color:#17656a}}
.t{{font-size:34px!important;line-height:1.22!important}}.p{{font-size:27px!important;line-height:1.38!important;color:#2d464e!important}}h1{{font-size:58px!important}}.kick{{font-size:24px!important}}.note{{font-size:28px!important}}.row{{background:rgba(255,255,255,.95)!important}}.foot{{font-size:22px!important;height:66px!important}}.tag{{position:absolute;right:40px;bottom:78px;font-size:18px;color:#5b6f75;background:rgba(255,255,255,.85);padding:6px 14px;border-radius:999px}}
.kick{{display:flex;align-items:center;gap:12px;color:#17807a!important;font-weight:700!important}}
.kick:before{{content:"";width:46px;height:4px;border-radius:2px;background:linear-gradient(90deg,#17807a,#e0892b);flex:none}}
h1 em{{font-style:normal;background:linear-gradient(90deg,#0f8f86,#17656a 55%,#e0892b);-webkit-background-clip:text;background-clip:text;color:transparent}}
h1{{color:#0f3c42!important}}
.n{{background:#0f3c42!important;box-shadow:0 0 0 4px rgba(255,255,255,.9)}}
.kick{{letter-spacing:.22em!important;font-size:21px!important}}
h1{{font-family:Anton,Impact,sans-serif;font-weight:400!important;text-transform:uppercase;font-size:66px!important;line-height:1.0!important;letter-spacing:.005em}}
.n{{font-family:Anton,sans-serif!important;font-weight:400!important}}
"""
def ic(ok):
    if ok == "ok": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#1f7a57"/><path d="M15 27l7 8 15-17" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    if ok == "no": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#b8433f"/><path d="M17 17l18 18M35 17L17 35" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
    if ok == "q": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#e0892b"/><text x="26" y="37" text-anchor="middle" font-size="30" font-weight="700" fill="#fff" font-family="Poppins">?</text></svg>'
def page(bg, body, src, a="46%", b="66%", w="900px", tag=""):
    t = f'<div class="tag">{tag}</div>' if tag else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="bg" style="background-image:url({U}/bg/{bg}.webp)"></div><div class="fade" style="--a:{a};--b:{b}"></div>'
            f'<div class="col" style="--w:{w}">{body}</div>{t}<div class="foot"><span>Sources: {src}</span><b>{NAME}, Pharmacist · sayedulabrar.site</b></div></body></html>')
def rows(items):
    return '<div class="list">' + "".join(
        f'<div class="row">{lead}<div><p class="t">{a}</p>' + (f'<p class="p">{b}</p>' if b else "") + '</div></div>' for lead, a, b in items) + "</div>"
N = lambda i: f'<div class="n">{"12345"[i]}</div>'

P = {}
P["cover"] = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
  f'<div class="bg" style="background-image:url({U}/bg/cover.webp)"></div><div class="fade" style="--a:42%;--b:60%"></div>'
  f'<div style="position:absolute;left:80px;top:150px;width:640px"><p class="kick">Health Made Simple</p>'
  f'<h1 style="font-size:92px!important;line-height:.98!important;margin-top:14px">Why You Must <em>Complete</em> an Antibiotic Course</h1>'
  f'<p style="font-size:32px;color:#4c6670;margin-top:16px">…and how antibiotic resistance starts</p>'
  f'<p style="display:inline-block;margin-top:38px;background:#17656a;color:#fff;font-weight:600;font-size:27px;padding:12px 28px;border-radius:999px">{BY}</p></div></body></html>')

P["resistance"] = page("resistance", '<p class="kick">Simplified</p><h1>How antibiotic <em>resistance</em> develops</h1>' + rows([
  (N(0), "An infection has many bacteria", "A few may naturally be less sensitive to the medicine."),
  (N(1), "The antibiotic kills the sensitive ones", "Misuse and overuse give resistant bacteria more chances to survive."),
  (N(2), "Survivors multiply and can spread", "Next time, the same antibiotic may not work.")]) +
  '<p class="note" style="background:#fdf0ee;color:#a8362f">Resistance happens to the bacteria, not to your body.</p>', "WHO; MedlinePlus", a="44%", b="60%", w="860px", tag="Illustrative photo")

P["viruses"] = page("viruses", '<p class="kick">The basics</p><h1>Antibiotics treat bacteria, <em>not viruses</em></h1>' + rows([
  (ic("ok"), "Bacterial infections", "A doctor prescribes an antibiotic when one is needed. Not every bacterial infection needs one."),
  (ic("no"), "Viral illnesses: colds and flu", "Antibiotics do not work on viruses and will not make you feel better.")]) +
  '<p class="note" style="background:#fff5df;border:1px solid #f0d99e">A fever or cough does not automatically mean you need an antibiotic. Let a doctor decide.</p>', "CDC", a="44%", b="58%", w="860px")

def two(h, items, ok):
    c = "#1f7a57" if ok else "#b8433f"; bg = "rgba(236,247,242,.93)" if ok else "rgba(251,238,236,.93)"
    li = "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:16px">{ic("ok" if ok else "no")}<p class="p" style="font-size:23px;color:#173d43">{x}</p></div>' for x in items)
    return f'<div style="flex:1;background:{bg};border-radius:22px;padding:22px 24px;box-shadow:0 10px 26px rgba(23,61,67,.08)"><p class="t" style="color:{c};font-size:34px">{h}</p>{li}</div>'
P["dosdonts"] = page("dosdonts", '<p class="kick">Do’s and don’ts</p><h1>How to take antibiotics <em>the right way</em></h1>'
  '<div style="display:flex;gap:22px;margin-top:24px;flex:1;align-items:stretch">' +
  two("Do", ["Take them exactly as prescribed", "Finish the course, even if you feel better, unless your doctor says otherwise", "Take each dose at the right time", "Tell your doctor or pharmacist about side effects"], True) +
  two("Don’t", ["Stop early on your own", "Save leftovers for a future illness", "Share them, or take someone else’s", "Buy them without a prescription"], False) +
  '</div>', "CDC; NHS; MedlinePlus", a="58%", b="74%", w="1060px")

P["missed"] = page("missed", '<p class="kick">Missed dose</p><h1><em>Missed a dose</em> of your antibiotic?</h1>' + rows([
  (ic("ok"), "Take it as soon as you remember", "Then carry on with your usual schedule."),
  (ic("q"), "Is the next dose almost due?", "Skip the missed dose and take the next one at the usual time."),
  (ic("no"), "Never take a double dose", "Do not take two doses to make up for a missed one.")]) +
  '<p class="note" style="background:rgba(255,255,255,.88);font-size:24px;font-weight:600">Not sure? Ask your doctor or pharmacist. Your own leaflet may give specific advice.</p>',
  "NHS patient leaflet; MedlinePlus", a="44%", b="60%", w="860px")

P["redlabel"] = page("redlabel", '<p class="kick" style="color:#b8433f">Bangladesh</p><h1>The <em>red mark</em> on antibiotic packs</h1>' + rows([
  (N(0), "What is it?", "Since December 2022, DGDA requires a red mark on antibiotic packs."),
  (N(1), "What does it say?", "“Antibiotic” and “Do not use without a prescription of registered physician”."),
  (N(2), "What should you do?", "Red mark = antibiotic. Take it only with a doctor’s prescription.")]) ,
  "WHO Bangladesh (DGDA, Drug Control Committee)", a="50%", b="60%", w="880px", tag="Illustrative photo, not a real product")

def tier(h, c, items, note):
    return (f'<div class="row" style="border-left:10px solid {c};align-items:flex-start;flex-direction:column;gap:4px;padding:16px 24px">'
            f'<p class="t" style="color:{c};font-size:30px">{h}</p><p class="p" style="color:#173d43">{" · ".join(items)}</p><p class="p" style="font-weight:700;color:{c};font-size:21px">{note}</p></div>')
P["sideeffects"] = page("sideeffects", '<p class="kick">Side effects</p><h1>When to <em>get help</em></h1><div class="list">' +
  tier("Common", "#2f8f83", ["Feeling or being sick", "Bloating or indigestion", "Diarrhoea"], "Usually mild. Ask a pharmacist if you are worried.") +
  tier("Tell your doctor", "#c27a12", ["Severe or watery diarrhoea", "Severe or worrying side effects", "Extra doses taken by mistake"], "Do not stop or change the medicine on your own.") +
  tier("Emergency", "#b8433f", ["Swelling of the face, lips or tongue", "Difficulty breathing"], "Can be signs of a serious allergic reaction. Get emergency help immediately.") +
  '</div>', "NHS patient leaflet (June 2025); not a complete list", a="48%", b="62%", w="880px")

P["takeaways"] = page("takeaways", '<p class="kick">Key takeaways</p><h1>Antibiotics: <em>5 things</em> to remember</h1><div class="list" style="gap:10px;margin-top:14px">' + "".join(
  f'<div class="row" style="padding:12px 22px">{N(i)}<div><p class="t" style="font-size:26px">{a}</p><p class="p" style="font-size:21px">{b}</p></div></div>' for i, (a, b) in enumerate([
  ("Finish the course", "Even if you feel better, unless your doctor says otherwise."),
  ("Only with a prescription", "In Bangladesh, the red mark tells you it is an antibiotic."),
  ("Not for viruses", "Antibiotics do not work on colds and flu."),
  ("Don’t save or share", "Ask a pharmacist how to get rid of leftovers."),
  ("Never double a missed dose", "Take doses on time and report side effects.")])) + '</div>',
  "NHS; CDC; MedlinePlus; WHO Bangladesh", a="46%", b="60%", w="900px")

NAMES = {"cover": "why-complete-antibiotic-course-cover-16x9", "resistance": "how-antibiotic-resistance-develops-simplified", "viruses": "antibiotics-treat-bacteria-not-viruses-cold-flu",
 "dosdonts": "antibiotic-dos-and-donts-take-as-prescribed", "missed": "missed-antibiotic-dose-what-to-do", "redlabel": "bangladesh-red-mark-on-antibiotic-packs-dgda",
 "sideeffects": "antibiotic-side-effects-when-to-get-help", "takeaways": "antibiotics-key-takeaways"}
with sync_playwright() as p:
    br = p.chromium.launch()
    for k, htm in P.items():
        pg = br.new_page(viewport={"width": 1600, "height": 900})
        f = H / "_en.html"; f.write_text(htm, encoding="utf-8"); pg.goto(f.as_uri()); pg.wait_for_timeout(500)
        over = pg.evaluate("()=>{const c=document.querySelector('.col');return c?c.scrollHeight>c.clientHeight+2:false}")
        im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
        out = OUT / f"{NAMES[k]}.webp"; im.save(out, "WEBP", quality=88, method=6)
        print(("OVERFLOW " if over else "") + out.name, out.stat().st_size)
        if k == "cover":
            im.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652)).save(OUT / "social-en.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    br.close()
