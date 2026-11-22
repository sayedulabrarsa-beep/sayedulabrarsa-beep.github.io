#!/usr/bin/env python3
"""Medicine Stability Testing article: 8 figures (EN + BN) + 1200x630 share images.

Backgrounds in ./bg are the user's own AI images (text-free). Every title, label and number is drawn here in code,
so spelling and values stay exact and follow the article text.

Look (deliberately different from earlier articles): midnight ink-blue + amber + ice-cyan, glass chips,
Sora (EN headlines), JetBrains Mono (labels / values), Noto Serif Bengali (BN).
Run:  python3 _src/stability_images/make_stab.py            (writes assets/img/blog/stability/*)
"""
import pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "assets/img/blog/stability"
W, H = 1600, 900

FONTS = """
@font-face{font-family:Sora;font-weight:600;src:url(fonts/sora-latin-600-normal.woff2)}
@font-face{font-family:Sora;font-weight:700;src:url(fonts/sora-latin-700-normal.woff2)}
@font-face{font-family:Sora;font-weight:800;src:url(fonts/sora-latin-800-normal.woff2)}
@font-face{font-family:JBM;font-weight:500;src:url(fonts/jetbrains-mono-latin-500-normal.woff2)}
@font-face{font-family:JBM;font-weight:700;src:url(fonts/jetbrains-mono-latin-700-normal.woff2)}
@font-face{font-family:NSB;font-weight:600;src:url(fonts/noto-serif-bengali-bengali-600-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}
@font-face{font-family:NSB;font-weight:600;src:url(fonts/noto-serif-bengali-latin-600-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F,U+2190-21FF}
@font-face{font-family:NSB;font-weight:700;src:url(fonts/noto-serif-bengali-bengali-700-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}
@font-face{font-family:NSB;font-weight:700;src:url(fonts/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F,U+2190-21FF}
@font-face{font-family:NSB;font-weight:800;src:url(fonts/noto-serif-bengali-bengali-800-normal.woff2);unicode-range:U+0980-09FF,U+200C-200D,U+0964-0965}
@font-face{font-family:NSB;font-weight:800;src:url(fonts/noto-serif-bengali-latin-700-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F,U+2190-21FF}
"""

