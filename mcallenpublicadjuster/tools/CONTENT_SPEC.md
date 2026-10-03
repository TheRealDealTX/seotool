# Content specification — McAllen Public Adjuster rebuild

Every page, service page, and article is a PHP file that **returns an array**. The site
code (already written) renders the layout, hero, breadcrumbs, sidebar, FAQs (from the
`faqs` key), schema, CTA band, author box, and related posts. You only write data + body HTML.

Site root: `/home/user/seotool/mcallenpublicadjuster/site/`

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, like the original WordPress permalinks) |

## File format (exact)

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claims in McAllen, TX',   // H1 + breadcrumb
    'seo_title'   => 'McAllen Hail Damage Claims | Public Adjuster Help',  // <title>, 50–62 chars ideal, unique
    'description' => 'Meta description, 120–150 characters, unique, includes the main keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services only).',
    'kicker'      => 'Short eyebrow label, e.g. "Hail Damage Claims" (optional)',
    'image'       => '/assets/img/featured/service-hail-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'date'        => '2026-04-26',   // original publish date (existing posts) or 2026-10-03 (new)
    'updated'     => '2026-10-03',
    'category'    => 'Hail Claims',  // one of: Hail Claims, Roof Claims, Wind & Storm Claims, Hurricane Claims, Fire Claims, Water Damage Claims, Claim Process, Commercial Claims, Weather Records, Building Codes
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/document-hail-damage-for-an-insurance-claim/'],  // optional preferred related posts
    'sources'     => [['NOAA Storm Events Database', 'https://www.ncdc.noaa.gov/stormevents/']],  // posts: authoritative references
    // services only:
    'service_name'  => 'Hail Damage Claims',
    'related_posts' => ['/roof-hail-damage-insurance-claim-mcallen/'],
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
* Allowed helpers: `<p>`, `<ul>/<ol>/<li>`, `<table>` with `<thead>/<tbody>`, `<blockquote>`, `<strong>`, `<em>`, `<a>`, `<figure><img …><figcaption>`.
* Styled boxes available:
  * `<div class="key-takeaways"><h2>Key takeaways</h2><ul>…</ul></div>` — put at the very top of articles.
  * `<div class="callout"><span class="callout-title">Title</span><p>…</p></div>` (variants: `callout callout-gold`, `callout callout-warn`).
* Shortcodes (write them literally on their own line):
  * `[[cta]]` — mid-content Free Claim Review band (use once in long pieces, roughly in the middle).
  * `[[cta-storm]]` — "Did a Recent Storm Damage Your Property?" band (storm/weather topics).
  * `[[phone]]` → linked phone number; `[[email]]` → linked public email; `[[license]]` → `3356839`; `[[company]]` → Rise Public Adjusting LLC.
  * `[[form]]` — the full Free Claim Review form (only on contact-type pages).
* Images inside bodies: `<figure><img src="/wp-content/uploads/…" alt="…" width="1024" height="683" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`. Only use image paths that exist on disk (check with `ls`).
* Internal links: plain root-relative `href="/services/hail-damage-claims/"`. Link only to URLs listed in **URL inventory** below. 4–10 contextual internal links per article/service page.
* External links: only to authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, weather.gov, ncei.noaa.gov / ncdc.noaa.gov, fema.gov, floodsmart.gov, twia.org, mcallen.net, census.gov). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners and business owners in McAllen, Hidalgo County, and the Rio Grande Valley dealing with property insurance claims. Professional but conversational; varied sentence length; plain English; no fluff.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If you are not sure something is true, leave it out or phrase it generally ("many policies", "may").
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage always depends on the policy and facts.
* Public adjusters are not attorneys: do not give legal advice; recommend consulting a Texas attorney for legal questions (suits, bad faith, deadlines to sue).
* Do not claim the business has a physical office. Say "serving McAllen, Hidalgo County, and surrounding Rio Grande Valley communities".
* Remove the old copy's unsupported claims, e.g. "You pay nothing unless we increase your settlement", "Texas insurance policy loopholes", "relentless", "fight insurance companies", "maximize your payout" promises, "team of licensed public adjusters" (say "licensed Texas public adjusters" / "our public adjusters" only generically, or "Joseph Dittman, a licensed Texas public adjuster"). Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keyword use must read naturally. Primary keyword "McAllen Public Adjuster"; secondary keywords in the master brief (e.g. "public adjuster in McAllen", "McAllen hail damage claims", "Hidalgo County public adjuster", "insurance claim help in McAllen", "denied insurance claim McAllen", "underpaid insurance claim McAllen", "roof insurance estimate McAllen"). Use the page's own topic keyword in the H1/title, first paragraph, one H2, and the meta description. No stuffing.
* US spelling. Use "Rio Grande Valley (RGV)". Use "Peñitas" with the ñ.
* Local context should be real: McAllen's hail season peaks April–May (NOAA data), severe straight-line wind events, tropical systems (Hurricane Dolly 2008, Hurricane Hanna 2020), flash flooding, the February 2021 freeze; common local construction: slab-on-grade homes, composition shingle roofs, stucco and brick veneer, metal roofs on outbuildings/commercial, flat/low-slope commercial roofs; 2024 ICC codes adopted by the City of McAllen effective January 1, 2026.

