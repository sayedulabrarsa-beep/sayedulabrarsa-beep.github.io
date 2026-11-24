"""Shared label helpers for photo figures (labels drawn in code, EN + BN)."""
from kchart import TEAL, CHAR, CORAL, SAGE, GOLD, STEEL
def lab_css(accent):
    return (f""".lab{{position:absolute;transform:translateX(-50%);white-space:nowrap;font-family:Pop,HS,sans-serif;font-weight:800;line-height:1.15;text-align:center}} body.bn .lab{{font-family:HS;font-weight:700}}
.pw{{background:#fff;color:{CHAR};padding:9px 20px;border-radius:999px;border:3px solid {accent};box-shadow:0 8px 20px rgba(37,50,56,.2)}}
.pt{{background:{TEAL};color:#fff;padding:9px 20px;border-radius:999px;box-shadow:0 8px 20px rgba(37,50,56,.25)}}
.ps{{background:{SAGE};color:{TEAL};padding:11px 26px;border-radius:999px;border:3px solid #fff;box-shadow:0 8px 20px rgba(37,50,56,.2)}}
.pk{{background:transparent;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.35)}}""")
def L(x, y, txt, cls="pw", fs=28, extra=""):
    return f'<div class="lab {cls}" style="left:{x}px;top:{y}px;font-size:{fs}px;{extra}">{txt}</div>'
def EB(fn):
    """Build an (EN, BN) pair from fn(lang_index)."""
    return (fn(0), fn(1))
TOP = "top:44px;bottom:auto;justify-content:flex-start;"
