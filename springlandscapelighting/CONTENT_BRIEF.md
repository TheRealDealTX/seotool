# Content brief — springlandscapelighting.com rebuild

You are writing body content for a custom PHP site for **Spring Landscape Lighting**, a
landscape lighting design / installation / repair company serving Spring, TX and nearby
North Houston communities (Spring, Klein, Champion Forest, Gleannloch Farms, Augusta Pines,
The Woodlands). Phone (281) 704-7210, email info@springlandscapelighting.com.
They design and install professional low-voltage LED systems, do repairs, halogen→LED
upgrades and smart controls. The brand voice: calm, expert, design-led, restrained
("great lighting is not about adding the most fixtures… it is about where darkness should
remain"). Homeowner audience.

Reference copy from the old site is in `backup-wordpress/*.txt` (read it for tone and facts).
Business data and the list of every page/post slug is in `public_html/app/config.php`.

## File format

Each file is a PHP fragment that outputs HTML. First line must be exactly:

```php
<?php defined('SLT') || exit; ?>
```

Then plain HTML. Do NOT output `<h1>`, page hero, breadcrumbs, or wrapper `<article>` —
the template adds those. Start with `<p class="lead">…</p>`.

## Components you can use (styled already)

- `<p class="lead">` — opening paragraph (one per file)
- `<h2>` sections (posts get an auto table of contents from h2s — keep h2 text short) and `<h3>`
- `<div class="callout"><strong>Tip:</strong> text</div>` (also `callout callout--warn`)
- `<div class="takeaways"><h3>Key takeaways</h3><ul><li>…</li></ul></div>`
- `<div class="table-wrap"><table><thead>…</thead><tbody>…</tbody></table></div>`
- `<ol class="steps"><li><strong>Step title.</strong> text</li>…</ol>`
- `<div class="grid-cards"><div class="mini-card"><h3>Title</h3><p>text</p></div>…</div>` (2–4 cards)
- `<blockquote class="pull">A short memorable line.</blockquote>`
- `<?php cta_box('Heading', 'One or two sentences.'); ?>` — a quote/consultation call to action box. Use once, mid or late.
- `<?php tool_embed('SLUG'); ?>` — embeds a working interactive tool. SLUG one of:
  `energy-cost-calculator`, `led-savings-calculator`, `transformer-sizing-calculator`,
  `color-temperature-guide`, `fixture-estimator`. Use only where genuinely relevant (max one per file).
- `<?php faq_block([['Question?', 'Answer text.'], …]); ?>` — renders an FAQ accordion and
  FAQPage schema. Put it LAST in the file, 4–6 questions. Answers are plain text (no HTML),
  use single quotes for the PHP strings and escape apostrophes as `\'`.

## Internal links (use real ones, 4–8 per file, descriptive anchor text)

Services: `/services/architectural-lighting/`, `/services/pathway-driveway-lighting/`,
`/services/tree-garden-lighting/`, `/services/patio-pool-lighting/`,
`/services/smart-lighting-controls/`, `/services/landscape-lighting-repair/`, hub `/services/`
Tools: `/tools/lighting-visualizer/`, `/tools/energy-cost-calculator/`, `/tools/fixture-estimator/`,
`/tools/transformer-sizing-calculator/`, `/tools/led-savings-calculator/`,
`/tools/color-temperature-guide/`, `/tools/sunset-timer-planner/`
Pages: `/quote/`, `/our-process/`, `/faq/`, `/about-us/`, `/inspiration/`, `/contact/`, `/service-areas/`
Areas: `/service-areas/spring-tx/`, `/service-areas/klein-tx/`, `/service-areas/champion-forest/`,
`/service-areas/gleannloch-farms/`, `/service-areas/augusta-pines/`, `/service-areas/the-woodlands-tx/`
Posts (root-level): `/electricity-landscape-lighting-use/`, `/landscape-lighting-cost-spring-tx/`,
`/landscape-lighting-techniques/`, `/warm-white-vs-cool-white-landscape-lighting/`,
`/path-light-spacing/`, `/tree-uplighting-guide/`, `/landscape-lighting-transformer-sizing/`,
`/halogen-to-led-landscape-lighting/`, `/landscape-lighting-maintenance-checklist/`,
`/landscape-lighting-for-home-security/`

## Rules

- Mention the brand "Spring Landscape Lighting" naturally 2–4 times per file.
- Genuinely useful, specific, expert content. Concrete numbers where they are general
  industry knowledge (e.g. LED fixtures ~2–12 W, halogen 20–50 W, 12 V systems, 80% transformer
  rule, 2700K/3000K norms, wire gauge resistance), hedged where they vary.
- Local relevance: Gulf Coast heat & humidity, heavy rain/flooding, St. Augustine lawns,
  irrigation, live oaks / loblolly pines / crape myrtles / palms, brick & stone elevations,
  HOAs and deed restrictions, fast plant growth, hurricane-season storms.
- NEVER invent: testimonials, reviews/ratings, years in business, number of projects,
  licenses/certifications, warranties, street addresses, staff names, awards, or specific
  company prices. Don't claim specific facts about a neighborhood unless you're confident
  they are true; keep neighborhood descriptions general and hedged ("many homes in…").
- US spelling. Write like a human expert: varied sentence length, no fluff, no
  "In today's world", no "Whether you're…, …" openers, minimal em dashes (prefer commas,
  periods, colons). Avoid listicle filler.
- Valid HTML, properly closed tags. Run `php -l` on each file you write.
