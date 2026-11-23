"""Drug Half-Life article graphics. Recipe: Charcoal headline, keyword in Deep Teal with an Amber Coral underline bar,
Steel Blue kicker with a gold line, gold rounded-square badges, coral legend edge, charcoal byline pill with gold edge."""
from kchart import *
OUT = "assets/img/blog/drug-half-life"
PREFIX = "drug-half-life"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:{TEAL};background:linear-gradient(transparent 82%,{CORAL} 82%,{CORAL} 96%,transparent 96%)}}
.kick{{color:{STEEL}}} .kick:before{{background:{GOLD}}} .badge{{background:{GOLD};color:{CHAR};border-radius:12px}} .li{{--lc:{CORAL}}}
.byline{{background:{CHAR};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}
.lab{{position:absolute;transform:translateX(-50%);white-space:nowrap;font-family:Pop,HS,sans-serif;font-weight:800;line-height:1.1;text-align:center}} body.bn .lab{{font-family:HS;font-weight:700}}
.lab small{{display:block;font-family:Int,HS,sans-serif;font-weight:600;font-size:.62em;margin-top:3px;color:{STEEL}}} body.bn .lab small{{font-family:HS;font-weight:700;font-size:.7em}}
.pw{{background:#fff;color:{CHAR};padding:9px 20px;border-radius:999px;border:3px solid {GOLD};box-shadow:0 8px 20px rgba(37,50,56,.2)}}
.pt{{background:{TEAL};color:#fff;padding:9px 20px;border-radius:999px;box-shadow:0 8px 20px rgba(37,50,56,.25)}}
.ps{{background:{SAGE};color:{TEAL};padding:11px 26px;border-radius:999px;border:3px solid #fff;box-shadow:0 8px 20px rgba(37,50,56,.2)}}
.hf{{width:70px;height:70px;padding:0;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:40px;line-height:1;transform:translate(-50%,0)}}"""
SRC = ("StatPearls; MSD Manual", "StatPearls; MSD Manual")
SOCIAL = dict(ts=(70, 74), pw=520, a=30)

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


def L(x, y, txt, cls="pw", fs=30, extra=""):
    return f'<div class="lab {cls}" style="left:{x}px;top:{y}px;font-size:{fs}px;{extra}">{txt}</div>'
def Ls(items, **k): return "".join(L(*i, **k) for i in items)
TOP = "top:48px;bottom:auto;justify-content:flex-start;"

CFG = {
 "cover": dict(kind="photo", bg="hl-cover", a=24, pw=560, byline=True, foot=False, ts=(92, 96),
   kick=("Drug half-life", "ওষুধের হাফ-লাইফ"),
   title=("How long a medicine <i>stays</i>", "ওষুধ শরীরে কতক্ষণ <i>থাকে</i>"),
   sub=("Half-life in simple words: halving, dosing and steady state.", "সহজ ভাষায় হাফ-লাইফ: অর্ধেক হওয়া, ডোজ ও স্থির অবস্থা।")),
 "meaning": dict(kind="photo", bg="hl-meaning", a=8, pw=420, ts=(52, 52), panelcss=TOP, src=SRC,
   kick=("What it means", "অর্থ"),
   title=("Half-life is the time to <i>halve</i>", "হাফ-লাইফ মানে <i>অর্ধেক</i> হওয়ার সময়"),
   sub=("The blood level falls by half in each half-life.", "প্রতি হাফ-লাইফে রক্তে ওষুধ অর্ধেক হয়।"),
   extra=tuple(Ls([(x, 700, t, "pw", 32, "") for x, t in zip((686, 903, 1103, 1294, 1483), v)]) + "".join(
       f'<div class="lab" style="left:{x}px;top:762px;font-size:23px;font-family:Int,HS;font-weight:600;color:{STEEL}">{c}</div>' for x, c in zip((686, 903, 1103, 1294, 1483), cap))
       for v, cap in ((("100%", "50%", "25%", "12.5%", "6.25%"), ("start", "1 half-life", "2", "3", "4")),
                      (("১০০%", "৫০%", "২৫%", "১২.৫%", "৬.২৫%"), ("শুরু", "১ হাফ-লাইফ", "২", "৩", "৪"))))),
 "rule": dict(kind="photo", bg="hl-rule", a=8, pw=410, ts=(50, 50), panelcss=TOP, src=SRC,
   kick=("The 4–5 rule", "৪–৫ এর নিয়ম"),
   title=("Almost gone after <i>4–5</i>", "৪–৫ হাফ-লাইফে প্রায় <i>শেষ</i>"),
   sub=("About 94–97% of a single dose is eliminated.", "একটি ডোজের প্রায় ৪–৫ হাফ-লাইফে ৯৪–৯৭% বেরিয়ে যায়।".replace("প্রায় ৪–৫ হাফ-লাইফে", "প্রায়")),
   extra=tuple(Ls([(860, 205, "½", "pw hf", 40, ""), (1040, 322, "½", "pw hf", 40, ""), (1215, 412, "½", "pw hf", 40, ""), (1392, 492, "½", "pw hf", 40, "")]) +
       L(960, 772, t, "ps", 29) for t in ("After 4–5 half-lives, about 94–97% is gone", "৪–৫ হাফ-লাইফ পরে প্রায় ৯৪–৯৭% বেরিয়ে যায়"))),
 "clearance": dict(kind="photo", bg="hl-clearance", a=14, pw=520, ts=(56, 56), src=SRC,
   kick=("What decides it", "কীসের ওপর নির্ভর"),
   title=("Liver and kidneys <i>clear</i> the drug", "যকৃত ও কিডনি ওষুধ <i>সরায়</i>"),
   sub=("Faster clearance means a shorter half-life.", "দ্রুত সরালে হাফ-লাইফ ছোট হয়।"),
   extra=tuple(L(1290, 268, a, "pt", 32) + L(1170, 762, b, "pt", 28) for a, b in (("Liver", "Kidneys"), ("যকৃত", "কিডনি")))),
 "dosing": dict(kind="photo", bg="hl-dosing", a=8, pw=600, ts=(56, 56), panelcss=TOP, src=SRC,
   kick=("Dosing times", "ডোজের সময়"),
   title=("Half-life helps set <i>how often</i>", "হাফ-লাইফ ঠিক করে <i>কতবার</i>"),
   sub=("Usually, a short half-life means more doses a day.", "সাধারণত ছোট হাফ-লাইফে দিনে বেশি ডোজ লাগে।"),
   extra=tuple(Ls([(718, 335, a, "pw", 26, ""), (866, 335, b, "pw", 26, ""), (1005, 335, c, "pw", 26, "")]) for a, b, c in (("Dose 1", "Dose 2", "Dose 3"), ("ডোজ ১", "ডোজ ২", "ডোজ ৩")))),
 "steady": dict(kind="photo", bg="hl-steady", a=12, pw=520, ts=(58, 58), src=SRC,
   kick=("Steady state", "স্থির অবস্থা"),
   title=("The level stops <i>climbing</i>", "মাত্রা আর <i>বাড়ে</i> না"),
   sub=("Drug in equals drug out, after about 4–5 half-lives.", "প্রায় ৪–৫ হাফ-লাইফ পরে যত ঢোকে, তত বেরোয়।"),
   extra=tuple(L(935, 128, a, "pw", 28) + L(850, 410, b, "pt", 28) + L(1290, 520, c, "pw", 28) + L(1235, 745, d, "ps", 26) for a, b, c, d in (("Dose in", "Builds up", "Levels off", "Removed"), ("ডোজ ঢোকে", "বাড়তে থাকে", "স্থির হয়", "বেরিয়ে যায়")))),
 "factors": dict(kind="photo", bg="hl-factors", a=8, pw=420, ts=(48, 48), panelcss=TOP, src=SRC,
   kick=("What changes it", "যা বদলায়"),
   title=("Age, organs and <i>other medicines</i>", "বয়স, অঙ্গ ও <i>অন্য ওষুধ</i>"),
   sub=("Your doctor may adjust the dose. Never adjust it yourself.", "চিকিৎসক ডোজ বদলাতে পারেন। নিজে বদলাবেন না।"),
   extra=tuple(L(672, 626, a, "", 31, "color:#fff") + L(904, 626, b, "", 31, f"color:{CHAR}") + L(1153, 626, c, "", 31, f"color:{CHAR}") + L(1428, 626, d, "", 28, f"color:{CHAR}")
               for a, b, c, d in (("Age", "Kidney", "Liver", "Other drugs"), ("বয়স", "কিডনি", "যকৃত", "অন্য ওষুধ")))),
 "halving": dict(svg=halving, pw=500, ts=(64, 66),
   kick=("The meaning", "অর্থ"),
   title=("Half gone, <i>again</i> and again", "বারবার <i>অর্ধেক</i>"),
   sub=("Half-life is the time for the drug level in blood to fall by half.", "হাফ-লাইফ হলো রক্তে ওষুধের মাত্রা অর্ধেক হতে যে সময় লাগে।"),
   src=SRC),
 "steadychart": dict(svg=steady, pw=500, ts=(64, 64),
   kick=("Regular dosing", "নিয়মিত ডোজ"),
   title=("Building to a <i>steady</i> level", "<i>স্থির</i> মাত্রায় পৌঁছানো"),
   sub=("Each dose adds to what is left, until intake and removal balance.", "প্রতিটি ডোজ বাকি ওষুধের সাথে যোগ হয়, যতক্ষণ না গ্রহণ ও নিষ্কাশন সমান হয়।"),
   src=SRC),
 "takeaways": dict(kind="photo", bg="hl-takeaways", a=24, pw=640, ts=(66, 66), ill=True,
   kick=("Key takeaways", "মূল কথা"), title=("Half-life in<br><i>5 points</i>", "৫ কথায়<br><i>হাফ-লাইফ</i>"),
   legend=[(("It is a time", "Time for the level to halve."), ("এটি একটি সময়", "মাত্রা অর্ধেক হওয়ার সময়।")),
           (("4–5 half-lives", "Most of the drug is gone."), ("৪–৫ হাফ-লাইফ", "বেশিরভাগ ওষুধ বেরিয়ে যায়।")),
           (("Sets the timing", "Helps decide how often to dose."), ("সময় ঠিক করে", "কতবার ডোজ, তা বুঝতে সাহায্য করে।")),
           (("Steady state", "Reached after about 4–5 half-lives."), ("স্থির অবস্থা", "প্রায় ৪–৫ হাফ-লাইফে আসে।")),
           (("It can change", "Kidney, liver, age and other drugs."), ("এটি বদলাতে পারে", "কিডনি, যকৃত, বয়স ও অন্য ওষুধে।"))],
   extra=tuple("".join(f'<div class="lab" style="left:1100px;top:{y-52}px;font-size:34px;transform:none;left:940px;color:{TEAL}">{t}</div>' for y, t in zip((271, 364, 457, 552, 649), ts))
               for ts in (("Time", "4–5 rule", "Dosing", "Steady", "Changes"), ("সময়", "৪–৫ নিয়ম", "ডোজ", "স্থির", "বদলায়"))),
   src=SRC),
}
NAMES = {"cover": "drug-half-life-cover", "meaning": "half-life-meaning-halving-glasses", "rule": "half-life-4-5-rule-stepping-stones",
         "clearance": "half-life-clearance-liver-kidney", "dosing": "half-life-dosing-schedule-pill-organizer",
         "steady": "half-life-steady-state-water-tank", "factors": "half-life-factors-age-kidney-liver-medicines",
         "halving": "half-life-halving-curve", "steadychart": "half-life-steady-state-build-up", "takeaways": "drug-half-life-key-takeaways"}
