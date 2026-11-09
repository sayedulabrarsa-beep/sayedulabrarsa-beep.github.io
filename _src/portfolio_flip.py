#!/usr/bin/env python3
"""Portfolio page: flip-pad skills hero, handwriting verses band, portfolio-only header/footer hooks.
Run once on portfolio/index.html (idempotent via markers). python3 _src/portfolio_flip.py"""
import re, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "portfolio" / "index.html"
e = html.escape
TOK = "pf4-20261109"

# (tag, title, line)  — titles come from the Learning record and the PMD role description
PAGES = [
 ("Role", "Pharmacist", "Patient-first thinking behind every brand decision"),
 ("Role", "Product Executive", "Gastro portfolio · Opsonin Pharma Ltd."),
 ("Role", "Pharmaceutical Marketer", "Rx-led planning, campaigns and field support"),
 ("Role", "Brand Development", "Brand Executive experience · Navana Pharmaceuticals"),
 ("Specialization", "Marketing Strategy", "Five-course specialization, from research to capstone"),
 ("Course", "Market Research", "Market Research and Consumer Behavior"),
 ("Course", "Positioning", "What you need for a successful marketing strategy"),
 ("Course", "Marketing Mix", "Marketing Mix Fundamentals and The Marketing Plan"),
 ("Specialization", "Drug Commercialization", "Part of the Drug Development Product Management specialization"),
 ("Course", "Product Launch", "Product Management: Launching Your Product"),
 ("Course", "Product Roadmaps", "Product Management: Building a Product Roadmap"),
 ("Course", "Product Marketing", "Product Marketing Foundations and Advanced Product Marketing"),
 ("Course", "Digital Marketing", "Master Digital Marketing, content and social media"),
 ("Certificate", "Generative AI for Marketing", "Professional certificate learning path"),
 ("Course", "Sales Management", "Sales Management Foundations, strategy and coaching"),
 ("Course", "Project Management", "Budgets, schedules, communication and teams"),
 ("Role", "Campaigns & Budgets", "Promotional plans and annual budgets for assigned products"),
 ("Role", "Training & CME", "Field conferences and scientific sessions with colleagues"),
]

def hero():
    first, second = PAGES[0], PAGES[1]
    def pg(p, cls):
        return f'<div class="pf-pg {cls}"><b>{e(p[1])}</b></div>'
    data = "".join(f'<li data-h="{e(h)}"></li>' for t, h, l in PAGES)
    rings = "".join("<i></i>" for _ in range(11))
    return f'''<section class="portfolio-intro pf-hero"><div class="wrap portfolio-intro-grid">
  <div class="portfolio-intro-copy"><p class="eyebrow">Selected work · Brand strategy · Healthcare</p><h1>Sayedul Abrar’s <em>Portfolio</em></h1>
  <p class="pf-lead">Pharmaceutical product management, brand development and meaningful work in healthcare.</p>
  <div class="pf-pad" id="pf-pad" role="img" aria-label="Rotating list of roles and skills"><div class="pf-rings" aria-hidden="true">{rings}</div><div class="pf-stack">{pg(second, "pf-under")}{pg(first, "pf-top")}</div></div>
  <ul class="pf-data" hidden>{data}</ul>
  <div class="pf-cta"><a class="portfolio-cta" href="/contact/">Discuss a collaboration <span aria-hidden="true">↗</span></a><a class="pf-ghost" href="#cabinet">See the cabinet ↓</a></div></div>
  <div class="portfolio-intro-art pf-art"><span class="pf-glow" aria-hidden="true"></span><img class="pf-figure" src="/assets/img/portfolio/formal-suit-cutout.webp" alt="Sayedul Abrar in a navy double-breasted suit" width="567" height="1496"><span class="pf-ground" aria-hidden="true"></span><div class="portfolio-stamp">PHARMACIST<br>LEARNER<br>CONTRIBUTOR</div></div>
</div></section>'''

def words():
    return '''<!--PQ-START--><section class="portfolio-highlight-band pq pf-words" id="words" aria-labelledby="pwr-h"><div class="wrap"><div class="pwr-head"><p class="eyebrow">Beyond the project list</p><h2 id="pwr-h">Progress through curiosity, consistency and collaboration.</h2>
<p>Pharmacy is a promise to put people first. Behind every pack on the shelf is someone waiting for relief, a family hoping for a good recovery and a doctor who needs clear, honest information. These are the words I try to work by, written one at a time.</p></div>
<div class="pwr" id="pwr" data-src="/assets/portfolio-words.json"><div class="pwr-paper"><span class="pwr-clip" aria-hidden="true"></span>
<div class="pwr-body" aria-live="off"><p class="pwr-ar" lang="ar" dir="rtl"></p><p class="pwr-en"></p><p class="pwr-bn" lang="bn"></p><p class="pwr-ref"></p></div>
<span class="pwr-pen" aria-hidden="true"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M3 21l1.6-5.2L16.8 3.6a2 2 0 012.8 0l.8.8a2 2 0 010 2.8L8.2 19.4 3 21z" fill="#5a3d1a"/><path d="M15.5 5l3.5 3.5" stroke="#fbeed0" stroke-width="1.4"/><path d="M3 21l1.6-5.2 3.6 3.6z" fill="#e7c98a"/></svg></span></div>
<div class="pwr-ctl"><button type="button" class="pwr-prev" aria-label="Previous verse or quote">‹</button><button type="button" class="pwr-pp" aria-label="Pause writing" aria-pressed="false">Pause</button><span class="pwr-n" aria-live="polite">1 / 1</span><button type="button" class="pwr-next" aria-label="Next verse or quote">›</button></div>
<p class="pwr-note">Quran text: Uthmani script via the open quran-json package; English by Saheeh International, Bangla by Muhiuddin Khan (as credited by that package). Please verify against a printed mushaf before quoting. Other quotes are labelled with their attribution caveats.</p></div></div></section><!--PQ-END-->'''

def main():
    s = PAGE.read_text(encoding="utf-8")
    a = s.index('<section class="portfolio-intro'); b = s.index("</section>", a) + len("</section>")
    s = s[:a] + hero() + s[b:]
    s = re.sub(r"<!--PQ-START-->.*?<!--PQ-END-->", lambda m: words(), s, flags=re.S)
    s = s.replace("<body>", '<body class="pf-page">', 1) if '<body class="pf-page">' not in s else s
    if "Amiri" not in s:
        s = s.replace("family=Dancing+Script:wght@700", "family=Dancing+Script:wght@700&family=Amiri:wght@400;700&family=Atma:wght@400;500", 1)
    if "portfolio-flip.js" not in s:
        s = s.replace("</body>", f'<script src="/assets/portfolio-flip.js?v={TOK}" defer></script>\n</body>', 1)
    s = re.sub(r'/assets/style\.css\?v=[^"]*', f'/assets/style.css?v={TOK}', s)
    PAGE.write_text(s, encoding="utf-8")
    print("ok")
main()
