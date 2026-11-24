#!/usr/bin/env python3
"""Add complete Google ImageObject rights metadata to first-party editorial images.

Enriches existing JSON-LD ImageObject nodes (the BlogPosting image property is
what Google evaluates) and creates supplemental ImageObjects for first-party
editorial images that are only referenced in HTML. It does not assign rights
to company/product packshots or third-party images.
"""
import re, json, html, pathlib
from urllib.parse import urlparse

R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sayedulabrar.site"
PERSON = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
OWN = re.compile(r"^/assets/img/(blog/|mirinja-valley/|chapainawabganj/|personal-moments/)")
SKIP = re.compile(r"(logo|favicon|badge|/icons/|-w\\d+\\.)", re.I)
NAME = re.compile(r"(Sayedul Abrar|সাইয়্যেদুল আবরার|সাইদুল আব্রার|সাইয়েদুল আবরার)")
BLOCK = re.compile(r'<script type="application/ld\\+json" id="image-credits">.*?</script>', re.S)
REQUIRED = ("creditText", "copyrightNotice", "license", "acquireLicensePage")
LICENSE = SITE + "/sayedul-abrar-logo/#copyright"
ACQUIRE = SITE + "/contact/"

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

changed = total = 0
for p in sorted(R.glob("**/index.html")):
    rel = p.relative_to(R).as_posix()
    if rel.startswith(("_src/", "learning/", "portfolio/", "node_modules/")):
        continue
    s = p.read_text(encoding="utf-8")
    if re.search(r'name="robots" content="[^"]*noindex', s) or 'http-equiv="refresh"' in s:
        continue

    # Enrich ImageObject nodes inside the primary Article/BlogPosting JSON-LD.
    def update_ld(match):
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)
        updated = enrich(data)
        return match.group(0).replace(raw, json.dumps(updated, ensure_ascii=False, separators=(",", ":")))
    s2 = re.sub(r'(<script type="application/ld\\+json"[^>]*>)([\\s\\S]*?)(</script>)',
                lambda m: m.group(1) + (json.dumps(enrich(json.loads(m.group(2))), ensure_ascii=False, separators=(",", ":")) if _valid_json(m.group(2)) else m.group(2)) + m.group(3), s)

    base = BLOCK.sub("", s2)
    ld = " ".join(re.findall(r'<script type="application/ld\\+json"[^>]*>(.*?)</script>', base, re.S))
    items, seen = [], set()
    for tag in re.findall(r"<img\\b[^>]*>", base):
        m = re.search(r'\\ssrc="([^"]+)"', tag)
        if not m:
            continue
        u = m.group(1).split("?")[0]
        if not OWN.match(u) or SKIP.search(u) or u.endswith(".svg") or u in seen:
            continue
        if not (R / u.lstrip("/")).exists():
            continue
        # Existing structured ImageObjects have already been enriched above.
        if u in ld and all(k in ld for k in REQUIRED):
            continue
        seen.add(u)
        alt = re.search(r'\\salt="([^"]*)"', tag)
        alt = html.unescape(alt.group(1)).strip() if alt else ""
        o = {"@type": "ImageObject", "contentUrl": SITE + u, "url": SITE + u,
             "creator": PERSON, "creditText": "Sayedul Abrar (sayedulabrar.site)",
             "copyrightNotice": "© 2026 Sayedul Abrar", "license": LICENSE,
             "acquireLicensePage": ACQUIRE}
        if alt:
            o["name"] = alt[:150]
            o["description"] = alt
        if NAME.search(alt) and not u.startswith("/assets/img/blog/"):
            o["about"] = {"@id": SITE + "/#person"}
        items.append(o)

    # The dedicated logo page also publishes the editable SVG mark as a first-party asset.
    if rel == "sayedul-abrar-logo/index.html":
        svg = "/assets/img/sayedul-abrar-logo.svg"
        if (R / svg.lstrip("/")).exists():
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
