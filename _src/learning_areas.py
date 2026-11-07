#!/usr/bin/env python3
"""Builds the Learning doors (on /learning/) and one landing page per skill area.
Single source of truth: the .course-row articles inside learning/index.html.
Run from the repository root:  python3 _src/learning_areas.py
"""
import re, html, json, os, datetime
from collections import OrderedDict

SITE = 'https://sayedulabrar.site'
TODAY = datetime.date.today().isoformat()
CSSV = 'ld9-20261107'
P = 'learning/index.html'

AREAS = OrderedDict([
 ('AI & Emerging Technology', dict(slug='ai-emerging-technology', icon='ai', lead='Generative AI, prompt writing and AI tools, mostly applied to marketing, healthcare and product work.')),
 ('Pharmaceutical & Product Management', dict(slug='pharmaceutical-product-management', icon='pharma', lead='From drug discovery to commercialization, plus product management, roadmaps and product marketing.')),
 ('Marketing & Brand Strategy', dict(slug='marketing-brand-strategy', icon='marketing', lead='Marketing strategy, digital and social media marketing, SEO, market research and personal branding.')),
 ('Data & Microsoft Office', dict(slug='data-microsoft-office', icon='data', lead='Excel from formulas to dashboards, Power Query and VBA, plus PowerPoint design and data visualization.')),
 ('Design & Content Creation', dict(slug='design-content-creation', icon='design', lead='Graphic design fundamentals, Canva, print production, and writing and presentation skills.')),
 ('Leadership & Communication', dict(slug='leadership-communication', icon='lead', lead='Public speaking, negotiation, business writing and communicating as a leader.')),
 ('Project Management & Business', dict(slug='project-management-business', icon='pm', lead='Project management foundations, teamwork and strategy, business development and Microsoft 365 at work.')),
 ('Health, Psychology & Well-being', dict(slug='health-psychology-well-being', icon='health', lead='Well-being, psychology, human physiology, food and health, and understanding medical research.')),
 ('Sales & Customer Experience', dict(slug='sales-customer-experience', icon='sales', lead='Sales management and strategy, coaching, customer service and building rapport with customers.')),
])
def svg(d): return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+d+'</svg>'
ICONS = {
 'ai': svg('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 12h4"/>'),
 'pharma': svg('<g transform="rotate(-45 12 12)"><rect x="2" y="8" width="20" height="8" rx="4"/><path d="M12 8v8"/></g>'),
 'marketing': svg('<path d="M3 11v3a1 1 0 001 1h2l7 4V6L6 10H4a1 1 0 00-1 1z"/><path d="M16 9a4 4 0 010 6M18.5 6.5a8 8 0 010 11"/>'),
 'data': svg('<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>'),
 'design': svg('<path d="M12 20l7-7-4-4-7 7v4z"/><path d="M14 8l2-2a2.1 2.1 0 013 3l-2 2"/>'),
 'lead': svg('<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.5a3 3 0 010 5.5M18 14.3c2 .8 3.5 2.8 3.5 5.2"/>'),
 'pm': svg('<rect x="3" y="4" width="5" height="16" rx="1.2"/><rect x="10" y="4" width="5" height="10" rx="1.2"/><rect x="17" y="4" width="4" height="13" rx="1.2"/>'),
 'health': svg('<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.4A4 4 0 0119 10c0 5.6-7 10-7 10z"/>'),
 'sales': svg('<path d="M3 4h2l2.2 10.2a1 1 0 001 .8h8.6a1 1 0 001-.8L20 8H6"/><circle cx="9" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/>'),
}
COLORS = [('#e39a2d','#9a5200'),('#2fa39a','#145f66'),('#7a6ff0','#403a9e'),('#e0675a','#9b2f2f'),('#4f9be0','#215a99'),('#c26ec9','#7a3a86'),('#5bb06a','#2c6d3b'),('#e0a52d','#8a6205'),('#d9706e','#8c3a52')]
MON = {m:i+1 for i,m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
esc = lambda t: html.escape(t, quote=True)

# ------------------------------------------------------------------ data
src = open(P, encoding='utf-8').read()
rows = re.findall(r'<article class="course-row" data-category="([^"]*)" data-provider="([^"]*)" data-search="[^"]*">(.*?)</article>', src, re.S)
seen = set(); courses = []
for cat, prov, b in rows:
    cat = html.unescape(cat); prov = html.unescape(prov)
    title = html.unescape(re.search(r'<h3>(.*?)</h3>', b).group(1)).strip()
    dl = html.unescape(re.search(r'<div class="date">(.*?)</div>', b).group(1)).strip()
    # the provider tag is wrong on a few records; the date line names the platform explicitly
    if dl.startswith('Coursera'): prov = 'Coursera'
    elif dl.startswith('LinkedIn Learning'): prov = 'LinkedIn Learning'
    key = (title.lower(), prov)
    if key in seen: continue
    seen.add(key)
    is_path = dl.startswith('Learning path') or 'Professional Certificate' in title
    sub = re.sub(r'^Learning path\s*·\s*', '', dl)
    sub = re.sub(r'^(Coursera|LinkedIn Learning)\s*·\s*', '', sub)
    m = re.search(r'(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})', dl)
    date = datetime.date(int(m.group(3)), MON[m.group(2)], int(m.group(1))) if m else None
    courses.append(dict(cat=cat, prov=prov, title=title, sub=sub, path=is_path, date=date))
by = OrderedDict((c, []) for c in AREAS)
for c in courses: by[c['cat']].append(c)
order = sorted(AREAS, key=lambda c: -len(by[c]))
for i, c in enumerate(order):
    AREAS[c].update(idx=i, n=len(by[c]), c=COLORS[i % len(COLORS)])
fmt = lambda d: f'{d.day} {d.strftime("%b %Y")}'

# ------------------------------------------------------------------ doors html
def door_html(cat, tag='a'):
    a = AREAS[cat]; n = a['n']
    return (f'<a class="ld-door" href="/learning/{a["slug"]}/" style="--c1:{a["c"][0]};--c2:{a["c"][1]}" aria-label="Open {esc(cat)}: {n} courses">'
            f'<span class="ld-frame"><span class="ld-room"><b>{n}</b><small>courses</small></span>'
            f'<span class="ld-panel"><span class="ld-num">{a["idx"]+1:02d}</span><span class="ld-ico">{ICONS[a["icon"]]}</span><span class="ld-name">{esc(cat)}</span><span class="ld-knob" aria-hidden="true"></span></span></span>'
            f'<span class="ld-floor" aria-hidden="true"></span><span class="ld-cta">Click to enter<em>{n} courses</em></span></a>')

# ------------------------------------------------------------------ restructure /learning/ once
if '<!--LD-DOORS-->' not in src:
    m_old = re.search(r'<section class="learning-hero learning-hero-redesign">.*?</section>\s*', src, re.S)
    metrics = re.findall(r'<div class="learning-metric[^"]*">(.*?)</div>\s*</div>', m_old.group(0), re.S) if False else None
    nums = re.findall(r'<div class="learning-metric-number">(.*?)</div><div class="learning-metric-label">(.*?)</div>', m_old.group(0))
    plat = re.search(r'<div class="learning-platform-line">.*?</div>', m_old.group(0), re.S).group(0)
    glance = ''.join(f'<div class="lp-glance-item"><b>{n}</b><span>{l}</span></div>' for n, l in nums)
    new = ('<section class="lp-hero" id="doors"><div class="wrap">'
           '<div class="lp-status"><span class="lp-dot" aria-hidden="true"></span><span>Continuous learning</span><i></i><span>Dhaka time <b id="lpTime">--:--</b></span></div>'
           '<h1 class="lp-title">Learning <span>&amp; Certifications</span></h1>'
           '<p class="lp-lead">Every skill area is a door. Open one to walk into its own page, with the full list of courses and learning paths I completed there.</p>'
           + plat +
           '<p class="lp-hint">Drag, swipe or use the arrows to walk the line <span aria-hidden="true">→</span></p></div>'
           '<div class="lp-stage"><button type="button" class="lp-arrow lp-prev" aria-label="Previous doors">←</button><button type="button" class="lp-arrow lp-next" aria-label="Next doors">→</button>'
           '<div class="lp-track" id="lpTrack" tabindex="0" aria-label="Skill area doors, scroll sideways"><!--LD-DOORS--><!--/LD-DOORS--></div></div>'
           '<div class="lp-floor" aria-hidden="true"></div></section>'
           '<section class="lp-glance" aria-label="Learning at a glance"><div class="wrap"><span class="lp-glance-head">My learning at a glance</span>' + glance + '<a class="lp-glance-link" href="#timeline">Full course record ↓</a></div></section> ')
    src = src.replace(m_old.group(0), new, 1)
    src = re.sub(r'<section class="ld-zone".*?</section>\s*', '', src, flags=re.S)
    src = src.replace('<script src="/assets/learning-doors.js?v=ld4-20261107" defer></script>', '')
    src = src.replace('<script src="/assets/site.js?', '<script src="/assets/learning-doors.js?v=' + CSSV + '" defer></script><script src="/assets/site.js?', 1)
src = re.sub(r'<!--LD-DOORS-->.*?<!--/LD-DOORS-->', lambda m: '<!--LD-DOORS-->' + ''.join(door_html(c) for c in order) + '<!--/LD-DOORS-->', src, flags=re.S)
src = re.sub(r'style\.css\?v=[\w-]+', 'style.css?v=' + CSSV, src)
src = re.sub(r'learning-doors\.js\?v=[\w-]+', 'learning-doors.js?v=' + CSSV, src)
open(P, 'w', encoding='utf-8').write(src)

# ------------------------------------------------------------------ area pages
head = src[:src.index('<main')]
head = re.sub(r'<style>.*?</style>', '', head, flags=re.S)           # page-specific inline css of /learning/ is not needed here
foot = src[src.index('</main>'):]
foot = re.sub(r'<script>\s*\(function\(\)\{\s*const burger.*?</script>', '<script>(function(){var b=document.getElementById("burger"),m=document.getElementById("menu");if(b&&m){b.addEventListener("click",function(){var o=b.getAttribute("aria-expanded")!=="true";b.setAttribute("aria-expanded",String(o));m.classList.toggle("open",o)})}var y=document.getElementById("year");if(y)y.textContent=new Date().getFullYear()})();</script>', foot, flags=re.S)
foot = foot.replace('<script src="/assets/learning-doors.js', '<script src="/assets/learning-doors.js')

def set_head(h, title, desc, url):
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h)
    h = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="#1a1818">', h)
    og = (f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
          f'<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og-image.png"><meta name="twitter:card" content="summary_large_image">')
    h = h.replace('<link rel="stylesheet" href="/assets/style.css', og + '<link rel="stylesheet" href="/assets/style.css', 1)
    h = h.replace('<script>try{if(localStorage', '<script>try{if(sessionStorage.getItem("ldEnter")){document.documentElement.classList.add("lp-arrive");sessionStorage.removeItem("ldEnter")}}catch(e){}</script><script>try{if(localStorage', 1)
    return h

