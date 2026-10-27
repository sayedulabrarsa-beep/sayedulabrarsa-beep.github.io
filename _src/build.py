#!/usr/bin/env python3
"""Static site generator for sayedulabrar.site.

Run from anywhere:  python3 _src/build.py
It rewrites every page (index.html files), 404.html, sitemap.xml, sitemap.xsl and
robots.txt in the repository root. Styles live in assets/style.css and scripts in
assets/site.js (edit those directly). Blog and vlog posts are JSON files in
_src/content/blog and _src/content/vlog (see _src/README.md).

Test builds: SITE_OUT=/some/dir SITE_CONTENT=/some/content python3 _src/build.py
"""
import datetime
import glob
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("SITE_OUT") or os.path.dirname(HERE)
CONTENT = os.environ.get("SITE_CONTENT") or os.path.join(HERE, "content")
IMG_ROOT = os.path.dirname(HERE)  # images always come from the repo itself

import hashlib


def asset_ver(name):
    """Short content hash so browsers fetch fresh CSS/JS whenever they change."""
    try:
        with open(os.path.join(IMG_ROOT, "assets", name), "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()[:8]
    except OSError:
        return "0"


CSS_V, JS_V = asset_ver("style.css"), asset_ver("site.js")

BASE = "https://sayedulabrar.site"
TODAY = "2026-10-26"
NAME = "Sayedul Abrar"
PHOTO_ALT = "Sayedul Abrar, pharmacist and Product Executive at Opsonin Pharma Ltd."
HERO_ALT = "Sayedul Abrar in a navy suit standing on a road at sunset"
LINKEDIN = "https://www.linkedin.com/in/sayedulabrar"
EMAIL = "sayedulabrar.sa@gmail.com"

SOCIAL = '''<div class="social-links" aria-label="Social and contact links"><a class="social-link social-email" href="mailto:sayedulabrar.sa@gmail.com"  aria-label="Email Sayedul Abrar" title="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg><span>Email</span></a><a class="social-link social-linkedin" href="https://www.linkedin.com/in/sayedulabrar" rel="me noopener" target="_blank" aria-label="LinkedIn profile" title="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5.2 8.6H2.4V21h2.8zM3.8 2.5a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4ZM21.6 13.9c0-3.7-2-5.5-4.7-5.5a4.1 4.1 0 0 0-3.7 2V8.6h-2.8V21h2.8v-6.1c0-1.6.3-3.2 2.3-3.2s2 1.9 2 3.3V21h2.9z"/></svg><span>LinkedIn</span></a><a class="social-link social-whatsapp" href="https://wa.me/8801949899373" rel="me noopener" target="_blank" aria-label="WhatsApp 01949899373" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.5 3.5A11.7 11.7 0 0 0 2.1 17.6L.5 23.5l6-1.6A11.7 11.7 0 0 0 20.5 3.5ZM12 21a9.6 9.6 0 0 1-4.9-1.3l-.4-.2-3.5.9.9-3.4-.2-.4A9.6 9.6 0 1 1 12 21Zm5.3-7.2c-.3-.2-1.7-.9-2-.9s-.5-.2-.7.2-.8.9-1 1.1-.4.2-.7.1a7.8 7.8 0 0 1-2.3-1.4 8.6 8.6 0 0 1-1.6-2c-.2-.3 0-.5.2-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-.9-2.1c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.2-1.2 2.8 1.2 3.2 1.4 3.4c.2.2 2.4 3.7 5.8 5.1.8.3 1.4.5 1.9.6.8.2 1.5.2 2 .1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.1-1.4s-.3-.2-.6-.4Z"/></svg><span>WhatsApp</span></a><a class="social-link social-facebook" href="https://www.facebook.com/share/1KD1WJHgtk/" rel="me noopener" target="_blank" aria-label="Facebook profile" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-8h2.7l.4-3.1h-3.1v-2c0-.9.3-1.5 1.6-1.5h1.7V3.6c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.1H7.3V13h2.8v8z"/></svg><span>Facebook</span></a><a class="social-link social-instagram" href="https://www.instagram.com/abrar_abdur_rahman/" rel="me noopener" target="_blank" aria-label="Instagram @abrar_abdur_rahman" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="17.6" cy="6.6" r="1.2" fill="currentColor"/></svg><span>Instagram</span></a></div>'''

BRAND_SHOWCASE = '''<div class="brand-showcase" aria-label="Selected pharmaceutical brands">
        <div class="brand-showcase-heading"><div><p class="eyebrow">Selected portfolio</p><h2 class="sec-h">Brands I’ve managed</h2><p>Explore selected brands from my current and previous pharmaceutical roles. The brand names and original artwork belong to their respective owners.</p></div><div class="brand-scroll-controls"><button type="button" class="brand-scroll-btn" data-scroll="left" aria-label="Scroll brands left">←</button><button type="button" class="brand-scroll-btn" data-scroll="right" aria-label="Scroll brands right">→</button></div></div>
        <div class="brand-marquee" id="brandMarquee" tabindex="0" aria-label="Scrollable brand portfolio">
          <a class="brand-product-card" href="/brands/finix-mups/"><span class="brand-company-mark"><img src="/assets/img/opsonin-pharma-logo.png" alt="Opsonin Pharma logo"><span>OPSONIN PHARMA</span></span><span class="brand-wordmark finix-mups-wordmark"><span>Finix</span><b>MUPS</b></span><span class="brand-kind">Rabeprazole sodium · MUPS</span><span class="brand-card-action">Explore product <span aria-hidden="true">↗</span></span></a>
          <a class="brand-product-card" href="/brands/finix/"><span class="brand-company-mark"><img src="/assets/img/opsonin-pharma-logo.png" alt="Opsonin Pharma logo"><span>OPSONIN PHARMA</span></span><span class="brand-wordmark finix-wordmark">Finix</span><span class="brand-kind">Rabeprazole sodium</span><span class="brand-card-action">Explore product <span aria-hidden="true">↗</span></span></a>
          <a class="brand-product-card" href="/brands/finix-hp/"><span class="brand-company-mark"><img src="/assets/img/opsonin-pharma-logo.png" alt="Opsonin Pharma logo"><span>OPSONIN PHARMA</span></span><span class="brand-wordmark finix-wordmark">Finix <small>HP</small></span><span class="brand-kind">Rabeprazole + antibiotics</span><span class="brand-card-action">Explore product <span aria-hidden="true">↗</span></span></a>
          <a class="brand-product-card" href="/brands/malifa/"><span class="brand-company-mark"><img src="/assets/img/navana-pharma-logo.png" alt="Navana Pharmaceuticals logo"><span>NAVANA PHARMACEUTICALS</span></span><span class="brand-wordmark malifa-wordmark">Malifa <small>30</small></span><span class="brand-kind">Ferric maltol · Iron</span><span class="brand-card-action">Explore product <span aria-hidden="true">↗</span></span></a>
        </div>
        <p class="brand-disclaimer">Independent career portfolio only. Not an official manufacturer website. Product information is summarised from public manufacturer sources; use the official product label for full prescribing information.</p>
      </div>'''

esc = html.escape

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


def img_size(src, default=(1200, 750)):
    """Read pixel size of a site image so width/height attributes can be set."""
    if Image and src.startswith("/"):
        p = os.path.join(IMG_ROOT, src.lstrip("/"))
        if os.path.exists(p):
            try:
                return Image.open(p).size
            except Exception:
                pass
    return default


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


THEME_BOOT = "<script>try{var t=localStorage.getItem('sa-theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"

NAV = [("/", "Home"), ("/about/", "About"), ("/experience/", "Experience"), ("/achievements/", "Achievements"),
       ("/education/", "Education"), ("/learning/", "Learning"), ("/publications/", "Publications"), ("/community/", "Community"),
       ("/blog/", "Pharma Blog"), ("/vlog/", "Daily Vlog"), ("/contact/", "Contact"), ("/portfolio/", "Portfolio")]


def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap bar">
    <a class="logo" href="/">{NAME}</a>
    <nav aria-label="Main"><ul class="menu" id="menu">{''.join(items)}</ul></nav>
    <button class="tgl" id="tgl" type="button" aria-label="Switch light or dark theme">&#9788;</button>
  </div>
</header>"""


FOOTER = f"""<footer>
  <div class="wrap">
    <div class="fc">
      <div>
        <a class="logo" href="/" style="font-size:24px">{NAME}</a>
        <p style="margin-top:14px">Pharmacist and Product Executive at Opsonin Pharma Ltd., Dhaka, Bangladesh.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        {SOCIAL}
      </div>
      <div>
        <h4>Pages</h4>
        <ul>
          <li><a href="/about/">About</a></li><li><a href="/experience/">Experience</a></li>
          <li><a href="/achievements/">Achievements</a></li><li><a href="/education/">Education</a></li>
          <li><a href="/learning/">Learning</a></li>
          <li><a href="/publications/">Publications &amp; Certifications</a></li>
        </ul>
      </div>
      <div>
        <h4>More</h4>
        <ul>
          <li><a href="/blog/">Medical &amp; Pharma Blog</a></li><li><a href="/vlog/">Daily Vlog</a></li>
          <li><a href="/community/">Community</a></li><li><a href="/portfolio/">Portfolio</a></li><li><a href="/contact/">Contact</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="cr">Copyright@sayedulabrar_<span id="year">2026</span></div>
  </div>
</footer>
<script src="/assets/site.js?v={JS_V}" defer></script>"""


# ---------- structured data ----------
def person_ld():
    return {
        "@context": "https://schema.org", "@type": "Person", "@id": f"{BASE}/#person", "name": NAME,
        "url": f"{BASE}/", "image": f"{BASE}/assets/img/sayedul-abrar.jpg", "jobTitle": "Product Executive",
        "alternateName": "Abrar",
        "description": "Pharmacist and Product Executive at Opsonin Pharma Ltd. in Dhaka, Bangladesh, working on pharmaceutical brand management including Finix and Finix MUPS. Bachelor of Pharmacy graduate of Daffodil International University.",
        "worksFor": {"@type": "Organization", "name": "Opsonin Pharma Ltd."},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Daffodil International University", "department": "Department of Pharmacy"},
        "address": {"@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD"},
        "knowsLanguage": ["Bengali", "English", "Hindi"],
        "knowsAbout": ["Pharmaceutical brand management", "Finix", "Finix MUPS", "Pharmaceutical marketing", "Product management", "Brand strategy", "Brand development", "Sales management", "Prescription data analysis"],
        "sameAs": [LINKEDIN, "https://www.facebook.com/share/1KD1WJHgtk/", "https://www.instagram.com/abrar_abdur_rahman/", "https://wa.me/8801949899373"],
    }


def site_ld():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/",
            "name": NAME, "inLanguage": "en", "publisher": {"@id": f"{BASE}/#person"}}


def crumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}{p}"} for i, (n, p) in enumerate(items)]}


def post_ld(post, kind, url):
    d = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"],
         "description": post.get("summary", ""), "datePublished": post["date"],
         "dateModified": post.get("updated", post["date"]), "mainEntityOfPage": url,
         "author": {"@id": f"{BASE}/#person"}, "publisher": {"@id": f"{BASE}/#person"}, "inLanguage": "en"}
    if post.get("cover"):
        d["image"] = f"{BASE}{post['cover']}"
    if post.get("tags"):
        d["keywords"] = ", ".join(post["tags"])
    return d


# ---------- page shell ----------
def page(path, title, desc, body, ld=None, og_type="website", noindex=False, nav=None, og_image="/assets/img/og-image.png"):
    canon = f"{BASE}{path}"
    t, d = esc(title, quote=False), esc(desc, quote=True)
    ld_html = "\n".join(
        '<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>"
        for x in (ld or []))
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    img = f"{BASE}{og_image}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#2B2D3F">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta property="og:image:alt" content="{NAME}, pharmacist and Product Executive">
<meta property="og:locale" content="en_BD">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,600&family=Dancing+Script:wght@700&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={CSS_V}">
{THEME_BOOT}
{ld_html}
</head>
<body>
{header(nav or path)}
{body}
{FOOTER}
</body>
</html>
"""


def crumbs(items):
    out = []
    for label, href in items:
        out.append(f'<a href="{href}">{label}</a>' if href else label)
    return '<p class="crumbs">' + "<span>/</span>".join(out) + "</p>"


def phead(items, h1, intro):
    return f"""<section class="phead">
  <div class="wrap">
    {crumbs(items)}
    <h1>{h1}</h1>
    <p>{intro}</p>
  </div>
</section>"""


def cta(title="Get in touch", text="For brand management, pharma marketing, campus programmes or collaboration, write to me by email or on LinkedIn."):
    return f"""<section class="cta"><div class="wrap"><h2>{title}</h2><p>{text}</p><a class="btn" href="/contact/">Contact Sayedul</a></div></section>"""


def entry(time, h, org, text="", bullets=None, level="h2"):
    b = f"<ul>{''.join(f'<li>{x}</li>' for x in bullets)}</ul>" if bullets else ""
    t = f"<p>{text}</p>" if text else ""
    return f"""<article class="entry"><time>{time}</time><div><{level}>{h}</{level}><p class="org">{org}</p>{t}{b}</div></article>"""


def card(h, p):
    return f'<div class="card"><h3>{h}</h3><p>{p}</p></div>'


def strip(items, label, direction="right"):
    """items: list of dicts(src, alt, caption, href=None). Slides left to right."""
    figs = []
    for it in items:
        w, h = it.get("size") or img_size(it["src"])
        im = f'<img src="{it["src"]}" alt="{esc(it["alt"])}" width="{w}" height="{h}" loading="lazy">'
        if it.get("href"):
            im = f'<a href="{it["href"]}">{im}</a>'
        cap = f'<figcaption>{esc(it["caption"], quote=False)}</figcaption>' if it.get("caption") else ""
        figs.append(f"<figure>{im}{cap}</figure>")
    return f"""<div class="strip" data-dir="{direction}" role="group" aria-label="{esc(label)}"><div class="strip-track">{''.join(figs)}</div></div>"""


pages = {}   # path -> (html, in_sitemap, lastmod)


def add(path, html_text, sitemap=True, lastmod=TODAY):
    pages[path] = (html_text, sitemap, lastmod)


# ---------- HOME ----------
home_body = f"""<main id="main">
  <section class="hero">
    <div class="wrap">
      <div class="hl">
        <h1><small>Pharmacist</small>Sayedul<br><em>Abrar</em></h1>
        <p style="max-width:44ch;color:var(--muted);margin-bottom:20px">Product Executive at Opsonin Pharma Ltd., working on pharmaceutical brand management including Finix® and Finix MUPS®. A Bachelor of Pharmacy graduate of Daffodil International University, based in Dhaka, Bangladesh.</p>
        <a class="more" href="/about/">Learn More</a>
      </div>
      <div class="hr">
        <p class="quote">“Each step is a chance to make a positive difference.”<cite>{NAME}</cite></p>
        <div class="hero-photo"><img src="/assets/img/hero-sayedul-abrar.jpg" alt="{HERO_ALT}" width="800" height="1000" fetchpriority="high"></div>
        <div class="pioneer"><b>Product Executive, <i>Finix®</i></b><span>Opsonin Pharma Ltd.</span></div>
      </div>
    </div>
  </section>

  <section class="band deep">
    <div class="wrap two">
      <div>
        <h2 class="h">Pharmacist &amp; Brand Manager</h2>
        <p class="lead">{NAME} is a Product Executive in the Product Management Department at Opsonin Pharma Ltd., managing the pharmaceutical brand Finix® and contributing to its market development and strategy.</p>
        <p style="color:var(--muted)">As a Pharmacy alumnus of Daffodil International University, he is dedicated to patient-centred pharmaceutical solutions through strategic brand development, innovation and collaboration. His professional interests include Finix® and Finix MUPS® brand development, pharmaceutical marketing and product management.</p>
        <a class="more" href="/about/">Read the full profile</a>
      </div>
      <div class="stats">
        <div><b>3</b><span>Years in Pharma</span></div>
        <div><b>6</b><span>Awards &amp; Achievements</span></div>
        <div><b>13</b><span>Certifications</span></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2 class="h">Recent recognition</h2>
      <div class="tiles">
        <div class="tile on"><b>Best Productive, 1st Place</b><span>Annual PMD Iconic Award 2025</span></div>
        <div class="tile"><b>Best Innovative, 1st Place</b><span>Annual PMD Iconic Award 2025</span></div>
        <div class="tile"><b>Scholarly Publication Award</b><span>Daffodil International University, 2022</span></div>
        <div class="tile"><b>Best Arteries &amp; Campus Ambassador</b><span>HRDI</span></div>
      </div>
      <p style="margin-top:22px"><a class="more" href="/achievements/">See all achievements</a></p>
    </div>
  </section>

  <div class="marq" aria-label="Organisations I have worked and studied with">
    <div class="track" id="track">
      <img src="/assets/img/opsonin-pharma-logo.png" alt="Opsonin Pharma Ltd. logo" width="107" height="64" loading="lazy">
      <img class="nav" src="/assets/img/navana-pharma-logo.png" alt="Navana Pharma logo" width="296" height="40" loading="lazy">
      <img class="diu" src="/assets/img/daffodil-international-university-logo.png" alt="Daffodil International University logo" width="213" height="56" loading="lazy">
    </div>
  </div>

  <section class="band deep">
    <div class="wrap">
      <h2 class="h">Explore</h2>
      <div class="cards">
        <a class="card link" href="/experience/"><h3>Experience</h3><p>Opsonin Pharma, Navana Pharmaceuticals, industry training and campus leadership.</p><b>View experience →</b></a>
        <a class="card link" href="/achievements/"><h3>Achievements</h3><p>PMD Iconic Awards 2025, scholarly publication award and scholarships, with photos.</p><b>View achievements →</b></a>
        <a class="card link" href="/blog/"><h3>Medical &amp; Pharma Blog</h3><p>Written articles with pictures and explanations on medicine and pharmacy.</p><b>Read the blog →</b></a>
        <a class="card link" href="/vlog/"><h3>Daily Vlog</h3><p>Day-by-day moments from work, learning and life.</p><b>Watch the vlog →</b></a>
        <a class="card link" href="/education/"><h3>Education</h3><p>Bachelor of Pharmacy, Daffodil International University, CGPA 3.77 / 4.00.</p><b>View education →</b></a>
        <a class="card link" href="/publications/"><h3>Publications &amp; Certifications</h3><p>Research paper, professional certificates, seminars and workshops.</p><b>View publications →</b></a>
        <a class="card link" href="/community/"><h3>Community</h3><p>Agrojatra Foundation, student clubs, expos and career programmes.</p><b>View community work →</b></a>
        <a class="card link" href="/about/"><h3>About</h3><p>Skills, languages and the approach behind the work.</p><b>Read more →</b></a>
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/", page("/", "Sayedul Abrar (Abrar) | Pharmacist, Finix MUPS & Pharma Product Executive",
                   "Official profile of Sayedul Abrar (Abrar), pharmacist and Product Executive at Opsonin Pharma in Bangladesh. Explore Finix and Finix MUPS brand work, Daffodil International University Pharmacy education, achievements and alumni connections.",
              home_body, ld=[person_ld(), site_ld()], og_image="/assets/img/og-image.png"))

# ---------- ABOUT ----------
about_body = f"""<main id="main">
<section class="phead">
  <div class="wrap phead-grid">
    <div>
      {crumbs([("Home", "/"), ("About", None)])}
      <h1>About Sayedul Abrar</h1>
      <p>Pharmacist, Product Executive and brand strategist focused on patient-centred pharmaceutical solutions.</p>
    </div>
    <div class="brush"><img src="/assets/img/sayedul-abrar.jpg" alt="{PHOTO_ALT}" width="360" height="450" fetchpriority="high"></div>
  </div>
</section>
  <section class="band">
    <div class="wrap">
      <h2 class="sec-h">Summary</h2>
      <p class="lead" style="max-width:66ch">{NAME} currently serves as a Product Executive in the Product Management Department at Opsonin Pharma Ltd., managing the pharmaceutical brand Finix® and contributing to its market development and strategy.</p>
      <p style="max-width:70ch">He graduated with a Bachelor of Pharmacy from Daffodil International University and holds certifications in drug development and decision-making. He is dedicated to delivering impactful, patient-centred pharmaceutical solutions through strategic brand development and a focus on innovation and collaboration.</p>
      <p style="max-width:70ch">His experience spans Gastro, NSAIDs, and vitamin and mineral portfolios, with key brands including Finix and Malifa. He analyses Rx data and turns the findings into targeted marketing strategies that support brand growth and market penetration.</p>
      <p style="color:var(--muted)">Recognised at the Annual PMD Iconic Award 2025 for both Best Productive and Best Innovative performance.</p>
    </div>
  </section>
  <section class="band deep">
    <div class="wrap">
      <h2 class="sec-h">Skills</h2>
      <ul class="chips" aria-label="Skills">
        <li>Brand Development</li><li>Brand Strategy</li><li>Business</li><li>Sales Management</li><li>Negotiation</li>
        <li>Critical Thinking</li><li>Leadership</li><li>Planning &amp; Execution</li><li>Time Management</li><li>Teamwork</li>
      </ul>
      <h2 class="sec-h" style="margin-top:40px">Languages</h2>
      <ul class="chips" aria-label="Languages"><li>Bangla, native or bilingual</li><li>English, full professional</li><li>Hindi, limited working</li></ul>
      <h2 class="sec-h" style="margin-top:40px">Tools</h2>
      <p style="color:var(--muted)">MS Word, PowerPoint, Excel, Canva, Photoshop Express, and working awareness of AI tools for marketing and content.</p>
    </div>
  </section>
  {cta()}
</main>"""
add("/about/", page("/about/", "About Sayedul Abrar | Pharmacist & Brand Manager, Dhaka",
                    "Learn about Sayedul Abrar, a Dhaka pharmacist and Product Executive at Opsonin Pharma managing Finix, with skills in brand strategy, sales management and Rx data analysis.",
                    about_body, ld=[person_ld(), crumb_ld([("Home", "/"), ("About", "/about/")])], og_type="profile"))

# ---------- EXPERIENCE ----------
exp_body = f"""<main id="main">
{phead([("Home", "/"), ("Experience", None)], "Professional Experience", "Pharmaceutical brand management at Opsonin Pharma and Navana Pharmaceuticals, plus industry training and campus leadership.")}
  <section class="band">
    <div class="wrap">
      <h2 class="sec-h">Industry experience</h2>
      {BRAND_SHOWCASE}
      <div class="stack">
{entry("January 2025 – Present", "Product Executive", "Opsonin Pharma Ltd. · Product Management Department (PMD) · Dhaka", "Manages the Gastro portfolio, including Finix, Finix MUPS and Finix HP, and contributes to market development and brand strategy.")}
{entry("August 2023 – December 2024", "Brand Executive", "Navana Pharmaceuticals PLC · Strategic Brand Management Department (SBMD) · Dhaka", "Managed the NSAIDs and Vitamins &amp; Minerals portfolio, including Malifa, Megamag and Loxodol.")}
{entry("August 2023", "Internship", "Lazz Pharma Ltd. · Dhanmondi", "Worked in community pharmacy to understand the role of a pharmacist and gain in-field experience.")}
{entry("January – February 2023", "In-Plant Training", "Drug International Limited · Tongi, Dhaka", "Training across dispensing, warehouse, liquid, ointment, tablet, blister, IPQC, hard capsule, dry syrup, microbiology, HVAC, quality assurance, water system, quality control and product development.")}
      </div>
    </div>
  </section>
  <section class="band deep">
    <div class="wrap">
      <h2 class="sec-h">Student leadership and ambassador roles</h2>
      <div class="stack">
{entry("May 2022 – March 2023", "Team Leader", "Admission.ac", "Led the UK &amp; USA Education Expo 2022, the International Education Expo 2022 and the Cucas China Online Exhibition 2022, and organised many other programmes.")}
{entry("May 2022 – February 2023", "Student Ambassador", "Admission.ac · Dhanmondi, Dhaka")}
{entry("April 2022 – March 2023", "Organizing Secretary", "DIU Pharmacia Club · Daffodil International University", "Organised events and activities on pharmacy and healthcare, creating opportunities for students and professionals to learn, grow and network.")}
{entry("February 2022 – February 2023", "Campus Ambassador for Next Gen Leaders", "CKH Network · Dhaka")}
{entry("January 2022 – February 2023", "Career Ambassador, and Volunteer Leader (December 2022)", "Career Development Center · Ashulia, Dhaka", "Worked to learn about the job market and gain the right skills and knowledge.")}
{entry("June 2021 – June 2022", "Arteries", "Human Resource Development Institute (HRDI) · Ashulia, Dhaka")}
{entry("July 2021 – April 2022", "Campus Ambassador", "Human Resource Development Institute (HRDI) · Bangladesh")}
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/experience/", page("/experience/", "Sayedul Abrar | Finix & Finix MUPS Brand Management Experience",
                                         "Explore Sayedul Abrar’s pharmaceutical career at Opsonin Pharma and Navana Pharma, including Finix, Finix MUPS, Finix HP, pharmaceutical marketing and brand development.",
                         exp_body, ld=[crumb_ld([("Home", "/"), ("Experience", "/experience/")])]))

