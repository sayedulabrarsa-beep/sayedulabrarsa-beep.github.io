#!/usr/bin/env python3
"""Rebuilds partner wall, responsibilities and the quote band on /portfolio/. Run after portfolio_cabinet.py."""
import re, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "portfolio" / "index.html"
e = html.escape
L = "/assets/img/logos/"

def li(img, alt, label, href=None):
    inner = f'<img src="{L}{img}" alt="{e(alt)}" loading="lazy"><span>{e(label)}</span>'
    return f'<li><a href="{href}">{inner}</a></li>' if href else f'<li>{inner}</li>'

def partner_wall():
    opsonin = "".join([
        li("finix-rabeprazole-sodium-logo.png", "Finix logo, rabeprazole sodium brand by Opsonin Pharma Ltd.", "Finix", "/brands/finix/"),
        li("finix-mups-rabeprazole-sodium-logo.png", "Finix MUPS logo, Finix MUPS 20 mg by Opsonin Pharma Ltd.", "Finix MUPS", "/brands/finix-mups/"),
        li("finix-hp-clarithromycin-amoxicillin-rabeprazole-logo.png", "Finix HP logo, rabeprazole, amoxicillin and clarithromycin pack by Opsonin Pharma Ltd.", "Finix HP", "/brands/finix-hp/")])
    navana = li("malifa-30-ferric-maltol-capsule-logo.png", "Malifa 30 logo, ferric maltol 30 mg capsule by Navana Pharmaceuticals PLC", "Malifa 30", "/brands/malifa/")
    def co(color, logo, alt, name, role, tag, brands, cls=""):
        return (f'<article class="pw-co {cls}" style="--c:{color}"><header><img src="{L}{logo}" alt="{e(alt)}" loading="lazy"><div><b>{e(name)}</b><span>{e(role)}</span></div><em>{e(tag)}</em></header>'
                f'<ul class="pw-brands">{brands}</ul></article>')
    early = (f'<article class="pw-co pw-co--early" style="--c:#6b7a99"><header><div><b>Early experience</b><span>Internship &amp; in-plant training</span></div><em>Foundation</em></header>'
             f'<ul class="pw-brands">{li("lazz-pharma-limited-logo.png", "Lazz Pharma Limited logo", "Lazz Pharma · Internship")}{li("drug-international-limited-logo.png", "Drug International Limited logo", "Drug International · In-plant training")}</ul></article>')
    companies = (co("#1d9a5b", "opsonin-pharma-ideas-for-healthcare-logo.png", "Opsonin Pharma Ltd. logo, Ideas for healthcare", "Opsonin Pharma Ltd.", "Product Executive", "Current", opsonin)
                 + co("#d3202a", "navana-pharmaceuticals-plc-logo.png", "Navana Pharmaceuticals PLC logo", "Navana Pharmaceuticals PLC", "Brand Executive", "Previous", navana) + early)
    def grp(title, sub, items):
        return f'<article class="pw-grp"><header><b>{e(title)}</b><span>{e(sub)}</span></header><ul class="pw-brands">{"".join(items)}</ul></article>'
    learning = "".join([
        grp("University & campus", "Where it started", [
            li("daffodil-international-university-logo.png", "Daffodil International University logo", "Daffodil International University · B.Pharm"),
            li("diu-career-development-center-cdc-logo.png", "DIU Career Development Center (CDC) logo", "DIU Career Development Center"),
            li("pharmacia-club-daffodil-international-university-logo.png", "Pharmacia Club, Daffodil International University logo", "DIU Pharmacia Club · Student leadership")]),
        grp("Professional bodies & trainers", "Skills for the field", [
            li("bshrm-bangladesh-society-for-human-resources-management-logo.png", "BSHRM logo", "BSHRM"),
            li("hrdi-human-resource-development-institute-logo.png", "HRDI logo", "HRDI"),
            li("briddhi-we-help-to-grow-logo.png", "Briddhi, We Help to Grow logo", "Briddhi · Professional growth"),
            li("coach-kamrul-hasan-ckh-network-logo.png", "CKH Network logo", "CKH Network")]),
        grp("Online learning platforms", "Always learning", [
            li("coursera-logo.png", "Coursera logo", "Coursera"),
            li("linkedin-learning-logo.png", "LinkedIn Learning logo", "LinkedIn Learning")]),
        grp("Community & education", "Giving back", [
            li("admission-ac-logo.png", "Admission.ac logo", "Admission.ac · Education events"),
            li("tamirul-millat-kamil-madrasah-logo.png", "Tamirul Millat Kamil Madrasah logo", "Tamirul Millat Kamil Madrasah · Education")])])
    return f'''<!--PW-START--><section class="partner-wall rf-partners pw2" aria-labelledby="pw-h"><div class="wrap"><p class="eyebrow">Companies, brands &amp; learning partners</p><h2 id="pw-h">Previous &amp; current brand partnerships</h2>
<p class="pw-note">Logos belong to their respective owners and are shown only to identify the organisations and brands mentioned on this website.</p>
<div class="pw-tabs" role="tablist" aria-label="Partner groups"><button type="button" role="tab" id="pw-t1" aria-controls="pw-p1" aria-selected="true">Companies &amp; brands</button><button type="button" role="tab" id="pw-t2" aria-controls="pw-p2" aria-selected="false">Education, community &amp; learning</button></div>
<div class="pw-panel" id="pw-p1" role="tabpanel" aria-labelledby="pw-t1"><h3 class="pw-h3">Pharmaceutical companies &amp; brands</h3><div class="pw-cos">{companies}</div></div>
<div class="pw-panel" id="pw-p2" role="tabpanel" aria-labelledby="pw-t2"><h3 class="pw-h3">Education, community &amp; professional learning</h3><div class="pw-grps">{learning}</div></div>
</div></section><!--PW-END-->'''

