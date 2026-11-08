#!/usr/bin/env python3
"""Rebuilds the 4 brand pages in the cabinet / drawer theme from _src/brand_orig/*.html,
blending the existing manufacturer-listed data with the pasted monographs (see portfolio_cabinet.py).
Run: python3 _src/brand_pages.py
"""
import re, sys, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_src"))
import portfolio_cabinet as C
e = html.escape
TOK = "pc3-20261108"

PAGES = {
 "finix": dict(ac="#1d9a5b", imgs=[("finix-10-capsule-box", C.P[0]["alt"]), ("finix-20-capsule-box", C.P[1]["alt"]), ("finix-20-tablet-box", C.P[2]["alt"])],
   plate=("Finix", "Rabeprazole sodium BP · 10 mg and 20 mg"),
   kicker="Brand portfolio · current", h="Finix",
   p="Rabeprazole sodium in three presentations from Opsonin Pharma: the 10 mg sprinkle capsule, the 20 mg capsule and the 20 mg enteric-coated tablet. Part of the Gastro portfolio I work on as Product Executive.",
   chips=["Rabeprazole sodium BP", "10 mg · 20 mg", "Capsule & tablet", "Opsonin Pharma"], prod=C.P[2]),
 "finix-mups": dict(ac="#2b6cc4", imgs=[("finix-mups-20-tablet-box", C.P[3]["alt"])],
   plate=("Finix MUPS 20", "Rabeprazole sodium BP 20 mg · MUPS tablet"),
   kicker="Brand portfolio · current", h="Finix MUPS 20",
   p="A rabeprazole sodium 20 mg enteric-coated Multiple-Unit Pellet System tablet from Opsonin Pharma, part of the Finix range in the Gastro portfolio I work on.",
   chips=["Rabeprazole 20 mg", "MUPS tablet", "Alu-Alu pack", "Opsonin Pharma"], prod=C.P[3]),
 "finix-hp": dict(ac="#7a3fb0", imgs=[("finix-hp-pack-box", C.HP["alt"])],
   plate=("Finix HP", "Rabeprazole + amoxicillin + clarithromycin"),
   kicker="Brand portfolio · current", h="Finix HP",
   p="The Finix HP combination pack for a prescribed H. pylori eradication regimen, from Opsonin Pharma. It is a prescription-only antibiotic combination, not an everyday acidity medicine.",
   chips=["3-drug combination", "7 sachets per carton", "Prescription only", "Opsonin Pharma"], prod=None),
 "malifa": dict(ac="#d3202a", imgs=[("malifa-30-capsule-box", C.MALIFA["alt"])],
   plate=("Malifa 30", "Ferric maltol 30 mg · Capsule"),
   kicker="Brand portfolio · previous experience", h="Malifa 30",
   p="An oral iron preparation I worked on as a Brand Executive at Navana Pharmaceuticals PLC, alongside the NSAIDs and Vitamins & Minerals portfolios.",
   chips=["Ferric maltol 30 mg", "30 mg twice daily", "6 × 10 capsules", "Navana Pharmaceuticals"], prod=None),
}
SIZES = {"finix-10-capsule-box": (689, 320), "finix-20-capsule-box": (900, 397), "finix-20-tablet-box": (385, 308),
         "finix-mups-20-tablet-box": (804, 673), "finix-hp-pack-box": (940, 594), "malifa-30-capsule-box": (692, 403)}

def drawer(n, title, body, open_=False):
    return (f'<details class="mdr"{" open" if open_ else ""}><summary><span class="mdr-no">{n:02d}</span>'
            f'<span class="mdr-t">{title}</span><span class="mdr-pull" aria-hidden="true"><i></i></span></summary><div class="mdr-b">{body}</div></details>')

def hero(key, cfg, logo):
    multi = len(cfg["imgs"]) > 1
    imgs = "".join(f'<img src="/assets/img/products/{n}.webp" alt="{e(a)}" width="{SIZES[n][0]}" height="{SIZES[n][1]}" decoding="async">' for n, a in cfg["imgs"])
    return f'''<div class="mf-hero" style="--ac:{cfg["ac"]}"><div class="mf-shelf"><div class="mf-niche{" is-multi" if multi else ""}"><i class="mf-led"></i>{imgs}<i class="mf-shadow"></i></div><div class="mf-board"></div><div class="mf-plate"><b>{e(cfg["plate"][0])}</b><small>{e(cfg["plate"][1])}</small></div></div>
<div class="mf-copy"><span class="product-brand-kicker">{e(cfg["kicker"])}</span><h2>{e(cfg["h"])}</h2><p>{e(cfg["p"])}</p><ul class="mf-chips">{"".join(f"<li>{e(c)}</li>" for c in cfg["chips"])}</ul>{logo}
<div class="mf-actions"><a class="mf-back-btn" href="/portfolio/#cabinet">← Back to the portfolio cabinet</a><button type="button" class="mf-all" id="mdr-all" aria-pressed="false">Open all drawers</button></div></div></div>'''

