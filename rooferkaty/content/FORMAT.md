# Content file format (Katy Roofer site)

Every content page is ONE file: a JSON header inside an HTML comment, then the body HTML.

```
<!--
{
  "slug": "url-slug-here",
  "title": "SEO <title>, 50-62 chars, keyword near the front, ends with '| Katy Roofer' if it fits",
  "h1": "Visible page headline (contains the primary keyword)",
  "description": "Meta description, 140-158 chars, contains the keyword, ends with a soft CTA.",
  "keyword": "primary keyword phrase",
  "image": "one image key from the list below",
  "image_alt": "Descriptive alt text",
  "intro": "1-2 sentence hero lead paragraph (plain text, no HTML).",
  "faqs": [ {"q": "Question?", "a": "Answer, 1-3 sentences, plain text."} ]
  ... plus the type-specific keys below ...
}
-->
<p>Body HTML...</p>
```

The JSON must be strictly valid (double quotes, no trailing commas, escape any `"` inside strings as `\"`, no raw newlines inside strings).

## Allowed body HTML
`<p> <h2> <h3> <ul> <ol> <li> <strong> <em> <a href="..."> <table><thead><tbody><tr><th><td> <blockquote>`
plus these two components:
- `<div class="callout"><strong>Short label:</strong> one or two sentences.</div>` (tip / warning box, max 2 per page)
- `<div class="cta-inline"></div>` — an empty placeholder the build replaces with a "Book a free roof inspection" banner. Put exactly ONE in the middle of each page.

Do NOT include the H1, the FAQ section, the hero, images, inline styles, scripts or classes other than the two above. The build adds those. Start the body with a `<p>`. Use `<h2>` for sections (5-8 per page) and `<h3>` beneath them where useful.

## Business facts (use exactly; never invent others)
- Business name: **Katy Roofer**. Phone: **(512) 297-7580** (link: `<a href="tel:+15122977580">(512) 297-7580</a>`). Do not write any email address. Do not invent a street address, years in business, license numbers, review counts, awards, manufacturer certifications, warranties with specific years from us, or named staff.
- We offer **free roof inspections** with photo documentation, no obligation. Mention them naturally on every page and link to `/free-roof-inspection/`.
- We help homeowners document storm damage and meet the insurance adjuster, but we are NOT public adjusters and never waive/"cover" deductibles (illegal in Texas — Business & Commerce Code §27.02).
- Service area: Katy, TX (77449, 77450, 77493, 77494; spans Harris, Fort Bend and Waller counties) plus Cinco Ranch, Fulshear, Brookshire, Cypress, Richmond and West Houston / Energy Corridor.
- Local color you may use: I-10 Katy Freeway, Grand Parkway (SH-99), Westpark Tollway, FM 1463, Mason Rd, Katy Mills, LaCenterra, Old Town Katy, Katy ISD; neighborhoods Cinco Ranch, Cane Island, Elyson, Cross Creek Ranch, Grand Lakes, Seven Meadows, Firethorne, Kelliwood, Nottingham Country, Pine Mill Ranch, Tamarron, Jordan Ranch. Climate: Gulf Coast humidity, long hot summers, hurricane/tropical storm season (June 1 - Nov 30), spring hail and severe thunderstorms, the May 2024 Houston derecho and July 2024 Hurricane Beryl (real events — mention only in general terms, no invented stats). Many homes have HOAs with roof color/material rules.
- Cost numbers must be framed as planning ranges, not quotes (e.g. architectural asphalt shingle replacement roughly $4.50-$7.50 per sq ft of roof area installed in the Houston area; standing-seam metal roughly $10-$16; a typical Katy home 2,400-3,200 sq ft roof area). Hedge legal/insurance specifics ("many Texas policies...", "check your policy").

## SEO rules
- Primary keyword in: title, h1, description, first paragraph, at least one h2, and 3-5 times in the body.
- Also weave in naturally (not stuffed): "Katy roofer", "Katy roofing", "roofer in Katy", "roofers in Katy" — 1-3 total per page.
- Link internally 3-6 times to relevant URLs from this list only:
  `/`, `/free-roof-inspection/`, `/services/`, `/services/roof-replacement-katy-tx/`, `/services/roof-repair-katy-tx/`, `/services/storm-hail-damage-katy-tx/`, `/services/insurance-claim-help-katy-tx/`, `/services/metal-roofing-katy-tx/`, `/services/commercial-roofing-katy-tx/`, `/services/gutters-katy-tx/`, `/areas/`, `/areas/roofing-cinco-ranch-tx/`, `/areas/roofing-fulshear-tx/`, `/areas/roofing-brookshire-tx/`, `/areas/roofing-cypress-tx/`, `/areas/roofing-richmond-tx/`, `/areas/roofing-west-houston-tx/`, `/weather/`, `/tools/roof-cost-calculator/`, `/tools/roof-pitch-calculator/`, `/tools/storm-damage-checklist/`, `/contact/`, and the blog post URLs `/blog/<slug>/` listed in the blog plan.
