"""Rx vs OTC in Bangladesh article graphics. Recipe: Charcoal headline, keyword in Charcoal on a Muted Gold tag, Deep Teal kicker
with a coral line, Deep Teal round badges, Steel Blue legend edge, Deep Teal byline pill with a gold edge."""
from kchart import *
from photo_common import L, EB, TOP, lab_css
OUT = "assets/img/blog/prescription-vs-otc"
PREFIX = "prescription-vs-otc"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:{CHAR};background:{GOLD};padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:{TEAL}}} .kick:before{{background:{CORAL}}} .badge{{background:{TEAL};color:#fff;border-radius:50%}} .li{{--lc:{STEEL}}}
.byline{{background:{TEAL};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
RECIPE += lab_css(GOLD)
SRC = ("FDA; Drugs and Cosmetics Act 2023; National Drug Policy 2016", "FDA; ঔষধ ও কসমেটিকস আইন ২০২৩; জাতীয় ঔষধনীতি ২০১৬")
SOCIAL = dict(ts=(68, 72), pw=540, a=26)
RED = "#C0392B"

def compare(bn):
    s = pill(40, 40, 400, 76, TEAL, r=16) + pill(468, 40, 400, 76, GOLD, r=16)
    s += T(240, 90, "প্রেসক্রিপশন (Rx)" if bn else "Prescription (Rx)", 30 if not bn else 32, "middle", "b", "#fff")
    s += T(668, 90, "OTC (প্রেসক্রিপশন ছাড়া)" if bn else "OTC (no prescription)", 30 if not bn else 30, "middle", "b", CHAR)
    rows = [
      (("কে ঠিক করেন", "Who decides"), ("রেজিস্টার্ড চিকিৎসক, একজন রোগীর জন্য", "A registered doctor, for one person"), ("আপনি, ছোট ও স্বল্পমেয়াদি সমস্যায়", "You, for minor short-term problems")),
      (("কোথায় পাবেন", "Where"), ("ফার্মেসি, প্রেসক্রিপশন দেখিয়ে", "A pharmacy, against the prescription"), ("ফার্মেসি, প্রেসক্রিপশন ছাড়াই", "A pharmacy, without a prescription")),
      (("কোন ওষুধ", "Which ones"), ("অ্যান্টিবায়োটিকসহ বেশিরভাগ ওষুধ", "Most medicines, including antibiotics"), ("শুধু সরকারি OTC তালিকার ওষুধ", "Only those on the official OTC list")),
      (("আপনার কাজ", "Your part"), ("পুরো কোর্স, নির্দেশমতো", "Follow the full course as directed"), ("লেবেল পড়ুন, ফার্মাসিস্টকে জিজ্ঞেস করুন", "Read the label, ask the pharmacist")),
    ]
    for k, (h, a, b) in enumerate(rows):
        y = 140 + k * 140
        s += T(40, y + 30, h[0] if bn else h[1], 23 if not bn else 25, "start", "b", STEEL)
        s += pill(40, y + 44, 400, 82, "#F3F8F7", r=14) + pill(468, y + 44, 400, 82, "#FBF5EA", r=14)
        for (cx, txt) in ((60, a), (488, b)):
            t = txt[0] if bn else txt[1]
            s += f'<foreignObject x="{cx}" y="{y+50}" width="364" height="72"><div xmlns="http://www.w3.org/1999/xhtml" style="height:72px;display:flex;align-items:center;font:{"500 25px HS" if bn else "500 23px Int"},sans-serif;line-height:1.2;color:{CHAR}">{t}</div></foreignObject>'
    return s

def label(bn):
    s = ""
    # fictional pack, front face
    px, py, pw, ph = 70, 90, 470, 300
    s += f'<path d="M{px+pw},{py} l60,-40 v{ph} l-60,40 Z" fill="#e9ecec"/><path d="M{px},{py} l60,-40 h{pw} l-60,40 Z" fill="#f4f6f6"/>'
    s += pill(px, py, pw, ph, "#fff", r=6, stroke="#d5dadb", sw=2)
    s += pill(px, py + 180, pw, 100, RED, r=0)
    s += T(px + 26, py + 64, "Generic name", 34, "start", "b", CHAR) + T(px + 26, py + 104, "500 mg · 10 capsules", 24, "start", "s", STEEL)
    s += T(px + 26, py + 152, "ANTIBIOTIC", 30, "start", "b", RED)
    s += T(px + pw / 2, py + 222, "Do not use without a prescription", 23, "middle", "b", "#fff")
    s += T(px + pw / 2, py + 258, "of registered physician", 23, "middle", "b", "#fff")
    s += T(px + 6, py + ph + 36, "কাল্পনিক উদাহরণ প্যাক, কোনো ব্র্যান্ড নয়" if bn else "Fictional example pack, not a real brand", 21 if not bn else 23, "start", "s", STEEL)
    calls = [(py + 60, "১ লাল রং ও লেখা" if bn else "1 Red marking", "অ্যান্টিবায়োটিক চেনায়" if bn else "Shows it is an antibiotic"),
             (py + 180, "২ সতর্কবার্তা" if bn else "2 The warning", "প্রেসক্রিপশন ছাড়া নয়" if bn else "Not without a prescription"),
             (py + 300, "৩ মানুষ ও পশু" if bn else "3 Human and animal", "দুই ধরনের প্যাকেই নিয়ম" if bn else "Rule covers both packs")]
    for y, a, b in calls:
        s += line(626, y, 600, y, CHAR, 2, "3 6")
        s += pill(626, y - 44, 270, 92, "#fff", r=12, stroke=RED, sw=3)
        s += T(642, y - 8, a, 23 if not bn else 25, "start", "b", RED) + T(642, y + 28, b, 20 if not bn else 22, "start", "s", CHAR)
    s += pill(40, 520, 828, 150, SAGE, r=16)
    s += T(64, 566, "DGDA-র নিয়ম (২০২২ থেকে)" if bn else "DGDA rule (from 2022)", 26 if not bn else 28, "start", "b", TEAL)
    s += T(64, 608, "অ্যান্টিবায়োটিকের প্যাকে লাল চিহ্ন, ‘Antibiotic’ শব্দ ও" if bn else "Antibiotic packs carry a red marking, the word ‘Antibiotic’", 23 if not bn else 25, "start", "s", CHAR)
    s += T(64, 644, "প্রেসক্রিপশন-সতর্কবার্তা থাকে (WHO বাংলাদেশ, ২০২৩)" if bn else "and a prescription warning (WHO Bangladesh, 2023)", 23 if not bn else 25, "start", "s", CHAR)
    return s

CFG = {
 "cover": dict(kind="photo", bg="rx-cover", a=22, pw=580, byline=True, foot=False, ts=(80, 84),
   kick=("Rx vs OTC in Bangladesh", "Rx বনাম OTC, বাংলাদেশে"),
   title=("Which medicines need a <i>prescription</i>?", "কোন ওষুধে <i>প্রেসক্রিপশন</i> লাগে?"),
   sub=("Prescription-only and over-the-counter medicines, simply explained.", "প্রেসক্রিপশন-ওষুধ ও OTC ওষুধ, সহজ ভাষায়।")),
 "compare": dict(svg=compare, pw=500, ts=(62, 64),
   kick=("Side by side", "পাশাপাশি তুলনা"),
   title=("Rx or <i>OTC</i>?", "Rx নাকি <i>OTC</i>?"),
   sub=("In Bangladesh, only medicines on the official OTC list may be sold without a prescription.", "বাংলাদেশে শুধু সরকারি OTC তালিকার ওষুধ প্রেসক্রিপশন ছাড়া বিক্রি করা যায়।"),
   src=SRC),
 "label": dict(svg=label, pw=500, ts=(60, 60),
   kick=("Spot an antibiotic", "অ্যান্টিবায়োটিক চিনুন"),
   title=("The <i>red</i> antibiotic label", "অ্যান্টিবায়োটিকের <i>লাল</i> লেবেল"),
   sub=("Red marking and a warning remind everyone: prescription only.", "লাল চিহ্ন ও সতর্কবার্তা মনে করিয়ে দেয়: শুধু প্রেসক্রিপশনে।"),
   src=("WHO Bangladesh 2023 and 2024; DGDA", "WHO বাংলাদেশ ২০২৩ ও ২০২৪; DGDA")),
 "takeaways": dict(kind="photo", bg="rx-takeaways", a=34, pw=640, ts=(62, 62),
   kick=("Key takeaways", "মূল কথা"), title=("Rx and OTC in <i>5 points</i>", "৫ কথায় <i>Rx ও OTC</i>"),
   legend=[(("Rx is personal", "Prescribed for one person."), ("Rx ব্যক্তিগত", "একজনের জন্য লেখা।")),
           (("OTC is a short list", "Not every medicine on the shelf."), ("OTC তালিকা ছোট", "তাকের সব ওষুধ OTC নয়।")),
           (("Antibiotics need Rx", "It is the law in Bangladesh."), ("অ্যান্টিবায়োটিকে Rx", "বাংলাদেশের আইন এটাই।")),
           (("Read the label", "Check the active ingredient."), ("লেবেল পড়ুন", "সক্রিয় উপাদান দেখুন।")),
           (("Ask the pharmacist", "Especially for children or other medicines."), ("ফার্মাসিস্টকে জিজ্ঞেস", "বিশেষ করে শিশু বা অন্য ওষুধ চললে।"))],
   src=SRC),
}
NAMES = {"cover": "prescription-vs-otc-cover", "compare": "rx-vs-otc-comparison-bangladesh",
         "label": "red-antibiotic-label-bangladesh", "takeaways": "prescription-vs-otc-key-takeaways"}

PACK = ('<div style="position:absolute;left:948px;top:441px;width:518px;height:76px;display:flex;align-items:center;justify-content:center;'
        'font-family:Pop,sans-serif;font-weight:800;font-size:40px;letter-spacing:.12em;color:#fff">ANTIBIOTIC</div>'
        '<div style="position:absolute;left:960px;top:340px;width:494px;text-align:center;font-family:Int,sans-serif;font-weight:600;font-size:21px;line-height:1.3;color:#253238">'
        'Do not use without a prescription<br>of registered physician</div>')
CFG.update({
 "prescription": dict(kind="photo", bg="rx-prescription", a=12, pw=420, ts=(52, 52), panelcss=TOP, src=("U.S. FDA", "U.S. FDA"),
   kick=("Prescription (Rx)", "প্রেসক্রিপশন (Rx)"),
   title=("Chosen for <i>one person</i>", "একজন মানুষের <i>জন্য</i>"),
   sub=("A registered doctor decides the medicine, dose and length of treatment.", "রেজিস্টার্ড চিকিৎসক ওষুধ, ডোজ ও কতদিন খাবেন তা ঠিক করেন।"),
   extra=EB(lambda b: L(1000, 740, ("Written by a registered doctor", "রেজিস্টার্ড চিকিৎসকের লেখা")[b], "ps", 27))),
 "amr": dict(kind="photo", bg="rx-amr", a=16, pw=500, ts=(56, 56), src=("WHO antimicrobial resistance fact sheet", "WHO অ্যান্টিমাইক্রোবিয়াল রেজিস্ট্যান্স ফ্যাক্ট শিট"),
   kick=("Why antibiotics need Rx", "অ্যান্টিবায়োটিকে কেন Rx"),
   title=("Misuse breeds <i>resistance</i>", "অপব্যবহারে বাড়ে <i>রেজিস্ট্যান্স</i>"),
   sub=("WHO: misuse and overuse of antimicrobials drive drug-resistant infections.", "WHO: অ্যান্টিমাইক্রোবিয়ালের অপব্যবহার ও অতিরিক্ত ব্যবহার ওষুধ-প্রতিরোধী সংক্রমণ বাড়ায়।"),
   extra=EB(lambda b: L(1170, 745, ("Bacteria in a lab dish (illustration)", "ল্যাবের ডিশে ব্যাকটেরিয়া (প্রতীকী)")[b], "pw", 25))),
 "antibiotic": dict(kind="photo", bg="rx-antibiotic", a=16, pw=470, ts=(56, 56), src=("WHO Bangladesh 2023 and 2024; DGDA", "WHO বাংলাদেশ ২০২৩ ও ২০২৪; DGDA"),
   kick=("Spot an antibiotic", "অ্যান্টিবায়োটিক চিনুন"),
   title=("The <i>red</i> antibiotic label", "অ্যান্টিবায়োটিকের <i>লাল</i> লেবেল"),
   sub=("Since 2022, DGDA requires a red marking, the word Antibiotic and a prescription warning.", "২০২২ থেকে DGDA লাল চিহ্ন, Antibiotic শব্দ ও প্রেসক্রিপশন-সতর্কবার্তা বাধ্যতামূলক করেছে।"),
   extra=EB(lambda b: PACK + L(1205, 745, ("Example pack, not a real brand", "উদাহরণ প্যাক, কোনো ব্র্যান্ড নয়")[b], "pw", 24))),
 "ask": dict(kind="photo", bg="rx-ask", a=16, pw=470, ts=(56, 56), src=("FDA; MedlinePlus", "FDA; MedlinePlus"),
   kick=("Use your pharmacist", "ফার্মাসিস্টের সাহায্য নিন"),
   title=("Ask before you <i>buy</i>", "কেনার আগে <i>জিজ্ঞেস</i> করুন"),
   sub=("Active ingredient, dose, timing, side effects and your other medicines.", "সক্রিয় উপাদান, ডোজ, সময়, পার্শ্বপ্রতিক্রিয়া ও আপনার অন্য ওষুধ।"),
   extra=EB(lambda b: L(1060, 745, ("Read the leaflet together", "লিফলেট একসাথে পড়ুন")[b], "ps", 27))),
})
NAMES.update({"prescription": "prescription-medicine-written-by-registered-doctor", "amr": "antibiotic-misuse-antimicrobial-resistance-bacteria",
              "antibiotic": "red-antibiotic-label-pack-bangladesh-dgda", "ask": "ask-your-pharmacist-medicine-leaflet-bangladesh"})

CFG.update({
 "otcshelf": dict(kind="photo", bg="rx-otcshelf", a=16, pw=470, ts=(56, 56), src=("U.S. FDA; MedlinePlus", "U.S. FDA; MedlinePlus"),
   kick=("Using OTC medicines", "OTC ওষুধের ব্যবহার"),
   title=("Read the label <i>every time</i>", "প্রতিবার <i>লেবেল পড়ুন</i>"),
   sub=("Check the active ingredient so you do not take the same medicine twice.", "সক্রিয় উপাদান মিলিয়ে নিন, যাতে একই ওষুধ দুবার না খান।"),
   extra=EB(lambda b: L(1010, 420, ("Active ingredient?", "সক্রিয় উপাদান কী?")[b], "pt", 27) + L(1060, 735, ("Dose · warnings · expiry", "ডোজ · সতর্কতা · মেয়াদ")[b], "pw", 25))),
})
NAMES.update({"otcshelf": "read-otc-medicine-label-active-ingredient"})