CSS = FONTS + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:900px;overflow:hidden;background:#0B1026}
.cv{position:relative;width:1600px;height:900px;overflow:hidden;color:#fff}
.bg{position:absolute;inset:0;width:1600px;height:900px}
.veil{position:absolute;inset:0;pointer-events:none}
.abs{position:absolute}
.kick{font:700 19px/1 JBM,monospace;letter-spacing:.2em;color:#7FE7FF;text-transform:uppercase;display:flex;align-items:center;gap:14px}
.kick:before{content:"";width:34px;height:3px;background:#FFB347;border-radius:2px;box-shadow:0 0 12px #FFB347}
.hd{font:800 58px/1.08 Sora,sans-serif;letter-spacing:-.015em;color:#fff;text-shadow:0 2px 24px rgba(5,9,28,.9)}
.hd em{font-style:normal;color:#FFB347;text-shadow:0 0 28px rgba(255,179,71,.45),0 2px 24px rgba(5,9,28,.9)}
.sub{font:600 24px/1.4 Sora,sans-serif;color:#C9D8F5;text-shadow:0 2px 16px rgba(5,9,28,.95)}
.chip{position:absolute;display:flex;align-items:center;gap:12px;padding:11px 18px 11px 14px;border-radius:14px;
  background:linear-gradient(135deg,rgba(18,34,82,.78),rgba(10,20,56,.72));border:1.5px solid rgba(127,231,255,.55);
  box-shadow:0 8px 28px rgba(2,6,22,.55),inset 0 1px 0 rgba(255,255,255,.18);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px)}
.chip.am{border-color:rgba(255,179,71,.7)}
.chip b{font:700 22px/1.15 Sora,sans-serif;color:#fff}
.chip small{display:block;font:500 16px/1.3 JBM,monospace;color:#9FD9F0;margin-top:4px;letter-spacing:.01em}
.chip .t{display:block}
.num{flex:none;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#FFB347;color:#0B1026;
  font:800 18px/1 Sora,sans-serif;box-shadow:0 0 14px rgba(255,179,71,.6)}
.dot{flex:none;width:14px;height:14px;border-radius:50%;background:#FFB347;box-shadow:0 0 12px #FFB347}
.dot.cy{background:#7FE7FF;box-shadow:0 0 12px #7FE7FF}
.dot.wh{background:#EAF3FF;box-shadow:0 0 10px #EAF3FF}
.lab{position:absolute;display:flex;align-items:center;justify-content:center;gap:10px;padding:9px 12px;border-radius:12px;text-align:center;
  background:linear-gradient(135deg,rgba(18,34,82,.8),rgba(10,20,56,.74));border:1.5px solid rgba(127,231,255,.5);
  box-shadow:0 8px 24px rgba(2,6,22,.55);backdrop-filter:blur(6px);font:700 19px/1.2 Sora,sans-serif;color:#fff}
.note{position:absolute;font:500 15.5px/1.45 JBM,monospace;color:#9FB6DC;letter-spacing:.01em;text-shadow:0 1px 8px rgba(3,7,24,.95)}
.panel{position:absolute;padding:18px 22px;border-radius:16px;background:linear-gradient(135deg,rgba(18,34,82,.78),rgba(10,20,56,.72));
  border:1.5px solid rgba(255,179,71,.6);box-shadow:0 8px 28px rgba(2,6,22,.55);backdrop-filter:blur(7px)}
.panel p{font:500 16.5px/1.5 JBM,monospace;color:#D5E4FF}
.panel p b{color:#FFB347;font-weight:700}
.by{position:absolute;display:flex;align-items:center;gap:12px;padding:10px 20px;border-radius:999px;background:rgba(255,179,71,.14);
  border:1.5px solid rgba(255,179,71,.7);font:600 20px/1 Sora,sans-serif;color:#FFE2B3}
.by i{width:10px;height:10px;border-radius:50%;background:#FFB347;box-shadow:0 0 10px #FFB347}
.mark{position:absolute;right:26px;bottom:20px;font:500 14px/1 JBM,monospace;letter-spacing:.14em;color:rgba(200,220,255,.62);text-shadow:0 1px 6px rgba(3,7,24,.9)}
svg.ln{position:absolute;inset:0;width:1600px;height:900px;pointer-events:none;overflow:visible}
body.bn .hd{font-family:NSB,serif;font-weight:800;line-height:1.22;letter-spacing:0}
body.bn .sub,body.bn .chip b,body.bn .lab,body.bn .by{font-family:NSB,serif}
body.bn .sub{font-weight:600}
body.bn .chip b{font-weight:700;font-size:22px;line-height:1.3}
body.bn .lab{font-weight:700;font-size:20px}
body.bn .by{font-weight:600}
body.bn .num{font-family:NSB,serif}
body.bn .kick{font-family:JBM,NSB,serif;font-size:22px;letter-spacing:0;font-weight:700}
body.bn .note{font-family:JBM,NSB,serif;font-size:18px;letter-spacing:0;font-weight:600}
body.bn .panel p{font-family:JBM,NSB,serif;font-size:18px;line-height:1.55;font-weight:600}
body.bn .chip small{font-family:JBM,NSB,serif;font-size:17px;font-weight:600}
"""

# --------------------------------------------------------------------------- text (EN / BN)
T = {
 "cover": {
  "en": dict(kick="Pharmaceutical quality", h="Medicine <em>Stability</em> Testing", sub="How companies establish shelf life",
             chips=["Temperature", "Humidity", "Light", "Time"], by="By Sayedul Abrar · Pharmacist"),
  "bn": dict(kick="ফার্মাসিউটিক্যাল কোয়ালিটি", h="ওষুধের <em>স্থায়িত্ব</em> পরীক্ষা", sub="মেয়াদ কীভাবে নির্ধারিত হয়",
             chips=["তাপমাত্রা", "আর্দ্রতা", "আলো", "সময়"], by="সাইয়্যেদুল আবরার · ফার্মাসিস্ট")},
 "tracks": {
  "en": dict(kick="Study design", h="Three studies,<br><em>three questions</em>",
             lanes=[("Accelerated", "40°C / 75% RH"), ("Intermediate", "30°C / 65% RH"), ("Long-term", "25°C / 60% RH or<br>30°C / 65% RH")],
             note="Illustrative ICH Q1A(R2) general-case conditions."),
  "bn": dict(kick="Study design", h="তিন ধরনের study,<br><em>তিনটি প্রশ্ন</em>",
             lanes=[("Accelerated", "40°C / 75% RH"), ("Intermediate", "30°C / 65% RH"), ("Long-term", "25°C / 60% RH অথবা<br>30°C / 65% RH")],
             note="ICH Q1A(R2)-এর সাধারণ উদাহরণ; পণ্যভেদে ভিন্ন হতে পারে।")},
 "lab": {
  "en": dict(kick="What labs test", h="Quality attributes<br><em>over time</em>",
             labs=["Physical properties", "Assay & impurities", "Dissolution", "Moisture", "pH", "Microbial limits"],
             note="The test panel depends on the dosage form and the approved specification."),
  "bn": dict(kick="Lab-এ কী পরীক্ষা হয়", h="সময়ের সঙ্গে<br><em>quality attribute</em>",
             labs=["ভৌত বৈশিষ্ট্য", "Assay ও impurity", "Dissolution", "আর্দ্রতা", "pH", "Microbial limit"],
             note="পরীক্ষার তালিকা dosage form ও অনুমোদিত specification-এর ওপর নির্ভর করে।")},
 "dome": {
  "en": dict(kick="Packaging", h="Packaging is part<br>of the <em>study</em>",
             pts=["Test the proposed marketed pack", "Container, closure and desiccant matter", "Secondary packaging counts when it protects"],
             a="Heat", b="Moisture"),
  "bn": dict(kick="Packaging", h="Packaging-ও<br>study-এর <em>অংশ</em>",
             pts=["বাজারজাত করার packaging-এ study করুন", "Container, closure ও desiccant গুরুত্বপূর্ণ", "সুরক্ষা দিলে secondary packaging-ও ধরা হয়"],
             a="তাপ", b="আর্দ্রতা")},
 "climate": {
  "en": dict(kick="Bangladesh context", h="Hot and humid:<br><em>why climate matters</em>",
             chips=["Storage", "Transport", "Distribution"],
             note="<b>WHO table:</b> Bangladesh listed as [30°C/65% RH], footnote 3 (IFPMA-derived estimate, not regulator-confirmed). Check current DGDA requirements.",
             ill="Illustration only"),
  "bn": dict(kick="বাংলাদেশ প্রেক্ষাপট", h="গরম ও আর্দ্র:<br><em>জলবায়ু কেন গুরুত্বপূর্ণ</em>",
             chips=["সংরক্ষণ", "পরিবহন", "বিতরণ"],
             note="<b>WHO table:</b> বাংলাদেশের জন্য [30°C/65% RH], footnote 3 (IFPMA-ভিত্তিক অনুমান, নিয়ন্ত্রক সংস্থা নিশ্চিত করেনি)। বর্তমান DGDA নির্দেশনা দেখুন।",
             ill="শুধু চিত্র")},
 "decision": {
  "en": dict(kick="Evidence to expiry date", h="A shelf life is<br><em>a decision</em>, not a date",
             c1="Long-term data", c2="Acceptance limit", c3="Supported shelf life", c4="Printed expiry date",
             note="Illustrative trend, not real data."),
  "bn": dict(kick="Data থেকে expiry date", h="Shelf life হলো<br><em>সিদ্ধান্ত</em>, শুধু তারিখ নয়",
             c1="Long-term data", c2="গ্রহণযোগ্য সীমা", c3="Data-সমর্থিত shelf life", c4="প্যাকে ছাপা expiry date",
             note="উদাহরণ-রেখা; প্রকৃত data নয়।")},
 "storage": {
  "en": dict(kick="At home", h="Store it<br><em>as the pack says</em>",
             tips=["Keep tablets in the original pack", "Choose a cool, dry place", "Follow the storage line on the label"],
             s1="Avoid heat and direct sun", s2="Avoid damp rooms"),
  "bn": dict(kick="বাড়িতে", h="প্যাকে যেভাবে লেখা,<br><em>সেভাবেই রাখুন</em>",
             tips=["ট্যাবলেট মূল প্যাকেই রাখুন", "ঠান্ডা ও শুকনো জায়গা বেছে নিন", "লেবেলের storage নির্দেশনা মানুন"],
             s1="গরম ও সরাসরি রোদ এড়ান", s2="স্যাঁতসেঁতে ঘর এড়ান")},
 "key": {
  "en": dict(kick="Key takeaways", h="Five things<br>to <em>remember</em>",
             labs=["Temperature", "Humidity", "Time", "Packaging", "Evidence"]),
  "bn": dict(kick="মূল কথা", h="পাঁচটি বিষয়<br>মনে <em>রাখুন</em>",
             labs=["তাপমাত্রা", "আর্দ্রতা", "সময়", "Packaging", "প্রমাণ"])},
}


def block(x, y, w, kick, h, sub=None, hs=None):
    st = f"font-size:{hs}px;" if hs else ""
    s = f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px"><div class="kick">{kick}</div>'
    s += f'<div class="hd" style="margin-top:22px;{st}">{h}</div>'
    if sub:
        s += f'<div class="sub" style="margin-top:16px">{sub}</div>'
    return s + "</div>"


def chip(x, y, w, title, small=None, kind="dot", cls=""):
    lead = '<span class="dot"></span>' if kind == "dot" else (f'<span class="num">{kind}</span>' if kind else "")
    sm = f"<small>{small}</small>" if small else ""
    return f'<div class="chip {cls}" style="left:{x}px;top:{y}px;width:{w}px">{lead}<span class="t"><b>{title}</b>{sm}</span></div>'


def lab(cx, y, w, text, n=None):
    nn = f'<span class="num" style="width:30px;height:30px;font-size:16px">{n}</span>' if n else ""
    return f'<div class="lab" style="left:{cx - w // 2}px;top:{y}px;width:{w}px">{nn}<span>{text}</span></div>'


def veil(css):
    return f'<div class="veil" style="background:{css}"></div>'


L = "linear-gradient(90deg,rgba(6,11,32,.90) 0%,rgba(6,11,32,.72) 26%,rgba(6,11,32,0) 52%)"
TOPV = "linear-gradient(180deg,rgba(6,11,32,.82) 0%,rgba(6,11,32,.45) 22%,rgba(6,11,32,0) 40%)"
BOT = "linear-gradient(0deg,rgba(6,11,32,.78) 0%,rgba(6,11,32,.35) 10%,rgba(6,11,32,0) 20%)"


def build(key, lang, social=False):
    t = T[key][lang]
    v = ""   # veil
    b = ""   # blocks
    if key == "cover":
        v = veil(L)
        hs = 80 if social else 66
        b += block(64, 150 if not social else 120, 640, t["kick"], t["h"], t["sub"], hs)
        yy = 440 if not social else 500
        for i, c in enumerate(t["chips"]):
            b += chip(64 + (i % 2) * 215, yy + (i // 2) * 78, 200, c, kind="")
        b += f'<div class="by" style="left:64px;top:{yy + 170}px"><i></i>{t["by"]}</div>'
    elif key == "tracks":
        v = veil(TOPV + "," + L.replace(".90", ".55").replace(".72", ".4"))
        b += block(60, 42, 560, t["kick"], t["h"], None, 50)
        pos = [(48, 395, "am", "#FFB347", (420, 470)), (48, 585, "", "#EAF3FF", (640, 620)), (48, 745, "", "#7FE7FF", (925, 745))]
        svg = ""
        for (x, y, cls, col, tip), (nm, cond) in zip(pos, t["lanes"]):
            kind = "dot"
            dotcls = {"#FFB347": "", "#EAF3FF": "wh", "#7FE7FF": "cy"}[col]
            b += f'<div class="chip {"am" if cls else ""}" style="left:{x}px;top:{y}px;width:360px"><span class="dot {dotcls}"></span><span class="t"><b>{nm}</b><small>{cond}</small></span></div>'
            svg += f'<line x1="{x + 360}" y1="{y + 38}" x2="{tip[0]}" y2="{tip[1]}" stroke="{col}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round" opacity=".85"/>'
        b += f'<svg class="ln">{svg}</svg>'
        b += f'<div class="note" style="left:48px;top:858px">{t["note"]}</div>'
    elif key == "lab":
        v = veil(TOPV + "," + BOT)
        b += block(60, 40, 600, t["kick"], t["h"], None, 46)
        xs = [234, 459, 713, 976, 1182, 1416]
        for i, (cx, tx) in enumerate(zip(xs, t["labs"])):
            b += lab(cx, 718, 194, tx, i + 1)
        b += f'<div class="note" style="left:0;width:1600px;text-align:center;top:850px">{t["note"]}</div>'
    elif key == "dome":
        v = veil(L)
        b += block(52, 150, 500, t["kick"], t["h"], None, 52)
        for i, p in enumerate(t["pts"]):
            b += chip(52, 410 + i * 92, 470, p, kind=str(i + 1), cls="am" if i == 0 else "")
        b += f'<div class="chip am" style="left:895px;top:96px;padding:9px 16px"><span class="dot"></span><span class="t"><b style="font-size:20px">{t["a"]}</b></span></div>'
        b += f'<div class="chip" style="left:1010px;top:96px;padding:9px 16px"><span class="dot cy"></span><span class="t"><b style="font-size:20px">{t["b"]}</b></span></div>'
    elif key == "climate":
        v = veil(L)
        b += block(52, 90, 470, t["kick"], t["h"], None, 52)
        for i, c in enumerate(t["chips"]):
            b += chip(52, 372 + i * 70, 250, c, kind="", cls="am" if i == 0 else "")
        b += f'<div class="panel" style="left:52px;top:612px;width:470px"><p>{t["note"]}</p></div>'
        b += f'<div class="note" style="left:52px;top:858px">{t["ill"]}</div>'
    elif key == "decision":
        v = veil("radial-gradient(ellipse 52% 40% at 80% 14%,rgba(6,11,32,.72),rgba(6,11,32,0) 100%)," + BOT)
        b += block(1010, 44, 560, t["kick"], t["h"], None, 46)
        b += chip(385, 128, 270, t["c1"], kind="dot", cls="")
        b += chip(690, 400, 270, t["c2"], kind="dot", cls="am")
        b += f'<svg class="ln"><line x1="673" y1="676" x2="673" y2="748" stroke="#FFB347" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/></svg>'
        b += chip(473, 748, 400, t["c3"], kind="dot", cls="am")
        b += chip(1262, 748, 290, t["c4"], kind="dot", cls="am")
        b += f'<div class="note" style="left:48px;top:858px">{t["note"]}</div>'
    elif key == "storage":
        v = veil(L)
        b += block(52, 56, 470, t["kick"], t["h"], None, 52)
        for i, p in enumerate(t["tips"]):
            b += chip(52, 330 + i * 92, 460, p, kind=str(i + 1), cls="am" if i == 0 else "")
        b += f'<div class="lab" style="left:1262px;top:296px;width:300px;border-color:rgba(255,179,71,.75)"><span class="dot"></span><span>{t["s1"]}</span></div>'
        b += f'<div class="lab" style="left:1262px;top:636px;width:300px;border-color:rgba(255,179,71,.75)"><span class="dot"></span><span>{t["s2"]}</span></div>'
    elif key == "key":
        v = veil(TOPV + "," + BOT)
        b += block(52, 44, 700, t["kick"], t["h"], None, 54)
        xs = [459, 660, 871, 1086, 1311]
        for i, (cx, tx) in enumerate(zip(xs, t["labs"])):
            b += lab(cx, 838, 190, tx, i + 1)
    mark = '<div class="mark"%s>SAYEDULABRAR.SITE</div>' % (' style="top:22px;bottom:auto"' if key == "key" else "")
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{lang}"><div class="cv"><img class="bg" src="bg/{key}.webp">{v}{b}{mark}</div></body></html>')


NAMES = {
    "cover": "stability-cover", "tracks": "stability-study-design", "lab": "stability-quality-tests",
    "dome": "stability-packaging", "climate": "stability-bangladesh-climate", "decision": "stability-shelf-life",
    "storage": "stability-patient-storage", "key": "stability-key-takeaways",
}


def main(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = HERE / "_render.html"
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        jobs = [(k, l, False) for k in NAMES for l in ("en", "bn")] + [("cover", l, True) for l in ("en", "bn")]
        for key, lang, social in jobs:
            if only and key not in only:
                continue
            tmp.write_text(build(key, lang, social), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(350)
            png = HERE / "_shot.png"
            pg.screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            if social:
                im = im.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
                im.save(OUT / f"stability-social-{lang}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
            else:
                suffix = "" if lang == "en" else "-bn"
                im.save(OUT / f"{NAMES[key]}{suffix}.webp", "WEBP", quality=88, method=6)
            print("ok", key, lang, "social" if social else "")
        br.close()
    for f in (tmp, HERE / "_shot.png"):
        if f.exists():
            f.unlink()


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
