#!/usr/bin/env python3
"""Cinematic EN + BN figures for the GMP article, built on the user's AI images (no text in source images).
Palette: Universal Medical Editorial Palette. GMP recipe = teal headline + gold-underline keyword,
steel-blue filled chips, white callouts with steel bar, gold rounded-square badges.
Usage: python3 make_gmp.py OUTDIR [keys...]"""
import pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image

H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
SC = 1600 / 1672

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
.veil{{position:absolute;inset:0}}
.panel{{position:absolute;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:30px 0}}
.panel.ctr{{align-items:center;text-align:center}}

.kick{{display:flex;align-items:center;gap:13px;font-family:Int;font-size:25px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:var(--steel)}}
.kick:before{{content:"";width:16px;height:16px;border-radius:3px;background:var(--gold);transform:rotate(45deg)}}
body.bn .kick{{letter-spacing:.02em;font-size:29px;font-family:HS;font-weight:700}}
.panel.ctr .kick{{justify-content:center}}

.title{{font-family:Pop,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.1;letter-spacing:-.01em;margin-top:14px;color:var(--teal)}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.2;letter-spacing:0}}
.title i{{font-style:normal;color:var(--char);box-shadow:inset 0 -.26em 0 rgba(216,168,78,.85);-webkit-box-decoration-break:clone;box-decoration-break:clone}}

.sub{{font-size:35px;line-height:1.32;color:var(--char);margin-top:16px;font-weight:500}}
body.bn .sub{{font-size:37px;line-height:1.42}}

