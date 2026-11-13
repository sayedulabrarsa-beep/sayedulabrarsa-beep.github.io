#!/usr/bin/env python3
"""Cinematic EN + BN graphics for the Drug Absorption article, built on the user's AI images (no text in source images).
Usage: python3 make_cine.py OUTDIR [keys...]"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
SC = 1600 / 1672  # source images are ~1672x941
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
body{{width:var(--w);height:var(--h);overflow:hidden;position:relative;font-family:Poppins,HS,sans-serif;color:#0f3c42;background:#f7f2ec}}
body.bn{{font-family:HS,Poppins,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(250,246,240,.97) 0%,rgba(250,246,240,.9) var(--a,30%),rgba(250,246,240,0) var(--b,44%))}}
.vig{{position:absolute;inset:0;box-shadow:inset 0 0 160px rgba(15,60,66,.18)}}
.panel{{position:absolute;left:64px;top:0;bottom:var(--fb,58px);width:var(--pw,560px);display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:30px 0}}
.chips{{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}}
.chip{{background:rgba(255,255,255,.92);border-radius:18px;padding:16px 18px;box-shadow:0 10px 26px rgba(15,60,66,.12);border-top:6px solid var(--c,#17807a)}}
.chip b{{display:block;font-family:Anton,sans-serif;font-weight:400;text-transform:uppercase;font-size:31px;line-height:1.05;color:var(--c,#17807a)}}
body.bn .chip b{{font-family:Anek;font-weight:800;text-transform:none;font-size:31px;line-height:1.2}}
.chip span{{display:block;font-size:21px;line-height:1.3;color:#2a4a51;margin-top:6px}}
body.bn .chip span{{font-size:23px}}
.kick{{display:flex;align-items:center;gap:12px;font-size:20px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#17807a}}
.kick:before{{content:"";width:46px;height:4px;border-radius:2px;background:linear-gradient(90deg,#17807a,#e0892b)}}
body.bn .kick{{letter-spacing:.02em;font-size:24px;font-family:Anek,HS}}
.title{{font-family:Anton,Impact,sans-serif;text-transform:uppercase;font-size:var(--ts,86px);line-height:.98;letter-spacing:.005em;margin-top:14px;color:#0f3c42}}
body.bn .title{{font-family:Anek,HS;font-weight:800;text-transform:none;line-height:1.12;letter-spacing:0}}
.title em{{font-style:normal;background:linear-gradient(90deg,#0d9488,#14b8a6);-webkit-background-clip:text;background-clip:text;color:transparent}}
.title i{{font-style:normal;background:linear-gradient(90deg,#e0562b,#f59e0b);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{font-size:30px;line-height:1.38;color:#2a4a51;margin-top:16px;font-weight:500}}
body.bn .sub{{font-size:32px;line-height:1.45}}
.legend{{margin-top:26px;display:flex;flex-direction:column;gap:18px}}
.li{{display:flex;gap:14px;align-items:flex-start}}
.badge{{flex:none;width:44px;height:44px;border-radius:50%;background:#0f3c42;color:#fff;font-family:Anton,Anek,sans-serif;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(255,255,255,.85)}}
body.bn .badge{{font-family:Anek;font-weight:800;font-size:25px}}
.li b{{display:block;font-size:28px;line-height:1.2;color:#0f3c42}}
.li span{{display:block;font-size:22px;line-height:1.3;color:#3b5960}}
body.bn .li b{{font-family:Anek;font-weight:700;font-size:30px}}
body.bn .li span{{font-size:24px}}
.li span.tag{{display:inline-block;color:#fff;margin-top:5px;font-size:15px;font-weight:700;color:#fff;padding:2px 10px;border-radius:999px;letter-spacing:.04em}}
body.bn .li span.tag{{font-size:17px;font-family:Anek}}
.call{{position:absolute;background:rgba(255,255,255,.93);backdrop-filter:blur(6px);border-radius:16px;padding:10px 16px;box-shadow:0 12px 30px rgba(15,60,66,.22);border-left:6px solid var(--c,#17807a);max-width:300px}}
.call b{{display:block;font-family:Anton,sans-serif;text-transform:uppercase;letter-spacing:.03em;font-size:25px;font-weight:400;color:#0f3c42;line-height:1.05}}
body.bn .call b{{font-family:Anek;font-weight:800;text-transform:none;font-size:27px;line-height:1.2}}
.call span{{display:block;font-size:19px;line-height:1.3;color:#36555c;margin-top:3px}}
body.bn .call span{{font-size:20px}}
.mk{{position:absolute;width:52px;height:52px;margin:-26px 0 0 -26px;border-radius:50%;background:#0f3c42;color:#fff;font-family:Anton,Anek,sans-serif;font-size:27px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px rgba(255,255,255,.9),0 0 0 11px rgba(23,128,122,.35),0 10px 24px rgba(0,0,0,.3)}}
body.bn .mk{{font-family:Anek;font-weight:800}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:54px;display:flex;justify-content:space-between;align-items:center;padding:0 64px;font-size:18px;color:#3b5960;background:linear-gradient(90deg,rgba(250,246,240,.95),rgba(250,246,240,.75))}}
body.bn .foot{{font-size:20px}}
.foot b{{color:#0f3c42;font-weight:700}}
.ill{{position:absolute;right:20px;bottom:64px;font-size:15px;color:#3b5960;background:rgba(255,255,255,.8);padding:3px 12px;border-radius:999px}}
body.bn .ill{{font-size:17px}}
"""
P = lambda x, y: (x * SC, y * SC)
def ring(x, y, r=34, c="#17807a"):
    x, y = P(x, y)
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#fff" stroke-width="4"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r+7}" fill="none" stroke="{c}" stroke-width="3" opacity=".75"/><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#fff"/>'
def leader(tx, ty, lx, ly, c="#ffffff"):
    a, b = P(tx, ty); c2, d = P(lx, ly)
    return f'<path d="M{a:.0f},{b:.0f} L{c2:.0f},{d:.0f}" stroke="{c}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" fill="none" style="filter:drop-shadow(0 1px 2px rgba(0,0,0,.45))"/>'

