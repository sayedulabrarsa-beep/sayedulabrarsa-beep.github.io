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

def is_due(item):
    release_at = datetime.strptime(
        item["date"] + "T" + item.get("time", DATA.get("publish_time", "20:00")),
        "%Y-%m-%dT%H:%M"
    ).replace(tzinfo=ZoneInfo("Asia/Dhaka"))
    return NOW >= release_at

def card_status(item, exists):
    due = is_due(item)
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
# Release each English/Bangla pair together only when both pages exist and the item is draftable.
for item in items:
    pub_date = item["date"]
    due = is_due(item)
    pair = [
        (f'blog/{item["slug"]}/index.html', f"{SITE}/blog/{item['slug']}/"),
        (f'blog/{item["slug"]}-bangla/index.html', f"{SITE}/blog/{item['slug']}-bangla/"),
    ]
    pages = [(ROOT / rel, url) for rel, url in pair]
    complete_pair = all(page.exists() for page, _ in pages)
    allowed_to_publish = item.get("status") != "not_drafted"
    release_pair = due and complete_pair and allowed_to_publish

    if not complete_pair:
        missing += sum(1 for page, _ in pages if not page.exists())

    for page, url in pages:
        if not page.exists():
            continue
        source = page.read_text(encoding="utf-8")
        robots = "index,follow,max-image-preview:large" if release_pair else "noindex,nofollow"
        if re.search(r'<meta name="robots" content="[^"]*">', source, re.I):
            source = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', source, count=1, flags=re.I)
        else:
            source = source.replace("</head>", f'<meta name="robots" content="{robots}"></head>', 1)
        if release_pair:
            for key in ("datePublished", "dateModified"):
                source = re.sub(r'("' + key + r'"\\s*:\\s*")[^"]+(")', lambda m: m.group(1)+pub_date+m.group(2), source)
            source = re.sub(r'(<time[^>]*datetime=")[^"]+(")', lambda m: m.group(1)+pub_date+m.group(2), source, count=1)
        page.write_text(source, encoding="utf-8")

        # Remove only this page's exact sitemap entry (tolerates entries missing </url>) before optionally adding it back.
        head, _, rest = sitemap.partition('<url>')
        body = rest.rsplit('</urlset>', 1)[0]
        chunks = ['<url>' + c for c in ('<url>' + body).split('<url>')[1:]] if rest else []
        keep = []
        for c in chunks:
            c = c.strip()
            if f'<loc>{url}</loc>' in c:
                continue
            if not c.endswith('</url>'):
                c += '</url>'
            keep.append('  ' + c)
        sitemap = head.rstrip() + '\n' + '\n'.join(keep) + '\n</urlset>\n'
        if release_pair:
            og = re.search(r'<meta property="og:image" content="([^"]+)"', source)
            alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', source)
            block = f'<url><loc>{url}</loc><lastmod>{pub_date}</lastmod>'
            if og:
                block += f'<image:image><image:loc>{html.escape(og.group(1), quote=False)}</image:loc>'
                if alt: block += f'<image:title>{html.escape(alt.group(1))}</image:title>'
                block += '</image:image>'
            seen = {og.group(1) if og else ''}
            for im in re.finditer(r'<img src="(/assets/img/blog/[^"?]+)[^"]*" alt="([^"]*)"', source):
                full = SITE + im.group(1)
                if full in seen or full.endswith('.svg'):
                    continue
                seen.add(full)
                block += f'<image:image><image:loc>{html.escape(full, quote=False)}</image:loc><image:title>{html.escape(html.unescape(im.group(2)))}</image:title></image:image>'
            block += '</url>'
            sitemap = sitemap.replace('</urlset>', '  ' + block + '\n</urlset>')
            released += 1
        else:
            hidden += 1


