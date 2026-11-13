#!/usr/bin/env python3
"""Drug absorption article diagrams (EN + BN). Usage: python3 make_abs.py OUTDIR [keys...]"""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
CSS = f"""
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;font-family:Poppins,HS,sans-serif;color:#173d43;background:linear-gradient(135deg,#f3faf8 0%,#ffffff 55%,#fff4ec 100%);position:relative}}
body.bn{{font-family:HS,Poppins,sans-serif}}
.frame{{position:absolute;inset:0;padding:44px 64px 0;display:flex;flex-direction:column}}
.kick{{font-size:22px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#2f8f83}}
body.bn .kick{{letter-spacing:0;font-size:25px}}
h1{{font-size:50px;line-height:1.15;font-weight:700;margin-top:4px}}
body.bn h1{{font-size:52px;line-height:1.3}}
.card{{background:#fff;border-radius:22px;box-shadow:0 10px 28px rgba(23,61,67,.09);border:1px solid #e3eeec}}
.t{{font-size:28px;font-weight:700;line-height:1.22}}
.p{{font-size:23px;line-height:1.38;color:#2d464e}}
body.bn .t{{font-size:31px;line-height:1.3}}
body.bn .p{{font-size:25px;line-height:1.45}}
.num{{width:48px;height:48px;border-radius:50%;background:#17656a;color:#fff;font-weight:700;font-size:25px;display:inline-flex;align-items:center;justify-content:center;flex:none}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:60px;display:flex;justify-content:space-between;align-items:center;padding:0 64px;font-size:20px;color:#5b6f75;border-top:2px solid #dbe9e6;background:rgba(255,255,255,.7)}}
body.bn .foot{{font-size:21px}}
.foot b{{color:#17656a}}
.lbl{{font-family:Poppins,HS,sans-serif;font-weight:600;fill:#173d43}}
body.bn .lbl{{font-family:HS,Poppins,sans-serif}}
"""
def page(lang, body, src):
    bn = lang == "bn"
    name = "সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "Sayedul Abrar, Pharmacist"
    lab = "সূত্র: " if bn else "Sources: "
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{lang}">'
            f'<div class="frame">{body}</div><div class="foot"><span>{lab}{src}</span><b>{name} · sayedulabrar.site</b></div></body></html>')
D = lambda n, bn: "০১২৩৪৫৬৭৮৯"[n] if bn else str(n)

# ---------- SVG parts ----------
def mol(x, y, r=7, c="#19a29a"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#0f6d68" stroke-width="1.5"/>'
def tablet(x, y, s=1): return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="8" rx="46" ry="12" fill="#cfd8da"/><rect x="-46" y="-8" width="92" height="16" fill="#e9eef0"/>'
                               f'<ellipse cx="0" cy="-8" rx="46" ry="14" fill="#ffffff" stroke="#c9d4d6" stroke-width="2"/><line x1="-30" y1="-8" x2="30" y2="-8" stroke="#d5dee0" stroke-width="3"/></g>')
def rbc(x, y, s=1): return f'<g transform="translate({x},{y}) scale({s})"><ellipse rx="16" ry="11" fill="#d94b45"/><ellipse rx="8" ry="5" fill="#b8352f"/></g>'
def arrow(x1, y1, x2, y2, c="#2f8f83", w=5):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 16
    p1 = (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)); p2 = (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><path d="M{p1[0]:.1f},{p1[1]:.1f} L{x2},{y2} L{p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def cell_row(x, y, n, w=110, h=150, micro=True):
    g = ""
    for i in range(n):
        cx = x + i * w
        g += f'<rect x="{cx}" y="{y}" width="{w-4}" height="{h}" rx="14" fill="#f6c9b8" stroke="#d9957d" stroke-width="2.5"/><ellipse cx="{cx+w/2-2}" cy="{y+h*0.62}" rx="20" ry="16" fill="#9b6fb3" opacity=".75"/>'
        if micro:
            for k in range(9):
                mx = cx + 8 + k * (w - 20) / 8
                g += f'<rect x="{mx-3}" y="{y-26}" width="7" height="28" rx="3.5" fill="#f2b7a3" stroke="#d9957d" stroke-width="1.5"/>'
    return g
def villus(x, y, h=210, w=70, fill="#f4a99a"):
    return (f'<path d="M{x-w/2},{y} L{x-w/2},{y-h+w/2} A{w/2},{w/2} 0 0 1 {x+w/2},{y-h+w/2} L{x+w/2},{y} Z" fill="{fill}" stroke="#d9806c" stroke-width="3"/>'
            f'<path d="M{x-10},{y} L{x-10},{y-h+w/2+6} A10,10 0 0 1 {x+10},{y-h+w/2+6} L{x+10},{y}" fill="none" stroke="#d94b45" stroke-width="5" opacity=".75"/>')

# ========== 0. Bangla cover ==========
def cover(lang, w=1600, h=900):
    bn = lang == "bn"
    k = "সহজ ভাষায় ফার্মাকোলজি" if bn else "Pharmacology made simple"
    t = "ওষুধের শোষণ: ওষুধ কীভাবে রক্তে প্রবেশ করে?" if bn else "Drug Absorption: How Does Medicine Enter the Bloodstream?"
    by = "লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"
    sc = w / 1600
    svg = f'''<svg viewBox="0 0 700 700" width="{700*sc}" height="{700*sc}" style="position:absolute;right:{40*sc}px;top:{(h-700*sc)/2}px">
      <circle cx="350" cy="350" r="320" fill="#fde9e3"/>
      <rect x="40" y="430" width="620" height="130" rx="60" fill="#f6dcd3"/>
      <path d="M40 520 Q350 560 660 520 L660 640 Q350 600 40 640Z" fill="#e45b52"/>{rbc(170,590,1.4)}{rbc(330,585,1.4)}{rbc(500,592,1.4)}
      {villus(140,470,250,90)}{villus(260,470,300,90)}{villus(380,470,270,90)}{villus(500,470,310,90)}{villus(610,470,240,80)}
      {mol(205,260,10)}{mol(320,200,10)}{mol(440,240,10)}{mol(560,200,10)}{mol(330,150,9)}{mol(210,330,9)}
      {arrow(560,300,545,540,"#0f6d68",4)}{arrow(330,250,320,540,"#0f6d68",4)}
      {tablet(470,95,1.4)}</svg>'''
    body = (f'<div style="position:absolute;left:{80*sc}px;top:{150*sc}px;width:{760*sc}px"><p class="kick" style="font-size:{24*sc}px">{k}</p>'
            f'<h1 style="font-size:{(70 if not bn else 66)*sc}px;line-height:{1.12 if not bn else 1.3};margin-top:{12*sc}px">{t}</h1>'
            f'<p style="margin-top:{36*sc}px;display:inline-block;background:#17656a;color:#fff;font-weight:600;font-size:{25*sc}px;padding:{12*sc}px {26*sc}px;border-radius:999px">{by}</p></div>{svg}')
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}body{{width:{w}px;height:{h}px}}</style></head><body class="{lang}">{body}</body></html>'

