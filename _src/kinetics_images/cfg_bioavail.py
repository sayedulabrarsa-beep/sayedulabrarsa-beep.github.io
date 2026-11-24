"""Bioavailability article graphics. Recipe: Deep Teal headline, keyword as white text on a Steel Blue tag, Charcoal kicker with a
Steel Blue line, Steel Blue square badges, gold legend edge, Steel Blue byline pill with a gold edge."""
import math
from kchart import *
from photo_common import L, EB, TOP, lab_css
OUT = "assets/img/blog/bioavailability"
PREFIX = "bioavailability"
RECIPE = f""".title{{color:{TEAL}}} .title i{{color:#fff;background:{STEEL};padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:{CHAR}}} .kick:before{{background:{STEEL}}} .badge{{background:{STEEL};color:#fff;border-radius:8px}} .li{{--lc:{GOLD}}}
.byline{{background:{STEEL};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
RECIPE += lab_css(STEEL)
SRC = ("StatPearls; MSD Manual; FDA; EUPATI", "StatPearls; MSD Manual; FDA; EUPATI")
SOCIAL = dict(ts=(68, 72), pw=520, a=26)
GREY = "#C9CFD2"

def dots(bn):
    s = ""
    def grid(ox, oy, cols, title):
        out = T(ox + 175, oy - 26, title, 28 if not bn else 30, "middle", "b", CHAR)
        for i in range(100):
            r, c = divmod(i, 10)
            out += f'<circle cx="{ox + c*35 + 14}" cy="{oy + r*35 + 14}" r="13" fill="{cols[i]}"/>'
        return out
    s += grid(60, 110, [TEAL] * 100, "ইনজেকশন (IV)" if bn else "Injection into a vein (IV)")
    s += grid(500, 110, [GREY] * 20 + [CORAL] * 20 + [TEAL] * 60, "মুখে খাওয়া (উদাহরণ)" if bn else "Tablet by mouth (example)")
    s += T(235, 510, "১০০ ভাগই রক্তে" if bn else "All 100 reach blood", 27 if not bn else 29, "middle", "b", TEAL)
    s += T(675, 510, "৬০ ভাগ রক্তে (উদাহরণ)" if bn else "60 reach blood (example)", 27 if not bn else 29, "middle", "b", TEAL)
    items = [(GREY, "শোষিত হয়নি" if bn else "Not absorbed"), (CORAL, "অন্ত্র-দেয়াল ও যকৃতে ভাঙা (first pass)" if bn else "Broken down in gut wall or liver (first pass)"), (TEAL, "অপরিবর্তিত অবস্থায় রক্তে পৌঁছায়" if bn else "Reaches the blood unchanged")]
    for k, (c, t) in enumerate(items):
        y = 572 + k * 44
        s += f'<circle cx="80" cy="{y-8}" r="13" fill="{c}"/>' + T(108, y, t, 25 if not bn else 27, "start", "s", CHAR)
    s += T(454, 724, "প্রকৃত সংখ্যা ওষুধভেদে আলাদা; এখানে শুধু ধারণা দেখানো হয়েছে" if bn else "Real numbers differ for every medicine; this only shows the idea", 22 if not bn else 24, "middle", "s", STEEL)
    return s

def auc(bn):
    x0, y0, x1, y1 = 120, 100, 860, 560
    X = lambda t: x0 + 10 + t * 62
    Y = lambda c: y1 - c * 400
    iv = [(X(t / 10), Y(math.exp(-0.35 * t / 10))) for t in range(0, 121)]
    oral = [(X(t / 10), Y(0.62 * bateman(t / 10))) for t in range(0, 121)]
    s = axes(x0, y0, x1, y1, "সময়" if bn else "Time", "রক্তে ওষুধের মাত্রা" if bn else "Drug level in blood", bn)
    s += poly([(X(0), y1)] + oral + [(X(12), y1)], "none", 0, fill="rgba(216,168,78,.35)")
    s += poly(iv, TEAL, 5) + poly(oral, CORAL, 5)
    m = max(oral, key=lambda p: -p[1])
    s += line(m[0], m[1], m[0], y1, CHAR, 2, "6 6") + line(x0, m[1], m[0], m[1], CHAR, 2, "6 6")
    s += pill(m[0] - 52, m[1] - 62, 104, 40, CORAL, r=10) + T(m[0], m[1] - 33, "Cmax", 24, "middle", "b", "#fff")
    s += pill(m[0] - 52, y1 + 10, 104, 38, CHAR, r=10) + T(m[0], y1 + 37, "Tmax", 23, "middle", "b", "#fff")
    s += T(X(1.0) + 30, Y(0.86), "IV", 30, "start", "b", TEAL)
    s += T(X(5.2), Y(0.36), "মুখে খাওয়া" if bn else "By mouth", 27 if not bn else 29, "start", "b", CORAL)
    s += T(X(2.6), Y(0.08), "AUC", 30, "middle", "b", "#8a6a1f")
    s += pill(470, 140, 400, 112, SAGE, r=16)
    s += T(490, 184, "AUC = মোট ওষুধ-এক্সপোজার" if bn else "AUC = total exposure", 26 if not bn else 28, "start", "b", TEAL)
    s += T(490, 224, "একই ডোজে মুখে ÷ IV = F" if bn else "Same dose: oral ÷ IV = F", 25 if not bn else 27, "start", "s", CHAR)
    s += T(454, 724, "প্রতীকী চিত্র, কোনো নির্দিষ্ট ওষুধের তথ্য নয়" if bn else "Illustrative curves, not data for any specific medicine", 22 if not bn else 24, "middle", "s", STEEL)
    return s

def be(bn):
    x0, x1 = 90, 840
    P = lambda v: x0 + (v - 70) / (135 - 70) * (x1 - x0)
    s = ""
    s += pill(P(80), 120, P(125) - P(80), 400, SAGE, r=14)
    s += T((P(80) + P(125)) / 2, 160, "গ্রহণযোগ্য সীমা ৮০–১২৫%" if bn else "Usual limit 80–125%", 28 if not bn else 30, "middle", "b", TEAL)
    for v in (80, 100, 125):
        s += line(P(v), 120 if v != 100 else 190, P(v), 520, TEAL if v != 100 else STEEL, 3, "8 8" if v == 100 else None)
        s += T(P(v), 560, num(v, bn) + "%", 26 if not bn else 28, "middle", "b", CHAR)
    s += line(x0, 520, x1, 520, CHAR, 3)
    rows = [(92, 106, 98, TEAL, "পাস: পুরো ব্যবধান সীমার ভেতরে" if bn else "Passes: whole interval inside"),
            (76, 101, 88, CORAL, "পাস নয়: সীমার বাইরে গেছে" if bn else "Fails: interval goes outside")]
    for k, (lo, hi, mid, c, lab) in enumerate(rows):
        y = 260 + k * 140
        s += line(P(lo), y, P(hi), y, c, 10) + line(P(lo), y - 22, P(lo), y + 22, c, 6) + line(P(hi), y - 22, P(hi), y + 22, c, 6)
        s += f'<circle cx="{P(mid):.0f}" cy="{y}" r="14" fill="#fff" stroke="{c}" stroke-width="6"/>'
        s += T(P(lo) if k else P(lo), y - 38, lab, 25 if not bn else 27, "start", "b", c)
    s += T(454, 620, "জেনেরিক ÷ রেফারেন্স ওষুধ (AUC ও Cmax-এর অনুপাত)" if bn else "Generic ÷ reference medicine (ratio of AUC and Cmax)", 24 if not bn else 26, "middle", "s", CHAR)
    s += T(454, 664, "রেখা = ৯০% কনফিডেন্স ইন্টারভাল; প্রতীকী উদাহরণ" if bn else "Line = 90% confidence interval; illustrative example", 22 if not bn else 24, "middle", "s", STEEL)
    return s

CFG = {
 "cover": dict(kind="photo", bg="ba-cover", a=22, pw=560, byline=True, foot=False, ts=(90, 92),
   kick=("Bioavailability", "বায়োঅ্যাভেইলেবিলিটি"),
   title=("How much <i>reaches</i> the blood", "রক্তে কতটুকু <i>পৌঁছায়</i>"),
   sub=("Why the dose you swallow is not always the dose your body gets.", "যে ডোজ খান, শরীর সবসময় পুরোটা পায় না কেন।")),
 "dots": dict(svg=dots, pw=500, ts=(62, 62),
   kick=("The percentage idea", "শতাংশের ধারণা"),
   title=("100 in, <i>how many</i> arrive?", "১০০ ভাগের <i>কত ভাগ</i> পৌঁছায়?"),
   sub=("IV is 100% by definition. By mouth, some is lost on the way.", "IV-তে সংজ্ঞা অনুযায়ী ১০০%। মুখে খেলে পথে কিছু অংশ হারায়।"),
   src=SRC),
 "auc": dict(svg=auc, pw=500, ts=(62, 62),
   kick=("How it is measured", "কীভাবে মাপা হয়"),
   title=("The area under <i>the curve</i>", "<i>কার্ভের</i> নিচের ক্ষেত্র"),
   sub=("Blood levels over time show total exposure (AUC) and the highest level (Cmax).", "সময়ের সাথে রক্তের মাত্রা থেকে মোট এক্সপোজার (AUC) ও সর্বোচ্চ মাত্রা (Cmax) জানা যায়।"),
   src=SRC),
 "be": dict(svg=be, pw=500, ts=(62, 64),
   kick=("Generic medicines", "জেনেরিক ওষুধ"),
   title=("What <i>bioequivalent</i> means", "<i>বায়োইকুইভ্যালেন্ট</i> মানে কী"),
   sub=("Same amount, same rate, same extent, within set statistical limits.", "একই পরিমাণ, একই গতি, একই মাত্রা, নির্দিষ্ট পরিসংখ্যান সীমার মধ্যে।"),
   src=("FDA Generic Drugs Q&A; FDA BE statistics guidance", "FDA Generic Drugs Q&A; FDA BE statistics guidance")),
 "takeaways": dict(kind="photo", bg="ba-takeaways", a=34, pw=640, ts=(64, 64),
   kick=("Key takeaways", "মূল কথা"), title=("Bioavailability in <i>5 points</i>", "৫ কথায় <i>বায়োঅ্যাভেইলেবিলিটি</i>"),
   legend=[(("A share of the dose", "The part reaching the blood unchanged."), ("ডোজের একটি অংশ", "যে অংশ অপরিবর্তিত অবস্থায় রক্তে যায়।")),
           (("IV = 100%", "It goes straight into the blood."), ("IV = ১০০%", "সরাসরি রক্তে যায়।")),
           (("Losses by mouth", "Absorption and first-pass metabolism."), ("মুখে খেলে ক্ষতি", "শোষণ ও first-pass metabolism।")),
           (("Food and form matter", "Meals, coating, other drugs."), ("খাবার ও রূপ", "খাবার, কোটিং, অন্য ওষুধ।")),
           (("Bioequivalence", "Generic matches the reference."), ("বায়োইকুইভ্যালেন্স", "জেনেরিক রেফারেন্সের সমান কাজ করে।"))],
   src=SRC),
}
NAMES = {"cover": "bioavailability-cover", "dots": "bioavailability-100-molecules-iv-vs-oral", "auc": "bioavailability-auc-cmax-tmax-curve",
         "be": "bioequivalence-80-125-percent-limits", "takeaways": "bioavailability-key-takeaways"}

SRCP = ("StatPearls; MSD Manual; FDA", "StatPearls; MSD Manual; FDA")
CFG.update({
 "iv": dict(kind="photo", bg="ba-iv", a=18, pw=520, ts=(60, 60), src=SRCP,
   kick=("The percentage idea", "শতাংশের ধারণা"),
   title=("IV is <i>100%</i>", "IV মানে <i>১০০%</i>"),
   sub=("An injection into a vein goes straight into the blood. A tablet often delivers less.", "শিরায় ইনজেকশন সরাসরি রক্তে যায়। ট্যাবলেটে প্রায়ই কম পৌঁছায়।"),
   extra=EB(lambda b: L(1185, 540, ("IV = 100%", "IV = ১০০%")[b], "pt", 30) + L(1010, 700, ("Tablet: often less", "ট্যাবলেট: প্রায়ই কম")[b], "pw", 28))),
 "firstpass": dict(kind="photo", bg="ba-firstpass", a=16, pw=480, ts=(56, 56), src=SRCP,
   kick=("First-pass effect", "ফার্স্ট-পাস প্রভাব"),
   title=("Some is lost <i>on the first trip</i>", "প্রথম যাত্রায় <i>কিছু হারায়</i>"),
   sub=("From the gut, blood goes through the portal vein to the liver before the rest of the body.", "অন্ত্র থেকে রক্ত পোর্টাল শিরা দিয়ে আগে যকৃতে যায়, তারপর সারা শরীরে।"),
   extra=EB(lambda b: L(1130, 745, ("1 · Gut", "১ · অন্ত্র")[b], "pw", 28) + L(1000, 440, ("2 · Portal vein", "২ · পোর্টাল শিরা")[b], "pw", 26)
                    + L(790, 140, ("3 · Liver breaks some down", "৩ · যকৃতে কিছু ভাঙে")[b], "pt", 28) + L(1290, 380, ("4 · The rest reaches the blood", "৪ · বাকিটা রক্তে যায়")[b], "pw", 26))),
 "food": dict(kind="photo", bg="ba-food", a=16, pw=500, ts=(58, 58), src=SRCP,
   kick=("Food matters", "খাবারের প্রভাব"),
   title=("Before or <i>after</i> food?", "খাবারের আগে না <i>পরে</i>?"),
   sub=("A meal can raise, lower or delay how much is absorbed. Follow the label.", "খাবার শোষণ বাড়াতে, কমাতে বা দেরি করাতে পারে। লেবেল মেনে চলুন।"),
   extra=EB(lambda b: L(1150, 735, ("Timing with meals changes absorption", "খাবারের সময় শোষণ বদলায়")[b], "ps", 27))),
 "forms": dict(kind="photo", bg="ba-forms", a=16, pw=500, ts=(58, 58), src=SRCP,
   kick=("The dosage form", "ওষুধের রূপ"),
   title=("Same drug, <i>different</i> forms", "একই ওষুধ, <i>ভিন্ন</i> রূপ"),
   sub=("Coating, particle size and how fast it dissolves change bioavailability.", "কোটিং, কণার আকার ও গলার গতি বায়োঅ্যাভেইলেবিলিটি বদলায়।"),
   extra=EB(lambda b: L(730, 745, ("Coated tablet", "কোটেড ট্যাবলেট")[b], "pw", 25) + L(1015, 745, ("Capsule", "ক্যাপসুল")[b], "pw", 25)
                    + L(1355, 745, ("Dispersible tablet", "ডিসপারসিবল ট্যাবলেট")[b], "pw", 25))),
 "measure": dict(kind="photo", bg="ba-measure", a=16, pw=470, ts=(56, 56), src=SRCP,
   kick=("How it is measured", "কীভাবে মাপা হয়"),
   title=("Blood samples <i>over time</i>", "সময়ের সাথে <i>রক্তের নমুনা</i>"),
   sub=("Levels at set times draw the curve that gives AUC, Cmax and Tmax.", "নির্দিষ্ট সময়ে মাপা মাত্রা থেকে কার্ভ, AUC, Cmax ও Tmax পাওয়া যায়।"),
   extra=EB(lambda b: L(757, 268, ("Time", "সময়")[b], "pt", 28) + L(1240, 735, ("Drug level in each sample", "প্রতিটি নমুনায় ওষুধের মাত্রা")[b], "pw", 26))),
 "bephoto": dict(kind="photo", bg="ba-be", a=16, pw=480, ts=(56, 56), src=("FDA Generic Drugs Q&A", "FDA Generic Drugs Q&A"),
   kick=("Generic medicines", "জেনেরিক ওষুধ"),
   title=("Same amount, <i>same rate</i>", "একই পরিমাণ, <i>একই গতি</i>"),
   sub=("A generic must be bioequivalent to the reference medicine.", "জেনেরিককে রেফারেন্স ওষুধের সাথে বায়োইকুইভ্যালেন্ট হতে হয়।"),
   extra=EB(lambda b: L(855, 300, ("Generic", "জেনেরিক")[b], "pt", 28) + L(1360, 300, ("Reference", "রেফারেন্স")[b], "pt", 28)
                    + L(1110, 745, ("Bioequivalent: they balance", "বায়োইকুইভ্যালেন্ট: সমান ভারসাম্য")[b], "ps", 27))),
})
NAMES.update({"iv": "bioavailability-iv-100-percent-vs-tablet", "firstpass": "first-pass-metabolism-gut-portal-vein-liver",
              "food": "food-effect-on-drug-absorption-before-after-meals", "forms": "dosage-form-coated-tablet-capsule-dispersible-bioavailability",
              "measure": "bioavailability-blood-samples-auc-measurement", "bephoto": "bioequivalence-generic-vs-reference-medicine-balance"})
