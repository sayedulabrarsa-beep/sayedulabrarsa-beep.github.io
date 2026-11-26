# SayedulAbrar.site — SEO and Publishing Baseline Audit

**Audit date:** 27 November 2026  
**Repository reviewed:** `sayedulabrarsa-beep/sayedulabrarsa-beep.github.io`  
**Production branch inspected:** `main`  
**Website:** https://sayedulabrar.site  
**Scope:** Repository configuration, crawl/discovery infrastructure, publishing workflow and a sample of publicly discoverable pages. This is a baseline audit, not a complete page-by-page medical fact check or Search Console performance audit.

## Executive summary

The website already has a substantial SEO foundation: a custom domain, sitemap, robots directives, image sitemap entries, RSS feed, AI-readable discovery files, bilingual article routes, structured data generation and an IndexNow workflow. Public search results also show that the homepage and Pharma Blog are discoverable, alongside multiple article pages.

The most important issue found is a **publishing-control mismatch**: the existing GitHub Actions workflow can publish scheduled articles directly to `main` every day at 20:00 Bangladesh time and can also run on selected pushes. This conflicts with the author's stated preference: review first and approve before publishing. Do not assume an article has author approval merely because its date appears in the editorial calendar.

A second important issue is **outdated technical documentation**: `_src/README.md` describes a JSON content workflow, but the current `_src/content/blog/` directory contains only `.gitkeep`, while `_src/build.py` explicitly says it is retired and warns that running it could overwrite current site components. The maintained source of individual pages must be confirmed before any page edits or build commands.

## Baseline findings

### 1. Domain and public visibility

- The repository is public and the configured default branch is `main`.
- The repository contains a root `CNAME` file and the live custom domain responds in public search results.
- Public search results surfaced the homepage, Pharma Blog, About/profile-related content, publications and multiple English/Bangla article pages.
- This confirms discoverability in the search engine used for this spot check; it does not establish complete Google indexing, ranking performance or AI-platform citation coverage.

### 2. Crawl and discovery infrastructure

- `robots.txt` allows general crawling and explicitly lists several search and AI crawler user agents.
- `robots.txt` points to `https://sayedulabrar.site/sitemap.xml`.
- `sitemap.xml` contains **86 URL entries** in the inspected version, including **58 blog article URLs** (excluding the blog landing page and feed).
- The repository includes image sitemap annotations and descriptive image titles for some images.
- The repository includes `llms.txt`, `llms-full.txt` and an RSS feed at `/blog/feed.xml`.
- `_src/seo_feeds.py` documents a generator for the RSS feed, article list in `llms.txt`, and Blog JSON-LD.

These are useful discovery mechanisms, but they do not guarantee crawling, indexing, ranking or citation by an AI system.

### 3. Content footprint

- The `blog/` directory contains **76 article route folders**, representing **38 apparent English/Bangla route pairs**. The inspected sitemap lists **58 blog article URLs** (about 29 pairs), so 18 route folders are not represented in the sitemap; this may be intentional for future, hidden or noindex pages, but it should be reconciled against each page's robots/canonical status.
- The site also has separate brand pages for Finix, Finix MUPS, Finix HP and Malifa.
- Publicly discoverable examples include medicine safety, pharmacology, GMP, pharmaceutical product management, pharmaceutical marketing and research-review topics.
- The public blog landing page presents bilingual educational content and a clear general-information disclaimer.

A complete article inventory should next reconcile all 76 route folders against the 58 sitemap article URLs, then verify each route's canonical URL, language alternate, indexability, metadata, structured data, internal links, image alt text and source references.

### 4. Publishing workflow — priority risk

The current `.github/workflows/scheduled-articles.yml`:

- Runs on a daily cron corresponding to **20:00 Asia/Dhaka**.
- Also runs on pushes affecting the editorial calendar, blog pages or the workflow itself.
- Has `contents: write` permission.
- Runs the scheduled-release script and supporting generators.
- Commits generated changes and pushes them to `main`.