def build(key):
    cfg = PAGES[key]
    src = (ROOT / "_src" / "brand_orig" / f"{key}.html").read_text(encoding="utf-8")
    a = src.index('<div class="wrap product-info">') + len('<div class="wrap product-info">')
    z = src.index("</div></section>", a)
    info = src[a:z]
    banner = re.search(r'<div class="product-brand-banner">(<img[^>]*>)', info)
    logo = banner.group(1)
    logo = logo.replace(' class="brand-logo-chip"', "")
    first = info.index('<h2 class="sec-h">')
    pre = info[:first]
    facts = re.search(r'<div class="drug-facts-grid">.*?</div></div>(?=\s*$|\s*<h2)', pre, re.S)
    facts_html = ""
    m = re.search(r'<div class="drug-facts-grid">.*', pre, re.S)
    if m: facts_html = m.group(0).strip()
    rest = info[first:]
    parts = re.findall(r'<h2 class="sec-h">(.*?)</h2>(.*?)(?=<h2 class="sec-h">|$)', rest, re.S)
    ex = {t: c.strip() for t, c in parts}

    # split FAQ part into faq list + trailing notes/actions
    faq_t = next(t for t in ex if t.startswith("Frequently"))
    fm = re.search(r'<div class="drug-faq-list">.*?</details></div>', ex[faq_t], re.S)
    faq = fm.group(0); tail = ex[faq_t].replace(fm.group(0), "", 1)
    rel_t = next((t for t in ex if t.startswith("Explore the related")), None)
    related = f'<h2 class="sec-h">{rel_t}</h2>{ex[rel_t]}' if rel_t else ""

    secs = []   # (title, html, open)
    if key == "malifa":
        table = ex["Product snapshot"].replace("</tbody>", "<tr><th>Drug class</th><td>Oral iron replacement therapy (non-salt ferric iron complex)</td></tr></tbody>")
        secs.append(("Product snapshot", table, True))
        secs += [(t, b, False) for t, b, *o in C.sec_malifa(C.MALIFA)]
        secs[1] = (secs[1][0], secs[1][1], False)
        secs.append(("Frequently asked questions", faq, False))
    elif key == "finix-hp":
        secs.append(("Product snapshot", facts_html or "", True)) if facts_html else None
        for t in ex:
            if t in (faq_t, rel_t): continue
            secs.append((t, ex[t], not secs))
        secs.append(("Frequently asked questions", faq, False))
    else:
        p = cfg["prod"]
        new = {t: b for t, b, *o in C.sec_finix(p)}
        if key == "finix":
            admin = "<ul>" + "".join(f"<li><b>{e(nm)}.</b> {e(tx)}</li>" for nm, tx in [
                ("Finix 10 sprinkle capsule", C.P[0]["admin"][0]),
                ("Finix 20 capsule", C.P[1]["admin"][0]),
                ("Finix 20 tablet", C.P[2]["admin"][0])]) + "</ul>" + C.dose_table()
        else:
            admin = C.ul(p["admin"]) + C.dose_table()
        gen = '<p class="cab-small"><b>Also described in general rabeprazole references:</b></p>' + C.ul(C.FX_IND_GEN)
        secs.append(("Product snapshot", facts_html, True))
        for t in ex:
            if t in (faq_t, rel_t): continue
            body = ex[t]
            if t.startswith("Manufacturer-listed indications"): body += gen
            if t == "How it works": body += f"<p>{e(C.FX_MOA)}</p>"
            secs.append((t, body, False))
            if t.startswith("Manufacturer-listed indications"):
                secs.append(("Dosage &amp; administration", admin, False))
            if t == "How it works":
                for k in ("Interactions", "Contraindications", "Side effects", "Precautions & warnings",
                          "Pregnancy, lactation & special populations", "Overdose & storage"):
                    secs.append((e(k), new[k], False))
        secs.append(("Frequently asked questions", faq + "".join(f"<p><b>{e(q)}</b><br>{e(a_)}</p>" for q, a_ in C.FX_FAQ), False))
    drawers = "".join(drawer(i + 1, t, b, o) for i, (t, b, o) in enumerate(secs))

    back = '<a class="btn secondary" href="/portfolio/#cabinet">← Back to the portfolio cabinet</a>'
    if 'class="product-actions">' in tail:
        tail = tail.replace('<div class="product-actions">', '<div class="product-actions">' + back, 1)
    else:
        tail += f'<div class="product-actions">{back}</div>'
    new_info = (hero(key, cfg, logo) + f'<div class="mdr-wrap" style="--ac:{cfg["ac"]}">{drawers}</div>' + tail + related)
    out = src[:a] + new_info + src[z:]
    out = out.replace("</main>", '<a class="mf-float" href="/portfolio/#cabinet" aria-label="Back to the portfolio cabinet">← Portfolio</a></main>', 1)
    out = re.sub(r'/assets/style\.css\?v=[^"]*', f'/assets/style.css?v={TOK}', out)
    if "drawers.js" not in out:
        out = re.sub(r'(<script src="/assets/site\.js[^>]*></script>)', r'\1\n<script src="/assets/drawers.js?v=%s" defer></script>' % TOK, out, 1)
    (ROOT / "brands" / key / "index.html").write_text(out, encoding="utf-8")
    print(key, len(secs), "drawers")

if __name__ == "__main__":
    for k in PAGES: build(k)