# Add newly released English/Bangla pairs to the public Pharma Blog grid, once only.
blog_index = ROOT / "blog" / "index.html"
if blog_index.exists():
    blog_html = blog_index.read_text(encoding="utf-8")
    for item in items:
        due = is_due(item)
        if not due or item.get("status") == "not_drafted":
            continue
        slug = item["slug"]
        en_path = ROOT / "blog" / slug / "index.html"
        bn_path = ROOT / "blog" / (slug + "-bangla") / "index.html"
        if not (en_path.exists() and bn_path.exists()):
            continue
        href = f"/blog/{slug}/"
        if href in blog_html:
            continue
        en = en_path.read_text(encoding="utf-8")
        bn = bn_path.read_text(encoding="utf-8")
        def get_meta(source, name, attr="name"):
            m = re.search(r'<meta ' + attr + r'="' + re.escape(name) + r'" content="([^"]*)"', source, re.I)
            return html.unescape(m.group(1)) if m else ""
        def get_h1(source):
            m = re.search(r'<h1[^>]*>(.*?)</h1>', source, re.S | re.I)
            return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else item["title"]
        title_en = get_h1(en)
        title_bn = get_h1(bn)
        desc_en = get_meta(en, "description") or item["title"]
        desc_bn = get_meta(bn, "description") or title_bn
        image = get_meta(en, "og:image", "property")
        image_alt = get_meta(en, "og:image:alt", "property") or title_en
        image = image.replace(SITE, "") if image.startswith(SITE) else image
        kicker = "PHARMACOLOGY BASICS"
        read_match = re.search(r'(\\d+)\\s*MIN', en, re.I)
        read_time = read_match.group(1) if read_match else "5"
        card = (
            f'<article class="pb-feature-card" data-topics="pharmacology basics medicine bangla" data-search="{html.escape(title_en + " " + title_bn + " " + desc_en + " " + desc_bn, quote=True)}">'
            f'<a href="{href}" class="pb-card-image"><img src="{html.escape(image, quote=True)}" alt="{html.escape(image_alt, quote=True)}" loading="lazy"><span class="pb-image-label">NEW · {kicker}</span></a>'
            f'<div class="pb-card-copy"><p class="pb-card-meta">{kicker} <span>·</span> {read_time} MIN READ</p>'
            f'<h3><a href="{href}">{html.escape(title_en)}</a></h3><p>{html.escape(desc_en)}</p>'
            f'<p class="pb-bangla" lang="bn">{html.escape(desc_bn)}</p>'
            f'<a class="pb-read-link" href="{href}">Read in English ↗</a>'
            f'<a class="pb-bangla-link" href="/blog/{slug}-bangla/">বাংলায় পড়ুন ↗</a></div></article>'
        )
        grid_open = '<div class="pb-featured-grid">'
        grid_close = '</div><div id="pb-no-results"'
        if grid_open in blog_html and grid_close in blog_html:
            blog_html = blog_html.replace(grid_open, grid_open + card, 1)
    blog_index.write_text(blog_html, encoding="utf-8")

sitemap_path.write_text(sitemap, encoding="utf-8")

# Remove any previously injected public calendar blocks. The editorial schedule stays private.
targets = [ROOT / "index.html", ROOT / "blog" / "index.html"] + list((ROOT / "blog").glob("*/index.html"))
for page in targets:
    if not page.exists(): continue
    source = page.read_text(encoding="utf-8")
    cleaned = re.sub(r'<!--editorial-calendar:start-->.*?<!--editorial-calendar:end-->', '', source, flags=re.S)
    if cleaned != source:
        page.write_text(cleaned, encoding="utf-8")

# Rebuild discovery surfaces from published pages only.
subprocess.run(["python3", "_src/blog_stacks.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/seo_feeds.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/article_index.py"], cwd=ROOT, check=True)
print(f"Dhaka date={TODAY}; released pages={released}; hidden pages={hidden}; missing draft pages={missing}; public calendar removed from {len(targets)} surfaces")
