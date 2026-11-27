# Search Console Export Analysis & Next SEO Action Plan — 27 November 2026

**Website:** https://sayedulabrar.site/  
**Repository:** `sayedulabrarsa-beep/sayedulabrarsa-beep.github.io`  
**Branch:** `seo-audit-2026-11-27`  
**Source files:** Two user-uploaded Google Search Console ZIP exports dated 27 November 2026.  
**Production status:** Analysis only. No live website changes, article edits, URL changes, metadata changes, merges or publication.

## 1. Source inventory and data limitations

### Export A
- Filter label: Search type = Web (text-based); Date = Last 3 months.
- Files: Chart (31 rows), Queries (221 rows), Pages (59 rows), Countries (101 rows), Devices (3 rows), Search appearance (0 rows), Filters (2 rows).
- Chart dates actually present: **25 October–24 November 2026** (31 dates), not the full three-month interval stated by the filter.
- Daily chart sum: **118 clicks, 3,108 impressions**.
- Country table sum matches chart: **118 clicks, 3,108 impressions**.
- Page table sums to **123 clicks and 3,496 impressions**; query table sums to **84 clicks and 977 impressions**. These dimensions do not reconcile with the chart/country totals, likely because exported dimension tables are partial/top rows, privacy suppression, or aggregation behavior. Do not sum these tables as a sitewide total.
- Search appearance table is empty.

### Export B
- Filter label: Search type = Web (text-based); Date = Last 28 days; query regex begins with common question words (who/what/where/when/why/how/was/did/do/is/are/does/if).
- Chart dates present: **28 October–24 November 2026** (28 dates).
- Daily chart sum: **1 click, 71 impressions**.
- Page table sum: **1 click, 72 impressions**; query/country table sums: **1 click, 71 impressions**.
- This is a filtered question-query subset, not the site's complete 28-day performance. It must not be compared directly with Export A as if it were an equivalent period or all-query report.

### Important interpretation rules
1. Export A's filter says Last 3 months, but its Chart.csv contains only 31 dates. The query/page/country dimension tables may represent a broader selected period or their own top-row extraction. Treat this export as a mixed-coverage report; use its chart totals only for the dates actually present and label page/query metrics as export-table observations.
2. Export B is a regex-filtered question-query report. It is useful for question-intent discovery, not for total site traffic.
3. Search Console average position is an impression-weighted average across queries, devices and locations, not a fixed rank.
4. No previous-period comparison was supplied. This report does not establish a confirmed ranking decline or recovery trend.
5. Low-volume query rows (one to a few impressions) are discovery signals only, not a basis for major content rewrites.

## 2. Sitewide chart observations (Export A, 25 Oct–24 Nov)

- **118 clicks / 3,108 impressions** in the 31 chart dates.
- Approximate aggregate CTR: **3.80%** (118 ÷ 3,108).
- Impression-weighted average position calculated from daily chart rows: approximately **9.97**.
- The chart's first recorded week (26 Oct–1 Nov) had 55 clicks and 528 impressions.
- 2–8 Nov: 21 clicks and 821 impressions.
- 9–15 Nov: 22 clicks and 776 impressions.
- 16–22 Nov: 14 clicks and 663 impressions.
- 23–24 Nov: 6 clicks and 320 impressions (partial two-day period).

The first seven-day period is unusually click-heavy compared with subsequent periods. Without query/page/day segmentation and a matched previous period, do not call this a confirmed decline. The 23–24 Nov segment is incomplete and should not be compared with full weeks.

## 3. Country and device observations (Export A)

### Country
- Bangladesh: **113 clicks, 1,699 impressions, 6.65% CTR, average position 7.38**.
- India: **3 clicks, 552 impressions, 0.54% CTR, average position 9.02**.
- United States: **0 clicks, 174 impressions, average position 23.82**.
- Pakistan: **0 clicks, 95 impressions, average position 9.29**.
- United Kingdom: **0 clicks, 74 impressions, average position 32.22**.

Bangladesh is the strongest market by clicks and CTR. India has substantial impressions but very low CTR; do not assume it is a content-quality issue without query and page segmentation. Prioritise Bangladesh-relevant search intent, terminology and official sources while retaining English content for international discovery.

### Device
- Mobile: **78 clicks, 2,497 impressions, 3.12% CTR, average position 6.89**.
- Desktop: **40 clicks, 586 impressions, 6.83% CTR, average position 23.26**.
- Tablet: **0 clicks, 25 impressions, 0% CTR, average position 7.16**.

Mobile accounts for about 80% of chart impressions. Desktop has a much weaker average position despite a higher CTR. This is a priority for device-specific inspection: test mobile rendering, title/snippet, page speed and content visibility, but do not infer a specific technical fault from Search Console data alone. Investigate desktop query mix and country mix before changing design.

## 4. Highest-value page opportunities (Export A Pages.csv)

