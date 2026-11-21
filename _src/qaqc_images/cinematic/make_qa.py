#!/usr/bin/env python3
"""Cinematic EN + BN figures for the GMP article, built on the user's AI images (no text in source images).
Palette: Universal Medical Editorial Palette. QA vs QC recipe = charcoal headline + sage-pill keyword, coral kicker with teal bar,
outlined white chips, sage callouts with coral bar, steel circles with coral ring.
Usage: python3 make_qa.py OUTDIR [keys...]"""
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

.kick{{display:flex;align-items:center;gap:14px;font-family:Int;font-size:25px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#C2542A}}
.kick:before{{content:"";width:7px;height:30px;border-radius:4px;background:var(--teal)}}
body.bn .kick{{letter-spacing:.02em;font-size:29px;font-family:HS;font-weight:700}}
.panel.ctr .kick{{justify-content:center}}

.title{{font-family:Pop,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.1;letter-spacing:-.01em;margin-top:14px;color:var(--char)}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.2;letter-spacing:0}}
.title i{{font-style:normal;color:var(--teal);background:var(--sage);border-radius:14px;padding:.02em .16em .06em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}

.sub{{font-size:35px;line-height:1.32;color:var(--char);margin-top:16px;font-weight:500}}
body.bn .sub{{font-size:37px;line-height:1.42}}

.chips{{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:24px}}
.chips.one{{grid-template-columns:1fr}}
.chip{{background:rgba(255,255,255,.95);border-radius:14px;padding:13px 18px;border:3px solid var(--teal)}}
.chip b{{display:block;font-family:Pop;font-weight:800;font-size:29px;line-height:1.1;color:var(--teal)}}
body.bn .chip b{{font-family:HS;font-weight:700;font-size:31px;line-height:1.25}}
.chip span{{display:block;font-size:22px;line-height:1.25;color:var(--char);margin-top:5px}}
body.bn .chip span{{font-size:25px;font-weight:500}}

.legend{{margin-top:22px;display:flex;flex-direction:column;gap:12px;width:100%}}
.li{{display:flex;gap:16px;align-items:center;background:rgba(220,235,231,.95);border-radius:14px;padding:12px 18px;border-left:8px solid var(--coral)}}
.badge{{flex:none;width:54px;height:54px;border-radius:50%;background:var(--steel);color:#fff;box-shadow:0 0 0 4px rgba(233,130,80,.85);font-family:Pop,HS;font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:30px;line-height:1.15;color:var(--teal)}}
.li span{{display:block;font-size:23px;line-height:1.25;color:var(--char)}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:32px}}
body.bn .li span{{font-size:26px;font-weight:500}}

.call{{position:absolute;background:rgba(224,238,234,.97);border-radius:14px;padding:12px 20px;box-shadow:0 12px 30px rgba(37,50,56,.3);border-left:8px solid var(--c,var(--coral));max-width:430px}}
.call b{{display:block;font-family:Pop;font-weight:800;font-size:30px;color:var(--teal);line-height:1.12}}
body.bn .call b{{font-family:HS;font-weight:700;font-size:33px;line-height:1.25}}
.call span{{display:block;font-size:23px;line-height:1.25;color:var(--char);margin-top:3px}}
body.bn .call span{{font-size:26px;font-weight:500}}

.mk{{position:absolute;width:52px;height:52px;margin:-26px 0 0 -26px;border-radius:50%;background:var(--steel);color:#fff;font-family:Pop,HS;font-weight:800;font-size:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff,0 0 0 10px rgba(233,130,80,.8),0 10px 24px rgba(0,0,0,.3)}}
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
    byline = (f'<p style="margin-top:30px;display:inline-block;background:#C2542A;color:#fff;border-left:7px solid #174F52;'
              f'font-family:Int,HS;font-weight:600;font-size:27px;padding:12px 26px;border-radius:999px;'
              f'box-shadow:0 10px 24px rgba(160,60,30,.28)">'
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
SRC = ("ICH Q10; ICH Q7; WHO TRS 986 Annex 2; US FDA OOS guidance",
       "ICH Q10; ICH Q7; WHO TRS 986 Annex 2; US FDA OOS নির্দেশিকা")

CFG = {
 # cover — text LEFT
 "cover": dict(bg="cover", side="l", a=33, pw=520, ts=(96, 90), byline=True, foot=False, ill=False,
   kick=("Pharmaceutical quality", "ফার্মাসিউটিক্যাল কোয়ালিটি"),
   title=("QA vs <i>QC</i>", "QA বনাম <i>QC</i>"),
   sub=("Quality Assurance builds the system. Quality Control does the testing. They are not the same job.",
        "কোয়ালিটি অ্যাসিওরেন্স ব্যবস্থা গড়ে তোলে, কোয়ালিটি কন্ট্রোল পরীক্ষা করে। দুটি এক কাজ নয়।")),

 # 1 — what is QA (LEFT)
 "qa": dict(bg="qa", side="l", a=29, pw=510, ts=(58, 56), src=SRC,
   kick=("Section 1", "অধ্যায় ১"),
   title=("What is <i>QA</i>?", "<i>QA</i> কী?"),
   sub=("Planned, systematic arrangements that give confidence a product will meet its quality requirements.",
        "পরিকল্পিত ও সুসংগঠিত ব্যবস্থা, যা আস্থা দেয় যে পণ্য তার মানের শর্ত পূরণ করবে।"),
   chips1=True,
   chips=[(("Builds the system", "Quality system, procedures, training, change control"),
           ("ব্যবস্থা গড়ে তোলে", "কোয়ালিটি সিস্টেম, পদ্ধতি, প্রশিক্ষণ, চেঞ্জ কন্ট্রোল")),
          (("Reviews and approves", "Documents, deviations, investigations, batch review"),
           ("পর্যালোচনা ও অনুমোদন", "নথি, ডেভিয়েশন, তদন্ত, ব্যাচ রিভিউ"))]),

 # 2 — what is QC (RIGHT)
 "qc": dict(bg="qc", side="r", a=33, pw=500, ts=(58, 56), src=SRC,
   kick=("Section 2", "অধ্যায় ২"),
   title=("What is <i>QC</i>?", "<i>QC</i> কী?"),
   sub=("The part of the quality system concerned with sampling, specifications and testing.",
        "কোয়ালিটি সিস্টেমের যে অংশ স্যাম্পলিং, স্পেসিফিকেশন ও পরীক্ষা নিয়ে কাজ করে।"),
   chips1=True,
   chips=[(("Samples and tests", "Raw materials, in-process samples, finished product"),
           ("নমুনা ও পরীক্ষা", "কাঁচামাল, ইন-প্রসেস নমুনা, তৈরি পণ্য")),
          (("Reports the evidence", "Analytical data, stability results, specifications"),
           ("প্রমাণ দেয়", "অ্যানালিটিক্যাল ডেটা, স্ট্যাবিলিটি ফল, স্পেসিফিকেশন"))],
   calls=[(540, 430, 300, 165, "l", TEAL, ("Test, don't guess", "Against an approved specification"),
           ("অনুমান নয়, পরীক্ষা", "অনুমোদিত স্পেসিফিকেশন অনুযায়ী"))]),

 # 3 — practical differences (CENTRE column)
 "diff": dict(bg="diff", side="ctr", a=39, pw=400, ts=(50, 48), src=SRC,
   kick=("Section 3", "অধ্যায় ৩"),
   title=("Prevent vs <i>detect</i>", "প্রতিরোধ বনাম <i>শনাক্ত</i>"),
   sub=("", ""),
   chips1=True,
   chips=[(("QA — prevent", "System-oriented: procedures, audits, CAPA, change control, batch review"),
           ("QA — প্রতিরোধ", "ব্যবস্থাভিত্তিক: পদ্ধতি, অডিট, CAPA, চেঞ্জ কন্ট্রোল, ব্যাচ রিভিউ")),
          (("QC — detect", "Measurement: sampling plans, laboratory testing, in-process checks"),
           ("QC — শনাক্ত", "পরিমাপ: স্যাম্পলিং প্ল্যান, ল্যাব পরীক্ষা, ইন-প্রসেস চেক"))],
   css=".chip{text-align:left}.chip b{font-size:26px!important}body.bn .chip b{font-size:28px!important}"
       ".chip span{font-size:19px!important}body.bn .chip span{font-size:22px!important}"),

 # 4 — a tablet batch (BOTTOM band)
 "batch": dict(bg="batch", side="bot", a=31, pw=272, ts=(50, 48), foot=False, ill=False,
   kick=("Section 4", "অধ্যায় ৪"),
   title=("One batch, <i>both roles</i>", "এক ব্যাচ, <i>দুই ভূমিকা</i>"),
   sub=("Before manufacturing, QA confirms procedures, training and validation; QC tests incoming materials. During and after, QC runs the specified checks and QA reviews the record before the batch is dispositioned.",
        "উৎপাদনের আগে QA নিশ্চিত করে পদ্ধতি, প্রশিক্ষণ, যন্ত্রের অবস্থা ও ভ্যালিডেশন ঠিক আছে, আর QC কাঁচামাল পরীক্ষা করে। উৎপাদনের সময় ও পরে QC নির্ধারিত পরীক্ষা চালায় এবং QA রেকর্ড পর্যালোচনা করে ব্যাচের সিদ্ধান্ত হয়।"),
   marks=[(230, 560, 1), (640, 480, 2), (1120, 560, 3), (1470, 540, 4)],
   css=".panel{justify-content:flex-start!important;padding:20px 0 0!important}.sub{font-size:24px!important;line-height:1.3!important;max-width:1440px;margin-top:10px!important}"
       "body.bn .sub{font-size:26px!important}"),

 # 5 — when a test result fails (LEFT)
 "oos": dict(bg="oos", side="l", a=26, pw=500, ts=(54, 52), src=SRC,
   kick=("Section 5", "অধ্যায় ৫"),
   title=("An <i>OOS</i> result", "<i>OOS</i> ফলাফল এলে"),
   sub=("An out-of-specification result is investigated, not retested until it passes.",
        "আউট-অব-স্পেসিফিকেশন ফল বারবার পরীক্ষা করে পাস করানোর বিষয় নয়, তদন্তের বিষয়।"),
   legend=[(("Investigate under procedure", "Documented and scientifically sound"),
            ("পদ্ধতি মেনে তদন্ত", "নথিভুক্ত ও বিজ্ঞানসম্মত")),
           (("Check the laboratory first", "Execution, calculation, instrument, sample handling"),
            ("আগে ল্যাব দেখুন", "কাজের ধরন, হিসাব, যন্ত্র, নমুনা ব্যবস্থাপনা")),
           (("Then look at production", "Manufacturing or material causes"),
            ("এরপর উৎপাদন দেখুন", "উৎপাদন বা কাঁচামালজনিত কারণ")),
           (("Retest only if justified", "Controlled, never to replace a result"),
            ("যুক্তি থাকলেই পুনঃপরীক্ষা", "নিয়ন্ত্রিত, ফল বদলানোর জন্য নয়")),
           (("QC tests, QA oversees", "QA checks the investigation and the decision"),
            ("QC পরীক্ষা, QA তদারকি", "QA তদন্ত ও সিদ্ধান্ত যাচাই করে"))],
   css=".sub{font-size:27px!important;margin-top:12px!important}body.bn .sub{font-size:29px!important}"
       ".legend{gap:9px!important;margin-top:16px!important}.li{padding:9px 15px!important}"
       ".badge{width:44px!important;height:44px!important;font-size:23px!important}"
       ".li b{font-size:24px!important}body.bn .li b{font-size:26px!important}"
       ".li span{font-size:19px!important}body.bn .li span{font-size:22px!important}"),

 # 6 — QA, QC and GMP together (RIGHT)
 "gmp": dict(bg="gmp", side="r", a=32, pw=500, ts=(54, 52), src=SRC,
   kick=("Section 6", "অধ্যায় ৬"),
   title=("QA, QC and <i>GMP</i>", "QA, QC ও <i>GMP</i>"),
   sub=("GMP is the requirement. QA is the wider assurance framework. QC is an essential part of it. None replaces another.",
        "GMP হলো শর্ত, QA হলো বৃহত্তর আশ্বাস কাঠামো, QC তার একটি অপরিহার্য অংশ। একটি অন্যটির বিকল্প নয়।"),
   chips1=True,
   chips=[(("A QC lab alone is not GMP", "Quality is built into people, premises and process"),
           ("শুধু QC ল্যাব মানেই GMP নয়", "মান গড়ে ওঠে মানুষ, স্থাপনা ও প্রক্রিয়ায়"))],
   css=".sub{font-size:28px!important}body.bn .sub{font-size:30px!important}"),

 # 7 — why it matters to patients (LEFT)
 "patient": dict(bg="patient", side="l", a=30, pw=515, ts=(54, 52), src=SRC,
   kick=("Section 7", "অধ্যায় ৭"),
   title=("What the <i>patient</i> gets", "<i>রোগী</i> যা পান"),
   sub=("Patients never see the audit trail or the batch review. They receive the outcome: the right identity, strength, purity and quality, through the shelf life when stored as directed.",
        "রোগী অডিট ট্রেইল বা ব্যাচ রিভিউ দেখেন না। তাঁরা ফলাফলটি পান: সঠিক পরিচয়, মাত্রা, বিশুদ্ধতা ও মান — নির্দেশমতো সংরক্ষণে মেয়াদকাল জুড়ে।"),
   css=".sub{font-size:28px!important}body.bn .sub{font-size:30px!important}"),

 # key takeaways (LEFT)
 "key": dict(bg="key", side="l", a=33, pw=540, ts=(52, 50), src=SRC,
   kick=("Key takeaways", "মূল কথা"),
   title=("Five things to <i>remember</i>", "পাঁচটি <i>মনে রাখার</i> কথা"),
   sub=("", ""),
   legend=[(("QA prevents, QC detects", "Different jobs inside one quality system"),
            ("QA প্রতিরোধ করে, QC শনাক্ত করে", "একই কোয়ালিটি সিস্টেমে ভিন্ন কাজ")),
           (("QC is part of QA", "Not a rival department"),
            ("QC হলো QA-র অংশ", "প্রতিদ্বন্দ্বী বিভাগ নয়")),
           (("Neither replaces GMP", "GMP is the requirement both work under"),
            ("কেউই GMP-র বিকল্প নয়", "GMP সেই শর্ত, যার অধীনে দুটিই কাজ করে")),
           (("An OOS result is investigated", "Not retested until it passes"),
            ("OOS ফলাফল তদন্ত হয়", "পাস না হওয়া পর্যন্ত পুনঃপরীক্ষা নয়")),
           (("Quality is everyone's job", "Production records its own checks too"),
            ("মান সবার দায়িত্ব", "উৎপাদন বিভাগও নিজের চেক লিপিবদ্ধ করে"))],
   css=".legend{gap:10px!important;margin-top:18px!important}.li{padding:10px 16px!important}"
       ".badge{width:46px!important;height:46px!important;font-size:24px!important}"
       ".li b{font-size:25px!important}body.bn .li b{font-size:27px!important}"
       ".li span{font-size:20px!important}body.bn .li span{font-size:23px!important}"),
}

NAMES = {
 "cover":   "quality-assurance-vs-quality-control-cover",
 "qa":      "what-is-quality-assurance-in-pharmaceuticals",
 "qc":      "what-is-quality-control-in-pharmaceuticals",
 "diff":    "qa-vs-qc-prevention-versus-detection",
 "batch":   "qa-and-qc-roles-in-a-tablet-batch",
 "oos":     "out-of-specification-result-investigation",
 "gmp":     "how-qa-qc-and-gmp-fit-together",
 "patient":"why-qa-and-qc-matter-to-patients",
 "key":     "qa-vs-qc-key-takeaways",
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
        for lang in ("en", "bn"):
            tmp = OUT / f"{NAMES[k]}{'-bn' if lang=='bn' else ''}.png"
            shot(pg, build(CFG[k], lang), tmp)
            Image.open(tmp).convert("RGB").save(tmp.with_suffix(".webp"), "WEBP", quality=88, method=6)
            tmp.unlink(); print("•", tmp.with_suffix(".webp").name)
    for lang in ("en", "bn"):
        tmp = OUT / f"qaqc-social-{lang}.png"
        shot(pg, build(CFG["cover"], lang, 1200, 675), tmp, 1200, 675)
        Image.open(tmp).convert("RGB").crop((0, 22, 1200, 652)).save(OUT / f"qaqc-social-{lang}.jpg", "JPEG", quality=86, optimize=True)
        tmp.unlink(); print("•", f"qaqc-social-{lang}.jpg")
    b.close()
TMP.unlink(missing_ok=True)
print("done")
