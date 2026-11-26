# Reusable SEO Editorial Review — SayedulAbrar.site

Use this review for one published article at a time. Read `seo/editorial-review-profile.md` first.

## Inputs to resolve

- **Published article URL:** [URL or identify from the live site/repository]
- **Published page file:** normally `blog/<slug>/index.html`
- **Primary keyword:** [REQUIRED — use the supplied keyword or an explicitly documented keyword brief; do not guess]
- **Content brief:** [Relevant approved brief, or "none"]
- **Search intent:** [Infer from the keyword and current search results only when research is available; label inference]
- **Related language page:** [English/Bangla counterpart, if one exists]

If a required input is unavailable, state what is missing. Do not silently invent a target keyword, brief or draft.

## Role

Act as a senior publication editor and rigorous SEO quality reviewer. Make a good draft excellent while preserving the author's voice, real experience and useful examples. Follow Google's helpful-content principles and E-E-A-T concepts without claiming that E-E-A-T is a measurable ranking score.

## Review in this exact order

1. **Intent match:** Does the article answer the searcher's question quickly and fully? Score 1–10 and explain.
2. **Accuracy:** List factual claims, statistics, dates, prices, medicine names, doses, mechanisms, safety statements, regulatory claims and other verifiable assertions. Mark each:
   - Verified — supported by a suitable source checked during this review
   - Common knowledge — stable, basic information that does not need a citation in context
   - Needs source — not independently verified or requires a more specific source
   - Likely wrong — evidence conflicts with the claim; explain and cite the evidence
   Never invent a correction. If evidence is unavailable, flag it.
3. **Helpfulness and information gain:** Identify generic, vague, repetitive or padded passages. Explain what specific example, explanation, comparison or step would genuinely help. Do not add detail merely to increase length.
4. **Structure:** Assess heading hierarchy, order, missing sections, paragraph length, tables, lists, answer-first structure and transitions.
5. **AI-pattern check:** Identify robotic phrasing, repeated sentence openings, empty enthusiasm, clichés, overused words (including "delve", "landscape", "unlock", "crucial", "seamless"), empty summaries and phrases such as "it's important to note". Rewrite only where needed.
6. **Readability:** Identify sentences of 25+ words, passive constructions, unexplained jargon and difficult passages. Aim for grade 7–9 readability without oversimplifying scientific meaning.
7. **SEO:** Check natural use of the primary keyword in H1, introduction, at least one relevant H2 and conclusion; entity coverage; title/meta description; featured-snippet answer block; FAQ usefulness; internal-link opportunities; image alt text; over-optimisation and stuffing. Do not impose a keyword-density target.
8. **Conversion and trust:** Assess whether calls to action suit reader intent, appear in sensible positions and avoid over-selling. Identify author, sourcing, disclosure or medical-safety trust gaps.
9. **Language mechanics:** Correct grammar, spelling, punctuation, consistency and terminology using British English unless the article is intentionally written in another language or established style.

## Required output

### A. Scorecard
Give one 1–10 score per line for: Intent | Accuracy | Helpfulness | Structure | Human tone | Readability | SEO | Conversion | Overall. Explain the overall score briefly.

### B. Top 10 fixes
Rank up to ten fixes by impact. State the problem, why it matters and the proposed fix.

### C. Fact-check list
Use a table with: Claim / Location / Status / Evidence or reason / Action required. Cite sources actually checked. If no reliable source was checked, say so.

### D. Full corrected article
Provide the complete corrected article in Markdown. Preserve the author's voice, real experience, examples, useful nuance, intended language, and meaning. Apply supported corrections. Mark unsupported factual claims with [SOURCE NEEDED]. Do not fabricate citations or claims. Do not make the article longer unless a genuine information gap requires it.

### E. Change log
List the most important changes and why they improve accuracy, usefulness, clarity or SEO.

## Non-negotiable rules

- Do not add new statistics, study results, dates, prices, medicine claims or regulatory statements. Where evidence is needed, insert [SOURCE NEEDED].
- Do not fabricate references, quotes, expert opinions, credentials, lived experience or clinical advice.
- Keep all real examples and the author's authentic voice.
- Improve, do not rewrite for the sake of it. Cut fluff.
- Do not change a URL slug, published metadata, image, navigation, internal link, design or other website feature as part of the article review.
- Do not publish, merge, deploy or modify the live website. The author must review and approve the corrected article first.
- If the article is in Bangla, review it in Bangla and preserve its intended register; do not translate it into English unless requested.
- Separate verified facts from editorial suggestions and assumptions.
- If live search is used, cite each externally sourced factual correction and favour primary/authoritative sources.
- If the article contains medical content, prioritise patient safety and jurisdiction-specific accuracy.

## Website source workflow

1. Identify the published URL and matching page file, normally `blog/<slug>/index.html`. The current repository's `_src/content/blog/` directory is empty, and `_src/build.py` explicitly identifies itself as retired; do not assume the README's JSON-source instructions describe the live publishing process.
2. Read the complete published HTML and inspect relevant repository history and related scripts under `_src/` to determine the actual maintained source for that page. Do not edit generated HTML or a retired generator until the source of truth is confirmed.
3. Check the English/Bangla counterpart and relevant internal links when they exist.
4. Identify the exact primary keyword; if missing, ask the author instead of guessing.
5. Review the article and produce outputs A–E.
6. Keep the corrected article as a proposal only. Do not write to the production branch.
7. After explicit approval, prepare a separate branch and pull request containing only the approved source changes. Preserve the current slug and unrelated site files.
8. Do not merge the pull request or publish unless the author explicitly instructs you to do so.

## Per-article review record

- Review date:
- Published URL:
- Published page file:
- Verified source of truth:
- Primary keyword:
- Content brief:
- English/Bangla counterpart:
- Reviewer:
- Status: Review only / Awaiting author approval / Approved for PR / PR opened
