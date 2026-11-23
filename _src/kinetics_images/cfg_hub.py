"""Series hub page graphics: How Medicines Work in the Body. Recipe: Charcoal headline, keyword in Deep Teal on a Soft Sage tag,
Muted Gold kicker line, numbered Deep Teal steps, coral byline edge."""
from kchart import *
OUT = "assets/img/blog/how-medicines-work-series"
PREFIX = "how-medicines-work-series"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:{TEAL};background:{SAGE};padding:0 .14em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:{STEEL}}} .kick:before{{background:{GOLD}}} .badge{{background:{TEAL};color:#fff;border-radius:10px}} .li{{--lc:{GOLD}}}
.byline{{background:{CHAR};border-left:6px solid {CORAL}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SOCIAL = dict(ts=(66, 70), pw=540, a=36)
STEPS = [("Absorption", "শোষণ", "Into the blood", "রক্তে প্রবেশ"), ("Distribution", "বণ্টন", "Around the body", "শরীরজুড়ে ছড়ানো"),
         ("Metabolism", "বিপাক", "Changed, mainly in the liver", "মূলত যকৃতে পরিবর্তন"), ("Excretion", "নিঃসরণ", "Removed, mainly by kidneys", "মূলত কিডনি দিয়ে বের হওয়া"),
         ("Half-life", "হাফ-লাইফ", "How long it stays", "কতক্ষণ থাকে"), ("Bioavailability", "বায়োঅ্যাভেইলেবিলিটি", "How much arrives", "কতটুকু পৌঁছায়"),
         ("Onset, peak, duration", "শুরু, সর্বোচ্চ, স্থায়িত্ব", "When it works", "কখন কাজ করে")]

def road(bn):
    s = ""
    for i, (en, b, d_en, d_bn) in enumerate(STEPS):
        y = 30 + i * 98; c = TEAL if i < 4 else CORAL
        s += pill(30, y, 888, 84, "#F7F9F8" if i < 4 else "#FDF6F0", r=16, stroke=c, sw=3)
        s += f'<circle cx="80" cy="{y+42}" r="28" fill="{c}"/>' + T(80, y + 53, num(i + 1, bn), 28, "middle", "b", "#fff")
        s += T(130, y + 53, b if bn else en, 28 if not bn else 30, "start", "b", CHAR)
        s += T(890, y + 53, d_bn if bn else d_en, 24 if not bn else 26, "end", "s", STEEL)
    s += line(30, 30 + 4 * 98 - 7, 918, 30 + 4 * 98 - 7, GOLD, 3, "4 8")
    return s

CFG = {
 "cover": dict(kind="photo", bg="hub", a=30, pw=600, byline=True, foot=False, ts=(84, 88),
   kick=("Series · 7 articles", "সিরিজ · ৭টি লেখা"),
   title=("How medicines work in <i>the body</i>", "শরীরে ওষুধ কীভাবে <i>কাজ করে</i>"),
   sub=("From swallowing a tablet to the medicine leaving the body, step by step.", "ট্যাবলেট খাওয়া থেকে শরীর থেকে বেরিয়ে যাওয়া পর্যন্ত, ধাপে ধাপে।")),
 "road": dict(svg=road, pw=470, ts=(58, 60), cx=600,
   kick=("Read in this order", "এই ক্রমে পড়ুন"),
   title=("The <i>7-step</i> series", "<i>৭ ধাপের</i> সিরিজ"),
   sub=("Four steps of the journey (ADME), then three ideas about timing and amount.", "যাত্রার চার ধাপ (ADME), তারপর সময় ও পরিমাণের তিনটি ধারণা।"),
   src=("Sayedul Abrar, Pharma Blog", "সাইয়্যেদুল আবরার, ফার্মা ব্লগ")),
}
NAMES = {"cover": "how-medicines-work-series-cover", "road": "how-medicines-work-series-roadmap"}
