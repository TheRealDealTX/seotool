# Content fragment format — txlandscapelights.com

Every page body lives in one `.html` fragment under `content/<group>/<slug>.html`.
`build.py` wraps it in the shared layout (header, page hero with H1 + breadcrumbs,
quote form, CTA band, footer, schema). Write **only the fragment**.

## Brand facts (use exactly; never invent others)

- Business: **Texas Landscape Lights** — custom low-voltage LED landscape lighting design,
  installation, repair and upgrades for homes (and select commercial properties) across Texas.
- Phone: **(281) 704-7210** → `<a href="tel:+12817047210">(281) 704-7210</a>`
- Email: **info@txlandscapelights.com**
- Free lighting consultation / night demo; written proposal; final adjustment visit after dark.
- Do NOT invent: street addresses, years in business, number of projects, review counts or
  star ratings, testimonials, named staff, license numbers, awards, specific warranty terms,
  brand partnerships. Price figures must be framed as typical planning ranges, not quotes.
- Line-voltage electrical work (new outlets/circuits) is handled by a licensed electrician;
  the lighting system itself is 12V low-voltage.
- US spelling. Plain, confident, helpful voice. Short paragraphs. No fluff, no
  "in today's world", no "look no further". Avoid em dashes (use commas, colons, periods).

## File structure

The first line is a metadata comment holding one JSON object, then the HTML body:

```html
<!--meta {"title": "...", "description": "...", "h1": "...", "eyebrow": "...", "lede": "...", "faqs": [["Question?", "Answer."]]} -->
<div class="prose">
  <h2>…</h2>
  <p>…</p>
</div>
```

Metadata keys:

| key | required | notes |
| --- | --- | --- |
| `title` | yes | SEO `<title>`, 50–62 chars, primary keyword near the front. Do NOT add the brand; build.py appends nothing. Write the whole title, e.g. `Landscape Lighting in Houston, TX \| Texas Landscape Lights` |
| `description` | yes | meta description, 140–158 chars, includes keyword + a reason to click |
| `h1` | yes | on-page H1 (contains the primary keyword) |
| `eyebrow` | yes | 2–4 word kicker shown above the H1 |
| `lede` | yes | 1–2 sentence intro shown under the H1 (plain text, no HTML) |
| `faqs` | yes for services/areas/blog | 4–6 `[question, answer]` pairs, answers 1–3 sentences, plain text. Rendered as accordion + FAQPage schema. Don't repeat them in the body. |
| `keyword` | yes | the primary keyword string |
| `category` | blog only | one of `guides`, `design-ideas`, `maintenance` |
| `excerpt` | blog only | 1 sentence for cards |
| `date` | blog only | ISO date, use dates between 2026-08-04 and 2026-10-14 |

## Components (CSS already exists for these — use them, don't add inline styles)

- `<div class="prose">…</div>` — long-form wrapper. Use `h2`, `h3`, `p`, `ul`, `ol`, `blockquote`, `strong`, links.
  Body content can be split into several `.prose` blocks with components between them.
- `<div class="table-wrap"><table>…</table></div>` — data tables (thead/tbody). Inside or outside prose.
- `<div class="callout"><p><strong>Tip:</strong> …</p></div>` — amber note. `callout callout--rust` for warnings.
- `<ul class="checks"><li>…</li></ul>` — checkmark list.
- `<div class="cards cards--3">` (or `cards--2`, `cards--4`) containing
  `<article class="card"><span class="card__k">01</span><h3>…</h3><p>…</p></article>`
  (`card__k` optional — a small kicker such as a number or label).
- `<div class="split"><div>…</div><div>…</div></div>` — two columns (prose inside each is fine).
- `<div class="facts"><div class="fact"><b>2700K</b><span>most-requested color temperature</span></div>…</div>` — 3–4 big numbers. Only real, general facts (no invented company stats).
- `<ol class="steps"><li><h3>…</h3><p>…</p></li></ol>` — numbered process.
- `<div class="art" data-art="NAME"></div>` — build.py swaps in an illustrated night-lighting SVG.
  NAME is one of: `facade`, `path`, `tree`, `patio`, `pool`, `controls`, `repair`, `commercial`, `city`.
  Use 1–2 per page, e.g. inside one side of a `.split`.
- `<p><a class="btn" href="/quote/">Get my free lighting plan</a></p>` — inline CTA button (use at most once).

Do NOT include: `<h1>`, the page hero, breadcrumbs, a quote/contact form, a final CTA band,
an FAQ section, `<script>`, `<style>`, or images. build.py adds those.

## Site map (link internally with these exact paths, 4–8 contextual links per page)

- `/` home, `/services/`, `/service-areas/`, `/tools/`, `/blog/`, `/about-us/`, `/our-process/`,
  `/faq/`, `/inspiration/`, `/contact/`, `/quote/`
- Services: `/services/architectural-lighting/`, `/services/pathway-driveway-lighting/`,
  `/services/tree-garden-lighting/`, `/services/patio-pool-lighting/`,
  `/services/smart-lighting-controls/`, `/services/landscape-lighting-repair/`,
  `/services/commercial-landscape-lighting/`
- Areas: `/service-areas/houston-tx/`, `/service-areas/dallas-tx/`, `/service-areas/austin-tx/`,
  `/service-areas/san-antonio-tx/`, `/service-areas/fort-worth-tx/`, `/service-areas/plano-tx/`,
  `/service-areas/frisco-tx/`, `/service-areas/the-woodlands-tx/`, `/service-areas/katy-tx/`,
  `/service-areas/sugar-land-tx/`, `/service-areas/round-rock-tx/`, `/service-areas/new-braunfels-tx/`
- Tools: `/tools/lighting-visualizer/`, `/tools/energy-cost-calculator/`, `/tools/fixture-estimator/`,
  `/tools/transformer-sizing-calculator/`, `/tools/led-savings-calculator/`,
  `/tools/color-temperature-guide/`, `/tools/sunset-timer-planner/`
- Blog (all under `/blog/<slug>/`): `landscape-lighting-cost-texas`, `best-landscape-lighting-for-texas-heat`,
  `landscape-lighting-techniques`, `warm-white-vs-cool-white-landscape-lighting`, `path-light-spacing`,
  `tree-uplighting-guide`, `landscape-lighting-transformer-sizing`, `halogen-to-led-landscape-lighting`,
  `protecting-landscape-lighting-from-texas-storms`, `landscape-lighting-for-home-security`,
  `landscape-lighting-maintenance-checklist`, `how-much-electricity-does-landscape-lighting-use`
