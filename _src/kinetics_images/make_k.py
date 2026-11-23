#!/usr/bin/env python3
"""EN + BN article graphics for the pharmacokinetics series (Half-Life, Bioavailability, Rx vs OTC, Onset/Peak/Duration, series hub).
Universal Medical Editorial Palette; Poppins/Inter for English, Hind Siliguri for Bangla. Backgrounds in bg/ carry no text;
every word and number is drawn here so spelling is exact.
Usage: python3 make_k.py cfg_halflife [keys...]   (cfg module defines CFG, NAMES, OUT, PREFIX, RECIPE)"""
import pathlib, sys, io, importlib
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
M = importlib.import_module(sys.argv[1])
ROOT = H.parent.parent
OUT = ROOT / M.OUT; OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
TEAL, CHAR, CORAL, CREAM, SAGE, GOLD, STEEL = "#174F52", "#253238", "#E98250", "#F7F1E6", "#DCEBE7", "#D8A84E", "#526D82"
BND = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
CSS = f"""
@font-face{{font-family:Pop;src:url({U}/poppins-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Pop;src:url({U}/poppins-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:Int;src:url({U}/inter-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:Int;src:url({U}/inter-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:Int;src:url({U}/inter-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-500-normal.woff2);font-weight:500;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-latin-700-normal.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);overflow:hidden;position:relative;font-family:Int,HS,sans-serif;color:{CHAR};background:{CREAM}}}
body.bn{{font-family:HS,Int,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.veil{{position:absolute;inset:0}}
.panel{{position:absolute;left:72px;top:0;bottom:var(--fb,58px);width:var(--pw,540px);display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
.kick{{display:flex;align-items:center;gap:12px;font-size:25px;font-weight:600;letter-spacing:.14em;text-transform:uppercase}}
.kick:before{{content:"";width:40px;height:4px;border-radius:2px}}
body.bn .kick{{letter-spacing:.02em;font-size:30px;font-family:HS;font-weight:700}}
.title{{font-family:Pop,HS,sans-serif;font-weight:800;text-transform:uppercase;font-size:var(--ts,76px);line-height:1.08;letter-spacing:-.01em;margin-top:16px}}
body.bn .title{{font-family:HS;font-weight:700;text-transform:none;line-height:1.22;letter-spacing:0}}
.title em,.title i{{font-style:normal}}
.sub{{font-size:33px;line-height:1.3;margin-top:16px;font-weight:500;color:{CHAR}}}
body.bn .sub{{font-size:35px;line-height:1.42}}
.legend{{margin-top:22px;display:flex;flex-direction:column;gap:11px;width:100%}}
.li{{display:flex;gap:16px;align-items:center;background:rgba(255,255,255,.94);border-radius:14px;padding:11px 18px;border-left:6px solid var(--lc,{TEAL})}}
.badge{{flex:none;width:50px;height:50px;font-family:Pop,HS;font-weight:800;font-size:26px;display:flex;align-items:center;justify-content:center}}
body.bn .badge{{font-family:HS;font-weight:700}}
.li b{{display:block;font-family:Pop;font-weight:800;font-size:28px;line-height:1.15;color:{CHAR}}}
.li span{{display:block;font-size:23px;line-height:1.25;color:{CHAR}}}
body.bn .li b{{font-family:HS;font-weight:700;font-size:31px}}
body.bn .li span{{font-size:26px;font-weight:500}}
.card{{position:absolute;left:var(--cx,640px);top:62px;right:52px;bottom:96px;background:#fff;border-radius:22px;box-shadow:0 14px 40px rgba(37,50,56,.10)}}
.card svg{{position:absolute;inset:0;width:100%;height:100%}}
svg text{{font-family:Int,HS,sans-serif;fill:{CHAR}}}
body.bn svg text{{font-family:HS,Int,sans-serif;font-weight:500}}
svg .b{{font-family:Pop,HS;font-weight:800}} body.bn svg .b{{font-family:HS;font-weight:700}}
svg .s{{font-weight:600}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:58px;display:flex;justify-content:space-between;align-items:center;padding:0 72px;font-size:20px;color:{STEEL};background:rgba(247,241,230,.95)}}
body.bn .foot{{font-size:22px}}
.foot b{{color:{TEAL};font-weight:600}}
.ill{{position:absolute;right:24px;bottom:70px;font-size:17px;color:{CHAR};background:rgba(255,255,255,.85);padding:3px 12px;border-radius:999px}}
body.bn .ill{{font-size:18px}}
.byline{{margin-top:32px;display:inline-block;color:#fff;font-weight:600;font-size:27px;padding:12px 26px;border-radius:999px;box-shadow:0 10px 24px rgba(15,60,66,.25)}}
"""

