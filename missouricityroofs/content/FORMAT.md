# Content file format (Missouri City Roofers site)

Every content page is ONE file: a JSON header inside an HTML comment, then the body HTML.

```
<!--
{
  "slug": "url-slug-here",
  "title": "SEO <title>, 50-65 chars, keyword near the front",
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
- Business name: **Missouri City Roofers**. Website: missouricityroofs.com. Phone: **(512) 297-7580** (link: `<a href="tel:+15122977580">(512) 297-7580</a>`). Do not write any email address. Do not invent a street address, years in business, license numbers, review counts, awards, manufacturer certifications, warranties with specific years from us, or named staff.
- We offer **free roof inspections** with photo documentation, no obligation. Mention them naturally on every page and link to `/free-roof-inspection/`.
- We help homeowners document storm damage and meet the insurance adjuster, but we are NOT public adjusters and never waive/"cover" deductibles (illegal in Texas — Business & Commerce Code §27.02).
- Service area: Missouri City, TX (ZIP codes 77459 and 77489; the city is mostly in Fort Bend County with a small slice in Harris County) plus Sienna, Sugar Land, Stafford, Pearland, Fresno and Richmond.
- Local color you may use: Fort Bend Parkway (Fort Bend Toll Road), Texas Parkway, Highway 6, US-90A (South Main / Alt 90), Beltway 8 (Sam Houston Tollway), FM 1092 (Murphy Road), Cartwright Road, Sienna Parkway, Vicksburg Boulevard, Lexington Boulevard, Independence Boulevard, the Brazos River, Oyster Creek, Quail Valley golf course and City Centre at Quail Valley, Buffalo Run Park, Fort Bend ISD. Neighborhoods: Sienna, Quail Valley, Lake Olympia, Riverstone, Vicksburg, Hunters Glen, Lexington Village, Colony Lakes, Olympia Estates, Creekmont, Thunderbird, Brightwater, Fondren Park. Housing stock: lots of 1970s-1990s brick ranch and two-story homes in Quail Valley, Hunters Glen and Fondren Park (many now on their second or third roof), plus newer master-planned two-stories in Sienna and Riverstone with HOA roof color/material rules. Many homes have big mature trees (leaves, limbs, shade-driven algae).
- Climate: Gulf Coast humidity, long hot summers, hurricane/tropical storm season (June 1 - Nov 30), spring hail and severe thunderstorms. Real events you may mention only in general terms (no invented stats): Hurricane Harvey (2017) and its Brazos River flooding, Winter Storm Uri (February 2021), the May 2024 Houston derecho, and Hurricane Beryl (July 2024), which knocked out power across Fort Bend County.
- Cost numbers must be framed as planning ranges, not quotes (e.g. architectural asphalt shingle replacement roughly $4.50-$7.50 per sq ft of roof area installed in the Houston area; standing-seam metal roughly $10-$16; a typical Missouri City home 2,200-3,200 sq ft of roof area). Hedge legal/insurance specifics ("many Texas policies...", "check your policy").

## SEO rules
- Primary keyword in: title, h1, description, first paragraph, at least one h2, and 3-5 times in the body.
- Also weave in naturally (not stuffed): "Missouri City roofers", "Missouri City roofing", "roofer in Missouri City", "roofing contractor in Missouri City" — 1-3 total per page.
- Link internally 3-6 times to relevant URLs from this list only:
  `/`, `/free-roof-inspection/`, `/services/`, `/services/roof-replacement-missouri-city-tx/`, `/services/roof-repair-missouri-city-tx/`, `/services/storm-hail-damage-missouri-city-tx/`, `/services/insurance-claim-help-missouri-city-tx/`, `/services/metal-roofing-missouri-city-tx/`, `/services/commercial-roofing-missouri-city-tx/`, `/services/gutters-missouri-city-tx/`, `/areas/`, `/areas/roofing-sienna-tx/`, `/areas/roofing-sugar-land-tx/`, `/areas/roofing-stafford-tx/`, `/areas/roofing-pearland-tx/`, `/areas/roofing-fresno-tx/`, `/areas/roofing-richmond-tx/`, `/weather/`, `/tools/roof-cost-calculator/`, `/tools/roof-pitch-calculator/`, `/tools/storm-damage-checklist/`, `/contact/`, and the blog post URLs `/blog/<slug>/` listed in the blog plan.
- Write for homeowners: concrete, practical, specific to Missouri City's climate and housing stock. US spelling. No fluff, no "In today's fast-paced world", no "Whether you're...". Vary sentence length. No emoji. Do not reuse phrasing from other roofing sites; write fresh.

## Image keys
hero-home (brick two-story suburban home with a shingle roof), roofer-work (roofer working on a shingle roof), shingles-close (close-up of asphalt shingles), metal-roof (house with a standing-seam metal roof), storm-sky (dark storm clouds), lightning (lightning at night), rain (heavy rain), suburb (suburban street of homes), home-modern (newer two-story home), home-brick (brick ranch home), home-trees (home surrounded by mature trees), home-dusk (home at dusk with lights on), commercial (commercial/flat roof building), gutter (rain gutter on a roof edge)

## Type-specific header keys

### Blog posts (`content/blog/<slug>.html`)
`"date": "YYYY-MM-DD"`, `"excerpt": "1-2 sentence card summary"`, `"read_minutes": int`, `"category": "Storm Prep" | "Hail Damage" | "Costs" | "Insurance" | "Materials" | "Maintenance" | "Hiring"`. 3-4 faqs. Body 1,100-1,500 words.

### Services (`content/services/<slug>.html`)
`"name": "short nav label"`, `"short": "card blurb, 15-25 words"`, `"icon": one of "shield","hammer","cloud-hail","file-check","layers","building","droplets","home"`, `"bullets": ["4-6 short 'what's included' items"]`. 4-5 faqs. Body 750-1,000 words.

### Service areas (`content/areas/<slug>.html`)
`"name": "City name"`, `"short": "card blurb, 15-25 words"`, `"county": "..."`, `"zips": "comma separated"`, `"drive": "e.g. 15 min from Missouri City via Fort Bend Parkway"`, `"neighborhoods": ["5-7 real neighborhood names"]`. 3-4 faqs. Body 550-750 words, genuinely different from the other area pages (local housing stock, HOA patterns, storm exposure, roads, typical roof age/materials). Only use neighborhood names you are confident are real.

## Blog plan (slug — date — primary keyword — category)
1. `hurricane-roof-prep-missouri-city-tx` — 2026-09-20 — hurricane roof prep Missouri City — Storm Prep
2. `hail-damage-signs-missouri-city-roof` — 2026-09-23 — hail damage roof Missouri City — Hail Damage
3. `roof-replacement-cost-missouri-city-tx` — 2026-09-26 — roof replacement cost Missouri City TX — Costs
4. `filing-a-roof-insurance-claim-in-fort-bend-county` — 2026-09-29 — roof insurance claim Fort Bend County — Insurance
5. `best-shingles-for-missouri-city-heat-and-humidity` — 2026-10-02 — best shingles for Texas heat and humidity — Materials
6. `older-roofs-in-quail-valley-repair-or-replace` — 2026-10-05 — repair or replace older roof — Maintenance
7. `how-to-hire-a-roofer-in-missouri-city` — 2026-10-08 — roofer in Missouri City — Hiring
8. `roof-algae-and-black-streaks-missouri-city` — 2026-10-11 — roof algae black streaks Texas — Maintenance
9. `impact-resistant-shingles-fort-bend-insurance-discount` — 2026-10-14 — impact resistant shingles insurance discount Texas — Insurance
10. `roof-leak-after-heavy-rain-what-to-do` — 2026-10-17 — roof leak after heavy rain — Storm Prep

## Services plan (slug — name — keyword — icon)
- `roof-replacement-missouri-city-tx` — Roof Replacement — roof replacement Missouri City TX — home
- `roof-repair-missouri-city-tx` — Roof Repair — roof repair Missouri City TX — hammer
- `storm-hail-damage-missouri-city-tx` — Storm & Hail Damage — storm damage roof repair Missouri City — cloud-hail
- `insurance-claim-help-missouri-city-tx` — Insurance Claim Help — roof insurance claim help Missouri City — file-check
- `metal-roofing-missouri-city-tx` — Metal Roofing — metal roofing Missouri City TX — layers
- `commercial-roofing-missouri-city-tx` — Commercial Roofing — commercial roofing Missouri City TX — building
- `gutters-missouri-city-tx` — Gutters & Drainage — gutter installation Missouri City TX — droplets

## Areas plan (slug — name — keyword)
- `roofing-sienna-tx` — Sienna — roofer Sienna TX
- `roofing-sugar-land-tx` — Sugar Land — roofing Sugar Land TX
- `roofing-stafford-tx` — Stafford — roofer Stafford TX
- `roofing-pearland-tx` — Pearland — roofing Pearland TX
- `roofing-fresno-tx` — Fresno — roofer Fresno TX
- `roofing-richmond-tx` — Richmond — roofing Richmond TX