# ---------- ACHIEVEMENTS ----------
ACH_PHOTOS = [
    {"src": "/assets/img/award-pmd-iconic-2025-stage.jpg",
     "alt": "Annual PMD Iconic Award 2025 stage with a screen showing Sayedul Abrar as 1st place, Best Innovative, General-A Team",
     "caption": "Annual PMD Iconic Award 2025: Best Innovative, 1st place, General-A Team."},
    {"src": "/assets/img/award-opsonin-conference-2026-trophies.jpg",
     "alt": "Sayedul Abrar holding two award trophies in front of the Opsonin Pharma Conference 2026 backdrop",
     "caption": "With two award trophies at the Opsonin Pharma Limited conference, Bashundhara ICCB."},
]
ach_body = f"""<main id="main">
{phead([("Home", "/"), ("Achievements", None)], "Awards &amp; Achievements", "Recognition for product management performance, innovation, scholarly publication and academic excellence.")}
  <section class="band deep" aria-labelledby="ph">
    <div class="wrap"><h2 class="sec-h" id="ph">Award photos</h2></div>
    {strip(ACH_PHOTOS, "Award photos, sliding from left to right")}
  </section>
  <section class="band">
    <div class="wrap">
      <h2 class="sec-h">Awards</h2>
      <div class="stack">
{entry("2025", "1st Place, Best Productive (General-A)", "Annual PMD Iconic Award 2025 · Opsonin Pharma Ltd.", "Recognising outstanding performance in product management.")}
{entry("2025", "1st Place, Best Innovative (General-A)", "Annual PMD Iconic Award 2025 · Opsonin Pharma Ltd.", "Recognising excellence in innovation and idea execution.")}
{entry("2022", "Prestigious Scholarly Publication Award", "Daffodil International University", "Awarded for publication in reputed indexed journals.")}
{entry("HRDI", "Best Arteries &amp; Campus Ambassador", "HRDI", "Awarded the prestigious Best Arteries &amp; Campus Ambassador title by the Human Resource Development Institute.")}
{entry("2013", "Masterpiece Student Reception-2013", "Upazila level", "Awarded for achieving 1st place in Upazila.")}
{entry("2012", "Talentpool Scholarship", "JDC Exam 2012", "Recipient of the esteemed Talentpool Scholarship.")}
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/achievements/", page("/achievements/", "Awards & Achievements | Sayedul Abrar",
                           "Awards won by Sayedul Abrar, including 1st place for Best Productive and Best Innovative at the Annual PMD Iconic Award 2025 and a scholarly publication award.",
                           ach_body, ld=[crumb_ld([("Home", "/"), ("Achievements", "/achievements/")])]))

# ---------- EDUCATION ----------
edu_body = f"""<main id="main">
{phead([("Home", "/"), ("Education", None)], "Education", "Bachelor of Pharmacy from Daffodil International University, built on a science background from secondary school onward.")}
  <section class="band">
    <div class="wrap">
      <div class="stack">
{entry("2019 – 2023", "Bachelor of Pharmacy (B.Pharm)", "Daffodil International University · Major: Pharmacy · CGPA 3.77 out of 4.00", "Passing year: 2023.")}
{entry("2015 – 2017", "Higher Secondary Certificate, Science", "Tamirul Millat Kamil Madrasah, Tongi, Gazipur · GPA 5.00 out of 5.00", "Passing year: 2017.")}
{entry("2007 – 2015", "Secondary School Certificate, Science", "Sunna Sammilita Alim Madrasah, Tangail · GPA 4.83 out of 5.00", "Passing year: 2015.")}
{entry("2012", "JDC / JSC", "Sunna Sammilita Alim Madrasah")}
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/education/", page("/education/", "Sayedul Abrar | Department of Pharmacy, Daffodil International University",
                                       "Sayedul Abrar (Abrar) is a Bachelor of Pharmacy graduate of Daffodil International University. Explore his Department of Pharmacy education, academic record and qualifications.",
                        edu_body, ld=[crumb_ld([("Home", "/"), ("Education", "/education/")])]))

