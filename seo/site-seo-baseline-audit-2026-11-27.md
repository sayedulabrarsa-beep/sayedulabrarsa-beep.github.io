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

This was an automatic publishing path with no author approval gate. A proposed fix is now included in this review branch: remove automatic cron/push triggers and require a manual workflow dispatch with an explicit author-approval checkbox before the release job can run. This proposal is not active on `main` until the pull request is approved and merged. The manual run releases all calendar items that the release script considers due, so the author should review every due item before checking the approval box.

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


## 8. Reconciliation of blog routes and sitemap

The earlier 18-route difference is now explained by the editorial calendar:

- The 76 route folders are 38 apparent English/Bangla pairs.
- The sitemap contains 58 article URLs.
- The 18 routes absent from the sitemap are exactly nine English/Bangla pairs scheduled for future publication between 28 November and 12 December 2026.
- Two sampled future pages (`onset-peak-duration-of-drug-action` and `how-to-read-a-medicine-label`) use `noindex,nofollow` while retaining their canonical URLs and future `datePublished` values.

This is consistent with the site's scheduled-release model and is not currently evidence of an accidental sitemap omission. Keep future pages out of the sitemap and search index until their approved release.

## 9. Search Console opportunity snapshot

**Property:** `sc-domain:sayedulabrar.site`  
**Country filter:** Bangladesh (`bgd`)  
**Effective data range:** 21–23 November 2026  
**Access limitation:** The connected Search Console integration currently exposes only the most recent three days, with no comparison period. Treat this as a small diagnostic sample, not a stable performance trend.

### Bangla expiry-date article

Page: https://sayedulabrar.site/blog/expiry-date-vs-manufacturing-date-medicine-bangla/

- 50 impressions, 0 clicks, 0% CTR, average position 7.9.
- Query `মেয়াদ শেষ হওয়ার তারিখ`: 47 impressions, 0 clicks, average position 8.04.
- Query `উৎপাদন তারিখ`: 2 impressions, average position 5.5.
- Query `osud er expiry date`: 1 impression, average position 6.

**Interpretation:** This is the clearest near-term opportunity. The page is already visible around positions 8–9 for a relevant Bangla query, but the short sample has not produced a click. Its current title and meta description already contain the core expiry-date wording and an informative Bangladesh-specific example. Do not rewrite the page based on only three days of data. Monitor a longer period first; if low CTR persists, test a more direct search-result title and concise description while preserving the article's factual meaning.

### Author-name query

Page: https://sayedulabrar.site/about/

- 5 impressions, 1 click, 20% CTR, average position 2.4 for `sayedul abrar`.
- Search Console also reports four pages appearing for this query: About, homepage, Learning and Achievements.

**Interpretation:** The four-page signal may reflect overlapping personal-brand relevance rather than harmful cannibalisation. The About page should remain the primary biography destination; homepage, Learning and Achievements should serve distinct supporting intents and link clearly to About. The sample is too small to justify removing pages, changing canonicals or consolidating content.

## 10. Representative on-page technical checks

A read-only sample was inspected: homepage, About, Pharma Blog index, English and Bangla expiry-date articles, Drug vs Medicine, Pharmacogenetics and Finix MUPS.

- All sampled pages had one H1 and a self-referencing canonical URL.
- All sampled pages had an index/follow robots directive, except future scheduled pages checked separately, which correctly had noindex/nofollow.
- The two sampled bilingual article pairs use reciprocal `hreflang` links for `en` and `bn`, plus `x-default`.
- The sampled homepage, About page and Pharma Blog landing page do not declare `hreflang`; these are currently English-led landing pages and should only gain alternates if genuine translated counterparts exist.
- The homepage, About and Pharma Blog descriptions were 149, 156 and 166 characters respectively. The Blog landing description is the clearest candidate for a small future trim; no change has been made.
- The five sampled pages had no images with missing or empty alt attributes.
- Sampled article pages include Article/BlogPosting structured data; the expiry-date article includes FAQPage data. The homepage includes Person, Organization, WebSite and WebPage-related data; About includes ProfilePage data.
- Some structured-data types recur across separate JSON-LD blocks. This is not automatically an error, but the complete graph should be validated for duplicate entities, conflicting values and stable `@id` relationships before changes are proposed.

This is a representative sample, not a full 86-URL crawl. A full technical crawl remains pending.

## 11. Medical-source verification — expiry-date example

The Bangla expiry-date article's core statement that a medicine expiry date shown only as month and year refers to the final day of that month is supported by the Bangladesh Directorate General of Drug Administration's *Guideline on Medical Information for Summary Product Characteristics, Patient Information Leaflet, Packaging and Labeling in Bangladesh*.

- Issued: 3 September 2023.
- Implementation: 10 September 2023.
- The guideline states that a month/year expiry date is taken to mean the last day of that month (see the section headed “Manufacturing Date & Expiry Date”, printed page 11; the same instruction appears for small immediate packaging units on printed page 13).
- Official document: https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-dgda/2024/12/f7a2b793f8a6460db4fe809a4cdba158.pdf

The page's example `EXP 07/2027` therefore correctly explains 31 July 2027 as the final day of the stated month, in the context of the cited DGDA guideline. Continue to distinguish expiry-date interpretation from any separate in-use shelf-life after opening, reconstitution or dilution.

## 12. Publishing safeguard — implemented

The author approved manual-only publishing with explicit approval. The change was merged into `main` in commit `9de0128e7c4961d860b1b41dcd62f0eab684f30c`.

The current `.github/workflows/scheduled-articles.yml` now:

- Has only a manual `workflow_dispatch` trigger.
- Has no daily cron trigger and no push trigger.
- Requires the `author_approval` boolean input, defaulting to false.
- Runs the release job only when `inputs.author_approval == true`.

