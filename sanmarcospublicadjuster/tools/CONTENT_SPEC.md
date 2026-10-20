# Content specification — San Marcos Public Adjuster rebuild

Every page, service page, and article is a PHP file that **returns an array**. The site
code (already written) renders the layout, hero, breadcrumbs, sidebar, FAQs (from the
`faqs` key), schema, CTA band, author box, and related posts. You only write data + body HTML.

Site root: `/home/user/seotool/sanmarcospublicadjuster/site/`
Format/quality references (sister sites on the same engine — read for structure only; NEVER copy or closely
paraphrase their text, and never reuse their city facts; San Marcos content must be written fresh):
* `/tmp/claude-0/-home-user-seotool/1a2be98a-bdc9-505f-a581-743fd8901faa/scratchpad/sa-removed/` (San Antonio: `pages/`, `services/`, `posts/`)
* `/tmp/claude-0/-home-user-seotool/1a2be98a-bdc9-505f-a581-743fd8901faa/scratchpad/mca/mcallenpublicadjuster/site/content/` (McAllen)

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, like the original WordPress permalinks) |

## File format (exact)

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claims in San Marcos, TX',   // H1 + breadcrumb
    'seo_title'   => 'San Marcos Hail Damage Claims | Public Adjuster Help',  // <title>, 50–62 chars ideal, unique
    'description' => 'Meta description, 120–155 characters, unique, includes the main keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services only).',
    'kicker'      => 'Short eyebrow label, e.g. "Hail Damage Claims" (optional)',
    'image'       => '/assets/img/featured/service-hail-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'author'      => 'Joseph Dittman',
    'date'        => '2026-04-01',   // see the URL inventory for each article's date
    'updated'     => '2026-10-20',
    'category'    => 'Hail Claims',  // one of: Hail Claims, Roof Claims, Wind & Storm Claims, Flood Claims, Freeze Claims, Fire Claims, Water Damage Claims, Claim Process, Commercial Claims, Weather Records, Building Codes, Hiring a Public Adjuster
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/roof-damage-public-adjuster/'],  // optional preferred related posts
    'sources'     => [['NOAA Storm Events Database', 'https://www.ncdc.noaa.gov/stormevents/']],  // posts: authoritative references
    // services only:
    'service_name'  => 'Hail Damage Claims',
    'related_posts' => ['/san-marcos-hail-season-storm-data/'],
    'cta_heading'   => 'Hail damage claim questions?',   // optional
    'order'       => 10,              // services: menu order
    'faqs' => [
        ['q' => 'Question text?', 'a' => '<p>Answer HTML.</p>'],
    ],
    'body' => <<<'HTML'
<p>Body HTML…</p>
HTML,
];
```

* Use a **nowdoc** (`<<<'HTML'`) for `body` so `$` signs need no escaping. The closing `HTML,` must be at the start of a line.
* Use single-quoted PHP strings for other values; escape apostrophes as `\'` (or use the typographic ’).
* Run `php -l <file>` on every file you write. A syntax error breaks the whole site.

## Body HTML rules

* **Do not** include an `<h1>` (the template prints it), the FAQ section (use the `faqs` key), the author bio, or a final CTA (the template adds them).
* Use `<h2>` for main sections and `<h3>` for sub-sections. Logical order, no skipped levels.
* Allowed: `<p>`, `<ul>/<ol>/<li>`, `<table>` with `<thead>/<tbody>`, `<blockquote>`, `<strong>`, `<em>`, `<a>`, `<figure><img …><figcaption>`.
* Styled boxes:
  * `<div class="key-takeaways"><h2>Key takeaways</h2><ul>…</ul></div>` — at the very top of articles.
  * `<div class="callout"><span class="callout-title">Title</span><p>…</p></div>` (variants: `callout callout-gold`, `callout callout-warn`).
* Shortcodes (literally, on their own line):
  * `[[cta]]` — mid-content Free Claim Review band (once in long pieces, roughly in the middle).
  * `[[cta-storm]]` — "Did a Recent Storm Damage Your Property?" band (storm/weather topics).
  * `[[phone]]` → linked phone; `[[email]]` → linked info@sanmarcospublicadjuster.com; `[[license]]` → `3356839`; `[[company]]` → Rise Public Adjusting LLC.
  * `[[form]]` — the full Free Claim Review form (only on contact-type pages).
