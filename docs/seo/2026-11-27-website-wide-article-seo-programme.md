# Website-Wide Article SEO & Competitor Improvement Programme
**Website:** https://sayedulabrar.site  
**Repository:** sayedulabrarsa-beep/sayedulabrarsa-beep.github.io  
**Working branch:** `seo-audit-2026-11-27`  
**Baseline:** main branch at the previously verified baseline; production remains untouched.  
**Scope:** All 58 article-language URLs (29 English/Bangla topic pairs) in the 27 November 2026 sitemap.

## Operating rules
1. Inspect each live URL and its corresponding repository source before proposing changes.
2. Use Search Console page/query/device/country evidence where available; label missing data instead of guessing.
3. Research the actual Bangladesh SERP and relevant competitors for each topic. Record positions only when measured in a specified location, device, query and date.
4. Compare topic coverage, examples, proof, formats, freshness, SEO, UX and reader next steps.
5. Preserve existing strong material, author voice, bilingual pairing, design system, navigation, URLs, canonical and hreflang.
6. Recommend only medically/pharmaceutically accurate additions supported by reliable references.
7. Never copy competitor wording or invent data, claims, quotes, ranking positions or first-hand experience.
8. Avoid mass metadata rewrites, keyword stuffing and thin/duplicative sections.
9. Work in the SEO branch only. Do not merge to main, publish, or alter production until the author explicitly approves the exact before/after patch.
10. Never run the retired `_src/build.py` or blindly run `_src/seo_meta_tune.py`.

## Standard per-article deliverable
For each article, create one audit file containing:
- URL, language, topic, current metadata and last-modified information.
- Search Console performance and query intent, including export/date/filter caveats.
- Full-page structure and content inventory.
- Five or fewer relevant competitor pages, their verified content coverage and any measurable SERP positions.
- Coverage matrix (Me / C1–C5; Deep / Brief / Missing).
- Gaps grouped into content, proof, format, freshness, SEO, UX and reader engagement.
- Competitor weaknesses and the article's existing strengths to preserve.
- Impact/effort-ranked action list.
- Up to three publication-ready sections only where genuine gaps exist.
- Metadata recommendation (change only when evidence warrants it).
- Internal-link recommendations and factual/source checks.
- Exact proposed patch and explicit approval status.

## Sitemap inventory — 29 topic clusters / 58 article-language URLs
1. When to take PPI before meals (EN/BN)
2. How to take iron tablets properly (EN/BN)
3. Iron deficiency vs anaemia (EN/BN)
4. Drug vs Medicine (EN/BN)
5. Expiry date vs manufacturing date (EN/BN)
6. Generic name vs brand name (EN/BN)
7. Heartburn vs acid reflux vs GERD (EN/BN)
8. Glucosamine and Alzheimer's research review (EN/BN)
9. What is the pharmaceutical industry (EN/BN)
10. How medicines work in the body (EN/BN)
11. Why complete an antibiotic course / antibiotic resistance (EN/BN)
12. Drug absorption (EN/BN)
13. Drug distribution (EN/BN)
14. Active pharmaceutical ingredient (API) (EN/BN)
15. Good manufacturing practices (GMP) (EN/BN)
16. Quality assurance vs quality control (EN/BN)
17. Medicine stability testing / shelf life (EN/BN)
18. Pharmacovigilance (EN/BN)
19. Biosimilars (EN/BN)
20. PPI / acid medicine market in Bangladesh (EN/BN)
21. Pharmaceutical product management in Bangladesh (EN/BN)
22. Clinical trial phases (EN/BN)
23. Pharmaceutical marketing strategy in Bangladesh (EN/BN)
24. Pharmacogenetics (EN/BN)
25. Drug metabolism (EN/BN)
26. Drug excretion (EN/BN)
27. Drug half-life (EN/BN)
28. Bioavailability (EN/BN)
29. Prescription vs OTC medicines in Bangladesh (EN/BN)

The blog landing page is an additional discovery/index URL and will be reviewed separately for topic architecture and internal linking, not counted as an article.

## Initial priority order
This is a provisional order from the supplied GSC exports and known query/page observations. Refresh it when full page/query exports are available.

**Tier 1 — demonstrated visibility or CTR opportunity**
1. Expiry date vs manufacturing date (EN + BN): 1,579 combined impressions, 12 clicks in the supplied page export; EN CTR 0.38%, BN CTR 1.14%.
2. Drug vs Medicine (BN): 197 impressions, 0 clicks, average position 7.68.
3. Generic name vs brand name (BN): 166 impressions, 2 clicks, average position 7.53.
4. How to take iron tablets (EN): 145 impressions, 0 clicks, page average position 21.34; query-specific "when to take iron tablets before or after food" 27 impressions, position 9.96.
5. Finix MUPS product guide: 80 impressions, 0 clicks, average position 4.90; query "finix mups 20" 42 impressions, position 3.43. Product page, not one of the 58 articles; audit separately and keep factual/independent framing.

**Tier 2 — strategic clusters and internal-link hubs**
6. Heartburn / acid reflux / GERD (EN + BN)
7. PPI timing (EN + BN)
8. Iron deficiency vs anaemia (EN + BN)
9. Drug absorption, distribution, metabolism, excretion, half-life and bioavailability (ADME learning cluster)
10. API, GMP, QA vs QC, stability testing and pharmacovigilance (manufacturing/quality cluster)

**Tier 3 — remaining topic clusters**
11. Generic name vs brand name (EN)
12. Drug vs Medicine (EN)
13. Antibiotic course / resistance (EN + BN)
14. Pharmaceutical industry (EN + BN)
15. Medicines work in body (EN + BN)
16. Biosimilars (EN + BN)
17. PPI market (EN + BN)
18. Product management (EN + BN)
19. Clinical trials (EN + BN)
20. Marketing strategy (EN + BN)
21. Pharmacogenetics (EN + BN)
22. Glucosamine research review (EN + BN)
23. Prescription vs OTC (EN + BN)
24. Remaining individual pages and bilingual parity checks.

## Search Console interpretation guardrails
- The main supplied export says "Last 3 months" but its chart rows cover only 31 days (25 Oct–24 Nov 2026); use the actual rows, not the filter label.
- Page and query tables do not reconcile with chart totals; country rows do. Treat page/query tables as partial exports, not site-wide totals.
- The second export is a filtered question-query sample with only 71 impressions and 1 click; it is not a site-wide benchmark.
- Early October 26–November 1 click spike may be an outlier/branded-query effect. Do not call an algorithmic penalty or site-wide demotion from this evidence.
- Desktop/mobile average-position differences require query-mix and rendering analysis, not an automatic redesign.
- Track future comparisons with consistent date windows, search type, country, device and filters.

## Progress ledger
- [x] Sitemap inventory: 59 blog URLs = blog landing page + 58 article-language URLs.
- [x] English expiry competitor review and proposed content gaps documented in conversation; no live edit.
- [x] Website-wide inventory and workflow documented here.
- [ ] Bangla Drug vs Medicine competitor audit — in progress.
- [ ] Remaining 56 article-language URLs — pending individual review.
- [ ] Blog landing page architecture review — pending.
- [ ] Full Search Console refresh and consistent baseline — pending.

## Completion standard
The programme is complete only when every article-language URL has an individual audit and a decision (change / preserve / monitor), every recommended change has supporting evidence, all proposed copy is source-checked, and the author has reviewed the complete patch set. Completion of audits does not mean automatic publication.