This is an automatic publishing path. It does not implement a per-article author review/approval gate. **Recommended action:** replace automatic scheduled release with a manual, explicitly authorised release process, or introduce a genuine approval gate. This change should be reviewed with the author because it affects the existing editorial calendar and publishing operations.

The separate IndexNow workflow is triggered after selected public HTML or sitemap changes on `main`; it is a notification workflow, not an approval mechanism.

### 5. Source-of-truth and build documentation — priority risk

- `_src/content/blog/` currently contains only `.gitkeep` in the inspected `main` branch.
- `_src/build.py` explicitly labels itself retired and exits unless an override is supplied; its own warning says running it could overwrite the current homepage, menu and blog pages.
- `_src/README.md` still describes adding blog posts as JSON files under `_src/content/blog/` and running the site build instructions.

**Recommended action:** document the actual current page-authoring workflow after inspecting repository history and the scripts responsible for each page family. Do not run the retired generator or assume the HTML page is safe to edit directly until its maintained source is established.

### 6. SEO implementation strengths observed

- Custom-domain canonical URLs are used in sitemap and SEO scripts.
- Robots directives include a sitemap reference and explicit crawler rules.
- A sitemap and image sitemap entries are present.
- RSS and AI-readable discovery files are part of the repository.
- The repository includes SEO-related scripts for metadata, profile structured data, entity links, feeds, bylines, image dimensions and sitemap image data.
- Public search snippets show clear article titles, summaries, author attribution, answer-first sections and sources on sampled pages.
- English and Bangla content routes are present.

### 7. Measurement limitations

This repository inspection did not access Google Search Console, Bing Webmaster Tools, analytics, crawl logs or private webmaster account data. Therefore this report does **not** claim to verify:
- impressions, clicks, CTR, average position or keyword rankings;
- submitted versus indexed URL counts or excluded-page reasons;
- Core Web Vitals or real-user performance;
- backlink profile or competitor gaps;
- actual crawl frequency or AI crawler visits.

Those require connected account data or fresh, page-level technical testing.

## Prioritised action plan

| Priority | Action | Approval needed |
|---|---|---|
| P0 | Resolve the automatic scheduled-publishing workflow so no article goes live without author approval | Yes — changes publishing behaviour |
| P0 | Confirm the real source-of-truth for articles and document the safe authoring/build process | Yes before changing build or publishing code |
| P1 | Crawl all 86 sitemap URLs for status, canonical, robots, title, description, H1, structured data, language alternates and broken internal links | No site change; report only |
| P1 | Audit all 38 apparent bilingual article pairs for parity, hreflang/alternate implementation and canonical consistency | No site change; report only |
| P1 | Validate medical/scientific references and high-risk claims article by article | Author/editor review required |
| P2 | Review author/profile schema, organization/person relationships, social profiles and professional claims | Approve any public content changes |
| P2 | Review internal-link architecture across the eight business-profile categories | Approve any public content changes |
| P2 | Review image alt text, image sitemap quality and social previews | Approve any public content changes |
| P3 | Connect Search Console/Bing performance data and build a measured query/page opportunity backlog | Account connection required |

## Safety and change log

- This audit report is documentation only.
- No production page, article, URL, image, CSS, JavaScript, sitemap, robots file or publishing workflow was changed as part of this report.
- The business/editorial profile and reusable review template are prepared on the separate review branch.
- The draft pull request remains unmerged. Production remains on `main` until the author reviews and approves the proposed changes.

## Sources inspected

- Repository: https://github.com/sayedulabrarsa-beep/sayedulabrarsa-beep.github.io
- Robots: https://sayedulabrar.site/robots.txt
- Sitemap: https://sayedulabrar.site/sitemap.xml
- Pharma Blog: https://sayedulabrar.site/blog/
- Homepage: https://sayedulabrar.site/
- Publishing workflow: `.github/workflows/scheduled-articles.yml`
- IndexNow workflow: `.github/workflows/indexnow.yml`
- Site build notes: `_src/README.md` and `_src/build.py`
- SEO feed generator: `_src/seo_feeds.py`
- SEO metadata helper: `_src/seo_meta_tune.py`
