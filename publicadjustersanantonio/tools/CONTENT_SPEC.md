# Content specification — San Antonio Public Adjuster rebuild

Every page, service page, and article is a PHP file that **returns an array**. The site
code (already written) renders the layout, hero, breadcrumbs, sidebar, FAQs (from the
`faqs` key), schema, CTA band, author box, and related posts. You only write data + body HTML.

Site root: `/home/user/seotool/publicadjustersanantonio/site/`
Reference (finished sister site with the same engine, McAllen; read for format/quality only, never copy its McAllen facts):
`/tmp/claude-0/-home-user-seotool/4348aa4a-17f4-566f-8ae1-90897ebadb51/scratchpad/mca/mcallenpublicadjuster/site/content/`

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, like the original WordPress permalinks) |

## File format (exact)

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claims in San Antonio, TX',   // H1 + breadcrumb
    'seo_title'   => 'San Antonio Hail Damage Claims | Public Adjuster Help',  // <title>, 50–62 chars ideal, unique
    'description' => 'Meta description, 120–150 characters, unique, includes the main keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services only).',
    'kicker'      => 'Short eyebrow label, e.g. "Hail Damage Claims" (optional)',
    'image'       => '/assets/img/featured/service-hail-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'date'        => '2026-04-26',   // original publish date (existing posts) or 2026-10-03 (new)
    'updated'     => '2026-10-03',
    'category'    => 'Hail Claims',  // one of: Hail Claims, Roof Claims, Wind & Storm Claims, Flood Claims, Freeze Claims, Fire Claims, Water Damage Claims, Claim Process, Commercial Claims, Weather Records, Building Codes
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/how-to-document-hail-damage-for-an-insurance-claim/'],  // optional preferred related posts
    'sources'     => [['NOAA Storm Events Database', 'https://www.ncdc.noaa.gov/stormevents/']],  // posts: authoritative references
    // services only:
    'service_name'  => 'Hail Damage Claims',
    'related_posts' => ['/hail-damage-roof-insurance-claim-how-to-protect-your-roof/'],
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
  * `[[joseph-email]]` → linked jditt@risepublicadjusting.com (Joseph Dittman's direct email; use on contact/about/author pages, sparingly elsewhere).
  * `[[phone]]` → linked phone number; `[[email]]` → linked public email; `[[license]]` → `3356839`; `[[company]]` → Rise Public Adjusting LLC.
  * `[[form]]` — the full Free Claim Review form (only on contact-type pages).
* Images inside bodies: `<figure><img src="/wp-content/uploads/…" alt="…" width="1024" height="683" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`. Only use image paths that exist on disk (check with `ls`).
* Internal links: plain root-relative `href="/services/hail-damage-claims/"`. Link only to URLs listed in **URL inventory** below. 4–10 contextual internal links per article/service page.
* External links: only to authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, weather.gov, ncei.noaa.gov / ncdc.noaa.gov, fema.gov, floodsmart.gov, twia.org, sanantonio.gov, bexar.org, saws.org, census.gov). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners and business owners in San Antonio, Bexar County, and Greater San Antonio (Alamo Heights, Leon Valley, Helotes, Live Oak, Converse, Universal City, Schertz, Boerne, New Braunfels, etc.) dealing with property insurance claims. Professional but conversational; varied sentence length; plain English; no fluff. Better and more useful than the original copy.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If you are not sure something is true, leave it out or phrase it generally ("many policies", "may").
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage always depends on the policy and facts.
* Public adjusters are not attorneys: no legal advice; recommend a Texas attorney for legal questions (suits, bad faith, deadlines to sue).
* No physical office. Say "serving San Antonio, Bexar County, and surrounding communities".
* Remove the old copy's unsupported claims: "You pay nothing unless we increase your settlement", "Texas insurance policy loopholes", "We fight insurance companies", "aggressively", "maximize your payout" promises, "team of licensed public adjusters". Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keywords read naturally. Primary keyword "San Antonio Public Adjuster" (brand name too); secondary: "public adjuster in San Antonio", "San Antonio public adjusters", "Bexar County public adjuster", "San Antonio hail damage claims", "insurance claim help in San Antonio", "denied insurance claim San Antonio", "underpaid insurance claim San Antonio". Use the page's topic keyword in title, first paragraph, one H2, meta description. No stuffing.
* US spelling.
* Real local context: Bexar County hail season peaks April–May (NOAA: 618 hail reports since 1957, 203 of them 1.75"+, largest 5.5" on May 3, 2021 near Sayers/China Grove); the April 12, 2016 hailstorm across northwest San Antonio (hail to 4.5" near Tezel Rd & Bandera Rd; widely reported as one of the costliest hailstorms in Texas history — say "one of the costliest" without a dollar figure); 2001-05-06 hail/wind storm; downbursts (May 27, 1997 >100 mph near Kelly AFB); San Antonio sits in "Flash Flood Alley" along the Balcones Escarpment (420 NOAA flash-flood reports); October 1998 floods; Winter Storm Uri, February 2021 (wind chills to -5, burst pipes); ice storms Feb 2022, Jan 2025, Jan 2026; Hurricane Harvey remnants Aug 2017. Common local construction: slab-on-grade, composition shingle roofs, standing-seam metal roofs in the Hill Country edge, stucco/limestone/brick veneer, older pier-and-beam homes in historic districts (King William, Monte Vista, Tobin Hill), flat/low-slope commercial roofs; expansive clay soils. Water utility: SAWS. Electric/gas: CPS Energy. Do not invent other specifics.

## Verified facts you may cite

### Business
* San Antonio Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (use `[[phone]]`). Public email **info@publicadjustersanantonio.com** (use `[[email]]`). Joseph Dittman's direct email **jditt@risepublicadjusting.com** (use `[[joseph-email]]`). No other email addresses.
* Main CTA: **Free Claim Review** → `/free-claim-review/`.
* Author of every article: **Joseph Dittman, Licensed Texas Public Adjuster**. Verified bio: Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Works with TX Public Adjusting (txpublicadjusting.com). Nothing else about him (no years, counts, awards).
* Tools used in claim documentation: Xactimate estimating software, Matterport 3D imaging.

### Texas insurance law (cite generally; link to statutes.capitol.texas.gov or tdi.texas.gov)
* Public adjusters are licensed and regulated by the Texas Department of Insurance under **Texas Insurance Code Chapter 4102**.
* Public adjuster compensation may not exceed **10% of the insurance settlement** on the claim (Tex. Ins. Code §4102.104). If the insurer pays or commits in writing to pay policy limits within 72 hours after the loss is reported, the adjuster cannot take a percentage fee (reasonable hourly compensation only).
* Public adjuster contracts must use TDI-approved terms, let the client **rescind within 72 hours** of signing, and display "WE REPRESENT THE INSURED ONLY" (§4102.103/§4102.104; 28 TAC §19.708).
* A public adjuster may not participate in the repair/reconstruction of the property on a claim they adjust (conflict-of-interest rules, Tex. Ins. Code §4102.158 and §4102.163). Do not quote exact section numbers for this point other than "Chapter 4102".
* **Prompt Payment of Claims** (Tex. Ins. Code Chapter 542, Subchapter B): insurer generally has 15 days after notice of a claim to acknowledge it, begin its investigation, and request needed information (§542.055); 15 business days after receiving all requested items to accept or reject, or it may notify the policyholder it needs more time and then has up to 45 more days (§542.056); payment within 5 business days after notifying acceptance (§542.057). Deadlines are extended by 15 days after a weather-related catastrophe or major natural disaster declared by the commissioner (§542.059). Eligible surplus lines insurers have different (30 business day) timeframes.
* Weather-related claim lawsuits: Tex. Ins. Code **Chapter 542A** requires written pre-suit notice at least 61 days before filing suit. (Mention only as "consult an attorney"; no legal advice.)
* Many Texas property policies contain contractual deadlines to file suit (often two years and one day from when the claim accrued, per Tex. Civ. Prac. & Rem. Code §16.070). Tell readers to check their own policy and consult an attorney.
* **TWIA** (Texas Windstorm Insurance Association) covers windstorm/hail in the designated catastrophe area: Aransas, Brazoria, Calhoun, **Cameron**, Chambers, Galveston, Jefferson, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio, **Willacy**, and part of Harris County. **Bexar County is not in the TWIA area**, so San Antonio properties typically get wind/hail coverage from their regular insurer (or the Texas FAIR Plan where applicable). TDI windstorm (WPI-8) certification applies only in the TWIA area.
* Standard homeowners and commercial property policies generally **exclude flood**; flood coverage comes from the National Flood Insurance Program (NFIP) or private flood policies (floodsmart.gov). NFIP policies typically have a 30-day waiting period.
* Many Texas policies carry separate wind/hail deductibles, often a percentage of Coverage A (dwelling) limit; named-storm/hurricane deductibles may apply. Always "check your declarations page".
* Appraisal clause: either party can demand appraisal to resolve a disagreement over the **amount** of loss (not coverage); each side selects an appraiser and the appraisers select an umpire; an award agreed by any two is binding on amount (policy language controls).
* Replacement cost vs. actual cash value: ACV = replacement cost minus depreciation; under replacement-cost policies the insurer typically pays ACV first and releases recoverable depreciation after repairs are completed (often within a deadline stated in the policy). Some Texas roof coverage is ACV-only or uses roof payment schedules — check the policy.
* Ordinance or law coverage pays (up to its limit) for increased costs to comply with building codes when repairing covered damage; it is often a separate, limited coverage or endorsement.

### City of San Antonio building codes
* Permits and inspections: City of San Antonio **Development Services Department (DSD)**, Cliff Morton Development and Business Services Center, 1901 S. Alamo St. Permits through the city's online portal (BuildSA). Re-roofing and most structural repairs generally require a permit; confirm with DSD.
* Code edition: whoever writes `/local-building-codes/` MUST verify the currently adopted ICC edition and effective date from sanantonio.gov (WebSearch/WebFetch) and record it in `tools/notes/building-codes.md`; everyone else should say "the city's adopted International Residential Code and International Building Code" without naming an edition.
* Suburban cities (e.g. Alamo Heights, Leon Valley, Schertz, Boerne, New Braunfels) and unincorporated Bexar County have their own permit offices.
* Compliance requirements do **not** automatically mean the insurer must pay for code upgrades — that depends on ordinance or law coverage.

### Storm data
See `tools/notes/storm-facts.md` (summary) and `tools/notes/storm-facts-raw.txt` (verified NOAA NCEI records with event links). Cite NCEI event links when you use a specific event. Do not cite damage dollar figures.

## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/claim-tools/`, `/claim-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`, `/faq/`
Area pages: `/service-areas/alamo-heights/`, `/service-areas/boerne/`, `/service-areas/converse/`, `/service-areas/helotes/`, `/service-areas/leon-valley/`, `/service-areas/live-oak/`, `/service-areas/new-braunfels/`, `/service-areas/schertz/`, `/service-areas/universal-city/`

Services: `/services/hail-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/wind-damage-claims/`, `/services/storm-damage-claims/`, `/services/flood-damage-claims/`, `/services/freeze-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/water-damage-claims/`, `/services/residential-property-claims/`, `/services/commercial-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Existing articles (original URLs — keep exactly):
`/do-i-need-a-public-adjuster/` (2026-03-05), `/how-to-find-a-public-adjuster/` (2026-03-14), `/fire-insurance-adjuster/` (2026-03-24), `/hail-damage-roof-insurance-claim-how-to-protect-your-roof/` (2026-04-14), `/how-to-document-hail-damage-for-an-insurance-claim/` (2026-04-14), `/what-to-do-if-your-hail-claim-was-denied-in-texas/` (2026-04-14), `/hail-damage-claim-supplements-what-carriers-miss-in-their-scope-xactimate-insights/` (2026-04-15), `/public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas/` (2026-04-15)

New articles (date 2026-10-20):
`/san-antonio-hail-season-storm-data/`, `/wind-damage-insurance-claims-san-antonio-tx/`, `/flash-flood-damage-insurance-san-antonio/`, `/freeze-damage-burst-pipe-claims-san-antonio/`, `/replacement-cost-vs-actual-cash-value-texas/`, `/how-to-review-underpaid-roof-insurance-estimate/`, `/building-codes-insurance-repairs-san-antonio/`

## Images

* Existing articles keep their original featured image and inline images — originals are in `tools/original-content/<slug>.md` ("Images in body") and the featured image is listed below. Use the `-1024x683.webp` size for inline figures if it exists on disk (`ls site/wp-content/uploads/2026/*/`), else the full file. Featured `image` = full-size original.
  * do-i-need-a-public-adjuster → /wp-content/uploads/2026/03/Do-I-Need-A-Public-Adjuster.webp
  * how-to-find-a-public-adjuster → /wp-content/uploads/2026/03/How-to-Find-a-Public-Adjuster.webp
  * fire-insurance-adjuster → /wp-content/uploads/2026/03/Fire-Insurance-Adjuster-1.webp
  * hail-damage-roof-insurance-claim-how-to-protect-your-roof → /wp-content/uploads/2026/04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-1.webp
  * how-to-document-hail-damage-for-an-insurance-claim → /wp-content/uploads/2026/04/How-to-Document-Hail-Damage-for-an-Insurance-Claim-3.webp
  * what-to-do-if-your-hail-claim-was-denied-in-texas → /wp-content/uploads/2026/04/What-to-Do-If-Your-Hail-Claim-Was-Denied-in-Texas-1.webp
  * hail-damage-claim-supplements-… → /wp-content/uploads/2026/04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-1.webp
  * public-adjuster-vs-insurance-adjuster-… → /wp-content/uploads/2026/04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-3.webp
* New articles: `'image' => '/assets/img/featured/<slug>.webp'`. Service pages: `/assets/img/featured/service-<slug>.webp`. Pages: `/assets/img/featured/page-<slug>.webp` (area pages: `page-area-<city>.webp`). These are generated separately — just use the path. New articles may also use inline figures from the uploads folder (other photos on disk) when relevant; describe them accurately (see `tools/notes/photos.md`).

## Length targets

* Existing articles: rewrite and expand to **1,700–2,500 words** of body (keep the topic, keep useful original points, improve accuracy, add San Antonio context).
* New articles: **1,600–2,500 words**.
* Service pages: **900–1,400 words** body + 5–7 FAQs.
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