A manual release processes all calendar entries considered due by the release script, so the author must review every due item before checking the approval box. No article was published by merging this safeguard. Existing published content and URLs were not changed.

## 13. Updated priorities

| Priority | Action | Current status |
|---|---|---|
| P0 | Manual-only publishing with explicit author approval | Implemented on `main` |
| P1 | Complete 86-URL crawl and technical issue inventory | Pending; representative sample only |
| P1 | Extend Search Console access beyond the latest three days | Access limitation; requires a fuller GSC data connection |
| P1 | Monitor Bangla expiry-date query and snippet CTR over a longer period | Opportunity identified; no content change |
| P1 | Review the four-page personal-name query cluster | Potential overlap; no consolidation recommended yet |
| P1 | Validate all medical references and high-risk claims article by article | Pending |
| P2 | Validate structured-data graphs and entity IDs across the site | Pending |
| P2 | Trim the Pharma Blog meta description if a full review confirms value | Proposed only |
| P2 | Audit internal links across the eight content categories | Pending |
| P3 | Review Bing and AI referral/visibility data where connected | Pending |

## 14. Change and publishing log

- Merged the editorial profile, article-review template, baseline audit and manual-only approval workflow.
- Merge commit: `9de0128e7c4961d860b1b41dcd62f0eab684f30c`.
- The publishing workflow is the only production workflow changed.
- No existing article body, page title, description, URL, canonical, image, CSS, JavaScript, navigation, sitemap or robots file was edited during this SEO review.
- GSC metrics and technical checks in this addendum are diagnostic findings; proposed on-page changes remain unimplemented pending separate review and approval.

## Safety and change log

- This audit report is documentation only.
- No production page, article, URL, image, CSS, JavaScript, sitemap or robots file was changed as part of this report. The publishing workflow change is a proposal on the review branch only and is not active until approved and merged.
- The business/editorial profile, reusable review template and baseline audit are committed under `seo/`.
- The manual-only publishing safeguard is active on `main` after the author's approval.

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


## Follow-up review: scheduled article quality and Bangladesh OTC legal source

**Reviewed:** 27 November 2026  
**Scope:** Selected calendar articles and the Bangladesh prescription-versus-OTC explainer. This is a focused source review, not a full medical-content audit.

### Scheduled content spot-check

- The English and Bangla Drug Metabolism pages both exist, are indexable, have self-referencing canonicals and concise language-specific metadata. The English page is approximately 980 words and cites NCBI Bookshelf and Merck Manual.
- Drug Excretion, Drug Half-Life, Bioavailability and Prescription vs OTC pages were present and indexable in the checked repository snapshot. Their titles, descriptions and canonical URLs were populated.
- The 28 November Onset, Peak and Duration article and its series hub were present but remained `noindex,nofollow`, as expected before their scheduled release.
- The 30 November Dosage Forms page was present but remained `noindex,nofollow`, as expected before its scheduled release.
- The Pharmacogenetics article was present, indexable and included references to MedlinePlus, FDA, CDC and peer-reviewed literature.
- This was a selected-page check only; it does not establish that all English/Bangla pairs are complete or scientifically verified.

### Action required before revising the published Rx vs OTC article

The current article states that a 2020 news report counted 39 OTC medicines and refers readers to the National Drug Policy 2016 appendices. A more direct and newer primary source is available: DGDA's **National Guideline on Accreditation of Model Pharmacy and Model Medicine Shop in Bangladesh**, authorized 2 June 2024. Annex 5 defines OTC and prescription-only medicines and lists 39 DGDA-authorized allopathic OTC medicine categories (PDF printed pages 21–22). The list includes, among others, omeprazole capsules, metronidazole tablets/suspension and paracetamol formulations. The article should cite this DGDA annex directly and make clear that the list is the DGDA's published list in that 2024 guideline, not a count inferred from a 2020 media report.

The article's statement about a fine of up to Tk 20,000 is consistent with the penalty schedule accompanying the Drugs and Cosmetics Act 2023 for a breach of section 40(d). The strongest citation is the official 18 September 2023 Gazette schedule, not a secondary WHO report. Section 40(d) itself establishes the prescription rule; the schedule sets the penalty. Keep these as distinct citations.

WHO Bangladesh's 7 March 2023 report supports the red-label explanation: the Drug Control Committee endorsed the red identification mark, and the requirement was to show the word “antibiotic” and a warning against use without a registered physician's prescription. The article's current wording is broadly consistent with this source.

**Recommended correction (not applied):** update the Rx vs OTC article's reference list and OTC-list paragraph to cite DGDA's 2024 guideline Annex 5; cite the official Gazette schedule for the Tk 20,000 penalty. Do not edit the published page until the author approves the content correction.

### Primary sources checked

- DGDA, *National Guideline on Accreditation of Model Pharmacy and Model Medicine Shop in Bangladesh* (authorized 2 June 2024), Annex 5, printed pp. 21–22: https://dgda.gov.bd/sites/default/files/files/dgda.portal.gov.bd/policies/538854fb_87f2_4ecd_97a3_22f1f67a6721/2024-11-28-10-09-f124b507dc7aa84fed18c304ade5c3c3.pdf
- Bangladesh Gazette, *Drugs and Cosmetics Act 2023*, schedule entry 22 for section 40(d): https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-da-feni/2024/12/4897c3ada3304c38b578594760fc7f1b.pdf
- Laws of Bangladesh, section 40: https://bdlaws.minlaw.gov.bd/act-print-1447/section-print-52497.html
- WHO Bangladesh, antibiotic red-label requirement: https://www.who.int/bangladesh/news/detail/07-03-2023-establishing-red-label-of-antibiotics-for-curbing-antimicrobial-resistance-in-bangladesh
