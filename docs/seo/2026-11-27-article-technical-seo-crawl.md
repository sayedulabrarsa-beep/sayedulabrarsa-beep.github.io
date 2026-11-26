# Article Technical SEO Crawl — 27 November 2026

**Site:** https://sayedulabrar.site  
**Repository:** `sayedulabrarsa-beep/sayedulabrarsa-beep.github.io`  
**Branch:** `seo-audit-2026-11-27`  
**Scope:** Direct source inspection of all 58 English/Bangla article HTML pages listed in the repository sitemap (29 language pairs). This is a repository-source audit, not a live HTTP crawl or a Google indexing validation.

> **Safety:** No production page, article, metadata, URL, design, navigation, sitemap or robots file was changed. This report is stored on the separate SEO audit branch. Manual publishing and explicit author approval remain required.

## 1. Coverage and checks

All 58 article-language URLs were enumerated from `sitemap.xml` and their corresponding `index.html` files were fetched from the audit branch, which was created from the current main branch before audit-only documents were added.

For each page, the inspection checked:
- HTML language declaration (`lang`)
- page title and meta description presence
- canonical URL presence and uniqueness
- H1 presence and language presentation
- image `alt` attribute presence and empty values
- JSON-LD script presence
- hreflang alternate declarations
- basic HTML source size and metadata extraction

## 2. Findings

### Positive findings

1. **58/58 article pages were accessible in the repository source** using the sitemap-derived paths.
2. **58/58 inspected pages declare a page language** (`en` or `bn`).
3. **58/58 inspected pages have a self-referencing canonical URL** in the HTML head; the inspected pages showed one canonical declaration each.
4. **58/58 inspected pages have a page title and meta description.**
5. **58/58 inspected pages have an H1.** Bangla and English versions generally use language-appropriate headings. Some bilingual templates contain both language spans in one H1, with the non-active language hidden; this should be judged in rendered DOM and not automatically treated as duplicate visible headings.
6. **No missing or empty image alt attributes were found** among the `img` elements inspected across these 58 article pages.
7. **JSON-LD is present** across the inspected article pages (typically 1–4 script blocks).
8. **hreflang declarations are present** across the inspected article pages (the inspected templates showed 3 or 5 declarations depending on template).

### Important scope limits

- This inspection verifies markup in the GitHub source. It does not prove that the deployed server returns HTTP 200, that Google has indexed each URL, that rendered JavaScript content is visible to crawlers, or that Google accepts every structured-data item.
- Presence of JSON-LD is not the same as schema validity. Each schema type still needs validation against the live rendered page and the applicable Google rich-result requirements.
- Hreflang presence is not a complete reciprocal-cluster audit. All 29 English/Bangla pairs should be checked for exact reciprocal targets, canonical consistency, correct language codes and return links.
- Image alt presence is not a quality assessment. Alt text still needs editorial review for accuracy, usefulness and avoidance of keyword stuffing.
- No 58-page content-fact check or medical/regulatory claim review is implied by this technical scan.

## 3. Editorial and snippet observations

The technical scan found a generally consistent metadata foundation. It does not justify a site-wide title rewrite. Improve only pages with a demonstrated query/CTR opportunity, and preserve titles that already communicate a clear search intent.

Examples from the inspected set:
- API English page title is descriptive but long; the Bangla API title is concise and query-led. Keep both page-language-specific.
- QA vs QC English title is long but accurately describes the pharmaceutical context; the Bangla title is concise. Do not shorten at the cost of losing the pharmaceutical qualifier.
- The English clinical-trial title and Bangla title are descriptive but long. Consider a shorter snippet variant only after checking actual GSC query and CTR data.
- The Bangla expiry page already targets the high-impression phrase “ওষুধের মেয়াদ শেষ হওয়ার তারিখ (EXP)”. Its GSC snapshot shows actual clicks, so optimise the snippet rather than assuming the page is failing.
- The iron-tablet pages should retain safe, formulation-specific advice. Do not introduce a universal tablet count or universal timing instruction across different iron salts and products.
- The PPI article pair has strong query specificity. Any medical wording about rabeprazole, omeprazole, MUPS and sprinkle products must remain product/formulation-aware and reference appropriate authoritative sources.