# ========== 1. Journey ==========
def journey(lang):
    bn = lang == "bn"
    k, t = ("সহজ চিত্র", "গিলে খাওয়া ট্যাবলেটের যাত্রা") if bn else ("Simplified diagram", "The journey of a swallowed tablet")
    L = (["মুখ ও খাদ্যনালি", "পাকস্থলী", "ক্ষুদ্রান্ত্র", "পোর্টাল শিরা", "যকৃৎ", "রক্তপ্রবাহ"] if bn else
         ["Mouth and food pipe", "Stomach", "Small intestine", "Portal vein", "Liver", "Bloodstream"])
    S = ([("গিলে ফেলা", "ট্যাবলেট খাদ্যনালি দিয়ে পাকস্থলীতে যায়।"), ("ভাঙে ও দ্রবীভূত হয়", "অনেক ট্যাবলেট তরলে ভেঙে গলতে শুরু করে।"),
          ("শোষণ", "বেশির ভাগ ওষুধ মূলত ক্ষুদ্রান্ত্রের দেয়াল পেরিয়ে রক্তে যায়।"), ("প্রথমে যকৃতে", "পোর্টাল শিরা ওষুধকে যকৃতে নেয়; কিছু অংশ এখানে বিপাক হতে পারে।"),
          ("সারা শরীরে", "বাকি ওষুধ রক্তপ্রবাহে মিশে কাজের জায়গায় পৌঁছায়।")] if bn else
         [("Swallow", "The tablet travels down the food pipe to the stomach."), ("Break up and dissolve", "Many tablets break apart and start dissolving in fluid."),
          ("Absorption", "Most medicines cross mainly through the small intestine wall."), ("Liver first", "The portal vein carries the drug to the liver; some may be metabolised here."),
          ("Around the body", "The rest enters the general circulation and reaches where it acts.")])
    fs = 25 if not bn else 27
    svg = f'''<svg viewBox="0 0 700 700" width="640" height="640" style="flex:none">
      <path d="M300 30 Q300 10 320 10 Q340 10 340 30 L338 150" fill="none" stroke="#e6a191" stroke-width="22" stroke-linecap="round"/>
      <path d="M338 150 C430 140 470 220 430 290 C400 340 300 330 270 290 C250 260 280 200 338 150Z" fill="#f4a99a" stroke="#d9806c" stroke-width="4"/>
      <path d="M290 320 C200 340 190 400 260 410 C340 420 420 400 400 450 C380 500 250 470 220 520 C200 560 290 590 360 570 C430 550 470 600 420 630" fill="none" stroke="#f0a090" stroke-width="30" stroke-linecap="round"/>
      <path d="M290 320 C200 340 190 400 260 410 C340 420 420 400 400 450 C380 500 250 470 220 520 C200 560 290 590 360 570 C430 550 470 600 420 630" fill="none" stroke="#f9cbbf" stroke-width="12" stroke-linecap="round"/>
      <path d="M120 200 C80 170 120 120 190 130 C250 140 270 190 240 230 C210 260 150 240 120 200Z" fill="#9c5a4a" stroke="#7a4134" stroke-width="4"/>
      <path d="M300 470 C240 430 210 330 200 240" fill="none" stroke="#6a7fd0" stroke-width="10" stroke-dasharray="4 0"/>{arrow(205,300,200,245,"#6a7fd0",6)}
      <path d="M150 140 C140 90 160 60 220 60" fill="none" stroke="#d94b45" stroke-width="10"/>{arrow(190,62,230,60,"#d94b45",6)}
      <g transform="translate(520,70)"><path d="M0 18 C-22 -8 -50 10 -30 34 L0 62 L30 34 C50 10 22 -8 0 18Z" fill="#d94b45"/></g>
      {tablet(320,35,.45)}{mol(300,440,7)}{mol(330,500,7)}{mol(260,520,7)}{mol(210,190,6)}{mol(170,200,6)}
      <g class="lbl" font-size="{fs}">
        <text x="360" y="40">① {L[0]}</text><text x="450" y="230">② {L[1]}</text><text x="455" y="405">③ {L[2]}</text>
        <text x="10" y="390" fill="#4256a8">④ {L[3]}</text><text x="20" y="285" fill="#7a4134">⑤ {L[4]}</text><text x="440" y="160" fill="#b8352f">⑥ {L[5]}</text></g></svg>'''
    rows = "".join(f'<div class="card" style="display:flex;gap:16px;align-items:center;padding:12px 20px"><div class="num">{D(i+1,bn)}</div><div><p class="t" style="font-size:{25 if not bn else 28}px">{a}</p><p class="p" style="font-size:{21 if not bn else 23}px">{b}</p></div></div>' for i, (a, b) in enumerate(S))
    body = f'<p class="kick">{k}</p><h1>{t}</h1><div style="display:flex;gap:30px;margin-top:4px;align-items:flex-start">{svg}<div style="flex:1;display:flex;flex-direction:column;gap:11px;margin-top:8px">{rows}</div></div>'
    return page(lang, body, "MSD Manual; StatPearls (NCBI Bookshelf)")

