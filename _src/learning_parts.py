#!/usr/bin/env python3
"""Hanging-line parts for /learning/ (workshops, featured, universities, professional bodies, long-form).
Source of truth: _src/learning_parts.json (first run extracts it from the old HTML sections).
Writes the block between <!--LD-PARTS--> and <!--/LD-PARTS--> in learning/index.html."""
import re, json, os, html
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'learning/index.html'); JS = os.path.join(ROOT, '_src/learning_parts.json')
src = open(IDX, encoding='utf-8').read()

def extract():
    soup = BeautifulSoup(src, 'html.parser')
    def img(t): return t['src'] if t and t.get('src') else None
    d = {}
    d['communities'] = [dict(logo=img(a.find('img')), name=a.h3.get_text(strip=True), desc=a.p.get_text(strip=True)) for a in soup.select('.workshop-card')]
    seen, feat = set(), []
    for a in soup.select('.rolling-card'):
        t = a.h3.get_text(strip=True)
        if t in seen: continue
        seen.add(t)
        feat.append(dict(logo=img(a.find('img')), topic=a.select_one('.pill').get_text(strip=True), title=t, provider=a.p.get_text(strip=True)))
    d['featured'] = feat
    secs = soup.select('section.rf-unisec')
    def cards(sec):
        out = []
        for li in sec.select('ul.rf-uni > li.rf-uni-card'):
            out.append(dict(logos=[im['src'] for im in li.find_all('img', recursive=True)], name=li.find('b').get_text(strip=True),
                            items=[dict(t=x.find(string=True, recursive=False) and ''.join(x.find_all(string=True, recursive=False)).strip(), d=x.em.get_text(strip=True)) for x in li.select('ul > li')],
                            skills=[s.get_text(strip=True) for s in li.select('.rf-skills span')]))
        return out
    d['universities'] = cards(secs[0]); d['professional'] = cards(secs[1]); d['trainings'] = cards(secs[2])
    d['stats'] = [dict(n=li.b.get_text(strip=True), l=li.span.get_text(strip=True)) for li in secs[1].select('ul.rf-stats li')]
    subs = secs[1].select('p.rf-sub'); d['prof_lead'] = subs[0].get_text(strip=True); d['prof_note'] = subs[1].get_text(strip=True)
    d['uni_lead'] = secs[0].select_one('p.rf-sub').get_text(strip=True); d['train_lead'] = secs[2].select_one('p.rf-sub').get_text(strip=True)
    return d
