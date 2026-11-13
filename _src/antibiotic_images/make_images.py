#!/usr/bin/env python3
"""Renders the antibiotic-course article infographics (EN + BN) to WebP with Playwright."""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
F = HERE.as_uri()

CSS = f"""
@font-face{{font-family:HS;src:url({F}/hind-siliguri-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0951-0952,U+0964-0965,U+0980-09FE,U+1CD0-1CF9,U+200C-200D,U+20B9,U+25CC,U+A8F1}}
@font-face{{font-family:HS;src:url({F}/hind-siliguri-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0951-0952,U+0964-0965,U+0980-09FE,U+1CD0-1CF9,U+200C-200D,U+20B9,U+25CC,U+A8F1}}
@font-face{{font-family:HS;src:url({F}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0951-0952,U+0964-0965,U+0980-09FE,U+1CD0-1CF9,U+200C-200D,U+20B9,U+25CC,U+A8F1}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:var(--w);height:var(--h);overflow:hidden}}
body{{font-family:Poppins,HS,sans-serif;color:#173d43;background:linear-gradient(135deg,#f3faf8 0%,#ffffff 55%,#fff6ea 100%);position:relative}}
body.bn{{font-family:HS,Poppins,sans-serif}}
.frame{{position:absolute;inset:0;padding:56px 72px 48px;display:flex;flex-direction:column}}
.kick{{font-size:20px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#2f8f83}}
body.bn .kick{{letter-spacing:.02em;font-size:24px}}
h1{{font-size:50px;line-height:1.15;font-weight:700;margin-top:8px;color:#173d43}}
body.bn h1{{font-size:54px;line-height:1.3}}
.sub{{font-size:24px;color:#4c6670;margin-top:8px}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:18px;color:#6b7f86;padding-top:14px;border-top:2px solid #dbe9e6}}
body.bn .foot{{font-size:21px}}
.brand{{font-weight:700;color:#17656a}}
.card{{background:#fff;border-radius:26px;box-shadow:0 12px 34px rgba(23,61,67,.10);border:1px solid #e3eeec}}
.num{{width:54px;height:54px;border-radius:50%;background:#17656a;color:#fff;font-weight:700;font-size:26px;display:flex;align-items:center;justify-content:center;flex:none}}
.row{{display:flex;gap:28px}}
.t{{font-size:31px;font-weight:700;line-height:1.25}}
.p{{font-size:24px;line-height:1.45;color:#3f5a63}}
body.bn .t{{font-size:34px;line-height:1.35}}
body.bn .p{{font-size:27px;line-height:1.5}}
.ok{{color:#1f7a57}} .no{{color:#b8433f}}
"""

# ---------- reusable SVG pieces ----------
def bac(x, y, r, fill="#4fb3a5", stroke="#2f8f83", rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-r*1.6}" y="{-r}" width="{r*3.2}" height="{r*2}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            f'<circle cx="{-r*.6}" cy="{-r*.2}" r="{r*.22}" fill="#fff" opacity=".55"/><circle cx="{r*.5}" cy="{r*.25}" r="{r*.16}" fill="#fff" opacity=".45"/></g>')
def rbac(x, y, r, rot=0):  # resistant bacterium: red with shield ring
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-r*1.6-7}" y="{-r-7}" width="{r*3.2+14}" height="{r*2+14}" rx="{r+7}" fill="none" stroke="#e0892b" stroke-width="4" stroke-dasharray="7 6"/>'
            f'<rect x="{-r*1.6}" y="{-r}" width="{r*3.2}" height="{r*2}" rx="{r}" fill="#d9654f" stroke="#b8433f" stroke-width="3"/>'
            f'<circle cx="{-r*.6}" cy="{-r*.2}" r="{r*.22}" fill="#fff" opacity=".5"/></g>')
def dead(x, y, r, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})" opacity=".55"><rect x="{-r*1.6}" y="{-r}" width="{r*3.2}" height="{r*2}" rx="{r}" fill="#d7dfe0" stroke="#aab7ba" stroke-width="3" stroke-dasharray="6 5"/>'
            f'<path d="M{-r*.5},{-r*.4} l{r*.8},{r*.8} M{r*.3},{-r*.4} l{-r*.8},{r*.8}" stroke="#8a989b" stroke-width="3"/></g>')
