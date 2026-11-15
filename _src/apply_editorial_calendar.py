#!/usr/bin/env python3
"""Apply the editorial calendar: hide future pages, release due pairs, and render the calendar across the site."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import json, html, re, subprocess

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
NOW = datetime.now(ZoneInfo("Asia/Dhaka"))
TODAY = NOW.date()
DATA = json.loads((ROOT / "_src/editorial_calendar.json").read_text(encoding="utf-8"))
items = DATA["items"]
sitemap_path = ROOT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
released = hidden = missing = 0

def card_status(item, exists):
    due = datetime.strptime(item["date"], "%Y-%m-%d").date() <= TODAY
    if item["status"].startswith("draft_on"):
        return "Published" if due and exists else ("Draft overdue" if due else "Draft planned")
    if not exists: return "Page in preparation"
    return "Published" if due else "Scheduled"

def render_calendar():
    rows = []
    for item in items:
        en = ROOT / "blog" / item["slug"] / "index.html"
        bn = ROOT / "blog" / (item["slug"] + "-bangla") / "index.html"
        exists = en.exists() and bn.exists()
        status = card_status(item, exists)
        href = f'/blog/{item["slug"]}/'
        link = f'<a href="{href}">View article</a>' if exists and status == "Published" else ""
        extra = f'<small>{html.escape(item.get("needs",""))}</small>' if item.get("needs") else ""
        dt = datetime.strptime(item["date"], "%Y-%m-%d").strftime("%a, %d %b")
        rows.append(f'<li class="ec-item"><span class="ec-date">{dt} · 8:00 PM</span><span class="ec-title">{html.escape(item["title"])}</span><span class="ec-status">{status}</span>{extra}{link}</li>')
    return '''<!--editorial-calendar:start-->
<section class="editorial-calendar" aria-labelledby="editorial-calendar-title">
<style>
.editorial-calendar{margin:34px auto;padding:22px;max-width:1120px;border:1px solid #d8e5e2;border-radius:20px;background:linear-gradient(135deg,#f1f8f6,#fffaf3);color:#193b3d}
.editorial-calendar .ec-kicker{font-size:.72rem;letter-spacing:.14em;font-weight:700;color:#287c73;text-transform:uppercase;margin:0 0 8px}
.editorial-calendar h2{font-size:clamp(1.35rem,3vw,1.9rem);margin:0 0 8px;color:#183e40}
.editorial-calendar .ec-intro{margin:0 0 16px;color:#526b6a}
.editorial-calendar ul{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));gap:9px}
.editorial-calendar .ec-item{display:flex;flex-direction:column;gap:4px;padding:12px 14px;background:rgba(255,255,255,.82);border:1px solid #e0eae7;border-radius:12px}
.editorial-calendar .ec-date{font-size:.76rem;font-weight:700;color:#287c73}
.editorial-calendar .ec-title{font-weight:650;line-height:1.35}
.editorial-calendar .ec-status{font-size:.78rem;color:#8a5a27}
.editorial-calendar small{font-size:.75rem;color:#6a7774}
.editorial-calendar a{font-size:.8rem;font-weight:700;color:#17656a}
@media(prefers-color-scheme:dark){.editorial-calendar{background:#142c2d;color:#e7f2ef;border-color:#315052}.editorial-calendar h2{color:#e7f2ef}.editorial-calendar .ec-intro{color:#b9cbc7}.editorial-calendar .ec-item{background:#1c393a;border-color:#315052}.editorial-calendar .ec-status{color:#f0bd7d}}
</style>
<p class="ec-kicker">Editorial calendar · Bangladesh time</p>
<h2 id="editorial-calendar-title">What’s coming next on the Pharma Blog</h2>
<p class="ec-intro">English and Bangla editions are planned together. Standard release time: 8:00 PM (UTC+6).</p>
<ul>''' + "".join(rows) + '''</ul>
</section>
<!--editorial-calendar:end-->'''

calendar_html = render_calendar()
# Hide future articles, release due English/Bangla pairs, and keep sitemap in sync.
for item in items:
    pub_date = item["date"]
    due = datetime.strptime(pub_date, "%Y-%m-%d").date() <= TODAY
    for suffix in ("", "-bangla"):
        rel = f'blog/{item["slug"]}{suffix}/index.html'
        page = ROOT / rel
        if not page.exists():
            missing += 1
            continue
        source = page.read_text(encoding="utf-8")
        robots = "index,follow,max-image-preview:large" if due else "noindex,nofollow"
        if re.search(r'<meta name="robots" content="[^"]*">', source, re.I):
            source = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', source, count=1, flags=re.I)
        else:
            source = source.replace("</head>", f'<meta name="robots" content="{robots}"></head>', 1)
        for key in ("datePublished", "dateModified"):
            source = re.sub(r'("' + key + r'"\\s*:\\s*")[^"]+(")', lambda m: m.group(1)+pub_date+m.group(2), source)
        source = re.sub(r'(<time[^>]*datetime=")[^"]+(")', lambda m: m.group(1)+pub_date+m.group(2), source, count=1)
        page.write_text(source, encoding="utf-8")
        url = f"{SITE}/{rel.rsplit('/index.html',1)[0]}/"
        # Remove only the exact URL block; never consume preceding sitemap entries.
        blocks = re.findall(r'<url>.*?</url>', sitemap, flags=re.S)
        sitemap = re.sub(r'<url>.*?</url>', lambda m: '' if f'<loc>{url}</loc>' in m.group(0) else m.group(0), sitemap, flags=re.S)
        if due:
            og = re.search(r'<meta property="og:image" content="([^"]+)"', source)
            alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', source)
            block = f'<url><loc>{url}</loc><lastmod>{pub_date}</lastmod>'
            if og:
                block += f'<image:image><image:loc>{html.escape(og.group(1), quote=False)}</image:loc>'
                if alt: block += f'<image:title>{html.escape(alt.group(1))}</image:title>'
                block += '</image:image>'
            sitemap = sitemap.replace('</urlset>', block + '</urlset>')
            released += 1
        else:
            hidden += 1

sitemap_path.write_text(sitemap, encoding="utf-8")

# Inject/update the same live calendar on the homepage, blog index, and every article page.
targets = [ROOT / "index.html", ROOT / "blog" / "index.html"] + list((ROOT / "blog").glob("*/index.html"))
for page in targets:
    if not page.exists(): continue
    source = page.read_text(encoding="utf-8")
    if "<!--editorial-calendar:start-->" in source:
        source = re.sub(r'<!--editorial-calendar:start-->.*?<!--editorial-calendar:end-->', lambda _: calendar_html, source, flags=re.S)
    elif page == ROOT / "index.html":
        anchor = '<section class="ed-blog-section">'
        source = source.replace(anchor, calendar_html + '\\n' + anchor, 1) if anchor in source else source.replace("</main>", calendar_html + "</main>", 1)
    elif page == ROOT / "blog" / "index.html":
        source = source.replace("<main", calendar_html + "\\n<main", 1) if "<main" in source else source.replace("</body>", calendar_html + "</body>", 1)
    else:
        source = source.replace("</main>", calendar_html + "</main>", 1)
    page.write_text(source, encoding="utf-8")

# Rebuild all discovery and homepage article components; generators omit noindex pages.
subprocess.run(["python3", "_src/blog_stacks.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/seo_feeds.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/article_index.py"], cwd=ROOT, check=True)
print(f"Dhaka date={TODAY}; released pages={released}; hidden pages={hidden}; missing draft pages={missing}; calendar surfaces={len(targets)}")
