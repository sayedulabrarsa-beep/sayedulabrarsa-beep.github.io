"""Dosage Forms (30 Nov) graphics. Recipe: Deep Teal headline, keyword in Amber Coral, Steel Blue kicker with a gold line,
gold round badges, teal byline pill with a coral edge."""
from kchart import *
from nw_common import fo, checklist
OUT = "assets/img/blog/dosage-forms"
PREFIX = "dosage-forms"
RECIPE = f""".title{{color:{TEAL}}} .title i{{color:{CORAL}}} .kick{{color:{STEEL}}} .kick:before{{background:{GOLD}}}
.badge{{background:{GOLD};color:#fff;border-radius:50%}} .li{{--lc:{CORAL}}} .byline{{background:{TEAL};border-left:6px solid {CORAL}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SRC = ("WHO EML dosage-form terms; IQWiG; NHS SPS", "WHO EML; IQWiG; NHS SPS")
SOCIAL = dict(ts=(64, 68), pw=520, a=24)

def tree(bn):
    groups = [
      (("Solid oral", "মুখে খাওয়ার কঠিন"), TEAL, [("Tablets", "ট্যাবলেট"), ("Capsules", "ক্যাপসুল"), ("Powders, granules", "পাউডার, গ্রানিউল")]),
      (("Liquid", "তরল"), STEEL, [("Solutions, syrups", "সলিউশন, সিরাপ"), ("Suspensions", "সাসপেনশন"), ("Drops", "ড্রপ")]),
      (("Skin and body surfaces", "ত্বক ও দেহের উপরিভাগ"), CORAL, [("Creams, ointments, gels", "ক্রিম, মলম, জেল"), ("Eye, ear, nose drops", "চোখ, কান, নাকের ড্রপ"), ("Transdermal patch", "ট্রান্সডার্মাল প্যাচ")]),
      (("Inhaled, injected, other", "ইনহেল, ইনজেকশন, অন্যান্য"), GOLD, [("Inhalers, nebulisers", "ইনহেলার, নেবুলাইজার"), ("Injections, infusions", "ইনজেকশন, ইনফিউশন"), ("Suppositories, pessaries", "সাপোজিটরি, পেসারি")]),
    ]
    s = pill(254, 24, 400, 76, TEAL, r=38) + T(454, 72, "ডোজেজ ফর্ম" if bn else "Dosage form", 34, "middle", "b", "#fff")
    for i, (h, c, items) in enumerate(groups):
        x = 24 + i * 218
        s += line(454, 100, x + 100, 150, CHAR, 2, op=.5)
        s += pill(x, 150, 200, 96, c, r=14)
        s += fo(x + 8, 152, 184, 92, f'<b style="color:#fff;text-align:center;width:100%">{h[1] if bn else h[0]}</b>', bn, (22, 24), 700, "#fff", "center", 1.15)
        for k, it in enumerate(items):
            y = 276 + k * 112
            s += line(x + 100, y - 30 if k == 0 else y - 18, x + 100, y, c, 3, op=.6)
            s += pill(x, y, 200, 92, "#fff", r=14, stroke=c, sw=3)
            s += fo(x + 10, y + 2, 180, 88, f'<span style="text-align:center;width:100%">{it[1] if bn else it[0]}</span>', bn, (21, 23), 600, CHAR, "center", 1.15)
    s += pill(24, 626, 860, 92, SAGE, r=16)
    s += fo(48, 630, 816, 84, ("একই সক্রিয় উপাদান একাধিক ফর্মে থাকতে পারে; ফর্মগুলো আপনাআপনি বদলযোগ্য নয়।" if bn else
                               "The same active ingredient can come in more than one form. Forms are not automatically interchangeable."), bn, (22, 24), 600, TEAL)
    return s

def liquids(bn):
    s = ""
    for i, (title, desc, kind) in enumerate([(("Solution", "সলিউশন"), ("Drug fully dissolved: clear, even liquid", "ওষুধ পুরো গলে থাকে: স্বচ্ছ, সমান তরল"), 0),
                                              (("Suspension", "সাসপেনশন"), ("Tiny particles spread through: may settle", "ছোট কণা ছড়িয়ে থাকে: নিচে জমতে পারে"), 1)]):
        x = 40 + i * 440
        s += pill(x, 24, 390, 470, "#FBFDFC", r=18, stroke="#d6e2df", sw=2)
        s += T(x + 195, 80, title[1] if bn else title[0], 34, "middle", "b", TEAL)
        bx, by = x + 125, 120
        s += f'<rect x="{bx+45}" y="{by}" width="50" height="34" rx="6" fill="{STEEL}"/>'
        s += f'<path d="M{bx+30},{by+34} h80 q30,10 30,50 v190 q0,22 -22,22 h-96 q-22,0 -22,-22 v-190 q0,-40 30,-50 Z" fill="#fff" stroke="{CHAR}" stroke-width="3"/>'
        fill = "#F6E2C4" if kind == 0 else "#F3EBDD"
        s += f'<path d="M{bx+10},{by+130} h120 v124 q0,18 -18,18 h-84 q-18,0 -18,-18 Z" fill="{fill}"/>'
        if kind:
            import random
            rnd = random.Random(4)
            for _ in range(34):
                px, py = bx + 18 + rnd.random() * 104, by + 140 + rnd.random() ** .5 * 120
                s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{CORAL}" opacity=".85"/>'
        s += fo(x + 24, 410, 342, 76, f'<span style="text-align:center;width:100%">{desc[1] if bn else desc[0]}</span>', bn, (22, 24), 600, CHAR, "center")
    s += pill(40, 520, 830, 196, SAGE, r=18)
    tips = [("Shake only if the label says so", "লেবেলে বললে তবেই ঝাঁকান"), ("Measure with the supplied syringe or cup", "সাথে দেওয়া সিরিঞ্জ বা কাপে মাপুন"), ("Not a household spoon", "ঘরের চামচ দিয়ে নয়")]
    for k, t in enumerate(tips):
        y = 552 + k * 56
        s += f'<circle cx="80" cy="{y+12}" r="16" fill="{CORAL}"/>' + T(80, y + 20, num(k + 1, bn), 22, "middle", "b", "#fff")
        s += T(112, y + 22, t[1] if bn else t[0], 25 if bn else 24, "start", "s", CHAR)
    return s

def takeaways(bn):
    return checklist([
      (("A form is the product's shape", "Tablet, capsule, liquid, cream, inhaler or injection."), ("ফর্ম মানে ওষুধের রূপ", "ট্যাবলেট, ক্যাপসুল, তরল, ক্রিম, ইনহেলার বা ইনজেকশন।")),
      (("Route is how it is used", "Form and route are related, not the same."), ("রুট মানে কীভাবে প্রয়োগ", "ফর্ম আর রুট সম্পর্কিত, কিন্তু এক নয়।")),
      (("Do not crush by habit", "Some tablets and capsules must stay whole."), ("অভ্যাসে গুঁড়ো করবেন না", "কিছু ট্যাবলেট ও ক্যাপসুল আস্ত রাখতে হয়।")),
      (("Measure liquids properly", "Use the supplied device, not a kitchen spoon."), ("তরল ঠিকভাবে মাপুন", "সাথে দেওয়া মাপনি, রান্নাঘরের চামচ নয়।")),
      (("Ask the pharmacist", "Before you split, crush, open or switch a form."), ("ফার্মাসিস্টকে জিজ্ঞেস করুন", "ভাঙা, গুঁড়ো, খোলা বা ফর্ম বদলের আগে।"))], CORAL, GOLD, bn)

CFG = {
 "cover": dict(kind="photo", bg="df-cover", a=22, pw=560, byline=True, foot=False, ts=(76, 80),
   kick=("Pharma Blog · Dosage forms", "ফার্মা ব্লগ · ডোজেজ ফর্ম"),
   title=("Why medicines come in <i>different forms</i>", "ওষুধ কেন <i>ভিন্ন ভিন্ন রূপে</i> আসে"),
   sub=("Tablets, capsules, liquids, creams, inhalers and injections, simply explained.", "ট্যাবলেট, ক্যাপসুল, তরল, ক্রিম, ইনহেলার ও ইনজেকশন, সহজ ভাষায়।")),
 "tree": dict(svg=tree, pw=470, cx=600, ts=(58, 60), kick=("The family of forms", "ফর্মের পরিবার"),
   title=("Four main <i>groups</i>", "চারটি প্রধান <i>দল</i>"),
   sub=("Each form is designed for a route, a site and a release pattern.", "প্রতিটি ফর্ম একটি রুট, স্থান ও নিঃসরণ-ধরনের জন্য তৈরি।"), src=SRC),
 "liquids": dict(svg=liquids, pw=470, cx=600, ts=(58, 60), kick=("Liquid medicines", "তরল ওষুধ"),
   title=("Solution or <i>suspension</i>?", "সলিউশন নাকি <i>সাসপেনশন</i>?"),
   sub=("Read the label: some bottles need shaking, all need careful measuring.", "লেবেল পড়ুন: কিছু বোতল ঝাঁকাতে হয়, সবই সাবধানে মাপতে হয়।"), src=SRC),
 "takeaways": dict(svg=takeaways, pw=460, cx=590, ts=(60, 62), kick=("Key takeaways", "মূল কথা"),
   title=("Dosage forms in <i>5 points</i>", "৫ কথায় <i>ডোজেজ ফর্ম</i>"), src=SRC),
}
NAMES = {"cover": "medicine-dosage-forms-cover", "tree": "types-of-dosage-forms-tablet-capsule-liquid-injection",
         "liquids": "solution-vs-suspension-liquid-medicine", "takeaways": "dosage-forms-key-takeaways"}
