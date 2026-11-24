#!/usr/bin/env python3
"""Add complete Google ImageObject rights metadata to first-party editorial images.

Enriches existing JSON-LD ImageObject nodes (including BlogPosting.image) and
creates supplemental ImageObjects for first-party editorial images referenced
only in HTML. Company/product packshots and third-party images are not assigned
personal rights metadata.
"""
import re, json, html, pathlib
from urllib.parse import urlparse

R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
PERSON = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
OWN = re.compile(r"^/assets/img/(blog/|mirinja-valley/|chapainawabganj/|personal-moments/)")
SKIP = re.compile(r"(logo|favicon|badge|/icons/|-w\d+\.)", re.I)
NAME = re.compile(r"(Sayedul Abrar|সাইয়্যেদুল আবরার|সাইদুল আব্রার|সাইয়েদুল আবরার)")
BLOCK = re.compile(r'<script type="application/ld\+json" id="image-credits">.*?</script>', re.S)
LICENSE = SITE + "/sayedul-abrar-logo/#copyright"
ACQUIRE = SITE + "/contact/"

def _is_json(raw):
    try:
        json.loads(raw)
        return True
    except Exception:
        return False

def image_path(value):
    if not isinstance(value, str):
        return ""
    return urlparse(value).path

def enrich(node):
    if isinstance(node, list):
        return [enrich(x) for x in node]
    if not isinstance(node, dict):
        return node
    out = {k: enrich(v) for k, v in node.items()}
    if out.get("@type") == "ImageObject":
        path = image_path(out.get("contentUrl") or out.get("url"))
        if OWN.match(path) and not SKIP.search(path):
            out.setdefault("creator", PERSON)
            out.setdefault("creditText", "Sayedul Abrar (sayedulabrar.site)")
            out.setdefault("copyrightNotice", "© 2026 Sayedul Abrar")
            out.setdefault("license", LICENSE)
            out.setdefault("acquireLicensePage", ACQUIRE)
    return out

def collect_image_objects(node, found):
    if isinstance(node, list):
        for item in node:
            collect_image_objects(item, found)
    elif isinstance(node, dict):
        if node.get("@type") == "ImageObject":
            u = node.get("contentUrl") or node.get("url")
            if isinstance(u, str):
                found.add(u.split("?")[0])
        for value in node.values():
            collect_image_objects(value, found)

changed = total = 0
for p in sorted(R.glob("**/index.html")):
    rel = p.relative_to(R).as_posix()
    if rel.startswith(("_src/", "learning/", "portfolio/", "node_modules/")):
        continue
    s = p.read_text(encoding="utf-8")
    if re.search(r'name="robots" content="[^"]*noindex', s) or 'http-equiv="refresh"' in s:
        continue

    # Enrich every valid JSON-LD block without changing unrelated page markup.
    def update_ld(match):
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)
        return match.group(0).replace(raw, json.dumps(enrich(data), ensure_ascii=False, separators=(",", ":")))

    s2 = re.sub(r'(<script type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)',
                lambda m: m.group(1) + json.dumps(enrich(json.loads(m.group(2))), ensure_ascii=False, separators=(",", ":")) + m.group(3)
                if _is_json(m.group(2)) else m.group(0), s)

    base = BLOCK.sub("", s2)
    covered = set()
    for raw in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', base, re.S):
        try:
            collect_image_objects(json.loads(raw), covered)
        except Exception:
            pass

    items, seen = [], set()
    for tag in re.findall(r"<img\b[^>]*>", base):
        m = re.search(r'\ssrc="([^"]+)"', tag)
        if not m:
            continue
        u = m.group(1).split("?")[0]
        if not OWN.match(u) or SKIP.search(u) or u.endswith(".svg") or u in seen:
            continue
        if not (R / u.lstrip("/")).exists():
            continue
        full = SITE + u
        if full in covered:
            continue
        seen.add(u)
        alt = re.search(r'\salt="([^"]*)"', tag)
        alt = html.unescape(alt.group(1)).strip() if alt else ""
        o = {"@type": "ImageObject", "contentUrl": full, "url": full,
             "creator": PERSON, "creditText": "Sayedul Abrar (sayedulabrar.site)",
             "copyrightNotice": "© 2026 Sayedul Abrar", "license": LICENSE,
             "acquireLicensePage": ACQUIRE}
        if alt:
            o["name"] = alt[:150]
            o["description"] = alt
        if NAME.search(alt) and not u.startswith("/assets/img/blog/"):
            o["about"] = {"@id": SITE + "/#person"}
        items.append(o)

    # The dedicated logo page publishes the personal SA mark as a first-party SVG.
    if rel == "sayedul-abrar-logo/index.html":
        svg = "/assets/img/sayedul-abrar-logo.svg"
        if (R / svg.lstrip("/")).exists() and SITE + svg not in covered:
            items.append({"@type": "ImageObject", "contentUrl": SITE + svg, "url": SITE + svg,
                          "name": "Official Sayedul Abrar SA monogram logo (SVG)",
                          "creator": PERSON, "creditText": "Sayedul Abrar (sayedulabrar.site)",
                          "copyrightNotice": "© 2026 Sayedul Abrar",
                          "license": LICENSE, "acquireLicensePage": ACQUIRE})

    new = base
    if items:
        block = '<script type="application/ld+json" id="image-credits">' + json.dumps(
            {"@context": "https://schema.org", "@graph": items}, ensure_ascii=False, separators=(",", ":")) + "</script>"
        new = base.replace("</head>", block + "</head>", 1)
        total += len(items)
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed += 1
print(f"image credits: {total} supplemental images; {changed} pages updated")
