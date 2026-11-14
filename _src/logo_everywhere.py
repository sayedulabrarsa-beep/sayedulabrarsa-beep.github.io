"""Put the official SA logo in the header and footer of every page, keep favicons consistent,
and use one copyright line. Learning and Portfolio pages are never touched.
Run from anywhere: python3 _src/logo_everywhere.py   (safe to re-run)
"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
V = "sa-logo-20261114"
SKIP = ("_src/", "learning/", "portfolio/", ".github/", "node_modules/")

ICONS = (
    f'<link rel="icon" href="/favicon.ico?v={V}" sizes="any">'
    f'<link rel="icon" type="image/png" sizes="48x48" href="/assets/icons/favicon-48x48.png?v={V}">'
    f'<link rel="icon" type="image/png" sizes="96x96" href="/assets/icons/favicon-96x96.png?v={V}">'
    f'<link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png?v={V}">'
    f'<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png?v={V}">'
    f'<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png?v={V}">'
    f'<link rel="manifest" href="/site.webmanifest?v={V}">'
    '<style id="logo-mark-css">.logo-mark{display:inline-block;width:1.3em;height:1.3em;border-radius:50%;'
    'vertical-align:-.28em;margin-right:.38em;box-shadow:0 0 0 1px rgba(194,140,30,.35)}'
    '@media (max-width:420px){.logo-mark{width:1.15em;height:1.15em}}</style>'
)
MARK = ('<img class="logo-mark" src="/assets/img/sayedul-abrar-logo-badge-96.webp" '
        'srcset="/assets/img/sayedul-abrar-logo-badge-96.webp 1x, /assets/img/sayedul-abrar-logo-badge-192.webp 2x" '
        'alt="Sayedul Abrar SA logo" width="34" height="34" decoding="async">')
CR = ('<div class="cr">© <span id="year">2026</span> Sayedul Abrar. All rights reserved. '
      'The SA monogram is the personal logo of Sayedul Abrar and may not be used without permission.</div>')

icon_re = re.compile(r'<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>\s*')
changed = 0
for p in sorted(R.rglob("*.html")):
    rel = p.relative_to(R).as_posix()
    if rel.startswith(SKIP):
        continue
    s = o = p.read_text(encoding="utf-8")
    if "<head" not in s:
        continue
    # favicons: one consistent block in every page head
    s = icon_re.sub("", s)
    s = re.sub(r'<style id="logo-mark-css">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", ICONS + "</head>", 1)
    # logo image in header/footer brand links (text kept for SEO)
    s = s.replace(MARK, "")
    s = re.sub(r'(<a class="logo" href="/"[^>]*>)(Sayedul Abrar</a>)', lambda m: m.group(1) + MARK + m.group(2), s)
    # one copyright line
    s = re.sub(r'<div class="cr">.*?</div>', CR, s, count=1, flags=re.S)
    if s != o:
        p.write_text(s, encoding="utf-8")
        changed += 1
print("pages updated:", changed)