# ========== 2. Three steps ==========
def steps(lang):
    bn = lang == "bn"
    k, t = ("কাছ থেকে দেখুন", "ট্যাবলেট থেকে রক্ত: তিনটি ধাপ") if bn else ("Close view", "From tablet to blood: three steps")
    S = ([("ডিসইন্টিগ্রেশন", "ট্যাবলেট পাকস্থলী-অন্ত্রের তরলে ছোট ছোট কণায় ভেঙে যায়।"), ("ডিসলিউশন", "কণাগুলো তরলে গলে যায়। দ্রবীভূত ওষুধই শোষিত হতে পারে।"), ("অ্যাবজর্পশন", "দ্রবীভূত অণু অন্ত্রের আবরণী পেরিয়ে রক্তনালিতে ঢোকে।")] if bn else
         [("Disintegration", "The tablet breaks into small particles in gut fluid."), ("Dissolution", "The particles dissolve. A drug must be in solution to be absorbed."), ("Absorption", "Dissolved molecules cross the gut lining into a blood vessel.")])
    p1 = f'{tablet(150,90,1.2)}' + "".join(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="#ffffff" stroke="#c9d4d6" stroke-width="2" transform="rotate({r},{x},{y})"/>' for x, y, s, r in [(70,170,22,20),(120,190,18,-15),(180,175,24,35),(230,195,16,10),(90,215,14,0),(200,225,20,-30),(150,230,16,45)])
    p2 = "".join(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="#ffffff" stroke="#c9d4d6" stroke-width="2" opacity=".6"/>' for x, y, s in [(80,80,16),(200,70,14),(140,120,12)]) + "".join(mol(x, y, 8) for x, y in [(70,160),(110,190),(160,150),(210,180),(250,140),(130,230),(190,225),(240,210),(90,120),(230,100)])
    p3 = (cell_row(10, 120, 3, 92, 80, True) + '<rect x="0" y="210" width="290" height="40" rx="20" fill="#e45b52"/>' + rbc(70,230) + rbc(200,232)
          + mol(60,60,8) + mol(150,40,8) + mol(240,70,8) + mol(110,160,7) + mol(205,165,7) + mol(140,232,7,"#7fe0d6") + mol(250,228,7,"#7fe0d6") + arrow(110,80,110,150,"#0f6d68",4) + arrow(205,90,205,152,"#0f6d68",4))
    pics = [p1, p2, p3]
    cards = ""
    for i, ((a, b), pic) in enumerate(zip(S, pics)):
        arr = '' if i == 2 else '<svg width="46" height="46" style="position:absolute;right:-40px;top:200px"><path d="M6 23 H36 M24 10 L38 23 L24 36" stroke="#2f8f83" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
        cards += f'<div class="card" style="flex:1;padding:22px 24px;position:relative"><div style="display:flex;gap:14px;align-items:center"><div class="num">{D(i+1,bn)}</div><p class="t" style="font-size:{31 if not bn else 33}px">{a}</p></div><svg viewBox="0 0 300 260" width="380" height="300" style="display:block;margin:10px auto">{pic}</svg><p class="p">{b}</p>{arr}</div>'
    note = ("সব ওষুধ একইভাবে চলে না: এন্টেরিক-কোটেড ও মডিফায়েড-রিলিজ ট্যাবলেট ইচ্ছাকৃতভাবে দেরিতে বা ধীরে ওষুধ ছাড়ে।" if bn else
            "Not every product behaves the same: enteric-coated and modified-release tablets release their medicine later or slowly, by design.")
    body = f'<p class="kick">{k}</p><h1>{t}</h1><div style="display:flex;gap:40px;margin-top:20px">{cards}</div><p class="p" style="margin-top:18px;font-weight:600;background:#fff5df;border:1px solid #f0d99e;border-radius:16px;padding:12px 20px">{note}</p>'
    return page(lang, body, "MSD Manual (drugs must be in solution to be absorbed); StatPearls")

# ========== 3. Zoom ==========
def zoom(lang):
    bn = lang == "bn"
    k, t = ("জুম করে দেখুন", "ক্ষুদ্রান্ত্রের ভেতরে: শোষণ কোথায় হয়") if bn else ("Zoom in", "Inside the small intestine: where absorption happens")
    C = ([("ক্ষুদ্রান্ত্রের ভাঁজ", "ভেতরের দেয়ালে অসংখ্য ভাঁজ থাকে।"), ("ভিলাস (Villus)", "আঙুলের মতো উঁচু অংশ; ভেতরে সূক্ষ্ম রক্তনালি।"), ("শোষণকারী কোষ", "কোষের মাথায় মাইক্রোভিলাই; ওষুধ কোষ পেরিয়ে রক্তে যায়।")] if bn else
         [("Folds of the small intestine", "The inner wall has many folds."), ("A villus", "A finger-like projection with tiny blood vessels inside."), ("Absorbing cells", "Microvilli on top; medicine crosses the cell into the blood.")])
    lab = (["মাইক্রোভিলাই", "অন্ত্রের ভেতর (দ্রবীভূত ওষুধ)", "কোষ", "রক্তনালি (ক্যাপিলারি)"] if bn else ["Microvilli", "Gut lumen (dissolved medicine)", "Cell", "Blood capillary"])
    p1 = ('<rect x="20" y="40" width="300" height="240" rx="120" fill="#f9cbbf" stroke="#d9806c" stroke-width="4"/><rect x="60" y="80" width="220" height="160" rx="80" fill="#fff5f2"/>'
          + "".join(f'<path d="M{70+i*22},235 q11,-40 22,0" fill="#f4a99a" stroke="#d9806c" stroke-width="2"/>' for i in range(9))
          + "".join(f'<path d="M{70+i*22},85 q11,40 22,0" fill="#f4a99a" stroke="#d9806c" stroke-width="2"/>' for i in range(9))
          + '<rect x="150" y="190" width="50" height="50" fill="none" stroke="#e0892b" stroke-width="4" stroke-dasharray="8 6"/>')
    p2 = (villus(110, 290, 240, 80) + villus(220, 290, 260, 80) + '<rect x="40" y="290" width="260" height="20" fill="#e45b52"/>' + mol(70,80,7) + mol(160,60,7) + mol(270,90,7)
          + '<rect x="185" y="40" width="70" height="60" fill="none" stroke="#e0892b" stroke-width="4" stroke-dasharray="8 6"/>')
    p3 = (cell_row(10, 110, 3, 106, 120, True) + '<rect x="0" y="240" width="330" height="56" rx="28" fill="#e45b52"/>' + rbc(70,268,1.1) + rbc(230,270,1.1)
          + mol(60,40,8) + mol(150,25,8) + mol(250,50,8) + mol(110,170,7) + mol(220,175,7) + mol(160,268,7,"#7fe0d6") + arrow(110,60,110,150,"#0f6d68",4) + arrow(220,70,220,155,"#0f6d68",4) + arrow(150,200,150,250,"#0f6d68",4)
          + f'<g class="lbl" font-size="{20 if not bn else 22}"><text x="230" y="76" fill="#a5543f">{lab[0]}</text><text x="8" y="16" fill="#0f6d68">{lab[1]}</text><text x="8" y="200" fill="#6b3f86">{lab[2]}</text><text x="190" y="322" fill="#b8352f">{lab[3]}</text></g>')
    pics = [p1, p2, p3]
    cards = ""
    for i, ((a, b), pic) in enumerate(zip(C, pics)):
        arr = '' if i == 2 else '<svg width="60" height="46" style="position:absolute;right:-50px;top:220px"><circle cx="16" cy="23" r="13" fill="none" stroke="#e0892b" stroke-width="4"/><path d="M26 32 L40 44" stroke="#e0892b" stroke-width="5" stroke-linecap="round"/><path d="M44 23 H58" stroke="#e0892b" stroke-width="4"/></svg>'
        cards += f'<div class="card" style="flex:1;padding:20px 22px;position:relative"><p class="t">{a}</p><svg viewBox="0 0 340 330" width="400" height="360" style="display:block;margin:6px auto">{pic}</svg><p class="p">{b}</p>{arr}</div>'
    note = ("ভাঁজ, ভিলাই ও মাইক্রোভিলাই মিলে শোষণের জন্য বিশাল জায়গা তৈরি করে। তাই বেশির ভাগ ওষুধ মূলত ক্ষুদ্রান্ত্রে শোষিত হয়।" if bn else
            "Folds, villi and microvilli create a very large surface area. That is why most oral medicines are absorbed mainly in the small intestine.")
    body = f'<p class="kick">{k}</p><h1 style="font-size:{46 if not bn else 48}px">{t}</h1><div style="display:flex;gap:46px;margin-top:16px">{cards}</div><p class="p" style="margin-top:14px;font-weight:600">{note}</p>'
    return page(lang, body, "StatPearls, Drug Absorption; MSD Manual")

# ========== 4. Mechanisms ==========
def mech(lang):
    bn = lang == "bn"
    k, t = ("অণুর স্তরে", "ওষুধ কীভাবে কোষের পর্দা পেরোয়") if bn else ("At the molecular level", "How medicine crosses the cell membrane")
    lum, bld = ("অন্ত্রের ভেতর", "রক্তের দিকে") if bn else ("Gut side", "Blood side")
    A = ("প্যাসিভ ডিফিউশন", "সবচেয়ে সাধারণ। বেশি ঘনত্ব থেকে কম ঘনত্বের দিকে, শক্তি লাগে না। চর্বিতে দ্রবণীয় ও আয়নহীন অণু সহজে পেরোয়।") if bn else ("Passive diffusion", "The most common way. Molecules move from high to low concentration, no energy needed. Fat-soluble, un-ionised molecules cross most easily.")
    B = ("ক্যারিয়ার বা ট্রান্সপোর্টার", "নির্দিষ্ট প্রোটিন অণুকে বহন করে। সক্রিয় পরিবহনে শক্তি লাগে এবং ঘনত্বের বিপরীতেও নিতে পারে। ক্যারিয়ার পূর্ণ হয়ে যেতে পারে।") if bn else ("Carrier or transporter", "A specific protein carries the molecule. Active transport uses energy and can work against the gradient. Carriers can become saturated.")
    E = ("কিছু পাম্প (যেমন P-glycoprotein) ওষুধকে আবার অন্ত্রে ফেরত পাঠায়, তাতে শোষণ কমতে পারে।" if bn else
         "Some pumps (for example P-glycoprotein) push drugs back into the gut, which can reduce absorption.")
    def membrane(y):
        g = ""
        for i in range(19):
            x = 20 + i * 24
            g += f'<circle cx="{x}" cy="{y}" r="9" fill="#e7a47c"/><line x1="{x-3}" y1="{y+8}" x2="{x-3}" y2="{y+40}" stroke="#e7c3a3" stroke-width="3"/><line x1="{x+3}" y1="{y+8}" x2="{x+3}" y2="{y+40}" stroke="#e7c3a3" stroke-width="3"/>'
            g += f'<circle cx="{x}" cy="{y+90}" r="9" fill="#e7a47c"/><line x1="{x-3}" y1="{y+50}" x2="{x-3}" y2="{y+82}" stroke="#e7c3a3" stroke-width="3"/><line x1="{x+3}" y1="{y+50}" x2="{x+3}" y2="{y+82}" stroke="#e7c3a3" stroke-width="3"/>'
        return g
    lb = 24 if not bn else 26
    pA = (membrane(120) + "".join(mol(x, y, 8) for x, y in [(60,40),(110,70),(170,40),(230,80),(300,45),(360,75),(420,40),(140,90),(330,95)])
          + "".join(mol(x, y, 8) for x, y in [(120,290),(320,300)]) + mol(220,165,8) + arrow(220,60,220,280,"#0f6d68",5)
          + f'<g class="lbl" font-size="{lb}"><text x="8" y="22" fill="#0f6d68">{lum}</text><text x="8" y="330" fill="#b8352f">{bld}</text></g>')
    pB = (membrane(120) + '<rect x="200" y="112" width="60" height="114" rx="20" fill="#7d6fc4"/><rect x="221" y="112" width="18" height="114" fill="#efeafc"/>'
          + "".join(mol(x, y, 8, "#e0892b") for x, y in [(80,60),(150,40),(330,50),(400,80)]) + mol(230,170,8,"#e0892b") + mol(260,300,8,"#e0892b") + mol(150,290,8,"#e0892b")
          + arrow(230,60,230,282,"#5a4bb0",5) + '<g transform="translate(330,170)"><circle r="22" fill="#f2b33d"/><path d="M-4 -12 L-10 2 L0 2 L-4 14 L10 -4 L1 -4 L5 -12Z" fill="#fff"/></g>'
          + f'<g class="lbl" font-size="{lb}"><text x="8" y="22" fill="#0f6d68">{lum}</text><text x="8" y="330" fill="#b8352f">{bld}</text></g>')
    def card(d, pic):
        return f'<div class="card" style="flex:1;padding:22px 26px"><p class="t" style="font-size:{31 if not bn else 33}px">{d[0]}</p><svg viewBox="0 0 470 340" width="560" height="330" style="display:block;margin:6px auto">{pic}</svg><p class="p">{d[1]}</p></div>'
    body = f'<p class="kick">{k}</p><h1>{t}</h1><div style="display:flex;gap:30px;margin-top:16px">{card(A,pA)}{card(B,pB)}</div><p class="p" style="margin-top:14px;font-weight:600;color:#8f2f2b">{E}</p>'
    return page(lang, body, "StatPearls, Drug Absorption; MSD Manual")

# ========== 5. First pass ==========
def firstpass(lang):
    bn = lang == "bn"
    k, t = ("বায়োঅ্যাভেইলেবিলিটি", "ফার্স্ট-পাস মেটাবলিজম: সব ওষুধ রক্তে পৌঁছায় না কেন") if bn else ("Bioavailability", "First-pass metabolism: why not all of a dose reaches the blood")
    N = (["মুখে খাওয়া ডোজ", "অন্ত্রের দেয়াল", "পোর্টাল শিরা", "যকৃৎ", "সারা শরীরের রক্তপ্রবাহ"] if bn else ["Oral dose", "Gut wall", "Portal vein", "Liver", "General circulation"])
    loss = (["কিছু শোষিত হয় না", "কিছু বিপাক হয়", "কিছু বিপাক হয়"] if bn else ["Some not absorbed", "Some metabolised", "Some metabolised"])
    fs = 22 if not bn else 24
    flow = f'''<svg viewBox="0 0 1470 330" width="1470" height="330">
      <g class="lbl" font-size="{fs}">
      <rect x="0" y="90" width="220" height="110" rx="20" fill="#ffffff" stroke="#cfe3df" stroke-width="3"/>{tablet(110,130,.7)}<text x="110" y="185" text-anchor="middle">{N[0]}</text>
      {arrow(230,145,300,145)}
      <rect x="310" y="90" width="230" height="110" rx="20" fill="#fde9e3" stroke="#f0c2b5" stroke-width="3"/>{cell_row(335,120,2,90,30,True).replace('height="30"','height="30"')}<text x="425" y="185" text-anchor="middle">{N[1]}</text>
      {arrow(550,145,620,145,"#6a7fd0")}
      <rect x="630" y="90" width="200" height="110" rx="20" fill="#eef1fb" stroke="#c9d0ee" stroke-width="3"/><path d="M660 140 H800" stroke="#6a7fd0" stroke-width="16" stroke-linecap="round"/><text x="730" y="185" text-anchor="middle" fill="#4256a8">{N[2]}</text>
      {arrow(840,145,910,145,"#6a7fd0")}
      <rect x="920" y="90" width="210" height="110" rx="20" fill="#f6ebe7" stroke="#e1c7bd" stroke-width="3"/><path d="M960 150 C940 120 980 100 1030 108 C1080 116 1095 145 1070 160 C1040 178 990 172 960 150Z" fill="#9c5a4a"/><text x="1025" y="190" text-anchor="middle" fill="#7a4134">{N[3]}</text>
      {arrow(1140,145,1210,145,"#d94b45")}
      <rect x="1220" y="90" width="245" height="110" rx="20" fill="#fdeceb" stroke="#f3c5c2" stroke-width="3"/>{rbc(1290,135)}{rbc(1340,128)}{rbc(1390,138)}<text x="1342" y="185" text-anchor="middle" fill="#b8352f">{N[4]}</text>
      {arrow(110,205,110,262,"#b8433f",4)}<text x="110" y="292" text-anchor="middle" fill="#b8433f" font-size="{fs-2}">{loss[0]}</text>
      {arrow(425,205,425,262,"#b8433f",4)}<text x="425" y="292" text-anchor="middle" fill="#b8433f" font-size="{fs-2}">{loss[1]}</text>
      {arrow(1025,205,1025,262,"#b8433f",4)}<text x="1025" y="292" text-anchor="middle" fill="#b8433f" font-size="{fs-2}">{loss[2]}</text>
      </g></svg>'''
    pts = ([("বায়োঅ্যাভেইলেবিলিটি", "যত দ্রুত ও যতটুকু সক্রিয় ওষুধ সারা শরীরের রক্তপ্রবাহে পৌঁছায়।"), ("শিরায় ইনজেকশন (IV)", "সরাসরি রক্তে যায়, তাই বায়োঅ্যাভেইলেবিলিটি ১০০%।"),
            ("জিভের নিচে (সাবলিঙ্গুয়াল)", "কিছু ওষুধ মুখের ভেতর থেকে শোষিত হয়ে প্রথমে যকৃৎ এড়িয়ে যায়, যেমন নাইট্রোগ্লিসারিন।")] if bn else
           [("Bioavailability", "How fast and how much active drug reaches the general circulation."), ("Injection into a vein (IV)", "Goes straight into the blood, so bioavailability is 100%."),
            ("Under the tongue (sublingual)", "Some medicines, such as nitroglycerin, are absorbed in the mouth and avoid the liver's first pass.")])
    cards = "".join(f'<div class="card" style="flex:1;padding:20px 24px"><p class="t" style="font-size:{27 if not bn else 30}px;color:#17656a">{a}</p><p class="p" style="margin-top:6px">{b}</p></div>' for a, b in pts)
    body = f'<p class="kick">{k}</p><h1 style="font-size:{46 if not bn else 46}px">{t}</h1><div style="margin-top:18px">{flow}</div><div style="display:flex;gap:22px;margin-top:6px">{cards}</div>'
    return page(lang, body, "StatPearls: Drug Absorption; First-Pass Effect")

# ========== 6. Routes ==========
def routes(lang):
    bn = lang == "bn"
    k, t = ("প্রয়োগের পথ", "সব পথে কি শোষণ লাগে?") if bn else ("Routes of administration", "Does every route need absorption?")
    R = ([("শিরায় ইনজেকশন (IV)", "সরাসরি রক্তে। শোষণের ধাপ নেই।", "no"), ("মাংসপেশি বা চামড়ার নিচে (IM/SC)", "ইনজেকশনের জায়গা থেকে রক্তে শোষিত হয়।", "yes"),
           ("মুখে খাওয়া", "দ্রবীভূত হয়ে অন্ত্রে শোষণ, তারপর যকৃৎ।", "yes"), ("জিভের নিচে", "মুখের ভেতরের আবরণী দিয়ে শোষণ।", "yes"),
           ("শ্বাসের মাধ্যমে (ইনহেলড)", "শ্বাসনালি ও ফুসফুসে জমা হয়; অনেকগুলো সেখানেই কাজ করে।", "part"), ("ত্বকে (টপিক্যাল / প্যাচ)", "কিছু ত্বকেই কাজ করে; প্যাচ ধীরে রক্তে পৌঁছায়।", "part")] if bn else
         [("Into a vein (IV)", "Straight into the blood. No absorption step.", "no"), ("Into muscle or under the skin (IM/SC)", "Absorbed from the injection site into the blood.", "yes"),
          ("Swallowed (oral)", "Dissolves, is absorbed in the gut, then passes the liver.", "yes"), ("Under the tongue (sublingual)", "Absorbed through the lining of the mouth.", "yes"),
          ("Inhaled", "Deposited in the airways and lungs; many act right there.", "part"), ("On the skin (topical or patch)", "Some act on the skin; patches reach the blood slowly.", "part")])
    tag = {"no": ("#1f7a57", "শোষণ লাগে না" if bn else "No absorption step"), "yes": ("#17656a", "শোষণ লাগে" if bn else "Absorption needed"), "part": ("#c27a12", "পণ্যভেদে ভিন্ন" if bn else "Depends on product")}
    icons = [
        '<path d="M10 40 L60 10" stroke="#5b6f75" stroke-width="6" stroke-linecap="round"/><rect x="40" y="2" width="44" height="18" rx="5" fill="#cfe3df" transform="rotate(-31 60 12)"/><path d="M5 52 H80" stroke="#d94b45" stroke-width="10" stroke-linecap="round"/>',
        '<path d="M15 45 L60 15" stroke="#5b6f75" stroke-width="6" stroke-linecap="round"/><rect x="45" y="5" width="40" height="18" rx="5" fill="#cfe3df" transform="rotate(-34 64 14)"/><rect x="0" y="48" width="85" height="16" rx="8" fill="#f4a99a"/>',
        tablet(42, 34, .7), '<path d="M10 40 Q42 70 74 40" fill="#f4a99a" stroke="#d9806c" stroke-width="3"/><ellipse cx="42" cy="44" rx="12" ry="6" fill="#ffffff" stroke="#c9d4d6"/>',
        '<rect x="22" y="10" width="40" height="44" rx="10" fill="#7fb7d6"/><rect x="30" y="0" width="24" height="16" rx="5" fill="#5b6f75"/><path d="M62 30 C72 30 80 24 84 18" stroke="#9fd3e8" stroke-width="5" fill="none" stroke-linecap="round"/>',
        '<rect x="8" y="16" width="70" height="40" rx="10" fill="#f2d4bd"/><rect x="22" y="24" width="42" height="24" rx="6" fill="#ffffff" stroke="#c9d4d6" stroke-width="2"/>']
    cards = ""
    for (a, b, kk), ic in zip(R, icons):
        c, tx = tag[kk]
        cards += (f'<div class="card" style="padding:26px 24px;display:flex;gap:20px;align-items:center"><svg viewBox="0 0 86 70" width="118" height="96" style="flex:none">{ic}</svg>'
                  f'<div style="flex:1"><p class="t" style="font-size:{28 if not bn else 31}px">{a}</p><p class="p" style="font-size:{23 if not bn else 25}px">{b}</p>'
                  f'<span style="display:inline-block;margin-top:8px;background:{c};color:#fff;font-weight:600;font-size:{19 if not bn else 21}px;padding:3px 12px;border-radius:999px">{tx}</span></div></div>')
    body = f'<p class="kick">{k}</p><h1>{t}</h1><div style="display:grid;grid-template-columns:1fr 1fr;gap:20px 24px;margin-top:22px">{cards}</div>'
    return page(lang, body, "StatPearls; MSD Manual")

# ========== 7. Factors ==========
def factors(lang):
    bn = lang == "bn"
    k, t = ("প্রভাবক", "কী কী বিষয় ওষুধের শোষণে প্রভাব ফেলে?") if bn else ("What changes absorption", "What can affect drug absorption?")
    F = ([("ডোজের ধরন", "দ্রবণ, ট্যাবলেট, ক্যাপসুল, এন্টেরিক-কোটেড ও মডিফায়েড-রিলিজ ভিন্নভাবে কাজ করে।"), ("খাবার", "নির্দিষ্ট ওষুধভেদে শোষণ দেরি করাতে, কমাতে বা বাড়াতে পারে।"),
          ("পেট ও অন্ত্রের অবস্থা", "বমি, ডায়রিয়া, অন্ত্রের গতি বা অস্ত্রোপচার প্রভাব ফেলতে পারে।"), ("ওষুধের বৈশিষ্ট্য", "দ্রবণীয়তা, কণার আকার, স্থিতিশীলতা ও পর্দা পেরোনোর ক্ষমতা।"),
          ("অন্য ওষুধ", "পাকস্থলীর অম্লতা বদলে, ওষুধকে বেঁধে ফেলে বা অন্ত্রের গতি বদলে।"), ("প্রয়োগের পথ", "মুখে, জিভের নিচে, ইনজেকশন, শ্বাসে বা ত্বকে আলাদা ধরন।")] if bn else
         [("Dosage form", "Solutions, tablets, capsules, enteric-coated and modified-release forms behave differently."), ("Food", "Can delay, reduce or increase absorption, depending on the medicine."),
          ("Gut conditions", "Vomiting, diarrhoea, gut movement changes or surgery can matter."), ("Drug properties", "Solubility, particle size, stability and ability to cross membranes."),
          ("Other medicines", "By changing stomach acidity, binding a drug or changing gut movement."), ("Route", "Oral, sublingual, injected, inhaled and skin routes all differ.")])
    icons = [tablet(40, 34, .6), '<path d="M10 40 Q40 70 70 40 Z" fill="#f2b33d"/><rect x="20" y="22" width="40" height="14" rx="7" fill="#d9806c"/>',
             '<path d="M20 15 C60 5 70 30 50 40 C30 50 25 65 60 62" fill="none" stroke="#f0a090" stroke-width="12" stroke-linecap="round"/>',
             mol(25, 35, 10) + mol(45, 25, 10) + mol(55, 45, 10), '<rect x="8" y="20" width="30" height="30" rx="8" fill="#ffffff" stroke="#c9d4d6" stroke-width="3"/><rect x="42" y="20" width="30" height="30" rx="15" fill="#e0892b"/>',
             '<path d="M10 35 H70 M50 15 L70 35 L50 55" stroke="#17656a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>']
    cards = "".join(f'<div class="card" style="padding:22px 24px;display:flex;flex-direction:column;gap:8px"><svg viewBox="0 0 80 70" width="96" height="84">{ic}</svg><p class="t">{a}</p><p class="p">{b}</p></div>' for (a, b), ic in zip(F, icons))
    note = "খাবারের সঙ্গে না খালি পেটে, তা প্রতিটি ওষুধের লেবেল বা ডাক্তারের নির্দেশনা দেখে মানুন।" if bn else "With food or on an empty stomach? Follow the label or your doctor for each medicine."
    body = f'<p class="kick">{k}</p><h1>{t}</h1><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;margin-top:18px">{cards}</div><p class="p" style="margin-top:14px;font-weight:600;background:#fff5df;border:1px solid #f0d99e;border-radius:16px;padding:12px 20px">{note}</p>'
    return page(lang, body, "MSD Manual; StatPearls; Edinburgh Pharmacology Education")

NAMES = {"cover": "drug-absorption-cover-16x9", "journey": "journey-of-a-swallowed-tablet-diagram", "steps": "tablet-disintegration-dissolution-absorption-steps",
         "zoom": "small-intestine-villi-microvilli-absorption-close-view", "mech": "passive-diffusion-vs-carrier-transport-cell-membrane",
         "firstpass": "first-pass-metabolism-bioavailability-diagram", "routes": "drug-absorption-by-route-of-administration", "factors": "factors-affecting-drug-absorption"}
FN = {"cover": cover, "journey": journey, "steps": steps, "zoom": zoom, "mech": mech, "firstpass": firstpass, "routes": routes, "factors": factors}
with sync_playwright() as p:
    br = p.chromium.launch()
    def shot(htm, w, h, path, fmt="webp"):
        pg = br.new_page(viewport={"width": w, "height": h}); f = H / "_abs.html"; f.write_text(htm, encoding="utf-8")
        pg.goto(f.as_uri()); pg.wait_for_timeout(450)
        over = pg.evaluate("()=>{const f=document.querySelector('.frame');if(!f)return false;const last=[...f.children].pop();return last? last.getBoundingClientRect().bottom>document.body.clientHeight-62:false}")
        im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
        im.save(path, "WEBP", quality=88, method=6) if fmt == "webp" else im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(("OVERFLOW " if over else "") + path.name)
    for key in (sys.argv[2:] or list(FN)):
        for lang in ("en", "bn"):
            shot(FN[key](lang), 1600, 900, OUT / f"{NAMES[key]}{'-bn' if lang == 'bn' else ''}.webp")
        if key == "cover":
            for lang in ("en", "bn"):
                shot(cover(lang, 1200, 630), 1200, 630, OUT / f"social-{lang}.jpg", "jpeg")
    br.close()
