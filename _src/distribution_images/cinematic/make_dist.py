#!/usr/bin/env python3
"""Cinematic EN + BN graphics for the Drug Distribution article, built on the user's AI images (no text in source images).
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
.chip{{background:var(--sage);border-radius:16px;padding:16px 18px;border-left:6px solid var(--c,var(--teal))}}
.chip b{{display:block;font-family:Pop;font-weight:800;font-size:23px;line-height:1.15;color:var(--teal)}}
body.bn .chip b{{font-family:HS;font-weight:700;font-size:27px;line-height:1.25}}
.chip span{{display:block;font-size:20px;line-height:1.35;color:var(--char);margin-top:6px}}
body.bn .chip span{{font-size:23px;font-weight:500}}
.kick{{display:flex;align-items:center;gap:12px;font-family:Int;font-size:20px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--steel)}}
.kick:before{{content:"";width:40px;height:4px;border-radius:2px;background:var(--coral)}}
body.bn .kick{{letter-spacing:.02em;font-size:24px;font-family:HS;font-weight:700}}
.title{{font-family:Pop,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.04;letter-spacing:-.01em;margin-top:16px;color:var(--teal)}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.2;letter-spacing:0}}
.title em{{font-style:normal;color:var(--teal)}}
.title i{{font-style:normal;color:var(--coral)}}
.sub{{font-size:29px;line-height:1.42;color:var(--char);margin-top:18px;font-weight:500}}
body.bn .sub{{font-size:31px;line-height:1.5}}
.legend{{margin-top:26px;display:flex;flex-direction:column;gap:14px;width:100%}}
.li{{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.9);border-radius:14px;padding:12px 16px}}
.badge{{flex:none;width:42px;height:42px;border-radius:50%;background:var(--teal);color:#fff;font-family:Pop,HS;font-weight:800;font-size:21px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700;font-size:24px}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:24px;line-height:1.2;color:var(--teal)}}
.li span{{display:block;font-size:20px;line-height:1.35;color:var(--char)}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:28px}}
body.bn .li span{{font-size:23px;font-weight:500}}
.li span.tag{{display:inline-block;color:#fff;margin-top:5px;font-size:15px;font-weight:600;padding:2px 10px;border-radius:999px}}
.call{{position:absolute;background:#fff;border-radius:14px;padding:11px 16px;box-shadow:0 10px 26px rgba(37,50,56,.22);border-left:6px solid var(--c,var(--teal));max-width:300px}}
.call b{{display:block;font-family:Pop;font-weight:800;font-size:21px;color:var(--teal);line-height:1.15}}
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
    byline = (f'<p style="margin-top:34px;display:inline-block;background:#174F52;color:#fff;font-family:Int,HS;font-weight:600;font-size:{22 if w>1300 else 19}px;padding:12px 26px;border-radius:999px;box-shadow:0 10px 24px rgba(15,60,66,.25)">{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>') if cfg.get('byline') else ''
    tight = '<style>.legend{gap:10px!important;margin-top:18px!important}body.bn .legend{gap:7px!important;margin-top:14px!important}.li b{font-size:25px!important}body.bn .li b{font-size:27px!important}.li span{font-size:20px!important}body.bn .li span{font-size:22px!important}.badge{width:38px!important;height:38px!important;font-size:20px!important}</style>' if cfg.get('tight') else ''
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body class="{lang}">{tight}'
            f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div><div class="veil" style="--a:{cfg.get("a","30%")};--b:{cfg.get("b","46%")};{cfg.get("veilcss","")}"></div><div class="vig"></div>'
            f'<svg width="{w}" height="{h}" style="position:absolute;inset:0">{svg}</svg>{html}'
            f'<div class="panel" style="--pw:{cfg.get("pw",560)}px;--ts:{ts}px;--fb:{58 if cfg.get("foot", True) else 0}px"><p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}{chips}{leg}{byline}</div>{ill if cfg.get("ill", True) else ""}{foot}</body></html>')

TEAL, ORANGE, RED, PURPLE, BLUE = "#174F52", "#E98250", "#E98250", "#D8A84E", "#526D82"  # palette: teal, coral, coral, gold, steel
TEAL, ORANGE, RED, PURPLE, BLUE = "#174F52", "#E98250", "#E98250", "#D8A84E", "#526D82"  # palette: teal, coral, coral, gold, steel
CFG = {
 "cover": dict(bg="cover", a="28%", b="40%", pw=640, byline=True, ts=(98, 92), foot=False, ill=False,
   kick=("Pharmacology made simple", "সহজ ভাষায় ফার্মাকোলজি"),
   title=("Drug <i>Distribution</i>", "ওষুধের <i>বণ্টন</i>"),
   sub=("How does medicine reach different parts of the body?", "ওষুধ কীভাবে শরীরের বিভিন্ন অংশে পৌঁছায়?")),
 "highway": dict(bg="highway", a="30%", b="40%", pw=540, ts=(66, 64),
   kick=("How it travels", "কীভাবে যায়"), title=("Riding the <i>bloodstream</i>", "রক্তপ্রবাহে <i>ওষুধের যাত্রা</i>"), sub=("", ""),
   marks=[(860, 380, 1), (1440, 110, 2), (1565, 395, 3), (1480, 700, 4)],
   legend=[(("Bloodstream", "The heart pumps blood that carries the medicine.", None), ("রক্তপ্রবাহ", "হৃৎপিণ্ডের পাম্প করা রক্ত ওষুধ বয়ে নেয়।", None)),
           (("Liver", "Rich blood supply, so medicine can arrive quickly.", None), ("যকৃৎ", "রক্ত সরবরাহ বেশি, তাই ওষুধ দ্রুত পৌঁছাতে পারে।", None)),
           (("Kidneys", "Also receive a large share of blood flow.", None), ("কিডনি", "এরাও রক্তপ্রবাহের বড় অংশ পায়।", None)),
           (("Muscle", "Muscle and fat may receive it more slowly.", None), ("মাংসপেশি", "মাংসপেশি ও চর্বিতে ওষুধ তুলনামূলক ধীরে পৌঁছাতে পারে।", None))],
   src=("StatPearls; MSD Manual", "StatPearls; MSD Manual")),
 "barrier": dict(bg="barrier", a="28%", b="38%", pw=540, ts=(66, 64),
   chips=[(("Often cross", "Small, fat-soluble molecules"), ("প্রায়ই পার হয়", "ছোট, চর্বিতে দ্রবণীয় অণু"), ORANGE), (("Often kept out", "Large or strongly charged molecules"), ("প্রায়ই আটকে যায়", "বড় বা বেশি চার্জযুক্ত অণু"), BLUE)],
   kick=("Special barriers", "বিশেষ বাধা"), title=("The <i>blood–brain</i> barrier", "<i>ব্লাড–ব্রেইন</i> ব্যারিয়ার"),
   sub=("Tightly joined cells let only some medicines into the brain.", "শক্তভাবে জোড়া লাগানো কোষ শুধু কিছু ওষুধকে মস্তিষ্কে ঢুকতে দেয়।"),
   calls=[(960, 255, 1200, 95, "l", BLUE, ("Kept out", "Larger molecules can't pass the wall"), ("আটকে যায়", "বড় অণু দেয়াল পেরোতে পারে না")),
          (1340, 600, 1655, 735, "r", ORANGE, ("Gets through", "Small, fat-soluble molecules reach the brain"), ("ঢুকে যায়", "ছোট, চর্বিতে দ্রবণীয় অণু মস্তিষ্কে পৌঁছায়")),
          (1095, 655, 690, 800, "l", PURPLE, ("Tight junctions", "Cells sealed closely together"), ("টাইট জাংশন", "কোষগুলো শক্তভাবে জোড়া লাগানো"))],
   src=("StatPearls; MSD Manual", "StatPearls; MSD Manual")),
 "binding": dict(bg="binding", a="27%", b="37%", pw=470, ts=(70, 66),
   kick=("Plasma protein binding", "প্লাজমা প্রোটিন বাইন্ডিং"), title=("Bound vs <i>free</i> drug", "আবদ্ধ বনাম <i>মুক্ত</i> ওষুধ"),
   sub=("Many medicines ride on albumin in the blood. In general, only the free part can leave the blood, act and be removed.",
        "অনেক ওষুধ রক্তে অ্যালবুমিনের সঙ্গে যুক্ত থাকে। সাধারণত শুধু মুক্ত অংশই রক্ত ছেড়ে কাজ করতে ও বের হতে পারে।"),
   calls=[(880, 470, 655, 800, "l", BLUE, ("Albumin + bound drug", "Held in the blood for now"), ("অ্যালবুমিন + আবদ্ধ ওষুধ", "আপাতত রক্তেই থাকে")),
          (1180, 505, 1150, 280, "c", ORANGE, ("Free drug", "Not attached to protein"), ("মুক্ত ওষুধ", "প্রোটিনের সঙ্গে যুক্ত নয়")),
          (1440, 630, 1655, 735, "r", TEAL, ("Into the tissue", "Free drug crosses the vessel wall"), ("টিস্যুতে প্রবেশ", "মুক্ত ওষুধ রক্তনালির দেয়াল পেরোয়"))],
   src=("StatPearls; MSD Manual", "StatPearls; MSD Manual")),
}
NAMES = {"cover": "drug-distribution-cover-cinematic", "highway": "medicine-travelling-in-bloodstream-to-organs",
         "barrier": "blood-brain-barrier-drug-distribution", "binding": "plasma-protein-binding-free-vs-bound-drug"}
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
                c = dict(CFG["cover"]); c["ts"] = (80, 72); c["pw"] = 500
                shot(build(c, lang, 1200, 630), 1200, 630, OUT / f"drug-distribution-social-{lang}.jpg", "jpeg")
    br.close()
