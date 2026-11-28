"""Paracetamol safety (B3, 3 Dec) graphics. No dose figures anywhere (doses come only from the product label; user review pending).
Recipe: Charcoal headline, keyword as white text on an Amber Coral tag, Steel Blue kicker with a teal line, coral round badges,
Deep Teal byline pill with a gold edge."""
from kchart import *
from nw_common import fo, checklist
from photo_common import L, EB, lab_css
OUT = "assets/img/blog/paracetamol-safety"
PREFIX = "paracetamol-safety"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:#fff;background:#c2452f;padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:{STEEL}}} .kick:before{{background:{TEAL}}} .badge{{background:{CORAL};color:#fff;border-radius:50%}} .li{{--lc:{CORAL}}}
.byline{{background:{TEAL};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}""" + lab_css(CORAL)
SRC = ("FDA; NHS; MedlinePlus; StatPearls", "FDA; NHS; MedlinePlus; StatPearls")
SOCIAL = dict(ts=(62, 66), pw=520, a=26)
RED = "#B03A2E"

def hidden(bn):
    packs = [(("Pain tablet", "ব্যথার ট্যাবলেট"), TEAL), (("Cold and flu remedy", "সর্দি-জ্বরের ওষুধ"), STEEL), (("Fever syrup", "জ্বরের সিরাপ"), GOLD)]
    s = ""
    for i, (nm, c) in enumerate(packs):
        x = 30 + i * 290
        s += pill(x, 30, 260, 250, "#fff", r=16, stroke=c, sw=4) + pill(x, 30, 260, 64, c, r=16) + pill(x, 70, 260, 24, c, r=0)
        s += fo(x + 10, 32, 240, 60, f'<span style="color:#fff;text-align:center;width:100%">{nm[1] if bn else nm[0]}</span>', bn, (22, 24), 700, "#fff", "center")
        s += T(x + 130, 140, "সক্রিয় উপাদান:" if bn else "Active ingredient:", 20 if not bn else 22, "middle", "", STEEL)
        s += pill(x + 22, 158, 216, 52, "#FBE3DA", r=10) + T(x + 130, 193, "প্যারাসিটামল" if bn else "Paracetamol", 25 if not bn else 27, "middle", "b", RED)
        s += T(x + 130, 248, "+ অন্য উপাদান থাকতে পারে" if bn else "+ maybe other ingredients", 18 if not bn else 20, "middle", "", STEEL)
        s += line(x + 130, 282, 454, 380, CHAR, 3, "6 6")
    s += f'<path d="M440,372 L454,392 L468,372 Z" fill="{CHAR}"/>'
    s += pill(170, 400, 568, 110, RED, r=20)
    s += fo(190, 404, 528, 102, ("<b>২৪ ঘণ্টায় সব মিলিয়ে একটাই মোট হিসাব</b>" if bn else "<b>All add up to ONE total for 24 hours</b>"), bn, (28, 30), 700, "#fff", "center")
    s += pill(30, 548, 848, 168, SAGE, r=18)
    s += fo(56, 556, 800, 152, ("<b style='color:#174F52'>অ্যাসিটামিনোফেন = প্যারাসিটামল</b><span style='margin-top:6px'>দুটি ওষুধ একসাথে খাওয়ার আগে সক্রিয় উপাদান মিলিয়ে নিন। নিশ্চিত না হলে ফার্মাসিস্টকে জিজ্ঞেস করুন। সর্বোচ্চ মাত্রা শুধু প্যাকের নির্দেশনা থেকে নিন।</span>" if bn else
                                "<b style='color:#174F52'>Acetaminophen = paracetamol</b><span style='margin-top:6px'>Compare active ingredients before combining two medicines. If unsure, ask a pharmacist. Take the maximum only from the product's own label.</span>"), bn, (23, 25), 500)
    return s

def urgent(bn):
    s = ""
    steps = [(("Do not wait for symptoms", "উপসর্গের অপেক্ষা করবেন না"), ("A person may feel well at first.", "শুরুতে মানুষটি ভালো বোধ করতে পারেন।")),
             (("Get urgent medical help", "দ্রুত চিকিৎসা নিন"), ("Nearest emergency department or emergency services.", "নিকটতম জরুরি বিভাগ বা জরুরি সেবা।")),
             (("Take the packs with you", "প্যাকগুলো সাথে নিন"), ("Product, strength, how much and when.", "কোন ওষুধ, শক্তি, কতটা ও কখন।")),
             (("Give no more paracetamol", "আর প্যারাসিটামল দেবেন না"), ("Do not try to treat it at home.", "বাড়িতে নিজে চিকিৎসার চেষ্টা নয়।"))]
    for i, (a, b) in enumerate(steps):
        y = 30 + i * 128
        s += pill(30, y, 848, 112, "#fff", r=16, stroke="#ecd2cb", sw=2) + pill(30, y, 12, 112, RED, r=4)
        s += f'<circle cx="104" cy="{y+56}" r="32" fill="{RED}"/>' + T(104, y + 67, num(i + 1, bn), 32, "middle", "b", "#fff")
        s += fo(160, y + 6, 700, 100, f'<b style="font-family:{"HS" if bn else "Pop"};font-weight:{700 if bn else 800};font-size:{31 if bn else 29}px;color:{CHAR}">{a[1] if bn else a[0]}</b><span style="margin-top:4px">{b[1] if bn else b[0]}</span>', bn)
    s += pill(30, 560, 848, 156, "#FBE3DA", r=18)
    s += fo(56, 566, 800, 144, ("অতিরিক্ত মাত্রা লিভারের মারাত্মক ক্ষতি করতে পারে, যদিও প্রথমে কোনো উপসর্গ না-ও থাকতে পারে। সন্দেহ হলেই সাহায্য নিন।" if bn else
                                "Too much paracetamol can seriously damage the liver, even when there are no early symptoms. If in doubt, get help."), bn, (25, 27), 600, RED)
    return s

def takeaways(bn):
    return checklist([
      (("Read the label every time", "Strength, dose, interval and maximum."), ("প্রতিবার লেবেল পড়ুন", "শক্তি, ডোজ, বিরতি ও সর্বোচ্চ মাত্রা।")),
      (("Count every product", "Cold and flu remedies may contain it too."), ("সব ওষুধ গুনে দেখুন", "সর্দি-জ্বরের ওষুধেও থাকতে পারে।")),
      (("Children need their own product", "Use the supplied measuring device."), ("শিশুর জন্য আলাদা ওষুধ", "সাথে দেওয়া মাপনি ব্যবহার করুন।")),
      (("Some people should ask first", "Liver disease, heavy alcohol use, low body weight."), ("কারও আগে জিজ্ঞেস করা দরকার", "লিভারের রোগ, বেশি অ্যালকোহল, কম ওজন।")),
      (("Too much? Act now", "Get urgent help even if the person feels well."), ("বেশি খেয়েছেন? এখনই", "ভালো বোধ করলেও দ্রুত চিকিৎসা নিন।"))], RED, CORAL, bn)

CFG = {
 "cover": dict(kind="photo", bg="pc-cover", a=24, pw=560, byline=True, foot=False, ts=(72, 76),
   kick=("Pharma Blog · Medicine safety", "ফার্মা ব্লগ · ওষুধের নিরাপত্তা"),
   title=("Paracetamol: use it <i>safely</i>", "প্যারাসিটামল: <i>নিরাপদে</i> ব্যবহার"),
   sub=("Read the label, count every product, and act fast if too much was taken.", "লেবেল পড়ুন, সব ওষুধ গুনুন, বেশি খেলে দ্রুত ব্যবস্থা নিন।"),
   extra=EB(lambda b: L(1410, 664, ("Read the label", "লেবেল পড়ুন")[b], "pw", 34, "padding:16px 34px"))),
 "hidden": dict(svg=hidden, pw=460, cx=590, ts=(56, 58), kick=("Hidden paracetamol", "লুকানো প্যারাসিটামল"),
   title=("One ingredient, <i>many packs</i>", "একই উপাদান, <i>অনেক প্যাকে</i>"),
   sub=("Accidental double dosing often comes from combination products.", "অজান্তে দ্বিগুণ ডোজ প্রায়ই আসে কম্বিনেশন ওষুধ থেকে।"), src=SRC),
 "urgent": dict(svg=urgent, pw=460, cx=590, ts=(56, 58), kick=("Possible overdose", "সম্ভাব্য অতিরিক্ত মাত্রা"),
   title=("Act <i>now</i>, not later", "<i>এখনই</i> ব্যবস্থা নিন"),
   sub=("Feeling well soon after does not rule out serious poisoning.", "পরে ভালো লাগলেও গুরুতর বিষক্রিয়া বাদ দেওয়া যায় না।"), src=("NHS; StatPearls; FDA", "NHS; StatPearls; FDA")),
 "takeaways": dict(svg=takeaways, pw=460, cx=590, ts=(58, 60), kick=("Key takeaways", "মূল কথা"),
   title=("Paracetamol in <i>5 points</i>", "৫ কথায় <i>প্যারাসিটামল</i>"), src=SRC),
}
NAMES = {"cover": "paracetamol-safety-cover", "hidden": "hidden-paracetamol-combination-products-one-total",
         "urgent": "paracetamol-overdose-what-to-do-urgent-help", "takeaways": "paracetamol-safety-key-takeaways"}
