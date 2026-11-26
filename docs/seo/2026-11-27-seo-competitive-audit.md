# SayedulAbrar.site — SEO Competitive Intelligence & Implementation Audit
**Audit date:** 27 November 2026  
**Repository:** `sayedulabrarsa-beep/sayedulabrarsa-beep.github.io`  
**Branch:** `seo-audit-2026-11-27`  
**Scope:** Read-only inspection of the current `main` branch, published HTML, sitemap, robots.txt, article metadata, selected content, and connected Google Search Console data.

> **Publication guardrail:** This document is a review artifact on a separate branch. No live page, article, URL, branding, navigation, sitemap or production file was changed. Do not merge this branch or publish any article changes without Sayedul Abrar's explicit approval.

## 1. Executive findings

1. The site has a substantive bilingual pharmaceutical knowledge base and an established static-site structure. The audit should optimise existing pages before creating new URLs.
2. Search Console's available access is limited to **21–23 November 2026** (three finalized days). It does not provide a valid previous-period comparison. Treat the results as short-window opportunity signals, not trends.
3. The strongest immediate opportunity is the expiry-date cluster. The English page has 72 impressions, zero clicks and average position 8.97. The Bangla page has 115 impressions, 3 clicks and average position 6.30; within it, the exact query **“মেয়াদ শেষ হওয়ার তারিখ”** has 47 impressions, zero clicks and average position 8.04.
4. Other short-window opportunities include the Bangla iron-tablet page (32 impressions, zero clicks, position 11.31), Bangla QA vs QC (22, zero clicks, position 7.09), and Bangla API (18, zero clicks, position 6.83).
5. The site-wide identity query “sayedul abrar” is returned for four URLs (About, homepage, Learning, Achievements). This may indicate overlapping identity signals, but the pages have distinct purposes. Improve their unique titles, descriptions and page roles; do not merge or delete them.
6. The current sitemap has 86 URLs, including 59 blog URLs (the blog landing page plus 58 article-language URLs). The article-language pages form 29 English/Bangla pairs. No duplicate sitemap locators were detected.
7. `robots.txt` allows general crawling and explicitly allows several AI/search crawlers; it points to the canonical sitemap.
8. Seven inspected article pages have canonical URLs, English/Bangla alternates where applicable, descriptive titles and descriptions, structured data, and no missing image alt attributes in the inspected image elements.
9. The legacy `_src/build.py` explicitly exits unless `ALLOW_OLD_GENERATOR=1` and warns it is retired because it can overwrite current homepage, menu and blog pages. **Do not run it.**
10. An old one-off metadata script `_src/seo_meta_tune.py` contains historical Search Console title/description replacements. Do not re-run it blindly; compare current production HTML first.

## 2. Verified Search Console snapshot

**Property:** `https://sayedulabrar.site/`  
**Effective range:** 2026-11-21 through 2026-11-23  
**Access mode:** free recent-three-days; comparison unavailable.

### Page-level metrics

| Page | Clicks | Impressions | CTR | Avg. position |
|---|---:|---:|---:|---:|
| English expiry article | 0 | 72 | 0.00% | 8.97 |
| Bangla expiry article | 3 | 115 | 2.61% | 6.30 |
| Bangla iron-tablet article | 0 | 32 | 0.00% | 11.31 |
| Bangla QA vs QC article | 0 | 22 | 0.00% | 7.09 |
| Bangla API article | 0 | 18 | 0.00% | 6.83 |

### Query-level details

**English expiry page**
- “date of manufacturing”: 1 impression, position 79.
- “is the mfg date the expiration date”: 1 impression, position 74.

**Bangla expiry page**
- “মেয়াদ শেষ হওয়ার তারিখ”: 47 impressions, 0 clicks, position 8.04.
- “উৎপাদন তারিখ”: 2 impressions, position 5.50.
- “ট্যাবলেট এর মেয়াদ কতদিন থাকে”: 1 impression, 1 click, position 1.
- “কোবে মেয়াদ শেষ হওয়ার তারিখ”: 1 impression, position 1.
- “osud er expiry date”: 1 impression, position 6.

