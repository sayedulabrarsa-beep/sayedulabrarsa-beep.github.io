# How this site is built

`_src/build.py` writes every page, `sitemap.xml`, `sitemap.xsl`, `robots.txt` and `404.html`.
Run it from the repository root: `python3 _src/build.py`
Folders that start with an underscore are not published by GitHub Pages.

Styles: `assets/style.css`. Scripts: `assets/site.js`. Images: `assets/img/`.

## Adding a blog post or vlog post

Create one JSON file per post:
- Blog: `_src/content/blog/<slug>.json`, images in `assets/img/blog/`
- Vlog: `_src/content/vlog/<slug>.json`, images in `assets/img/vlog/`

```json
{
  "slug": "my-first-post",
  "title": "Post title",
  "date": "2026-10-27",
  "summary": "One or two sentences shown on the list page and in search results.",
  "cover": "/assets/img/blog/my-first-post.jpg",
  "cover_alt": "Describe the picture",
  "tags": ["Pharmacy", "Medicine"],
  "youtube": "optional YouTube video id (vlog)",
  "body": [
    {"type": "p", "text": "A paragraph."},
    {"type": "h2", "text": "A heading"},
    {"type": "img", "src": "/assets/img/blog/figure-1.jpg", "alt": "What the picture shows", "caption": "Optional caption"},
    {"type": "ul", "items": ["Point one", "Point two"]},
    {"type": "quote", "text": "A highlighted line"}
  ]
}
```

The Blog and Daily Vlog list pages stay hidden from search engines until the first post exists.
