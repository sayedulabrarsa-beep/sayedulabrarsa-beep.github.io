"""Builds the list of every Pharma Blog article and keeps the end-of-article links in sync.

Outputs
  assets/articles.json  - read by assets/blog-related.js for the auto-scrolling "You can also read" band
  every article page    - a plain-HTML "More from the Pharma Blog" link list between <!--more-articles--> markers,
                          so search engines can follow links to every article even without JavaScript

Curated card text lives in _src/data/articles.json; any article under /blog that is missing there is
discovered from its own HTML. Run by .github/workflows/featured-stacks.yml on every push to /blog.
Run from anywhere: python3 _src/article_index.py   (safe to re-run)
"""
import html, json, pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
CUR = json.loads((R / "_src/data/articles.json").read_text(encoding="utf-8"))
START, END = "<!--more-articles-->", "<!--/more-articles-->"


def txt(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def meta(s, prop):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(prop), s)
    return html.unescape(m.group(1)) if m else ""


def short(t, n=96):
    t = t.strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind(". "), cut.rfind("। "))
    return cut[: k + 1] if k > 50 else cut.rsplit(" ", 1)[0] + "…"


def local_img(url):
    p = url.split("?")[0].replace("https://sayedulabrar.site", "")
    if not p.startswith("/") or not (R / p.lstrip("/")).exists():
        return ""
    # prefer a small web copy if the stacks generator made one
    stem = (R / p.lstrip("/")).with_suffix("")
    for w in (640, 720, 800, 480):
        c = stem.parent / f"{stem.name}-w{w}.webp"
        if c.exists():
            return "/" + c.relative_to(R).as_posix()
    return p


def is_article(s):
    return "<article" in s and 'content="noindex' not in s


arts = []
for d in sorted((R / "blog").iterdir()):
    f = d / "index.html"
    if not f.is_file() or d.name.endswith("-bangla"):
        continue
    s = f.read_text(encoding="utf-8")
    if not is_article(s):
        continue
    slug = d.name
    bnf = R / "blog" / f"{slug}-bangla" / "index.html"
    bn_s = bnf.read_text(encoding="utf-8") if bnf.is_file() else ""
    date = (meta(s, "article:published_time") or "")[:10]
    if not date:
        m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})', s)
        date = m.group(1) if m else ""
    if not date:
        m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', s)
        date = m.group(1) if m else ""
    c = CUR.get(slug, {})
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    t_en = c.get("title_en") or re.sub(r"\s*\|\s*Sayedul Abrar\s*$", "", meta(s, "og:title")) or (txt(h1.group(1)) if h1 else slug)
    t_bn = c.get("title_bn")
    if not t_bn and bn_s:
        hb = re.search(r"<h1[^>]*>(.*?)</h1>", bn_s, re.S)
        t_bn = txt(hb.group(1)) if hb else t_en
    arts.append({
        "slug": slug,
        "date": date,
        "tag_en": c.get("tag_en", "Pharma Blog"),
        "tag_bn": c.get("tag_bn", "ফার্মা ব্লগ"),
        "title_en": t_en,
        "title_bn": t_bn or t_en,
        "desc_en": c.get("desc_en") or short(meta(s, "description")),
        "desc_bn": c.get("desc_bn") or (short(meta(bn_s, "description")) if bn_s else short(meta(s, "description"))),
        "url_en": f"/blog/{slug}/",
        "url_bn": f"/blog/{slug}-bangla/" if bn_s else (f"/blog/{slug}/#bn" if 'id="pane-bn"' in s else f"/blog/{slug}/"),
        "img": c.get("img") or local_img(meta(s, "og:image")),
    })

arts.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
(R / "assets/articles.json").write_text(json.dumps(arts, ensure_ascii=False, indent=1), encoding="utf-8")

# plain-HTML link list at the end of every article (EN and BN pages)
n = 0
for a in arts:
    for lang, path in (("en", R / "blog" / a["slug"] / "index.html"), ("bn", R / "blog" / f"{a['slug']}-bangla" / "index.html")):
        if not path.is_file():
            continue
        s = o = path.read_text(encoding="utf-8")
        s = re.sub(re.escape(START) + ".*?" + re.escape(END), "", s, flags=re.S)
        others = [x for x in arts if x["slug"] != a["slug"]]
        head = "ফার্মা ব্লগ থেকে আরও পড়ুন" if lang == "bn" else "More from the Pharma Blog"
        items = "".join(
            f'<li><a href="{html.escape(x["url_" + lang])}">{html.escape(x["title_" + lang])}</a></li>' for x in others
        )
        block = (f'{START}<nav class="more-articles" aria-label="{html.escape(head)}" lang="{lang}">'
                 f'<h2>{html.escape(head)}</h2><ul>{items}</ul></nav>{END}')
        k = s.rfind("</main>")
        if k < 0:
            continue
        s = s[:k] + block + s[k:]
        if s != o:
            path.write_text(s, encoding="utf-8")
            n += 1
print(f"articles.json: {len(arts)} articles; pages with updated link lists: {n}")