* Images inside bodies: `<figure><img src="/path.webp" alt="…" width="1024" height="683" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`. Only use paths that exist on disk; see `tools/notes/photos.md` for the list and what each photo shows (use real width/height from that list).
* Internal links: root-relative, e.g. `href="/services/hail-damage-claims/"`. Link only to URLs in the **URL inventory**. 5–10 contextual internal links per article/service page; always link at least once to the homepage with anchor text "San Marcos public adjuster" (or close variant) and to `/free-claim-review/`.
* External links: only authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, weather.gov, ncei.noaa.gov / ncdc.noaa.gov, fema.gov, floodsmart.gov, twia.org, sanmarcostx.gov, hayscountytx.gov, census.gov, iccsafe.org). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners and business owners in San Marcos, Hays County, and nearby Central Texas communities (Kyle, Buda, Wimberley, Dripping Springs, New Braunfels, Lockhart, Seguin, Martindale, Maxwell, Uhland) dealing with property insurance claims. Professional, warm, conversational; varied sentence length; plain English; no fluff. Clearly better and more useful than the original copy.
* Author of every article: **Joseph Dittman, licensed Texas public adjuster**. You may write in a first-person-plural practice voice ("we", "our public adjusters") or neutral voice; do not invent personal anecdotes, case stories, or client quotes.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If unsure, leave it out or phrase it generally ("many policies", "may").
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage always depends on the policy and facts.
* Public adjusters are not attorneys: no legal advice; recommend a Texas attorney for legal questions (suits, bad faith, deadlines to sue).
* No physical office. Say "serving San Marcos, Hays County, and surrounding Central Texas communities".
* Remove the old copy's unsupported claims: "You pay nothing unless we increase your settlement", "We fight insurance companies", "aggressively", "relentless", "maximize your payout" promises, "team of licensed public adjusters". Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keywords read naturally. Primary keyword "San Marcos Public Adjuster" (also the brand name); secondary: "public adjuster in San Marcos", "San Marcos public adjusters", "Hays County public adjuster", "San Marcos hail damage claims", "insurance claim help in San Marcos", "denied insurance claim San Marcos", "underpaid insurance claim San Marcos", "public adjuster San Marcos TX". Use the page's topic keyword in title, first paragraph, one H2, and meta description. Use "San Marcos" + "public adjuster" phrasing 3–6 times per article/service page. No stuffing.
* US spelling. Write "Hays County", "Texas State University", "Interstate 35 (I-35)", "Blanco River", "San Marcos River".

## Verified local facts you may cite

Full sheet with sources and confidence levels: `tools/notes/local-facts.md` (use only High/Med items; never UNVERIFIED ones).
Storm records: `tools/notes/storm-facts.md` (NOAA NCEI, Hays County, 502 events 1953–2026, with event links).