**Bangla iron-tablet page**
- “আয়রন ট্যাবলেট কখন খেতে হয়”: 2 impressions, position 10.50.
- “আয়রন ট্যাবলেট খাওয়ার নিয়ম”: 1 impression, position 10.
- “আয়রন ট্যাবলেট দিনে কয়টা খাওয়া যায়”: 1 impression, position 9.
- “আয়রন ট্যাবলেট খেলে কি হয়”: 1 impression, position 80.

**Bangla QA vs QC**
- “qa and qc difference bangla”: 1 impression, position 9.

**Bangla API**
- “api full form in pharmaceutical”: 1 impression, position 4.
- “api meaning pharma”: 3 impressions, position 7.
- “api full form in pharma”: 2 impressions, position 7.5.
- Other close variants: 1 impression each.

### Interpretation and cautions

- Do not call a page-level CTR of zero a stable performance pattern on a three-day sample.
- For the Bangla expiry page, the page itself has 3 clicks / 115 impressions. The 47-impression zero-click figure belongs to one query, not the whole page.
- Search Console's position is an average across impressions and is not a fixed rank.
- No traffic, volume, keyword difficulty or ranking increase should be inferred from these figures.

## 3. Technical inspection

### Sitemap
- 86 total URL entries.
- 59 blog URLs including `/blog/`.
- 58 article-language URLs, forming 29 English/Bangla pairs.
- 86 unique locators; no duplicate locators detected.
- Recent lastmod values include 2026-11-27.
- The earlier strategy PDF recorded a smaller snapshot (75 URLs / 49 blog entries); the current repository sitemap has grown since that snapshot.

### Robots
- `robots.txt` returns Allow: / for general crawlers and named AI/search bots.
- Sitemap declaration: `https://sayedulabrar.site/sitemap.xml`.
- No blocking issue identified in the inspected file.

### Canonical and hreflang
The following pages were inspected in source:
- `blog/expiry-date-vs-manufacturing-date-medicine/index.html`
- `blog/expiry-date-vs-manufacturing-date-medicine-bangla/index.html`
- `blog/how-to-take-iron-tablets-properly-bangla/index.html`
- `blog/quality-assurance-vs-quality-control-bangla/index.html`
- `blog/active-pharmaceutical-ingredient-api-from-raw-material-to-medicine-bangla/index.html`
- `blog/drug-vs-medicine/index.html`
- `blog/drug-vs-medicine-bangla/index.html`

These inspected pages contain self-referencing canonical tags. Paired English/Bangla examples include reciprocal hreflang annotations. The broader site should still be crawled before declaring every page technically clean.

### Images and structured data
- The seven inspected pages contain no image elements with absent or empty alt attributes.
- The selected pages use Article/BlogPosting, Person, BreadcrumbList and, where present, FAQPage structured data.
- Do not assume FAQ rich-result eligibility; Google's FAQ rich results are restricted. Keep FAQs for readers and validate schema against current search-engine policies.
- Validate that all schema facts (dates, author, language, image, main entity) match visible content.

### Build safety
- `_src/build.py` is explicitly retired and exits by default; it warns it can overwrite current homepage, menu and blog pages. Never execute it for this audit.
- `_src/seo_meta_tune.py` is a one-off historical script with hard-coded Search Console changes. Do not rerun without a page-by-page diff and approval.

## 4. Content-level assessment

### Expiry date / manufacturing date (English and Bangla)
The existing English page already includes:
- Direct answer and EXP/MFG/batch definitions.
- Month-year rule with worked date examples.
- Date decoder, two-clock timeline, use-after-opening limits.
- Storage guidance, four-step pack check, quiz, myths, FAQs and references.
- Bangladesh DGDA packaging/label guidance in the page's visible content.

**Do not add another generic DGDA section or repeat the month-year explanation.** The next content review should:
- Check that all date-format examples are consistent with the Bangladesh DGDA guidance and the manufacturer's label.
- Ensure the statement “good through the last day of the month” is clearly scoped to a month/year-only expiry label and local applicable guidance.
- Make the Bangladesh regulatory reference easy to find and cite the official DGDA PDF with its exact page.
- Ensure any use-after-opening period is described as product-specific, not a universal 28-day or 30-day rule.
- Review whether the English title and description can better match search intent without sacrificing accuracy.