## 4. Priority actions

| Priority | Work | Reason | Publication gate |
|---|---|---|---|
| P0 | Obtain a full 28-day and 3-month GSC export | Current connector snapshot only covers 21–23 Nov 2026; trend and CTR decisions need a longer baseline | No live change |
| P0 | Validate all 29 hreflang clusters for reciprocal links | Hreflang presence alone does not prove cluster correctness | Audit branch |
| P1 | Run live HTTP status, redirect, canonical and robots checks for all 86 sitemap URLs | Repository source cannot prove deployed response behavior | Audit branch |
| P1 | Validate structured data on representative page types, then all templates | JSON-LD presence does not prove schema correctness | Audit branch |
| P1 | Prioritise five GSC-supported refreshes already drafted in the priority pack | Expiry, iron, QA/QC and API have visible short-window impressions | Author approval before production |
| P2 | Review title/description truncation and duplication across identity pages | Protect the brand query while clarifying each page's purpose | Draft first |
| P2 | Review image alt text quality and image sitemap consistency | Presence is good; meaning and image discoverability still need review | Draft first |
| P2 | Build topic-cluster links between foundational and advanced articles | Improve discovery and topical relationships without creating duplicate URLs | Author approval before production |

## 5. Recommended internal-link architecture

Use contextual links in the article body, not only a generic “related articles” block. Suggested pathways:

### Medicine safety cluster
- Expiry date vs manufacturing date ↔ Medicine stability testing
- Expiry date vs manufacturing date ↔ Prescription vs OTC medicines in Bangladesh
- Iron tablets ↔ Iron deficiency vs anemia
- Antibiotic course ↔ Pharmacovigilance
- Prescription vs OTC ↔ Drug vs medicine

### Pharmacology cluster
- How medicines work ↔ Drug absorption ↔ Drug distribution ↔ Drug metabolism ↔ Drug excretion
- Drug half-life ↔ Drug metabolism and drug excretion
- Bioavailability ↔ Drug absorption
- Pharmacogenetics ↔ Drug metabolism

### Manufacturing and quality cluster
- Bangladesh pharmaceutical industry ↔ API ↔ GMP ↔ QA vs QC ↔ Stability testing
- API ↔ GMP ↔ Quality assurance vs quality control
- Stability testing ↔ Expiry date vs manufacturing date

### Research and clinical science cluster
- Clinical trial phases ↔ Pharmacovigilance
- Biosimilars ↔ Clinical trial phases
- Glucosamine research review ↔ How to interpret clinical evidence

### Product management and marketing cluster
- Pharmaceutical product management ↔ Pharmaceutical marketing strategy
- Product management ↔ Bangladesh pharmaceutical industry

These are recommendations, not a claim that every link is currently absent. Before adding a link, inspect the actual article body and avoid duplicate or forced anchors.

## 6. Immediate next validation cycle

1. Export Search Console data for 28 days and 3 months, grouped by page and query, with country/device filters where useful.
2. Compare sitemap URLs with live HTTP response codes and final canonical URLs.
3. Verify reciprocal hreflang across all 29 pairs.
4. Validate structured data on the homepage, blog landing page, English article, Bangla article and any special research/article template.
5. Review the top five refresh drafts against the latest query-level data and authoritative references.
6. Prepare a change set on a review branch; do not merge or publish until the author approves the exact changes.

## 7. Completion status

- [x] Enumerated 58 article-language URLs from sitemap.
- [x] Retrieved all 58 article HTML source files from the audit branch.
- [x] Checked language, title, description, canonical, H1, image alt, JSON-LD and hreflang presence.
- [x] Documented findings and limits.
- [ ] Live HTTP crawl of all sitemap URLs.
- [ ] Reciprocal hreflang validation of all 29 pairs.
- [ ] Structured-data validation against live rendered pages.
- [ ] Full 28-day and 3-month GSC trend analysis.
- [ ] Author approval for production changes.
- [ ] Manual GitHub publication after explicit approval.
