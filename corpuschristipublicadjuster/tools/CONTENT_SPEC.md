# Content specification — Corpus Christi Public Adjuster rebuild

Every page, service page, area page, and article is a PHP file that **returns an array**. The site
code (already written) renders the layout, hero, breadcrumbs, sidebar, FAQs (from the `faqs` key),
schema, CTA band, author box, and related posts. You only write data + body HTML.

Site root: `/home/user/seotool/corpuschristipublicadjuster/site/`

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, same as the original WordPress permalinks) |

Area pages are pages named `service-areas__<slug>.php` → `/service-areas/<slug>/`.

## File format (exact)

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claims in Corpus Christi, TX',   // H1 + breadcrumb
    'seo_title'   => 'Corpus Christi Hail Damage Claims | Public Adjuster',  // <title>, 50–62 chars, unique
    'description' => 'Meta description, 130–155 characters, unique, includes the page keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services/areas).',
    'kicker'      => 'Short eyebrow label, e.g. "Hail Damage Claims" (optional)',
    'image'       => '/assets/img/featured/service-hail-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'date'        => '2026-04-23',   // original publish date (existing posts) or the date given in your brief (new)
    'updated'     => '2026-10-22',
    'category'    => 'Hail Claims',  // one of: Hail Claims, Roof Claims, Wind & Storm Claims, Hurricane Claims, TWIA & Windstorm, Fire Claims, Water & Flood Claims, Claim Process, Commercial Claims, Weather Records
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/document-hail-damage-for-an-insurance-claim/'],  // optional preferred related posts
    'sources'     => [['NOAA Storm Events Database', 'https://www.ncdc.noaa.gov/stormevents/']],  // posts: 2–5 authoritative references
    // services only:
    'service_name'  => 'Hail Damage Claims',
    'related_posts' => ['/hail-damage-roof-insurance-claim/'],
    'cta_heading'   => 'Hail damage claim questions?',   // optional
    'order'       => 10,
    // area pages only:
    'breadcrumb_parent' => ['Areas We Serve', '/service-areas/'],
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
* `<h2>` for main sections, `<h3>` for sub-sections. Logical order, no skipped levels.
* Allowed: `<p>`, `<ul>/<ol>/<li>`, `<table>` with `<thead>/<tbody>`, `<blockquote>`, `<strong>`, `<em>`, `<a>`, `<figure><img …><figcaption>`.
* Styled boxes:
  * `<div class="key-takeaways"><h2>Key takeaways</h2><ul>…</ul></div>` — at the very top of articles.
  * `<div class="callout"><span class="callout-title">Title</span><p>…</p></div>` (variants `callout callout-gold`, `callout callout-warn`).
* Shortcodes (literal, on their own line):
  * `[[cta]]` — mid-content Free Claim Review band (once in long pieces, roughly in the middle).
  * `[[cta-storm]]` — "Did a Recent Storm Damage Your Property?" band (storm/weather topics).
  * `[[phone]]` linked phone; `[[email]]` linked public email (info@corpuschristipublicadjuster.com);
    `[[author-email]]` linked direct email for Joseph Dittman (jditt@risepublicadjusting.com);
    `[[license]]` → 3356839; `[[company]]` → Rise Public Adjusting LLC.
  * `[[form]]` — the full Free Claim Review form (only on contact-type pages).
* Images in bodies: `<figure><img src="/wp-content/uploads/…-1024x683.webp" alt="…" width="1024" height="683" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`.
  Only use files that exist (`ls site/wp-content/uploads/2026/*/`).
