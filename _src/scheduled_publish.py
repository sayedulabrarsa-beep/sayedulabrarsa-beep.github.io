#!/usr/bin/env python3
"""Hide upcoming pharmacology articles and release each EN/BN pair on its calendar date."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import html, re, subprocess

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
TODAY = datetime.now(ZoneInfo("Asia/Dhaka")).date()
TOPICS = [
 ("drug-distribution-how-medicines-reach-their-target", "2026-11-16"),
 ("drug-metabolism-how-the-body-processes-medicines", "2026-11-18"),
 ("drug-excretion-how-medicines-leave-the-body", "2026-11-21"),
 ("drug-half-life-explained", "2026-11-23"),
 ("bioavailability-explained", "2026-11-25"),
 ("onset-peak-duration-of-drug-action", "2026-11-28"),
 ("different-types-of-medicine-dosage-forms", "2026-11-30"),
 ("immediate-sustained-enteric-coated-medicines", "2026-12-02"),
 ("routes-of-drug-administration", "2026-12-05"),
 ("drug-interactions-explained", "2026-12-07"),
 ("side-effects-vs-adverse-drug-reactions", "2026-12-09"),
 ("how-to-read-a-medicine-label", "2026-12-12"),
]
sitemap_path = ROOT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
released = hidden = 0

for slug, date_text in TOPICS:
    pub_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    is_live = pub_date <= TODAY
    display_date = pub_date.strftime("%B %-d, %Y")
    for suffix in ("", "-bangla"):
        rel = f"blog/{slug}{suffix}/index.html"
        page = ROOT / rel
        if not page.exists():
            raise SystemExit(f"Missing scheduled page: {rel}")
        source = page.read_text(encoding="utf-8")
        robots = "index,follow,max-image-preview:large" if is_live else "noindex,nofollow"
        if re.search(r'<meta name="robots" content="[^"]*">', source, re.I):
            source = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', source, count=1, flags=re.I)
        else:
            source = source.replace("</head>", f'<meta name="robots" content="{robots}"></head>', 1)
        if re.search(r'<meta property="article:published_time" content="[^"]*">', source, re.I):
            source = re.sub(r'<meta property="article:published_time" content="[^"]*">', f'<meta property="article:published_time" content="{date_text}T20:00:00+06:00">', source, count=1, flags=re.I)
        else:
            source = source.replace("</head>", f'<meta property="article:published_time" content="{date_text}T20:00:00+06:00"></head>', 1)
        source = re.sub(r'("datePublished"\s*:\s*")[^"]+(")', rf'\g<1>{date_text}\2', source)
        source = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', rf'\g<1>{date_text}\2', source)
        source = re.sub(r'(<time[^>]*datetime=")[^"]+(")', rf'\g<1>{date_text}\2', source, count=1)
        page.write_text(source, encoding="utf-8")
        url = f"{SITE}/{rel.rsplit('/index.html',1)[0]}/"
        pattern = re.compile(r'<url>.*?<loc>' + re.escape(url) + r'</loc>.*?</url>\s*', re.S)
        sitemap = pattern.sub("", sitemap)
        if is_live:
            og = re.search(r'<meta property="og:image" content="([^"]+)"', source)
            alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', source)
            block = f"  <url><loc>{url}</loc><lastmod>{date_text}</lastmod>"
            if og:
                block += f"<image:image><image:loc>{html.escape(og.group(1), quote=False)}</image:loc>"
                if alt: block += f"<image:title>{html.escape(alt.group(1))}</image:title>"
                block += "</image:image>"
            block += "</url>\n"
            sitemap = sitemap.replace("</urlset>", block + "</urlset>")
            released += 1
        else:
            hidden += 1

sitemap_path.write_text(sitemap, encoding="utf-8")
print(f"Dhaka date: {TODAY}; released pages: {released}; hidden pages: {hidden}")

# Rebuild all discovery surfaces from the pages that are now indexable.
subprocess.run(["python3", "_src/blog_stacks.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/seo_feeds.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "_src/article_index.py"], cwd=ROOT, check=True)