### Iron tablets (Bangla)
Current page already covers timing, food, interactions, side effects, missed doses, overdose, duration, caution groups, dietary iron and references.
- Keep the article's formulation-specific distinction visible.
- Do not generalise ferrous sulfate timing to every oral iron product.
- Ensure dose advice is not inferred from GSC query “দিনে কয়টা”; direct readers to their prescription and clinician/pharmacist rather than suggesting a universal dose.
- Improve the snippet to emphasise the exact user intent (when to take, before/after food, tea/coffee/dairy/calcium interactions).
- Check references and distinguish local prescribing context from NHS guidance.

### QA vs QC (Bangla)
Current page covers QA, QC, production-batch example, OOS, GMP and patient relevance.
- Keep its practical batch example.
- Strengthen the relationship to ICH Q10 pharmaceutical quality systems without implying ICH Q10 replaces local GMP requirements.
- Add a concise QA-vs-QC answer near the beginning if not already prominent.
- Use the current page's existing GMP internal link; do not create a duplicate QA/QC article.

### API (Bangla)
Current page covers API definition, API vs finished product, manufacturing steps, purification, quality testing, GMP and Bangladesh context.
- Add the query-matched phrase “API-এর পূর্ণরূপ” in a natural early answer if not already present.
- Clarify API is active pharmaceutical ingredient, not a brand or finished tablet.
- Keep Bangladesh manufacturing claims dated and sourced; do not invent capacity, export or self-sufficiency figures.
- Link to the existing English pair, pharmaceutical-industry page, GMP and QA/QC pages.

### Drug vs Medicine
Current English and Bangla articles already contain direct answers, comparisons, rabeprazole/Finix examples, FAQs and references. The English page has a separate scientific/legal terminology section. The key review is to ensure the educational distinction is not presented as a universal legal definition. Use WHO terminology carefully and distinguish API/drug substance from finished pharmaceutical product. Do not create a second Drug vs Medicine article.

## 5. Search snippet candidates — drafts only

These are proposed candidates for review, not applied metadata.

| Page | Proposed title | Proposed description |
|---|---|---|
| English expiry | Medicine Expiry Date: What EXP and MFG Mean | Sayedul Abrar | Learn what EXP, MFG and batch numbers mean on medicine packs. Understand month/year expiry dates, use-after-opening limits and safe storage. |
| Bangla expiry | ওষুধের মেয়াদ শেষ ও উৎপাদনের তারিখ: EXP ও MFG বুঝুন | Sayedul Abrar | ওষুধের EXP ও MFG তারিখ কীভাবে পড়বেন? মেয়াদ শেষের তারিখ, উৎপাদনের তারিখ, ব্যাচ নম্বর ও সংরক্ষণের নিয়ম সহজে জানুন। |
| Bangla iron | আয়রন ট্যাবলেট কখন খাবেন? খাবারের আগে না পরে? | Sayedul Abrar | আয়রন ট্যাবলেটের সময়, খাবারের সঙ্গে সম্পর্ক, চা-কফি, দুধ ও ক্যালসিয়ামের ব্যবধান এবং ডোজ মিস হলে করণীয় জানুন। |
| Bangla QA/QC | QA vs QC: ওষুধশিল্পে পার্থক্য কী? | Sayedul Abrar | ওষুধ উৎপাদনে Quality Assurance (QA) ও Quality Control (QC)-এর পার্থক্য, GMP, OOS, CAPA ও বাস্তব উদাহরণ সহজ বাংলায় জানুন। |
| Bangla API | API-এর পূর্ণরূপ কী? ওষুধে API কীভাবে কাজ করে? | Sayedul Abrar | API-এর পূর্ণরূপ Active Pharmaceutical Ingredient। কাঁচামাল, উৎপাদন, বিশুদ্ধকরণ, quality testing ও finished medicine-এর পার্থক্য জানুন। |

Metadata lengths and truncation should be checked against actual rendered snippets before approval. Titles are not ranking guarantees.

## 6. Internal-link recommendations

Only use verified existing destinations:
- Expiry EN ↔ Stability testing EN; Generic vs Brand EN; Prescription vs OTC EN.
- Expiry BN ↔ Stability testing BN; Generic vs Brand BN; Prescription vs OTC BN.
- Iron BN ↔ Iron Deficiency vs Anemia BN; Prescription vs OTC BN.
- QA/QC BN ↔ GMP BN; API BN; Pharmaceutical Industry BN.
- API BN ↔ API EN; Pharmaceutical Industry BN; GMP BN; QA/QC BN.
- Drug vs Medicine EN ↔ Generic vs Brand EN; Pharmacology hub EN.
- Drug vs Medicine BN ↔ Generic vs Brand BN; Prescription vs OTC BN.

