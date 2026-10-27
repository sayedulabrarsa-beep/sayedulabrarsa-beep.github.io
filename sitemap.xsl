<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Sitemap | Sayedul Abrar</title>
<style>
:root{--bg:#2B2D3F;--bg2:#232536;--fg:#F2F3F8;--muted:#A9ADC2;--line:#44476A;--accent:#FFA91F}
@media (prefers-color-scheme:light){:root{--bg:#F3F4F9;--bg2:#E8EAF2;--fg:#1C1E2D;--muted:#5A5F78;--line:#D3D6E4;--accent:#C26E00}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 Poppins,system-ui,sans-serif}
header{background:var(--bg2);border-bottom:1px solid var(--line);padding:14px 16px}
header a{font:700 24px "Dancing Script","Brush Script MT",cursive;color:var(--accent);text-decoration:none}
main{max-width:900px;margin:0 auto;padding:36px 16px 56px}
h1{font-size:clamp(26px,5vw,40px);line-height:1.15;margin:0 0 10px}
p{color:var(--muted);margin:0 0 26px}
.list{border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:1fr auto;gap:12px;padding:14px 0;border-bottom:1px solid var(--line);align-items:center}
.row a{color:var(--fg);text-decoration:none;overflow-wrap:anywhere;font-weight:500}
.row a:hover{color:var(--accent)}
.row time{color:var(--muted);font-size:13px;white-space:nowrap}
@media(max-width:520px){.row{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><a href="/">Sayedul Abrar</a></header>
<main>
<h1>Sitemap</h1>
<p><xsl:value-of select="count(s:urlset/s:url)"/> pages on sayedulabrar.site. Search engines read this file to find every page.</p>
<div class="list">
<xsl:for-each select="s:urlset/s:url">
<div class="row"><a href="{s:loc}"><xsl:value-of select="s:loc"/></a><time><xsl:value-of select="s:lastmod"/></time></div>
</xsl:for-each>
</div>
</main>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
