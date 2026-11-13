#!/usr/bin/env python3
"""Bangla photo-style infographics: Hugging Face (Z-Image Turbo) background photo + Bangla text set in code."""
import pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
H = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
U = H.as_uri()
NAME = "সাইয়্যেদুল আবরার"
BY = f"লিখেছেন {NAME}, ফার্মাসিস্ট"
CSS = f"""
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-400-normal.woff2);font-weight:400;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-600-normal.woff2);font-weight:600;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:HS;src:url({U}/hind-siliguri-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anton;src:url({U}/anton-latin-400-normal.woff2)}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-800-normal.woff2);font-weight:800;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-bengali-700-normal.woff2);font-weight:700;unicode-range:U+0964-0965,U+0980-09FE,U+200C-200D,U+25CC}}
@font-face{{font-family:Anek;src:url({U}/anek-bangla-latin-700-normal.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;height:900px;overflow:hidden;font-family:HS,Poppins,sans-serif;color:#173d43;position:relative;background:#f7f4ee}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:right center}}
.fade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(250,248,243,.97) 0%,rgba(250,248,243,.94) var(--a,46%),rgba(250,248,243,0) var(--b,66%))}}
.col{{position:absolute;left:72px;top:54px;bottom:96px;width:var(--w,900px);display:flex;flex-direction:column}}
.kick{{font-size:25px;font-weight:600;color:#2f8f83}}
h1{{font-size:54px;line-height:1.28;font-weight:700;margin-top:2px}}
.list{{display:flex;flex-direction:column;gap:16px;margin-top:22px;flex:1;justify-content:center}}
.row{{display:flex;gap:20px;align-items:center;background:rgba(255,255,255,.88);border:1px solid #e3eeec;border-radius:22px;padding:18px 24px;box-shadow:0 10px 26px rgba(23,61,67,.08)}}
.n{{width:52px;height:52px;border-radius:50%;background:#17656a;color:#fff;font-weight:700;font-size:28px;display:flex;align-items:center;justify-content:center;flex:none}}
.t{{font-size:31px;font-weight:700;line-height:1.3}}
.p{{font-size:25px;line-height:1.45;color:#3f5a63}}
.note{{margin-top:16px;font-size:26px;font-weight:700;border-radius:16px;padding:14px 22px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:62px;display:flex;justify-content:space-between;align-items:center;padding:0 72px;font-size:20px;color:#5b6f75;background:rgba(250,248,243,.92);border-top:1px solid #e2ebe8}}
.foot b{{color:#17656a}}
.t{{font-size:37px!important;line-height:1.22!important}}.p{{font-size:29px!important;line-height:1.38!important;color:#2d464e!important}}h1{{font-size:60px!important}}.kick{{font-size:24px!important}}.note{{font-size:30px!important}}.row{{background:rgba(255,255,255,.95)!important}}.foot{{font-size:22px!important;height:66px!important}}.tag{{position:absolute;right:40px;bottom:78px;font-size:18px;color:#5b6f75;background:rgba(255,255,255,.85);padding:6px 14px;border-radius:999px}}
.kick{{display:flex;align-items:center;gap:12px;color:#17807a!important;font-weight:700!important}}
.kick:before{{content:"";width:46px;height:4px;border-radius:2px;background:linear-gradient(90deg,#17807a,#e0892b);flex:none}}
h1 em{{font-style:normal;background:linear-gradient(90deg,#0f8f86,#17656a 55%,#e0892b);-webkit-background-clip:text;background-clip:text;color:transparent}}
h1{{color:#0f3c42!important}}
.n{{background:#0f3c42!important;box-shadow:0 0 0 4px rgba(255,255,255,.9)}}
.kick{{font-family:Anek,HS;font-size:25px!important}}
h1{{font-family:Anek,HS;font-weight:800!important;font-size:62px!important;line-height:1.2!important}}
.t{{font-family:Anek,HS;font-weight:700!important}}
.n{{font-family:Anek,HS!important;font-weight:800!important}}
"""
def ic(ok):
    if ok == "ok": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#1f7a57"/><path d="M15 27l7 8 15-17" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    if ok == "no": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#b8433f"/><path d="M17 17l18 18M35 17L17 35" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
    if ok == "q": return '<svg width="52" height="52" style="flex:none"><circle cx="26" cy="26" r="24" fill="#e0892b"/><text x="26" y="37" text-anchor="middle" font-size="30" font-weight="700" fill="#fff" font-family="Poppins">?</text></svg>'