| Page | Clicks | Impressions | CTR | Avg. position | Priority interpretation |
|---|---:|---:|---:|---:|---|
| Bangla expiry/MFG | 9 | 791 | 1.14% | 7.38 | Highest priority: strong visibility, weak CTR |
| English expiry/MFG | 3 | 788 | 0.38% | 7.97 | Highest priority: strong visibility, very weak CTR |
| Homepage | 76 | 346 | 21.97% | 3.12 | Protect; strong personal-brand result |
| About | 16 | 219 | 7.31% | 5.51 | Protect; clarify identity and author authority |
| Bangla Drug vs Medicine | 0 | 197 | 0% | 7.68 | High-priority snippet/content-intent review |
| Bangla Generic vs Brand | 2 | 166 | 1.20% | 7.53 | Improve snippet and early answer |
| English Iron Tablets | 0 | 145 | 0% | 21.34 | Ranking/content gap; do not treat as CTR-only issue |
| Bangla Iron Tablets | 0 | 83 | 0% | 14.51 | Improve relevance and internal links; validate medical wording |
| Finix MUPS brand page | 0 | 80 | 0% | 4.90 | High-position/zero-click review; check exact queries and snippet intent |
| Publications | 5 | 52 | 9.62% | 10.27 | Keep and strengthen author/research entity signals |
| English Generic vs Brand | 0 | 46 | 0% | 22.67 | Ranking gap; assess query fit |
| Bangla API | 0 | 37 | 0% | 6.00 | Low CTR at strong average position; snippet/answer refinement |
| Bangla QA vs QC | 0 | 37 | 0% | 7.46 | Low CTR at page-one average position; snippet/intent review |
| Bangla How Medicines Work | 0 | 37 | 0% | 14.35 | Internal-link and ranking support |
| Bangla Pharma Industry | 0 | 34 | 0% | 12.82 | Strengthen topic-cluster links |

The English and Bangla expiry pair together received **1,579 page impressions and 12 clicks** in the exported page table, a combined observed CTR of approximately **0.76%**. The page-table figures are not a complete sitewide total, but this pair is a clear optimisation candidate.

## 5. Query-level opportunities (Export A Queries.csv)

| Query | Clicks | Impressions | CTR | Avg. position | Action |
|---|---:|---:|---:|---:|---|
| sayedul abrar | 82 | 294 | 27.89% | 2.24 | Protect brand query and homepage/About distinction |
| মেয়াদ শেষ হওয়ার তারিখ | 0 | 195 | 0% | 9.83 | First Bangla non-brand opportunity |
| finix mups 20 | 0 | 42 | 0% | 3.43 | Review Finix MUPS page title, snippet and query intent |
| when to take iron tablets before or after food | 0 | 27 | 0% | 9.96 | Improve English iron article's direct answer and trust signals |
| drug distribution | 0 | 24 | 0% | 61.88 | Low ranking; build topic-cluster authority, not snippet-only edits |
| ড্রাগ ও মেডিসিনের পার্থক্য | 0 | 19 | 0% | 9.79 | Improve Bangla drug-vs-medicine snippet |
| api full form in pharma | 0 | 9 | 0% | 5.67 | Put exact full form in first answer |
| মেয়াদ উত্তীর্ণের তারিখ | 0 | 8 | 0% | 9.50 | Natural synonym; include only where useful |
| উৎপাদন তারিখ | 0 | 6 | 0% | 7.83 | Retain MFG terminology and explanation |
| expiry date and manufacturing date | 0 | 6 | 0% | 6.83 | Strengthen English expiry snippet |

### Brand and product-query protection
- The query “sayedul abrar” generated 82 clicks and 294 impressions in the exported query table.
- The homepage generated 76 clicks and 346 impressions; About generated 16 clicks and 219 impressions.
- Do not consolidate or delete Home, About, Learning, Achievements or Publications. Their purposes differ. Improve page roles and links without competing title tags or duplicated identity descriptions.
- “finix mups 20” showed 42 impressions at average position 3.43 with zero clicks; the Finix MUPS page showed 80 impressions at average position 4.90 with zero clicks. Review whether the snippet clearly answers the brand/product search and whether the page is the correct landing page. Keep employer/product claims accurate and professionally contextualised.

## 6. Question-query findings (Export B, filtered subset)

The filtered 28-day question-query export has only 71 impressions and one click. Its strongest query is:
- “when to take iron tablets before or after food” — 27 impressions, zero clicks, average position 9.96.

Other query examples have only 1–3 impressions each:
- “how to take iron properly” — 3 impressions, position 6.67.
- “is low iron and anemia the same thing” — 3 impressions, position 9.
- Half-life questions — generally positions 67–82.
- “what is api in chemical industry” — 1 impression, position 9.
- “how expiry date of medicine is determined” — 1 impression, position 11.

Actions:
- Iron tablets is the only clear question-query cluster in this filtered sample. Improve the first-screen answer to the food/timing question, while distinguishing iron salts and formulations and avoiding universal dosing advice.
- Half-life content has a ranking problem, not a snippet-only problem. Build contextual internal links from ADME, metabolism, excretion and bioavailability pages.
- Do not create new articles for one-impression queries. Add concise answers to the best-matching existing pages where they genuinely fit.