Highlights:
* San Marcos is the county seat of Hays County, on I-35 between Austin and San Antonio (about 25 miles south of Austin); home of Texas State University and the spring-fed San Marcos River. Census Vintage 2025 population estimate: 77,830 (July 1, 2025). ZIP 78666 (street delivery). Part of the I-35 growth corridor with many newer subdivisions.
* NWS forecast office: **NWS Austin/San Antonio (EWX)** in New Braunfels. Live weather on this site comes from the **San Marcos Regional Airport station (KHYI)**.
* San Marcos and Hays County sit along the Balcones Escarpment in "Flash Flood Alley".
* **NOAA, Hays County:** 180 hail reports (1967–2026); 58 at golf-ball size (1.75") or larger; 8 at baseball size (2.75") or larger. Hail peaks in **May (67) and April (57)**, then March (23). 109 thunderstorm wind reports (peak May, June). 31 tornado reports. 127 flash-flood reports (peaks June, May, October). Largest hail: **4.5" on March 16, 2000 just north of San Marcos** (widespread roof and window damage); **4.25" on April 20, 2006** along I-35 near the San Marcos outlet malls; **May 9, 2024**: 3" hail at San Marcos Academy west of the city, 2.5" near the outlet mall, 2.5" near Wimberley, 3" south of Dripping Springs, plus 70 mph wind gusts that damaged roofs and downed trees in San Marcos (Hays County Judge signed a local disaster declaration — local, not federal); **May 22, 2025**: baseball-size (2.75") hail in Uhland and tennis-ball-size (2.5") hail in Kyle. Wind: Jan 13, 2007 70–80 mph along I-35 in San Marcos tore metal roofs off; June 9, 2019 ~75 mph gust peeled a metal roof off a house in San Marcos and ~80 mph blew a roof section off a house in Niederwald; Jan 10, 2020 ~75 mph gusts in Kyle blew siding off a house, multiple houses had shingle damage. Tornadoes: EF1 Oct 30, 2015 crossing into Hays near Centerpoint Rd (San Marcos); EF1 Feb 19, 2017 Wimberley; EF0s June 12, 2025 south of Wimberley.
* **Floods:** Memorial Day flood, May 23–24, 2015 — Blanco River at Wimberley rose from about 5 ft to about 41 ft in roughly four hours; San Marcos River near San Marcos crested at 43.08 ft on May 24; NWS issued Flash Flood Emergencies for Wimberley and San Marcos (FEMA DR-4223). October 30–31, 2015 — 18.46" two-day rain at 1 WNW Buda, 15.63" north of San Marcos (FEMA DR-4245). Halloween flood Oct 30–31, 2013 — 12–14" from Wimberley to Driftwood (DR-4159). October 17–18, 1998 — NWS estimated over 30" of rain over a small area south of San Marcos in 36 hours (DR-1257). Since 2015 the city has used HUD CDBG-DR funds for flood mitigation (Blanco River Flood Mitigation Project).
* **Freezes:** Winter Storm Uri, Feb 10–18, 2021 — 7.0" snow 5 WNW of San Marcos, 5.9" in Kyle; widespread burst pipes; FEMA DR-4586 included Hays County. Ice storm Jan 30–Feb 2, 2023 (DR-4705).
* FEMA declarations including Hays County: DR-1257 (1998 floods), DR-1425 (2002 floods), DR-4159 (2013), DR-4223 (May 2015), DR-4245 (Oct 2015), DR-4586 (Feb 2021 winter storm), DR-4705 (2023 winter storm), DR-4781 (Apr–Jun 2024 storms). Link: `https://www.fema.gov/disaster/4223` etc.
* **Flood insurance:** City of San Marcos participates in the NFIP. New FEMA flood maps for the Blanco River, San Marcos River, and parts of Sink, Purgatory, Willow Springs, and Cottonwood Creeks took effect **January 17, 2025** (sanmarcostx.gov/402/FEMA-Flood-Map-Revision-Process). Flood-zone lookup: city GIS map and FEMA Flood Map Service Center (msc.fema.gov).
* **Building codes (City of San Marcos):** 2021 International Codes (IBC, IRC, IECC, IEBC, IPMC, IMC, IPC, IFGC, IFC, ISPSC) and the 2020 NEC, adopted by Ordinance 2023-09, **in effect since April 1, 2023**. Local amendment: **roof covering replacement permits are not required unless the replacement roof is heavier than the existing roof covering**; all foundations must be designed by a licensed engineer. Permit Center: 630 E. Hopkins Street, San Marcos, TX 78666, 512-805-2630, permitinfo@sanmarcostx.gov; online permits via **MGO Connect** (mgoconnect.org). Sources: https://www.sanmarcostx.gov/1289/Codes-Ordinances , https://www.sanmarcostx.gov/1000/Permit-Center . Hays County does not issue residential building permits in unincorporated areas (it handles septic/OSSF, development, floodplain and applies the 2018 IFC to commercial/multifamily). Kyle, Buda, Wimberley, Dripping Springs, New Braunfels, Lockhart, Seguin have their own permit offices — tell readers to check with their city. Code requirements do **not** automatically mean the insurer pays for upgrades — that depends on ordinance or law coverage.
* Local construction: slab-on-grade homes on expansive clay soils east of I-35 and limestone/thin soils in the Hill Country to the west; composition shingle roofs dominate in subdivisions; standing-seam and exposed-fastener metal roofs are common on Hill Country homes, barns and outbuildings; brick, stone, Hardie/fiber-cement and stucco exteriors; many student rental and multifamily properties near Texas State; older homes in historic neighborhoods near downtown; flat/low-slope commercial roofs along I-35.
* Counties: Kyle, Buda, Wimberley, Dripping Springs = Hays; Lockhart, Martindale, Maxwell = Caldwell (Uhland split Hays/Caldwell); New Braunfels = mostly Comal (part Guadalupe); Seguin = Guadalupe.

