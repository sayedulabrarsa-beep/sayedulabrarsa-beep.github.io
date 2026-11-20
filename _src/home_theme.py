"""Generate assets/home-theme.css, the homepage-only colour theme.

Usage (from the repo root, with the site served on localhost:8765):
  python3 -m http.server 8765 &
  python3 _src/home_theme.py . assets/home-theme.css
Needs tinycss2 and playwright. Hand-tuned rules live in _src/data/home-theme-tuning.css.

Reads the stylesheets the homepage loads (in order), keeps only rules whose
selectors match something on the homepage, and re-emits the colour
declarations with the palette transform applied.
"""
import asyncio, colorsys, re, sys
import tinycss2
from playwright.async_api import async_playwright

ROOT = sys.argv[1]
OUT = sys.argv[2]
FILES = ["style.css", "stacks.css", "nav-pill.css", "home-motion.css", "site-polish.css"]

# Brand colours that must never change (social icons etc.)
KEEP = {"0a66c2", "1877f2", "25d366", "c13584", "ffffff", "000000"}

def hsl(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, s, l

def tohex(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s)))
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

NAVY_H, GOLD_H, MIST_H = 218, 38, 214

def transform(hex6):
    hex6 = hex6.lower()
    if hex6 in KEEP:
        return None
    h, s, l = hsl(hex6)
    blue = 195 <= h <= 265
    if blue:
        return None
    # greens / teals -> navy family
    if 120 <= h < 195 and s > 0.22:
        if l > 0.78:
            return tohex(MIST_H, min(s, 0.35), l)
        return tohex(NAVY_H, 0.52, l * 0.86)
    # yellow highlights (sticky note) -> soft gold
    if 40 <= h <= 58 and s > 0.6 and l > 0.55:
        return tohex(40, 0.72, max(l, 0.68))
    # coral / rust / orange -> gold family
    if (h < 45 or h >= 340) and s > 0.42 and 0.25 < l <= 0.74:
        return tohex(GOLD_H, 0.6, l * 0.8)
    # warm or greenish light tints (cream, peach, beige borders) -> cool mist
    if l > 0.72 and s > 0.04:
        return tohex(MIST_H, min(s, 0.4) * 0.75, l)
    # dark inks -> navy ink
    if l < 0.3 and s < 0.5:
        return tohex(222, 0.42, l)
    # muted grey-greens / warm greys -> slate
    if s < 0.25 and 0.3 <= l <= 0.72:
        return tohex(222, 0.13, l)
    return None

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGBA = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*[\d.]+\s*)?\)")

def remap(value):
    changed = False
    def hx(m):
        nonlocal changed
        v = m.group(1)
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        t = transform(v)
        if t:
            changed = True
            return t
        return m.group(0)
    def rg(m):
        nonlocal changed
        v = "%02x%02x%02x" % tuple(int(m.group(i)) for i in (1, 2, 3))
        t = transform(v)
        if not t:
            return m.group(0)
        changed = True
        r, g, b = (int(t[i:i + 2], 16) for i in (1, 3, 5))
        a = m.group(4)
        return "rgba(%d,%d,%d%s)" % (r, g, b, a.replace(" ", "")) if a else "rgb(%d,%d,%d)" % (r, g, b)
    out = HEX.sub(hx, value)
    out = RGBA.sub(rg, out)
    return out, changed

def strip_pseudo(sel):
    s = re.sub(r"::?[a-zA-Z-]+(\([^)]*\))?", "", sel)
    return s.strip() or "*"

def walk(rules, ctx, acc):
    for r in rules:
        if r.type == "qualified-rule":
            sel = tinycss2.serialize(r.prelude).strip()
            decls = tinycss2.parse_declaration_list(r.content, skip_whitespace=True, skip_comments=True)
            out = []
            for d in decls:
                if d.type != "declaration":
                    continue
                val = tinycss2.serialize(d.value).strip()
                new, ch = remap(val)
                if ch:
                    out.append("%s:%s%s" % (d.name, new, " !important" if d.important else ""))
            if out:
                acc.append((ctx, sel, out))
        elif r.type == "at-rule" and r.content is not None and r.lower_at_keyword in ("media", "supports"):
            pre = "@%s %s" % (r.lower_at_keyword, tinycss2.serialize(r.prelude).strip())
            walk(tinycss2.parse_rule_list(r.content, skip_whitespace=True, skip_comments=True), ctx + [pre], acc)

async def matching(selectors):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page()
        await pg.goto("http://localhost:8765/", wait_until="networkidle")
        res = await pg.evaluate("""(sels)=>sels.map(s=>{try{return !!document.querySelector(s)}catch(e){return true}})""", selectors)
        await b.close()
        return res

def main():
    acc = []
    for f in FILES:
        css = open(f"{ROOT}/assets/{f}", encoding="utf-8").read()
        walk(tinycss2.parse_stylesheet(css, skip_whitespace=True, skip_comments=True), [], acc)
    parts = []
    for ctx, sel, out in acc:
        parts.append([strip_pseudo(s) for s in sel.split(",")])
    flat = sorted({s for p in parts for s in p})
    ok = dict(zip(flat, asyncio.run(matching(flat))))
    lines = ["/* Homepage colour theme: navy, gold and mist. Generated; loaded only on the homepage. */"]
    kept = 0
    for (ctx, sel, out), p in zip(acc, parts):
        sels = [s.strip() for s, ps in zip(sel.split(","), p) if ok.get(ps)]
        if not sels:
            continue
        kept += 1
        rule = "%s{%s}" % (",".join(sels), ";".join(out))
        for c in reversed(ctx):
            rule = "%s{%s}" % (c, rule)
        lines.append(rule)
    tuning = open(f"{ROOT}/_src/data/home-theme-tuning.css", encoding="utf-8").read()
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n\n" + tuning)
    print("rules kept:", kept, "of", len(acc))

main()
