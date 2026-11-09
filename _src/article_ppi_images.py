#!/usr/bin/env python3
"""Flat infographics for the PPI article (rendered with Playwright, saved as webp/jpg)."""
import pathlib, subprocess, json, tempfile, os
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/blog/ppi-tablets"
CSS = """
*{box-sizing:border-box;margin:0}body{font-family:Inter,'Segoe UI',Arial,sans-serif;color:#10283a;background:#eaf6f4;width:var(--w);height:var(--h);overflow:hidden;position:relative}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 85% 12%,#fff4e3 0,transparent 38%),linear-gradient(160deg,#e6f5f2,#f6fbfa 60%,#fff6ea)}
.pill{position:absolute;border-radius:999px;background:linear-gradient(90deg,#f26b1d 50%,#fff 50%);border:5px solid #fff;box-shadow:0 10px 24px rgba(14,90,99,.22)}
.title{position:absolute;left:5%;right:5%;top:4.5%;padding:24px 34px;border-radius:28px;background:#0e5a63;color:#fff;font-weight:900;font-size:62px;line-height:1.08;letter-spacing:-.02em;box-shadow:0 10px 0 #0a434a}
.title em{font-style:normal;color:#ffb36b}
.card{position:absolute;border-radius:28px;background:#fff;border:3px solid #cfe6e2;box-shadow:0 12px 26px rgba(14,90,99,.14);padding:30px 34px}
.card h3{font-size:40px;font-weight:900;margin-bottom:12px;letter-spacing:-.01em}
.card p{font-size:31px;line-height:1.32;font-weight:600;color:#274456}
.card small{display:block;margin-top:12px;font-size:23px;color:#6d8391;font-weight:600}
.g h3{color:#14803f}.o h3{color:#d9560c}.r h3{color:#c4262e}.t h3{color:#0e5a63}
.g{border-color:#bfe3cc;background:#f2fbf5}.o{border-color:#f5d2b6;background:#fff7f0}.r{border-color:#f2c2c4;background:#fff4f4}
.foot{position:absolute;left:5%;right:5%;bottom:4%;padding:18px 28px;border-radius:22px;background:#e3f1ff;border:3px solid #bcd9f2;font-size:29px;font-weight:800;color:#12365a;text-align:center}
.chip{display:inline-block;margin:6px 6px 0 0;padding:10px 20px;border-radius:999px;background:#0e5a63;color:#fff;font-size:27px;font-weight:700}
.chip.w{background:#fff;color:#0e5a63;border:3px solid #0e5a63}
.by{position:absolute;left:5%;bottom:5%;padding:12px 26px;border-radius:999px;background:#0e5a63;color:#fff;font-size:30px;font-weight:700}
"""
def clock(x, y, s):
    return f'''<svg style="position:absolute;left:{x}px;top:{y}px" width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#fff" stroke="#0e5a63" stroke-width="7"/><path d="M50 50 L50 20 A30 30 0 0 1 76 65 Z" fill="#f26b1d" opacity=".85"/><path d="M50 50V24M50 50L68 60" stroke="#10283a" stroke-width="5" stroke-linecap="round"/><circle cx="50" cy="50" r="4" fill="#10283a"/></svg>'''
def glass(x, y, s):
    return f'<svg style="position:absolute;left:{x}px;top:{y}px" width="{s}" height="{s*1.3}" viewBox="0 0 60 78"><path d="M8 6h44l-5 64a6 6 0 0 1-6 5H19a6 6 0 0 1-6-5z" fill="#dff1fb" stroke="#0e5a63" stroke-width="3.5"/><path d="M11 30h38l-2.6 40a4 4 0 0 1-4 3.6H19a4 4 0 0 1-4-3.6z" fill="#8fd0ee" opacity=".7"/></svg>'
PAGES = {}
def page(name, w, h, body): PAGES[name] = (w, h, f'<html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body><div class="bg"></div>{body}</body></html>')

