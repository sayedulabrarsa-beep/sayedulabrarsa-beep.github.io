#!/usr/bin/env python3
"""Regulatory Inspections, OOS Results and Paracetamol Safety: 18 user-supplied text-free photos -> 1600x900 WebP with bold, large title zones (EN + BN),
a different palette and font family per article, plus 1200x630 share images and card thumbnails. Credit pill is stamped afterwards by _src/credit/stamp.py."""
import pathlib, json, sys
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = pathlib.Path("/mnt/user-data/attachments/919b65f6-4fba-51b3-bfa5-5b31e569d401")
BG = R / "_src/qa3_images/bg"
FD = lambda d, f: (R / d / f).as_uri()
QQ = "_src/qaqc_images/cinematic"; EX = "_src/excretion_images/fonts"; ST = "_src/stability_images/fonts"
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
BNG = "U+0980-09FF,U+200C-200D,U+0964-0965,U+25CC"
def face(fam, w, url, rng): return f"@font-face{{font-family:{fam};font-weight:{w};src:url({url});unicode-range:{rng}}}"
ART = {
 "ri": dict(dir="regulatory-inspections", pre="ri", fam="'RIF'", ink="#0F2D4F", key="#1B4F8F", acc="#E59A1F", hi="rgba(229,154,31,.55)", veil="#EEF3F9", pill="#0F2D4F", bandrgb="15,45,79", gold="#FFD27A",
   css="".join([face("RIF", 800, FD(QQ, "poppins-latin-800-normal.woff2"), LAT), face("RIF", 600, FD(QQ, "poppins-latin-600-normal.woff2"), LAT), face("RIF", 800, FD(QQ, "hind-siliguri-bengali-700-normal.woff2"), BNG), face("RIF", 600, FD(QQ, "hind-siliguri-bengali-700-normal.woff2"), BNG)]), lh=(1.14, 1.32), ls=".1em"),
 "oos": dict(dir="oos-investigation", pre="oos", fam="'OOF'", ink="#2B1B5A", key="#4B2FB8", acc="#F0644B", hi="rgba(240,100,75,.45)", veil="#F3F0FB", pill="#2B1B5A", bandrgb="43,27,90", gold="#FFB4A6",
   css="".join([face("OOF", 800, FD(EX, "manrope-latin-800-normal.woff2"), LAT), face("OOF", 600, FD(EX, "manrope-latin-700-normal.woff2"), LAT), face("OOF", 800, FD(EX, "noto-sans-bengali-bengali-700-normal.woff2"), BNG), face("OOF", 600, FD(EX, "noto-sans-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.12, 1.4), ls=".1em"),
 "pc": dict(dir="paracetamol-safety", pre="pc", fam="'PCF','Lora',serif", ink="#14372E", key="#0E7A55", acc="#F08A24", hi="rgba(240,138,36,.5)", veil="#F2F7EF", pill="#14372E", bandrgb="20,55,46", gold="#FFC98A",
   css="".join([face("PCF", 800, FD(ST, "noto-serif-bengali-bengali-800-normal.woff2"), BNG), face("PCF", 600, FD(ST, "noto-serif-bengali-bengali-600-normal.woff2"), BNG)]), lh=(1.14, 1.36), ls=".1em"),
}
# image id -> (article, key). L = (tw, y0, y1) in 1600x900 px, B = bottom band
M = {"bae9a1cc": ("ri", "cover"), "56f7e301": ("ri", "what"), "512ed13f": ("ri", "types"), "0b871a7a": ("ri", "check"), "22c6a773": ("ri", "during"), "8d299c0c": ("ri", "capa"),
     "af490ca2": ("oos", "cover"), "1c69deb9": ("oos", "terms"), "f95d89a5": ("oos", "causes"), "4924dc9d": ("oos", "investigation"), "98e97fae": ("oos", "retest"), "77cf04b2": ("oos", "decision"),
     "9cdf70b8": ("pc", "cover"), "994fcba0": ("pc", "label"), "24de19e9": ("pc", "double"), "e08f1d04": ("pc", "children"), "17a498bc": ("pc", "liver"), "aaf9605c": ("pc", "help")}
LAY = {("ri", "cover"): ("L", 620, 70, 830), ("ri", "what"): ("L", 420, 70, 830), ("ri", "types"): ("L", 440, 70, 830), ("ri", "check"): ("L", 380, 40, 610), ("ri", "during"): ("B",), ("ri", "capa"): ("B",),
       ("oos", "cover"): ("B",), ("oos", "terms"): ("L", 480, 70, 830), ("oos", "causes"): ("L", 400, 50, 580), ("oos", "investigation"): ("B",), ("oos", "retest"): ("L", 390, 50, 545), ("oos", "decision"): ("B",),
       ("pc", "cover"): ("L", 540, 70, 830), ("pc", "label"): ("L", 420, 50, 540), ("pc", "double"): ("L", 560, 70, 830), ("pc", "children"): ("B",), ("pc", "liver"): ("L", 480, 50, 590), ("pc", "help"): ("B",)}
# kicker, title (<i> = keyword), 3 chips   (cover: chips[0] = sub line)
T = {
 ("ri", "cover"): (("REGULATORY INSPECTIONS", "রেগুলেটরি ইন্সপেকশন"), ("What do <i>inspectors</i> check?", "ইন্সপেক্টররা <i>কী কী</i> যাচাই করেন?"),
   (["Scope, evidence, findings and CAPA, with Bangladesh context"], ["পরিধি, প্রমাণ, ফলাফল ও CAPA, বাংলাদেশের প্রেক্ষাপটসহ"])),
 ("ri", "what"): (("WHAT IT IS", "এটি কী"), ("An inspection is a <i>structured check</i>", "ইন্সপেকশন হলো <i>কাঠামোবদ্ধ যাচাই</i>"),
   (["Premises, people and records", "Practice compared with requirements", "Evidence, not assumption"], ["প্রাঙ্গণ, মানুষ ও নথি", "বাস্তব কাজ ও প্রয়োজনীয় মানের তুলনা", "অনুমান নয়, প্রমাণ"])),
 ("ri", "types"): (("RISK-BASED PLANNING", "ঝুঁকিভিত্তিক পরিকল্পনা"), ("Look <i>harder</i> where risk is higher", "যেখানে ঝুঁকি বেশি, <i>সেখানে নজর বেশি</i>"),
   (["Routine, follow-up and for-cause visits", "Site history and product risk guide the plan", "Scope is set before the visit"], ["রুটিন, ফলো-আপ ও কারণভিত্তিক পরিদর্শন", "সাইটের ইতিহাস ও পণ্যের ঝুঁকি পরিকল্পনা ঠিক করে", "পরিদর্শনের আগেই পরিধি নির্ধারণ"])),
 ("ri", "check"): (("WHAT THEY CHECK", "যা যা দেখা হয়"), ("Records must <i>match reality</i>", "নথি ও বাস্তব অবস্থা <i>মিলতে হবে</i>"),
   (["Batch records and documents", "Equipment, laboratory and data", "Quality system and training"], ["ব্যাচ রেকর্ড ও নথি", "যন্ত্রপাতি, ল্যাবরেটরি ও ডেটা", "মান ব্যবস্থা ও প্রশিক্ষণ"])),
 ("ri", "during"): (("DURING THE VISIT", "পরিদর্শনের সময়"), ("Open questions, <i>clear answers</i>", "খোলামেলা প্রশ্ন, <i>স্পষ্ট উত্তর</i>"),
   (["Opening meeting and site walk-through", "Document and record review", "Closing meeting and feedback"], ["শুরুর সভা ও সাইট পরিদর্শন", "নথি ও রেকর্ড পর্যালোচনা", "শেষ সভা ও মতামত"])),
 ("ri", "capa"): (("FINDINGS AND CAPA", "পর্যবেক্ষণ ও CAPA"), ("Fix the cause, <i>not only the finding</i>", "শুধু পর্যবেক্ষণ নয়, <i>কারণ</i> ঠিক করুন"),
   (["Understand the root cause", "Corrective and preventive actions", "Track every action to closure"], ["মূল কারণ বুঝুন", "সংশোধনমূলক ও প্রতিরোধমূলক পদক্ষেপ", "প্রতিটি পদক্ষেপ শেষ পর্যন্ত অনুসরণ করুন"])),
 ("oos", "cover"): (("OUT-OF-SPECIFICATION (OOS)", "আউট-অব-স্পেসিফিকেশন (OOS)"), ("A failed result starts <i>an investigation</i>", "ব্যর্থ ফল মানেই শুরু হয় <i>তদন্ত</i>"),
   (["Check the laboratory first", "Document every step", "Decide on evidence"], ["আগে ল্যাবরেটরি যাচাই করুন", "প্রতিটি ধাপ লিপিবদ্ধ করুন", "প্রমাণের ভিত্তিতে সিদ্ধান্ত নিন"])),
 ("oos", "terms"): (("OOS · OOT · DEVIATION", "OOS · OOT · DEVIATION"), ("Three terms, <i>three meanings</i>", "তিনটি শব্দ, <i>তিনটি অর্থ</i>"),
   (["OOS: fails the specification", "OOT: an unusual trend", "Deviation: departs from procedure"], ["OOS: স্পেসিফিকেশনে ব্যর্থ", "OOT: অস্বাভাবিক প্রবণতা", "Deviation: পদ্ধতি থেকে বিচ্যুতি"])),
 ("oos", "causes"): (("POSSIBLE CAUSES", "সম্ভাব্য কারণ"), ("The cause may be <i>in the lab or the batch</i>", "কারণ হতে পারে <i>ল্যাবে বা ব্যাচে</i>"),
   (["Analyst or method error", "Instrument or sample issue", "A real batch problem"], ["বিশ্লেষক বা পদ্ধতির ত্রুটি", "যন্ত্র বা নমুনার সমস্যা", "ব্যাচেরই প্রকৃত সমস্যা"])),
 ("oos", "investigation"): (("THE INVESTIGATION", "তদন্ত"), ("Facts first, <i>then conclusions</i>", "আগে তথ্য, <i>তারপর সিদ্ধান্ত</i>"),
   (["Laboratory phase first", "Review records and data", "Extend to production if needed"], ["প্রথমে ল্যাবরেটরি পর্যায়", "রেকর্ড ও ডেটা পর্যালোচনা", "প্রয়োজনে উৎপাদন পর্যন্ত বিস্তার"])),
 ("oos", "retest"): (("RETEST AND RESAMPLE", "পুনঃপরীক্ষা ও পুনঃনমুনা"), ("Retest <i>only with a reason</i>", "পুনঃপরীক্ষা হবে <i>কারণসহ</i>"),
   (["Follow the written procedure", "Do not test into compliance", "Record every result"], ["লিখিত পদ্ধতি মানুন", "শুধু পাস করানোর জন্য পরীক্ষা নয়", "প্রতিটি ফল লিপিবদ্ধ করুন"])),
 ("oos", "decision"): (("BATCH DECISION AND CAPA", "ব্যাচ সিদ্ধান্ত ও CAPA"), ("The batch waits <i>for the evidence</i>", "প্রমাণ না মেলা পর্যন্ত <i>ব্যাচ অপেক্ষায়</i>"),
   (["The quality unit decides", "Root cause and CAPA", "Learn and prevent repeats"], ["সিদ্ধান্ত নেয় কোয়ালিটি ইউনিট", "মূল কারণ ও CAPA", "শিখুন, পুনরাবৃত্তি রোধ করুন"])),
 ("pc", "cover"): (("PARACETAMOL SAFETY", "প্যারাসিটামল নিরাপত্তা"), ("Use it <i>correctly</i>, avoid overdose", "<i>সঠিকভাবে</i> ব্যবহার করুন, ওভারডোজ এড়ান"),
   (["Label, limits, children and when to seek help"], ["লেবেল, সীমা, শিশু ও কখন সাহায্য নেবেন"])),
 ("pc", "label"): (("READ THE LABEL", "লেবেল পড়ুন"), ("Check <i>every pack</i>, every time", "<i>প্রতিটি প্যাক</i>, প্রতিবার দেখুন"),
   (["Active ingredient and strength", "Dose and interval on the pack", "The daily limit it states"], ["সক্রিয় উপাদান ও শক্তি", "প্যাকে লেখা ডোজ ও বিরতি", "প্যাকে উল্লেখিত দৈনিক সীমা"])),
 ("pc", "double"): (("AVOID DOUBLE DOSING", "দ্বিগুণ ডোজ এড়ান"), ("Many products <i>contain paracetamol</i>", "অনেক ওষুধেই <i>থাকে প্যারাসিটামল</i>"),
   (["Check cold and flu products", "Add up every source", "Ask if you are unsure"], ["ঠান্ডা-ফ্লুর ওষুধও দেখুন", "সব উৎস মিলিয়ে হিসাব রাখুন", "নিশ্চিত না হলে জিজ্ঞাসা করুন"])),
 ("pc", "children"): (("CHILDREN", "শিশু"), ("Children need <i>extra care</i>", "শিশুদের জন্য <i>বাড়তি সতর্কতা</i>"),
   (["Use a product made for children", "Measure with the supplied device", "Follow the label or ask a professional"], ["শিশুদের জন্য নির্ধারিত পণ্য নিন", "সঙ্গের মাপক দিয়ে মাপুন", "লেবেল মানুন বা পেশাদারের পরামর্শ নিন"])),
 ("pc", "liver"): (("THE LIVER", "লিভার"), ("Too much can <i>harm the liver</i>", "বেশি খেলে <i>লিভারের ক্ষতি</i> হতে পারে"),
   (["Stay within the labelled limit", "Liver condition? Ask first", "Overdose needs urgent care"], ["লেবেলের সীমার মধ্যে থাকুন", "লিভারের সমস্যা? আগে জিজ্ঞাসা করুন", "ওভারডোজে জরুরি চিকিৎসা দরকার"])),
 ("pc", "help"): (("WHEN TO SEEK HELP", "কখন সাহায্য নেবেন"), ("Do not ignore <i>pain that persists</i>", "<i>দীর্ঘস্থায়ী ব্যথা</i> উপেক্ষা করবেন না"),
   (["Possible overdose: seek urgent help", "Fever or pain that continues", "Ask a doctor or pharmacist"], ["ওভারডোজের সন্দেহ হলে জরুরি সাহায্য নিন", "জ্বর বা ব্যথা কমতে না চাইলে", "চিকিৎসক বা ফার্মাসিস্টকে জিজ্ঞাসা করুন"])),
}
SOC = {  # share-image text: kicker, full title, sub, layout  (EN, BN)
 "ri": (("PHARMA BLOG · REGULATORY INSPECTIONS", "PHARMA BLOG · রেগুলেটরি ইন্সপেকশন"), ("Pharmaceutical Regulatory <i>Inspections</i>: What Do Inspectors Check?", "ফার্মাসিউটিক্যাল রেগুলেটরি <i>ইন্সপেকশন</i>: পরিদর্শকেরা কী কী যাচাই করেন?"),
        ("Scope, evidence, findings and CAPA", "পরিধি, প্রমাণ, ফলাফল ও CAPA")),
 "oos": (("PHARMA BLOG · QUALITY CONTROL", "PHARMA BLOG · কোয়ালিটি কন্ট্রোল"), ("Out-of-Specification (<i>OOS</i>) Results in Pharma: How Are Failed Tests Investigated?", "ফার্মাসিউটিক্যাল শিল্পে <i>OOS</i> ফলাফল: মানের বাইরে পরীক্ষা হলে কীভাবে তদন্ত করা হয়?"),
         ("From the first result to batch decision and CAPA", "প্রথম ফল থেকে ব্যাচ সিদ্ধান্ত ও CAPA পর্যন্ত")),
 "pc": (("PHARMA BLOG · MEDICINE SAFETY", "PHARMA BLOG · ওষুধের নিরাপত্তা"), ("<i>Paracetamol</i> Safety: How to Use It Correctly and Avoid Overdose", "<i>প্যারাসিটামল</i> নিরাপদে ব্যবহারের নিয়ম: অতিরিক্ত সেবন ও লিভারের ঝুঁকি"),
        ("Labels, dose limits, children, liver safety and when to seek help", "লেবেল, ডোজের সীমা, শিশু, লিভারের নিরাপত্তা ও কখন সাহায্য নেবেন")),
}
SOCIAL_L = {"ri": (600, 60, 780), "pc": (520, 60, 780)}  # tw, y0, y1 on the 1600x840 share canvas
BY = ("By Sayedul Abrar · Pharmacist", "ফার্মাসিস্ট সাইয়্যেদুল আবরার")
def page(a, lang, body_inner, W, H, bgp, shift):
    A = ART[a]; bn = lang == "bn"
    return (f"<meta charset='utf-8'><style>{A['css']}html,body{{margin:0}}.s{{position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{A['veil']};font-family:{A['fam']},sans-serif}}"
            f".s>img{{position:absolute;left:0;top:{shift}px;width:1600px;height:900px}}:root{{--s:1}}</style>"
            f"<div class='s'><img src='{bgp.as_uri()}'>{body_inner}</div>")
def left_block(a, lang, kick, title, rows, tw, y0, y1, sub=None, by=None):
    A = ART[a]; bn = lang == "bn"; fam = A["fam"]; lh = A["lh"][1 if bn else 0]; ls = "0" if bn else A["ls"]
    ch = "" if not rows else '<div class="ch">' + "".join(f'<div class="c">{c}</div>' for c in rows) + "</div>"
    sb = f'<div class="sub">{sub}</div>' if sub else ""; bb = f'<div class="by">{by}</div>' if by else ""
    kf = 22 if not bn else 27; tf = 56 if not bn else 52; cf = 25 if not bn else 24; maxt = 124 if not bn else 108
    h = y1 - y0; veil = 64 + tw + 28
    css = (f"<style>.v{{position:absolute;left:0;top:0;width:{veil+80}px;height:100%;background:linear-gradient(90deg,{A['veil']} 0,{A['veil']}f2 {veil}px,{A['veil']}00 100%)}}"
           f".t{{position:absolute;left:64px;top:{y0}px;width:{tw}px;height:{h}px;display:flex;flex-direction:column;justify-content:center}}.in{{display:flex;flex-direction:column}}"
           f".k{{font:800 calc(var(--s)*{kf}px)/1.12 {fam};letter-spacing:{ls};color:{A['key']}}}.bar{{width:calc(var(--s)*110px);height:calc(var(--s)*9px);border-radius:5px;background:{A['acc']};margin:calc(var(--s)*16px) 0 calc(var(--s)*22px)}}"
           f".h{{font:800 calc(var(--s)*{tf}px)/{lh} {fam};color:{A['ink']}}}.h i{{font-style:normal;color:{A['key']};box-shadow:inset 0 -.3em 0 {A['hi']}}}"
           f".ch{{margin-top:calc(var(--s)*26px);display:flex;flex-direction:column;gap:calc(var(--s)*12px)}}.c{{background:#fff;border-left:calc(var(--s)*9px) solid {A['key']};border-bottom:calc(var(--s)*4px) solid {A['acc']};border-radius:10px;padding:calc(var(--s)*12px) calc(var(--s)*18px);font:700 calc(var(--s)*{cf}px)/1.34 {fam};color:{A['ink']};box-shadow:0 4px 14px rgba(0,0,0,.12)}}"
           f".sub{{margin-top:calc(var(--s)*22px);font:600 calc(var(--s)*{cf+2}px)/1.4 {fam};color:{A['ink']}}}.by{{margin-top:calc(var(--s)*24px);align-self:flex-start;white-space:nowrap;font:700 calc(var(--s)*{cf-1}px)/1 {fam};color:#fff;background:{A['pill']};padding:calc(var(--s)*14px) calc(var(--s)*26px);border-radius:999px}}</style>")
    js = (f"<script>document.fonts.ready.then(function(){{var r=document.documentElement,e=document.getElementById('in'),best=1;for(var s=1;s<=3.4;s+=0.02){{r.style.setProperty('--s',s);"
          f"if(e.getBoundingClientRect().height>{h}||e.scrollWidth>{tw}+2||{tf}*s>{maxt}||{cf}*s>46)break;best=s}}r.style.setProperty('--s',best)}});</script>")
    return css + f'<div class="v"></div><div class="t"><div class="in" id="in"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div>{sb}{ch}{bb}</div></div>' + js
def band_block(a, lang, kick, title, rows, H, bandh, right_html=None, left_w=760, right_w=640):
    A = ART[a]; bn = lang == "bn"; fam = A["fam"]; lh = A["lh"][1 if bn else 0]; ls = "0" if bn else A["ls"]
    tf = 50 if not bn else 48; kf = 22 if not bn else 26; cf = 22 if not bn else 22; maxt = 96 if not bn else 90
    avail = bandh - 76
    chips = right_html if right_html else '<div class="r">' + "".join(f'<div class="c">{c}</div>' for c in rows) + "</div>"
    css = (f"<style>.bd{{position:absolute;left:0;bottom:0;width:1600px;height:{bandh}px;background:linear-gradient(180deg,rgba({A['bandrgb']},0) 0,rgba({A['bandrgb']},.94) 46px,rgba({A['bandrgb']},.97) 100%)}}"
           f".l{{position:absolute;left:64px;bottom:40px;width:{left_w}px}}.k{{font:800 calc(var(--s)*{kf}px)/1.1 {fam};letter-spacing:{ls};color:{A['gold']}}}.bar{{width:calc(var(--s)*92px);height:calc(var(--s)*8px);border-radius:4px;background:{A['acc']};margin:calc(var(--s)*12px) 0 calc(var(--s)*16px)}}"
           f".h{{font:800 calc(var(--s)*{tf}px)/{lh} {fam};color:#fff}}.h i{{font-style:normal;color:{A['gold']}}}"
           f".r{{position:absolute;right:64px;bottom:40px;width:{right_w}px;display:flex;flex-direction:column;gap:calc(var(--s)*10px)}}.c{{background:rgba(255,255,255,.97);border-left:calc(var(--s)*8px) solid {A['key']};border-bottom:calc(var(--s)*3px) solid {A['acc']};border-radius:10px;padding:calc(var(--s)*10px) calc(var(--s)*16px);font:700 calc(var(--s)*{cf}px)/1.32 {fam};color:{A['ink']}}}"
           f".sub{{font:600 calc(var(--s)*{cf+3}px)/1.4 {fam};color:#fff}}.by{{margin-top:calc(var(--s)*16px);display:inline-block;white-space:nowrap;font:700 calc(var(--s)*{cf}px)/1 {fam};color:{A['ink']};background:#fff;padding:calc(var(--s)*13px) calc(var(--s)*24px);border-radius:999px}}</style>")
    js = (f"<script>document.fonts.ready.then(function(){{var r=document.documentElement,l=document.getElementById('l'),q=document.getElementById('rr'),best=1;for(var s=1;s<=3.2;s+=0.02){{r.style.setProperty('--s',s);"
          f"if(l.getBoundingClientRect().height>{avail}||q.getBoundingClientRect().height>{avail}||l.scrollWidth>{left_w}+2||{tf}*s>{maxt}||{cf}*s>40)break;best=s}}r.style.setProperty('--s',best)}});</script>")
    chips = chips.replace('<div class="r">', '<div class="r" id="rr">', 1)
    return css + f'<div class="bd"></div><div class="l" id="l"><div class="k">{kick}</div><div class="bar"></div><div class="h">{title}</div></div>{chips}' + js
def main_html(a, key, lang, bgp):
    b = 1 if lang == "bn" else 0; kick, title, rows = T[(a, key)][0][b], T[(a, key)][1][b], T[(a, key)][2][b]; lay = LAY[(a, key)]
    if lay[0] == "L":
        _, tw, y0, y1 = lay
        if key == "cover": body = left_block(a, lang, kick, title, [], tw, y0, y1, sub=rows[0], by=BY[b])
        else: body = left_block(a, lang, kick, title, rows, tw, y0, y1)
    else: body = band_block(a, lang, kick, title, rows, 900, 400)
    return page(a, lang, body, 1600, 900, bgp, 0)
def social_html(a, lang, bgp):
    b = 1 if lang == "bn" else 0; kick, title, sub = SOC[a][0][b], SOC[a][1][b], SOC[a][2][b]; lay = LAY[(a, "cover")]
    if lay[0] == "L":
        tw, y0, y1 = SOCIAL_L[a]; body = left_block(a, lang, kick, title, [], tw, y0, y1, sub=sub, by=BY[b])
    else:
        r = f'<div class="r" style="width:520px"><div class="sub">{sub}</div><div class="by">{BY[b]}</div></div>'
        body = band_block(a, lang, kick, title, [], 840, 440, right_html=r, left_w=860, right_w=520)
    return page(a, lang, body, 1600, 840, bgp, -30)
if __name__ == "__main__":
    only = set(sys.argv[1:])
    stamp = []
    tmp = BG / "_t.html"
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        def shot(html, w, h, out):
            tmp.write_text(html, encoding="utf-8"); pg = br.new_page(viewport={"width": w, "height": h}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(1300); pg.screenshot(path=str(out)); pg.close()
        for iid, (a, key) in M.items():
            if only and a not in only: continue
            A = ART[a]; out = R / "assets/img/blog" / A["dir"]; bgp = BG / f"{a}-{key}.webp"
            im = Image.open(SRC / f"{iid}-image.png").convert("RGB").resize((1600, 900), Image.LANCZOS)
            if (a, key) == ("pc", "label"):  # blur the printed dose lines: an illustrative picture must not carry a specific dose
                box = (1280, 770, 1600, 900); sx = 1600 / 1672
                region = (int(735 * sx), int(440 * sx), int(1185 * sx), int(630 * sx)); im.paste(im.crop(region).filter(ImageFilter.GaussianBlur(9)), region)
            im.save(bgp, "WEBP", quality=92, method=6)
            for lang in ("en", "bn"):
                png = BG / "_o.png"; shot(main_html(a, key, lang, bgp), 1600, 900, png)
                dst = out / (f"{A['pre']}-{key}" + ("" if lang == "en" else "-bn") + ".webp")
                Image.open(png).convert("RGB").save(dst, "WEBP", quality=86, method=6)
                stamp.append([f"/assets/img/blog/{A['dir']}/{dst.name}", "tr" if LAY[(a, key)][0] == "B" else "br"])
            if key == "cover":
                for lang in ("en", "bn"):
                    png = BG / "_o.png"; shot(social_html(a, lang, bgp), 1600, 840, png)
                    sm = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS); sm.save(out / f"{A['pre']}-social-{lang}.jpg", "JPEG", quality=88, optimize=True)
                    if lang == "en":
                        sm.save(out / f"{A['pre']}-card.webp", "WEBP", quality=84, method=6); sm.resize((750, 394), Image.LANCZOS).save(out / f"{A['pre']}-card-w750.webp", "WEBP", quality=82, method=6)
        br.close()
    for x in (tmp, BG / "_o.png"): x.unlink(missing_ok=True)
    json.dump(stamp, open("/tmp/stamp_q3.json", "w")); print(len(stamp), "images")