- Write for homeowners: concrete, practical, specific to Katy's climate and housing stock. US spelling. No fluff, no "In today's fast-paced world". Vary sentence length. No emoji.

## Image keys
hero-roofer (roofer kneeling on a shingle roof of a brick suburban house), roofer-shingles (roofer in harness on asphalt shingle roof), metal-roof (white house with red standing-seam metal roof), storm-clouds (dark rolling storm clouds), lightning (lightning over a field), storm-dark (dark vertical storm sky), brick-homes (row of brick suburban homes with two-car garages), suburban-street (suburban houses and driveways), suburban-home (suburban home under dramatic clouds), home-porch (two-story home with porch), home-classic (white classic house), home-gables (gabled home with porch and trees), home-sunset (wooden home at sunset), crew-commercial (two workers in hard hats on a commercial site), home-shingle-trees (brick house with shingle roof among trees)

## Type-specific header keys

### Blog posts (`content/blog/<slug>.html`)
`"date": "YYYY-MM-DD"`, `"excerpt": "1-2 sentence card summary"`, `"read_minutes": int`, `"category": "Storm Prep" | "Hail Damage" | "Costs" | "Insurance" | "Materials" | "Maintenance" | "Hiring"`. 3-4 faqs. Body 1,100-1,500 words.

### Services (`content/services/<slug>.html`)
`"name": "short nav label"`, `"short": "card blurb, 15-25 words"`, `"icon": one of "shield","hammer","cloud-hail","file-check","layers","building","droplets","home"`, `"bullets": ["4-6 short 'what's included' items"]`. 4-5 faqs. Body 750-1,000 words.

### Service areas (`content/areas/<slug>.html`)
`"name": "City name"`, `"short": "card blurb, 15-25 words"`, `"county": "..."`, `"zips": "comma separated"`, `"drive": "e.g. 15 min from central Katy via Grand Parkway"`, `"neighborhoods": ["5-7 real neighborhood names"]`. 3-4 faqs. Body 550-750 words, genuinely different from the other area pages (local housing stock, HOA patterns, storm exposure, roads, typical roof age/materials).

## Blog plan (slug — date — primary keyword — category)
1. `hurricane-season-roof-prep-katy-tx` — 2026-09-05 — hurricane roof preparation Katy TX — Storm Prep
2. `how-to-spot-hail-damage-on-your-katy-roof` — 2026-09-08 — hail damage roof Katy — Hail Damage
3. `roof-replacement-cost-katy-tx` — 2026-09-11 — roof replacement cost Katy TX — Costs
4. `texas-roof-insurance-claim-guide-katy` — 2026-09-14 — roof insurance claim Texas — Insurance
5. `best-roofing-materials-for-katy-heat-and-humidity` — 2026-09-17 — best roofing materials Katy TX — Materials
6. `roof-repair-vs-replacement-katy-homeowners` — 2026-09-20 — roof repair vs replacement — Maintenance
7. `how-to-choose-a-roofer-in-katy` — 2026-09-23 — roofer in Katy — Hiring
8. `attic-ventilation-energy-bills-katy-tx` — 2026-09-26 — attic ventilation Katy TX — Materials
9. `class-4-impact-resistant-shingles-texas-insurance-discount` — 2026-09-29 — Class 4 impact-resistant shingles Texas — Insurance
10. `fall-roof-maintenance-checklist-katy` — 2026-10-02 — fall roof maintenance checklist Katy — Maintenance

## Services plan (slug — name — keyword — icon)
- `roof-replacement-katy-tx` — Roof Replacement — roof replacement Katy TX — home
- `roof-repair-katy-tx` — Roof Repair — roof repair Katy TX — hammer
- `storm-hail-damage-katy-tx` — Storm & Hail Damage — hail damage roof repair Katy — cloud-hail
- `insurance-claim-help-katy-tx` — Insurance Claim Help — roof insurance claim help Katy — file-check
- `metal-roofing-katy-tx` — Metal Roofing — metal roofing Katy TX — layers
- `commercial-roofing-katy-tx` — Commercial Roofing — commercial roofing Katy TX — building
- `gutters-katy-tx` — Gutters & Drainage — gutter installation Katy TX — droplets

## Areas plan (slug — name — keyword)
- `roofing-cinco-ranch-tx` — Cinco Ranch — roofing Cinco Ranch TX
- `roofing-fulshear-tx` — Fulshear — roofer Fulshear TX
- `roofing-brookshire-tx` — Brookshire — roofing Brookshire TX
- `roofing-cypress-tx` — Cypress — roofer Cypress TX
- `roofing-richmond-tx` — Richmond — roofing Richmond TX
- `roofing-west-houston-tx` — West Houston & Energy Corridor — roofer West Houston