RS = [
 ("Launch & nurture products", "Undertake all activities regarding new product launching and nourishing assigned products based on market potential and prospect.",
  ["Market potential", "Launch planning", "Lifecycle care"], "/brands/finix/", "Explore the Finix brands", "#e8f3ee"),
 ("Strategy & campaigns", "Formulate the strategies and promotional campaign to achieve the sales target.",
  ["Positioning", "Campaign planning", "Sales targets"], "/experience/", "See my experience", "#fbeee0"),
 ("Annual budgeting", "Formulate annual budget for assigned products.",
  ["Budget planning", "Prioritisation", "Brand investment"], "/about/#journey", "Read my journey", "#fdf3d8"),
 ("Promotional materials & activities", "Develop promotional materials and define necessary promotional activities for establishing new and existing products.",
  ["Leaflets & visuals", "Presentations", "Activity plans"], "#cabinet", "See the packs on the shelf", "#f1ebf8"),
 ("Conferences, seminars & CME", "Conduct field conferences, scientific seminar/CME on regular basis at different regions.",
  ["Field conferences", "Scientific seminars", "CME", "Regions"], "/learning/", "My learning & workshops", "#e6eefb"),
 ("Training the field team", "Train the field colleagues regarding assigned products.",
  ["Product knowledge", "Field coaching", "Confidence"], "/learning/", "How I keep learning", "#fde9e6"),
]

def responsibilities(old):
    cards = []
    for i, (t, line, chips, href, cta, bg) in enumerate(RS, 1):
        rev = " portfolio-project-reverse" if i % 2 == 0 else ""
        cards.append(f'''<article id="resp-{i}" class="portfolio-project rs-card{rev}"><div class="portfolio-project-visual rs-vis" style="--bg:{bg}"><span class="rs-n" aria-hidden="true">{i:02d}</span><img src="/assets/img/portfolio/rs-{i}.svg" alt="" width="480" height="340" loading="lazy" decoding="async"></div>
<div class="portfolio-project-copy"><span class="portfolio-project-kicker">Responsibility {i:02d}</span><h3>{e(t)}</h3><p>{e(line)}</p><ul class="rf-chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul><a href="{href}" class="portfolio-text-link">{e(cta)} <span>↗</span></a></div></article>''')
    def grab(pid):
        k = old.index(f'id="{pid}"'); a = old.rindex("<article", 0, k); b = old.index("</article>", k) + len("</article>")
        return old[a:b]
    p4, p5 = grab("proj-4"), grab("proj-5")
    p4 = p4.replace("04 · Previous experience", "Beyond the role · Previous experience").replace('<p class="rf-next"><a href="#proj-5">Next project ↓</a></p>', "").replace('id="proj-4" class="portfolio-project portfolio-project-reverse"', 'id="proj-4" class="portfolio-project"')
    p5 = p5.replace("05 · Education & development", "Beyond the role · Education & development").replace('<p class="rf-next"><a href="#top">Back to top ↑</a></p>', "").replace('id="proj-5" class="portfolio-project"', 'id="proj-5" class="portfolio-project portfolio-project-reverse"')
    return f'''<!--RS-START--><section class="portfolio-projects"><div class="wrap portfolio-projects-wrap">
<div class="portfolio-section-heading"><p class="eyebrow">Product Management Department · Executive</p><h2>The responsibilities behind the brands</h2><p>The six major responsibilities of a PMD executive, and the foundations that support them. Product names and trademarks belong to their respective owners.</p></div>
{"".join(cards)}
<h3 class="rs-sub">Beyond the role</h3>{p4}{p5}
</div></section><!--RS-END-->'''

