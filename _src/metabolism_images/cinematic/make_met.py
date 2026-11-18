#!/usr/bin/env python3
"""Cinematic EN + BN graphics for the Drug Metabolism article, built on the user's AI images (no text in source images).
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
.chip{{background:#fff;border-radius:14px;padding:14px 16px;border-top:5px solid var(--c,var(--gold));box-shadow:0 8px 20px rgba(37,50,56,.10)}}
.chip b{{display:block;font-family:Pop;font-weight:800;font-size:21px;line-height:1.15;color:var(--char)}}
body.bn .chip b{{font-family:HS;font-weight:700;font-size:27px;line-height:1.25}}
.chip span{{display:block;font-size:18px;line-height:1.35;color:var(--char);margin-top:6px}}
body.bn .chip span{{font-size:23px;font-weight:500}}
.kick{{display:flex;align-items:center;gap:12px;font-family:Int;font-size:20px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--teal)}}
.kick:before{{content:"";width:40px;height:4px;border-radius:2px;background:var(--gold)}}
body.bn .kick{{letter-spacing:.02em;font-size:24px;font-family:HS;font-weight:700}}
.title{{font-family:Pop,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.08;letter-spacing:-.01em;margin-top:16px;color:var(--char)}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.2;letter-spacing:0}}
.title em{{font-style:normal;color:var(--teal)}}
.title i{{font-style:normal;color:var(--char);background:linear-gradient(transparent 56%,rgba(216,168,78,.85) 56%,rgba(216,168,78,.85) 90%,transparent 90%);padding:0 .06em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.sub{{font-size:29px;line-height:1.42;color:var(--char);margin-top:18px;font-weight:500}}
body.bn .sub{{font-size:31px;line-height:1.5}}
.legend{{margin-top:26px;display:flex;flex-direction:column;gap:14px;width:100%}}
.li{{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.92);border-radius:14px;padding:12px 16px;border-left:5px solid var(--gold)}}
.badge{{flex:none;width:42px;height:42px;border-radius:12px;background:var(--steel);color:#fff;font-family:Pop,HS;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700;font-size:24px}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:24px;line-height:1.2;color:var(--char)}}
.li span{{display:block;font-size:20px;line-height:1.35;color:var(--char)}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:28px}}
body.bn .li span{{font-size:23px;font-weight:500}}
.li span.tag{{display:inline-block;color:#fff;margin-top:5px;font-size:15px;font-weight:600;padding:2px 10px;border-radius:999px}}
.call{{position:absolute;background:#fff;border-radius:14px;padding:11px 16px;box-shadow:0 10px 26px rgba(37,50,56,.22);border-left:6px solid var(--c,var(--teal));max-width:300px}}
.call b{{display:block;font-family:Pop;font-weight:800;font-size:21px;color:var(--char);line-height:1.15}}
body.bn .call b{{font-family:HS;font-weight:700;font-size:25px;line-height:1.25}}
.call span{{display:block;font-size:18px;line-height:1.35;color:var(--char);margin-top:3px}}
body.bn .call span{{font-size:20px;font-weight:500}}
.mk{{position:absolute;width:50px;height:50px;margin:-25px 0 0 -25px;border-radius:50%;background:var(--teal);color:#fff;font-family:Pop,HS;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff,0 0 0 10px var(--mkc,rgba(233,130,80,.55)),0 10px 24px rgba(0,0,0,.3)}}
body.bn .mk{{font-family:HS;font-weight:700}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:54px;display:flex;justify-content:space-between;align-items:center;padding:0 96px;font-size:17px;color:var(--steel);background:rgba(247,241,230,.94)}}
body.bn .foot{{font-size:19px}}
.foot b{{color:var(--teal);font-weight:600}}
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
.ill{{font-size:17px!important;bottom:70px!important}}
.title{{color:var(--char)!important}}
.title i{{color:#fff!important;background:var(--teal)!important;padding:0 .14em!important;border-radius:.12em}}
.kick{{color:var(--steel)!important}} .kick:before{{background:var(--coral)!important}}
.badge{{background:var(--coral)!important;border-radius:50%!important}}
.li{{border-left-color:var(--teal)!important}}
.chip{{background:var(--sage)!important}}"""
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
    byline = (f'<p style="margin-top:34px;display:inline-block;background:#174F52;color:#fff;border-left:6px solid #E98250;font-family:Int,HS;font-weight:600;font-size:{27 if w>1300 else 24}px;padding:12px 26px;border-radius:999px;box-shadow:0 10px 24px rgba(15,60,66,.25)">{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>') if cfg.get('byline') else ''
    tight = '<style>.legend{gap:10px!important;margin-top:18px!important}body.bn .legend{gap:7px!important;margin-top:14px!important}.li b{font-size:25px!important}body.bn .li b{font-size:27px!important}.li span{font-size:20px!important}body.bn .li span{font-size:22px!important}.badge{width:38px!important;height:38px!important;font-size:20px!important}</style>' if cfg.get('tight') else ''
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body class="{lang}">{tight}'
            f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div><div class="veil" style="--a:{cfg.get("a","30%")};--b:{cfg.get("b","46%")};{cfg.get("veilcss","")}"></div><div class="vig"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0">{svg}</svg>{html}'
            f'<div class="panel" style="{cfg.get("panelcss","")};--pw:{cfg.get("pw",560)}px;--ts:{ts}px;--fb:{58 if cfg.get("foot", True) else 0}px"><p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}{chips}{leg}{byline}</div>{ill if cfg.get("ill", True) else ""}{foot}</body></html>')