Do not insert links until exact live URLs are verified and reciprocal language links are confirmed.

## 7. Identity-query overlap

GSC reports four pages for “sayedul abrar”:
- `/about/`
- `/`
- `/learning/`
- `/achievements/`

These pages have distinct intent. Keep all four. Make each page's title/H1/description clearly describe its unique purpose and retain consistent Person entity references. The About page should be the primary biographical destination; homepage should be the overview; Learning and Achievements should remain specific supporting pages. Do not force every identity query to one URL.

## 8. Competitive research: evidence boundaries

Search research identified these useful reference sources:
- Bangladesh DGDA packaging and labelling guideline: official rule for month/year-only expiry dates and after-opening/reconstitution information.
- FDA expiration-date Q&A: stability and labelled storage conditions.
- NHS ferrous sulfate guidance: product-specific timing and interactions.
- ICH Q10: pharmaceutical quality system benchmark.
- WHO pharmaceutical terminology: contextual terminology for drug, medicine and pharmaceutical product.
- NIDDK / ACG / Mayo Clinic: clinical GERD education and guideline references.
- CPIC: pharmacogenetic guideline examples.

A public search result is not a reliable record of the exact Bangladesh Google SERP order. No exact top-five ranking positions are claimed in this report. A country/language/device-specific Google SERP capture is required before publishing a ranked competitor table.

## 9. Priority action plan

| Priority | Action | Impact | Effort | Evidence / reason |
|---:|---|---|---|---|
| 1 | Review English expiry snippet | High | Low | 72 impressions, 0 clicks, position 8.97 |
| 2 | Review Bangla expiry snippet and exact query fit | High | Low | Exact query 47 impressions, 0 clicks, position 8.04; page total 3/115 clicks |
| 3 | Review Bangla iron snippet and safety language | High | Low | 32 impressions, 0 clicks, position 11.31 |
| 4 | Review Bangla QA/QC snippet | Medium | Low | 22 impressions, 0 clicks, position 7.09 |
| 5 | Review Bangla API snippet for “API full form” intent | Medium | Low | 18 impressions, 0 clicks, position 6.83 |
| 6 | Validate identity-page differentiation | Medium | Medium | Four URLs returned for author-name query |
| 7 | Validate reciprocal hreflang across all 29 pairs | High | Medium | Bilingual site; selected pairs pass source inspection |
| 8 | Validate Article/Person/Breadcrumb schema sitewide | Medium | Medium | Schema present on selected pages; full validation pending |
| 9 | Expand contextual internal links across clusters | High | Medium | Existing content cluster has natural relationships |
| 10 | Re-run GSC after a full 28-day period is available | High | Low | Current connector access only supplies 3 days; no comparison |

## 10. Next validation cycle

1. Collect a full 28-day GSC export when connector access allows; compare the same dates and country/device slices.
2. Review query and page metrics separately; never confuse query CTR with page CTR.
3. Recheck the five priority pages after any approved snippet change.
4. Verify live page source, canonical, hreflang, structured data and image alt after manual publishing.
5. Check sitemap and Search Console indexing only after an approved page is actually deployed.
6. Maintain a register with page URL, language, primary keyword, intent, parent cluster, last reviewed date and approval status.

## 11. Publication and implementation status

- [x] Main branch inspected read-only.
- [x] Sitemap and robots.txt inspected.
- [x] Seven priority article HTML pages inspected.
- [x] GSC recent-three-day opportunities retrieved.
- [x] Page-level query data retrieved for five opportunity pages.
- [x] Search snippet candidates prepared.
- [x] Internal-link recommendations mapped.
- [ ] Full 28-day GSC baseline (not available through current connector entitlement).
- [ ] Full sitewide crawler audit (not run; no crawler results available in this audit).
- [ ] Exact top-five country/language SERP ranking comparison.
- [ ] Author approval for any production content or metadata change.
- [ ] Manual GitHub publishing and post-deployment validation.

**Final status:** Research and source inspection are complete for this initial evidence-backed cycle. The audit and drafts are stored on this separate branch for review. Production remains unchanged.
