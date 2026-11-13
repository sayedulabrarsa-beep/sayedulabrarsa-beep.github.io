"""Add the extra English + Bangla FAQs from _src/data/brand_faqs.json to the brand pages.

Run from the repository root:  python3 _src/brand_faq_inject.py
Safe to re-run: the added block sits between <!--faq-plus--> markers and is replaced each time,
and FAQPage schema questions are de-duplicated by question text.
"""
import html, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "_src/data/brand_faqs.json").read_text(encoding="utf-8"))
START, END = "<!--faq-plus-->", "<!--/faq-plus-->"
MODIFIED = "2026-11-13"


def esc(t):
    return html.escape(t, quote=True)


def faq_items(pairs, lang=None):
    attr = f' lang="{lang}"' if lang else ""
    return "".join(
        f'<details class="drug-faq"{attr}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>\n'
        for q, a in pairs
    )


def extra_block(d):
    refs = "".join(f'<li><a href="{esc(u)}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, u in d["refs"])
    rel = " · ".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in d["related"])
    return (
        f'{START}<h3 class="drug-faq-h" lang="bn" style="margin:22px 0 4px;font-size:17px">{esc(d["bn_heading"])}</h3>'
        f'<div class="drug-faq-list" lang="bn">\n{faq_items(d["bn"], "bn")}</div>'
        f'<p style="font-size:14px"><b>Related reading:</b> {rel}</p>'
        f'<p style="font-size:14px;margin-bottom:4px"><b>Sources for these answers</b></p>'
        f'<ol style="font-size:13px;line-height:1.6;padding-left:20px">{refs}</ol>'
        f'<p style="font-size:13px;color:var(--muted)">Reviewed against the sources above on 13 November 2026. '
        f'This is general education, not medical advice. Follow the current approved insert and your prescriber.</p>{END}'
    )


def add_schema(s, pairs):
    def fix(m):
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except ValueError:
            return m.group(0)
        found = []

        def walk(x):
            if isinstance(x, dict):
                if x.get("@type") == "FAQPage":
                    found.append(x)
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)

        walk(data)
        if not found:
            return m.group(0)
        faq = found[0]
        have = {q.get("name") for q in faq.get("mainEntity", [])}
        for q, a in pairs:
            if q not in have:
                faq.setdefault("mainEntity", []).append(
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                )
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)


def set_meta(s, d):
    old = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    s = s.replace(f"<title>{old}</title>", f"<title>{esc(d['title'])}</title>")
    for prop in ("og:title", "twitter:title"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")', lambda m: m.group(1) + esc(d["title"]) + m.group(2), s)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*(")', lambda m: m.group(1) + esc(d["description"]) + m.group(2), s)
    s = re.sub(r'"dateModified":\s*"[^"]*"', f'"dateModified":"{MODIFIED}"', s)
    return s


for slug, d in DATA.items():
    if slug.startswith("_"):
        continue
    p = ROOT / "brands" / slug / "index.html"
    s = p.read_text(encoding="utf-8")
    # remove a previous run's block and items
    s = re.sub(re.escape(START) + ".*?" + re.escape(END), "", s, flags=re.S)
    s = re.sub(r"<!--faq-plus-en-->.*?<!--/faq-plus-en-->", "", s, flags=re.S)
    i = s.index('<div class="drug-faq-list">')
    j = s.index("</div>", i)
    en = "<!--faq-plus-en-->" + faq_items(d["en"]) + "<!--/faq-plus-en-->"
    s = s[:j] + en + s[j:]
    # Bangla FAQs + sources go at the end of the FAQ drawer, after any short Q&A paragraphs
    k = s.find("</div></details>", s.index("<!--/faq-plus-en-->"))
    s = s[:k] + extra_block(d) + s[k:]
    # every visible FAQ item (old and new) goes into the schema, so the two always match
    visible = [
        (html.unescape(q), html.unescape(a))
        for q, a in re.findall(r'<details class="drug-faq"[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', s, re.S)
    ]
    s = add_schema(s, visible)
    s = set_meta(s, d)
    p.write_text(s, encoding="utf-8")
    print(slug, "updated:", len(d["en"]), "EN +", len(d["bn"]), "BN questions")
