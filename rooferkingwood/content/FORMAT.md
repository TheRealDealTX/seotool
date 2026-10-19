# Content file format (Kingwood Roofers site — rooferkingwood.com)

Every content page is ONE file: a JSON header inside an HTML comment, then the body HTML.

```
<!--
{
  "slug": "url-slug-here",
  "title": "SEO <title>, 50-62 chars, keyword near the front, ends with '| Kingwood Roofers' if it fits",
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

The JSON must be strictly valid (double quotes, no trailing commas, escape any `"` inside strings as `\"`, no raw newlines inside strings). Validate it with `python3 -c "import json,re,sys; t=open(sys.argv[1]).read(); json.loads(re.match(r'\s*<!--\s*(\{.*?\})\s*-->', t, re.S).group(1))" FILE`.

## Allowed body HTML
`<p> <h2> <h3> <ul> <ol> <li> <strong> <em> <a href="..."> <table><thead><tbody><tr><th><td> <blockquote>`
plus these two components:
- `<div class="callout"><strong>Short label:</strong> one or two sentences.</div>` (tip / warning box, max 2 per page)
- `<div class="cta-inline"></div>` — an empty placeholder the build replaces with a "Book a free roof inspection" banner. Put exactly ONE in the middle of each page.

Do NOT include the H1, the FAQ section, the hero, images, inline styles, scripts or classes other than the two above. The build adds those. Start the body with a `<p>`. Use `<h2>` for sections (5-8 per page) and `<h3>` beneath them where useful.