QS = [
 ("q", "وَقُل رَّبِّ زِدْنِي عِلْمًا", "“…and say, ‘My Lord, increase me in knowledge.’”", "Quran 20:114", "Sahih International"),
 ("t", None, "“All things are poison, and nothing is without poison; the dose alone makes a thing not a poison.”", "Paracelsus", "Common English rendering of his Third Defense. Wording varies by translation."),
 ("q", "وَمَنْ أَحْيَاهَا فَكَأَنَّمَا أَحْيَا النَّاسَ جَمِيعًا", "“…and whoever saves one, it is as if he had saved mankind entirely.”", "Quran 5:32 (closing part)", "Sahih International"),
 ("t", None, "“The good physician treats the disease; the great physician treats the patient who has the disease.”", "Attributed to William Osler", "Widely attributed; I could not confirm the original source."),
 ("q", "وَأَن لَّيْسَ لِلْإِنسَانِ إِلَّا مَا سَعَىٰ", "“And that there is not for man except that [good] for which he strives.”", "Quran 53:39", "Sahih International"),
 ("q", "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "“Indeed, with hardship [will be] ease.”", "Quran 94:6", "Sahih International"),
]

def band():
    slides = []
    for i, (k, ar, en, ref, note) in enumerate(QS):
        arh = f'<p class="pq-ar" lang="ar" dir="rtl">{ar}</p>' if ar else ""
        slides.append(f'<blockquote class="pq-s{" is-on" if i == 0 else ""}" data-k="{k}"{"" if i == 0 else " hidden"}>{arh}<p class="pq-en">{en}</p><footer><cite>{e(ref)}</cite><small>{e(note)}</small></footer></blockquote>')
    dots = "".join(f'<button type="button" aria-label="Show quote {i+1}"{" aria-current=true" if i == 0 else ""}></button>' for i in range(len(QS)))
    return f'''<!--PQ-START--><section class="portfolio-highlight-band pq"><div class="wrap"><div class="pq-grid"><div class="pq-copy"><p class="eyebrow">Beyond the project list</p><h2>Progress through curiosity, consistency and collaboration.</h2>
<p>Pharmacy is a promise to put people first. Behind every pack on the shelf is someone waiting for relief, a family hoping for a good recovery and a doctor who needs clear, honest information.</p>
<p>The best work in healthcare is often quiet and consistent: explaining a medicine clearly, supporting a colleague in the field, and keeping safety and trust ahead of every target. That is the standard I try to bring to every brand and every team.</p>
<a href="/about/#journey" class="portfolio-light-link">Read my journey ↗</a></div>
<div class="pq-card" id="pq" aria-roam="x"><span class="pq-mark" aria-hidden="true">“</span><div class="pq-stage" aria-live="polite">{"".join(slides)}</div>
<div class="pq-ctl"><button type="button" class="pq-prev" aria-label="Previous quote">‹</button><div class="pq-dots">{dots}</div><button type="button" class="pq-next" aria-label="Next quote">›</button></div></div></div>
<div class="portfolio-highlights pq-row"><div><strong>2025</strong><span>PMD Iconic Award recognition</span></div><div><strong>Rx + Sales</strong><span>Data-informed brand decisions</span></div><div><strong>Healthcare</strong><span>Patient-centred perspective</span></div></div></div></section><!--PQ-END-->'''.replace(' aria-roam="x"', "")

def main():
    s = PAGE.read_text(encoding="utf-8")
    # partner wall
    s = re.sub(r"<!--PW-START-->.*?<!--PW-END-->", "", s, flags=re.S)
    a = s.index('<section class="partner-wall'); b = s.index("</section>", a) + len("</section>")
    s = s[:a] + partner_wall() + s[b:]
    # responsibilities
    if "<!--RS-START-->" in s:
        raise SystemExit("responsibilities already built; restore proj-4/5 source first")
    a = s.index('<section class="portfolio-projects'); b = s.index("</section>", a) + len("</section>")
    s = s[:a] + responsibilities(s[a:b]) + s[b:]
    # quote band
    a = s.index('<section class="portfolio-highlight-band'); b = s.index("</section>", a) + len("</section>")
    s = s[:a] + band() + s[b:]
    s = re.sub(r"/assets/style\.css\?v=[^\"]*", "/assets/style.css?v=pc3-20261108", s)
    s = re.sub(r"/assets/cabinet\.js\?v=[^\"]*", "/assets/cabinet.js?v=pc3-20261108", s)
    PAGE.write_text(s, encoding="utf-8"); print("ok")
main()