def build(cfg, lang, w=1600, h=900):
    bn = lang == "bn"; g = lambda k: cfg[k][1 if bn else 0]
    svg = ""; html = ""
    for c in cfg.get("calls", []):
        tx, ty, lx, ly, anchor, col, en, bnx = c
        t, s = bnx if bn else en
        svg += leader(tx, ty, lx, ly) + ring(tx, ty, c=col)
        x, y = P(lx, ly)
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
    byline = (f'<p style="margin-top:34px;display:inline-block;background:#0f3c42;color:#fff;font-weight:700;font-size:{26 if w>1300 else 22}px;padding:12px 26px;border-radius:999px;box-shadow:0 10px 24px rgba(15,60,66,.25)">{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>') if cfg.get('byline') else ''
    tight = '<style>.legend{gap:10px!important;margin-top:18px!important}body.bn .legend{gap:7px!important;margin-top:14px!important}.li b{font-size:25px!important}body.bn .li b{font-size:27px!important}.li span{font-size:20px!important}body.bn .li span{font-size:22px!important}.badge{width:38px!important;height:38px!important;font-size:20px!important}</style>' if cfg.get('tight') else ''
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body class="{lang}">{tight}'
            f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div><div class="veil" style="--a:{cfg.get("a","30%")};--b:{cfg.get("b","46%")};{cfg.get("veilcss","")}"></div><div class="vig"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0">{svg}</svg>{html}'
            f'<div class="panel" style="--pw:{cfg.get("pw",560)}px;--ts:{ts}px;--fb:{58 if cfg.get("foot", True) else 0}px"><p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}{chips}{leg}{byline}</div>{ill if cfg.get("ill", True) else ""}{foot}</body></html>')

