"""Release systems (2 Dec) graphics. Recipe: Charcoal headline, keyword with a Muted Gold underline, Deep Teal kicker with a coral line,
Steel Blue square badges, white byline on charcoal with a gold edge. Cover sits on a teal photo, so the panel text stays on the light left side."""
from kchart import *
from nw_common import fo, checklist
import math
OUT = "assets/img/blog/release-systems"
PREFIX = "release-systems"
RECIPE = f""".title{{color:{CHAR}}} .title i{{color:{CHAR};text-decoration:underline;text-decoration-color:{GOLD};text-decoration-thickness:.12em;text-underline-offset:.08em}}
.kick{{color:{TEAL}}} .kick:before{{background:{CORAL}}} .badge{{background:{STEEL};color:#fff;border-radius:10px}} .li{{--lc:{TEAL}}}
.byline{{background:{CHAR};border-left:6px solid {GOLD}}} body.bn .byline{{font-family:HS;font-weight:700}}"""
SRC = ("EMA modified-release guideline; FDA; NHS SPS", "EMA মডিফায়েড-রিলিজ গাইডলাইন; FDA; NHS SPS")
SOCIAL = dict(ts=(60, 64), pw=520, a=26)

def curves(bn):
    x0, y0, x1, y1 = 90, 60, 860, 560
    s = axes(x0, y0, x1, y1, "সময় (প্রতীকী)" if bn else "Time (illustrative)", "রক্তে মাত্রা" if bn else "Drug level in blood", bn)
    def path(f, c, dash=None):
        pts = [(x0 + t / 24 * (x1 - x0 - 20), y1 - f(t) * (y1 - y0 - 40)) for t in [i * 0.1 for i in range(241)]]
        return poly(pts, c, 6, dash=dash)
    ir = lambda t: 0.95 * bateman(t, 1.6, 0.35) / 0.70
    sr = lambda t: 0.50 * (1 - math.exp(-0.45 * t)) * math.exp(-0.06 * max(0, t - 6))
    ec = lambda t: 0 if t < 3 else 0.80 * bateman(t - 3, 1.6, 0.35) / 0.70
    s += path(ir, CORAL) + path(sr, TEAL) + path(ec, GOLD, "14 8")
    leg = [(CORAL, None, "Immediate-release (IR)", "ইমিডিয়েট-রিলিজ (IR)", "No special delay or slowing", "বিশেষ বিলম্ব বা ধীরগতি নেই"),
           (TEAL, None, "Sustained / extended (SR, ER)", "সাসটেইনড / এক্সটেন্ডেড (SR, ER)", "Released slowly over a longer time", "দীর্ঘ সময় ধরে ধীরে নিঃসরণ"),
           (GOLD, "14 8", "Delayed / enteric-coated (EC)", "ডিলেইড / এন্টেরিক-কোটেড (EC)", "Starts later, after the stomach", "দেরিতে শুরু, পাকস্থলী পেরিয়ে")]
    for i, (c, d, a, ab, b, bb) in enumerate(leg):
        y = 630 + i * 0  # placeholder
    s += pill(380, 70, 470, 220, "#fff", r=14, stroke="#d6e2df", sw=2)
    for i, (c, d, a, ab, b, bb) in enumerate(leg):
        y = 112 + i * 64
        s += line(400, y - 8, 448, y - 8, c, 6, d)
        s += T(462, y - 2, ab if bn else a, 22 if not bn else 24, "start", "b", CHAR)
        s += T(462, y + 24, bb if bn else b, 19 if not bn else 21, "start", "", STEEL)
    s += T(x1, y1 + 40, "শুধু ধারণা দিতে আঁকা; প্রকৃত রেখা ওষুধ অনুযায়ী আলাদা" if bn else "Shapes are illustrative; real curves differ by product", 19 if not bn else 21, "end", "", STEEL)
    return s