def page(bg, body, src, a="46%", b="66%", w="900px", tag=""):
    t = f'<div class="tag">{tag}</div>' if tag else ""
    return (f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="bg" style="background-image:url({U}/bg/{bg}.webp)"></div><div class="fade" style="--a:{a};--b:{b}"></div>'
            f'<div class="col" style="--w:{w}">{body}</div>{t}<div class="foot"><span>সূত্র: {src}</span><b>{NAME}, ফার্মাসিস্ট · sayedulabrar.site</b></div></body></html>')
def rows(items):
    return '<div class="list">' + "".join(
        f'<div class="row">{lead}<div><p class="t">{a}</p>' + (f'<p class="p">{b}</p>' if b else "") + '</div></div>' for lead, a, b in items) + "</div>"
N = lambda i: f'<div class="n">{"১২৩৪৫"[i]}</div>'

P = {}
P["cover"] = (f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
  f'<div class="bg" style="background-image:url({U}/bg/cover.webp)"></div><div class="fade" style="--a:42%;--b:60%"></div>'
  f'<div style="position:absolute;left:80px;top:150px;width:640px"><p class="kick">সহজ ভাষায় স্বাস্থ্য</p>'
  f'<h1 style="font-size:66px!important;line-height:1.22!important;margin-top:14px">অ্যান্টিবায়োটিক কোর্স <em>শেষ করা</em> কেন জরুরি?</h1>'
  f'<p style="font-size:32px;color:#4c6670;margin-top:16px">অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে শুরু হয়</p>'
  f'<p style="display:inline-block;margin-top:38px;background:#17656a;color:#fff;font-weight:600;font-size:27px;padding:12px 28px;border-radius:999px">{BY}</p></div></body></html>')

P["resistance"] = page("resistance", '<p class="kick">সরল ব্যাখ্যা</p><h1>অ্যান্টিবায়োটিক <em>রেজিস্ট্যান্স</em> কীভাবে তৈরি হয়</h1>' + rows([
  (N(0), "সংক্রমণে অনেক ব্যাকটেরিয়া থাকে", "এদের কয়েকটি স্বাভাবিকভাবেই ওষুধে কম সংবেদনশীল হতে পারে।"),
  (N(1), "অ্যান্টিবায়োটিক সংবেদনশীলগুলোকে মারে", "ভুল বা অপ্রয়োজনীয় ব্যবহারে প্রতিরোধী ব্যাকটেরিয়া টিকে যাওয়ার সুযোগ পায়।"),
  (N(2), "টিকে থাকা ব্যাকটেরিয়া বাড়ে ও ছড়ায়", "পরের সংক্রমণে একই অ্যান্টিবায়োটিক আর কাজ নাও করতে পারে।")]) +
  '<p class="note" style="background:#fdf0ee;color:#a8362f">রেজিস্ট্যান্স হয় ব্যাকটেরিয়ার, আপনার শরীরের নয়।</p>', "WHO; MedlinePlus", a="44%", b="60%", w="860px", tag="প্রতীকী ছবি")

P["viruses"] = page("viruses", '<p class="kick">মৌলিক ধারণা</p><h1>অ্যান্টিবায়োটিক ব্যাকটেরিয়ার জন্য, <em>ভাইরাসের জন্য নয়</em></h1>' + rows([
  (ic("ok"), "ব্যাকটেরিয়াজনিত সংক্রমণ", "দরকার মনে করলে ডাক্তার অ্যান্টিবায়োটিক দেন। তবে সব ব্যাকটেরিয়াজনিত সংক্রমণে এটি লাগে না।"),
  (ic("no"), "ভাইরাসজনিত অসুখ: সর্দি-কাশি ও ফ্লু", "অ্যান্টিবায়োটিক ভাইরাসে কাজ করে না, তাই এতে আপনি ভালো বোধ করবেন না।")]) +
  '<p class="note" style="background:#fff5df;border:1px solid #f0d99e">জ্বর বা কাশি মানেই অ্যান্টিবায়োটিক নয়। সিদ্ধান্ত নেবেন ডাক্তার।</p>', "CDC", a="44%", b="58%", w="860px")