TEAL, ORANGE, RED, PURPLE, BLUE = "#17807a", "#e0892b", "#d0453c", "#7b5cc4", "#4a6fd6"
CFG = {
 "cover": dict(bg="cover", veilcss="background:linear-gradient(90deg,#f8f3ee 0%,#f8f3ee 22%,rgba(248,243,238,.9) 36%,rgba(248,243,238,0) 50%);", bgcss="background-size:auto 100%;background-position:calc(100% + 150px) center;", a="34%", b="50%", pw=700, top=110, byline=True, ts=(124, 94), foot=False, ill=False,
   kick=("Pharmacology made simple", "সহজ ভাষায় ফার্মাকোলজি"),
   title=("<i>Drug</i> <em>Absorption</em>", "<i>ওষুধের</i> <em>শোষণ</em>"),
   sub=("How does medicine enter the bloodstream?", "ওষুধ কীভাবে রক্তে প্রবেশ করে?")),
 "journey": dict(bg="journey", a="32%", b="48%", pw=600, ts=(84, 72),
   kick=("The big picture", "পুরো চিত্র"), title=("The <i>journey</i> of <em>a tablet</em>", "একটি <em>ট্যাবলেটের</em> <i>যাত্রা</i>"), sub=("", ""),
   marks=[(1268, 495, 1), (1120, 700, 2), (1015, 470, 3), (1235, 185, 4)],
   legend=[(("Stomach", "The tablet breaks up and starts to dissolve.", None), ("পাকস্থলী", "ট্যাবলেট ভেঙে গলতে শুরু করে।", None)),
           (("Small intestine", "Most of the medicine is absorbed here.", None), ("ক্ষুদ্রান্ত্র", "বেশির ভাগ ওষুধ এখানে শোষিত হয়।", None)),
           (("Portal vein → liver", "Some drug is metabolised on this first pass.", None), ("পোর্টাল শিরা → যকৃৎ", "এই প্রথম যাত্রায় কিছু ওষুধ বিপাক হয়।", None)),
           (("Heart → whole body", "The rest travels in the blood to where it acts.", None), ("হৃৎপিণ্ড → সারা শরীর", "বাকি ওষুধ রক্তে মিশে কাজের জায়গায় যায়।", None))],
   src=("MSD Manual; StatPearls", "MSD Manual; StatPearls")),
 "villi": dict(bg="villi", a="30%", b="44%", pw=560, ts=(88, 76), chips=[(("Huge surface", "Folds, villi and microvilli"), ("বিশাল জায়গা", "ভাঁজ, ভিলাই ও মাইক্রোভিলাই"), "#17807a"), (("Main site", "Small intestine absorbs most oral drugs"), ("প্রধান জায়গা", "মুখে খাওয়া বেশির ভাগ ওষুধ ক্ষুদ্রান্ত্রে শোষিত হয়"), "#d0453c")],
   kick=("Close view", "কাছ থেকে দেখুন"), title=("Where <em>absorption</em> <i>happens</i>", "<em>শোষণ</em> <i>কোথায়</i> হয়"),
   sub=("Folds, villi and microvilli give the small intestine a huge surface, so most oral medicines are absorbed here.",
        "ভাঁজ, ভিলাই ও মাইক্রোভিলাই ক্ষুদ্রান্ত্রে বিশাল জায়গা তৈরি করে, তাই বেশির ভাগ মুখে খাওয়া ওষুধ এখানেই শোষিত হয়।"),
   calls=[(935, 92, 600, 205, "l", TEAL, ("Medicine molecules", "Dissolved drug in gut fluid"), ("ওষুধের অণু", "অন্ত্রের তরলে দ্রবীভূত ওষুধ")),
          (1330, 125, 1655, 60, "r", ORANGE, ("Microvilli", "Tiny brush border on each cell"), ("মাইক্রোভিলাই", "প্রতিটি কোষের মাথায় সূক্ষ্ম ব্রাশ")),
          (1215, 640, 700, 440, "l", PURPLE, ("Villus", "Finger-like fold lined with absorbing cells"), ("ভিলাস", "শোষণকারী কোষে ঢাকা আঙুলের মতো অংশ")),
          (1330, 772, 1655, 610, "r", RED, ("Into the blood", "Molecules enter tiny capillaries"), ("রক্তে প্রবেশ", "অণু সূক্ষ্ম রক্তনালিতে ঢোকে"))],
   src=("StatPearls, Drug Absorption", "StatPearls, Drug Absorption")),
 "membrane": dict(bg="membrane", a="30%", b="42%", pw=560, ts=(82, 70), chips=[(("No energy", "Passive diffusion: high → low"), ("শক্তি লাগে না", "প্যাসিভ ডিফিউশন: বেশি → কম"), "#17807a"), (("Uses energy", "Active transport by a carrier"), ("শক্তি লাগে", "ক্যারিয়ারের মাধ্যমে সক্রিয় পরিবহন"), "#e0892b")],
   kick=("Molecular level", "অণুর স্তরে"), title=("Crossing the <em>cell</em> <i>membrane</i>", "<em>কোষপর্দা</em> <i>পেরোনো</i>"),
   sub=("Medicines cross the fat-like (lipid) membrane of gut cells in two main ways.", "অন্ত্রের কোষের চর্বিজাতীয় পর্দা ওষুধ মূলত দুইভাবে পার হয়।"),
   calls=[(905, 505, 600, 790, "l", TEAL, ("Passive diffusion", "High → low concentration, no energy"), ("প্যাসিভ ডিফিউশন", "বেশি থেকে কম ঘনত্বে, শক্তি লাগে না")),
          (1395, 450, 1655, 90, "r", ORANGE, ("Transporter protein", "Carries a molecule; active transport uses energy"), ("ট্রান্সপোর্টার প্রোটিন", "অণু বহন করে; সক্রিয় পরিবহনে শক্তি লাগে")),
          (1140, 560, 1160, 790, "c", BLUE, ("Lipid bilayer", "The cell's outer membrane"), ("লিপিড বাইলেয়ার", "কোষের বাইরের পর্দা"))],
   src=("StatPearls; MSD Manual", "StatPearls; MSD Manual")),
 "liver": dict(bg="liver", a="30%", b="44%", pw=560, ts=(88, 74), chips=[(("IV = 100%", "Skips absorption and the first pass"), ("শিরায় = ১০০%", "শোষণ ও ফার্স্ট পাস এড়িয়ে যায়"), "#4a6fd6"), (("Under the tongue", "Some medicines avoid much of the first pass"), ("জিভের নিচে", "কিছু ওষুধ ফার্স্ট পাসের বড় অংশ এড়ায়"), "#e0892b")],
   kick=("Bioavailability", "বায়োঅ্যাভেইলেবিলিটি"), title=("<i>First-pass</i> <em>metabolism</em>", "<i>ফার্স্ট-পাস</i> <em>মেটাবলিজম</em>"),
   sub=("Blood from the gut passes the liver first, so less active drug reaches the rest of the body.", "অন্ত্রের রক্ত আগে যকৃতে যায়, তাই কম সক্রিয় ওষুধ সারা শরীরে পৌঁছায়।"),
   calls=[(860, 720, 600, 800, "l", BLUE, ("Portal vein", "Brings absorbed drug from the gut"), ("পোর্টাল শিরা", "অন্ত্র থেকে শোষিত ওষুধ আনে")),
          (1195, 335, 1010, 105, "c", ORANGE, ("Liver breaks some down", "First-pass metabolism"), ("যকৃৎ কিছু ভেঙে ফেলে", "ফার্স্ট-পাস মেটাবলিজম")),
          (1350, 200, 1655, 380, "r", RED, ("To the heart", "Then to the whole body"), ("হৃৎপিণ্ডের দিকে", "তারপর সারা শরীরে"))],
   src=("StatPearls, First-Pass Effect", "StatPearls, First-Pass Effect")),
 "routes": dict(bg="routes", a="33%", b="40%", pw=570, ts=(72, 54), tight=True,
   kick=("Routes of administration", "প্রয়োগের পথ"), title=("Does every <i>route</i> need <em>absorption?</em>", "সব <i>পথে</i> কি <em>শোষণ</em> লাগে?"), sub=("", ""),
   marks=[(668, 462, 1), (1040, 300, 2), (1190, 260, 3), (1480, 240, 4), (825, 700, 5), (1130, 650, 6)],
   legend=[(("Swallowed tablet", "Dissolves and is absorbed in the gut.", ("Absorption needed", TEAL)), ("মুখে খাওয়া ট্যাবলেট", "গলে গিয়ে অন্ত্রে শোষিত হয়।", ("শোষণ লাগে", TEAL))),
           (("Injection (IM / SC)", "Absorbed from muscle or under the skin.", ("Absorption needed", TEAL)), ("ইনজেকশন (IM / SC)", "মাংসপেশি বা চামড়ার নিচ থেকে শোষিত হয়।", ("শোষণ লাগে", TEAL))),
           (("Inhaler", "Many act right in the airways.", ("Depends on product", "#b26a0e")), ("ইনহেলার", "অনেকগুলো শ্বাসনালিতেই কাজ করে।", ("পণ্যভেদে ভিন্ন", "#b26a0e"))),
           (("IV drip", "Goes straight into the blood.", ("No absorption step", "#1f7a57")), ("আইভি স্যালাইন", "সরাসরি রক্তে যায়।", ("শোষণ লাগে না", "#1f7a57"))),
           (("Skin patch", "Slowly passes through the skin.", ("Depends on product", "#b26a0e")), ("স্কিন প্যাচ", "ধীরে ধীরে ত্বক পেরোয়।", ("পণ্যভেদে ভিন্ন", "#b26a0e"))),
           (("Under the tongue", "Absorbed through the lining of the mouth.", ("Absorption needed", TEAL)), ("জিভের নিচে", "মুখের ভেতরের আবরণী দিয়ে শোষিত হয়।", ("শোষণ লাগে", TEAL)))],
   src=("StatPearls; MSD Manual", "StatPearls; MSD Manual")),
}
NAMES = {"cover": "drug-absorption-cover-cinematic", "journey": "journey-of-a-tablet-through-the-body", "villi": "intestinal-villi-close-up-drug-absorption",
         "membrane": "drug-crossing-cell-membrane-diffusion-transporter", "liver": "first-pass-metabolism-liver-portal-vein", "routes": "routes-of-medicine-administration-absorption"}
with sync_playwright() as p:
    br = p.chromium.launch()
    def shot(htm, w, h, path, fmt="webp"):
        pg = br.new_page(viewport={"width": w, "height": h}); f = H / "_c.html"; f.write_text(htm, encoding="utf-8")
        pg.goto(f.as_uri()); pg.wait_for_timeout(500)
        over = pg.evaluate("()=>{const p=document.querySelector('.panel');return p.getBoundingClientRect().bottom>document.body.clientHeight-58}")
        im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
        im.save(path, "WEBP", quality=88, method=6) if fmt == "webp" else im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(("OVERFLOW " if over else "") + path.name)
    for key in (sys.argv[2:] or list(CFG)):
        for lang in ("en", "bn"):
            shot(build(CFG[key], lang), 1600, 900, OUT / f"{NAMES[key]}{'-bn' if lang == 'bn' else ''}.webp")
        if key == "cover":
            for lang in ("en", "bn"):
                c = dict(CFG["cover"]); c["ts"] = (96, 74); c["top"] = 90; c["pw"] = 560
                shot(build(c, lang, 1200, 630), 1200, 630, OUT / f"social-{lang}.jpg", "jpeg")
    br.close()