def virus(x, y, r, fill="#8a7cc4"):
    spikes = "".join(f'<g transform="rotate({a})"><line x1="0" y1="{-r}" x2="0" y2="{-r*1.45}" stroke="{fill}" stroke-width="4"/><circle cx="0" cy="{-r*1.5}" r="{r*.14}" fill="{fill}"/></g>' for a in range(0, 360, 30))
    return f'<g transform="translate({x},{y})">{spikes}<circle r="{r}" fill="{fill}" opacity=".9"/><circle cx="{-r*.3}" cy="{-r*.3}" r="{r*.22}" fill="#fff" opacity=".4"/></g>'
def capsule(x, y, s=1, rot=-30, a="#17656a", b="#f2b33d"):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M-60,-24 h60 v48 h-60 a24,24 0 0 1 0,-48z" fill="{a}"/>'
            f'<path d="M0,-24 h60 a24,24 0 0 1 0,48 h-60z" fill="{b}"/><rect x="-70" y="-14" width="40" height="8" rx="4" fill="#fff" opacity=".35"/></g>')
def check(x, y, s=1, c="#1f7a57"):
    return f'<g transform="translate({x},{y}) scale({s})"><circle r="22" fill="{c}"/><path d="M-10,0 l7,8 l13,-15" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
def cross(x, y, s=1, c="#b8433f"):
    return f'<g transform="translate({x},{y}) scale({s})"><circle r="22" fill="{c}"/><path d="M-9,-9 l18,18 M9,-9 l-18,18" stroke="#fff" stroke-width="5" stroke-linecap="round"/></g>'

def page(lang, body, w=1600, h=900):
    cls = "bn" if lang == "bn" else "en"
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body class="{cls}">{body}</body></html>'

def foot(lang, src):
    by = "সায়েদুল আবরার, ফার্মাসিস্ট · sayedulabrar.site" if lang == "bn" else "Sayedul Abrar, Pharmacist · sayedulabrar.site"
    lab = "সূত্র: " if lang == "bn" else "Sources: "
    return f'<div class="foot"><span>{lab}{src}</span><span class="brand">{by}</span></div>'

T = {}  # key -> {lang: html}

# 1 ---------------- cover ----------------
def cover(lang, w=1600, h=900):
    if lang == "bn":
        k, t, s, by = "সহজ ভাষায় স্বাস্থ্য", "অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি?", "অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে শুরু হয়, সহজ ভাষায়", "লিখেছেন সায়েদুল আবরার, ফার্মাসিস্ট"
        days = ["দিন ১", "২", "৩", "৪", "৫", "৬", "৭"]
    else:
        k, t, s, by = "Health Made Simple", "Why You Must Complete an Antibiotic Course", "…and how antibiotic resistance starts", "By Sayedul Abrar, Pharmacist"
        days = ["Day 1", "2", "3", "4", "5", "6", "7"]
    sc = w / 1600
    cells = ""
    for i, d in enumerate(days):
        x = 40 + i * 92
        done = i < 7
        cells += (f'<g transform="translate({x},0)"><rect width="80" height="96" rx="16" fill="#fff" stroke="#cfe3df" stroke-width="3"/>'
                  f'<text x="40" y="30" text-anchor="middle" font-size="{17 if lang=="en" else 19}" font-weight="600" fill="#4c6670" font-family="Poppins,HS">{d}</text>'
                  f'{check(40, 64, .8) if done else ""}</g>')
    svg = f'''<svg width="{760}" height="{620}" viewBox="0 0 760 620" style="position:absolute;right:{40*sc}px;top:{(h-620*sc)/2}px;transform:scale({sc});transform-origin:top right">
      <circle cx="400" cy="300" r="270" fill="#e3f2ef"/><circle cx="560" cy="160" r="90" fill="#fff1dc"/>
      {bac(230,160,30,rot=-20)}{bac(600,420,26,rot=25)}{rbac(590,160,28,rot=10)}{dead(180,410,26,rot=15)}
      {capsule(330,320,1.6,-28)}{capsule(560,300,1.0,35,"#c4573a","#f6efe6")}
      <g transform="translate(-14,500)">{cells}</g></svg>'''
    title_w = 820 * sc
    body = f'''<div class="frame" style="padding:{70*sc}px {80*sc}px"><div style="width:{title_w}px;margin-top:{60*sc}px">
      <p class="kick" style="font-size:{22*sc}px">{k}</p>
      <h1 style="font-size:{(74 if lang=='en' else 72)*sc}px;line-height:{1.12 if lang=='en' else 1.3};margin-top:{14*sc}px">{t}</h1>
      <p class="sub" style="font-size:{30*sc}px;margin-top:{18*sc}px">{s}</p>
      <p style="margin-top:{40*sc}px;display:inline-block;background:#17656a;color:#fff;font-weight:600;font-size:{24*sc}px;padding:{12*sc}px {26*sc}px;border-radius:999px">{by}</p></div></div>{svg}'''
    return page(lang, body, w, h)