## 7. Prioritised execution backlog

### P0 — First actions
1. Refresh the Bangla expiry search snippet: retain the exact phrase “ওষুধের মেয়াদ শেষ হওয়ার তারিখ”, add EXP/MFG clarity and keep the DGDA source close to the relevant explanation.
2. Refresh the English expiry snippet: include EXP/MFG and practical pack-reading value. Do not rewrite its existing decoder/FAQ content without evidence.
3. Review the Bangla Drug vs Medicine title/description and opening answer: 197 impressions, zero clicks, average position 7.68.
4. Review the Finix MUPS landing-page snippet against “finix mups 20” and the 80 page impressions. Confirm the page answers the user's likely brand/product intent and has appropriate, accurate content.
5. Improve the English iron article's opening answer for “before or after food”; preserve formulation-specific safety qualifications.

### P1 — Next
6. Review Bangla API snippet and put “API = Active Pharmaceutical Ingredient” in the immediate answer.
7. Review Bangla QA vs QC snippet and clarify the practical distinction in the first paragraph.
8. Strengthen internal links across ADME and half-life content.
9. Inspect desktop search performance by query and country; compare actual desktop/mobile rendering before UI changes.
10. Check Bangladesh and India query/page differences separately.

### P2 — Authority and content architecture
11. Improve the Bangla Generic vs Brand page's snippet and label-reading answer.
12. Strengthen internal links among API, GMP, QA/QC, stability testing and Bangladesh pharma industry.
13. Add contextual links among iron tablets, iron deficiency vs anemia and medicine safety content.
14. Maintain the personal-brand query cluster with distinct, useful Home, About, Publications, Learning and Achievements pages.
15. Build future content only where multiple query/page signals support a clear unmet intent.

## 8. Proposed metadata tests — drafts only

These are candidates for a controlled manual update, not approved production edits.

### Bangla expiry
Suggested title:
`ওষুধের মেয়াদ শেষ হওয়ার তারিখ: EXP ও MFG বুঝুন | Sayedul Abrar`

Suggested description:
`ওষুধের EXP ও MFG তারিখ কীভাবে পড়বেন? 07/2027-এর অর্থ, ব্যাচ নম্বর, সংরক্ষণ এবং খোলার পর ব্যবহারের সময়সীমা DGDA নির্দেশনাসহ জানুন।`

### English expiry
Suggested title:
`Medicine Expiry Date: What EXP and MFG Mean | Sayedul Abrar`

Suggested description:
`Learn what EXP, MFG and batch numbers mean on medicine packs. Understand month/year expiry dates, use-after-opening limits and safe storage.`

### Bangla Drug vs Medicine
Suggested title:
`ড্রাগ ও মেডিসিনের পার্থক্য কী? সহজ উদাহরণে বুঝুন | Sayedul Abrar`

Suggested description:
`ড্রাগ ও মেডিসিন কি একই? WHO-এর পরিভাষা, বাংলাদেশের আইন এবং সহজ উদাহরণে drug, medicine ও pharmaceutical product-এর পার্থক্য জানুন।`

### Finix MUPS landing page
Do not rewrite the page until its current live title, meta description, page content and query list have been checked together. The query “finix mups 20” may be looking for a specific strength/formulation or product information. Ensure title and description match the actual page and avoid unsupported superiority or clinical claims.

## 9. Measurement plan

For every approved metadata/content change:
1. Record exact URL, old title/description, new title/description, change date and reason.
2. Capture a pre-change GSC baseline by page and query, with Bangladesh and device filters where useful.
3. Change one meaningful variable at a time where practical.
4. Allow Google to recrawl; do not expect immediate results.
5. Compare matched 28-day windows after enough data accumulates. Use clicks, impressions, CTR and average position together.
6. Check whether clicks increased for the intended query cluster, not just whether average position moved.
7. Revert only if evidence shows a sustained deterioration and the change is plausibly responsible.

## 10. Completion checklist and guardrails

- [x] Opened and inspected both uploaded ZIP exports.
- [x] Read all seven CSVs from each export.
- [x] Recorded filter/date coverage and dimension-total inconsistencies.
- [x] Analysed chart, page, query, country and device data.
- [x] Identified high-impression, low-CTR page and query opportunities.
- [x] Prioritised work by impressions, position, clicks and search intent.
- [x] Drafted three metadata test candidates.
- [ ] Obtain a true full three-month export with all daily rows and matching query/page dimensions.
- [ ] Obtain an unfiltered full 28-day export to complement the question-query subset.
- [ ] Re-check current live page metadata before implementing changes.
- [ ] Complete live HTTP, canonical, hreflang and structured-data validation.
- [ ] Obtain explicit author approval for the exact production changes.
- [ ] Publish manually through GitHub only after approval.

**Final safeguard:** This work is an evidence-based SEO action plan. It does not assert that rankings have definitively fallen, that a Google penalty exists, or that a specific technical issue caused the observed performance. No production content has been changed.