def two(h, items, ok):
    c = "#1f7a57" if ok else "#b8433f"; bg = "rgba(236,247,242,.93)" if ok else "rgba(251,238,236,.93)"
    li = "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:16px">{ic("ok" if ok else "no")}<p class="p" style="font-size:25px;color:#173d43">{x}</p></div>' for x in items)
    return f'<div style="flex:1;background:{bg};border-radius:22px;padding:22px 24px;box-shadow:0 10px 26px rgba(23,61,67,.08)"><p class="t" style="color:{c};font-size:34px">{h}</p>{li}</div>'
P["dosdonts"] = page("dosdonts", '<p class="kick">করণীয় ও বর্জনীয়</p><h1>অ্যান্টিবায়োটিক খাওয়ার <em>সঠিক নিয়ম</em></h1>'
  '<div style="display:flex;gap:22px;margin-top:24px;flex:1;align-items:stretch">' +
  two("যা করবেন", ["প্রেসক্রিপশনে যেভাবে লেখা, ঠিক সেভাবে খান", "ভালো লাগলেও কোর্স শেষ করুন, যদি না ডাক্তার অন্য কথা বলেন", "প্রতিটি ডোজ নির্দিষ্ট সময়ে খান", "পার্শ্বপ্রতিক্রিয়া হলে ডাক্তার বা ফার্মাসিস্টকে জানান"], True) +
  two("যা করবেন না", ["নিজে নিজে মাঝপথে বন্ধ করবেন না", "বাকি ওষুধ পরের অসুখের জন্য রেখে দেবেন না", "অন্যকে দেবেন না, অন্যের ওষুধ খাবেন না", "প্রেসক্রিপশন ছাড়া কিনবেন না"], False) +
  '</div>', "CDC; NHS; MedlinePlus", a="58%", b="74%", w="1060px")

P["missed"] = page("missed", '<p class="kick">ডোজ বাদ পড়লে</p><h1>একটি <em>ডোজ মিস</em> হলে কী করবেন?</h1>' + rows([
  (ic("ok"), "মনে পড়ার সঙ্গে সঙ্গে খেয়ে নিন", "তারপর আগের মতো নিয়ম মেনে চলুন।"),
  (ic("q"), "পরের ডোজের সময় প্রায় হয়ে গেছে?", "তাহলে বাদ পড়া ডোজটি বাদ দিন, পরেরটি নিয়মমতো খান।"),
  (ic("no"), "কখনও একসাথে দুটি ডোজ খাবেন না", "বাদ পড়া ডোজ পূরণ করতে দ্বিগুণ খাওয়া যাবে না।")]) +
  '<p class="note" style="background:rgba(255,255,255,.88);font-size:24px;font-weight:600">নিশ্চিত না হলে ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন। আপনার ওষুধের লিফলেটে আলাদা নির্দেশনা থাকতে পারে।</p>',
  "NHS রোগী-তথ্য লিফলেট; MedlinePlus", a="44%", b="60%", w="860px")

P["redlabel"] = page("redlabel", '<p class="kick" style="color:#b8433f">বাংলাদেশ</p><h1>অ্যান্টিবায়োটিকের প্যাকে <em>লাল চিহ্ন</em></h1>' + rows([
  (N(0), "কী?", "ডিসেম্বর ২০২২ থেকে অ্যান্টিবায়োটিকের প্যাকে লাল চিহ্ন বাধ্যতামূলক (DGDA)।"),
  (N(1), "কী লেখা থাকে?", "“Antibiotic” এবং প্রেসক্রিপশন ছাড়া ব্যবহার না করার সতর্কবার্তা।"),
  (N(2), "আপনার করণীয়", "লাল চিহ্ন মানে অ্যান্টিবায়োটিক। শুধু ডাক্তারের প্রেসক্রিপশনে খান।")]) +
  '',
  "WHO বাংলাদেশ (DGDA, ড্রাগ কন্ট্রোল কমিটি)", a="50%", b="60%", w="880px", tag="প্রতীকী ছবি, আসল পণ্য নয়")

def tier(h, c, items, note):
    return (f'<div class="row" style="border-left:10px solid {c};align-items:flex-start;flex-direction:column;gap:4px;padding:16px 24px">'
            f'<p class="t" style="color:{c};font-size:30px">{h}</p><p class="p" style="color:#173d43">{" · ".join(items)}</p><p class="p" style="font-weight:700;color:{c};font-size:23px">{note}</p></div>')