def page(cfg, lang, w=1600, h=900):
    bn = lang == "bn"
    g = lambda k, d="": (cfg.get(k) or (d, d))[1 if bn else 0]
    kind = cfg.get("kind", "chart")
    foot_on = cfg.get("foot", True)
    src = g("src")
    foot = (f'<div class="foot"><span>{("সূত্র: " if bn else "Sources: ") + src if src else ""}</span><b>{"সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "Sayedul Abrar, Pharmacist"} · sayedulabrar.site</b></div>') if foot_on else ""
    ts = cfg.get("ts", (74, 74))[1 if bn else 0]
    sub = g("sub")
    leg = ""
    if cfg.get("legend"):
        for i, item in enumerate(cfg["legend"]):
            a, b = item[1] if bn else item[0]
            n = str(i + 1).translate(BND) if bn else str(i + 1)
            leg += f'<div class="li"><div class="badge">{n}</div><div><b>{a}</b><span>{b}</span></div></div>'
        leg = f'<div class="legend">{leg}</div>'
    byline = f'<p class="byline">{"লিখেছেন সাইয়্যেদুল আবরার, ফার্মাসিস্ট" if bn else "By Sayedul Abrar, Pharmacist"}</p>' if cfg.get("byline") else ""
    if kind == "photo":
        back = (f'<div class="bg" style="background-image:url({U}/bg/{cfg["bg"]}.webp);{cfg.get("bgcss","")}"></div>'
                f'<div class="veil" style="background:linear-gradient(90deg,{CREAM} 0%,{CREAM} {cfg.get("a",30)}%,rgba(247,241,230,.86) {cfg.get("a",30)+8}%,rgba(247,241,230,0) {cfg.get("a",30)+22}%)"></div>')
        mid = f'<div class="ill">{"AI-তৈরি প্রতীকী ছবি" if bn else "AI-generated illustration"}</div>' if cfg.get("ill", True) else ""
    else:
        back = f'<div class="bg" style="background:radial-gradient(circle at 85% 20%,{SAGE} 0,{CREAM} 60%)"></div>'
        svg = cfg["svg"](bn)
        mid = f'<div class="card" style="--cx:{cfg.get("cx",640)}px"><svg viewBox="0 0 {w-52-cfg.get("cx",640)} {h-96-62}">{svg}</svg></div>'
    extra = (cfg.get("extra") or ("", ""))[1 if bn else 0]
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{M.RECIPE}</style></head><body class="{lang}">'
            f'{back}{mid}<div class="panel" style="--pw:{cfg.get("pw",540)}px;--ts:{ts}px;--fb:{58 if foot_on else 0}px;{cfg.get("panelcss","")}">'
            f'<p class="kick">{g("kick")}</p><h1 class="title">{g("title")}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}{leg}{byline}</div>{extra}{foot}</body></html>')

if __name__ == "__main__":
    with sync_playwright() as p:
        br = p.chromium.launch()
        def shot(htm, w, h, path, fmt="webp"):
            pg = br.new_page(viewport={"width": w, "height": h}); f = H / "_c.html"; f.write_text(htm, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(500)
            over = pg.evaluate("()=>{const p=document.querySelector('.panel');const r=p.getBoundingClientRect();return r.bottom>document.body.clientHeight-(document.querySelector('.foot')?58:0)+2||p.scrollHeight>p.clientHeight+2}")
            im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
            im.save(path, "WEBP", quality=86, method=6) if fmt == "webp" else im.save(path, "JPEG", quality=86, optimize=True, progressive=True)
            print(("OVERFLOW " if over else "") + path.name, f"{path.stat().st_size//1024} KB")
        for key in (sys.argv[2:] or list(M.CFG)):
            for lang in ("en", "bn"):
                shot(page(M.CFG[key], lang), 1600, 900, OUT / f"{M.NAMES[key]}{'-bn' if lang == 'bn' else ''}.webp")
            if key == "cover":
                for lang in ("en", "bn"):
                    c = dict(M.CFG["cover"]); c.update(M.SOCIAL)
                    shot(page(c, lang, 1200, 630), 1200, 630, OUT / f"{M.PREFIX}-social-{lang}.jpg", "jpeg")
        (H / "_c.html").unlink(missing_ok=True)
        br.close()
