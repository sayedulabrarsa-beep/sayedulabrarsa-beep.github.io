"""Small SVG helpers for code-drawn pharmacology charts (card viewBox ~908 x 742)."""
import math
TEAL, CHAR, CORAL, CREAM, SAGE, GOLD, STEEL = "#174F52", "#253238", "#E98250", "#F7F1E6", "#DCEBE7", "#D8A84E", "#526D82"
BND = str.maketrans("0123456789.", "০১২৩৪৫৬৭৮৯.")

def num(s, bn):
    return str(s).translate(BND) if bn else str(s)

def T(x, y, s, size=24, anchor="start", cls="", fill=CHAR, extra=""):
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" text-anchor="{anchor}" class="{cls}" style="fill:{fill}" {extra}>{s}</text>'

def pill(x, y, w, h, fill, r=None, stroke="none", sw=0, op=1):
    r = h / 2 if r is None else r
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'

def line(x1, y1, x2, y2, c=CHAR, w=3, dash=None, op=1, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linecap="{cap}"/>'

def poly(pts, c=TEAL, w=5, fill="none", op=1, dash=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    if fill != "none":
        d += " Z"
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" opacity="{op}" stroke-linejoin="round" stroke-linecap="round"{ds}/>'

def axes(x0, y0, x1, y1, xl, yl, bn):
    s = line(x0, y1, x1, y1, CHAR, 3) + line(x0, y0, x0, y1, CHAR, 3)
    s += f'<path d="M{x1-2},{y1-8} L{x1+12},{y1} L{x1-2},{y1+8} Z" fill="{CHAR}"/><path d="M{x0-8},{y0+2} L{x0},{y0-12} L{x0+8},{y0+2} Z" fill="{CHAR}"/>'
    s += T((x0 + x1) / 2, y1 + 74, xl, 24 if not bn else 26, "middle", "s", STEEL)
    s += T(x0 - 22, (y0 + y1) / 2, yl, 24 if not bn else 26, "middle", "s", STEEL, f'transform="rotate(-90 {x0-22:.0f} {(y0+y1)/2:.0f})"')
    return s

def bateman(t, ka=1.6, ke=0.35):
    """One-compartment oral curve, arbitrary units (illustrative only)."""
    return (ka / (ka - ke)) * (math.exp(-ke * t) - math.exp(-ka * t))