### Business
* San Marcos Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (use `[[phone]]`). Email **info@sanmarcospublicadjuster.com** (use `[[email]]`). Never show any other email address.
* Main CTA: **Free Claim Review** → `/free-claim-review/`.
* Joseph Dittman verified bio: licensed Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Nothing else about him (no years, counts, awards).
* Tools used in claim documentation: Xactimate estimating software, Matterport 3D imaging, drone/roof photography is NOT verified — don't mention drones.

### Texas insurance law (cite generally; link to statutes.capitol.texas.gov or tdi.texas.gov)
* Public adjusters are licensed and regulated by the Texas Department of Insurance under **Texas Insurance Code Chapter 4102**.
* Public adjuster compensation may not exceed **10% of the insurance settlement** on the claim (Tex. Ins. Code §4102.104). If the insurer pays or commits in writing to pay policy limits within 72 hours after the loss is reported, the adjuster cannot take a percentage fee (reasonable hourly compensation only).
* Public adjuster contracts must use TDI-approved terms, let the client **rescind within 72 hours** of signing, and display "WE REPRESENT THE INSURED ONLY" (§4102.103/§4102.104; 28 TAC §19.708).
* A public adjuster may not participate in the repair/reconstruction of the property on a claim they adjust (conflict-of-interest rules, Tex. Ins. Code §4102.158 and §4102.163). Do not quote exact section numbers for this point other than "Chapter 4102".
* **Prompt Payment of Claims** (Tex. Ins. Code Chapter 542, Subchapter B): insurer generally has 15 days after notice of a claim to acknowledge it, begin its investigation, and request needed information (§542.055); 15 business days after receiving all requested items to accept or reject, or it may notify the policyholder it needs more time and then has up to 45 more days (§542.056); payment within 5 business days after notifying acceptance (§542.057). Deadlines are extended by 15 days after a weather-related catastrophe or major natural disaster declared by the commissioner (§542.059). Eligible surplus lines insurers have different (30 business day) timeframes.
* Weather-related claim lawsuits: Tex. Ins. Code **Chapter 542A** requires written pre-suit notice at least 61 days before filing suit. (Mention only as "consult an attorney"; no legal advice.)
* Many Texas property policies contain contractual deadlines to file suit (often two years and one day from when the claim accrued, per Tex. Civ. Prac. & Rem. Code §16.070). Tell readers to check their own policy and consult an attorney.
* **TWIA** (Texas Windstorm Insurance Association) covers windstorm/hail in the designated catastrophe area: Aransas, Brazoria, Calhoun, **Cameron**, Chambers, Galveston, Jefferson, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio, **Willacy**, and part of Harris County. **Hays County is not in the TWIA area**, so San Marcos properties typically get wind/hail coverage from their regular insurer (or the Texas FAIR Plan where applicable). TDI windstorm (WPI-8) certification applies only in the TWIA area.
* Standard homeowners and commercial property policies generally **exclude flood**; flood coverage comes from the National Flood Insurance Program (NFIP) or private flood policies (floodsmart.gov). NFIP policies typically have a 30-day waiting period.
* Many Texas policies carry separate wind/hail deductibles, often a percentage of Coverage A (dwelling) limit; named-storm/hurricane deductibles may apply. Always "check your declarations page".
* Appraisal clause: either party can demand appraisal to resolve a disagreement over the **amount** of loss (not coverage); each side selects an appraiser and the appraisers select an umpire; an award agreed by any two is binding on amount (policy language controls).
* Replacement cost vs. actual cash value: ACV = replacement cost minus depreciation; under replacement-cost policies the insurer typically pays ACV first and releases recoverable depreciation after repairs are completed (often within a deadline stated in the policy). Some Texas roof coverage is ACV-only or uses roof payment schedules — check the policy.
* Ordinance or law coverage pays (up to its limit) for increased costs to comply with building codes when repairing covered damage; it is often a separate, limited coverage or endorsement.


## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/claim-tools/`, `/claim-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`, `/faq/`, `/sitemap/`
Area pages: `/service-areas/kyle/`, `/service-areas/buda/`, `/service-areas/wimberley/`, `/service-areas/dripping-springs/`, `/service-areas/new-braunfels/`, `/service-areas/lockhart/`, `/service-areas/seguin/`, `/service-areas/martindale/`

Services: `/services/hail-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/wind-damage-claims/`, `/services/storm-damage-claims/`, `/services/flood-damage-claims/`, `/services/freeze-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/water-damage-claims/`, `/services/residential-property-claims/`, `/services/commercial-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Articles (all by Joseph Dittman):

Original posts — rewrite completely at the same URL (original text in `tools/original-content/<slug>.md`):
* `/roof-damage-public-adjuster/` — date 2026-02-16 — image `/wp-content/uploads/2026/02/Roof-Damage-Public-Adjuster.webp`
* `/do-i-need-a-public-adjuster/` — date 2026-03-21 — image `/wp-content/uploads/2026/03/The-Claim-Decision-That-Can-Cost-You-Thousands-Do-I-Need-a-Public-Adjuster_.webp`; inline also `/wp-content/uploads/2026/03/7-Signs-You-Should-Hire-a-Public-Adjuster.webp` and `/wp-content/uploads/2026/03/How-to-Choose-the-Right-Public-Adjuster-in-San-Marcos.webp`
* `/after-the-flames-insurance-adjuster/` — date 2026-04-01 — image `/wp-content/uploads/2026/04/After-the-Flames-Insurance-Adjuster.webp`

Former image-attachment URLs on the old site, now full articles (date as listed):
* `/what-is-a-public-adjuster-and-how-to-hire-one/` — 2026-09-08 — image `/wp-content/uploads/2026/02/What-Is-a-Public-Adjuster-and-How-to-Hire-One.webp`
* `/what-is-a-public-claims-adjuster/` — 2026-09-15 — image `/wp-content/uploads/2026/02/What-Is-a-Public-Claims-Adjuster.webp`
* `/how-to-find-a-public-adjuster/` — 2026-09-22 — image `/wp-content/uploads/2026/02/How-to-Find-a-Public-Adjuster.webp`
* `/when-is-it-too-late-to-hire-a-public-adjuster/` — 2026-09-29 — image `/wp-content/uploads/2026/02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp`
* `/are-public-adjusters-worth-it/` — 2026-10-06 — image `/wp-content/uploads/2026/02/Are-Public-Adjusters-Worth-It.webp`

New articles (image `/assets/img/featured/<slug>.webp`):
* `/san-marcos-hail-season-storm-data/` — 2026-10-01
* `/wind-damage-insurance-claims-san-marcos-tx/` — 2026-10-02
* `/flood-damage-insurance-claims-san-marcos/` — 2026-10-05
* `/freeze-damage-burst-pipe-claims-san-marcos/` — 2026-10-07
* `/building-codes-insurance-repairs-san-marcos/` — 2026-10-08
* `/what-to-do-if-your-claim-was-denied-in-san-marcos/` — 2026-10-09
* `/replacement-cost-vs-actual-cash-value-texas/` — 2026-10-12
* `/how-to-review-underpaid-roof-insurance-estimate/` — 2026-10-13
* `/why-property-insurance-claims-are-delayed-texas/` — 2026-10-14
* `/hail-damage-claim-supplements/` — 2026-10-15
* `/public-adjuster-vs-insurance-adjuster/` — 2026-10-16
* `/commercial-property-insurance-claims-san-marcos/` — 2026-10-19

## Images

* Service pages: `/assets/img/featured/service-<slug>.webp`. Pages: `/assets/img/featured/page-<slug>.webp` (area pages: `page-area-<city>.webp`; author page `page-author-joseph-dittman.webp`). These exist.
* Inline figures: see `tools/notes/photos.md`.

## Length targets

* Rewritten original articles: **1,800–2,600 words** of body.
* Other articles: **1,600–2,400 words**.
* Service pages: **1,000–1,500 words** body + 5–7 FAQs.
* Area pages: **800–1,200 words**, unique to that city (county, distance/direction from San Marcos, local storm/flood history only if verified, permit office note), + 4–5 FAQs.
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
