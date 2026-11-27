# Minimal-Change SEO Implementation Review — 27 November 2026

**Website:** https://sayedulabrar.site/  
**Branch:** `seo-audit-2026-11-27`  
**Purpose:** Apply the user's instruction to make only necessary changes and avoid unnecessary design or layout changes.  
**Production status:** Review document only. No live HTML, CSS, JavaScript, article body, URL, design, navigation or published content changed.

## Decision

Do not perform a blanket metadata rewrite. The current page source already contains relevant, descriptive titles and descriptions on several high-opportunity URLs. Search Console's low CTR is a reason to investigate the exact query/SERP presentation and content match, not proof that every title is wrong.

Keep the current design, colours, typography, hero images, article sections, interactive elements, navigation, URLs, canonical tags and hreflang structure unchanged.

## Page-by-page decisions

### 1. English expiry / manufacturing-date article

URL: https://sayedulabrar.site/blog/expiry-date-vs-manufacturing-date-medicine/

Current source metadata observed:
- Title: `Expiry Date vs Manufacturing Date on Medicine: EXP vs MFG`
- Description: `What do EXP and MFG mean on medicine? Learn how to read expiry dates, why 07/2027 means 31 July, and how to check batch numbers and storage.`

GSC export: 788 impressions, 3 clicks, 0.38% CTR, average position 7.97 (page-dimension export).

Decision:
- The title already contains the main subject and EXP/MFG terminology. Do not replace it just to force a different keyword order.
- The description is clear and specific. Retain it for now; test the exact Google-rendered snippet and query mix before changing it.
- If a small content edit is later approved, improve only the first-screen answer and make the distinction between printed expiry and shorter in-use shelf life immediately clear. Do not rebuild the article or duplicate its existing DGDA section.

### 2. Bangla expiry / manufacturing-date article

URL: https://sayedulabrar.site/blog/expiry-date-vs-manufacturing-date-medicine-bangla/

GSC export: 791 impressions, 9 clicks, 1.14% CTR, average position 7.38.

Decision:
- Keep the existing article URL and overall structure.
- Preserve the exact high-intent Bangla wording “মেয়াদ শেষ হওয়ার তারিখ” naturally in the title/opening answer if it is already present; do not stuff synonyms.
- Before changing metadata, inspect the exact current title/description and live Google snippet. The earlier proposed title is only a candidate, not an automatic replacement.
- If an edit is needed, make a one-sentence opening-answer improvement and a precise snippet adjustment only.

### 3. Bangla Drug vs Medicine

URL: https://sayedulabrar.site/blog/drug-vs-medicine-bangla/

Current source metadata observed:
- Title: `ড্রাগ ও মেডিসিনের পার্থক্য: সহজ উদাহরণে বুঝুন | Sayedul Abrar`
- Description: `ড্রাগ ও মেডিসিনের পার্থক্য কী? সহজ উদাহরণ, তুলনামূলক ছক, WHO-এর সংজ্ঞা ও বাংলাদেশের আইনের আলোকে ফার্মাসিস্টের ব্যাখ্যা পড়ুন।`

GSC export: 197 impressions, 0 clicks, average position 7.68.

Decision:
- Metadata already matches the query topic and communicates a useful differentiator.
- Do not change the title merely to add “কি” or repeat the query.
- Inspect actual search appearance and ensure the opening paragraph answers whether the terms are identical in context, without claiming an absolute universal distinction.
- Consider only a concise opening-answer refinement and relevant internal links from the English/Bangla generic-vs-brand and medicine-label articles.

### 4. Bangla Generic Name vs Brand Name

URL: https://sayedulabrar.site/blog/generic-name-vs-brand-name-bangla/

GSC export: 166 impressions, 2 clicks, average position 7.53.

Decision:
- Retain page URL and article design.
- Inspect exact current metadata and the live result before editing.
- Prioritise a clear first-screen explanation of generic name versus brand name and a contextual link to the medicine-label guide. Avoid duplicating the same explanation across articles.

### 5. English iron-tablet article

Likely relevant URL from repository source: https://sayedulabrar.site/blog/how-to-take-iron-tablets-properly/

GSC export page observation: 145 impressions, 0 clicks, average position 21.34. Question-query export: “when to take iron tablets before or after food” had 27 impressions, 0 clicks, average position 9.96.

Decision:
- This is not a title-only CTR problem; page-level average position is materially weaker.
- Keep the article's clinical qualifications and formulation-specific advice.
- If approved, improve the direct answer to the food/timing question near the beginning, then link to the iron-deficiency-vs-anemia article.
- Do not make a universal dosing recommendation or imply all iron products have identical instructions.

### 6. Finix MUPS 20 product information page

URL: https://sayedulabrar.site/brands/finix-mups/

Current source metadata observed:
- Title: `Finix MUPS 20 mg: Rabeprazole Product Guide | Sayedul Abrar`
- Description: `Independent guide to Finix MUPS 20 mg (rabeprazole sodium) by Opsonin Pharma: MUPS formulation, product details, uses and common questions.`

GSC export: 80 impressions, 0 clicks, average position 4.90. Query “finix mups 20”: 42 impressions, average position 3.43.

Decision:
- Current title and description are already descriptive and factual.
- Do not add “fastest”, “number one”, superiority, or unsupported efficacy claims.
- Check the live search result, product image preview and query mix before any snippet change.
- Keep the independent educational framing and manufacturer-source links. No promotional redesign or new claims.

## Small, safe improvements to consider after live verification

1. Verify the exact title and description currently served by the live URL, not only source files.
2. Compare the actual Google snippet with the page title/description for the two expiry pages and Bangla Drug vs Medicine.
3. Check whether the page's first visible answer directly satisfies the query without scrolling.
4. Add only contextual internal links where they help the reader continue: expiry ↔ medicine-label guide; generic vs brand ↔ medicine-label guide; iron tablets ↔ iron deficiency vs anemia.
5. Inspect desktop/mobile rendering and page speed before considering any visual or CSS changes.
6. Record each approved edit and its baseline; change one meaningful element at a time.

## Explicitly out of scope

- No redesign, theme, colour, font, spacing or layout changes.
- No navigation or homepage changes.
- No URL, slug, canonical or hreflang changes.
- No mass title/description rewrite.
- No deletion, merging or rewriting of existing articles.
- No unsupported clinical or comparative product claims.
- No automatic publishing or merging to `main`.

## Approval gate

This review is not approval to publish. Any production edit must be shown as an exact before/after change and approved by the author. Publish manually only after that approval.
