# Arrive Outdoors — article format and writing standard

Every article is one file: `content/articles/<slug>.html`, where `<slug>` is the
URL path without slashes at the ends (nested legacy slugs use `__` in the file
name: `blogs__the-outdoor-traveler__camping-101-a-guide-for-the-first-time-camper.html`).

## File format

The file starts with a metadata block, then the article body as an HTML fragment.

```html
<!--meta
{
  "title": "Class 3 Scramble: What It Is, Gear, Safety & First Routes",
  "description": "150–160 char meta description that states the payoff.",
  "h1": "Class 3 Scramble: The Sweet Spot Between Hiking and Climbing",
  "keyword": "class 3 scramble",
  "category": "hiking",
  "published": "2025-09-16",
  "updated": "2026-10-31",
  "summary": "One or two sentences shown on cards and as the article's dek.",
  "related": ["class-4-scramble", "can-you-hike-el-capitan"],
  "tools": ["hiking-time-calculator", "trail-weather"],
  "destinations": ["yosemite"],
  "faq": [
    {"q": "Do you need a rope for class 3?", "a": "Usually not..."}
  ]
}
-->
<p class="lead">Opening paragraph...</p>
<h2 id="what-is-class-3">What counts as class 3</h2>
<p>...</p>
```

Rules for the metadata:

- `category` is one of: `camping`, `hiking`, `backpacking`, `skills`, `gear`, `rentals`, `places`.
- `published`: keep the original WordPress date for rewritten posts (it is in
  `source-archive/index.tsv`); use `2026-10-31` for new posts. `updated` is `2026-10-31`.
- `related` (2–4) are other article slugs from `siteconfig.ARTICLES`.
- `tools` (1–3) are tool slugs from `siteconfig.TOOLS`; `destinations` (0–3) are destination slugs from `siteconfig.DESTINATIONS`.
- `faq`: 3–5 real questions people search, short factual answers (plain text, no HTML). Rendered as an FAQ section with FAQPage schema, so don't also write an FAQ section in the body.
- Valid JSON (double quotes, no trailing commas).

Rules for the body:

- Do **not** include the H1, the date, the byline, the affiliate disclosure, a
  table of contents, or an FAQ section — the template adds all of those.
- Every `<h2>` must have a unique, short, kebab-case `id` (used for the table of contents). Use `<h3>` freely under them (no id needed).
- Allowed markup: `p` (first one `class="lead"`), `h2`, `h3`, `ul`, `ol`, `li`,
  `strong`, `em`, `a`, `table` / `thead` / `tbody` / `tr` / `th` / `td` (wrap in
  `<div class="table-wrap">`), `blockquote`, and these callouts:
  - `<div class="callout tip"><strong>Tip:</strong> ...</div>`
  - `<div class="callout warn"><strong>Safety:</strong> ...</div>`
  - `<div class="callout tool">Try it: <a href="/tools/packing-list/">Packing List Generator</a> builds this checklist for your trip.</div>`
- No images, no inline styles, no scripts, no `<h1>`.
- Internal links: root-relative with trailing slash, e.g. `/class-4-scramble/`,
  `/tools/trail-weather/`, `/destinations/zion/`, `/weather/`, `/gear/`,
  `/rent-camping-gear/`. Link to 3–8 internal pages per article, where they genuinely help.
  Only link to URLs that exist in `siteconfig.py` (ARTICLES, TOOLS, DESTINATIONS,
  `/weather/<month>/` for months, `/gear/`, `/guides/`, `/about/`).
- External links: only to authoritative sources (nps.gov, fs.usda.gov, recreation.gov,
  weather.gov, cdc.gov, smokeybear.com, lnt.org, manufacturer pages). Plain `<a href="https://...">`.
- Amazon links: **never invent an ASIN.** You may reuse a `https://www.amazon.com/dp/<ASIN>/?tag=arriveoutdoors-20`
  link that appears in the source article *for the same product named the same way*. For any
  other product or a generic item, use a search link:
  `https://www.amazon.com/s?k=<url-encoded+query>&tag=arriveoutdoors-20`. Add
  `rel="sponsored nofollow"` to every Amazon link. Keep it to the products that actually help the reader
  (typically 2–8 per article); never make shopping the point of a section.

## Writing standard

The old posts read like generic AI filler. The rewrite has to be clearly better:

- Answer the search intent in the first 2–3 sentences (the `lead` paragraph).
- Specific over generic: numbers, temperatures, distances, weights, named routes,
  named techniques, real decision rules ("if X, do Y"). Cut every sentence that
  could appear in any article ("Whether you're a seasoned hiker or a beginner...",
  "In this guide we'll explore...", "Nature is calling...").
- No first-person experience claims ("I tested", "on my last trip", "we spent
  a week"). There is no named author yet, so write in a confident second-person
  guide voice. Don't invent testing, quotes, statistics or studies. Only state
  facts you are confident are accurate and stable; for things that change
  (fees, permit systems, reservation windows, prices, current deals) describe how it works and point to the official source
  instead of quoting a number or date.
- Safety content must be correct and conservative (fire, getting lost, scrambling,
  water treatment, cold, heat). When in doubt, say less and cite the agency.
- US spelling, imperial units first with metric in parentheses where useful.
- Length: whatever fully answers the query — usually 1,200–2,000 words. Use a
  table or checklist where it helps someone decide or act.
- Each article should naturally point to the relevant interactive tool with a
  `callout tool` (that's the site's differentiator).
- Title (meta `title`) ≤ 60 chars where possible, includes the keyword near the front.