* Internal links: root-relative, only to URLs in the **URL inventory** below. 5–10 contextual internal links per article/service page.
* External links: only authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, texreg.sos.state.tx.us, twia.org, texasfairplan.org, weather.gov, nhc.noaa.gov, ncei.noaa.gov / ncdc.noaa.gov, tidesandcurrents.noaa.gov, fema.gov, floodsmart.gov, corpuschristitx.gov, tcss.legis.texas.gov, census.gov). Note: the City of Corpus Christi moved from cctexas.com to corpuschristitx.gov; for statute text link tcss.legis.texas.gov (see local-facts.md). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners and business owners in Corpus Christi, Nueces County, and the Coastal Bend (Portland, Rockport, Port Aransas, Aransas Pass, Ingleside, Robstown, Kingsville, Padre Island, Calallen, Flour Bluff) with property insurance claims. Professional, warm, plain English, varied sentence length, no fluff, no filler intros.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If unsure, leave it out or phrase generally ("many policies", "may").
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage depends on the policy and facts.
* Public adjusters are not attorneys: no legal advice; suggest consulting a Texas attorney for lawsuits, bad faith, or deadlines to sue.
* No physical office claims. Say "serving Corpus Christi, Nueces County, and surrounding Coastal Bend communities".
* Remove the old copy's unsupported claims: "You pay nothing unless we increase your settlement", "Texas insurance policy loopholes", "aggressively", "fight insurance companies", "maximize payout" promises, "team of licensed public adjusters". Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keywords must read naturally. Primary keyword **"Corpus Christi Public Adjuster"** (brand + keyword). Secondary: "public adjuster in Corpus Christi", "Corpus Christi hurricane damage claims", "TWIA claim help", "Nueces County public adjuster", "Coastal Bend public adjuster", "denied insurance claim Corpus Christi", "underpaid insurance claim Corpus Christi", "Corpus Christi hail damage claims". Use the page's own topic keyword in the title, first paragraph, one H2, and the meta description. No stuffing.
* US spelling. Write "Coastal Bend". Accents: none needed.
* Local context should be real (see the facts files): hurricane exposure (Celia 1970, Harvey 2017, Hanna 2020, Tropical Storm Harold 2023), storm surge on the bays and barrier islands, wind-driven rain, salt-air corrosion, the May 8, 2025 derecho-style windstorm (NWS-estimated 105–115 mph gusts around Petronila/Driscoll/Agua Dulce), hail peaking in April–May, flash flooding, the February 2021 freeze; TWIA as the wind/hail insurer of last resort for most coastal properties; NFIP for flood; common construction: slab-on-grade homes, composition shingles, metal roofs, stucco/brick veneer/fiber cement, elevated homes on the islands, low-slope commercial roofs.

## Verified facts you may cite

