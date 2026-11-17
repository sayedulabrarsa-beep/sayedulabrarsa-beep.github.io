#!/usr/bin/env python3
"""Cinematic EN + BN graphics for the Expiry Date vs Manufacturing Date article, built on the user's AI images (no text in source images).
Usage: python3 make_cine.py OUTDIR [keys...]"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
SC = 1600 / 1672  # source images are ~1672x941
CSS = f"""
@font-face{{font-family:Pop;src:url({U}/poppins-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Pop;src:url({U}/poppins-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:Int;src:url({U}/inter-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:Int;src:url({U}/inter-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:Int;src:url({U}/inter-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-500-normal.woff2);font-weight:500;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-latin-700-normal.woff2);font-weight:700}}
:root{{--teal:#174F52;--char:#253238;--coral:#E98250;--cream:#F7F1E6;--sage:#DCEBE7;--gold:#D8A84E;--steel:#526D82}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);overflow:hidden;position:relative;font-family:Int,HS,sans-serif;color:var(--char);background:var(--cream)}}
body.bn{{font-family:HS,Int,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(247,241,230,.97) 0%,rgba(247,241,230,.9) var(--a,30%),rgba(247,241,230,0) var(--b,44%))}}
.vig{{display:none}}
.panel{{position:absolute;left:96px;top:0;bottom:var(--fb,58px);width:var(--pw,560px);display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:30px 0}}
.chips{{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}}
.chip{{background:var(--sage);border-radius:14px;padding:14px 16px;border-left:7px solid var(--c,var(--coral))}}
.chip b{{display:block;font-family:Pop;font-weight:800;font-size:21px;line-height:1.15;color:var(--char)}}
body.bn .chip b{{font-family:HS;font-weight:700;font-size:27px;line-height:1.25}}
.chip span{{display:block;font-size:18px;line-height:1.35;color:var(--char);margin-top:6px}}
body.bn .chip span{{font-size:23px;font-weight:500}}
.kick{{display:flex;align-items:center;gap:12px;font-family:Int;font-size:20px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--char)}}
.kick:before{{content:"";width:14px;height:14px;border-radius:50%;background:var(--coral)}}
body.bn .kick{{letter-spacing:.02em;font-size:24px;font-family:HS;font-weight:700}}
.title{{font-family:Pop,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.12;letter-spacing:-.01em;margin-top:16px;color:var(--teal)}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.2;letter-spacing:0}}
.title em{{font-style:normal;color:var(--teal)}}
.title i{{font-style:normal;color:#fff;background:var(--coral);padding:0 .14em;border-radius:.14em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.sub{{font-size:29px;line-height:1.42;color:var(--char);margin-top:18px;font-weight:500}}
body.bn .sub{{font-size:31px;line-height:1.5}}
.legend{{margin-top:26px;display:flex;flex-direction:column;gap:14px;width:100%}}
.li{{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.92);border-radius:14px;padding:12px 16px;border-left:5px solid var(--teal)}}
.badge{{flex:none;width:42px;height:42px;border-radius:50%;background:var(--coral);color:#fff;font-family:Pop,HS;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700;font-size:24px}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:24px;line-height:1.2;color:var(--char)}}
.li span{{display:block;font-size:20px;line-height:1.35;color:var(--char)}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:28px}}
body.bn .li span{{font-size:23px;font-weight:500}}
.li span.tag{{display:inline-block;color:#fff;margin-top:5px;font-size:15px;font-weight:600;padding:2px 10px;border-radius:999px}}
.call{{position:absolute;background:var(--teal);border-radius:14px;padding:11px 16px;box-shadow:0 10px 26px rgba(37,50,56,.22);border-left:6px solid var(--c,var(--teal));max-width:300px}}
.call b{{display:block;font-family:Pop;font-weight:800;font-size:21px;color:#fff;line-height:1.15}}
body.bn .call b{{font-family:HS;font-weight:700;font-size:25px;line-height:1.25}}
.call span{{display:block;font-size:18px;line-height:1.35;color:#DCEBE7;margin-top:3px}}
body.bn .call span{{font-size:20px;font-weight:500}}
.mk{{position:absolute;width:50px;height:50px;margin:-25px 0 0 -25px;border-radius:50%;background:var(--teal);color:#fff;font-family:Pop,HS;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff,0 0 0 10px var(--mkc,rgba(233,130,80,.55)),0 10px 24px rgba(0,0,0,.3)}}
body.bn .mk{{font-family:HS;font-weight:700}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:54px;display:flex;justify-content:space-between;align-items:center;padding:0 96px;font-size:17px;color:var(--steel);background:rgba(247,241,230,.94)}}
body.bn .foot{{font-size:19px}}
.foot b{{color:var(--teal);font-weight:600}}
.stamp{{position:absolute;font-family:Int;font-weight:600;color:#2a3236;letter-spacing:.05em;line-height:1.28;white-space:nowrap;text-align:left}}
.ill{{position:absolute;right:24px;bottom:66px;font-size:14px;color:var(--char);background:rgba(255,255,255,.85);padding:3px 12px;border-radius:999px}}
body.bn .ill{{font-size:16px}}
.panel{{left:72px!important}}
.kick{{font-size:26px!important}} body.bn .kick{{font-size:30px!important}}
.sub{{font-size:36px!important;line-height:1.3!important;margin-top:16px!important}} body.bn .sub{{font-size:38px!important;line-height:1.4!important}}
.chips{{gap:14px!important;margin-top:24px!important}}
.chip{{padding:14px 16px!important}}
.chip b{{font-size:30px!important;line-height:1.1!important}} body.bn .chip b{{font-size:32px!important}}
.chip span{{font-size:23px!important;line-height:1.25!important;margin-top:4px!important}} body.bn .chip span{{font-size:26px!important}}
.call{{max-width:420px!important;padding:12px 20px!important;border-left-width:8px!important}}
.call b{{font-size:31px!important}} body.bn .call b{{font-size:34px!important}}
.call span{{font-size:24px!important;line-height:1.25!important}} body.bn .call span{{font-size:27px!important}}
.legend{{gap:12px!important;margin-top:22px!important}}
.li{{padding:12px 18px!important;gap:16px!important;align-items:center!important}}
.badge{{width:54px!important;height:54px!important;font-size:28px!important}}
.li b{{font-size:31px!important}} body.bn .li b{{font-size:33px!important}}
.li span{{font-size:24px!important;line-height:1.25!important}} body.bn .li span{{font-size:27px!important}}
.foot{{height:58px!important;font-size:21px!important;padding:0 72px!important}} body.bn .foot{{font-size:22px!important}}
.ill{{font-size:17px!important;bottom:70px!important}}"""
DX = [0]
P = lambda x, y: (x * SC + DX[0], y * SC)
def ring(x, y, r=34, c="#17807a"):
    x, y = P(x, y)
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#fff" stroke-width="4"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r+7}" fill="none" stroke="{c}" stroke-width="3" opacity=".75"/><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#fff"/>'
def leader(tx, ty, lx, ly, c="#ffffff"):
    a, b = P(tx, ty); c2, d = P(lx, ly)
    return f'<path d="M{a:.0f},{b:.0f} L{c2:.0f},{d:.0f}" stroke="{c}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" fill="none" style="filter:drop-shadow(0 1px 2px rgba(0,0,0,.45))"/>'

def build(cfg, lang, w=1600, h=900):
    bn = lang == "bn"; g = lambda k: cfg[k][1 if bn else 0]; DX[0] = cfg.get("dx", 0)
    svg = ""; html = ""
    for st in cfg.get("stamps", []):
        x, y, ang, en, bnl, fs, css = st
        X, Y = P(x, y)
        html += f'<div class="stamp" style="left:{X:.0f}px;top:{Y:.0f}px;transform:translate(-50%,-50%) rotate({ang}deg);font-size:{fs}px;{css}">{bnl if bn else en}</div>'
    for c in cfg.get("calls", []):
        tx, ty, lx, ly, anchor, col, en, bnx = c
        t, s = bnx if bn else en
        svg += leader(tx, ty, lx, ly) + ring(tx, ty, c=col)
        x, y = P(lx, ly)
        if anchor == "r": x = min(x, w - 24)
        pos = {"l": f"left:{x:.0f}px", "r": f"right:{w-x:.0f}px", "c": f"left:{x-150:.0f}px"}[anchor]
        html += f'<div class="call" style="{pos};top:{y-30:.0f}px;--c:{col}"><b>{t}</b>{f"<span>{s}</span>" if s else ""}</div>'
    for (x, y, n) in cfg.get("marks", []):
        X, Y = P(x, y); html += f'<div class="mk" style="left:{X:.0f}px;top:{Y:.0f}px">{"১২৩৪৫৬"[n-1] if bn else n}</div>'
    leg = ""
    if "legend" in cfg:
        for i, item in enumerate(cfg["legend"]):
            (a, b, tag) = item[1] if bn else item[0]
            tg = f'<span class="tag" style="background:{tag[1]}">{tag[0]}</span>' if tag else ""
            leg += f'<div class="li"><div class="badge">{"১২৩৪৫৬"[i] if bn else i+1}</div><div><b>{a}</b><span>{b}</span>{tg}</div></div>'
        leg = f'<div class="legend">{leg}</div>'
    sub = g("sub")
    ill = f'<div class="ill">{"AI-তৈরি প্রতীকী ছবি" if bn else "AI-generated illustration"}</div>'
    src = g("src") if "src" in cfg else ""
    foot = (f'<div class="foot"><span>{("সূত্র: " if bn else "Sources: ") + src if src else ""}</span><b>{"সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "Sayedul Abrar, Pharmacist"} · sayedulabrar.site</b></div>') if cfg.get("foot", True) else ""
    ts = cfg.get("ts", (86, 74))[1 if bn else 0]
    chips = ('<div class="chips">' + ''.join(f'<div class="chip" style="--c:{c[2]}"><b>{(c[1] if bn else c[0])[0]}</b><span>{(c[1] if bn else c[0])[1]}</span></div>' for c in cfg['chips']) + '</div>') if cfg.get('chips') else ''
    byline = (f'<p style="margin-top:34px;display:inline-block;background:#174F52;color:#fff;border-left:6px solid #E98250;font-family:Int,HS;font-weight:600;font-size:{27 if w>1300 else 24}px;padding:12px 26px;border-radius:999px;box-shadow:0 10px 24px rgba(15,60,66,.25)">{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>') if cfg.get('byline') else ''
    tight = '<style>.legend{gap:10px!important;margin-top:18px!important}body.bn .legend{gap:7px!important;margin-top:14px!important}.li b{font-size:25px!important}body.bn .li b{font-size:27px!important}.li span{font-size:20px!important}body.bn .li span{font-size:22px!important}.badge{width:38px!important;height:38px!important;font-size:20px!important}</style>' if cfg.get('tight') else ''
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body class="{lang}">{tight}'
            f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div><div class="veil" style="--a:{cfg.get("a","30%")};--b:{cfg.get("b","46%")};{cfg.get("veilcss","")}"></div><div class="vig"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0">{svg}</svg>{html}'
            f'<div class="panel" style="{cfg.get("panelcss","")};--pw:{cfg.get("pw",560)}px;--ts:{ts}px;--fb:{58 if cfg.get("foot", True) else 0}px"><p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}{chips}{leg}{byline}</div>{ill if cfg.get("ill", True) else ""}{foot}</body></html>')

TEAL, CORAL, GOLD, STEEL = "#174F52", "#E98250", "#D8A84E", "#526D82"
SRC = ("US FDA; medicine label and leaflet", "US FDA; ওষুধের লেবেল ও লিফলেট")
SH = lambda px: f"background-size:auto 100%;background-position:calc(100% + {px}px) center;"
VE = lambda a: f"background:linear-gradient(90deg,#F7F1E6 0%,#F7F1E6 {a}%,rgba(247,241,230,.88) {a+7}%,rgba(247,241,230,0) {a+20}%);"
CODES = "MFG 05/2025<br>EXP 04/2027<br>B.No. A123"
EMB = "color:rgba(52,60,64,.88);text-shadow:0 1px 0 rgba(255,255,255,.7),0 -1px 0 rgba(0,0,0,.18)"
CFG = {
 "cover": dict(bg="cover", dx=60, bgcss=SH(60), veilcss=VE(28), pw=470, byline=True, ts=(118, 112), foot=False, ill=False,
   kick=("Medicine safety", "ওষুধের নিরাপত্তা"), title=("MFG vs <i>EXP</i>", "MFG বনাম <i>EXP</i>"),
   sub=("Read any medicine pack in 10 seconds.", "যেকোনো ওষুধের প্যাক পড়ুন ১০ সেকেন্ডে।"),
   stamps=[(1168, 430, -9, CODES, CODES, 30, "")]),
 "mfg": dict(bg="mfg", veilcss=VE(27), pw=500, ts=(84, 80),
   kick=("Manufacturing date", "উৎপাদনের তারিখ"), title=("<i>MFG</i>: when it was made", "<i>MFG</i>: কবে তৈরি"),
   sub=("Printed as MFG, Mfg. Date or Manu. Date. It is not a deadline.", "লেখা থাকে MFG, Mfg. Date বা Manu. Date। এটি শেষ সময় নয়।"),
   stamps=[(1126, 463, -10, "MFG 05/2025 &nbsp; EXP 04/2027", "MFG 05/2025 &nbsp; EXP 04/2027", 44, EMB)],
   calls=[(905, 505, 700, 780, "l", CORAL, ("Made: May 2025", "Shows how old the pack is"), ("তৈরি: মে ২০২৫", "প্যাক কত পুরোনো বোঝায়"))],
   src=SRC),
 "exp": dict(bg="exp", dx=50, bgcss=SH(50), veilcss=VE(25), pw=430, ts=(92, 84),
   kick=("Expiry date", "মেয়াদ শেষের তারিখ"), title=("<i>07/2027</i> = 31 July", "<i>07/2027</i> = ৩১ জুলাই"),
   sub=("Month and year only? Good through the last day of that month.", "শুধু মাস ও বছর? ওই মাসের শেষ দিন পর্যন্ত ব্যবহারযোগ্য।"),
   stamps=[(861, 595, -9, "MFG 08/2025<br>EXP 07/2027", "MFG 08/2025<br>EXP 07/2027", 27, ""),
           (1305, 250, -1, "JULY 2027", "জুলাই ২০২৭", 34, "color:#fff;font-family:Pop,HS;font-weight:800;letter-spacing:.12em")],
   calls=[(1420, 530, 1655, 725, "r", CORAL, ("Last day to use", "31 July 2027"), ("ব্যবহারের শেষ দিন", "৩১ জুলাই ২০২৭"))],
   src=SRC),
 "batch": dict(bg="batch", veilcss=VE(28), pw=520, ts=(86, 82),
   kick=("Batch number", "ব্যাচ নম্বর"), title=("<i>B.No.</i>: which batch?", "<i>B.No.</i>: কোন ব্যাচ?"),
   sub=("Also printed as Batch No. or Lot. It helps trace a recall.", "Batch No. বা Lot নামেও থাকে। রিকল হলে প্যাক খুঁজে পেতে সাহায্য করে।"),
   stamps=[(1092, 528, 1.5, "B.No. A123", "B.No. A123", 38, "font-weight:600")],
   calls=[(1290, 545, 1655, 725, "r", CORAL, ("Report a problem?", "Keep the pack or note B.No., MFG and EXP"), ("সমস্যা জানাবেন?", "প্যাক রাখুন বা B.No., MFG, EXP লিখুন"))],
   src=SRC),
 "opened": dict(bg="opened", dx=90, bgcss=SH(90), veilcss=VE(26), pw=470, ts=(80, 76),
   kick=("After opening", "খোলার পর"), title=("Opened? <i>Sooner</i> date wins", "খোলার পর <i>আগের</i> তারিখই মানুন"),
   sub=("Drops, syrups, mixed liquids and jar creams can have a shorter limit.", "ড্রপ, সিরাপ, মেশানো তরল ও কৌটার ক্রিমে আরও ছোট সীমা থাকতে পারে।"),
   chips=[(("Unopened", "Follow the printed EXP"), ("না খোলা", "ছাপা EXP মানুন"), TEAL), (("Opened", "Follow the use-within limit"), ("খোলার পর", "ব্যবহারসীমা মানুন"), CORAL)],
   calls=[(1130, 330, 1655, 90, "r", CORAL, ("Whichever comes first", "EXP or after-opening limit"), ("যেটি আগে আসে", "EXP বা খোলার পরের সীমা"))],
   src=SRC),
 "expired": dict(bg="expired", veilcss=VE(28), pw=470, ts=(86, 80),
   kick=("After the expiry date", "মেয়াদ শেষের পর"), title=("Expired? <i>Don't use</i>", "মেয়াদ শেষ? <i>ব্যবহার নয়</i>"),
   sub=("Strength and safety are no longer guaranteed. Ask how to dispose of it.", "শক্তি ও নিরাপত্তার নিশ্চয়তা আর নেই। কীভাবে ফেলবেন, জিজ্ঞেস করুন।"),
   stamps=[(1050, 500, -2, "MFG 03/2023<br>EXP 02/2025", "MFG 03/2023<br>EXP 02/2025", 32, "color:rgba(60,55,50,.8)")],
   calls=[(1000, 560, 650, 800, "l", CORAL, ("EXP has passed", "Do not use it"), ("EXP পেরিয়ে গেছে", "ব্যবহার করবেন না")),
          (1450, 420, 1655, 725, "r", TEAL, ("Dispose safely", "Ask your pharmacy"), ("নিরাপদে ফেলুন", "ফার্মেসিতে জিজ্ঞেস করুন"))],
   src=SRC),
 "storage": dict(bg="storage", veilcss=VE(26), pw=450, ts=(84, 80),
   kick=("Storage at home", "ঘরে সংরক্ষণ"), title=("Good <i>spot</i>, bad spot", "সঠিক <i>জায়গা</i>, ভুল জায়গা"),
   sub=("Cool, dry, away from sunlight, in the original pack.", "ঠান্ডা, শুকনো, রোদ থেকে দূরে, আসল প্যাকেটে।"),
   calls=[(830, 515, 640, 110, "l", TEAL, ("Good: cool, dry shelf", "Out of children's reach"), ("সঠিক: ঠান্ডা, শুকনো তাক", "শিশুদের নাগালের বাইরে")),
          (1390, 230, 1655, 470, "r", CORAL, ("Bad: steamy bathroom", "Humidity can spoil it"), ("ভুল: ভেজা বাথরুম", "আর্দ্রতা ক্ষতি করে")),
          (1495, 660, 1060, 800, "l", CORAL, ("Bad: sunny windowsill", "Heat and light"), ("ভুল: রোদের জানালা", "তাপ ও আলো"))],
   src=SRC),
 "damaged": dict(bg="damaged", dx=120, bgcss=SH(120), veilcss=VE(25), pw=430, ts=(84, 76),
   kick=("Safety check", "নিরাপত্তা পরীক্ষা"), title=("<i>Damaged</i>? Ask first", "<i>ক্ষতিগ্রস্ত</i>? আগে জিজ্ঞেস করুন"),
   sub=("Even before EXP, don't use a medicine that looks, smells or feels wrong.", "EXP-এর আগেও চেহারা, গন্ধ বা অনুভূতি অস্বাভাবিক হলে ব্যবহার নয়।"),
   calls=[(600, 680, 520, 370, "l", CORAL, ("Torn foil", "Moisture can get in"), ("ছেঁড়া ফয়েল", "আর্দ্রতা ঢুকতে পারে")),
          (1010, 520, 980, 90, "c", CORAL, ("Cloudy liquid", "Colour or clarity changed"), ("ঘোলা তরল", "রং বা স্বচ্ছতা বদলেছে")),
          (1450, 590, 1600, 720, "r", TEAL, ("Unreadable date", "Never guess. Ask."), ("অস্পষ্ট তারিখ", "আন্দাজ নয়, জিজ্ঞেস করুন"))],
   src=SRC),
 "check": dict(bg="check", dx=80, bgcss=SH(80), veilcss=VE(28), pw=500, ts=(76, 74),
   kick=("Before every dose", "প্রতিবার খাওয়ার আগে"), title=("<i>10-second</i> pack check", "<i>১০ সেকেন্ডে</i> প্যাক যাচাই"), sub=("", ""),
   marks=[(668, 428, 1), (925, 235, 2), (1245, 225, 3), (1490, 430, 4)],
   legend=[(("Find EXP", "Read it in good light.", None), ("EXP খুঁজুন", "ভালো আলোয় পড়ুন।", None)),
           (("Month-year rule", "07/2027 = through 31 July.", None), ("মাস-বছরের নিয়ম", "০৭/২০২৭ = ৩১ জুলাই পর্যন্ত।", None)),
           (("After-opening limit", "Whichever comes first.", None), ("খোলার পরের সীমা", "যেটি আগে আসে।", None)),
           (("Check pack, ask", "Damage or doubt? Ask a pharmacist.", None), ("প্যাক দেখুন, জিজ্ঞেস করুন", "ক্ষতি বা সন্দেহ? ফার্মাসিস্টকে বলুন।", None))],
   src=SRC),
 "takeaways": dict(bg="batch", veilcss=VE(38), pw=660, ts=(78, 76),
   kick=("Key takeaways", "মূল কথা"), title=("Remember <i>5 rules</i>", "মনে রাখুন <i>৫ নিয়ম</i>"), sub=("", ""),
   stamps=[(1092, 528, 1.5, "B.No. A123", "B.No. A123", 38, "font-weight:600")],
   legend=[(("MFG = made", "When the batch was made.", None), ("MFG = তৈরি", "ব্যাচ কবে তৈরি হয়েছে।", None)),
           (("EXP = last trusted date", "Month and year only? Last day of the month.", None), ("EXP = শেষ ভরসার তারিখ", "শুধু মাস-বছর? ওই মাসের শেষ দিন।", None)),
           (("Opened? Sooner limit", "Drops, syrups, jar creams.", None), ("খোলা? আগের সীমা", "ড্রপ, সিরাপ, কৌটার ক্রিম।", None)),
           (("Store it right", "Original pack, cool, dry, away from sun and children.", None), ("সঠিকভাবে রাখুন", "আসল প্যাকে, ঠান্ডা-শুকনো, রোদ ও শিশুর নাগালের বাইরে।", None)),
           (("Never guess", "Unreadable date? Ask a pharmacist.", None), ("আন্দাজ নয়", "তারিখ অস্পষ্ট? ফার্মাসিস্টকে জিজ্ঞেস করুন।", None))],
   src=SRC),
 "codes": dict(bg="cover", dx=60, bgcss=SH(60), veilcss=VE(28), pw=470, ts=(88, 84),
   kick=("Where to look", "কোথায় দেখবেন"), title=("Find the <i>3 codes</i>", "<i>৩টি কোড</i> খুঁজুন"),
   sub=("Strip edge, box end flap or bottle label.", "স্ট্রিপের কিনারা, বাক্সের ভাঁজ বা বোতলের লেবেল।"),
   stamps=[(1168, 430, -9, CODES, CODES, 30, "")],
   legend=[(("MFG", "When it was made", None), ("MFG", "কবে তৈরি", None)), (("EXP", "Last trusted date", None), ("EXP", "শেষ ভরসার তারিখ", None)), (("B.No.", "Which batch", None), ("B.No.", "কোন ব্যাচ", None))],
   calls=[(1318, 500, 1655, 725, "r", CORAL, ("Read in good light", "Can't read it? Ask a pharmacist"), ("ভালো আলোয় পড়ুন", "পড়া না গেলে ফার্মাসিস্টকে জিজ্ঞেস করুন"))],
   src=SRC),
}
NAMES = {"cover": "expiry-cover-read-medicine-pack-10-seconds", "mfg": "expiry-mfg-date-on-blister-strip", "exp": "expiry-exp-month-year-rule-calendar",
         "batch": "expiry-batch-number-on-medicine-box", "opened": "expiry-after-opening-whichever-comes-first", "expired": "expiry-expired-medicine-do-not-use",
         "storage": "expiry-store-medicine-good-vs-bad-spot", "damaged": "expiry-damaged-pack-warning-signs", "check": "expiry-10-second-pack-check",
         "takeaways": "expiry-key-takeaways-5-rules", "codes": "expiry-find-mfg-exp-batch-codes"}
with sync_playwright() as p:
    br = p.chromium.launch()
    def shot(htm, w, h, path, fmt="webp"):
        pg = br.new_page(viewport={"width": w, "height": h}); f = H / "_c.html"; f.write_text(htm, encoding="utf-8")
        pg.goto(f.as_uri()); pg.wait_for_timeout(600)
        over = pg.evaluate("()=>{const p=document.querySelector('.panel');return p.getBoundingClientRect().bottom>document.body.clientHeight-58}")
        im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
        im.save(path, "WEBP", quality=88, method=6) if fmt == "webp" else im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(("OVERFLOW " if over else "") + path.name)
    for key in (sys.argv[2:] or list(CFG)):
        for lang in ("en", "bn"):
            shot(build(CFG[key], lang), 1600, 900, OUT / f"{NAMES[key]}{'-bn' if lang == 'bn' else ''}.webp")
        if key == "cover":
            for lang in ("en", "bn"):
                c = dict(CFG["cover"]); c["ts"] = (100, 96); c["pw"] = 400; c["dx"] = 40; c["bgcss"] = SH(40)
                shot(build(c, lang, 1200, 630), 1200, 630, OUT / f"expiry-social-{lang}.jpg", "jpeg")
    br.close()

# Share images: the cover scaled to 1200x675 and centre-cropped to 1200x630 (stamps stay aligned with the box label).
for lang, suf in (("en", ""), ("bn", "-bn")):
    im = Image.open(OUT / f"expiry-cover-read-medicine-pack-10-seconds{suf}.webp").convert("RGB").resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
    im.save(OUT / f"expiry-social-{lang}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
