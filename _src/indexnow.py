#!/usr/bin/env python3
"""Submit all sitemap URLs (or URLs given as args) to IndexNow (Bing, Yandex, Naver, Seznam...). Run after each deploy:
   python3 _src/indexnow.py            # all sitemap URLs
   python3 _src/indexnow.py https://sayedulabrar.site/blog/xyz/"""
import re, sys, json, pathlib, urllib.request
R = pathlib.Path(__file__).resolve().parent.parent
KEY = "a7f3c9e1b25d4086a1c7e3f95b2d8046"; HOST = "sayedulabrar.site"
urls = sys.argv[1:] or re.findall(r"<loc>([^<]+)</loc>", (R/"sitemap.xml").read_text(encoding="utf-8"))
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", body, {"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow", r.status, len(urls), "URLs")
except Exception as e: print("IndexNow failed:", e)