### Business
* Corpus Christi Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (`[[phone]]`, call or text). Public email **info@corpuschristipublicadjuster.com** (`[[email]]`) — every form submission goes there.
* People who want to reach Joseph Dittman directly can email **jditt@risepublicadjusting.com** (`[[author-email]]`). Mention it on contact/author-type pages only (and optionally once in an article's closing paragraph), not everywhere.
* Main call to action: **Free Claim Review** → `/free-claim-review/`.
* Author of every article: **Joseph Dittman, Licensed Public Adjuster**. Verified bio: Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Do not add anything else about him (no years, no counts, no awards).
* Tools commonly used in claim documentation: Xactimate estimating software, Matterport 3D imaging, drones/roof photos (generic).

### Texas insurance law and TWIA
Read `tools/notes/local-facts.md` (researched 2026-10-22 with sources) for: Texas Insurance Code Chapter 4102 (public adjusters, 10% cap, 72-hour rescission, "WE REPRESENT THE INSURED ONLY"), Chapter 542 prompt-payment deadlines, Chapter 542A pre-suit notice, TWIA claim deadlines and dispute process (Chapter 2210), WPI-8 windstorm certificates, NFIP basics, City of Corpus Christi building codes and permits, hurricane history. **Only cite numbers/deadlines that appear there.** If a fact is marked UNVERIFIED, do not use it.
General points that are safe:
* Standard homeowners and commercial policies generally exclude flood; flood coverage comes from NFIP or private flood policies (floodsmart.gov). NFIP usually has a 30-day waiting period.
* TWIA covers wind and hail (not flood) for eligible properties in the designated catastrophe area, which includes Nueces, San Patricio, Aransas, and Kleberg counties. Many coastal homeowners therefore have **three** policies: a homeowners policy that excludes wind/hail, a TWIA windstorm policy, and a flood policy. Wind vs. water (surge/flood) disputes are common after hurricanes.
* Many Texas policies carry separate wind/hail or named-storm deductibles, often a percentage of Coverage A; check the declarations page.
* Appraisal clause: resolves disagreements over the **amount** of loss, not coverage; each side picks an appraiser, appraisers pick an umpire; an award agreed by any two is binding on amount (policy language controls).
* RCV vs. ACV: ACV = replacement cost minus depreciation; under RCV policies the insurer typically pays ACV first and releases recoverable depreciation after repairs (within a deadline in the policy).
* Ordinance or law coverage pays (up to its limit) for increased costs of code compliance; code requirements alone don't create coverage.

### Storm data
`tools/notes/storm-facts.md` is generated from the NOAA NCEI Storm Events Database (Nueces, San Patricio, Aransas, Kleberg counties). Cite NCEI event links when you use a specific event. Do not cite damage dollar figures. Counts are reports, not storm days.

## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/faq/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/hurricane-season-guide/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/claim-tools/`, `/claim-calculator/`, `/hurricane-deductible-calculator/`, `/claim-deadline-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`, `/sitemap/`

Area pages: `/service-areas/portland-tx/`, `/service-areas/rockport-tx/`, `/service-areas/port-aransas-tx/`, `/service-areas/aransas-pass-tx/`, `/service-areas/ingleside-tx/`, `/service-areas/padre-island-tx/`, `/service-areas/robstown-tx/`, `/service-areas/kingsville-tx/`

Services: `/services/hurricane-damage-claims/`, `/services/twia-windstorm-claims/`, `/services/wind-damage-claims/`, `/services/hail-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/storm-damage-claims/`, `/services/flood-damage-claims/`, `/services/water-damage-claims/`, `/services/mold-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/residential-property-claims/`, `/services/commercial-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Original articles (URLs must stay exactly as they are):
`/document-hail-damage-for-an-insurance-claim/`, `/hail-claim-was-denied-in-texas/`, `/hail-damage-claim-supplements-what-carriers-miss-in-their-scope/`, `/hail-damage-roof-insurance-claim/`, `/questions-about-public-adjusters/`, `/fire-insurance-adjuster/`, `/public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas/`

New articles:
`/hurricane-damage-claims-corpus-christi-guide/`, `/twia-claim-process-corpus-christi/`, `/wind-vs-storm-surge-damage-claims-texas-coast/`, `/named-storm-hurricane-deductibles-texas/`, `/windstorm-certificate-wpi-8-insurance-claims/`, `/wind-damage-insurance-claims-corpus-christi-tx/`, `/water-damage-vs-flood-damage-corpus-christi/`, `/replacement-cost-vs-actual-cash-value-texas/`, `/why-property-insurance-claims-are-delayed-texas/`, `/how-to-review-underpaid-roof-insurance-estimate/`, `/document-commercial-property-damage-after-storm/`, `/freeze-damage-burst-pipe-claims-corpus-christi/`, `/noaa-weather-records-document-property-damage-corpus-christi/`, `/corpus-christi-storm-history-hail-wind-hurricanes/`

## Images

* Original articles keep their original featured image and inline images (`/wp-content/uploads/2026/…`; see `tools/original-content/<slug>.html`). Featured `image` = full-size original (no size suffix); inline figures use the `-1024x683.webp` size.
* New articles: `'image' => '/assets/img/featured/<slug>.webp'`.
* Service pages: `'image' => '/assets/img/featured/service-<slug>.webp'`.
* Pages: `'image' => '/assets/img/featured/page-<slug>.webp'` (area pages: `page-area-<slug>.webp`). These are generated separately; just use the path.

## Length targets

* Original articles: rewrite and expand to **1,700–2,500 words** (keep the topic and useful original points, improve accuracy, localize to Corpus Christi).
* New articles: **1,600–2,500 words**.
* Service pages: **1,000–1,500 words** body + 5–7 FAQs.
* Area pages: **800–1,200 words** body + 4–5 FAQs, genuinely local (neighborhoods, county, TWIA/flood context, storms from storm-facts.md for that county).
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