## Verified facts you may cite

### Business
* McAllen Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (use `[[phone]]`). Public email **info@mcallenpublicadjuster.com** (use `[[email]]`). Never show any other email address.
* Main call to action: **Free Claim Review** → `/free-claim-review/`.
* Author of every article: **Joseph Dittman, Public Adjuster**. Verified bio (from txpublicadjusting.com): Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Works with TX Public Adjusting (txpublicadjusting.com). Do not add anything else about him (no years, no counts, no awards).
* Tools commonly used in claim documentation (from the company site): Xactimate estimating software, Matterport 3D imaging.

### Texas insurance law (cite generally; link to statutes.capitol.texas.gov or tdi.texas.gov)
* Public adjusters are licensed and regulated by the Texas Department of Insurance under **Texas Insurance Code Chapter 4102**.
* Public adjuster compensation may not exceed **10% of the insurance settlement** on the claim (Tex. Ins. Code §4102.104). If the insurer pays or commits in writing to pay policy limits within 72 hours after the loss is reported, the adjuster cannot take a percentage fee (reasonable hourly compensation only).
* Public adjuster contracts must use TDI-approved terms, let the client **rescind within 72 hours** of signing, and display "WE REPRESENT THE INSURED ONLY" (§4102.103/§4102.104; 28 TAC §19.708).
* A public adjuster may not participate in the repair/reconstruction of the property on a claim they adjust (conflict-of-interest rules, Tex. Ins. Code §4102.158 and §4102.163). Do not quote exact section numbers for this point other than "Chapter 4102".
* **Prompt Payment of Claims** (Tex. Ins. Code Chapter 542, Subchapter B): insurer generally has 15 days after notice of a claim to acknowledge it, begin its investigation, and request needed information (§542.055); 15 business days after receiving all requested items to accept or reject, or it may notify the policyholder it needs more time and then has up to 45 more days (§542.056); payment within 5 business days after notifying acceptance (§542.057). Deadlines are extended by 15 days after a weather-related catastrophe or major natural disaster declared by the commissioner (§542.059). Eligible surplus lines insurers have different (30 business day) timeframes.
* Weather-related claim lawsuits: Tex. Ins. Code **Chapter 542A** requires written pre-suit notice at least 61 days before filing suit. (Mention only as "consult an attorney"; no legal advice.)
* Many Texas property policies contain contractual deadlines to file suit (often two years and one day from when the claim accrued, per Tex. Civ. Prac. & Rem. Code §16.070). Tell readers to check their own policy and consult an attorney.
* **TWIA** (Texas Windstorm Insurance Association) covers windstorm/hail in the designated catastrophe area: Aransas, Brazoria, Calhoun, **Cameron**, Chambers, Galveston, Jefferson, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio, **Willacy**, and part of Harris County. **Hidalgo County is not in the TWIA area**, so McAllen properties typically get wind/hail coverage from their regular insurer (or the Texas FAIR Plan where applicable). TDI windstorm (WPI-8) certification applies only in the TWIA area.
* Standard homeowners and commercial property policies generally **exclude flood**; flood coverage comes from the National Flood Insurance Program (NFIP) or private flood policies (floodsmart.gov). NFIP policies typically have a 30-day waiting period.
* Many Texas policies carry separate wind/hail deductibles, often a percentage of Coverage A (dwelling) limit; named-storm/hurricane deductibles may apply. Always "check your declarations page".
* Appraisal clause: either party can demand appraisal to resolve a disagreement over the **amount** of loss (not coverage); each side selects an appraiser and the appraisers select an umpire; an award agreed by any two is binding on amount (policy language controls).
* Replacement cost vs. actual cash value: ACV = replacement cost minus depreciation; under replacement-cost policies the insurer typically pays ACV first and releases recoverable depreciation after repairs are completed (often within a deadline stated in the policy). Some Texas roof coverage is ACV-only or uses roof payment schedules — check the policy.
* Ordinance or law coverage pays (up to its limit) for increased costs to comply with building codes when repairing covered damage; it is often a separate, limited coverage or endorsement.