def coating(bn):
    s = ""
    # stomach
    s += f'<path d="M80,170 q-40,170 80,250 q160,90 260,-40 q60,-90 20,-190 q-40,-90 -170,-70 q-110,10 -190,50 Z" fill="#F7DCCB" stroke="{CORAL}" stroke-width="4"/>'
    s += T(250, 112, "পাকস্থলী (অ্যাসিডিক)" if bn else "Stomach (acidic)", 26 if not bn else 28, "middle", "b", CORAL)
    s += f'<ellipse cx="250" cy="300" rx="62" ry="36" fill="{GOLD}" stroke="{CHAR}" stroke-width="3"/><ellipse cx="250" cy="300" rx="44" ry="22" fill="#fff"/>'
    s += fo(120, 360, 260, 80, ("আবরণ অক্ষত থাকে" if bn else "Coating stays intact"), bn, (22, 24), 700, CHAR, "center")
    # arrow
    s += line(430, 300, 520, 300, CHAR, 5) + f'<path d="M520,288 L544,300 L520,312 Z" fill="{CHAR}"/>'
    # intestine
    s += f'<path d="M560,190 h300 q30,0 30,30 v20 q0,30 -30,30 h-260 q-30,0 -30,30 v20 q0,30 30,30 h260 q30,0 30,30 v20 q0,30 -30,30 h-300" fill="none" stroke="#C9E2DC" stroke-width="56" stroke-linecap="round"/>'
    s += T(725, 112, "অন্ত্র (কম অ্যাসিডিক)" if bn else "Intestine (less acidic)", 26 if not bn else 28, "middle", "b", TEAL)
    s += f'<ellipse cx="740" cy="300" rx="44" ry="22" fill="#fff" stroke="{TEAL}" stroke-width="3" stroke-dasharray="8 6"/>'
    for k in range(10):
        a = k / 10 * 6.28
        s += f'<circle cx="{740+70*math.cos(a):.0f}" cy="{300+34*math.sin(a):.0f}" r="7" fill="{TEAL}"/>'
    s += fo(600, 400, 280, 70, ("আবরণ গলে, ওষুধ বের হয়" if bn else "Coating dissolves, drug is released"), bn, (22, 24), 700, CHAR, "center")
    s += pill(30, 520, 848, 196, SAGE, r=18)
    s += fo(56, 530, 800, 176, ("<b style='color:#174F52'>গুঁড়ো বা চিবালে কী হয়?</b><span style='margin-top:6px'>আবরণ নষ্ট হতে পারে: ওষুধ পাকস্থলীর অ্যাসিডে পড়ে বা ভুল জায়গায় বের হতে পারে। প্যাকের নির্দেশনা না বললে আস্ত গিলুন।</span>" if bn else
                                "<b style='color:#174F52'>What if it is crushed or chewed?</b><span style='margin-top:6px'>The coating can be damaged, so the drug may meet stomach acid or be released in the wrong place. Swallow whole unless the product leaflet says otherwise.</span>"), bn, (23, 25), 500)
    return s

def takeaways(bn):
    return checklist([
      (("IR is not instant", "It has no special delay, but still needs time to absorb."), ("IR মানেই তাৎক্ষণিক নয়", "বিশেষ বিলম্ব নেই, তবু শোষণে সময় লাগে।")),
      (("SR, ER release slowly", "Designed to release over a longer period."), ("SR, ER ধীরে ছাড়ে", "দীর্ঘ সময় ধরে নিঃসরণের জন্য তৈরি।")),
      (("EC delays the start", "The coating resists stomach acid."), ("EC শুরু পিছিয়ে দেয়", "আবরণ পাকস্থলীর অ্যাসিড ঠেকায়।")),
      (("Letters are only a clue", "Check the full name and the leaflet."), ("অক্ষর শুধু ইঙ্গিত", "পুরো নাম ও লিফলেট দেখুন।")),
      (("Do not crush or chew", "Unless the product leaflet says it is safe."), ("গুঁড়ো করবেন না, চিবাবেন না", "লিফলেট নিরাপদ বললে তবেই।"))], TEAL, STEEL, bn)

CFG = {
 "cover": dict(kind="photo", bg="rs-cover", a=24, pw=560, byline=True, foot=False, ts=(66, 72),
   kick=("Pharma Blog · Release systems", "ফার্মা ব্লগ · রিলিজ সিস্টেম"),
   title=("Immediate, sustained or <i>enteric-coated</i>?", "ইমিডিয়েট, সাসটেইনড নাকি <i>এন্টেরিক-কোটেড</i>?"),
   sub=("How a tablet's design decides when and how it releases medicine.", "ট্যাবলেটের নকশা কীভাবে ঠিক করে কখন ও কীভাবে ওষুধ বের হবে।")),
 "curves": dict(svg=curves, pw=470, cx=600, ts=(56, 58), kick=("Three release patterns", "তিন ধরনের নিঃসরণ"),
   title=("Same drug, <i>different timing</i>", "একই ওষুধ, <i>ভিন্ন সময়</i>"),
   sub=("The release design changes the shape of the blood-level curve.", "নিঃসরণের নকশা রক্তে মাত্রার রেখার আকার বদলে দেয়।"), src=SRC),
 "coating": dict(svg=coating, pw=460, cx=590, ts=(56, 58), kick=("Enteric coating", "এন্টেরিক কোটিং"),
   title=("A coat that waits for the <i>intestine</i>", "আবরণ অপেক্ষা করে <i>অন্ত্রের</i> জন্য"),
   sub=("It resists stomach acid and dissolves at the higher pH further along.", "পাকস্থলীর অ্যাসিড ঠেকায়, সামনে বেশি pH-এ গলে যায়।"), src=SRC),
 "takeaways": dict(svg=takeaways, pw=460, cx=590, ts=(58, 60), kick=("Key takeaways", "মূল কথা"),
   title=("Release systems in <i>5 points</i>", "৫ কথায় <i>রিলিজ সিস্টেম</i>"), src=SRC),
}
NAMES = {"cover": "immediate-sustained-enteric-coated-cover", "curves": "immediate-vs-sustained-vs-delayed-release-curves",
         "coating": "enteric-coated-tablet-stomach-vs-intestine", "takeaways": "release-systems-key-takeaways"}