# ---------- PUBLICATIONS ----------
pub_body = f"""<main id="main">
{phead([("Home", "/"), ("Publications", None)], "Publications, Certifications &amp; Workshops", "Published research and the professional learning behind the work in brand strategy, sales, public speaking and generative AI.")}
  <section class="band">
    <div class="wrap">
      <h2 class="sec-h">Publication</h2>
      <div class="stack">
{entry("Research paper", "Emerging Promise of Computational Techniques in Anti Cancer Research: At a Glance", "Listed in the Publications section of Sayedul Abrar's LinkedIn profile", level="h3")}
      </div>
    </div>
  </section>
  <section class="band deep" id="certifications">
    <div class="wrap">
      <h2 class="sec-h">Certifications</h2>
      <div class="cards">
{card("Generative AI for Marketing", "Professional Certificate, American Marketing Association, via LinkedIn Learning.")}
{card("Sales Management Foundations", "Professional Certificate, The Sales Management Association, via LinkedIn Learning.")}
{card("Public Speaking Skills", "Professional Certificate, Toastmasters International, via LinkedIn Learning.")}
{card("Career Essentials in Project Management", "Microsoft, via LinkedIn Learning.")}
{card("Marketing Strategy", "Coursera.")}
{card("Market Research and Consumer Behavior", "Coursera.")}
{card("Generative AI in Healthcare: Transforming Bedside Outcomes", "LinkedIn Learning.")}
{card("Master Microsoft PowerPoint", "LinkedIn Learning.")}
{card("Master Microsoft Excel", "LinkedIn Learning.")}
{card("The Art of Negotiation", "LinkedIn Learning.")}
{card("AI Essentials for Marketers", "LinkedIn Learning.")}
{card("Nano Tips for Using ChatGPT for Marketers with Ross Simmonds", "LinkedIn Learning.")}
{card("How to use ChatGPT for Content Creation", "LinkedIn Learning.")}
      </div>
    </div>
  </section>
  <section class="band" id="workshops">
    <div class="wrap">
      <h2 class="sec-h">Seminars &amp; workshops</h2>
      <div class="cards">
{card("Mastering Presentation Skills for Effective Brand Communication", "Conducted by Briddhi, organised by Opsonin Pharma.")}
{card("Strategic Marketing &amp; Brand Management", "Workshop conducted by Toss, organised by Navana Pharma.")}
{card("Unleash Your True Potential", "Training session organised by Bangladesh Society for Human Resources Management (BSHRM).")}
{card("Failures Talk DIU Edition", "Learning session, as organiser and volunteer.")}
{card("Road To Corporate", "Learning workshop, as organiser and volunteer, by the Career Development Center (CDC).")}
{card("Dynamic Professional Mastering Impression Management", "Certified by HRDI's online learning session.")}
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/publications/", page("/publications/", "Sayedul Abrar | Pharmacy Research, Publications & Certifications",
                                             "Explore Sayedul Abrar’s pharmacy research, scholarly publication, professional certifications and training in pharmaceutical marketing, product management, public speaking and generative AI.",
                           pub_body, ld=[crumb_ld([("Home", "/"), ("Publications", "/publications/")])]))

# ---------- COMMUNITY ----------
com_body = f"""<main id="main">
{phead([("Home", "/"), ("Community", None)], "Community &amp; Social Contribution", "Founding a foundation and leading student programmes, expos and career events across Dhaka.")}
  <section class="band">
    <div class="wrap">
      <div class="stack">
{entry("Founder", "Agrojatra Foundation", "Founded by Sayedul Abrar")}
{entry("2022 – 2023", "Admission.ac, Team Leader", "UK &amp; USA Education Expo, International Education Expo, Cucas China Online Exhibition", "Led three expos and organised many other education programmes.")}
{entry("2022 – 2023", "DIU Pharmacia Club, Organizing Secretary", "Daffodil International University", "Organised events that raise awareness of the importance of pharmacy in healthcare and give students and professionals a platform to share knowledge.")}
{entry("2022 – 2023", "Career Development Center (CDC)", "Career Ambassador and Volunteer Leader", "Organiser and volunteer leader for the Road To Corporate learning workshop.")}
{entry("2022", "Failures Talk DIU Edition", "Organiser and volunteer", "Learning session for students.")}
{entry("2021 – 2022", "Human Resource Development Institute (HRDI)", "Arteries and Campus Ambassador", "Campus programmes and learning sessions.")}
      </div>
    </div>
  </section>
  {cta()}