P["sideeffects"] = page("sideeffects", '<p class="kick">পার্শ্বপ্রতিক্রিয়া</p><h1>কখন <em>সাহায্য</em> নেবেন</h1><div class="list">' +
  tier("সাধারণ", "#2f8f83", ["বমি ভাব বা বমি", "পেট ফাঁপা বা বদহজম", "পাতলা পায়খানা"], "সাধারণত হালকা হয়। চিন্তা হলে ফার্মাসিস্টকে জিজ্ঞেস করুন।") +
  tier("ডাক্তারকে জানান", "#c27a12", ["তীব্র বা পানির মতো পাতলা পায়খানা", "তীব্র বা দুশ্চিন্তার পার্শ্বপ্রতিক্রিয়া", "ভুল করে বাড়তি ডোজ"], "নিজে নিজে ওষুধ বন্ধ বা বদলাবেন না।") +
  tier("জরুরি", "#b8433f", ["মুখ, ঠোঁট বা জিহ্বা ফুলে যাওয়া", "শ্বাস নিতে কষ্ট"], "গুরুতর অ্যালার্জির লক্ষণ হতে পারে। সঙ্গে সঙ্গে জরুরি চিকিৎসা নিন।") +
  '</div>', "NHS রোগী-তথ্য লিফলেট (জুন ২০২৫); পূর্ণ তালিকা নয়", a="48%", b="62%", w="880px")

P["takeaways"] = page("takeaways", '<p class="kick">মনে রাখার কথা</p><h1>অ্যান্টিবায়োটিক: <em>৫টি মূল কথা</em></h1><div class="list" style="gap:10px;margin-top:14px">' + "".join(
  f'<div class="row" style="padding:12px 22px">{N(i)}<div><p class="t" style="font-size:28px">{a}</p><p class="p" style="font-size:23px">{b}</p></div></div>' for i, (a, b) in enumerate([
  ("পুরো কোর্স শেষ করুন", "ভালো লাগলেও, যদি না ডাক্তার অন্য কথা বলেন।"),
  ("শুধু প্রেসক্রিপশনে খান", "প্যাকে লাল চিহ্ন দেখলেই বুঝবেন এটি অ্যান্টিবায়োটিক।"),
  ("ভাইরাসে কাজ করে না", "সর্দি-কাশি ও ফ্লুতে অ্যান্টিবায়োটিক কাজ করে না।"),
  ("রেখে দেবেন না, ভাগ করবেন না", "বাকি ওষুধ ফেলার নিয়ম ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
  ("ডোজ মিস হলে দ্বিগুণ নয়", "সময়মতো খান, সমস্যা হলে ডাক্তারকে জানান।")])) + '</div>',
  "NHS; CDC; MedlinePlus; WHO বাংলাদেশ", a="46%", b="60%", w="900px")

NAMES = {"cover": "why-complete-antibiotic-course-cover-16x9", "resistance": "how-antibiotic-resistance-develops-simplified", "viruses": "antibiotics-treat-bacteria-not-viruses-cold-flu",
 "dosdonts": "antibiotic-dos-and-donts-take-as-prescribed", "missed": "missed-antibiotic-dose-what-to-do", "redlabel": "bangladesh-red-mark-on-antibiotic-packs-dgda",
 "sideeffects": "antibiotic-side-effects-when-to-get-help", "takeaways": "antibiotics-key-takeaways"}
with sync_playwright() as p:
    br = p.chromium.launch()
    for k, htm in P.items():
        pg = br.new_page(viewport={"width": 1600, "height": 900})
        f = H / "_bn.html"; f.write_text(htm, encoding="utf-8"); pg.goto(f.as_uri()); pg.wait_for_timeout(500)
        over = pg.evaluate("()=>{const c=document.querySelector('.col');return c?c.scrollHeight>c.clientHeight+2:false}")
        im = Image.open(io.BytesIO(pg.screenshot())).convert("RGB"); pg.close()
        out = OUT / f"{NAMES[k]}-bn.webp"; im.save(out, "WEBP", quality=88, method=6)
        print(("OVERFLOW " if over else "") + out.name, out.stat().st_size)
        if k == "cover":
            im.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652)).save(OUT / "social-bn.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    br.close()