# 2 ---------------- resistance ----------------
def resistance(lang):
    if lang == "bn":
        k, t = "সরল চিত্র", "অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে তৈরি হয়"
        steps = [("সংক্রমণে অনেক ব্যাকটেরিয়া থাকে", "এদের মধ্যে কয়েকটি স্বাভাবিকভাবেই ওষুধে কম সংবেদনশীল হতে পারে।"),
                 ("অ্যান্টিবায়োটিক সংবেদনশীলগুলোকে মারে", "ভুলভাবে বা অপ্রয়োজনে ব্যবহার করলে প্রতিরোধী ব্যাকটেরিয়া টিকে যাওয়ার সুযোগ পায়।"),
                 ("টিকে থাকা ব্যাকটেরিয়া বাড়ে ও ছড়ায়", "পরের সংক্রমণে একই অ্যান্টিবায়োটিক আর কাজ নাও করতে পারে।")]
        note = "রেজিস্ট্যান্স হয় ব্যাকটেরিয়ার, আপনার শরীরের নয়।"
        leg = ["সংবেদনশীল", "প্রতিরোধী", "মারা গেছে"]
    else:
        k, t = "Simplified illustration", "How antibiotic resistance develops"
        steps = [("An infection has many bacteria", "A few may naturally be less sensitive to the medicine."),
                 ("The antibiotic kills the sensitive ones", "Misuse and overuse give resistant bacteria more chances to survive."),
                 ("Survivors multiply and can spread", "Next time, the same antibiotic may not work.")]
        note = "Resistance happens to the bacteria, not to your body."
        leg = ["Sensitive", "Resistant", "Killed"]
    pics = [
        bac(70,70,20,rot=10)+bac(190,60,20,rot=-15)+bac(120,150,20,rot=30)+rbac(250,150,20)+bac(60,230,20,rot=-5)+bac(200,240,20,rot=20),
        dead(70,70,20,rot=10)+dead(190,60,20,rot=-15)+dead(120,150,20,rot=30)+rbac(250,150,20)+dead(60,230,20,rot=-5)+dead(200,240,20,rot=20)+capsule(150,250,.7,-20),
        rbac(70,70,20,rot=10)+rbac(200,60,20,rot=-15)+rbac(120,150,20,rot=30)+rbac(250,170,20)+rbac(60,240,20,rot=-5)+rbac(200,250,20,rot=20)]
    cards = ""
    for i, ((a, b), pic) in enumerate(zip(steps, pics)):
        arrow = '' if i == 2 else '<svg width="44" height="44" style="position:absolute;right:-38px;top:150px"><path d="M6 22 H34 M24 10 L36 22 L24 34" stroke="#2f8f83" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
        cards += f'''<div class="card" style="flex:1;padding:26px 28px;position:relative"><div class="row" style="gap:14px;align-items:center"><div class="num">{i+1 if lang=="en" else "১২৩"[i]}</div><p class="t" style="font-size:{25 if lang=="en" else 29}px">{a}</p></div>
        <svg width="320" height="300" viewBox="0 0 320 300" style="display:block;margin:10px auto 4px">{pic}</svg><p class="p" style="font-size:{20 if lang=="en" else 23}px">{b}</p>{arrow}</div>'''
    legend = (f'<div class="row" style="gap:30px;align-items:center;font-size:20px;color:#4c6670">'
              f'<svg width="60" height="40">{bac(30,20,10)}</svg>{leg[0]}<svg width="60" height="40">{rbac(30,20,10)}</svg>{leg[1]}<svg width="60" height="40">{dead(30,20,10)}</svg>{leg[2]}</div>')
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1><div class="row" style="gap:44px;margin-top:22px">{cards}</div>
      <div class="row" style="justify-content:space-between;align-items:center;margin-top:18px"><p style="font-size:24px;font-weight:700;color:#b8433f">{note}</p>{legend}</div>
      {foot(lang, "WHO; MedlinePlus")}</div>'''
    return page(lang, body)

# 3 ---------------- viruses ----------------
def viruses(lang):
    if lang == "bn":
        k, t = "মৌলিক ধারণা", "অ্যান্টিবায়োটিক ব্যাকটেরিয়ার জন্য, ভাইরাসের জন্য নয়"
        L = ("ব্যাকটেরিয়াজনিত সংক্রমণ", "ডাক্তার প্রয়োজন মনে করলে অ্যান্টিবায়োটিক দেন।", "সব ব্যাকটেরিয়াজনিত সংক্রমণে অ্যান্টিবায়োটিক লাগে না।")
        R = ("ভাইরাসজনিত অসুখ", "যেমন সাধারণ সর্দি-কাশি ও ফ্লু।", "অ্যান্টিবায়োটিক ভাইরাসে কাজ করে না, তাই এতে আপনি ভালো বোধ করবেন না।")
        q = "জ্বর বা কাশি মানেই অ্যান্টিবায়োটিক নয়। ডাক্তারই ঠিক করবেন।"
    else:
        k, t = "The basics", "Antibiotics treat bacteria, not viruses"
        L = ("Bacterial infections", "A doctor prescribes an antibiotic when one is needed.", "Not every bacterial infection needs an antibiotic.")
        R = ("Viral illnesses", "Such as common colds and flu.", "Antibiotics do not work on viruses and will not make you feel better.")
        q = "A fever or cough does not automatically mean you need an antibiotic. Let a doctor decide."
    def side(data, pic, good):
        icon = check(0, 0, 1.4) if good else cross(0, 0, 1.4)
        return f'''<div class="card" style="flex:1;padding:32px 36px;display:flex;gap:30px;align-items:center"><svg width="300" height="300" viewBox="0 0 300 300" style="flex:none">{pic}<g transform="translate(250,250)">{icon}</g></svg>
          <div><p class="t" style="font-size:{32 if lang=="en" else 36}px">{data[0]}</p><p class="p" style="margin-top:12px">{data[1]}</p><p class="p" style="margin-top:12px;font-weight:600;color:{"#1f7a57" if good else "#b8433f"}">{data[2]}</p></div></div>'''
    pb = bac(110,90,30,rot=-10)+bac(190,170,30,rot=20)+bac(90,200,30,rot=5)+capsule(200,70,.8,-25)
    pv = virus(100,100,40)+virus(200,190,34,"#a593d6")+virus(90,220,26)
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1><div class="row" style="gap:36px;margin-top:34px">{side(L,pb,True)}{side(R,pv,False)}</div>
      <p style="margin-top:34px;font-size:{27 if lang=="en" else 30}px;font-weight:600;background:#fff5df;border:1px solid #f0d99e;border-radius:18px;padding:20px 28px">{q}</p>
      {foot(lang, "CDC")}</div>'''
    return page(lang, body)

# 4 ---------------- do's and don'ts ----------------
def dosdonts(lang):
    if lang == "bn":
        k, t = "করণীয় ও বর্জনীয়", "অ্যান্টিবায়োটিক খাওয়ার সঠিক নিয়ম"
        H = ("যা করবেন", "যা করবেন না")
        D = ["প্রেসক্রিপশনে যেভাবে লেখা, ঠিক সেভাবে খান", "ভালো লাগলেও পুরো কোর্স শেষ করুন, যদি না ডাক্তার অন্য কথা বলেন", "প্রতিটি ডোজ নির্দিষ্ট সময়ে খান", "পার্শ্বপ্রতিক্রিয়া হলে ডাক্তার বা ফার্মাসিস্টকে জানান"]
        N = ["নিজে নিজে মাঝপথে বন্ধ করবেন না", "বাকি ওষুধ পরের অসুখের জন্য রেখে দেবেন না", "অন্যকে দেবেন না, অন্যের ওষুধ খাবেন না", "প্রেসক্রিপশন ছাড়া কিনবেন না"]
    else:
        k, t = "Do's and don'ts", "How to take antibiotics the right way"
        H = ("Do", "Don't")
        D = ["Take them exactly as prescribed", "Finish the course, even if you feel better, unless your doctor says otherwise", "Take each dose at the right time", "Tell your doctor or pharmacist about side effects"]
        N = ["Stop early on your own", "Save leftovers for a future illness", "Share them, or take someone else's", "Buy them without a prescription"]
    def col(head, items, good):
        c = "#1f7a57" if good else "#b8433f"; bg = "#ecf7f2" if good else "#fbeeec"
        li = "".join(f'<div class="row" style="gap:18px;align-items:center;margin-top:34px"><svg width="48" height="48" style="flex:none"><g transform="translate(24,24)">{check(0,0) if good else cross(0,0)}</g></svg><p class="p" style="font-size:{29 if lang=="en" else 32}px;color:#173d43">{x}</p></div>' for x in items)
        return f'<div class="card" style="flex:1;padding:30px 36px;background:{bg};border-color:{bg}"><p class="t" style="color:{c};font-size:{36 if lang=="en" else 40}px">{head}</p>{li}</div>'
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1><div class="row" style="gap:36px;margin-top:30px;flex:1;margin-bottom:22px">{col(H[0],D,True)}{col(H[1],N,False)}</div>
      {foot(lang, "CDC; NHS; MedlinePlus")}</div>'''
    return page(lang, body)