if not os.path.exists(JS):
    json.dump(extract(), open(JS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
D = json.load(open(JS, encoding='utf-8'))

esc = lambda t: html.escape(t, quote=True)
PM = {'LinkedIn Learning': '/assets/img/linkedin-learning-mark.svg', 'Coursera': '/assets/img/coursera-mark.svg'}
LENS = [30, 58, 42, 70, 36, 52]; ROT = (-0.9, 0.7, -0.5, 1.0, -0.7, 0.5)
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
def style(i, ln=None): return f'--len:{ln if ln else LENS[i % 6]}px;--d:{(i % 7) * 0.45:.2f}s;--r:{ROT[i % 6]}deg;--k:{(0.7, 1.0, 1.3, 0.85, 1.15, 0.95)[i % 6]}'
def cell(i, cls, inner, ln=None): return f'<li class="hg-cell"><div class="hg-card {cls}" style="{style(i, ln)}"><i class="hg-peg" aria-hidden="true"></i>{inner}</div></li>'
def logo(src_, big=False): return f'<img src="{esc(src_)}" alt="" width="40" height="40" loading="lazy">'
def split_item(t):
    """trailing '(…)' -> chip: durations get a clock, credits plain"""
    m = re.search(r'\s*\(([^()]*)\)\s*$', t)
    if m and re.search(r'\d\s*h\b|\bmin\b|PDU|CDU|CPE', m.group(1)):
        k = 'dur' if re.search(r'\bh\b|\bmin\b', m.group(1)) else 'cr'
        return t[:m.start()], m.group(1), k
    return t, None, None
def items_html(items):
    o = ''
    for it in items:
        t, chip, k = split_item(it['t'])
        c = (f'<span class="hg-chip hg-chip--{k}">{CLOCK if k == "dur" else ""}{esc(chip)}</span>' if chip else '')
        o += f'<li><span>{esc(t)}{c}</span><em>{esc(it["d"])}</em></li>'
    return f'<ul class="hg-courses">{o}</ul>'
def logos_row(ls): return '<div class="hg-logorow">' + ''.join(logo(l) for l in ls) + '</div>'
def uni_card(i, c):
    return cell(i, 'hg-card--uni', logos_row(c['logos']) + f'<h4>{esc(c["name"])}</h4>' + items_html(c['items']) +
                ('<p class="hg-skills">' + ''.join(f'<span>{esc(s)}</span>' for s in c['skills']) + '</p>' if c['skills'] else ''))

def rail(label, cells, name):
    lab = f'<h5 class="hg-linelabel">{label}</h5>' if label else ''
    return (f'{lab}<div class="hg-rail"><button type="button" class="hg-arrow hg-prev" aria-label="Scroll {esc(name)} back">←</button>'
            f'<button type="button" class="hg-arrow hg-next" aria-label="Scroll {esc(name)} forward">→</button>'
            f'<div class="hg-track" tabindex="0" role="region" aria-label="{esc(name)}, scroll sideways"><ol class="hg-line">{cells}</ol></div></div>')
def part(pid, letter, c1, c2, kick, title, lead, extra, rails, note=''):
    w = title.rsplit(' ', 1)
    h = (esc(w[0]) + ' <em>' + esc(w[1]) + '</em>') if len(w) == 2 else '<em>' + esc(title) + '</em>'
    return (f'<article class="hg-part hg-part--x" id="{pid}" style="--c1:{c1};--c2:{c2}"><div class="hg-meta"><span class="hg-num">{letter}</span><span class="hg-cat">{esc(kick)}</span>'
            f'<h3>{h}</h3><p>{esc(lead)}</p>{extra}</div>{"".join(rails)}{("<p class=hg-note>" + esc(note) + "</p>") if note else ""}'
            f'<p class="hg-hint">Scroll to walk the line <span aria-hidden="true">→</span></p></article>')

parts = []
# A. workshops & communities (+ trainings)
com = ''.join(cell(i, 'hg-card--org', logo(c['logo']) + f'<h4>{esc(c["name"])}</h4><p>{esc(c["desc"])}</p>') for i, c in enumerate(D['communities']))
tr = ''.join(cell(i + 3, 'hg-card--uni', logos_row(c['logos']) + f'<h4>{esc(c["name"])}</h4>' + items_html(c['items'])) for i, c in enumerate(D['trainings']))
parts.append(part('workshops', 'A', '#e5566d', '#9e2a40', 'Hands-on experience', 'Workshops & professional development',
    'Practical workshops and professional communities. The trainings line holds participation and completion certificates.', '',
    [rail('Communities &amp; professional growth', com, 'communities'), rail('Trainings, workshops &amp; short courses', tr, 'trainings')]))
# B. featured learning: every specialization, learning path / professional certificate, master course and 5 h+ course in the record
AFF = [(r'Duke University', 'Duke University', 'universities/duke-university-logo.png'), (r'IE Business School', 'IE Business School', 'universities/ie-business-school-logo.png'),
 (r'University of California San Diego', 'UC San Diego', 'universities/university-of-california-san-diego-ucsd-logo.png'),
 (r'American Marketing Association|Generative AI for Marketing', 'American Marketing Association', 'institutions/american-marketing-association-ama-logo.png'),
 (r'Toastmasters', 'Toastmasters International', 'institutions/toastmasters-international-logo.png'),
 (r'Microsoft and LinkedIn|Career Essentials in Project Management', 'Microsoft', 'institutions/microsoft-logo.png'),
 (r'Sales Management Foundations', 'Sales Management Association', 'institutions/sales-management-association-logo.png'),
 (r'Zendesk', 'Zendesk', 'institutions/zendesk-logo.png')]
DUR = {'master microsoft excel': '14 h 54 min', 'master microsoft powerpoint': '9 h 32 min', 'presentation tips': '5 h 11 min'}
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
import datetime
FE = []
for m in re.finditer(r'<article class="course-row" data-category="([^"]*)" data-provider="([^"]*)".*?<h3>(.*?)</h3>.*?<div class="date">(.*?)</div>', src, re.S):
    cat, prov, title, dl = (html.unescape(x) for x in m.groups())
    isp = dl.startswith('Learning path') or 'Professional Certificate' in title
    dk = next((v for k, v in DUR.items() if title.lower().startswith(k)), None)
    if not (isp or dk or re.match(r'Master ', title)): continue
    dm = re.search(r'(\d+) (\w{3})\w* (\d{4})', dl)
    dt = datetime.date(int(dm.group(3)), MON[dm.group(2)], int(dm.group(1))) if dm else None
    key = re.sub(r'\s+by .*$|\s*\(.*\)$', '', title).lower().replace(' professional certificate', '')
    if any(f['key'] == key for f in FE): continue
    kind = 'Learning path' if isp else ('Master course' if title.startswith('Master ') else 'Course · 5 h+')
    FE.append(dict(key=key, title=title, prov=prov, cat=cat, dt=dt, dur=dk, kind=kind))
FE.sort(key=lambda f: (f['dt'] is None, -(f['dt'].toordinal() if f['dt'] else 0)))
SPEC = [dict(key='spec1', title='Marketing Strategy Specialization', prov='Coursera', cat='Marketing & Brand Strategy', dt=None, dur=None, kind='Specialization · 5 courses', org='IE Business School', logo='universities/ie-business-school-logo.png', when='Jan 2023'),
        dict(key='spec2', title='Drug Development Product Management Specialization', prov='Coursera', cat='Pharmaceutical & Product Management', dt=None, dur=None, kind='Specialization · 3 courses', org='UC San Diego', logo='universities/university-of-california-san-diego-ucsd-logo.png', when='Oct 2020')]
def fe_card(i, f):
    if 'org' not in f:
        for pat, nm, lg in AFF:
            if re.search(pat, f['title'], re.I): f['org'], f['logo'] = nm, lg; break
    when = f.get('when') or (f['dt'].strftime('%b %Y') if f['dt'] else '')
    h = f'<span class="hg-pill">{esc(f["cat"])}</span><h4>{esc(f["title"])}</h4>'
    if f.get('dur'): h += f'<div class="hg-dur">{CLOCK}{esc(f["dur"])}</div>'
    h += f'<div class="hg-src"><img src="{esc(PM.get(f["prov"], ""))}" alt="" width="18" height="18" loading="lazy"><span>{esc(f["prov"])}</span></div>'
    if f.get('org'): h += '<div class="hg-aff">' + (f'<img src="/assets/img/logos/{f["logo"]}" alt="" width="34" height="34" loading="lazy">' if f.get('logo') else '') + f'<span>{esc(f["org"])}</span></div>'
    h += f'<div class="hg-foot"><span class="hg-path">{esc(f["kind"])}</span>' + (f'<time>{esc(when)}</time>' if when else '') + '</div>'
    return cell(i, 'hg-card--feat', h)
ALLF = SPEC + FE
fe = ''.join(fe_card(i, f) for i, f in enumerate(ALLF))
parts.append(part('featured', 'B', '#2f9be0', '#145e9b', 'Featured learning', 'Specializations, paths & master courses',
    'Every specialization, learning path, professional certificate and master course, plus the courses over five hours, hanging in one line. Nothing moves on its own: scroll or swipe at your own pace.',
    f'<div class="hg-tags"><span class="hg-tag">{len(ALLF)} credentials &amp; paths</span></div><a class="hg-open" href="#timeline">Browse all courses <span aria-hidden="true">↓</span></a>',
    [rail('', fe, 'featured learning')], 'Learning time is shown only where a certificate states it.'))
# C. universities behind Coursera
un = ''.join(uni_card(i, c) for i, c in enumerate(D['universities']))
parts.append(part('universities', 'C', '#1fae7b', '#0b6f4d', 'Coursera · online certificates', 'Universities behind my Coursera certificates',
    D['uni_lead'], f'<div class="hg-tags"><span class="hg-tag">{len(D["universities"])} universities</span></div>', [rail('', un, 'universities')]))
# D. professional bodies
pr = ''.join(uni_card(i, c) for i, c in enumerate(D['professional']))
stats = '<ul class="hg-stats">' + ''.join(f'<li><b>{esc(s["n"])}</b><span>{esc(s["l"])}</span></li>' for s in D['stats']) + '</ul>'
parts.append(part('professional', 'D', '#ee8a22', '#9c4c00', 'LinkedIn Learning · professional bodies', 'Specialised institutions behind my skill courses',
    D['prof_lead'], stats, [rail('', pr, 'professional bodies')], D['prof_note']))
block = ('<!--LD-PARTS-->\n<section class="hg hg--x" id="learningParts" aria-label="Workshops, certificates and long courses"><div class="hg-xwrap">' + ''.join(parts) + '</div></section>\n<!--/LD-PARTS-->')
if '<!--LD-PARTS-->' not in src:
    a = src.index('<section class="workshop-zone"'); b = src.index('<section class="band">')
    src = src[:a] + block + '\n' + src[b:]
    # move the by-skill block ahead of the filters band
    m = re.search(r'<!--LD-HANG-->.*?<!--/LD-HANG-->', src, re.S)
    if m:
        hang = m.group(0); src = src.replace(hang, '', 1); src = src.replace('<section class="band">', hang + '\n<section class="band">', 1)
    # drop featured credentials block (specializations already sit on the university cards)
    src = re.sub(r'<div class="section-title" style="margin-top:0"><div class="kick">Featured credentials</div>.*?</div>\s*<div class="featured-cert">.*?</div>\s*(?=<div class="section-title")', '', src, count=1, flags=re.S)
else:
    src = re.sub(r'<!--LD-PARTS-->.*?<!--/LD-PARTS-->', lambda m: block, src, flags=re.S)
open(IDX, 'w', encoding='utf-8').write(src)
print('parts', len(parts), 'featured', len(ALLF), {k: len(v) for k, v in D.items() if isinstance(v, list)})