## Business facts (use exactly; never invent others)
- Business name: **Kingwood Roofers**. Phone: **(512) 297-7580** (link: `<a href="tel:+15122977580">(512) 297-7580</a>`). Do not write any email address. Do not invent a street address, years in business, license numbers, review counts, star ratings, awards, manufacturer certifications, warranties with specific years from us, project counts, or named staff/customers. No testimonials.
- We offer **free roof inspections** with photo documentation, no obligation. Mention them naturally on every page and link to `/free-roof-inspection/`.
- We help homeowners document storm damage and meet the insurance adjuster, but we are NOT public adjusters and never waive/"cover" deductibles (illegal in Texas — Business & Commerce Code §27.02).
- Service area: Kingwood, TX (ZIP 77339, 77345 and the Kingwood part of 77346; mostly Harris County, with the Kings Mill / Kingwood Lakes edge in Montgomery County; part of the City of Houston since the 1996 annexation) plus Atascocita, Humble, Porter, New Caney, Huffman and Crosby.
- Local color you may use (real places): "The Livable Forest" nickname; the villages — Kingwood Forest, Bear Branch, Elm Grove, Forest Cove, Greentree Village, Trailwood, Woodland Hills, Sand Creek, Hunters Ridge, Kings Forest, Kingwood Lakes, Kings Mill, Mills Branch, Fosters Mill, Deer Ridge Estates, Royal Shores, Kingwood Greens, Barrington, Kingwood Place, North Woods/Northwoods; roads Kingwood Drive, Northpark Drive, West Lake Houston Parkway, Woodland Hills Drive, US-59 / I-69 (Eastex Freeway), Loop 494, Hamblen Road, Russell Palmer Road; Lake Houston, the San Jacinto River (West Fork) and Caney Creek / Bens Branch / Taylor Gully; Kingwood Town Center, East End Park, Deer Ridge Park, the greenbelt trail system, Lone Star College-Kingwood, Kingwood High and Kingwood Park High (Humble ISD), Bush Intercontinental Airport to the west.
- Kingwood-specific roofing realities (use these, they are the site's angle): dense mature pine and hardwood canopy → pine needles and debris packing valleys and gutters, shade that feeds algae/moss and black streaks, limbs and whole trees falling on roofs in storms (Hurricane Ike 2008, Hurricane Beryl July 2024), squirrels and rodents chewing vents/roof edges; much of the housing stock was built from the 1970s through the 1990s so many roofs are on their second or third replacement, and older homes can have original wood decking issues or leftover cedar shake; village community associations and the Kingwood Service Association with deed restrictions — re-roofs usually need architectural (ACC) approval of shingle color/material, so tell readers to check with their village association (hedge — rules differ by village). Climate: Gulf humidity, long hot summers, hurricane/tropical storm season June 1 - Nov 30, spring hail and severe thunderstorms. Hurricane Harvey (2017) and Tropical Storm Imelda (2019) caused severe flooding in Kingwood — mention only in general terms; flooding is not a roof problem, so don't overstate. No invented statistics.
- Cost numbers must be framed as planning ranges, not quotes (e.g. architectural asphalt shingle replacement roughly $4.50-$7.50 per sq ft of roof area installed in the Houston area; Class 4 impact-resistant roughly $5.50-$8.50; standing-seam metal roughly $10-$16; a typical Kingwood home has 2,200-3,400 sq ft of roof area). Hedge legal/insurance specifics ("many Texas policies...", "check your policy").

## SEO rules
- Primary keyword in: title, h1, description, first paragraph, at least one h2, and 3-5 times in the body.
- Also weave in naturally (not stuffed): "Kingwood roofers", "Kingwood roofing", "roofer in Kingwood", "roofing company in Kingwood" — 1-3 total per page.
- Link internally 3-6 times to relevant URLs from this list only:
  `/`, `/free-roof-inspection/`, `/services/`, `/services/roof-replacement-kingwood-tx/`, `/services/roof-repair-kingwood-tx/`, `/services/storm-damage-roof-repair-kingwood-tx/`, `/services/tree-damage-roof-repair-kingwood-tx/`, `/services/insurance-claim-help-kingwood-tx/`, `/services/metal-roofing-kingwood-tx/`, `/services/commercial-roofing-kingwood-tx/`, `/services/gutters-kingwood-tx/`, `/areas/`, `/areas/roofing-atascocita-tx/`, `/areas/roofing-humble-tx/`, `/areas/roofing-porter-tx/`, `/areas/roofing-new-caney-tx/`, `/areas/roofing-huffman-tx/`, `/areas/roofing-crosby-tx/`, `/weather/`, `/tools/`, `/tools/roof-cost-calculator/`, `/tools/roof-pitch-calculator/`, `/tools/storm-damage-checklist/`, `/tools/roof-age-estimator/`, `/contact/`, and the blog post URLs `/blog/<slug>/` from the blog plan below.
- Write for homeowners: concrete, practical, specific to Kingwood's trees, climate, HOAs and housing stock. US spelling. No fluff, no "In today's fast-paced world", no "nestled", no "look no further". Vary sentence length. No emoji. No em-dash overuse (max 3 per page).

## Image keys
hero-pines (two-story home surrounded by tall trees), roofer-work (roofer working on a shingle roof), shingles (close-up of asphalt shingles), metal-roof (home with a metal roof), storm-sky (dark storm clouds), lightning (lightning strike at night), hail (hailstones on the ground), fallen-tree (tree fallen onto a house roof after a storm), roof-tarp (blue tarps on storm-damaged roofs), forest-home (house among woods), brick-home (brick suburban house), lake-sunset (lake at sunset), gutter (gutter and downspout), commercial-roof (flat commercial roof), tree-street (tree-lined residential street)

## Type-specific header keys

### Blog posts (`content/blog/<slug>.html`)
`"date": "YYYY-MM-DD"`, `"excerpt": "1-2 sentence card summary"`, `"read_minutes": int`, `"category": "Storm Prep" | "Hail Damage" | "Costs" | "Insurance" | "Materials" | "Maintenance" | "Hiring" | "HOA"`. 3-4 faqs. Body 1,100-1,500 words.

### Services (`content/services/<slug>.html`)
`"name": "short nav label"`, `"short": "card blurb, 15-25 words"`, `"icon": one of "shield","hammer","cloud-hail","file-check","layers","building","droplets","home","tree"`, `"bullets": ["4-6 short 'what's included' items"]`. 4-5 faqs. Body 750-1,000 words.

### Service areas (`content/areas/<slug>.html`)
`"name": "City name"`, `"short": "card blurb, 15-25 words"`, `"county": "..."`, `"zips": "comma separated"`, `"drive": "e.g. 10 min from Kingwood via West Lake Houston Pkwy"`, `"neighborhoods": ["5-7 real neighborhood names"]`. 3-4 faqs. Body 550-750 words, genuinely different from the other area pages (local housing stock, HOA patterns, storm exposure, trees, roads, typical roof age/materials). Only use neighborhood names you are confident are real.

## Blog plan (slug — date — primary keyword — category)
1. `pine-trees-and-your-roof-kingwood` — 2026-09-21 — pine trees and roof damage Kingwood — Maintenance
2. `hurricane-season-roof-prep-kingwood-tx` — 2026-09-24 — hurricane roof preparation Kingwood TX — Storm Prep
3. `roof-replacement-cost-kingwood-tx` — 2026-09-27 — roof replacement cost Kingwood TX — Costs
4. `kingwood-hoa-roof-approval-guide` — 2026-09-30 — Kingwood HOA roof approval — HOA
5. `how-to-spot-hail-damage-kingwood-roof` — 2026-10-03 — hail damage roof Kingwood — Hail Damage
6. `roof-insurance-claim-guide-kingwood-tx` — 2026-10-06 — roof insurance claim Kingwood TX — Insurance
7. `best-roofing-materials-for-kingwood-homes` — 2026-10-09 — best roofing materials Kingwood TX — Materials
8. `how-to-choose-kingwood-roofers` — 2026-10-12 — Kingwood roofers — Hiring
9. `black-streaks-moss-on-roof-kingwood` — 2026-10-15 — black streaks on roof Kingwood — Maintenance
10. `fall-roof-and-gutter-checklist-kingwood` — 2026-10-18 — fall roof maintenance Kingwood — Maintenance

## Services plan (slug — name — keyword — icon)
- `roof-replacement-kingwood-tx` — Roof Replacement — roof replacement Kingwood TX — home
- `roof-repair-kingwood-tx` — Roof Repair — roof repair Kingwood TX — hammer
- `storm-damage-roof-repair-kingwood-tx` — Storm & Hail Damage — storm damage roof repair Kingwood — cloud-hail
- `tree-damage-roof-repair-kingwood-tx` — Tree & Limb Damage — tree damage roof repair Kingwood — tree
- `insurance-claim-help-kingwood-tx` — Insurance Claim Help — roof insurance claim help Kingwood — file-check
- `metal-roofing-kingwood-tx` — Metal Roofing — metal roofing Kingwood TX — layers
- `commercial-roofing-kingwood-tx` — Commercial Roofing — commercial roofing Kingwood TX — building
- `gutters-kingwood-tx` — Gutters & Gutter Guards — gutter installation Kingwood TX — droplets

## Areas plan (slug — name — keyword)
- `roofing-atascocita-tx` — Atascocita — roofing Atascocita TX
- `roofing-humble-tx` — Humble — roofer Humble TX
- `roofing-porter-tx` — Porter — roofing Porter TX
- `roofing-new-caney-tx` — New Caney — roofer New Caney TX
- `roofing-huffman-tx` — Huffman — roofing Huffman TX
- `roofing-crosby-tx` — Crosby — roofer Crosby TX
