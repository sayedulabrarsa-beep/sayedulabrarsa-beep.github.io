"""Drug Half-Life article graphics. Recipe: Charcoal headline, keyword in Deep Teal with an Amber Coral underline bar,
Steel Blue kicker with a gold line, gold rounded-square badges, coral legend edge, charcoal byline pill with gold edge."""
from kchart import *
OUT = "assets/img/blog/drug-half-life"
PREFIX = "drug-half-life"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:{TEAL};background:linear-gradient(transparent 82%,{CORAL} 82%,{CORAL} 96%,transparent 96%)}}
.kick{{color:{STEEL}}} .kick:before{{background:{GOLD}}} .badge{{background:{GOLD};color:{CHAR};border-radius:12px}} .li{{--lc:{CORAL}}}
.byline{{background:{CHAR};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SRC = ("StatPearls; MSD Manual", "StatPearls; MSD Manual")
SOCIAL = dict(ts=(70, 74), pw=520, a=34)

def halving(bn):
    x0, y0, x1, y1 = 120, 120, 860, 600
    vals = [100, 50, 25, 12.5, 6.25, 3.1]
    s = axes(x0, y0, x1, y1, "সময় (হাফ-লাইফ সংখ্যা)" if bn else "Time (number of half-lives)", "শরীরে বাকি ওষুধ (%)" if bn else "Drug left in the body (%)", bn)
    bw, gap = 88, 32
    pts = []
    for i, v in enumerate(vals):
        bx = x0 + 40 + i * (bw + gap); hgt = (y1 - y0 - 30) * v / 100; by = y1 - hgt
        col = TEAL if i == 0 else (STEEL if i < 4 else CORAL)
        s += pill(bx, by, bw, hgt, col, r=10, op=.92)
        lab = ("৩.১" if bn else "3.1") if v == 3.1 else num(("%g" % v), bn)
        s += T(bx + bw / 2, by - 14, lab + "%", 28 if not bn else 30, "middle", "b", CHAR)
        s += T(bx + bw / 2, y1 + 34, ("শুরু" if bn else "Start") if i == 0 else num(i, bn), 25 if not bn else 27, "middle", "s", CHAR)
        pts.append((bx + bw / 2, by))
    s += poly(pts, GOLD, 4, dash="2 10")
    s += pill(470, 150, 400, 116, SAGE, r=16)
    s += T(492, 196, "৪–৫ হাফ-লাইফ পরে" if bn else "After 4–5 half-lives", 27 if not bn else 29, "start", "b", TEAL)
    s += T(492, 238, "প্রায় ৯৪–৯৭% বেরিয়ে যায়" if bn else "about 94–97% is gone", 26 if not bn else 28, "start", "s", CHAR)
    s += T(454, 728, "উদাহরণ: প্রতিটি হাফ-লাইফে বাকি ওষুধ অর্ধেক হয়" if bn else "Each half-life, the amount left is halved", 25 if not bn else 27, "middle", "s", STEEL)
    return s

def steady(bn):
    x0, y0, x1, y1 = 120, 110, 860, 590
    # dose every half-life; concentration units where steady-state trough = 1
    pts = []; c = 0; scale = (y1 - y0 - 60) / 2.0
    tx = lambda t: x0 + 20 + t * 118
    troughs = []
    for n in range(6):
        c += 1
        for k in range(0, 41):
            t = n + k / 40; cc = c * 0.5 ** (k / 40)
            pts.append((tx(t), y1 - cc * scale))
        c *= 0.5; troughs.append((tx(n + 1), y1 - c * scale, c))
    s = axes(x0, y0, x1, y1, "সময় (হাফ-লাইফ সংখ্যা)" if bn else "Time (number of half-lives)", "রক্তে ওষুধের মাত্রা" if bn else "Drug level in blood", bn)
    ss = y1 - 1 * scale
    s += pill(x0 + 4, y1 - 2 * scale, x1 - x0 - 10, scale, SAGE, r=0, op=.7)
    s += line(x0 + 4, ss, x1 - 10, ss, TEAL, 3, "10 8")
    s += T(x1 - 14, y1 - 2 * scale - 14, "স্থির অবস্থা (steady state)" if bn else "Steady state range", 25 if not bn else 27, "end", "b", TEAL)
    s += poly(pts, CORAL, 5)
    pct = ["50", "75", "88", "94", "97"]
    for i, (x, y, c) in enumerate(troughs[:5]):
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{TEAL}" stroke="#fff" stroke-width="3"/>'
        s += T(x, y + 44, num(pct[i], bn) + "%", 25 if not bn else 27, "middle", "b", TEAL)
    for i in range(6):
        s += T(tx(i), y1 + 34, num(i, bn), 24 if not bn else 26, "middle", "s", CHAR)
    s += T(454, 724, "নিয়মিত ডোজে প্রায় ৪–৫ হাফ-লাইফে মাত্রা স্থির হয় (প্রতীকী চিত্র)" if bn else "With regular doses, levels settle after about 4–5 half-lives (illustrative)", 23 if not bn else 25, "middle", "s", STEEL)
    return s

CFG = {
 "cover": dict(kind="photo", bg="halflife", a=30, pw=560, byline=True, foot=False, ts=(92, 96),
   kick=("Drug half-life", "ওষুধের হাফ-লাইফ"),
   title=("How long a medicine <i>stays</i>", "ওষুধ শরীরে কতক্ষণ <i>থাকে</i>"),
   sub=("Half-life in simple words: halving, dosing and steady state.", "সহজ ভাষায় হাফ-লাইফ: অর্ধেক হওয়া, ডোজ ও স্থির অবস্থা।")),
 "halving": dict(svg=halving, pw=500, ts=(64, 66),
   kick=("The meaning", "অর্থ"),
   title=("Half gone, <i>again</i> and again", "বারবার <i>অর্ধেক</i>"),
   sub=("Half-life is the time for the drug level in blood to fall by half.", "হাফ-লাইফ হলো রক্তে ওষুধের মাত্রা অর্ধেক হতে যে সময় লাগে।"),
   src=SRC),
 "steady": dict(svg=steady, pw=500, ts=(64, 64),
   kick=("Regular dosing", "নিয়মিত ডোজ"),
   title=("Building to a <i>steady</i> level", "<i>স্থির</i> মাত্রায় পৌঁছানো"),
   sub=("Each dose adds to what is left, until intake and removal balance.", "প্রতিটি ডোজ বাকি ওষুধের সাথে যোগ হয়, যতক্ষণ না গ্রহণ ও নিষ্কাশন সমান হয়।"),
   src=SRC),
 "takeaways": dict(kind="photo", bg="halflife", a=40, pw=640, ts=(66, 66), ill=True,
   kick=("Key takeaways", "মূল কথা"), title=("Half-life in <i>5 points</i>", "৫ কথায় <i>হাফ-লাইফ</i>"),
   legend=[(("It is a time", "Time for the level to halve."), ("এটি একটি সময়", "মাত্রা অর্ধেক হওয়ার সময়।")),
           (("4–5 half-lives", "Most of the drug is gone."), ("৪–৫ হাফ-লাইফ", "বেশিরভাগ ওষুধ বেরিয়ে যায়।")),
           (("Sets the timing", "Helps decide how often to dose."), ("সময় ঠিক করে", "কতবার ডোজ, তা বুঝতে সাহায্য করে।")),
           (("Steady state", "Reached after about 4–5 half-lives."), ("স্থির অবস্থা", "প্রায় ৪–৫ হাফ-লাইফে আসে।")),
           (("It can change", "Kidney, liver, age and other drugs."), ("এটি বদলাতে পারে", "কিডনি, যকৃত, বয়স ও অন্য ওষুধে।"))],
   src=SRC),
}
NAMES = {"cover": "drug-half-life-cover", "halving": "half-life-halving-curve", "steady": "half-life-steady-state-build-up",
         "takeaways": "drug-half-life-key-takeaways"}