def card(c, a):
    provcls = 'li' if c['prov'] == 'LinkedIn Learning' else 'co'
    sub = esc(c['sub']) if c['sub'] else ''
    when = fmt(c['date']) if c['date'] else ''
    return (f'<article class="lp-card"><span class="lp-prov lp-prov-{provcls}">{esc(c["prov"])}</span><h3>{esc(c["title"])}</h3>'
            f'<p class="lp-sub">{sub if not (c["date"] and sub.startswith("Completed")) else ""}</p>'
            f'<div class="lp-card-foot"><span class="lp-type">{"Learning path" if c["path"] else "Course"}</span><span class="lp-when">{esc(when)}</span></div></article>')

def groups_for(cat):
    cs = sorted(by[cat], key=lambda c: (c['date'] is None, -(c['date'].toordinal() if c['date'] else 0), c['title']))
    g = []
    paths = [c for c in cs if c['path']]
    li = [c for c in cs if not c['path'] and c['prov'] == 'LinkedIn Learning']
    co = [c for c in cs if not c['path'] and c['prov'] == 'Coursera']
    if paths: g.append(('Learning paths', 'Learning paths & certificates', 'Multi-course learning paths completed in this area.', paths))
    if li: g.append(('LinkedIn Learning', 'LinkedIn Learning courses', 'Individual courses, newest first.', li))
    if co: g.append(('Coursera', 'Coursera courses', 'University-led courses and specialization courses.', co))
    return g

