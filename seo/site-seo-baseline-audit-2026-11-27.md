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
- The scheduled article release workflow was changed to manual-only operation with an explicit `author_approval` input; it no longer has a cron or push publishing trigger.
- After this baseline review, the English and Bangla Prescription vs OTC pages were separately corrected on 27 November 2026. Their URLs, canonical tags, publication dates, layout and indexability were preserved; JSON-LD `dateModified` was updated.
- Other proposed on-page changes remain unimplemented unless explicitly recorded as completed below.

## Safety and change log

- This audit report is documentation; the separately recorded Rx vs OTC correction is live in the repository.
- The manual-only publishing safeguard is active on `main` after the author's approval and is not a proposal on a review branch.
- The business/editorial profile, reusable review template and baseline audit are committed under `seo/`.
- No scheduled article was released as part of this follow-up verification.

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

### Bangladesh prescription-versus-OTC correction — completed

Both published language versions have been corrected using primary Bangladesh sources. DGDA's **National Guideline on Accreditation of Model Pharmacy and Model Medicine Shop in Bangladesh**, authorized 2 June 2024, Annex 5, defines OTC and prescription-only medicines and lists 39 DGDA-authorized allopathic OTC medicine categories (PDF printed pages 21–22). The list includes omeprazole capsules, metronidazole tablets/suspension and paracetamol formulations. The article now cites this Annex directly rather than relying on a 2020 media count or the National Drug Policy 2016 appendices.

The fine of up to Tk 20,000 is now tied specifically to the official 18 September 2023 Gazette penalty schedule for a breach of section 40(d). The article distinguishes the prescription rule in section 40(d) from the penalty schedule. WHO Bangladesh's 7 March 2023 report remains the supporting source for the red-label explanation.

**Correction implemented on 27 November 2026:** the English and Bangla Rx vs OTC articles now cite DGDA's 2024 guideline Annex 5 and the official Gazette schedule for section 40(d). Both pages explain that section 40 has an OTC-list exception and avoid the inaccurate blanket statement that every antibiotic is always prescription-only; Annex 5 lists metronidazole tablet/suspension among its 39 entries. The superseded National Drug Policy 2016 / 2020 media-count references were replaced by the direct DGDA primary source. Publication dates remain 26 November 2026; Article JSON-LD `dateModified` is updated to 27 November 2026.

### Primary sources checked

- DGDA, *National Guideline on Accreditation of Model Pharmacy and Model Medicine Shop in Bangladesh* (authorized 2 June 2024), Annex 5, printed pp. 21–22: https://dgda.gov.bd/sites/default/files/files/dgda.portal.gov.bd/policies/538854fb_87f2_4ecd_97a3_22f1f67a6721/2024-11-28-10-09-f124b507dc7aa84fed18c304ade5c3c3.pdf
- Bangladesh Gazette, *Drugs and Cosmetics Act 2023*, schedule entry 22 for section 40(d): https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-da-feni/2024/12/4897c3ada3304c38b578594760fc7f1b.pdf
- Laws of Bangladesh, section 40: https://bdlaws.minlaw.gov.bd/act-print-1447/section-print-52497.html
- WHO Bangladesh, antibiotic red-label requirement: https://www.who.int/bangladesh/news/detail/07-03-2023-establishing-red-label-of-antibiotics-for-curbing-antimicrobial-resistance-in-bangladesh

## Follow-up review: complete sitemap page-level technical check

**Reviewed:** 27 November 2026  
**Scope:** All 86 HTML pages listed in the production XML sitemap, plus key excluded utility/redirect pages. This is a static HTML/repository audit, not a browser-based crawl or a full medical-content fact-check.

### Results

- **86 of 86 sitemap URLs** were matched to and checked against the corresponding HTML page in the repository (including the homepage root).
- All checked sitemap pages had a non-empty page title, meta description, self-referencing canonical URL and robots directive.
- Every checked page had exactly one H1.
- No checked image element was missing an `alt` attribute or had an empty `alt` value.
- All JSON-LD script blocks parsed as valid JSON. This confirms syntax only; it does not validate Schema.org semantics, entity relationships, Google rich-result eligibility or consistency across the graph.
- No sitemap page showed an accidental `noindex` directive.
- English/Bangla page pairs were present in the sitemap for the reviewed published article set. A complete reciprocal hreflang graph validation and destination-by-destination internal/external link crawl remain separate tasks.
- The sitemap contains 86 public page URLs. The 18 future English/Bangla article pages in the repository are intentionally excluded from the sitemap while their release status remains future/scheduled.
- Utility routes excluded from the sitemap were checked for intent: `/search/` is `noindex,follow`; `/experience/` redirects to the About journey section and is noindex; `/finix/` redirects to the canonical Finix brand page; and `/404.html` is noindex. These are not missing public content pages.
- The publications page and glucosamine article metadata were inspected directly after an initial automated length check was found to truncate descriptions at apostrophes. Their actual description values are complete and descriptive; no edit was warranted.