.chips{{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:24px}}
.chips.one{{grid-template-columns:1fr}}
.chip{{background:var(--steel);border-radius:13px;padding:13px 17px;border-bottom:6px solid var(--gold)}}
.chip b{{display:block;font-family:Pop;font-weight:800;font-size:29px;line-height:1.1;color:#fff}}
body.bn .chip b{{font-family:HS;font-weight:700;font-size:31px;line-height:1.25}}
.chip span{{display:block;font-size:22px;line-height:1.25;color:#E7EDF2;margin-top:5px}}
body.bn .chip span{{font-size:25px;font-weight:500}}

.legend{{margin-top:22px;display:flex;flex-direction:column;gap:12px;width:100%}}
.li{{display:flex;gap:16px;align-items:center;background:rgba(255,255,255,.95);border-radius:13px;padding:12px 18px;border-left:7px solid var(--steel)}}
.badge{{flex:none;width:54px;height:54px;border-radius:14px;background:var(--gold);color:#253238;font-family:Pop,HS;font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:30px;line-height:1.15;color:var(--teal)}}
.li span{{display:block;font-size:23px;line-height:1.25;color:var(--char)}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:32px}}
body.bn .li span{{font-size:26px;font-weight:500}}

.call{{position:absolute;background:rgba(255,255,255,.97);border-radius:13px;padding:12px 20px;box-shadow:0 12px 30px rgba(37,50,56,.3);border-left:8px solid var(--c,var(--steel));max-width:420px}}
.call b{{display:block;font-family:Pop;font-weight:800;font-size:30px;color:var(--teal);line-height:1.12}}
body.bn .call b{{font-family:HS;font-weight:700;font-size:33px;line-height:1.25}}
.call span{{display:block;font-size:23px;line-height:1.25;color:var(--char);margin-top:3px}}
body.bn .call span{{font-size:26px;font-weight:500}}

.mk{{position:absolute;width:52px;height:52px;margin:-26px 0 0 -26px;border-radius:14px;background:var(--steel);color:#fff;font-family:Pop,HS;font-weight:800;font-size:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff,0 0 0 10px rgba(216,168,78,.75),0 10px 24px rgba(0,0,0,.3)}}
body.bn .mk{{font-family:HS;font-weight:700}}

.foot{{position:absolute;left:0;right:0;bottom:0;height:58px;display:flex;justify-content:space-between;align-items:center;padding:0 72px;font-size:21px;color:var(--steel);background:rgba(247,241,230,.94)}}
body.bn .foot{{font-size:22px}}
.foot b{{color:var(--teal);font-weight:600}}
.ill{{position:absolute;right:24px;bottom:70px;font-size:17px;color:var(--char);background:rgba(255,255,255,.85);padding:3px 12px;border-radius:999px}}
body.bn .ill{{font-size:19px}}
"""

DX = [0]
P = lambda x, y: (x * SC + DX[0], y * SC)

def ring(x, y, r=32, c="#526D82"):
    x, y = P(x, y)
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#fff" stroke-width="4"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r+7}" fill="none" stroke="{c}" stroke-width="3" opacity=".8"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#fff"/>')

def leader(tx, ty, lx, ly, c="#ffffff"):
    a, b = P(tx, ty); c2, d = P(lx, ly)
    return (f'<path d="M{a:.0f},{b:.0f} L{c2:.0f},{d:.0f}" stroke="{c}" stroke-width="3" stroke-dasharray="2 7" '
            f'stroke-linecap="round" fill="none" style="filter:drop-shadow(0 1px 2px rgba(0,0,0,.45))"/>')

CR = "247,241,230"
def veil_css(side, a):
    """a = where the clear image starts/ends, in %"""
    if side == "l":
        return f"background:linear-gradient(90deg,rgba({CR},.99) 0%,rgba({CR},.97) {a}%,rgba({CR},.8) {a+8}%,rgba({CR},0) {a+20}%);"
    if side == "r":
        return f"background:linear-gradient(270deg,rgba({CR},.99) 0%,rgba({CR},.97) {a-6}%,rgba({CR},.8) {a+3}%,rgba({CR},0) {a+16}%);"
    if side == "top":
        return f"background:linear-gradient(180deg,rgba({CR},.99) 0%,rgba({CR},.97) {a}%,rgba({CR},.75) {a+6}%,rgba({CR},0) {a+13}%);"
    if side == "bot":
        return f"background:linear-gradient(0deg,rgba({CR},.99) 0%,rgba({CR},.97) {a}%,rgba({CR},.75) {a+6}%,rgba({CR},0) {a+14}%);"
    if side == "ctr":
        return (f"background:linear-gradient(90deg,rgba({CR},0) {a-14}%,rgba({CR},.8) {a-5}%,rgba({CR},.98) {a}%,"
                f"rgba({CR},.98) {100-a}%,rgba({CR},.8) {100-a+5}%,rgba({CR},0) {100-a+14}%);")
    return ""

def panel_css(side, pw, w, h, foot):
    fb = 58 if foot else 0
    if side == "l":   return f"left:72px;top:0;bottom:{fb}px;width:{pw}px"
    if side == "r":   return f"right:72px;top:0;bottom:{fb}px;width:{pw}px"
    if side == "top": return f"left:72px;right:72px;top:0;height:{pw}px"
    if side == "bot": return f"left:72px;right:72px;bottom:{fb}px;height:{pw}px"
    if side == "ctr": return f"left:50%;transform:translateX(-50%);top:0;bottom:{fb}px;width:{pw}px"
    return ""

def build(cfg, lang, w=1600, h=900):
    bn = lang == "bn"; g = lambda k: cfg[k][1 if bn else 0]; DX[0] = cfg.get("dx", 0)
    side = cfg.get("side", "l"); foot = cfg.get("foot", True)
    svg = ""; html = ""
    for c in cfg.get("calls", []):
        tx, ty, lx, ly, anchor, col, en, bnx = c
        t, s = bnx if bn else en
        svg += leader(tx, ty, lx, ly) + ring(tx, ty, c=col)
        x, y = P(lx, ly)
        if anchor == "r": x = min(x, w - 24)
        pos = {"l": f"left:{max(x,16):.0f}px", "r": f"right:{w-x:.0f}px", "c": f"left:{x-180:.0f}px"}[anchor]
        html += f'<div class="call" style="{pos};top:{y-32:.0f}px;--c:{col}"><b>{t}</b>{f"<span>{s}</span>" if s else ""}</div>'
    for (x, y, n) in cfg.get("marks", []):
        X, Y = P(x, y); html += f'<div class="mk" style="left:{X:.0f}px;top:{Y:.0f}px">{"১২৩৪৫৬৭"[n-1] if bn else n}</div>'
    leg = ""
    if "legend" in cfg:
        for i, item in enumerate(cfg["legend"]):
            a, b = item[1] if bn else item[0]
            leg += (f'<div class="li"><div class="badge">{"১২৩৪৫৬৭"[i] if bn else i+1}</div>'
                    f'<div><b>{a}</b><span>{b}</span></div></div>')
        leg = f'<div class="legend">{leg}</div>'
    sub = g("sub")
    ill = f'<div class="ill">{"AI-তৈরি প্রতীকী ছবি" if bn else "AI-generated illustration"}</div>'
    src = g("src") if "src" in cfg else ""
    footer = (f'<div class="foot"><span>{("সূত্র: " if bn else "Sources: ") + src if src else ""}</span>'
              f'<b>{"সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "Sayedul Abrar, Pharmacist"} · sayedulabrar.site</b></div>') if foot else ""
    ts = cfg.get("ts", (76, 72))[1 if bn else 0]
    chips = ('<div class="chips' + (' one' if cfg.get('chips1') else '') + '">' + ''.join(
        f'<div class="chip"><b>{(c[1] if bn else c[0])[0]}</b><span>{(c[1] if bn else c[0])[1]}</span></div>'
        for c in cfg['chips']) + '</div>') if cfg.get('chips') else ''
    byline = (f'<p style="margin-top:30px;display:inline-block;background:#174F52;color:#fff;border-left:7px solid #D8A84E;'
              f'font-family:Int,HS;font-weight:600;font-size:27px;padding:12px 26px;border-radius:999px;'
              f'box-shadow:0 10px 24px rgba(15,60,66,.25)">'
              f'{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>') if cfg.get('byline') else ''
    extra = cfg.get("css", "")
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{extra}</style></head>'
            f'<body class="{lang}">'
            f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div>'
            f'<div class="veil" style="{veil_css(side, cfg.get("a", 32))}"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0">{svg}</svg>{html}'
            f'<div class="panel{" ctr" if side=="ctr" else ""}" style="{panel_css(side, cfg.get("pw",520), w, h, foot)};--ts:{ts}px">'
            f'<p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}{chips}{leg}{byline}</div>'
            f'{ill if cfg.get("ill", True) else ""}{footer}</body></html>')

STEEL, GOLD, TEAL, CORAL = "#526D82", "#D8A84E", "#174F52", "#E98250"
SRC = ("WHO TRS 986 Annex 2; ICH Q10; Drugs and Cosmetics Act, 2023",
       "WHO TRS 986 Annex 2; ICH Q10; ঔষধ ও কসমেটিকস আইন, ২০২৩")
SH = lambda px: f"background-size:auto 100%;background-position:calc(100% + {px}px) center;"

CFG = {
 # 1 — cover / thumbnail (text LEFT)
 "cover": dict(bg="cover", side="l", a=30, pw=520, ts=(104, 98), byline=True, foot=False, ill=False,
   kick=("Pharmaceutical quality", "ফার্মাসিউটিক্যাল কোয়ালিটি"),
   title=("What is <i>GMP</i>?", "<i>GMP</i> আসলে কী?"),
   sub=("Good Manufacturing Practices: the system that makes every batch the same.",
        "গুড ম্যানুফ্যাকচারিং প্র্যাকটিস — যে ব্যবস্থায় প্রতিটি ব্যাচ একই মানের হয়।")),

 # 2 — GMP is one connected system (text RIGHT)
 "system": dict(bg="system", side="r", a=34, pw=500, ts=(60, 58), src=SRC,
   kick=("Section 2", "অধ্যায় ২"),
   title=("One connected <i>system</i>", "একটি সংযুক্ত <i>ব্যবস্থা</i>"),
   sub=("", ""),
   chips=[(("People", "Trained, healthy, following written rules"), ("মানুষ", "প্রশিক্ষিত, সুস্থ, লিখিত নিয়ম মেনে চলা")),
          (("Premises", "Designed and cleaned to prevent mix-ups"), ("স্থাপনা", "মিশ্রণ ও দূষণ ঠেকাতে নকশা ও পরিচ্ছন্নতা")),
          (("Materials", "Approved suppliers, tested and released"), ("কাঁচামাল", "অনুমোদিত সরবরাহকারী, পরীক্ষা ও রিলিজ")),
          (("Records", "Every step written down as it happens"), ("রেকর্ড", "প্রতিটি ধাপ তখনই লিখে রাখা")),
          (("Process", "Validated and kept within set limits"), ("প্রক্রিয়া", "ভ্যালিডেটেড ও নির্ধারিত সীমার ভেতরে")),
          (("Oversight", "An independent quality unit decides"), ("তদারকি", "স্বাধীন কোয়ালিটি ইউনিট সিদ্ধান্ত নেয়"))],
   css=".chip b{font-size:26px!important}body.bn .chip b{font-size:28px!important}.chip span{font-size:19px!important}body.bn .chip span{font-size:22px!important}.chips{gap:11px!important}"),

 # 3 — people, training, hygiene (text LEFT)
 "people": dict(bg="people", side="l", a=29, pw=510, ts=(64, 60), src=SRC,
   kick=("Section 3", "অধ্যায় ৩"),
   title=("People make <i>quality</i>", "মান গড়ে তোলেন <i>মানুষ</i>"),
   sub=("Training, health checks and hygiene rules are GMP requirements, not extras.",
        "প্রশিক্ষণ, স্বাস্থ্য পরীক্ষা ও স্বাস্থ্যবিধি GMP-এর শর্ত, বাড়তি কিছু নয়।"),
   chips1=True,
   chips=[(("Trained for the job", "Written procedures, repeated training, records kept"),
           ("কাজের জন্য প্রশিক্ষণ", "লিখিত পদ্ধতি, বারবার প্রশিক্ষণ, রেকর্ড সংরক্ষণ")),
          (("Gowning and hygiene", "Change, wash and gown before entering clean areas"),
           ("গাউনিং ও স্বাস্থ্যবিধি", "ক্লিন এরিয়ায় ঢোকার আগে পোশাক বদল, হাত ধোয়া, গাউন"))],
   calls=[(1065, 400, 790, 165, "l", STEEL, ("Gloves last", "Hands washed, then gloved inside the airlock"),
           ("গ্লাভস শেষে", "হাত ধুয়ে, এরপর এয়ারলকের ভেতরে গ্লাভস"))]),

 # 4 — premises, equipment, contamination control (text RIGHT)
 "premises": dict(bg="premises", side="r", a=33, pw=500, ts=(60, 58), src=SRC,
   kick=("Section 4", "অধ্যায় ৪"),
   title=("Premises and <i>equipment</i>", "স্থাপনা ও <i>যন্ত্রপাতি</i>"),
   sub=("Clean areas, controlled air and qualified machines keep products apart and uncontaminated.",
        "ক্লিন এরিয়া, নিয়ন্ত্রিত বাতাস ও যোগ্যতা-যাচাই করা যন্ত্র পণ্যকে আলাদা ও দূষণমুক্ত রাখে।"),
   calls=[(205, 395, 205, 150, "l", STEEL, ("Airlock", "A controlled entry between clean areas"),
           ("এয়ারলক", "ক্লিন এরিয়ার মাঝে নিয়ন্ত্রিত প্রবেশপথ")),
          (415, 425, 300, 760, "l", GOLD, ("Pressure difference", "Air flows the way the design intends"),
           ("চাপের পার্থক্য", "বাতাস যেদিকে যাওয়ার কথা সেদিকেই যায়"))]),

 # 5 — documentation (text LEFT)
 "docs": dict(bg="docs", side="l", a=28, pw=505, ts=(60, 58), src=SRC,
   kick=("Section 5", "অধ্যায় ৫"),
   title=("If it was not <i>recorded</i>", "লেখা না থাকলে <i>প্রমাণ</i> নেই"),
   sub=("Batch records, procedures and audit trails are how quality is proved later.",
        "ব্যাচ রেকর্ড, পদ্ধতি ও অডিট ট্রেইল দিয়েই পরে মান প্রমাণ করা হয়।"),
   chips1=True,
   chips=[(("Write it as it happens", "Not from memory at the end of the shift"),
           ("যখন হচ্ছে তখনই লিখুন", "শিফট শেষে স্মৃতি থেকে নয়")),
          (("Keep the trail", "Changes stay visible, signed and dated"),
           ("ট্রেইল রাখুন", "পরিবর্তন দৃশ্যমান, স্বাক্ষর ও তারিখসহ"))]),

 # 6 — production control and validation (text TOP banner)
 "line": dict(bg="line", side="top", a=30, pw=300, ts=(58, 56), src=SRC,
   kick=("Section 6", "অধ্যায় ৬"),
   title=("Validated, then kept <i>in control</i>", "ভ্যালিডেশন, এরপর <i>নিয়ন্ত্রণে</i> রাখা"),
   sub=("Validation shows the process can work. In-process checks show it is still working, batch after batch.",
        "ভ্যালিডেশন দেখায় প্রক্রিয়াটি কাজ করতে পারে। ইন-প্রসেস চেক দেখায় এটি প্রতিটি ব্যাচেই কাজ করছে।"),
   marks=[(150, 640, 1), (430, 620, 2), (700, 600, 3), (1010, 620, 4), (1390, 620, 5)],
   css=".panel{justify-content:flex-start!important;padding-top:34px!important}.sub{max-width:1180px}"),

 # 7 — QA vs QC (text CENTRE column)
 "qaqc": dict(bg="qaqc", side="ctr", a=36, pw=430, ts=(54, 52), src=SRC,
   kick=("Section 7", "অধ্যায় ৭"),
   title=("QA is not <i>QC</i>", "QA আর <i>QC</i> এক নয়"),
   sub=("", ""),
   chips1=True,
   chips=[(("QA — the system", "Plans, approves and builds confidence that quality will be met"),
           ("QA — ব্যবস্থা", "পরিকল্পনা, অনুমোদন ও মান নিশ্চিত হওয়ার আস্থা তৈরি")),
          (("QC — the testing", "Sampling, specifications and laboratory checks"),
           ("QC — পরীক্ষা", "স্যাম্পলিং, স্পেসিফিকেশন ও ল্যাব পরীক্ষা"))],
   css=".chip{text-align:left}.chip b{font-size:27px!important}body.bn .chip b{font-size:29px!important}.chip span{font-size:20px!important}body.bn .chip span{font-size:23px!important}"),

 # 8 — deviation, CAPA, change control (text RIGHT)
 "capa": dict(bg="capa", side="r", a=38, pw=540, ts=(58, 56), src=SRC,
   kick=("Section 8", "অধ্যায় ৮"),
   title=("When something <i>goes wrong</i>", "কিছু <i>ভুল হলে</i>"),
   sub=("A deviation is recorded, investigated and closed with corrective and preventive action.",
        "ডেভিয়েশন লিপিবদ্ধ হয়, তদন্ত হয়, এরপর CAPA দিয়ে বন্ধ করা হয়।"),
   legend=[(("Detect and record", "Stop, document what was seen"), ("শনাক্ত ও লিপিবদ্ধ", "থামুন, যা দেখা গেল তা লিখুন")),
           (("Assess the impact", "Which batches could be affected"), ("প্রভাব যাচাই", "কোন ব্যাচগুলো প্রভাবিত হতে পারে")),
           (("Find the root cause", "Not just the symptom"), ("মূল কারণ খুঁজুন", "শুধু উপসর্গ নয়")),
           (("Act — CAPA", "Correct it, then prevent recurrence"), ("পদক্ষেপ — CAPA", "সংশোধন, এরপর পুনরাবৃত্তি রোধ")),
           (("Verify it worked", "Check the fix held"), ("কার্যকারিতা যাচাই", "সমাধান টিকল কি না দেখুন"))],
   css=".sub{font-size:28px!important;margin-top:12px!important}body.bn .sub{font-size:30px!important}"
       ".legend{gap:9px!important;margin-top:16px!important}.li{padding:9px 16px!important}"
       ".badge{width:44px!important;height:44px!important;font-size:23px!important}"
       ".li b{font-size:25px!important}body.bn .li b{font-size:27px!important}"
       ".li span{font-size:20px!important}body.bn .li span{font-size:23px!important}"),

 # 9 — suppliers, storage, complaints, recall (text LEFT)
 "supply": dict(bg="supply", side="l", a=31, pw=515, ts=(58, 56), src=SRC,
   kick=("Section 9", "অধ্যায় ৯"),
   title=("Quality does not stop at the <i>gate</i>", "মান <i>গেটেই</i> শেষ নয়"),
   sub=("Approved suppliers, controlled storage and a workable recall route are part of GMP.",
        "অনুমোদিত সরবরাহকারী, নিয়ন্ত্রিত সংরক্ষণ ও কার্যকর রিকল পদ্ধতি GMP-এরই অংশ।"),
   calls=[(900, 560, 700, 215, "l", GOLD, ("Quarantine", "Held until tested and released"),
           ("কোয়ারেন্টিন", "পরীক্ষা ও রিলিজ না হওয়া পর্যন্ত আটক")),
          (1430, 640, 1105, 715, "l", TEAL, ("Released stock", "Approved, labelled, ready to ship"),
           ("রিলিজড স্টক", "অনুমোদিত, লেবেলযুক্ত, পাঠানোর জন্য প্রস্তুত"))]),

 # 10 — GMP in Bangladesh (text BOTTOM band)
 "bd": dict(bg="bd", side="bot", a=34, pw=250, ts=(54, 52), foot=False, ill=False,
   kick=("Section 10", "অধ্যায় ১০"),
   title=("GMP in <i>Bangladesh</i>", "<i>বাংলাদেশে</i> GMP"),
   sub=("Section 17 of the Drugs and Cosmetics Act, 2023 addresses WHO Good Practices, and DGDA adopted WHO TRS 986 Annex 2 by an office order dated 11 May 2018. Licence conditions and current DGDA notices also apply.",
        "ঔষধ ও কসমেটিকস আইন, ২০২৩-এর ১৭ ধারায় WHO Good Practices-এর কথা বলা হয়েছে এবং DGDA ১১ মে ২০১৮ তারিখের অফিস আদেশে WHO TRS 986 Annex 2 গ্রহণ করে। লাইসেন্সের শর্ত ও DGDA-র চলতি নির্দেশনাও প্রযোজ্য।"),
   css=".panel{justify-content:flex-start!important}.sub{font-size:26px!important;line-height:1.3!important;max-width:1400px}"
       "body.bn .sub{font-size:28px!important}"),

 # 11 — key takeaways (text RIGHT)
 "key": dict(bg="key", side="r", a=34, pw=530, ts=(56, 54), src=SRC,
   kick=("Key takeaways", "মূল কথা"),
   title=("Five things to <i>remember</i>", "পাঁচটি <i>মনে রাখার</i> কথা"),
   sub=("", ""),
   legend=[(("GMP is a whole system", "People, premises, materials, records, process, oversight"),
            ("GMP একটি পূর্ণ ব্যবস্থা", "মানুষ, স্থাপনা, কাঁচামাল, রেকর্ড, প্রক্রিয়া, তদারকি")),
           (("Records are the proof", "If it was not recorded, it is hard to prove"),
            ("রেকর্ডই প্রমাণ", "লেখা না থাকলে প্রমাণ করা কঠিন")),
           (("QA and QC are different", "One is the system, the other is the testing"),
            ("QA ও QC আলাদা", "একটি ব্যবস্থা, অন্যটি পরীক্ষা")),
           (("Problems get investigated", "Deviation, root cause, CAPA, verification"),
            ("সমস্যার তদন্ত হয়", "ডেভিয়েশন, মূল কারণ, CAPA, যাচাই")),
           (("It is law here too", "Drugs and Cosmetics Act, 2023 and DGDA requirements"),
            ("এটি এখানেও আইন", "ঔষধ ও কসমেটিকস আইন, ২০২৩ ও DGDA-র শর্ত"))],
   css=".legend{gap:10px!important;margin-top:18px!important}.li{padding:10px 16px!important}"
       ".badge{width:46px!important;height:46px!important;font-size:24px!important}"
       ".li b{font-size:26px!important}body.bn .li b{font-size:28px!important}"
       ".li span{font-size:20px!important}body.bn .li span{font-size:23px!important}"),
}

NAMES = {
 "cover": "gmp-good-manufacturing-practices-cover",
 "system": "gmp-one-connected-pharmaceutical-quality-system",
 "people": "gmp-people-training-and-hygiene",
 "premises": "gmp-premises-equipment-and-contamination-control",
 "docs": "gmp-documentation-and-batch-records",
 "line": "gmp-production-control-and-process-validation",
 "qaqc": "gmp-quality-assurance-versus-quality-control",
 "capa": "gmp-deviation-capa-and-change-control",
 "supply": "gmp-suppliers-storage-complaints-and-recall",
 "bd": "gmp-requirements-in-bangladesh-dgda",
 "key": "gmp-key-takeaways",
}

TMP = H / "_render.html"
def shot(pg, html, path, w=1600, h=900):
    pg.set_viewport_size({"width": w, "height": h})
    TMP.write_text(html, encoding="utf-8")
    pg.goto(TMP.as_uri(), wait_until="load")
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(path))

keys = sys.argv[2:] or list(CFG)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(device_scale_factor=1)
    for k in keys:
        cfg = CFG[k]
        for lang in ("en", "bn"):
            tmp = OUT / f"{NAMES[k]}{'-bn' if lang=='bn' else ''}.png"
            shot(pg, build(cfg, lang), tmp)
            im = Image.open(tmp).convert("RGB")
            im.save(tmp.with_suffix(".webp"), "WEBP", quality=88, method=6)
            tmp.unlink()
            print("•", tmp.with_suffix(".webp").name)
    # social share images from the cover
    for lang in ("en", "bn"):
        tmp = OUT / f"gmp-social-{lang}.png"
        shot(pg, build(CFG["cover"], lang, 1200, 675), tmp, 1200, 675)
        im = Image.open(tmp).convert("RGB").crop((0, 22, 1200, 652))
        im.save(OUT / f"gmp-social-{lang}.jpg", "JPEG", quality=86, optimize=True)
        tmp.unlink()
        print("•", f"gmp-social-{lang}.jpg")
    b.close()
TMP.unlink(missing_ok=True)
print("done")