# 5 ---------------- missed dose ----------------
def missed(lang):
    if lang == "bn":
        k, t = "ডোজ বাদ পড়লে", "একটি ডোজ মিস হলে কী করবেন?"
        a = ("মনে পড়ার সঙ্গে সঙ্গে খেয়ে নিন", "তারপর আগের মতো নিয়ম মেনে চলুন।")
        b = ("পরের ডোজের সময় প্রায় হয়ে গেছে?", "তাহলে বাদ পড়া ডোজটি বাদ দিন, পরেরটি নিয়মমতো খান।")
        c = "বাদ পড়া ডোজ পূরণে কখনও একসাথে দুটি ডোজ খাবেন না।"
        d = "নিশ্চিত না হলে ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন। আপনার ওষুধের লিফলেটে আলাদা নির্দেশনা থাকতে পারে।"
        q = "ডোজ মিস হয়েছে?"
    else:
        k, t = "Missed dose", "Missed a dose of your antibiotic?"
        a = ("Take it as soon as you remember", "Then carry on with your usual schedule.")
        b = ("Is the next dose almost due?", "Skip the missed dose and take the next one at the usual time.")
        c = "Never take a double dose to make up for a missed one."
        d = "Not sure? Ask your doctor or pharmacist. Your own leaflet may give specific advice."
        q = "Missed a dose?"
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1>
      <div class="row" style="gap:34px;margin-top:34px;align-items:stretch">
        <div class="card" style="width:330px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#17656a;border:none;color:#fff;padding:26px">
          <svg width="160" height="160" viewBox="0 0 160 160"><circle cx="80" cy="80" r="66" fill="none" stroke="#fff" stroke-width="8"/><path d="M80 40 V82 L108 98" stroke="#f2b33d" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
          <p style="font-size:{32 if lang=="en" else 36}px;font-weight:700;margin-top:14px;text-align:center">{q}</p></div>
        <div style="flex:1;display:flex;flex-direction:column;gap:24px">
          <div class="card row" style="padding:38px 34px;align-items:center;gap:24px"><svg width="56" height="56"><g transform="translate(28,28)">{check(0,0,1.2)}</g></svg><div><p class="t">{a[0]}</p><p class="p">{a[1]}</p></div></div>
          <div class="card row" style="padding:38px 34px;align-items:center;gap:24px"><svg width="56" height="56"><g transform="translate(28,28)"><circle r="26" fill="#e0892b"/><text y="11" text-anchor="middle" font-size="32" font-weight="700" fill="#fff" font-family="Poppins">?</text></g></svg><div><p class="t">{b[0]}</p><p class="p">{b[1]}</p></div></div>
          <div class="card row" style="padding:38px 34px;align-items:center;gap:24px;background:#fbeeec;border-color:#f3d2cd"><svg width="56" height="56"><g transform="translate(28,28)">{cross(0,0,1.2)}</g></svg><p class="t" style="color:#8f2f2b">{c}</p></div>
        </div></div>
      <p class="p" style="margin-top:24px;font-weight:600">{d}</p>
      {foot(lang, "NHS রোগী-তথ্য লিফলেট; MedlinePlus" if lang=="bn" else "NHS patient leaflet; MedlinePlus")}</div>'''
    return page(lang, body)

# 6 ---------------- red label ----------------
def redlabel(lang):
    if lang == "bn":
        k, t = "বাংলাদেশ", "অ্যান্টিবায়োটিকের প্যাকে লাল চিহ্ন"
        lab, warn = "অ্যান্টিবায়োটিক", "রেজিস্টার্ড চিকিৎসকের প্রেসক্রিপশন ছাড়া ব্যবহার করবেন না"
        pts = [("কী?", "ডিসেম্বর ২০২২ থেকে মানুষ ও প্রাণীর অ্যান্টিবায়োটিকের প্যাকে লাল চিহ্ন দেওয়ার সিদ্ধান্ত (DGDA)।"),
               ("কী লেখা থাকে?", "“Antibiotic” লেখা লাল লেবেল এবং প্রেসক্রিপশন ছাড়া ব্যবহার না করার সতর্কবার্তা।"),
               ("আপনার করণীয়", "লাল চিহ্ন দেখলে বুঝবেন এটি অ্যান্টিবায়োটিক। শুধু রেজিস্টার্ড চিকিৎসকের প্রেসক্রিপশনে খান।")]
        ill = "উদাহরণমূলক চিত্র, কোনো আসল পণ্য নয়"
    else:
        k, t = "Bangladesh", "The red mark on antibiotic packs"
        lab, warn = "ANTIBIOTIC", "Do not use without a prescription of registered physician"
        pts = [("What is it?", "A DGDA decision to put a red identification mark on human and veterinary antibiotic packs, from December 2022."),
               ("What does it say?", "A red label reading “antibiotic” and a warning not to use it without a registered physician’s prescription."),
               ("What should you do?", "If you see the red mark, it is an antibiotic. Take it only with a registered doctor’s prescription.")]
        ill = "Illustration only, not a real product"
    box = f'''<svg width="470" height="470" viewBox="0 0 560 560" style="flex:none">
      <ellipse cx="280" cy="500" rx="210" ry="26" fill="#173d43" opacity=".08"/>
      <path d="M120 140 L360 100 L460 160 L460 440 L220 480 L120 420 Z" fill="#fff" stroke="#cfdcdc" stroke-width="3"/>
      <path d="M360 100 L460 160 L220 200 L120 140 Z" fill="#f1f6f5" stroke="#cfdcdc" stroke-width="3"/>
      <path d="M220 200 L460 160 L460 440 L220 480 Z" fill="#fbfdfd" stroke="#cfdcdc" stroke-width="3"/>
      <path d="M220 330 L460 290 L460 360 L220 400 Z" fill="#c62f2a"/>
      <text transform="translate(240,382) skewY(-9.5)" font-size="{30 if lang=="en" else 32}" font-weight="700" fill="#fff" font-family="Poppins,HS">{lab}</text>
      <rect x="236" y="230" width="150" height="16" rx="8" fill="#dbe6e6" transform="skewY(-9.5) translate(0,40)"/>
      <rect x="236" y="262" width="100" height="14" rx="7" fill="#e7eeee" transform="skewY(-9.5) translate(0,40)"/>
      <path d="M120 140 L220 200 L220 480 L120 420 Z" fill="#eef4f3" stroke="#cfdcdc" stroke-width="3"/>
      <path d="M120 340 L220 400 L220 330 L120 270 Z" fill="#a82621"/>
    </svg>'''
    items = "".join(f'<div class="card" style="padding:22px 28px"><p class="t" style="color:#b8433f">{a}</p><p class="p" style="margin-top:6px">{b}</p></div>' for a, b in pts)
    body = f'''<div class="frame"><p class="kick" style="color:#b8433f">{k}</p><h1>{t}</h1>
      <div class="row" style="gap:30px;margin-top:12px;align-items:center"><div style="text-align:center">{box}<p style="font-size:18px;color:#6b7f86;margin-top:-22px">{ill}</p>
        <p style="margin:12px auto 0;max-width:520px;font-size:{21 if lang=="en" else 23}px;font-weight:600;color:#a82621;border:2px solid #e8b3ae;background:#fdf1ef;border-radius:14px;padding:10px 16px">“{warn}”</p></div>
        <div style="flex:1;display:flex;flex-direction:column;gap:20px">{items}</div></div>
      {foot(lang, "WHO বাংলাদেশ (DGDA, ড্রাগ কন্ট্রোল কমিটি)" if lang=="bn" else "WHO Bangladesh (DGDA, Drug Control Committee)")}</div>'''
    return page(lang, body)

# 7 ---------------- side effects ----------------
def sideeffects(lang):
    if lang == "bn":
        k, t = "পার্শ্বপ্রতিক্রিয়া", "কখন সাহায্য নেবেন"
        cols = [("সাধারণ", "#2f8f83", "#ecf7f2", ["বমি বমি ভাব বা বমি", "পেট ফাঁপা বা বদহজম", "পাতলা পায়খানা"], "সাধারণত হালকা হয়। চিন্তা হলে ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
                ("ডাক্তারকে জানান", "#d08a1f", "#fff5e3", ["তীব্র বা পানির মতো পাতলা পায়খানা", "তীব্র বা দুশ্চিন্তার পার্শ্বপ্রতিক্রিয়া", "ভুল করে বাড়তি ডোজ খেয়ে ফেললে"], "নিজে নিজে ওষুধ বন্ধ বা বদলাবেন না।"),
                ("জরুরি", "#b8433f", "#fbeeec", ["মুখ, ঠোঁট বা জিহ্বা ফুলে যাওয়া", "শ্বাস নিতে কষ্ট", "এগুলো গুরুতর অ্যালার্জির লক্ষণ হতে পারে"], "সঙ্গে সঙ্গে জরুরি চিকিৎসা নিন।")]
    else:
        k, t = "Side effects", "When to get help"
        cols = [("Common", "#2f8f83", "#ecf7f2", ["Feeling sick or being sick", "Bloating or indigestion", "Diarrhoea"], "Usually mild. Ask a pharmacist if you are worried."),
                ("Tell your doctor", "#d08a1f", "#fff5e3", ["Severe or watery diarrhoea", "Side effects that are severe or worrying", "You took extra doses by mistake"], "Do not stop or change the medicine on your own."),
                ("Emergency", "#b8433f", "#fbeeec", ["Swelling of the face, lips or tongue", "Difficulty breathing", "These can be signs of a serious allergic reaction"], "Get emergency medical help immediately.")]
    out = ""
    for h, c, bg, items, note in cols:
        li = "".join(f'<li style="margin:22px 0 22px 30px;font-size:{27 if lang=="en" else 30}px" class="p">{x}</li>' for x in items)
        out += f'<div class="card" style="flex:1;padding:28px 30px;background:{bg};border-color:{bg};border-top:10px solid {c};display:flex;flex-direction:column"><p class="t" style="color:{c};font-size:{32 if lang=="en" else 36}px">{h}</p><ul style="margin-top:10px;color:#173d43">{li}</ul><p class="p" style="margin-top:auto;font-weight:600;color:{c}">{note}</p></div>'
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1><div class="row" style="gap:28px;margin-top:28px;flex:1;margin-bottom:22px">{out}</div>
      {foot(lang, "NHS রোগী-তথ্য লিফলেট (Royal Berkshire, জুন ২০২৫); পূর্ণ তালিকা নয়" if lang=="bn" else "NHS patient leaflet (Royal Berkshire, June 2025); not a complete list")}</div>'''
    return page(lang, body)