### Changes made from this page-level pass

No production HTML or design changes were necessary. The audit report itself was updated to record the completed scope and distinguish static syntax checks from semantic/schema and link validation.

### Remaining work

1. Validate reciprocal hreflang pairs and all local navigation/article links, including link targets and redirects.
2. Validate structured-data graphs semantically and test eligible rich-result types.
3. Continue article-by-article medical reference and claim verification, prioritising high-risk medicine-use, dosing, safety, pregnancy, interaction and Bangladesh regulatory claims.
4. Review image delivery, responsive behaviour, accessibility and performance in a real browser/device environment.
5. Obtain longer-window Search Console data before changing pages based on short-term impressions or CTR.

## Follow-up: bilingual navigation, structured data, accessibility and medical-label review

**Reviewed:** 27 November 2026  
**Scope:** Published sitemap pages, all 29 published English/Bangla article pairs, four medicine brand pages, selected complex article fragments, global CSS/JavaScript and connected Search Console data.

### Bilingual navigation and internal links

- Checked all **29 published English/Bangla article pairs (58 article pages)** for reciprocal `hreflang="en"`, `hreflang="bn"` and `hreflang="x-default"`. Each page points to its own canonical URL for its language, the paired page for the other language, and the English canonical for x-default. No mismatches were found.
- Checked local internal link targets across the 58 article pages and 28 other sitemap pages. No missing local page or asset target was found in the repository.
- Checked same-page fragment links on eight complex articles with tables/contents and long section navigation. All tested fragment targets resolve to an element ID.
- Found and removed premature links from published pages to future, noindex articles and a future series hub. A published page should not send readers to a page that is still awaiting its scheduled release and author approval. The affected English/Bangla links were in Drug vs Medicine, Drug Half-Life and Bioavailability pages. The underlying future articles and their manual-only release status were not changed.

### Image delivery and accessibility checks

- The production sitemap contains **927 image entries**. Every image URL (after removing cache query strings) maps to a file present in the repository.
- The previous 86-page audit found no missing or empty image alt attributes.
- Representative homepage, article and learning pages use explicit image dimensions. The homepage and article hero images are prioritised; below-the-fold images generally use lazy loading. A complete per-image runtime layout-shift measurement was not available.
- The global amber text/control accent was darkened from `#C26E00` to `#9A5600` in the shared stylesheet, article-end component and sitemap stylesheet. Calculated contrast is 5.16:1 on the main light background (`#F3F4F9`), 4.72:1 on the secondary light background (`#E8EAF2`) and 5.67:1 on white. The amber appearance is retained while normal-size text and white button labels gain a stronger contrast margin. The dark-theme accent was not changed.
- Updated the site navigation script so keyboard focus pauses the moving navigation rail. The full-screen navigation overlay now has dialog semantics, an accessible title, a Tab/Shift+Tab focus loop and Escape-to-close behaviour. Existing reduced-motion handling remains in place.

### Structured-data semantic corrections

