"""Shared helpers for the 30 Nov - 5 Dec drafts (Dosage Forms, Release Systems, Paracetamol, Routes)."""
from kchart import *

def fo(x, y, w, h, html, bn, size=(23, 25), weight=500, color=CHAR, align="flex-start", lh=1.22):
    fs = size[1] if bn else size[0]
    fam = "HS" if bn else "Int"
    return (f'<foreignObject x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}"><div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="height:{h:.0f}px;display:flex;flex-direction:column;justify-content:center;align-items:{align};'
            f'font:{weight} {fs}px {fam},sans-serif;line-height:{lh};color:{color}">{html}</div></foreignObject>')

def checklist(points, accent, badge, bn):
    """5 numbered rows filling the card (908 x 742 viewBox)."""
    s = ""
    n = len(points)
    hgt = (742 - 60) / n
    for i, (en, bnp) in enumerate(points):
        y = 30 + i * hgt
        a, b = bnp if bn else en
        s += pill(30, y + 6, 848, hgt - 14, "#FBFDFC", r=16, stroke="#d6e2df", sw=2)
        s += pill(30, y + 6, 10, hgt - 14, accent, r=4)
        s += f'<circle cx="94" cy="{y + 6 + (hgt - 14) / 2:.0f}" r="30" fill="{badge}"/>'
        s += T(94, y + 6 + (hgt - 14) / 2 + 10, num(i + 1, bn), 30, "middle", "b", "#fff")
        s += fo(146, y + 8, 710, hgt - 18, f'<b style="font-family:{"HS" if bn else "Pop"};font-weight:{700 if bn else 800};font-size:{30 if bn else 28}px;color:{TEAL}">{a}</b><span style="margin-top:4px">{b}</span>', bn)
    return s
