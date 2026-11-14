#!/usr/bin/env python3
"""Cinematic EN + BN graphics for the How to Read a Prescription article.
Photo backgrounds (no text) are reused from earlier articles' AI images; the "parts", "pattern" and "food"
graphics are drawn in code. All words are set in code so spelling is exact.
Usage: python3 make_rx.py OUTDIR [keys...]"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2:])
U = H.as_uri()
CSS = f"""
@font-face{{font-family:Anton;src:url({U}/anton-latin-400-normal.woff2)}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-800-normal.woff2);font-weight:800;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;position:relative;font-family:Poppins,HS,sans-serif;color:#0f3c42;background:#f7f2ec}}
body.bn{{font-family:HS,Poppins,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:right center}}
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(250,246,240,.97) 0%,rgba(250,246,240,.93) var(--a,44%),rgba(250,246,240,0) var(--b,60%))}}
.vig{{position:absolute;inset:0;box-shadow:inset 0 0 160px rgba(15,60,66,.16)}}
.panel{{position:absolute;left:64px;top:0;bottom:58px;width:var(--pw,820px);display:flex;flex-direction:column;justify-content:center;padding:26px 0}}
.kick{{display:flex;align-items:center;gap:12px;font-size:20px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#17807a}}
.kick:before{{content:"";width:46px;height:4px;border-radius:2px;background:linear-gradient(90deg,#17807a,#e0892b)}}
body.bn .kick{{letter-spacing:.02em;font-size:24px;font-family:Anek,HS;font-weight:700}}
.title{{font-family:Anton,Impact,sans-serif;text-transform:uppercase;font-size:var(--ts,72px);line-height:.98;margin-top:12px;color:#0f3c42}}
body.bn .title{{font-family:Anek,HS;font-weight:800;text-transform:none;line-height:1.15}}
.title em{{font-style:normal;background:linear-gradient(90deg,#0d9488,#14b8a6);-webkit-background-clip:text;background-clip:text;color:transparent}}
.title i{{font-style:normal;background:linear-gradient(90deg,#e0562b,#f59e0b);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{font-size:30px;line-height:1.38;color:#2a4a51;margin-top:14px;font-weight:500}}
body.bn .sub{{font-size:32px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:24px}}
body.bn .grid{{gap:10px;margin-top:16px}} body.bn .chip{{padding:10px 18px}}
.chip{{background:rgba(255,255,255,.94);border-radius:18px;padding:14px 18px;box-shadow:0 10px 26px rgba(15,60,66,.12);border-top:6px solid var(--c,#17807a)}}
.chip b{{display:block;font-family:Anton,sans-serif;font-weight:400;font-size:34px;line-height:1.05;color:var(--c,#17807a);letter-spacing:.02em}}
.chip span{{display:block;font-size:23px;line-height:1.3;color:#173d43;margin-top:4px;font-weight:600}}
body.bn .chip span{{font-size:25px;font-family:Anek,HS;font-weight:700}}
.chip small{{display:block;font-size:19px;line-height:1.3;color:#3b5960;margin-top:2px}}
body.bn .chip small{{font-size:21px}}
.rows{{display:flex;flex-direction:column;gap:12px;margin-top:22px}}
.row{{display:flex;gap:16px;align-items:center;background:rgba(255,255,255,.95);border-radius:18px;padding:13px 20px;box-shadow:0 10px 26px rgba(15,60,66,.1);border-left:8px solid var(--c,#17807a)}}
.code{{flex:none;min-width:118px;font-family:Anton,sans-serif;font-size:36px;color:var(--c,#17807a);letter-spacing:.02em}}
body.bn .code{{font-family:Anek,Anton,sans-serif;font-weight:800}}
body.bn .tagc{{font-family:Anek,Anton,sans-serif;font-weight:800}}
.row b{{display:block;font-size:26px;line-height:1.22;color:#0f3c42}}
body.bn .row b{{font-family:Anek,HS;font-weight:700;font-size:28px}}
.row span{{display:block;font-size:21px;line-height:1.32;color:#3b5960}}
body.bn .row span{{font-size:23px}}
.badge{{flex:none;width:46px;height:46px;border-radius:50%;background:#0f3c42;color:#fff;font-family:Anton,Anek,sans-serif;font-size:25px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(255,255,255,.85)}}
body.bn .badge{{font-family:Anek;font-weight:800}}
.note{{margin-top:16px;font-size:24px;font-weight:700;line-height:1.35;border-radius:16px;padding:13px 20px;background:#fff5df;border:1px solid #f0d99e;color:#6b4300}}
body.bn .note{{font-family:Anek,HS;font-size:26px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:56px;display:flex;justify-content:space-between;align-items:center;padding:0 64px;font-size:19px;color:#3b5960;background:linear-gradient(90deg,rgba(250,246,240,.96),rgba(250,246,240,.8))}}
body.bn .foot{{font-size:21px}}
.foot b{{color:#0f3c42;font-weight:700}}
.ill{{position:absolute;right:22px;bottom:68px;font-size:16px;color:#3b5960;background:rgba(255,255,255,.85);padding:4px 12px;border-radius:999px}}
body.bn .ill{{font-size:18px}}
.mk{{position:absolute;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:50%;background:#0f3c42;color:#fff;font-family:Anton,Anek,sans-serif;font-size:25px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px rgba(255,255,255,.9),0 0 0 11px rgba(23,128,122,.35),0 10px 24px rgba(0,0,0,.25)}}
body.bn .mk{{font-family:Anek;font-weight:800}}
.tagc{{position:absolute;background:rgba(255,255,255,.94);border-radius:14px;padding:8px 16px;box-shadow:0 12px 28px rgba(15,60,66,.22);border-left:6px solid var(--c,#17807a);font-family:Anton,sans-serif;font-size:30px;color:var(--c,#17807a)}}
"""
BN_DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
def page(lang, inner, src, bg=None, a="44%", b="60%", pw="820px", ts="72px", ill="", extra=""):
    bn = lang == "bn"
    bgh = (f'<div class="bg" style="background-image:url({U}/bg/{bg}.webp)"></div><div class="veil" style="--a:{a};--b:{b}"></div><div class="vig"></div>') if bg else ""
    name = "সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "Sayedul Abrar, Pharmacist"
    srcl = ("সূত্র: " if bn else "Sources: ") + src
    il = f'<div class="ill">{ill}</div>' if ill else ""
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{lang}">{bgh}{extra}'
            f'<div class="panel" style="--pw:{pw};--ts:{ts}">{inner}</div>{il}<div class="foot"><span>{srcl}</span><b>{name} · sayedulabrar.site</b></div></body></html>')
def head(k, t, s=""):
    return f'<p class="kick">{k}</p><h1 class="title">{t}</h1>' + (f'<p class="sub">{s}</p>' if s else "")
def chips(items, cols=2):
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr)">' + "".join(
        f'<div class="chip" style="--c:{c}"><b>{a}</b><span>{b}</span>' + (f'<small>{d}</small>' if d else "") + '</div>' for c, a, b, d in items) + "</div>"
def rows(items, codew="118px"):
    return '<div class="rows">' + "".join(
        f'<div class="row" style="--c:{c}"><div class="code" style="min-width:{codew}">{a}</div><div><b>{b}</b>' + (f'<span>{d}</span>' if d else "") + '</div></div>' for c, a, b, d in items) + "</div>"
T, O, R, P, G = "#17807a", "#d0661f", "#b8433f", "#6f4bb0", "#1f7a57"
P_ = {}

# ---------------------------------------------------------------- cover
def cover(lang):
    bn = lang == "bn"
    t = ('<em>প্রেসক্রিপশন</em> পড়ার <i>সহজ নিয়ম</i>' if bn else 'How to <em>Read</em> a <i>Prescription</i>')
    s = ('BD, TDS, OD, ১+০+১ আর অন্যান্য সংক্ষেপের মানে' if bn else 'BD, TDS, OD, 1+0+1 and other abbreviations, explained')
    by = 'লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট' if bn else 'By Sayedul Abrar, Pharmacist'
    inner = head("সহজ ভাষায় স্বাস্থ্য" if bn else "Health Made Simple", t, s) + \
        f'<p style="display:inline-block;align-self:flex-start;margin-top:34px;background:#17656a;color:#fff;font-weight:600;font-size:27px;padding:12px 28px;border-radius:999px;{"font-family:Anek,HS;font-weight:700" if bn else ""}">{by}</p>'
    tags = "".join(f'<div class="tagc" style="left:{x}px;top:{y}px;--c:{c}">{w}</div>' for x, y, c, w in
                   [(1010, 150, T, "BD"), (1300, 120, O, "TDS"), (1180, 300, P, "1+0+1" if not bn else "১+০+১"), (1420, 260, G, "AC · PC")])
    return page(lang, inner, "WHO Guide to Good Prescribing; ISMP", bg="cover", a="40%", b="58%", pw="760px", ts="104px" if not bn else "92px",
                extra=tags, ill="প্রতীকী ছবি" if bn else "Illustrative photo")
P_["cover"] = cover

# ---------------------------------------------------------------- parts (drawn prescription sheet)
def parts(lang):
    bn = lang == "bn"
    legend = [("ডাক্তারের নাম, ডিগ্রি ও রেজি. নম্বর", "যিনি লিখেছেন, তাঁকে চেনার উপায়"),
              ("রোগীর নাম, বয়স ও তারিখ", "প্রেসক্রিপশনটি আপনার কি না, মিলিয়ে নিন"),
              ("Rx চিহ্ন", "এখান থেকে ওষুধের তালিকা শুরু"),
              ("ওষুধের নাম, ধরন ও শক্তি", "যেমন Tab. … 20 mg; প্যাকের সঙ্গে মেলান"),
              ("কতটা ও কতবার", "১+০+১, BD, TDS ইত্যাদি"),
              ("খাবারের আগে না পরে", "AC / PC বা বাংলায় লেখা"),
              ("কতদিন", "যেমন ৭ দিন, ১ মাস, বা চলবে"),
              ("স্বাক্ষর ও পরামর্শ", "পরের ভিজিট, পরীক্ষা, সতর্কতা")] if bn else [
              ("Doctor’s name, degrees, reg. no.", "Who wrote it and how to reach them"),
              ("Patient’s name, age and date", "Check the prescription is yours"),
              ("Rx symbol", "The medicine list starts here"),
              ("Medicine name, form, strength", "e.g. Tab. … 20 mg; match it to the pack"),
              ("How much and how often", "1+0+1, BD, TDS and so on"),
              ("Before or after food", "AC / PC, or written in words"),
              ("For how long", "e.g. 7 days, 1 month, or “continue”"),
              ("Signature and advice", "Follow-up, tests, warnings")]
    lg = '<div style="display:flex;flex-direction:column;gap:9px;margin-top:20px">' + "".join(
        f'<div style="display:flex;gap:14px;align-items:center"><div class="badge">{str(i+1).translate(BN_DIG) if bn else i+1}</div><div><b style="display:block;font-size:{"26" if bn else "24"}px;line-height:1.15;{"font-family:Anek,HS;font-weight:700" if bn else ""}">{a}</b><span style="display:block;font-size:{"21" if bn else "19"}px;color:#3b5960;line-height:1.25">{b}</span></div></div>'
        for i, (a, b) in enumerate(legend)) + "</div>"
    inner = head("প্রেসক্রিপশনের অংশ" if bn else "Parts of a prescription", ('প্রেসক্রিপশনের <em>৮টি</em> <i>অংশ</i>' if bn else 'The <em>8 parts</em> of a <i>prescription</i>'), "") + lg
    # sheet (English handwriting-style text is kept in English on both, as on real pads)
    hw = "font-family:'Segoe Script','Comic Sans MS',Poppins,cursive;"
    sheet = f'''<div style="position:absolute;left:880px;top:46px;width:640px;height:780px;background:#fffdf8;border-radius:10px;box-shadow:0 30px 60px rgba(15,60,66,.25);transform:rotate(1.2deg);overflow:hidden">
<div style="height:120px;background:linear-gradient(90deg,#e6f3f1,#fdf3e7);padding:20px 30px;border-bottom:3px solid #17807a">
 <p style="font-size:28px;font-weight:700;color:#0f3c42">Dr. A. Rahman</p><p style="font-size:19px;color:#36555c">MBBS, FCPS (Medicine) · BMDC Reg. No. A-00000</p><p style="font-size:17px;color:#36555c">Chamber: 12 Sample Road, Dhaka · 01X-XXXXXXXX</p></div>
<div style="display:flex;gap:26px;padding:14px 30px;font-size:19px;color:#36555c;border-bottom:1px dashed #b9cfcc"><span>Name: <b style="{hw}color:#1d3f8a">Karim Uddin</b></span><span>Age: <b style="{hw}color:#1d3f8a">38 y</b></span><span>Date: <b style="{hw}color:#1d3f8a">14/11/26</b></span></div>
<div style="padding:16px 30px 0 30px"><p style="font-family:Georgia,serif;font-size:62px;font-weight:700;color:#0f3c42;line-height:1">℞</p>
<div style="{hw}color:#1d3f8a;font-size:26px;line-height:1.5;margin-top:6px">
<p>1. Tab. Medicine A 20 mg</p><p style="padding-left:40px">1+0+1 — before food — 14 days</p>
<p style="margin-top:54px">2. Syp. Medicine B</p><p style="padding-left:40px">2 tsf (10 mL) TDS — after food — 5 days</p>
<p style="margin-top:12px">3. Tab. Medicine C 10 mg</p><p style="padding-left:40px">0+0+1 — continue</p></div>
<p style="font-size:18px;color:#36555c;margin-top:16px">Advice: Follow up after 2 weeks.</p></div>
<div style="position:absolute;right:40px;bottom:46px;text-align:center"><p style="{hw}font-size:30px;color:#1d3f8a">A. Rahman</p><p style="font-size:15px;color:#36555c;border-top:1px solid #9bb;padding-top:2px">Signature</p></div>
<div style="position:absolute;left:30px;bottom:22px;font-size:15px;color:#8a9a9d">Sample only · fictional doctor, patient and medicines</div></div>'''
    mks = "".join(f'<div class="mk" style="left:{x}px;top:{y}px">{str(n).translate(BN_DIG) if bn else n}</div>' for n, x, y in
                  [(1, 868, 104), (2, 866, 196), (3, 880, 268), (4, 866, 330), (5, 900, 372), (6, 1150, 412), (7, 1322, 412), (8, 1500, 742)])
    return page(lang, inner, "WHO Guide to Good Prescribing (1994)", pw="760px", ts="62px", extra=sheet + mks)
P_["parts"] = parts

# ---------------------------------------------------------------- frequency
def frequency(lang):
    bn = lang == "bn"
    it = [(T, "OD", "দিনে ১ বার", "লিখুন: daily / once a day"), (T, "BD", "দিনে ২ বার", "bis die"),
          (O, "TDS", "দিনে ৩ বার", "ter die sumendum"), (O, "QDS · QID", "দিনে ৪ বার", "quater die"),
          (P, "MANE", "সকালে", "mane"), (P, "HS · NOCTE", "রাতে, ঘুমানোর আগে", "hora somni / nocte"),
          (G, "PRN · SOS", "শুধু দরকার হলে", "কতবার পর্যন্ত, জেনে নিন"), (R, "STAT", "এখনই, সঙ্গে সঙ্গে", "statim")] if bn else [
         (T, "OD", "Once a day", "Safer to write: daily"), (T, "BD", "Twice a day", "bis die"),
         (O, "TDS", "Three times a day", "ter die sumendum"), (O, "QDS · QID", "Four times a day", "quater die"),
         (P, "MANE", "In the morning", "mane"), (P, "HS · NOCTE", "At night / bedtime", "hora somni / nocte"),
         (G, "PRN · SOS", "Only when needed", "Ask the maximum per day"), (R, "STAT", "Straight away", "statim")]
    inner = head("কতবার খাবেন" if bn else "How often", ('<em>OD, BD, TDS</em> <i>মানে কী?</i>' if bn else 'How <em>often?</em> <i>OD, BD, TDS</i>')) + chips(it) + \
        f'<p class="note">{"ডোজগুলোর মাঝে কত ঘণ্টা ফাঁকা রাখবেন, তা গুরুত্বপূর্ণ হলে ফার্মাসিস্টকে জিজ্ঞেস করুন।" if bn else "If the gap between doses matters, ask your pharmacist how many hours apart."}</p>'
    return page(lang, inner, "ISMP; Dept of Health, Western Australia; ACSQHC", bg="frequency", a="46%", b="62%", pw="800px", ts="60px" if bn else "70px",
                ill="প্রতীকী ছবি" if bn else "Illustrative photo")
P_["frequency"] = frequency

# ---------------------------------------------------------------- 1+0+1 pattern (drawn)
def pattern(lang):
    bn = lang == "bn"
    d = (lambda s: s.translate(BN_DIG)) if bn else (lambda s: s)
    ex = [(T, d("1+0+1"), "সকালে ১টি, রাতে ১টি", "দিনে ২ বার (BD-এর মতো)"), (O, d("1+1+1"), "সকাল, দুপুর, রাতে ১টি করে", "দিনে ৩ বার (TDS-এর মতো)"),
          (P, d("0+0+1"), "শুধু রাতে ১টি", "দিনে ১ বার, রাতে"), (G, "½+0+½", "সকালে আধা, রাতে আধা", "ট্যাবলেট ভাঙা যাবে কি না, জেনে নিন")] if bn else [
         (T, "1+0+1", "1 in the morning, 1 at night", "Twice a day (like BD)"), (O, "1+1+1", "1 morning, 1 midday, 1 night", "Three times a day (like TDS)"),
         (P, "0+0+1", "1 at night only", "Once a day, at night"), (G, "½+0+½", "Half in the morning, half at night", "Ask if the tablet can be split")]
    inner = head("বাংলাদেশে প্রচলিত লেখা" if bn else "Common in Bangladesh", ('<i>১+০+১</i> <em>মানে কী?</em>' if bn else 'What does <i>1+0+1</i> <em>mean?</em>')) + rows(ex, "150px") + \
        f'<p class="note">{"সংখ্যাগুলো ট্যাবলেট বা ডোজের সংখ্যা, ঘণ্টা নয়। শক্তি (mg) প্যাকে মিলিয়ে নিন।" if bn else "The numbers are tablets or doses, not hours. Check the strength (mg) on the pack."}</p>'
    lab = ["সকাল", "দুপুর", "রাত"] if bn else ["Morning", "Midday", "Night"]
    nums = ["১", "০", "১"] if bn else ["1", "0", "1"]
    ic = ['<circle cx="60" cy="60" r="26" fill="#f6a623"/>' + "".join(f'<line x1="60" y1="60" x2="{60+44*c}" y2="{60+44*s}" stroke="#f6a623" stroke-width="5" stroke-linecap="round" stroke-dasharray="0 30 14"/>' for c, s in [(1,0),(-1,0),(0,1),(0,-1),(.7,.7),(-.7,.7),(.7,-.7),(-.7,-.7)]),
          '<circle cx="60" cy="60" r="32" fill="#f59e0b"/><circle cx="60" cy="60" r="44" fill="none" stroke="#fcd38a" stroke-width="6"/>',
          '<path d="M74 22a40 40 0 1 0 22 62 32 32 0 1 1-22-62z" fill="#4b5fa8"/><circle cx="34" cy="30" r="3" fill="#4b5fa8"/><circle cx="100" cy="40" r="2.5" fill="#4b5fa8"/>']
    pill = '<svg width="74" height="40"><rect x="2" y="6" width="70" height="28" rx="14" fill="#fff" stroke="#17807a" stroke-width="3"/><line x1="37" y1="6" x2="37" y2="34" stroke="#17807a" stroke-width="2"/></svg>'
    cols = [f'''<div style="width:200px;background:{bgc};border-radius:26px;padding:22px 0 26px;text-align:center;box-shadow:0 20px 40px rgba(15,60,66,.18)">
<svg width="120" height="120" style="display:block;margin:0 auto">{ic[i]}</svg>
<p style="font-family:{'Anek' if bn else 'Anton'},sans-serif;font-weight:800;font-size:{'36' if bn else '30'}px;color:{fg};{'text-transform:uppercase;letter-spacing:.06em' if not bn else ''}">{lab[i]}</p>
<p style="font-family:{'Anek' if bn else 'Anton'},sans-serif;font-weight:800;font-size:130px;line-height:1.05;color:{fg}">{nums[i]}</p>
<div style="height:44px">{pill if nums[i] in ('1','১') else ''}</div></div>''' for i, (bgc, fg) in enumerate([("#fff6e2", "#a35a00"), ("#fffaf0", "#b3b3b3"), ("#e9edfb", "#2f3f88")])]
    plus = '<p style="font-family:Anton,sans-serif;font-size:80px;color:#9bb0b3;align-self:center">+</p>'
    art = '<div style="position:absolute;left:870px;top:120px;display:flex;gap:10px">' + plus.join(cols) + '</div>'
    cap = ("উদাহরণ: ১+০+১ = সকালে ১টি, দুপুরে নয়, রাতে ১টি" if bn else "Example: 1+0+1 = 1 in the morning, none at midday, 1 at night")
    art += f'<p style="position:absolute;left:880px;top:640px;width:680px;text-align:center;font-size:{"28" if bn else "25"}px;font-weight:700;color:#0f3c42;{"font-family:Anek,HS" if bn else ""}">{cap}</p>'
    return page(lang, inner, "Pharmacist explainer; ask your doctor or pharmacist if unsure", pw="770px", ts="78px", extra=art)
P_["pattern"] = pattern

# ---------------------------------------------------------------- food (drawn)
def food(lang):
    bn = lang == "bn"
    it = [(T, "AC", "খাবারের আগে", "কতক্ষণ আগে, তা ওষুধভেদে আলাদা; জেনে নিন"), (O, "PC", "খাবারের পরে বা সঙ্গে", "পেটে সহ্য করতে সাহায্য করতে পারে"),
          (P, "খালি পেটে", "সাধারণত খাবারের ১ ঘণ্টা আগে বা ২ ঘণ্টা পরে", "লিফলেট বা ফার্মাসিস্টের নির্দেশ দেখুন"), (G, "HS", "রাতে ঘুমানোর আগে", "hora somni")] if bn else [
         (T, "AC", "Before food", "How long before depends on the medicine; ask"), (O, "PC", "After or with food", "Can help some medicines sit better"),
         (P, "EMPTY", "Empty stomach", "Often 1 hour before or 2 hours after food"), (G, "HS", "At bedtime", "hora somni")]
    inner = head("খাবার ও ওষুধ" if bn else "Food and timing", ('খাবারের <em>আগে</em> না <i>পরে?</i>' if bn else '<em>Before</em> or <i>after</i> food?')) + rows(it, "130px") + \
        f'<p class="note">{"উদাহরণ: অনেক PPI (যেমন ওমিপ্রাজল) সাধারণত খাবারের আগে খেতে বলা হয়।" if bn else "Example: many PPIs (such as omeprazole) are usually taken before a meal."}</p>'
    lab = ("আগে", "পরে") if bn else ("BEFORE", "AFTER")
    art = f'''<svg style="position:absolute;left:900px;top:110px" width="640" height="600" viewBox="0 0 640 600">
<defs><radialGradient id="pl" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e7ecea"/></radialGradient></defs>
<ellipse cx="320" cy="330" rx="230" ry="200" fill="rgba(15,60,66,.10)"/>
<circle cx="320" cy="300" r="210" fill="url(#pl)" stroke="#d6dfdd" stroke-width="4"/><circle cx="320" cy="300" r="160" fill="none" stroke="#e3e9e7" stroke-width="3"/>
<g fill="#fffdf5" stroke="#efe6cf" stroke-width="2">{"".join(f'<ellipse cx="{260+(i*37)%120}" cy="{250+(i*23)%90}" rx="13" ry="7" transform="rotate({(i*47)%180} {260+(i*37)%120} {250+(i*23)%90})"/>' for i in range(34))}</g>
<circle cx="400" cy="350" r="62" fill="#f2b84b" stroke="#d99a2b" stroke-width="4"/><circle cx="400" cy="350" r="48" fill="#f7c968"/>
<rect x="40" y="70" width="110" height="46" rx="23" fill="#17807a"/><text x="95" y="102" text-anchor="middle" font-family="{'Anek' if bn else 'Anton'}" font-weight="800" font-size="{'26' if bn else '24'}" fill="#fff">{lab[0]}</text>
<path d="M150 100 Q 220 90 250 150" stroke="#17807a" stroke-width="5" fill="none" stroke-dasharray="4 10" stroke-linecap="round"/>
<rect x="490" y="500" width="110" height="46" rx="23" fill="#d0661f"/><text x="545" y="532" text-anchor="middle" font-family="{'Anek' if bn else 'Anton'}" font-weight="800" font-size="{'26' if bn else '24'}" fill="#fff">{lab[1]}</text>
<path d="M490 520 Q 440 510 420 450" stroke="#d0661f" stroke-width="5" fill="none" stroke-dasharray="4 10" stroke-linecap="round"/>
<g transform="translate(60 150) rotate(-20)"><rect width="84" height="36" rx="18" fill="#fff" stroke="#17807a" stroke-width="4"/><rect width="42" height="36" rx="18" fill="#17807a"/></g>
<g transform="translate(520 430) rotate(15)"><rect width="84" height="36" rx="18" fill="#fff" stroke="#d0661f" stroke-width="4"/><rect width="42" height="36" rx="18" fill="#d0661f"/></g>
</svg>'''
    return page(lang, inner, "NHS medicine leaflets; ask your pharmacist", pw="800px", ts="74px", extra=art,
                ill="উদাহরণমূলক চিত্র" if bn else "Illustration")
P_["food"] = food

# ---------------------------------------------------------------- forms & routes
def forms(lang):
    bn = lang == "bn"
    it = [(T, "TAB · CAP", "ট্যাবলেট · ক্যাপসুল", ""), (O, "SYP · SUSP", "সিরাপ · সাসপেনশন", "সাসপেনশন খাওয়ার আগে ঝাঁকিয়ে নিন"),
          (P, "INJ", "ইনজেকশন", "IM = মাংসপেশিতে, IV = শিরায়"), (G, "INH · DROPS", "ইনহেলার · ড্রপ", "চোখ, কান বা নাকের ড্রপ"),
          (R, "PO", "মুখে খাওয়ার জন্য", "per os"), (T, "TSF", "১ চা-চামচ = ৫ mL", "রান্নাঘরের চামচ নয়, মাপার কাপ বা সিরিঞ্জ")] if bn else [
         (T, "TAB · CAP", "Tablet · Capsule", ""), (O, "SYP · SUSP", "Syrup · Suspension", "Shake a suspension before use"),
         (P, "INJ", "Injection", "IM = into muscle, IV = into a vein"), (G, "INH · DROPS", "Inhaler · Drops", "Eye, ear or nose drops"),
         (R, "PO", "By mouth", "per os"), (T, "TSF", "1 teaspoonful = 5 mL", "Use the cup or syringe, not a kitchen spoon")]
    inner = head("ধরন ও প্রয়োগের পথ" if bn else "Forms and routes", ('<em>Tab, Syp, Inj</em> <i>মানে কী?</i>' if bn else '<em>Tab, Syp, Inj:</em> <i>forms</i> and routes')) + chips(it)
    return page(lang, inner, "ISMP; FDA (mL dosing); ACSQHC", bg="forms", a="47%", b="60%", pw="790px", ts="66px",
                ill="প্রতীকী ছবি" if bn else "Illustrative photo")
P_["forms"] = forms

# ---------------------------------------------------------------- error-prone abbreviations
def mistakes(lang):
    bn = lang == "bn"
    it = [(R, "OD", "দিনে একবার, নাকি ডান চোখ?", "OD = oculus dexter (ডান চোখ) হিসেবেও পড়া হয়"), (R, "QD", "দিনে ১ বার, পড়া হয় QID (৪ বার)", "নিরাপদ লেখা: daily"),
          (R, "U", "ইউনিট, পড়া হয় ০ বা ৪", "নিরাপদ লেখা: units"), (O, "1.0 mg", "পড়া হতে পারে 10 mg", "নিরাপদ লেখা: 1 mg"),
          (O, ".5 mg", "পড়া হতে পারে 5 mg", "নিরাপদ লেখা: 0.5 mg")] if bn else [
         (R, "OD", "Once daily, or right eye?", "OD also means oculus dexter (right eye)"), (R, "QD", "Daily, misread as QID (4 times)", "Safer: daily"),
         (R, "U", "Units, misread as 0 or 4", "Safer: units"), (O, "1.0 mg", "Can be misread as 10 mg", "Safer: 1 mg"),
         (O, ".5 mg", "Can be misread as 5 mg", "Safer: 0.5 mg")]
    inner = head("সাবধান" if bn else "Watch out", ('যে সংক্ষেপে <i>ভুল</i> <em>হয়</em>' if bn else 'Abbreviations that <i>cause</i> <em>mistakes</em>')) + rows(it, "140px") + \
        f'<p class="note">{"কিছু অস্পষ্ট লাগলে অনুমান করবেন না। ফার্মাসিস্টকে পড়ে দিতে বলুন, দরকারে ডাক্তারকে ফোন করুন।" if bn else "If anything is unclear, don’t guess. Ask the pharmacist to read it with you, and check with the doctor."}</p>'
    return page(lang, inner, "ISMP List of Error-Prone Abbreviations", bg="mistakes", a="50%", b="64%", pw="840px", ts="64px",
                ill="প্রতীকী ছবি" if bn else "Illustrative photo")
P_["mistakes"] = mistakes

# ---------------------------------------------------------------- takeaways
def takeaways(lang):
    bn = lang == "bn"
    it = [("নাম, তারিখ ও ডাক্তারের তথ্য মিলিয়ে নিন", "প্রেসক্রিপশনটি আপনার কি না, নিশ্চিত হোন"),
          ("ওষুধের নাম ও শক্তি প্যাকের সঙ্গে মেলান", "জেনেরিক নাম ও mg দেখুন"),
          ("কতটা, কতবার, কতদিন", "১+০+১, BD, ৭ দিন ইত্যাদি পড়ে নিন"),
          ("খাবারের আগে না পরে", "AC / PC খেয়াল করুন"),
          ("অনুমান করবেন না", "ফার্মাসিস্ট বা ডাক্তারকে জিজ্ঞেস করুন")] if bn else [
          ("Check your name, date and the doctor’s details", "Make sure the prescription is yours"),
          ("Match the medicine name and strength", "Check the generic name and mg on the pack"),
          ("Read how much, how often, how long", "1+0+1, BD, 7 days and so on"),
          ("Check before or after food", "Look for AC / PC"),
          ("Never guess", "Ask your pharmacist or doctor")]
    lst = '<div class="rows" style="gap:10px">' + "".join(
        f'<div class="row" style="padding:11px 18px"><div class="badge">{str(i+1).translate(BN_DIG) if bn else i+1}</div><div><b>{a}</b><span>{b}</span></div></div>' for i, (a, b) in enumerate(it)) + "</div>"
    inner = head("মনে রাখুন" if bn else "Key takeaways", ('প্রেসক্রিপশন পড়ার <em>৫টি</em> <i>ধাপ</i>' if bn else '<em>5 steps</em> to read <i>any prescription</i>')) + lst
    return page(lang, inner, "WHO Guide to Good Prescribing; ISMP", bg="takeaways", a="48%", b="62%", pw="820px", ts="66px",
                ill="প্রতীকী ছবি" if bn else "Illustrative photo")
P_["takeaways"] = takeaways

NAMES = {"cover": "how-to-read-a-prescription-cover", "parts": "parts-of-a-prescription-labelled", "frequency": "prescription-frequency-abbreviations-od-bd-tds",
         "pattern": "what-does-1-0-1-mean-on-a-prescription", "food": "before-or-after-food-ac-pc-meaning", "forms": "medicine-forms-and-routes-tab-syp-inj",
         "mistakes": "error-prone-prescription-abbreviations", "takeaways": "how-to-read-a-prescription-key-takeaways"}
with sync_playwright() as p:
    br = p.chromium.launch()
    for k, fn in P_.items():
        if ONLY and k not in ONLY: continue
        for lang in ("en", "bn"):
            pg = br.new_page(viewport={"width": 1600, "height": 900})
            f = H / f"_{lang}.html"; f.write_text(fn(lang), encoding="utf-8"); pg.goto(f.as_uri()); pg.wait_for_timeout(600)
            over = pg.evaluate("()=>{const c=document.querySelector('.panel');return c.scrollHeight>c.clientHeight+2}")
            im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close(); f.unlink()
            out = OUT / f"{NAMES[k]}{'-bn' if lang == 'bn' else ''}.webp"; im.save(out, "WEBP", quality=86, method=6)
            print(("OVERFLOW " if over else "") + out.name, out.stat().st_size)
            if k == "cover":
                im.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652)).save(OUT / f"social-{lang}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    br.close()