</main>"""
add("/community/", page("/community/", "Sayedul Abrar | Pharmacy Alumni & Community Engagement",
                                       "Learn about Sayedul Abrar’s community and student leadership, including pharmacy-related activities, Daffodil International University connections, education events and Agrojatra Foundation.",
                        com_body, ld=[crumb_ld([("Home", "/"), ("Community", "/community/")])]))

# ---------- CONTACT ----------
ct_body = f"""<main id="main">
{phead([("Home", "/"), ("Contact", None)], "Contact Sayedul Abrar", "For professional collaboration, pharmaceutical marketing or networking, contact me by email, WhatsApp, Facebook, Instagram or LinkedIn.")}
  <section class="band">
    <div class="wrap ctbox">
      <div>
        <h2 class="sec-h">Email</h2>
        <div class="mail"><code id="mail">{EMAIL}</code><button class="cp" id="copy" type="button">Copy email</button></div>
        <p><a href="mailto:{EMAIL}">Open in your email app</a></p>
      </div>
      <div>
        <h2 class="sec-h">Connect with me</h2>
        <p style="color:var(--muted);margin-bottom:16px">Choose your preferred channel below.</p>
        {SOCIAL}
        <p style="color:var(--muted);margin-top:18px">WhatsApp: 01949899373 · Instagram: @abrar_abdur_rahman</p>
        <h2 class="sec-h" style="margin-top:28px">Location</h2>
        <p style="color:var(--muted)">Dhaka, Bangladesh</p>
      </div>
    </div>
  </section>
