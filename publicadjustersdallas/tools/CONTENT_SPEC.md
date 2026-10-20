# Content specification — Dallas Public Adjuster rebuild (publicadjustersdallas.com)

Every page, service page, and article is a PHP file that **returns an array**. The site
code (already written) renders the layout, hero, breadcrumbs, sidebar, FAQs (from the
`faqs` key), schema, CTA band, author box, and related posts. You only write data + body HTML.

Site root: `/home/user/seotool/publicadjustersdallas/site/`
Format reference (finished sister site, SAME engine, San Antonio): `/tmp/claude-0/-home-user-seotool/0b51aff2-7047-5f3c-828b-45ecba5cb983/scratchpad/sa-content/`
(`pages/`, `services/`, `posts/`). Read the matching file there for structure, keys and quality level — **never copy its San Antonio / Bexar facts, event IDs, or sentences**. Write fresh Dallas copy.
Original Dallas site copy (WordPress export, for topic/points to keep): `/home/user/seotool/publicadjustersdallas/tools/original-content/<slug>.md`

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, like the original WordPress permalinks) |

## File format (exact)

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claims in Dallas, TX',   // H1 + breadcrumb
    'seo_title'   => 'Dallas Hail Damage Claims | Public Adjuster Help',  // <title>, 45–62 chars, unique
    'description' => 'Meta description, 120–155 characters, unique, includes the main keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services only).',
    'kicker'      => 'Short eyebrow label, e.g. "Hail Damage Claims" (optional)',
    'image'       => '/assets/img/featured/service-hail-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'date'        => '2026-04-19',   // original publish date (existing posts) or 2026-10-20 (new)
    'updated'     => '2026-10-20',
    'category'    => 'Hail Claims',  // one of: Hail Claims, Roof Claims, Wind & Storm Claims, Tornado Claims, Flood Claims, Freeze Claims, Fire Claims, Water Damage Claims, Claim Process, Commercial Claims, Weather Records, Building Codes
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/document-hail-damage-for-an-insurance-claim/'],  // optional preferred related posts
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
* Check other keys used by the reference file of the same kind (e.g. `template`, `hide_hero_cta`, `breadcrumb_parent`, `schema_type`, `hero_compact`) and keep them — templates depend on them.

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
* Images inside bodies: `<figure><img src="/wp-content/uploads/…" alt="…" width="1024" height="683" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`. Only use image paths that exist on disk (check with `ls`). See `tools/notes/photos.md` for what each photo shows — describe images accurately.
* Internal links: plain root-relative `href="/services/hail-damage-claims/"`. Link only to URLs listed in **URL inventory** below. 4–10 contextual internal links per article/service page.
* External links: only to authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, texas.public.law is NOT allowed, weather.gov, ncei.noaa.gov / ncdc.noaa.gov, fema.gov, floodsmart.gov, twia.org, dallascityhall.com, dallascounty.org, dallasnow.dallascityhall.com, census.gov, iccsafe.org). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners and business owners in Dallas, Dallas County, and nearby North Texas cities (Highland Park, University Park, Richardson, Garland, Irving, Mesquite, Carrollton, Grand Prairie, Plano, Rowlett, plus Addison, Farmers Branch, Coppell, DeSoto, Cedar Hill, Duncanville, Lancaster, Sachse, Balch Springs) dealing with property insurance claims. Professional but conversational; varied sentence length; plain English; no fluff. Clearly better and more useful than the original copy.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If you are not sure something is true, leave it out or phrase it generally ("many policies", "may").
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage always depends on the policy and facts.
* Public adjusters are not attorneys: no legal advice; recommend a Texas attorney for legal questions (suits, bad faith, deadlines to sue).
* No physical office. Say "serving Dallas, Dallas County, and surrounding North Texas communities".
* Remove the old copy's unsupported claims: "You pay nothing unless we increase your settlement", "Texas insurance policy loopholes", "We fight insurance companies", "aggressively negotiated", "maximize your claim/payout" promises, "our team of licensed public adjusters". Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keywords read naturally. Primary keyword **"Dallas Public Adjuster"** (also the brand name); secondary: "public adjuster in Dallas", "Dallas public adjusters", "Dallas County public adjuster", "Dallas hail damage claims", "insurance claim help in Dallas", "denied insurance claim Dallas", "underpaid insurance claim Dallas", "public adjuster Dallas TX". Use the page's topic keyword in title, first paragraph, one H2, meta description. No stuffing.
* US spelling.
* Real local context you may use: North Texas sits in the southern Plains hail belt — Dallas County hail peaks April–May with a long March–June season and a secondary October bump (see `tools/notes/storm-facts.md` for exact NOAA counts and event IDs). Severe straight-line winds (May 28, 2024: up to 95 mph in Garland/Richardson), tornadoes (EF4 Garland/Rowlett Dec 26, 2015; EF3 north Dallas Oct 20, 2019), flash flooding (Aug 2022: upwards of 15" of rain in parts of Dallas), Winter Storm Uri (Feb 2021: single-digit lows, burst pipes), ice storms (Feb 2023, Jan 2025, Jan 2026). Common local construction: brick-veneer homes with composition shingle roofs; slab-on-grade foundations and older pier-and-beam homes in neighborhoods like Lakewood, the M Streets, Oak Cliff/Kessler Park, and Lower Greenville; Tudor and Craftsman houses in the Park Cities; mid-century ranches in Lake Highlands and Richardson; flat/low-slope TPO and modified-bitumen roofs on commercial buildings, apartments and warehouses; expansive Blackland Prairie clay soils (foundation movement is usually excluded unless caused by a covered peril — say "check your policy"). Waterways: Trinity River (levee system downtown), White Rock Creek and White Rock Lake, Turtle Creek, Five Mile and Ten Mile creeks, Rowlett Creek, Lake Ray Hubbard. Utilities: Dallas Water Utilities (City of Dallas), Oncor (electric delivery), Atmos Energy (natural gas). Do not invent other specifics (no neighborhood-level statistics, no claim counts).

## Verified facts you may cite

### Business
* Dallas Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (use `[[phone]]`; calls and texts). Public email **info@publicadjustersdallas.com** (use `[[email]]`) — every website form is delivered there. Joseph Dittman's direct email **jditt@risepublicadjusting.com** (use `[[joseph-email]]`). No other email addresses.
* Main CTA: **Free Claim Review** → `/free-claim-review/`.
* Author of every article: **Joseph Dittman, Licensed Texas Public Adjuster**. Verified bio: Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Works with TX Public Adjusting (txpublicadjusting.com). Nothing else about him (no years, counts, awards).
* Tools used in claim documentation: Xactimate estimating software, Matterport 3D imaging.

### Texas insurance law (cite generally; link to statutes.capitol.texas.gov or tdi.texas.gov)
* Public adjusters are licensed and regulated by the Texas Department of Insurance under **Texas Insurance Code Chapter 4102**.
* Public adjuster compensation may not exceed **10% of the insurance settlement** on the claim (Tex. Ins. Code §4102.104). If the insurer pays or commits in writing to pay policy limits within 72 hours after the loss is reported, the adjuster cannot take a percentage fee (reasonable hourly compensation only).
* Public adjuster contracts must use TDI-approved terms, let the client **rescind within 72 hours** of signing, and display "WE REPRESENT THE INSURED ONLY" (§4102.103/§4102.104; 28 TAC §19.708).
* A public adjuster may not participate in the repair/reconstruction of the property on a claim they adjust (conflict-of-interest rules in Chapter 4102). Do not quote section numbers for this point.
* **Prompt Payment of Claims** (Tex. Ins. Code Chapter 542, Subchapter B): insurer generally has 15 days after notice of a claim to acknowledge it, begin its investigation, and request needed information (§542.055); 15 business days after receiving all requested items to accept or reject, or it may notify the policyholder it needs more time and then has up to 45 more days (§542.056); payment within 5 business days after notifying acceptance (§542.057). Deadlines are extended by 15 days after a weather-related catastrophe or major natural disaster declared by the commissioner (§542.059). Eligible surplus lines insurers have different (30 business day) timeframes.
* Weather-related claim lawsuits: Tex. Ins. Code **Chapter 542A** requires written pre-suit notice at least 61 days before filing suit. (Mention only as "consult an attorney"; no legal advice.)
* Many Texas property policies contain contractual deadlines to file suit (often two years and one day from when the claim accrued, per Tex. Civ. Prac. & Rem. Code §16.070). Tell readers to check their own policy and consult an attorney.
* **TWIA** covers windstorm/hail only in the designated coastal catastrophe area (14 coastal counties and part of Harris County). **Dallas County is not in the TWIA area**, so Dallas properties typically get wind/hail coverage from their regular insurer (or the Texas FAIR Plan where applicable). Mention only when relevant.
* Standard homeowners and commercial property policies generally **exclude flood**; flood coverage comes from the National Flood Insurance Program (NFIP) or private flood policies (floodsmart.gov). NFIP policies typically have a 30-day waiting period.
* Many Texas policies carry separate wind/hail deductibles, often a percentage of Coverage A (dwelling) limit (e.g. 1% or 2%). Always "check your declarations page".
* Appraisal clause: either party can demand appraisal to resolve a disagreement over the **amount** of loss (not coverage); each side selects an appraiser and the appraisers select an umpire; an award agreed by any two is binding on amount (policy language controls).
* Replacement cost vs. actual cash value: ACV = replacement cost minus depreciation; under replacement-cost policies the insurer typically pays ACV first and releases recoverable depreciation after repairs are completed (often within a deadline stated in the policy). Some Texas roof coverage is ACV-only or uses roof payment schedules, and some policies have cosmetic-damage exclusions for metal roofing — check the policy.
* Ordinance or law coverage pays (up to its limit) for increased costs to comply with building codes when repairing covered damage; it is often a separate, limited coverage or endorsement.

### City of Dallas building codes
* Permits and inspections: City of Dallas **Development Services Department**, Oak Cliff Municipal Center, 320 E. Jefferson Blvd. Permits are applied for online through the city's permitting portal (DallasNow). Re-roofing and most structural repairs generally require a permit; confirm with Development Services.
* Code edition: whoever writes `/local-building-codes/` MUST verify the currently adopted ICC edition and effective date (and the current permit portal name and office address) from dallascityhall.com (WebSearch/WebFetch) and record findings in `tools/notes/building-codes.md`; everyone else should say "the city's adopted International Residential Code and International Building Code" without naming an edition, and say "the City of Dallas Development Services Department" without an address.
* Suburban cities (Highland Park, University Park, Richardson, Garland, Irving, Mesquite, Carrollton, Grand Prairie, Plano, Rowlett, etc.) have their own building inspection/permit offices.
* Compliance requirements do **not** automatically mean the insurer must pay for code upgrades — that depends on ordinance or law coverage.

### Storm data
See `tools/notes/storm-facts.md` (verified NOAA NCEI facts with event IDs). Event link format: `https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=<number>`. You may also query `site/data/storm-history.json` (fields: id "ncei-<n>", type, date, loc, hail_in, wind_mph, tor_scale, text, url) with python for more Dallas-area events — cite only what the data says. Do not cite damage dollar figures or death tolls.

## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/claim-tools/`, `/claim-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`, `/faq/`, `/sitemap/`
Area pages: `/service-areas/highland-park/`, `/service-areas/university-park/`, `/service-areas/richardson/`, `/service-areas/garland/`, `/service-areas/irving/`, `/service-areas/mesquite/`, `/service-areas/carrollton/`, `/service-areas/grand-prairie/`, `/service-areas/plano/`, `/service-areas/rowlett/`

Services: `/services/hail-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/wind-damage-claims/`, `/services/tornado-damage-claims/`, `/services/storm-damage-claims/`, `/services/flood-damage-claims/`, `/services/freeze-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/water-damage-claims/`, `/services/residential-property-claims/`, `/services/commercial-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Existing articles (original URLs — keep exactly; date = original publish date):
`/what-is-a-public-claims-adjuster/` (2026-02-09), `/knowing-when-to-call-a-public-adjuster/` (2026-03-13), `/fire-insurance-adjuster/` (2026-03-24), `/hail-damage-roof-insurance-claim-how-to-protect-your-roof/` (2026-04-19), `/document-hail-damage-for-an-insurance-claim/` (2026-04-19), `/what-to-do-if-your-hail-claim-was-denied-in-texas/` (2026-04-19), `/hail-damage-claim-supplements-what-carriers-miss-in-their-scope/` (2026-04-19), `/public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas/` (2026-04-20)

New articles (date 2026-10-20 — stagger: use 2026-10-06, 2026-10-08, 2026-10-10, 2026-10-12, 2026-10-14, 2026-10-16, 2026-10-18, 2026-10-20 in the order listed):
`/dallas-hail-season-storm-data/`, `/wind-damage-insurance-claims-dallas-tx/`, `/tornado-damage-insurance-claims-dallas/`, `/flash-flood-damage-insurance-dallas/`, `/freeze-damage-burst-pipe-claims-dallas/`, `/replacement-cost-vs-actual-cash-value-texas/`, `/how-to-review-underpaid-roof-insurance-estimate/`, `/building-codes-insurance-repairs-dallas/`

## Images

* Existing articles keep their original featured image and inline images. Featured `image` = full-size original:
  * what-is-a-public-claims-adjuster → /wp-content/uploads/2026/02/What-Is-a-Public-Claims-Adjuster.webp (inline candidates: 02/Are-Public-Adjusters-Worth-It, 02/How-to-Find-a-Public-Adjuster, 02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster)
  * knowing-when-to-call-a-public-adjuster → /wp-content/uploads/2026/03/The-Moment-That-Changes-Your-Claim-Knowing-When-to-Call-a-Public-Adjuster.webp (inline: 03/Benefits-of-Hiring-a-Public-Adjuster, 03/The-Key-Differences-Between-Adjuster-Types)
  * fire-insurance-adjuster → /wp-content/uploads/2026/03/Fire-Insurance-Adjuster.webp (inline: Fire-Insurance-Adjuster-2, -3)
  * hail-damage-roof-insurance-claim-how-to-protect-your-roof → /wp-content/uploads/2026/04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-1.png (inline: -2.png, -3.png, -4.png)
  * document-hail-damage-for-an-insurance-claim → /wp-content/uploads/2026/04/Document-Hail-Damage-for-an-Insurance-Claim-1.webp (inline: -2, -3, -5)
  * what-to-do-if-your-hail-claim-was-denied-in-texas → /wp-content/uploads/2026/04/What-to-Do-If-Your-Hail-Claim-Was-Denied-in-Texas-1.webp (inline: -2, -3, -4)
  * hail-damage-claim-supplements-what-carriers-miss-in-their-scope → /wp-content/uploads/2026/04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-1.webp (inline: -2, -3, -4)
  * public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas → /wp-content/uploads/2026/04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-2.webp (inline: -1-1, the un-numbered one)
  For inline figures use the `-1024x683` size if it exists on disk (PNGs: check), else the full file.
* New articles: `'image' => '/assets/img/featured/<slug>.webp'`. Service pages: `/assets/img/featured/service-<slug>.webp`. Pages: `/assets/img/featured/page-<slug>.webp` (area pages: `page-area-<city>.webp`, author: `page-author-joseph-dittman.webp`). These are generated separately — just use the path. New articles may also use one or two inline figures from the uploads folder when relevant.

## Length targets

* Existing articles: rewrite and expand to **1,700–2,500 words** of body (keep the topic and the useful original points, improve accuracy, add Dallas context). Do NOT reuse original sentences.
* New articles: **1,600–2,500 words**.
* Service pages: **900–1,400 words** body + 5–7 FAQs.
* Area pages: **700–1,100 words** + 4–6 FAQs, with real NOAA events for that city from storm-history.json.
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
