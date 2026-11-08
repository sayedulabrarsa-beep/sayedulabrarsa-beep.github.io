#!/usr/bin/env python3
"""Restyles /brands/malifa/ in the cabinet / drawer theme (idempotent)."""
import re, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "brands" / "malifa" / "index.html"
s = P.read_text(encoding="utf-8")
if "mf-hero" in s:
    raise SystemExit("already converted")

# 1) hero: replace the plain banner with a shelf showcase
m = re.search(r'<div class="product-brand-banner">(<img[^>]*>)<span class="product-brand-kicker">.*?</div>', s, re.S)
logo = m.group(1)
hero = f'''<div class="mf-hero"><div class="mf-shelf" aria-hidden="false"><div class="mf-niche"><i class="mf-led"></i><img src="/assets/img/products/malifa-30-capsule-box.webp" alt="Malifa 30 (ferric maltol 30 mg) capsule carton and blister strip by Navana Pharmaceuticals" width="692" height="403" decoding="async"><i class="mf-shadow"></i></div><div class="mf-board"></div><div class="mf-plate"><b>Malifa 30</b><small>Ferric maltol 30 mg · Capsule</small></div></div>
<div class="mf-copy"><span class="product-brand-kicker">Brand portfolio · previous experience</span><h2>Malifa 30</h2><p>An oral iron preparation I worked on as a Brand Executive at Navana Pharmaceuticals PLC, alongside the NSAIDs and Vitamins &amp; Minerals portfolios.</p><ul class="mf-chips"><li>Ferric maltol 30 mg</li><li>30 mg twice daily</li><li>6 × 10 capsules</li><li>Navana Pharmaceuticals</li></ul>{logo}
<div class="mf-actions"><button type="button" class="mf-all" id="mdr-all" aria-pressed="false">Open all drawers</button><a class="mf-back" href="/portfolio/#cabinet">← Back to the portfolio cabinet</a></div></div></div>'''
s = s.replace(m.group(0), hero, 1)

# 2) every section after the hero becomes a drawer
a = s.index('<h2 class="sec-h">Product snapshot</h2>')
b = s.index('<p class="medical-note-src">')
body = s[a:b]
parts = re.findall(r'<h2 class="sec-h">(.*?)</h2>(.*?)(?=<h2 class="sec-h">|$)', body, re.S)
out = []
for n, (t, c) in enumerate(parts):
    op = " open" if n == 0 else ""
    out.append(f'<details class="mdr"{op}><summary><span class="mdr-no">{n+1:02d}</span><span class="mdr-t">{t}</span><span class="mdr-pull" aria-hidden="true"><i></i></span></summary><div class="mdr-b">{c}</div></details>')
s = s[:a] + '<div class="mdr-wrap">' + "".join(out) + '</div>' + s[b:]

# 3) actions + assets
s = s.replace('<a class="btn secondary" href="/experience/">Back to experience</a>',
              '<a class="btn secondary" href="/portfolio/#cabinet">Back to portfolio cabinet</a><a class="btn secondary" href="/experience/">Back to experience</a>')
s = s.replace('<script src="/assets/site.js?v=nd2-20261103" defer></script>',
              '<script src="/assets/site.js?v=nd2-20261103" defer></script>\n<script src="/assets/drawers.js?v=pc2-20261108" defer></script>')
s = re.sub(r'/assets/style\.css\?v=[^"]*', '/assets/style.css?v=pc2-20261108', s)
P.write_text(s, encoding="utf-8")
print("ok", len(parts), "drawers")