</main>"""
add("/contact/", page("/contact/", "Contact Sayedul Abrar (Abrar) | Pharmacist & Pharma Executive",
                                   "Contact Sayedul Abrar in Bangladesh for pharmaceutical product management, Finix and Finix MUPS brand-related professional collaboration, pharmacy alumni connections or speaking opportunities.",
                      ct_body, ld=[crumb_ld([("Home", "/"), ("Contact", "/contact/")])]))


# ---------- PAGES EDITED BY HAND ----------
# Every page except the ones this script owns (about, achievements, blog, vlog) is
# edited directly in its index.html. For those, the script only refreshes the shared
# header, footer and script tag so the menu and footer are identical everywhere, and
# lists them in the sitemap. Hand-edited pages therefore always win over the older
# builders above.
import re as _re
OWNED = {"/about/", "/achievements/"}
old_lastmod = {}
_sm = os.path.join(IMG_ROOT, "sitemap.xml")
if os.path.exists(_sm):
    with open(_sm, encoding="utf-8") as fh:
        for loc, lm in _re.findall(r"<loc>https://sayedulabrar\.site(.*?)</loc><lastmod>(.*?)</lastmod>", fh.read()):
            old_lastmod[loc] = lm
static = ["/"]
for fp in sorted(glob.glob(os.path.join(IMG_ROOT, "**", "index.html"), recursive=True)):
    rel = "/" + os.path.relpath(os.path.dirname(fp), IMG_ROOT).replace(os.sep, "/").strip(".") 
    rel = "/" if rel in ("/", "//") else rel.rstrip("/") + "/"
    if rel == "/":
        pass
    if rel in OWNED or rel.startswith(("/blog/", "/vlog/", "/_src/")) or rel in ("/blog/", "/vlog/"):
        continue
    if rel != "/" and rel not in static:
        static.append(rel)
for sp in static:
    fp = os.path.join(IMG_ROOT, "index.html" if sp == "/" else os.path.join(sp.strip("/"), "index.html"))
    with open(fp, encoding="utf-8") as fh:
        t = fh.read()
    cur = sp if sp in dict(NAV) else ("/portfolio/" if sp.startswith("/brands/") else sp)
    t = _re.sub(r'<a class="skip".*?</header>', lambda m: header(cur), t, count=1, flags=_re.S)
    t = _re.sub(r'<footer.*?</footer>\s*<script src="/assets/site.js[^"]*" defer></script>|<footer.*?</footer>', lambda m: FOOTER, t, count=1, flags=_re.S)
    t = _re.sub(r'href="/assets/style\.css[^"]*"', 'href="/assets/style.css?v=%s"' % CSS_V, t)
    t = _re.sub(r'src="/assets/site\.js[^"]*"', 'src="/assets/site.js?v=%s"' % JS_V, t)
    if sp == "/":
        # blended sunset hero photo and the blog / vlog cards
        t = _re.sub(r'<div class="arch"><img [^>]*></div>',
                    '<div class="hero-photo"><img src="/assets/img/hero-sayedul-abrar.jpg" alt="%s" width="800" height="1000" fetchpriority="high"></div>' % HERO_ALT, t, count=1)
        if 'href="/blog/"' not in t.split("<h2 class=\"h\">Explore</h2>")[-1]:
            t = t.replace('<b>View achievements →</b></a>\n',
                '<b>View achievements →</b></a>\n        <a class="card link" href="/blog/"><h3>Medical &amp; Pharma Blog</h3><p>Written articles with pictures and explanations on medicine and pharmacy.</p><b>Read the blog →</b></a>\n        <a class="card link" href="/vlog/"><h3>Daily Vlog</h3><p>Day-by-day moments from work, learning and life.</p><b>Watch the vlog →</b></a>\n', 1)
    add(sp, t, sitemap=True, lastmod=old_lastmod.get(sp, TODAY))

# ---------- BLOG + VLOG ----------
def load_posts(kind):
    posts = []
    for f in sorted(glob.glob(os.path.join(CONTENT, kind, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            p = json.load(fh)
        p.setdefault("slug", os.path.splitext(os.path.basename(f))[0])
        posts.append(p)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_body(blocks):
    out = []
    for b in blocks:
        t = b.get("type", "p")
        if t == "p":
            out.append(f"<p>{esc(b['text'], quote=False)}</p>")
        elif t == "h2":
            out.append(f"<h2>{esc(b['text'], quote=False)}</h2>")
        elif t == "h3":
            out.append(f"<h3>{esc(b['text'], quote=False)}</h3>")
        elif t == "quote":
            out.append(f"<blockquote>{esc(b['text'], quote=False)}</blockquote>")
        elif t == "ul":
            out.append("<ul>" + "".join(f"<li>{esc(x, quote=False)}</li>" for x in b["items"]) + "</ul>")
        elif t == "img":
            w, h = img_size(b["src"])
            cap = f"<figcaption>{esc(b['caption'], quote=False)}</figcaption>" if b.get("caption") else ""
            out.append(f'<figure><img src="{b["src"]}" alt="{esc(b.get("alt", ""))}" width="{w}" height="{h}" loading="lazy">{cap}</figure>')
    return "\n".join(out)


KINDS = {
    "blog": {
        "path": "/blog/", "label": "Pharma Blog", "h1": "Medical &amp; Pharma Blog",
        "intro": "Written articles on medicines, pharmacy and the pharmaceutical industry, with pictures and explanations.",
        "title": "Medical & Pharma Blog | Sayedul Abrar",
        "desc": "Articles on medicine, pharmacy and the pharmaceutical industry by Sayedul Abrar, a Dhaka pharmacist, with pictures and clear explanations.",
        "empty_h": "The first article is on its way",
        "empty_p": "Articles about medicine and pharmacy, with pictures and explanations, will appear here.",
        "note": "This blog shares general information about medicines and pharmacy. It is not medical advice. Please ask a doctor or pharmacist about your own treatment.",
        "strip_label": "Blog topic pictures, sliding from left to right",
    },
    "vlog": {
        "path": "/vlog/", "label": "Daily Vlog", "h1": "Daily Vlog",
        "intro": "Day-by-day moments from work, learning and life as a pharmacist and brand manager.",
        "title": "Daily Vlog | Sayedul Abrar",
        "desc": "Daily vlog by Sayedul Abrar: pictures, short write-ups and videos from work, learning and life as a pharmacist and brand manager in Bangladesh.",
        "empty_h": "The first vlog is on its way",
        "empty_p": "Daily pictures, notes and videos will appear here.",
        "note": "",
        "strip_label": "Vlog moments, sliding from left to right",
    },
}

MOMENTS = [
    {"src": "/assets/img/moment-sunset-walk.jpg", "alt": "Sayedul Abrar in a navy suit standing on a quiet road at sunset", "caption": "Sunset portrait."},
    {"src": "/assets/img/award-opsonin-conference-2026-trophies.jpg", "alt": "Sayedul Abrar holding two award trophies at the Opsonin Pharma Conference 2026", "caption": "Opsonin Pharma conference."},
    {"src": "/assets/img/award-pmd-iconic-2025-stage.jpg", "alt": "Annual PMD Iconic Award 2025 stage", "caption": "Annual PMD Iconic Award 2025."},
]


def post_card(p, kind):
    cover = ""
    if p.get("cover"):
        w, h = img_size(p["cover"])
        cover = f'<img src="{p["cover"]}" alt="{esc(p.get("cover_alt", p["title"]))}" width="{w}" height="{h}" loading="lazy">'
    tags = "".join(f"<li>{esc(t, quote=False)}</li>" for t in p.get("tags", [])[:3])
    tg = f'<ul class="tagline">{tags}</ul>' if tags else ""
    return f"""<article class="pc"><a href="/{kind}/{p['slug']}/">{cover}<div class="bd"><time datetime="{p['date']}">{nice_date(p['date'])}</time><h2>{esc(p['title'], quote=False)}</h2><p>{esc(p.get('summary', ''), quote=False)}</p>{tg}</div></a></article>"""


for kind, cfg in KINDS.items():
    posts = load_posts(kind)
    path = cfg["path"]
    items = [{"src": p["cover"], "alt": p.get("cover_alt", p["title"]), "caption": p["title"], "href": f"/{kind}/{p['slug']}/"}
             for p in posts if p.get("cover")]
    if kind == "vlog" or not items:
        items = items + MOMENTS  # blog shows these until it has posts with cover pictures
    strip_html = ""
    if items:
        strip_html = f"""<section class="band deep" aria-label="Pictures"><div class="wrap"><h2 class="sec-h">{'Featured pictures' if kind == 'blog' else 'Recent moments'}</h2></div>{strip(items, cfg['strip_label'])}</section>"""
    note = f'<p class="note">{esc(cfg["note"], quote=False)}</p>' if cfg["note"] else ""
    if posts:
        listing = '<div class="posts">' + "".join(post_card(p, kind) for p in posts) + "</div>"
    else:
        listing = f'<div class="empty"><h2>{cfg["empty_h"]}</h2><p>{cfg["empty_p"]}</p></div>'
    body = f"""<main id="main">
{phead([("Home", "/"), (cfg['label'], None)], cfg['h1'], cfg['intro'])}
  {strip_html}
  <section class="band">
    <div class="wrap">
      {note}
      <h2 class="sec-h">{'Latest articles' if kind == 'blog' else 'Latest vlogs'}</h2>
      {listing}
    </div>
  </section>
  {cta()}