TEAL, CORAL, GOLD, STEEL = "#174F52", "#E98250", "#D8A84E", "#526D82"
SRC = ("Goodman & Gilman; StatPearls; Merck Manual", "Goodman & Gilman; StatPearls; Merck Manual")
SH = lambda px: f"background-size:auto 100%;background-position:calc(100% + {px}px) center;"
VE = lambda a: f"background:linear-gradient(90deg,#F7F1E6 0%,#F7F1E6 {a}%,rgba(247,241,230,.88) {a+7}%,rgba(247,241,230,0) {a+20}%);"
TOP = "justify-content:flex-start;padding-top:70px"
CFG = {
 "cover": dict(bg="cover", dx=60, bgcss=SH(60), veilcss=VE(30), pw=560, byline=True, ts=(100, 104), foot=False, ill=False,
   kick=("Drug metabolism", "ওষুধের বিপাক"),
   title=("How the body <i>changes</i> medicines", "শরীর কীভাবে ওষুধ <i>বদলায়</i>"),
   sub=("The liver, enzymes and first-pass metabolism in simple words.", "যকৃত, enzyme ও first-pass metabolism—সহজ ভাষায়।")),
 "liver": dict(bg="liver", veilcss=VE(28), pw=540, ts=(80, 80),
   kick=("Why the liver matters", "যকৃত কেন গুরুত্বপূর্ণ"),
   title=("The main <i>processing</i> centre", "ওষুধ প্রক্রিয়ার <i>প্রধান</i> কেন্দ্র"),
   sub=("Other tissues help too: gut wall, kidneys, lungs and blood.", "অন্ত্রের দেয়াল, কিডনি, ফুসফুস ও রক্তেও বিপাক হয়।"),
   calls=[(1420, 330, 1655, 120, "r", TEAL, ("Liver", "Many drug enzymes"), ("যকৃত", "অনেক enzyme থাকে")),
          (1160, 760, 760, 760, "l", CORAL, ("Portal vein", "Blood from the gut"), ("Portal vein", "অন্ত্র থেকে আসা রক্ত"))],
   src=SRC),
 "enzyme": dict(bg="enzyme", veilcss=VE(28), pw=540, ts=(80, 80),
   kick=("Drug-metabolising enzymes", "ওষুধ-বিপাকী enzyme"),
   title=("<i>CYP</i> enzymes do the work", "কাজ করে <i>CYP</i> enzyme"),
   sub=("Enzymes are proteins that speed up chemical reactions.", "Enzyme হলো প্রোটিন, যা রাসায়নিক বিক্রিয়া দ্রুত করে।"),
   chips=[(("Genes", "Fast or slow enzymes"), ("জিন", "দ্রুত বা ধীর enzyme"), TEAL), (("Other medicines", "Can block or boost"), ("অন্য ওষুধ", "কমাতে বা বাড়াতে পারে"), CORAL)],
   calls=[(1030, 560, 760, 130, "l", CORAL, ("Enzyme pocket", "Holds the drug"), ("Enzyme-এর খাঁজ", "ওষুধকে ধরে রাখে")),
          (1560, 470, 1655, 760, "r", TEAL, ("Metabolite", "The changed molecule"), ("Metabolite", "পরিবর্তিত অণু"))],
   src=SRC),
 "phases": dict(bg="phases", veilcss=VE(18), pw=430, ts=(64, 66), panelcss=TOP,
   kick=("Two kinds of reaction", "দুই ধরনের বিক্রিয়া"),
   title=("Phase I and <i>Phase II</i>", "Phase I ও <i>Phase II</i>"),
   sub=("Often makes a drug easier to remove.", "প্রায়ই ওষুধকে বের হওয়ার উপযোগী করে।"),
   calls=[(690, 500, 690, 700, "c", STEEL, ("Drug", "Original molecule"), ("ওষুধ", "মূল অণু")),
          (1075, 380, 1030, 700, "c", CORAL, ("Phase I", "Oxidation, reduction, hydrolysis"), ("Phase I", "Oxidation, reduction, hydrolysis")),
          (1430, 370, 1440, 150, "c", TEAL, ("Phase II", "A group is attached, e.g. glucuronide"), ("Phase II", "নতুন group যুক্ত হয়, যেমন glucuronide"))],
   src=SRC),
 "firstpass": dict(bg="firstpass", veilcss=VE(28), pw=540, ts=(78, 76),
   kick=("First-pass metabolism", "First-pass metabolism"),
   title=("Some is <i>changed</i> on the first trip", "প্রথম যাত্রায় কিছু অংশ <i>বদলে</i> যায়"),
   sub=("So less unchanged drug may reach the blood.", "তাই রক্তে কম অপরিবর্তিত ওষুধ পৌঁছাতে পারে।"),
   calls=[(985, 815, 760, 640, "l", STEEL, ("1 · Gut", "Drug is absorbed"), ("১ · অন্ত্র", "ওষুধ শোষিত হয়")),
          (1250, 250, 760, 110, "l", CORAL, ("2 · Liver", "Part of the dose is metabolised"), ("২ · যকৃত", "ডোজের কিছু অংশ বিপাক হয়")),
          (1470, 240, 1655, 470, "r", TEAL, ("3 · Bloodstream", "The rest circulates"), ("৩ · রক্তপ্রবাহ", "বাকিটা শরীরে ছড়ায়"))],
   src=SRC),
 "prodrug": dict(bg="prodrug", veilcss=VE(28), pw=540, ts=(76, 76),
   kick=("Prodrugs", "Prodrug"),
   title=("Metabolism can <i>switch on</i> a drug", "বিপাকে ওষুধ <i>সক্রিয়</i> হতে পারে"),
   sub=("Example: codeine → morphine by CYP2D6. The response varies between people.", "উদাহরণ: CYP2D6-এর মাধ্যমে codeine থেকে morphine। মানুষভেদে প্রতিক্রিয়া ভিন্ন।"),
   calls=[(985, 520, 760, 730, "l", STEEL, ("Prodrug", "Inactive form"), ("Prodrug", "নিষ্ক্রিয় রূপ")),
          (1400, 520, 1655, 730, "r", TEAL, ("Active drug", "Made in the liver cell"), ("সক্রিয় ওষুধ", "যকৃত-কোষে তৈরি"))],
   src=SRC),
 "takeaways": dict(bg="takeaways", dx=40, bgcss=SH(40), veilcss=VE(33), pw=600, ts=(76, 76),
   kick=("Key takeaways", "মূল কথা"), title=("Metabolism in <i>5 points</i>", "৫ কথায় <i>বিপাক</i>"), sub=("", ""),
   legend=[(("Chemical change", "The body alters the medicine.", None), ("রাসায়নিক পরিবর্তন", "শরীর ওষুধের গঠন বদলায়।", None)),
           (("The liver leads", "Other tissues help too.", None), ("যকৃত প্রধান", "অন্য টিস্যুতেও হয়।", None)),
           (("CYP enzymes", "Drive many reactions.", None), ("CYP enzyme", "অনেক বিক্রিয়া চালায়।", None)),
           (("First pass", "Less drug may reach the blood.", None), ("First pass", "রক্তে কম ওষুধ পৌঁছাতে পারে।", None)),
           (("Not always 'off'", "Some drugs become active.", None), ("সবসময় নিষ্ক্রিয় নয়", "কিছু ওষুধ সক্রিয় হয়।", None))],
   src=SRC),
}
NAMES = {"cover": "drug-metabolism-cover", "liver": "liver-main-site-of-drug-metabolism", "enzyme": "cyp-enzyme-drug-metabolism",
         "phases": "phase-1-phase-2-drug-metabolism", "firstpass": "first-pass-metabolism-gut-liver-bloodstream",
         "prodrug": "prodrug-activated-by-metabolism", "takeaways": "drug-metabolism-key-takeaways"}
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
                c = dict(CFG["cover"]); c["ts"] = (84, 88); c["pw"] = 470; c["dx"] = 60; c["bgcss"] = SH(60)
                shot(build(c, lang, 1200, 630), 1200, 630, OUT / f"drug-metabolism-social-{lang}.jpg", "jpeg")
    br.close()
