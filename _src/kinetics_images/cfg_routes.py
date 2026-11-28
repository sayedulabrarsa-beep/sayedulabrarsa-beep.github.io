"""Routes of administration (5 Dec) graphics. Recipe: Deep Teal headline, keyword in Deep Teal on a Soft Sage pill, Amber Coral kicker
with a steel line, teal round badges, coral byline pill."""
from kchart import *
from nw_common import fo, checklist
OUT = "assets/img/blog/routes-of-administration"
PREFIX = "routes-of-administration"
RECIPE = f""".title{{color:{TEAL}}} .title i{{color:{TEAL};background:{SAGE};padding:0 .16em;border-radius:.3em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:#a8382a}} .kick:before{{background:{STEEL}}} .badge{{background:{TEAL};color:#fff;border-radius:50%}} .li{{--lc:{STEEL}}}
.byline{{background:#c2452f}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SRC = ("MSD Manual; StatPearls; IQWiG", "MSD Manual; StatPearls; IQWiG")
SOCIAL = dict(ts=(62, 66), pw=520, a=26)

def layers(bn):
    s = ""
    L = [(40, 110, "#F3D9C8", ("Skin (epidermis, dermis)", "ত্বক (এপিডার্মিস, ডার্মিস)")),
         (150, 120, "#FBEBD3", ("Fat under the skin", "ত্বকের নিচের চর্বি")),
         (270, 250, "#E9B7A6", ("Muscle", "পেশি"))]
    for y, h, c, nm in L:
        s += pill(30, y, 848, h, c, r=0)
        s += T(44, y + 34, nm[1] if bn else nm[0], 21 if not bn else 23, "start", "s", CHAR)
    s += f'<ellipse cx="800" cy="400" rx="70" ry="24" fill="#B9473F" stroke="#8E2F29" stroke-width="3"/>'
    s += T(800, 448, "শিরা" if bn else "Vein", 22 if not bn else 24, "middle", "b", "#8E2F29")
    needles = [(360, 96, 330, 140, "ID", ("within skin", "ত্বকের ভেতরে")), (470, 70, 470, 210, "SC", ("under skin", "ত্বকের নিচে")),
               (590, 60, 590, 380, "IM", ("into muscle", "পেশিতে")), (680, 60, 790, 395, "IV", ("into a vein", "শিরায়"))]
    for x1, y1, x2, y2, tag, d in needles:
        s += line(x1, y1 - 40, x2, y2, STEEL, 7) + line(x1, y1 - 40, x1 + (x2 - x1) * .25, y1 - 40 + (y2 - y1 + 40) * .25, CHAR, 14)
        s += f'<circle cx="{x2}" cy="{y2}" r="8" fill="{CORAL}"/>'
    for i, (x1, y1, x2, y2, tag, d) in enumerate(needles):
        x = 30 + i * 214
        s += pill(x, 540, 200, 120, "#fff", r=16, stroke=TEAL, sw=3)
        s += T(x + 100, 590, tag, 36, "middle", "b", TEAL) + T(x + 100, 632, d[1] if bn else d[0], 22 if not bn else 24, "middle", "s", CHAR)
    s += T(30, 700, "প্রতীকী, মাপ অনুযায়ী নয়; ইনজেকশন দেন প্রশিক্ষিত স্বাস্থ্যকর্মী" if bn else "Illustrative, not to scale. Injections are given by trained health workers or as taught.", 20 if not bn else 22, "start", "", STEEL)
    return s

def groups(bn):
    cols = [(("Enteral", "এন্টেরাল"), ("through the gut", "পরিপাকতন্ত্র দিয়ে"), TEAL, [("Oral (swallowed)", "মুখে খাওয়া"), ("Sublingual, buccal", "জিভের নিচে, গালে"), ("Rectal", "মলদ্বারে")]),
            (("Parenteral", "প্যারেন্টেরাল"), ("bypasses the gut", "পরিপাকতন্ত্র এড়িয়ে"), CORAL, [("Intravenous (IV)", "শিরায় (IV)"), ("Intramuscular (IM)", "পেশিতে (IM)"), ("Subcutaneous (SC)", "ত্বকের নিচে (SC)")]),
            (("Other routes", "অন্যান্য পথ"), ("airways, skin, eye, ear", "শ্বাসনালি, ত্বক, চোখ, কান"), STEEL, [("Inhaled, nasal", "ইনহেল, নাকে"), ("Topical, transdermal", "টপিক্যাল, ট্রান্সডার্মাল"), ("Eye, ear", "চোখ, কান")])]
    s = ""
    for i, (h, sub, c, items) in enumerate(cols):
        x = 24 + i * 292
        s += pill(x, 24, 272, 110, c, r=16)
        s += T(x + 136, 72, h[1] if bn else h[0], 30 if not bn else 32, "middle", "b", "#fff") + T(x + 136, 110, sub[1] if bn else sub[0], 20 if not bn else 22, "middle", "", "#fff")
        for k, it in enumerate(items):
            y = 160 + k * 112
            s += pill(x, y, 272, 92, "#fff", r=14, stroke=c, sw=3)
            s += fo(x + 12, y + 2, 248, 88, f'<span style="text-align:center;width:100%">{it[1] if bn else it[0]}</span>', bn, (23, 25), 600, CHAR, "center")
    s += pill(24, 520, 860, 196, SAGE, r=18)
    s += fo(50, 528, 810, 180, ("<b style='color:#174F52'>রুট বদলালে ফল বদলায়</b><span style='margin-top:6px'>IV ওষুধ সরাসরি রক্তে যায়; মুখে খাওয়া ওষুধ আগে শোষিত হতে হয়। তবু কোনো রুট সব ওষুধের জন্য সবসময় দ্রুত বা ভালো, এমন নয়। শুধু লেবেলে লেখা রুটেই ব্যবহার করুন।</span>" if bn else
                                "<b style='color:#174F52'>The route changes the result</b><span style='margin-top:6px'>IV medicine goes straight into the blood; oral medicine must be absorbed first. Still, no route is always faster or better for every medicine. Use only the route on the label.</span>"), bn, (23, 25), 500)
    return s

def takeaways(bn):
    return checklist([
      (("Route is the path in", "How a medicine enters or is applied to the body."), ("রুট মানে প্রবেশপথ", "ওষুধ কীভাবে শরীরে ঢোকে বা লাগানো হয়।")),
      (("Form is not route", "A tablet is a form; oral is a route."), ("ফর্ম আর রুট এক নয়", "ট্যাবলেট ফর্ম; মুখে খাওয়া রুট।")),
      (("IV, IM, SC differ", "Vein, muscle or under the skin."), ("IV, IM, SC আলাদা", "শিরা, পেশি বা ত্বকের নিচে।")),
      (("Technique matters", "Inhalers and patches need correct use."), ("কৌশল জরুরি", "ইনহেলার ও প্যাচ ঠিকভাবে ব্যবহার করুন।")),
      (("Only the labelled route", "Never put ear drops or skin creams in the eye."), ("শুধু লেবেলের রুট", "কানের ড্রপ বা ত্বকের ক্রিম চোখে নয়।"))], STEEL, TEAL, bn)

CFG = {
 "cover": dict(kind="photo", bg="ro-cover", a=22, pw=560, byline=True, foot=False, ts=(72, 76),
   kick=("Pharma Blog · Routes", "ফার্মা ব্লগ · প্রয়োগের পথ"),
   title=("How medicines <i>get in</i>", "ওষুধ শরীরে <i>কোন পথে</i> যায়"),
   sub=("By mouth, injection, inhaler, skin and more: the routes, simply explained.", "মুখে খাওয়া, ইনজেকশন, ইনহেলার, ত্বক ও আরও: সহজ ভাষায়।")),
 "groups": dict(svg=groups, pw=460, cx=590, ts=(56, 58), kick=("Three families", "তিন দলের পথ"),
   title=("Enteral, parenteral and <i>other</i>", "এন্টেরাল, প্যারেন্টেরাল ও <i>অন্যান্য</i>"),
   sub=("Grouping varies between references; the idea stays the same.", "শ্রেণিবিন্যাস বইভেদে একটু আলাদা; মূল ধারণা একই।"), src=SRC),
 "layers": dict(svg=layers, pw=460, cx=590, ts=(56, 58), kick=("Injection routes", "ইনজেকশনের পথ"),
   title=("ID, SC, IM and <i>IV</i>", "ID, SC, IM ও <i>IV</i>"),
   sub=("Where the needle delivers the medicine changes how it is absorbed.", "সুই কোথায় ওষুধ পৌঁছায়, তাতে শোষণ বদলায়।"), src=SRC),
 "takeaways": dict(svg=takeaways, pw=460, cx=590, ts=(58, 60), kick=("Key takeaways", "মূল কথা"),
   title=("Routes in <i>5 points</i>", "৫ কথায় <i>প্রয়োগের পথ</i>"), src=SRC),
}
NAMES = {"cover": "routes-of-drug-administration-cover", "groups": "enteral-parenteral-other-routes-of-administration",
         "layers": "injection-routes-intradermal-subcutaneous-intramuscular-intravenous", "takeaways": "routes-of-administration-key-takeaways"}