### City of McAllen building codes (verified 2026-10-03)
* City of McAllen adopted the **2024 International Code Council (ICC) codes** — International Residential Code, International Building Code, International Existing Building Code, International Energy Conservation Code, plumbing, mechanical, fuel gas, fire, swimming pool & spa, wildland-urban interface — plus the **2023 National Electrical Code**, **effective January 1, 2026**, with local exceptions (interior residential lighting controls, commercial adult changing-table requirement, municipal residential fire sprinkler requirements). Sources: City of McAllen Residential Building Permit Checklist (REV 01/2026) lists "International Residential Code 2024" and "International Energy Code 2024"; Texas Border Business, Nov 2025 article quoting Chief Building Official Norma Yado, CPM, CBO.
* Permits: Building Permits & Inspections, 311 N. 15th Street, McAllen, TX 78501, (956) 681-1300; inspection request line (956) 681-1328; online permit portal https://onlinepermits.mcallen.net/portal/ ; department page https://www.mcallen.net/departments/permits/home .
* Residential permit application includes Repair/Remodeling options and roof types (wood shingle, composition, metal, built-up, cement). Permits become invalid if work does not start within six months; a permit is good for one year. Re-inspection fee $48. New construction/addition/remodel permit fee $0.16 per sq ft, minimum $48 (fee schedule effective Oct 1, 2016). Structures built before 1978 trigger EPA lead-safe renovation rule disclosure.
* Re-roofing generally requires a building permit in McAllen; confirm the scope with the Building Permits & Inspections department. (Do not state permit fees for re-roofing.)
* Design wind speeds, roof underlayment, drip edge, and fastening requirements come from the adopted IRC/IBC (and ASCE 7 referenced standards); do not quote a specific design wind speed number for McAllen.
* Compliance requirements do **not** automatically mean the insurer must pay for code upgrades — that depends on ordinance or law coverage and policy terms.

### Storm data
See `tools/notes/storm-facts.md` (verified from the NOAA NCEI Storm Events Database). Cite NCEI event links when you use a specific event. Do not cite damage dollar figures.

## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/claim-tools/`, `/claim-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`

Services: `/services/hail-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/wind-damage-claims/`, `/services/storm-damage-claims/`, `/services/hurricane-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/water-damage-claims/`, `/services/commercial-property-claims/`, `/services/residential-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Existing articles (original URLs — keep): 
`/public-adjuster-vs-insurance-adjuster-for-hail-claims/`, `/hail-damage-claim-supplements/`, `/what-to-do-if-your-hail-claim-was-denied-in-mcallen/`, `/document-hail-damage-for-an-insurance-claim/`, `/roof-hail-damage-insurance-claim-mcallen/`, `/fire-insurance-adjuster/`, `/claim-changes-knowing-when-to-hire-a-public-adjuster/`, `/fire-insurance-public-adjuster/`

New articles:
`/wind-damage-insurance-claims-mcallen-tx/`, `/hurricane-damage-mcallen-homeowners-guide/`, `/building-codes-insurance-repairs-mcallen/`, `/how-to-review-underpaid-roof-insurance-estimate/`, `/why-property-insurance-claims-are-delayed-texas/`, `/water-damage-vs-flood-damage-mcallen/`, `/document-commercial-property-damage-after-storm/`, `/replacement-cost-vs-actual-cash-value-texas/`, `/insurance-company-disputes-storm-damage/`, `/noaa-weather-records-document-property-damage-mcallen/`, `/freeze-damage-burst-pipe-claims-rio-grande-valley/`, `/mcallen-hail-season-storm-data/`

## Images

* Existing articles keep their original featured image and inline images (paths under `/wp-content/uploads/2026/…`, see the original HTML in `tools/original-content/posts_full.json`). Prefer the `-1024x683.webp` size for inline figures; featured `image` uses the full-size original (no size suffix).
* New articles: `'image' => '/assets/img/featured/<slug>.webp'`.
* Service pages: `'image' => '/assets/img/featured/service-<slug>.webp'`.
* Pages: `'image' => '/assets/img/featured/page-<slug>.webp'` (the images are generated separately; just use the path).

## Length targets

* Existing articles: rewrite and expand to **1,600–2,400 words** of body text (keep the topic, keep useful original points, improve accuracy).
* New articles: **1,500–2,500 words**.
* Service pages: **900–1,400 words** body + 5–7 FAQs.
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
