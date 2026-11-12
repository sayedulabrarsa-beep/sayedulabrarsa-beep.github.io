#!/usr/bin/env python3
"""One-off: split the four single-page EN+BN articles into a separate English page and a separate, indexable Bangla page."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://sayedulabrar.site"
SLUGS = ["when-to-take-ppi-before-meals", "drug-vs-medicine", "how-to-take-iron-tablets-properly", "iron-deficiency-vs-anemia"]
def span(s, start):
    d = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[start:]):
        d += -1 if m.group(1) else 1
        if d == 0: return start, start + m.end()
    raise SystemExit("unbalanced")
def txt(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
def cut(t, n=158):
    if len(t) <= n: return t
    c = t[:n]; k = max(c.rfind("। "), c.rfind(". "), c.rfind("? "))
    return c[:k+1] if k > 70 else c.rsplit(" ", 1)[0] + "…"
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
def ld_fix(s, fn):
    def sub(m):
        j = fn(json.loads(m.group(2)))
        return "" if j is None else m.group(1) + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + m.group(3)
    return LD.sub(sub, s)
for slug in SLUGS:
    p = R/"blog"/slug/"index.html"; s = p.read_text(encoding="utf-8")
    if 'id="pane-bn"' not in s: print("skip", slug); continue
    en_url, bn_url = f"/blog/{slug}/", f"/blog/{slug}-bangla/"
    a0 = s.index('<div class="lang-pane" id="pane-en"'); b0 = s.index('<div class="lang-pane" id="pane-bn"')
    a1 = b0; b1 = s.index("</article>", b0)   # panes are siblings inside <article>; robust even if a pane has an unclosed div
    pane_bn = s[b0:b1]
    bn_h1 = txt(re.search(r"<h1[^>]*>(.*?)</h1>", pane_bn, re.S).group(1))
    sub_m = re.search(r'<p class="article-subtitle"[^>]*>(.*?)</p>', pane_bn, re.S)
    bn_desc = cut(txt(sub_m.group(1))) if sub_m else bn_h1
    old_js = re.search(r"<script>\(function\(\)\{var K='sa-blog-lang'.*?</script>", s, re.S).group(0)
    def js(cur):
        return ("<script>(function(){var E='%s',N='%s';document.querySelectorAll('.language-switch button').forEach(function(b){b.addEventListener('click',function(){var t=b.dataset.lang==='bn'?N:E;if(location.pathname!==t)location.href=t})});%s})()</script>"
                % (en_url, bn_url, "if(location.hash==='#bn')location.replace(N)" if cur == "en" else ""))
    alt = (f'<link rel="alternate" hreflang="en" href="{B}{en_url}"><link rel="alternate" hreflang="bn" href="{B}{bn_url}">'
           f'<link rel="alternate" hreflang="x-default" href="{B}{en_url}">')
    canon = f'<link rel="canonical" href="{B}{en_url}">'
    assert canon in s
    # ---------- English page ----------
    en = s[:b0] + s[b1:]
    en = en.replace(old_js, js("en")).replace(canon, canon + alt)
    def en_ld(j):
        t = json.dumps(j, ensure_ascii=False).replace('"inLanguage": ["en", "bn"]', '"inLanguage": "en"')
        return json.loads(t)
    en = ld_fix(en, en_ld)
    # ---------- Bangla page ----------
    bn = s[:a0] + s[a1:b0] + pane_bn.replace(' data-pane="bn" hidden>', ' data-pane="bn">', 1) + s[b1:]
    assert 'data-pane="bn" hidden' not in bn
    bn = bn.replace('<html lang="en">', '<html lang="bn">', 1)
    bn = re.sub(r"<title>.*?</title>", lambda m: f"<title>{html.escape(bn_h1, quote=False)} | Sayedul Abrar</title>", bn, count=1, flags=re.S)
    q = html.escape(bn_desc, quote=True); qt = html.escape(bn_h1, quote=True)
    bn = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + q + m.group(2), bn, count=1)
    for k in ("og:title", "twitter:title"): bn = re.sub(r'((?:property|name)="%s" content=")[^"]*(")' % k, lambda m: m.group(1) + qt + m.group(2), bn, count=1)
    for k in ("og:description", "twitter:description"): bn = re.sub(r'((?:property|name)="%s" content=")[^"]*(")' % k, lambda m: m.group(1) + q + m.group(2), bn, count=1)
    bn = bn.replace(f'og:url" content="{B}{en_url}"', f'og:url" content="{B}{bn_url}"').replace('og:locale" content="en_BD"', 'og:locale" content="bn_BD"')
    bn = bn.replace(canon, f'<link rel="canonical" href="{B}{bn_url}">' + alt)
    bn = bn.replace('data-lang="en" aria-pressed="true"', 'data-lang="en" aria-pressed="false"').replace('data-lang="bn" aria-pressed="false"', 'data-lang="bn" aria-pressed="true"')
    bn = bn.replace(old_js, js("bn"))
    def bn_ld(j):
        nodes = j.get("@graph") if isinstance(j, dict) and "@graph" in j else None
        if nodes is not None: j["@graph"] = [n for n in nodes if n.get("@type") != "FAQPage"]
        elif isinstance(j, dict) and j.get("@type") == "FAQPage": return None
        t = json.dumps(j, ensure_ascii=False).replace(B + en_url, B + bn_url)
        t = t.replace('"inLanguage": ["en", "bn"]', '"inLanguage": "bn"').replace('"inLanguage": "en"', '"inLanguage": "bn"')
        j = json.loads(t)
        for n in (j.get("@graph") or [j]):
            if n.get("@type") in ("BlogPosting", "Article", "MedicalWebPage", "WebPage"):
                if "headline" in n: n["headline"] = bn_h1[:110]
                if "name" in n: n["name"] = bn_h1
                if "description" in n: n["description"] = bn_desc
                n.setdefault("inLanguage", "bn")
        return j
    bn = ld_fix(bn, bn_ld)
    p.write_text(en, encoding="utf-8"); (R/"blog"/(slug+"-bangla")/"index.html").write_text(bn, encoding="utf-8")
    print(slug, "| BN title:", bn_h1, "|", len(en), len(bn))