- Changed the main medicine entity from the generic Schema.org `Substance` type to the more specific `Drug` type on the Finix MUPS, Finix, Finix HP and Malifa pages. The `Drug` type supports the active ingredient, dosage form, proprietary name and manufacturer properties used on these pages. See [Schema.org Drug](https://schema.org/Drug).
- Removed duplicate Bengali alternate names from the homepage Person entity.
- Rechecked the edited pages: all JSON-LD blocks parse as valid JSON. This is a syntax check plus targeted type/property review, not a full external Schema.org or Google Rich Results validation of every graph on all 86 pages.

### Medical/product-label accuracy corrections

The following corrections keep the Bangladeshi manufacturer's insert distinct from a US label for another rabeprazole product:

1. **When to Take a PPI** — clarified that Opsonin's published Finix 10 mg information identifies a delayed-release sprinkle capsule but does not specify a method for opening or mixing it. Instructions from a different US rabeprazole sprinkle product are now explicitly labelled as product-specific and must not be treated as Finix instructions. The Finix 20 tablet food-timing statement is similarly qualified.
2. **Finix MUPS 20 brand page** — updated the English and Bangla visible FAQs and FAQ structured data. The Opsonin Finix MUPS insert lists once-daily dosing for most indications and states that all three medicines in H. pylori triple therapy are taken with morning and evening meals; it does not provide a universal meal-timing rule for other indications. The US ACIPHEX label is now clearly distinguished from the Finix MUPS insert.
3. **Finix brand page** — updated the visible FAQ and FAQ structured data to distinguish the local Finix insert from US ACIPHEX food-timing instructions.

Primary sources checked:
- [Opsonin Finix MUPS 20 manufacturer insert](https://www.opsonin-pharma.com/uploads/pdf/pdf_1742274302.pdf)
- [Opsonin Finix 10 mg manufacturer insert](https://www.opsonin-pharma.com/uploads/pdf/pdf_1762153089.pdf)
- [DailyMed: US ACIPHEX rabeprazole delayed-release tablet label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1eb38279-0237-4967-be7a-c53a826c1138)
- [DailyMed: US rabeprazole delayed-release sprinkle product label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5b1b1530-abc8-487a-b673-2b35cbf14e0c)

### Search Console review

The connected property is `sc-domain:sayedulabrar.site`, with owner access. The available integration currently provides only the three-day window **21–23 November 2026**, with no comparison period.

- Bangla expiry-date article: 50 impressions, 0 clicks, average position 7.9. The query `মেয়াদ শেষ হওয়ার তারিখ` contributed 47 impressions at average position about 8.0.
- Bangla API article: 8 impressions, 0 clicks, average position 7.
- Branded query `sayedul abrar` appeared across four pages, but the data volume is too small to establish harmful cannibalisation. The homepage remains the main identity page and About remains the detailed biography page.
- No title, description or page consolidation change was made from this three-day sample. The Bangla expiry page's current title and description already match the main query intent. Reassess after a longer data window becomes available.

### Remaining limitations and next checks

1. A live mobile/desktop browser session and a completed PageSpeed Insights/Lighthouse run were not available in this audit. CSS breakpoints, reduced-motion rules, image dimensions and navigation code were reviewed statically; this is not a substitute for real-device testing.
2. Full semantic validation of every structured-data graph with Schema.org Validator and Google's Rich Results Test remains outstanding.
3. External outbound links have not all been followed and verified individually. Internal route/asset targets were checked against the repository.
4. Medical references and claims still need a complete article-by-article review. The targeted product-label corrections above do not constitute a clinical review of every article.
5. Search Console comparisons and trend conclusions must wait until a longer date range is available.

No future article was published and the manual author-approval safeguard remains in force.

## Follow-up: additional medicine-label safety corrections

**Reviewed:** 27 November 2026  
**Scope:** Finix, Finix MUPS, Finix HP and Malifa public brand pages, plus the PPI and antibiotic education articles.

### Corrections implemented

- **Antibiotic-course article (English and Bangla):** changed the headline and search/social metadata from a blanket “must complete the course” slogan to “take antibiotics exactly as prescribed”. The article body continues to advise readers not to stop, skip, extend, share or save antibiotics without professional advice; duration remains the prescriber's decision. This better reflects current CDC wording and preserves the article's discussion of stewardship and shorter evidence-based durations.
- **Finix MUPS paediatric section:** retained the manufacturer-listed 1–11-year GERD doses but added a prominent formulation caution. This page describes the 20 mg MUPS tablet; it must not be split, crushed or chewed to create a lower dose. The insert does not explain how to obtain a 5 mg dose from the 10 mg sprinkle capsule. The English insert gives 12 weeks for the under-15 kg group, while the Bangla section gives 8 weeks; the page now tells readers that the prescriber/manufacturer must confirm the formulation, dose and duration.
- **Finix brand paediatric section:** removed the unsupported 12-years-and-older regimen extrapolated from a US label. The page now reports the local insert's 1–11-year doses and warns that it does not explain how to measure a 5 mg dose from the 10 mg sprinkle capsule.
- **Finix / Finix MUPS food instructions:** the English and Bangla blocks of the Opsonin inserts differ. The English sections say food effects have not been evaluated; the Bangla sections say food does not hinder absorption. The pages now disclose this discrepancy, retain the explicit morning/evening-meal instruction for the H. pylori triple regimen, and avoid inventing a universal food-timing rule for other indications.
- **Finix pregnancy/lactation FAQ:** now distinguishes the Opsonin insert's benefit–risk wording and lack of breast-milk data from animal information in the US ACIPHEX label.
- **Finix HP course and safety FAQs:** replaced the US-label-derived seven-day statement with the Opsonin insert's 7–14-day instruction, clarified that meal timing is not universally specified, and tells readers to confirm duration and pack count because seven sachets per carton should not be assumed to cover the full prescribed course. Added matching English and Bangla pregnancy/breastfeeding FAQs based on the manufacturer insert.
- **Malifa pregnancy/lactation:** replaced the US ACCRUFER-style “no fetal/infant exposure expected” statement with the Navana Malifa insert's actual wording: use during pregnancy if necessary and during breastfeeding if clinically needed, subject to individual clinical assessment.
- **Malifa with PPIs:** softened the specific PPI interaction claim. The Navana insert lists dimercaprol, bisphosphonates, levodopa, thyroid medicines and tetracycline antibiotics; it does not give a specific rabeprazole/PPI instruction. The FAQ now recommends prescriber/pharmacist review rather than telling readers to avoid the combination.

Primary product-label sources:
- [Opsonin Finix MUPS insert](https://www.opsonin-pharma.com/uploads/pdf/pdf_1742274302.pdf)
- [Opsonin Finix 10 mg insert](https://www.opsonin-pharma.com/uploads/pdf/pdf_1762153089.pdf)
- [Opsonin Finix HP insert](https://www.opsonin-pharma.com/uploads/pdf/pdf_1748761563.pdf)
- [Navana Malifa insert](https://navanapharma.com/upload/label_files/164411133.pdf)
- [CDC: Antibiotic use and taking antibiotics exactly as prescribed](https://www.cdc.gov/antibiotic-use/about/index.html)

### Manufacturer-document follow-up recommended

The text extracted from the linked Finix MUPS insert shows additional English/Bangla differences beyond the food statement: the English section lists a 50-tablet (10 × 5) pack while the Bangla section lists 60 tablets (10 × 6), and the paediatric duration differs for the under-15 kg group. The current website pack information follows the 60-tablet packaging brief, but the bilingual manufacturer insert should be reconciled by Opsonin Regulatory/Medical Affairs before it is treated as a single consistent source.

Text extraction from the Finix HP PDF also appears to show a possible English/Bangla difference in the ingredient and sachet-count text. Because the PDF could not be visually verified in this audit, this is **not treated as a confirmed label error**. The original artwork and printed carton should be checked by the manufacturer. The public page follows the English insert/product listing and tells readers to confirm the pack count and course with the prescriber or pharmacist.

No manufacturer PDF was edited. No future article was published.

## Final verification note: product-label discrepancies and indexing queue

**Reviewed:** 27 November 2026

- The Finix MUPS page now explicitly flags the English/Bangla insert differences on food effects and paediatric duration. The insert text also lists different carton counts: 50 tablets (10 × 5) in the English section and 60 tablets (10 × 6) in the Bangla section. The current website page does not publish a numeric pack count. Do not add one until Opsonin confirms the current approved pack size and reconciles the bilingual PDF with the printed carton through Regulatory/Medical Affairs.
- The older Finix HP insert (pdf_1748761563) produced a possible English/Bangla text-extraction mismatch. A newer official Opsonin insert (pdf_1764844756) was found and the product page now links to it; its indexed text confirms the Rabeprazole + Amoxicillin + Clarithromycin composition, seven sachets per carton and 7–14-day regimen. The older-PDF mismatch is therefore not treated as a current label error. The printed carton and latest approved insert should still be checked before dispensing.
- The Finix HP FAQ now includes pregnancy and breastfeeding cautions in both languages and in FAQ structured data. The Malifa FAQ and interaction guidance now follow the Navana insert rather than extrapolating a US ferric-maltol label.
- The IndexNow workflow's concurrency setting was changed so a newer push does not cancel an already-running submission. GitHub still permits only one pending run per concurrency group, so the final affected-page updates were consolidated into a single batch commit. Submission is not marked complete until the queued run finishes after the Pages deployment.
- The scheduled article workflow remains manual-only with explicit author approval. No scheduled or future article was published.
