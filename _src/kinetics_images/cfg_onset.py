"""Onset, Peak and Duration article graphics. Recipe: Deep Teal headline, keyword in Charcoal on an Amber Coral highlighter,
Steel Blue kicker with a teal line, Charcoal round badges, teal legend edge, Deep Teal byline pill with a coral edge."""
import math
from kchart import *
OUT = "assets/img/blog/onset-peak-duration"
PREFIX = "onset-peak-duration"
RECIPE = f""".title{{color:{TEAL}}} .title i{{color:{CHAR};background:linear-gradient(transparent 18%,rgba(233,130,80,.55) 18%,rgba(233,130,80,.55) 92%,transparent 92%);padding:0 .08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.kick{{color:{STEEL}}} .kick:before{{background:{TEAL}}} .badge{{background:{CHAR};color:#fff;border-radius:50%}} .li{{--lc:{TEAL}}}
.byline{{background:{TEAL};border-left:6px solid {CORAL}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SRC = ("StatPearls; MSD Manual; Open RN Pharmacology", "StatPearls; MSD Manual; Open RN Pharmacology")
SOCIAL = dict(ts=(70, 72), pw=520, a=34)
x0, y0, x1, y1 = 120, 100, 860, 570
X = lambda t: x0 + 10 + t * 60
Y = lambda c: y1 - c * 430

def window(s, mec, mtc, bn, labels=True):
    s += pill(x0 + 4, Y(mtc), x1 - x0 - 10, Y(mec) - Y(mtc), SAGE, r=0, op=.75)
    s += line(x0 + 4, Y(mtc), x1 - 10, Y(mtc), CORAL, 3, "10 8") + line(x0 + 4, Y(mec), x1 - 10, Y(mec), TEAL, 3, "10 8")
    if labels:
        s += T(x1 - 14, Y(mtc) - 12, "বিষাক্ত মাত্রার সীমা" if bn else "Toxic level", 24 if not bn else 26, "end", "b", CORAL)
        s += T(x1 - 14, Y(mec) - 14, "কার্যকর হওয়ার ন্যূনতম মাত্রা" if bn else "Minimum effective level", 24 if not bn else 26, "end", "b", TEAL)
    return s

def curve(bn):
    mec, mtc = 0.22, 0.86
    f = lambda t: 1.05 * bateman(t, 1.4, 0.3)
    pts = [(X(t / 10), Y(f(t / 10))) for t in range(0, 121)]
    s = axes(x0, y0, x1, y1, "সময়" if bn else "Time", "রক্তে ওষুধের মাত্রা" if bn else "Drug level in blood", bn)
    s = window(s, mec, mtc, bn)
    s += T(X(9.6), (Y(mtc) + Y(mec)) / 2 + 8, "থেরাপিউটিক উইন্ডো" if bn else "Therapeutic window", 25 if not bn else 27, "middle", "b", STEEL)
    s += poly(pts, TEAL, 6)
    ts = [t / 100 for t in range(0, 1200)]
    on = next(t for t in ts if f(t) >= mec); off = next(t for t in ts if t > 3 and f(t) <= mec)
    pk = max(ts, key=f)
    for t, c, lab in ((on, CORAL, "১ শুরু" if bn else "1 Onset"), (pk, CHAR, "২ সর্বোচ্চ" if bn else "2 Peak")):
        s += f'<circle cx="{X(t):.0f}" cy="{Y(f(t)):.0f}" r="12" fill="{c}" stroke="#fff" stroke-width="4"/>'
    s += pill(X(on) + 34, Y(mec) - 92, 130, 42, CORAL, r=10) + T(X(on) + 99, Y(mec) - 63, "১ শুরু" if bn else "1 Onset", 23 if not bn else 25, "middle", "b", "#fff")
    s += pill(X(pk) - 66, Y(f(pk)) - 64, 132, 42, CHAR, r=10) + T(X(pk), Y(f(pk)) - 35, "২ সর্বোচ্চ" if bn else "2 Peak", 23 if not bn else 25, "middle", "b", "#fff")
    s += f'<circle cx="{X(off):.0f}" cy="{Y(mec):.0f}" r="12" fill="{TEAL}" stroke="#fff" stroke-width="4"/>'
    yb = y1 - 26
    s += line(X(on), yb, X(off), yb, GOLD, 6) + line(X(on), yb - 14, X(on), yb + 14, GOLD, 5) + line(X(off), yb - 14, X(off), yb + 14, GOLD, 5)
    s += pill((X(on) + X(off)) / 2 - 110, yb - 58, 220, 40, GOLD, r=10)
    s += T((X(on) + X(off)) / 2, yb - 30, "৩ কাজের স্থায়িত্ব" if bn else "3 Duration", 23 if not bn else 25, "middle", "b", CHAR)
    s += T(454, 724, "প্রতীকী চিত্র; প্রতিটি ওষুধের কার্ভ আলাদা" if bn else "Illustrative; every medicine has its own curve", 22 if not bn else 24, "middle", "s", STEEL)
    return s

def routes(bn):
    s = axes(x0, y0, x1, y1, "সময়" if bn else "Time", "রক্তে ওষুধের মাত্রা" if bn else "Drug level in blood", bn)
    iv = [(X(t / 10), Y(0.9 * math.exp(-0.45 * t / 10))) for t in range(0, 121)]
    ir = [(X(t / 10), Y(0.8 * bateman(t / 10, 1.3, 0.38))) for t in range(0, 121)]
    er = [(X(t / 10), Y(0.42 * bateman(t / 10, 0.45, 0.12))) for t in range(0, 121)]
    s += poly(iv, TEAL, 6) + poly(ir, CORAL, 6) + poly(er, GOLD, 6)
    s += pill(470, 120, 400, 160, "#fff", r=16, stroke="#e3e7e8", sw=2)
    for k, (c, t) in enumerate(((TEAL, "IV ইনজেকশন: সবচেয়ে দ্রুত" if bn else "IV injection: fastest"),
                                 (CORAL, "সাধারণ ট্যাবলেট" if bn else "Ordinary tablet"),
                                 (GOLD, "ধীরে-নিঃসৃত (SR/ER) ট্যাবলেট" if bn else "Slow-release (SR/ER) tablet"))):
        y = 162 + k * 44
        s += line(492, y - 8, 532, y - 8, c, 8) + T(548, y, t, 24 if not bn else 26, "start", "b", CHAR)
    s += T(454, 724, "প্রতীকী চিত্র; পথ ও রূপ বদলালে শুরু ও স্থায়িত্ব বদলায়" if bn else "Illustrative: route and form change the onset and duration", 22 if not bn else 24, "middle", "s", STEEL)
    return s

def double(bn):
    mec, mtc = 0.22, 0.86
    g = lambda t: 0.62 * bateman(t, 1.4, 0.3)
    one = [(X(t / 10), Y(g(t / 10))) for t in range(0, 121)]
    e = lambda t: g(t - 1.2) if t > 1.2 else 0
    k = (0.97 - 0) / max(g(t / 100) + e(t / 100) for t in range(0, 1200))
    two = [(X(t / 10), Y(g(t / 10) + (k * (g(t / 10) + e(t / 10)) - g(t / 10)))) for t in range(0, 121)]
    s = axes(x0, y0, x1, y1, "সময়" if bn else "Time", "রক্তে ওষুধের মাত্রা" if bn else "Drug level in blood", bn)
    s = window(s, mec, mtc, bn)
    s += poly(two, CORAL, 6, dash="14 10") + poly(one, TEAL, 6)
    pk = max(two, key=lambda p: -p[1])
    px, py = X(3.4), 92
    s += pill(px, py, 360, 76, "#fff", r=12, stroke=CORAL, sw=3)
    s += T(px + 16, py + 32, "আগেভাগে দ্বিগুণ ডোজ" if bn else "Extra doses taken early", 23 if not bn else 25, "start", "b", CORAL)
    s += T(px + 16, py + 64, "মাত্রা বেশি উঠে যেতে পারে" if bn else "can push the level too high", 22 if not bn else 24, "start", "s", CHAR)
    s += T(X(2.0), Y(0.44), "নির্দেশিত ডোজ" if bn else "Dose as directed", 24 if not bn else 26, "start", "b", TEAL)
    s += T(454, 724, "প্রতীকী চিত্র; ধীরে কাজ করলে ডোজ না বাড়িয়ে ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন" if bn else "Illustrative. If it feels slow, ask a doctor or pharmacist; do not add doses", 21 if not bn else 23, "middle", "s", STEEL)
    return s

CFG = {
 "cover": dict(kind="photo", bg="onset", a=28, pw=560, byline=True, foot=False, ts=(86, 90),
   kick=("Onset, peak and duration", "শুরু, সর্বোচ্চ ও স্থায়িত্ব"),
   title=("When a medicine <i>starts</i> and stops", "ওষুধ কখন <i>কাজ</i> শুরু করে, কখন থামে"),
   sub=("Reading the time curve of drug action in simple words.", "ওষুধের কাজের সময়-রেখা সহজ ভাষায়।")),
 "curve": dict(svg=curve, pw=500, ts=(60, 60),
   kick=("The time curve", "সময়-রেখা"),
   title=("Onset, peak, <i>duration</i>", "শুরু, সর্বোচ্চ, <i>স্থায়িত্ব</i>"),
   sub=("The medicine works while its level stays between the two lines.", "দুই রেখার মাঝে মাত্রা থাকলে ওষুধ কাজ করে।"),
   src=SRC),
 "routes": dict(svg=routes, pw=500, ts=(60, 60),
   kick=("Route and form", "পথ ও রূপ"),
   title=("Fast, <i>steady</i> or slow", "দ্রুত, <i>স্থির</i> না ধীর"),
   sub=("An injection, a tablet and a slow-release tablet give different curves.", "ইনজেকশন, ট্যাবলেট ও ধীরে-নিঃসৃত ট্যাবলেটের কার্ভ ভিন্ন।"),
   src=("MSD Manual; StatPearls", "MSD Manual; StatPearls")),
 "double": dict(svg=double, pw=500, ts=(60, 60),
   kick=("A safety point", "নিরাপত্তার কথা"),
   title=("Slow is not a reason to <i>double</i>", "ধীর মানে <i>দ্বিগুণ</i> ডোজ নয়"),
   sub=("Doses taken too close together raise the risk of side effects.", "খুব কাছাকাছি ডোজ নিলে পার্শ্বপ্রতিক্রিয়ার ঝুঁকি বাড়ে।"),
   src=("NHS Specialist Pharmacy Service; Open RN", "NHS Specialist Pharmacy Service; Open RN")),
 "takeaways": dict(kind="photo", bg="onset", a=40, pw=640, ts=(64, 64),
   kick=("Key takeaways", "মূল কথা"), title=("Drug timing in <i>5 points</i>", "৫ কথায় <i>ওষুধের সময়</i>"),
   legend=[(("Onset", "When the effect first starts."), ("শুরু", "যখন প্রথম কাজ শুরু হয়।")),
           (("Peak", "When the level is highest."), ("সর্বোচ্চ", "যখন মাত্রা সবচেয়ে বেশি।")),
           (("Duration", "How long the effect lasts."), ("স্থায়িত্ব", "কাজ কতক্ষণ থাকে।")),
           (("Route and form", "Change how fast and how long."), ("পথ ও রূপ", "কত দ্রুত ও কতক্ষণ, তা বদলায়।")),
           (("Do not double", "Ask before adding a dose."), ("দ্বিগুণ নয়", "ডোজ বাড়ানোর আগে জিজ্ঞেস করুন।"))],
   src=SRC),
}
NAMES = {"cover": "onset-peak-duration-cover", "curve": "onset-peak-duration-therapeutic-window-curve",
         "routes": "onset-iv-tablet-slow-release-comparison", "double": "why-not-double-a-dose-curve",
         "takeaways": "onset-peak-duration-key-takeaways"}