for cat, a in AREAS.items():
    cs = by[cat]; n = len(cs); grp = groups_for(cat)
    dated = [c['date'] for c in cs if c['date']]
    provs = OrderedDict()
    for c in cs: provs[c['prov']] = provs.get(c['prov'], 0) + 1
    url = f'{SITE}/learning/{a["slug"]}/'
    title = f'{cat}: Courses & Learning Paths | Sayedul Abrar'
    desc = f'{n} completed courses and learning paths in {cat} by Sayedul Abrar, from LinkedIn Learning and Coursera. {a["lead"]}'
    h = set_head(head, title, desc, url).replace('<body>', f'<body class="lp-page" style="--c1:{a["c"][0]};--c2:{a["c"][1]}">', 1)
    prev_c = order[(a['idx']-1) % len(order)]; next_c = order[(a['idx']+1) % len(order)]
    stats = [f'<div class="lp-stat"><b>{n}</b><span>courses and paths</span></div>',
             f'<div class="lp-stat"><b>{len(provs)}</b><span>{esc(" · ".join(f"{k} {v}" for k, v in provs.items()))}</span></div>']
    if dated: stats.append(f'<div class="lp-stat"><b>{fmt(max(dated))}</b><span>latest completion</span></div>')
    sec = []
    for i, (tag, h2, d, items) in enumerate(grp, 1):
        ds = [c['date'] for c in items if c['date']]
        k = len(items); noun = ('path' if k == 1 else 'paths') if tag == 'Learning paths' else ('course' if k == 1 else 'courses')
        chips = [f'{k} {noun}']
        if ds:
            y0, y1 = min(ds).year, max(ds).year
            chips.append(str(y0) if y0 == y1 else f'{y0} – {y1}')
        if tag == 'Coursera':
            inst = []
            for c in items:
                s = c['sub'].split('·')[0].strip()
                if s and not s.startswith('Completed') and s not in inst: inst.append(s)
            chips += inst[:2]
        elif tag != 'Learning paths': chips.append(tag)
        sec.append(f'<section class="lp-group" aria-labelledby="g{i}"><div class="lp-group-head"><div><p class="lp-group-tag"><span>{i:02d}</span> {esc(tag)} · {esc(cat)}</p><h2 id="g{i}">{esc(h2)}</h2><p class="lp-group-desc">{esc(d)}</p>'
                   f'<ul class="lp-chips">{"".join(f"<li>{esc(x)}</li>" for x in chips)}</ul></div>'
                   f'<div class="lp-gal-ctl"><span class="lp-scroll-cue">Scroll <span aria-hidden="true">→</span></span><button type="button" class="lp-arrow lp-gprev" aria-label="Scroll back">←</button><button type="button" class="lp-arrow lp-gnext" aria-label="Scroll forward">→</button></div></div>'
                   f'<div class="lp-gallery" tabindex="0" aria-label="{esc(h2)}, scroll sideways">{"".join(card(c, a) for c in items)}</div></section>')
    chips_all = ''.join(f'<a href="/learning/{AREAS[c]["slug"]}/"{" aria-current=\"page\"" if c == cat else ""}>{esc(c)}</a>' for c in order)
    main = (f'<main id="main"><div class="lp-curtain" aria-hidden="true"></div>'
            f'<div class="lp-strip"><div class="wrap"><span class="lp-dot" aria-hidden="true"></span><span>Sayedul Abrar · learning record</span><span class="lp-strip-time">Dhaka time <b id="lpTime">--:--</b></span><a href="/learning/#doors">← Back to the doors</a></div></div>'
            f'<section class="lp-intro"><div class="wrap lp-intro-grid"><div class="lp-intro-copy"><p class="lp-kick">Door {a["idx"]+1:02d} of {len(order):02d}</p><h1>{esc(cat)}</h1><p class="lp-lead">{esc(a["lead"])}</p>'
            f'<div class="lp-stats">{"".join(stats)}</div><p class="lp-hint">Scroll to walk the line <span aria-hidden="true">↓</span></p></div>'
            f'<div class="lp-arch" aria-hidden="true"><span class="lp-arch-in"><span class="lp-arch-ico">{ICONS[a["icon"]]}</span><b>{n}</b><small>courses</small></span></div></div></section>'
            f'<div class="wrap lp-groups">{"".join(sec)}</div>'
            f'<section class="lp-nextdoor"><div class="wrap"><a class="lp-nd lp-nd-prev" href="/learning/{AREAS[prev_c]["slug"]}/"><small>← Previous door</small><b>{esc(prev_c)}</b></a><a class="lp-nd lp-nd-next" href="/learning/{AREAS[next_c]["slug"]}/"><small>Next door →</small><b>{esc(next_c)}</b></a></div></section>'
            f'<section class="lp-cta"><div class="wrap"><p class="lp-kick">All doors</p><div class="lp-door-links">{chips_all}</div>'
            f'<p class="lp-note">Individual courses are completed courses, not separate certificates, unless a credential was issued. Learning paths are shown as paths.</p>'
            f'<div class="lp-cta-row"><a class="lp-btn" href="/contact/">Get in touch</a><a class="lp-btn lp-btn-ghost" href="/learning/#timeline">Full course record</a></div></div></section></main>')
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learning", "item": SITE + "/learning/"},
            {"@type": "ListItem", "position": 3, "name": cat, "item": url}]},
          {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{cat}: courses and learning paths", "url": url, "description": desc,
           "author": {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"},
           "mainEntity": {"@type": "ItemList", "numberOfItems": n, "itemListElement": [{"@type": "ListItem", "position": i, "name": c['title']} for i, c in enumerate(cs, 1)]}}]
    ldh = ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>' for o in ld)
    page = h.replace('</head>', ldh + '</head>', 1) + main + foot
    os.makedirs(f'learning/{a["slug"]}', exist_ok=True)
    open(f'learning/{a["slug"]}/index.html', 'w', encoding='utf-8').write(page)

# ------------------------------------------------------------------ sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
add = ''
for cat, a in AREAS.items():
    loc = f'{SITE}/learning/{a["slug"]}/'
    if loc not in sm: add += f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod></url>\n'
if add: sm = sm.replace('</urlset>', add + '</urlset>'); open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('areas', len(AREAS), 'unique courses', len(courses), [(c, AREAS[c]['n']) for c in order])