</main>"""
    indexable = bool(posts)
    last = posts[0]["date"] if posts else TODAY
    add(path, page(path, cfg["title"], cfg["desc"], body,
                   ld=[crumb_ld([("Home", "/"), (cfg["label"], path)])], noindex=not indexable),
        sitemap=indexable, lastmod=last)

    for p in posts:
        ppath = f"/{kind}/{p['slug']}/"
        url = f"{BASE}{ppath}"
        video = ""
        if p.get("youtube"):
            video = f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{esc(p["youtube"])}" title="{esc(p["title"])}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
        cover = ""
        if p.get("cover") and p.get("show_cover", True):
            w, h = img_size(p["cover"])
            cover = f'<figure><img src="{p["cover"]}" alt="{esc(p.get("cover_alt", p["title"]))}" width="{w}" height="{h}" fetchpriority="high"></figure>'
        tags = "".join(f"<li>{esc(t, quote=False)}</li>" for t in p.get("tags", []))
        tg = f'<ul class="tagline">{tags}</ul>' if tags else ""
        disc = f'<p class="note" style="margin-top:36px">{esc(cfg["note"], quote=False)}</p>' if cfg["note"] else ""
        pbody = f"""<main id="main">
{phead([("Home", "/"), (cfg['label'], path), (esc(p['title'], quote=False), None)], esc(p['title'], quote=False), esc(p.get('summary', ''), quote=False))}
  <section class="band">
    <div class="wrap">
      <article class="article">
        <div class="meta"><time datetime="{p['date']}">{nice_date(p['date'])}</time>{tg}</div>
        {video}{cover}
        {render_body(p.get('body', []))}
        {disc}
        <p style="margin-top:28px"><a class="more" href="{path}">Back to {cfg['label']}</a></p>
      </article>
    </div>
  </section>
