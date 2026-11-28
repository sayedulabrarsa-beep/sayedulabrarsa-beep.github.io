#!/usr/bin/env python3
import re, json, html, pathlib, sys, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply3 import ART, EN, BN, SITE, V, fn
R = pathlib.Path(__file__).resolve().parent.parent.parent
TITLE = {"ri": ("Pharmaceutical Regulatory Inspections: What Do Inspectors Check?", "ফার্মাসিউটিক্যাল রেগুলেটরি ইন্সপেকশন: পরিদর্শকেরা কী কী যাচাই করেন?"),
         "oos": ("Out-of-Specification (OOS) Results in Pharma: How Are Failed Tests Investigated?", "ফার্মাসিউটিক্যাল শিল্পে OOS ফলাফল: মানের বাইরে পরীক্ষা হলে কীভাবে তদন্ত করা হয়?")}
sm = (R / "sitemap.xml").read_text(encoding="utf-8"); fd = (R / "blog/feed.xml").read_text(encoding="utf-8")
ar = json.loads((R / "assets/articles.json").read_text(encoding="utf-8")); ds = json.loads((R / "_src/data/articles.json").read_text(encoding="utf-8"))
b = (R / "blog/index.html").read_text(encoding="utf-8")
for a in ("ri", "oos"):
    A = ART[a]; IMG = f"/assets/img/blog/{A['dir']}/"; slug = A["slug"]
    for lang, ti in (("en", 0), ("bn", 1)):
        path = f"blog/{slug}{'' if lang == 'en' else '-bangla'}/"; loc = f"{SITE}/{path}"; L = EN if lang == "en" else BN
        m = re.search(r"<url><loc>" + re.escape(loc) + r"</loc>.*?</url>", sm, re.S); assert m, loc
        lm = re.search(r"<lastmod>[^<]*</lastmod>", m.group(0)).group(0)
        imgs = f"<image:image><image:loc>{SITE}{IMG}{A['pre']}-social-{lang}.jpg</image:loc><image:title>{html.escape(TITLE[a][ti], quote=False)}</image:title></image:image>"
        imgs += "".join(f"<image:image><image:loc>{SITE}{IMG}{fn(a, k, lang)}</image:loc><image:title>{html.escape(L[(a, k)][1].split(' AI-')[0], quote=False)}</image:title></image:image>" for k in A["order"])
        sm = sm[:m.start()] + f"<url><loc>{loc}</loc>{lm}{imgs}</url>" + sm[m.end():]
        f = R / f"assets/img/blog/{A['dir']}/{A['pre']}-social-{lang}.jpg"
        pat = re.compile(r'(<link>' + re.escape(loc) + r'</link>(?:(?!</item>).)*?)<enclosure[^>]*/>', re.S)
        fd, n = pat.subn(lambda mm: mm.group(1) + f'<enclosure url="{SITE}{IMG}{f.name}" type="image/jpeg" length="{f.stat().st_size}" />', fd, count=1)
        if n != 1: print("WARN feed", loc)
    for x in ar:
        if x.get("slug") == slug: x["img"] = IMG + f"{A['pre']}-card.webp"
    if slug in ds: ds[slug]["img"] = IMG + f"{A['pre']}-card.webp"
    i = b.find(slug + '/" class="pb-card-image"'); s = b.rfind("<article", 0, i); e = b.find("</article>", i)
    card = b[s:e]
    card = re.sub(r'data-bn-img="[^"]*"', f'data-bn-img="{IMG}{A["pre"]}-social-bn.jpg{V}"', card)
    card = re.sub(r'<img src="[^"]*"[^>]*>', f'<img src="{IMG}{A["pre"]}-card-w750.webp{V}" alt="{html.escape(EN[(a, "cover")][0], quote=True)}" width="1200" height="630" loading="lazy" decoding="async" srcset="{IMG}{A["pre"]}-card-w750.webp{V} 750w, {IMG}{A["pre"]}-card.webp{V} 1200w" sizes="357px">', card, count=1)
    b = b[:s] + card + b[e:]
(R / "sitemap.xml").write_text(sm, encoding="utf-8"); (R / "blog/feed.xml").write_text(fd, encoding="utf-8")
(R / "assets/articles.json").write_text(json.dumps(ar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(R / "_src/data/articles.json").write_text(json.dumps(ds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(R / "blog/index.html").write_text(b, encoding="utf-8"); print("ok")