W, H = 1448, 960
page("when-to-take-omeprazole-and-other-ppis-timing-and-food", W, H, f'''
<div class="title" style="font-size:58px">When to Take a <em>PPI</em></div>
<div class="card g" style="left:5%;top:21%;width:42%;height:22%;padding:24px 30px"><h3>NHS (omeprazole)</h3><p>Same time each morning. With or without food.</p></div>
<div class="card o" style="right:5%;top:21%;width:42%;height:22%;padding:24px 30px"><h3>MedlinePlus (omeprazole)</h3><p>Prescription capsules: usually once a day before a meal.</p></div>
<div class="card t" style="left:5%;top:47%;width:90%;height:27%"><h3>Rabeprazole tablets (FDA label)</h3><p>Can be taken without regard to timing of meals for most uses.</p><small>Exceptions: duodenal ulcer, after the morning meal. H. pylori triple therapy, with food.</small></div>
<div class="foot" style="bottom:4%">Your leaflet and prescriber come first. Keep the same time every day.</div>
''')
page("rabeprazole-finix-tablet-mups-and-sprinkle-how-to-take", W, H, f'''
<div class="title" style="font-size:54px">Rabeprazole Forms: <em>How to Take</em></div>
<div class="card t" style="left:4%;top:21%;width:29%;height:40%;padding:26px 26px"><h3 style="font-size:36px">Tablet</h3><p style="font-size:27px">Finix 20 tablet. Swallow whole with water. Do not chew, crush or split.</p><small>FDA label: with or without food for most uses</small></div>
<div class="card o" style="left:35.5%;top:21%;width:29%;height:40%;padding:26px 26px"><h3 style="font-size:36px">MUPS tablet</h3><p style="font-size:27px">Finix MUPS 20. Swallow whole unless the insert says otherwise.</p><small>Pellet-based enteric-coated tablet</small></div>
<div class="card g" style="right:4%;top:21%;width:29%;height:40%;padding:26px 26px"><h3 style="font-size:36px">Sprinkle 10 mg</h3><p style="font-size:27px">Open and scatter on a little soft food or liquid. Take all within 15 minutes. Do not chew the granules.</p><small>US label: dose 30 minutes before a meal</small></div>
<div class="foot">Always follow your own pack insert and prescriber.</div>
''')
page("swallow-ppi-capsule-or-tablet-whole-do-not-crush-or-chew", W, H, f'''
<div class="title" style="font-size:56px">Swallow It <em>Whole</em></div>
<div class="card g" style="left:5%;top:24%;width:56%;height:27%"><h3>Do</h3><p>Swallow with water. Follow your leaflet if it says the capsule or tablet can be opened or dissolved.</p></div>
<div class="card r" style="left:5%;top:55%;width:56%;height:21%"><h3>Do not</h3><p>Chew or crush enteric coated or gastro-resistant tablets (NHS).</p></div>
{glass(1010,300,230)}
<div class="pill" style="left:68%;top:66%;width:210px;height:78px;transform:rotate(-14deg)"></div>
<div class="foot">Trouble swallowing? Ask a pharmacist for options.</div>''')
chips = "".join(f'<span class="chip">{c}</span>' for c in ["Warfarin","Clopidogrel","Digoxin","Phenytoin","Diazepam","Famotidine","Iron supplements","St John’s wort","Ketoconazole","Itraconazole","Atazanavir","Nelfinavir","High-dose methotrexate"])
page("ppi-medicine-interactions-warfarin-clopidogrel-digoxin-iron", W, H, f'''
<div class="title" style="font-size:54px">Tell Your Pharmacist <em>Everything</em> You Take</div>
<div class="card t" style="left:5%;top:25%;width:90%;height:48%"><h3>Named in the NHS, MedlinePlus and a UK rabeprazole leaflet</h3><div style="margin-top:12px">{chips}</div><small>Not a complete list. Different PPIs have different interactions.</small></div>
<div class="foot">Ask how to space or adjust them. Do not guess.</div>''')
page("ppi-long-term-use-risks-and-when-to-see-a-doctor", W, H, f'''
<div class="title" style="font-size:54px">See a Doctor <em>Promptly</em> If</div>
<div class="card r" style="left:5%;top:23%;width:90%;height:52%"><p style="font-size:30px">• Trouble swallowing, vomiting (especially bloody)<br>• Black or bloody stools, stomach pain<br>• Chest or shoulder pain, shortness of breath<br>• Unexplained weight loss<br>• Severe watery or bloody diarrhoea with fever<br>• Heartburn for 3 months or more, or no better after 14 days</p></div>
<div class="foot">Long-term use (a year or more) needs regular review.</div>''')
page("missed-dose-and-too-much-ppi-what-to-do", W, H, f'''
<div class="title" style="font-size:54px">Missed a Dose? <em>Do This</em></div>
<div class="card g" style="left:5%;top:24%;width:42%;height:24%"><h3>Remember it</h3><p>Take it when you remember.</p></div>
<div class="card o" style="right:5%;top:24%;width:42%;height:24%"><h3>Nearly next dose?</h3><p>Skip the missed one.</p></div>
<div class="card r" style="left:5%;top:52%;width:90%;height:15%;padding:22px 34px"><p style="text-align:center">Never take two doses together to make up.</p></div>
<div class="foot">Taken too much? Get medical advice and bring the packet.</div>''')
# thumbnail 1600x900
page("when-to-take-ppi-before-meals-thumbnail-16x9", 1600, 900, f'''
<div style="position:absolute;left:5%;top:9%;width:60%;padding:34px 44px;border-radius:34px;background:#0e5a63;color:#fff;box-shadow:0 12px 0 #0a434a"><div style="font-size:84px;font-weight:900;line-height:1.02;letter-spacing:-.03em">When to Take<br>a <span style="color:#ffb36b">PPI</span></div></div>
<div style="position:absolute;left:5%;top:56%;padding:16px 34px;border-radius:22px;background:#fff3dc;font-size:40px;font-weight:800;color:#8a4a0c">Before Meals &amp; Common Mistakes</div>
{clock(1040,120,340)}{glass(1330,170,170)}
<div class="pill" style="left:1010px;top:560px;width:280px;height:104px;transform:rotate(-12deg)"></div><div class="pill" style="left:1220px;top:660px;width:230px;height:86px;transform:rotate(18deg)"></div>
<div class="by">Sayedul Abrar, Pharmacist</div>''')
page("social", 1200, 630, f'''
<div style="position:absolute;left:5%;top:10%;width:64%;padding:26px 36px;border-radius:28px;background:#0e5a63;color:#fff;box-shadow:0 9px 0 #0a434a"><div style="font-size:66px;font-weight:900;line-height:1.04;letter-spacing:-.03em">When to Take a <span style="color:#ffb36b">PPI</span></div></div>
<div style="position:absolute;left:5%;top:60%;padding:12px 26px;border-radius:18px;background:#fff3dc;font-size:32px;font-weight:800;color:#8a4a0c">Before Meals &amp; Common Mistakes</div>
{clock(820,80,260)}{glass(1050,110,120)}
<div class="pill" style="left:800px;top:400px;width:210px;height:80px;transform:rotate(-12deg)"></div>
<div class="by" style="font-size:26px">Sayedul Abrar, Pharmacist</div>''')

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (w, h, html) in PAGES.items():
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(html); pg.wait_for_timeout(200)
        tmp = OUT / (name + ".png"); pg.screenshot(path=str(tmp)); pg.close()
        im = Image.open(tmp).convert("RGB")
        if name == "social":
            im.save(ROOT / "assets/img/blog/when-to-take-ppi-before-meals-social.jpg", quality=88)
        else:
            im.save(OUT / (name + ".webp"), quality=86, method=6)
        tmp.unlink()
    b.close()
print(sorted(os.listdir(OUT)))