</main>"""
        og = p.get("cover") or "/assets/img/og-image.png"
        add(ppath, page(ppath, f"{p['title']} | {cfg['label']} | {NAME}", p.get("summary", cfg["desc"]), pbody,
                        ld=[post_ld(p, kind, url), crumb_ld([("Home", "/"), (cfg["label"], path), (p["title"], ppath)])],
                        og_type="article", nav=path, og_image=og),
            sitemap=True, lastmod=p.get("updated", p["date"]))

# ---------- write everything ----------
for path, (text, _, _) in pages.items():
    d = OUT if path == "/" else os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(text)

nf = page("/404.html", "Page not found | Sayedul Abrar", "This page could not be found. Return to the Sayedul Abrar home page.",
          """<main id="main"><section class="phead"><div class="wrap"><h1>Page not found</h1><p>The page you wanted does not exist or has moved.</p></div></section>
<section class="band"><div class="wrap"><p><a class="more" href="/">Go to the home page</a></p></div></section></main>""",
          noindex=True)
with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
    f.write(nf)

if not os.path.exists(os.path.join(IMG_ROOT, "robots.txt")):
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
elif OUT != IMG_ROOT:
    import shutil
    shutil.copy(os.path.join(IMG_ROOT, "robots.txt"), os.path.join(OUT, "robots.txt"))

urls = "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>{m}</lastmod></url>\n" for p, (_, s, m) in pages.items() if s)
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

XSL = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Sitemap | Sayedul Abrar</title>
<style>
:root{--bg:#2B2D3F;--bg2:#232536;--fg:#F2F3F8;--muted:#A9ADC2;--line:#44476A;--accent:#FFA91F}
@media (prefers-color-scheme:light){:root{--bg:#F3F4F9;--bg2:#E8EAF2;--fg:#1C1E2D;--muted:#5A5F78;--line:#D3D6E4;--accent:#C26E00}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 Poppins,system-ui,sans-serif}
header{background:var(--bg2);border-bottom:1px solid var(--line);padding:14px 16px}
header a{font:700 24px "Dancing Script","Brush Script MT",cursive;color:var(--accent);text-decoration:none}
main{max-width:900px;margin:0 auto;padding:36px 16px 56px}
h1{font-size:clamp(26px,5vw,40px);line-height:1.15;margin:0 0 10px}
p{color:var(--muted);margin:0 0 26px}
.list{border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:1fr auto;gap:12px;padding:14px 0;border-bottom:1px solid var(--line);align-items:center}
.row a{color:var(--fg);text-decoration:none;overflow-wrap:anywhere;font-weight:500}
.row a:hover{color:var(--accent)}
.row time{color:var(--muted);font-size:13px;white-space:nowrap}
@media(max-width:520px){.row{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><a href="/">Sayedul Abrar</a></header>
<main>
<h1>Sitemap</h1>
<p><xsl:value-of select="count(s:urlset/s:url)"/> pages on sayedulabrar.site. Search engines read this file to find every page.</p>
<div class="list">
<xsl:for-each select="s:urlset/s:url">
<div class="row"><a href="{s:loc}"><xsl:value-of select="s:loc"/></a><time><xsl:value-of select="s:lastmod"/></time></div>
</xsl:for-each>
</div>
</main>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
with open(os.path.join(OUT, "sitemap.xsl"), "w") as f:
    f.write(XSL)

print("built", len(pages), "pages;", sum(1 for v in pages.values() if v[1]), "in sitemap")