# 8 ---------------- key takeaways ----------------
def takeaways(lang):
    if lang == "bn":
        k, t = "মনে রাখার কথা", "অ্যান্টিবায়োটিক: ৫টি মূল কথা"
        P = [("পুরো কোর্স শেষ করুন", "ভালো লাগলেও, যদি না ডাক্তার অন্য কথা বলেন।"), ("শুধু প্রেসক্রিপশনে", "লাল চিহ্ন দেখলেই বুঝবেন এটি অ্যান্টিবায়োটিক।"),
             ("ভাইরাসে কাজ করে না", "সর্দি-কাশি ও ফ্লুতে অ্যান্টিবায়োটিক কাজ করে না।"), ("রেখে দেবেন না, ভাগ করবেন না", "বাকি ওষুধ ফেলার নিয়ম ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
             ("ডোজ মিস হলে দ্বিগুণ নয়", "সময়মতো খান, সমস্যা হলে ডাক্তারকে জানান।")]
        s = "সঠিক ব্যবহারই অ্যান্টিবায়োটিককে ভবিষ্যতের জন্য কার্যকর রাখে।"
    else:
        k, t = "Key takeaways", "Antibiotics: 5 things to remember"
        P = [("Finish the course", "Even if you feel better, unless your doctor says otherwise."), ("Only with a prescription", "In Bangladesh, the red mark tells you it is an antibiotic."),
             ("Not for viruses", "Antibiotics do not work on colds and flu."), ("Don't save or share", "Ask a pharmacist how to get rid of leftovers."),
             ("Never double a missed dose", "Take doses on time and report side effects.")]
        s = "Using antibiotics correctly keeps them working for everyone."
    cards = "".join(f'<div class="card row" style="padding:34px 30px;gap:22px;align-items:center"><div class="num">{i+1 if lang=="en" else "১২৩৪৫"[i]}</div><div><p class="t">{a}</p><p class="p">{b}</p></div></div>' for i, (a, b) in enumerate(P))
    cards += f'<div class="card row" style="padding:22px 26px;gap:20px;align-items:center;background:#17656a;border:none;padding:34px 30px"><svg width="120" height="80" viewBox="0 0 120 80" style="flex:none">{capsule(60,40,.75,-20,"#f2b33d","#ffffff")}</svg><p class="t" style="color:#fff">{s}</p></div>'
    body = f'''<div class="frame"><p class="kick">{k}</p><h1>{t}</h1><div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:26px;margin-bottom:22px">{cards}</div>
      {foot(lang, "NHS; CDC; MedlinePlus; WHO Bangladesh")}</div>'''
    return page(lang, body)

NAMES = {
 "cover": "why-complete-antibiotic-course-cover-16x9",
 "resistance": "how-antibiotic-resistance-develops-simplified",
 "viruses": "antibiotics-treat-bacteria-not-viruses-cold-flu",
 "dosdonts": "antibiotic-dos-and-donts-take-as-prescribed",
 "missed": "missed-antibiotic-dose-what-to-do",
 "redlabel": "bangladesh-red-mark-on-antibiotic-packs-dgda",
 "sideeffects": "antibiotic-side-effects-when-to-get-help",
 "takeaways": "antibiotics-key-takeaways",
}
FN = {"cover": cover, "resistance": resistance, "viruses": viruses, "dosdonts": dosdonts, "missed": missed, "redlabel": redlabel, "sideeffects": sideeffects, "takeaways": takeaways}

with sync_playwright() as p:
    b = p.chromium.launch()
    def shot(htm, w, h, path, fmt="webp"):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        f = HERE / "_tmp.html"; f.write_text(htm, encoding="utf-8")
        pg.goto(f.as_uri()); pg.wait_for_timeout(400)
        over = pg.evaluate("()=>{const f=document.querySelector('.frame');return f? f.scrollHeight>f.clientHeight+2 : false}")
        if over: print("OVERFLOW", path.name)
        png = pg.screenshot(); pg.close()
        im = Image.open(io.BytesIO(png)).convert("RGB")
        if fmt == "webp": im.save(path, "WEBP", quality=88, method=6)
        else: im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(path.name, im.size, path.stat().st_size)
    only = sys.argv[2:] or list(FN)
    for key in only:
        for lang in ("en", "bn"):
            suffix = "" if lang == "en" else "-bn"
            shot(FN[key](lang), 1600, 900, OUT / f"{NAMES[key]}{suffix}.webp")
    if "cover" in only:
        shot(cover("en", 1200, 630), 1200, 630, OUT / "social-en.jpg", "jpeg")
        shot(cover("bn", 1200, 630), 1200, 630, OUT / "social-bn.jpg", "jpeg")
    b.close()
