# Content specification — Port Arthur Public Adjuster rebuild

Every page, service page, and article is a PHP file that **returns an array**. The site
code renders the layout, hero, breadcrumbs, sidebar, FAQs (from the `faqs` key), schema,
CTA band, author box, and related posts. Writers only supply data + body HTML.

Site root: `/home/user/seotool/portarthurpublicadjuster/site/`

| Type     | Folder               | URL                          |
|----------|----------------------|------------------------------|
| Page     | `content/pages/`     | `/<filename>/` (`a__b.php` → `/a/b/`) |
| Service  | `content/services/`  | `/services/<filename>/`      |
| Article  | `content/posts/`     | `/<filename>/` (root level, like the original WordPress permalinks) |

## File format (exact)

```php
<?php
return [
    'title'       => 'Hurricane Damage Insurance Claims in Port Arthur, TX',   // H1 + breadcrumb
    'seo_title'   => 'Port Arthur Hurricane Damage Claims | Public Adjuster',  // <title>, 50–62 chars, unique
    'description' => 'Meta description, 120–155 characters, unique, includes the page keyword naturally.',
    'lead'        => 'One or two sentence intro shown under the H1 in the hero (pages/services only).',
    'kicker'      => 'Short eyebrow label, e.g. "Hurricane Claims" (optional)',
    'image'       => '/assets/img/featured/service-hurricane-damage-claims.webp',
    'image_alt'   => 'Descriptive alt text of the image',
    // posts only:
    'date'        => '2026-10-20',
    'updated'     => '2026-10-20',
    'category'    => 'Hurricane Claims',
    'excerpt'     => '1–2 sentence card summary (≤ 200 chars).',
    'related'     => ['/twia-windstorm-claim-guide-port-arthur/'],  // optional preferred related posts
    'sources'     => [['National Weather Service Lake Charles — Hurricane Harvey', 'https://www.weather.gov/lch/2017Harvey']],
    // services only:
    'service_name'  => 'Hurricane Damage Claims',
    'related_posts' => ['/hurricane-damage-insurance-claim-port-arthur/'],
    'cta_heading'   => 'Hurricane claim questions?',   // optional
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
* `<h2>` for main sections, `<h3>` for sub-sections. Logical order, no skipped levels.
* Allowed: `<p>`, `<ul>/<ol>/<li>`, `<table>` with `<thead>/<tbody>`, `<blockquote>`, `<strong>`, `<em>`, `<a>`, `<figure><img …><figcaption>`.
* Styled boxes:
  * `<div class="key-takeaways"><h2>Key takeaways</h2><ul>…</ul></div>` — at the very top of articles.
  * `<div class="callout"><span class="callout-title">Title</span><p>…</p></div>` (variants: `callout callout-gold`, `callout callout-warn`).
* Shortcodes (literally, on their own line):
  * `[[cta]]` — mid-content Free Claim Review band (once in long pieces, roughly in the middle).
  * `[[cta-storm]]` — "Did a Recent Storm Damage Your Property?" band (storm/weather topics).
  * `[[phone]]` → linked phone; `[[email]]` → linked public email; `[[license]]` → `3356839`; `[[company]]` → Rise Public Adjusting LLC.
  * `[[form]]` — the full Free Claim Review form (only on contact-type pages).
* Inline images: `<figure><img src="/assets/img/photos/<file>.webp" alt="…" width="1536" height="1024" loading="lazy" decoding="async"><figcaption>…</figcaption></figure>`. Only use files that exist (`ls site/assets/img/photos/`). All photos there are 1536×1024 except `roof-inspection-brick-home.webp` (640×427). One or two figures per article/service page is plenty; don't reuse the same photo twice on a page.
* Internal links: root-relative `href="/services/hurricane-damage-claims/"`. Link only to URLs in the **URL inventory** below. 4–10 contextual internal links per article/service page.
* External links: only authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, twia.org, weather.gov, nhc.noaa.gov, ncei.noaa.gov / ncdc.noaa.gov, fema.gov, floodsmart.gov, portarthurtx.gov, co.jefferson.tx.us, census.gov, texasfairplan.org). Add `target="_blank" rel="noopener"`.

## Writing rules (very important)

* Audience: homeowners, landlords and business owners in **Port Arthur, Jefferson County, and the Golden Triangle / Southeast Texas** (Beaumont, Nederland, Groves, Port Neches, Sabine Pass, Orange, Bridge City, Pleasure Island) dealing with property insurance claims. Professional but conversational; varied sentence length; plain English; no fluff, no filler intros.
* **Never invent** facts, statistics, testimonials, reviews, awards, settlement amounts, client counts, years in business, case results, team size, office address, or certifications. If unsure, leave it out or phrase generally ("many policies", "may"). If you want to use a fact not listed below, verify it on an official source first (you have WebFetch/WebSearch) and cite it.
* **No guarantees.** Never promise a higher settlement, approval, or outcome. Use "may", "can help", "often". Coverage always depends on the policy and facts.
* Public adjusters are not attorneys: no legal advice; recommend a Texas attorney for legal questions (suits, bad faith, deadlines to sue).
* No physical office claims. Say "serving Port Arthur, Jefferson County, and surrounding Southeast Texas communities".
* Remove the old copy's unsupported claims: "We fight insurance companies", "You pay nothing unless we increase your settlement", "No upfront fees — we only get paid if we recover", "Texas insurance policy loopholes", "relentless", "pursued aggressively", "team of licensed public adjusters". Fee wording: "Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement."
* Keywords must read naturally. Primary keyword **"Port Arthur Public Adjuster"** (brand + keyword). Secondary: "public adjuster in Port Arthur", "Port Arthur public adjusters", "Jefferson County public adjuster", "Southeast Texas public adjuster", "Port Arthur hurricane damage claim", "TWIA claim Port Arthur", "denied insurance claim Port Arthur", "underpaid insurance claim Port Arthur", "insurance claim help in Port Arthur". Put the page's own topic keyword in the H1/title, first paragraph, one H2, and meta description. No stuffing (primary keyword 2–5× on inner pages).
* US spelling. "Golden Triangle" = Beaumont–Port Arthur–Orange. "Southeast Texas" is fine.
* Local context must be real: Gulf Coast hurricane and tropical storm exposure, storm surge, wind-driven rain, extreme rainfall flooding, severe thunderstorms with straight-line winds and occasional hail, tornadoes in tropical systems, the February 2021 freeze, high humidity → fast mold growth after water losses; refinery/petrochemical industry and port (business interruption); common construction: slab and pier-and-beam homes, composition shingle roofs, vinyl/fiber-cement/brick veneer, older housing stock in many neighborhoods, metal buildings for commercial/industrial, low-slope commercial roofs. The city's hurricane flood protection levee/seawall system reduces surge risk but does not stop rainfall flooding.

## Verified facts you may cite

### Business
* Port Arthur Public Adjuster — a public adjusting service of **Rise Public Adjusting LLC**, Texas Department of Insurance license **#3356839**.
* Phone **+1 (832) 503-5866** (use `[[phone]]`). Public email **info@portarthurpublicadjuster.com** (use `[[email]]`). Never show any other email address.
* Main call to action: **Free Claim Review** → `/free-claim-review/`.
* Author of every article: **Joseph Dittman, licensed public adjuster**. Verified bio: Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness; experience across residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses; background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience. Nothing else (no years, counts, awards).
* Tools commonly used in claim documentation: Xactimate estimating software, Matterport 3D imaging, moisture meters/thermal imaging (general practice).

### Texas insurance law (cite generally; link statutes.capitol.texas.gov or tdi.texas.gov)
* Public adjusters are licensed and regulated by TDI under **Texas Insurance Code Chapter 4102**.
* Compensation may not exceed **10% of the insurance settlement** (Tex. Ins. Code §4102.104). If the insurer pays or commits in writing to pay policy limits within 72 hours after the loss is reported, no percentage fee (reasonable hourly compensation only).
* Contracts must use TDI-approved terms, allow the client to **rescind within 72 hours** of signing, and state "WE REPRESENT THE INSURED ONLY".
* A public adjuster may not participate in repair/reconstruction of the property on a claim they adjust (Chapter 4102 conflict-of-interest rules).
* **Prompt Payment of Claims** (Tex. Ins. Code Ch. 542, Subch. B): generally 15 days after notice to acknowledge, begin investigating, and request information (§542.055); 15 business days after receiving all requested items to accept or reject, or notify it needs more time (up to 45 more days) (§542.056); payment within 5 business days after acceptance (§542.057). Extended by 15 days after a weather-related catastrophe declared by the commissioner (§542.059). Surplus lines insurers differ.
* Weather-related claim lawsuits: **Chapter 542A** requires written pre-suit notice at least 61 days before suit (mention only as "consult an attorney").
* Many policies set a contractual deadline to sue (often two years and one day, Tex. Civ. Prac. & Rem. Code §16.070). Tell readers to check their policy and consult an attorney.
* Standard homeowners/commercial policies generally **exclude flood** (including storm surge and rising water); flood coverage comes from the NFIP or private flood policies (floodsmart.gov). NFIP policies generally have a 30-day waiting period. NFIP claims: proof of loss generally due within 60 days of the loss (floodsmart.gov) — verify wording before citing.
* Appraisal clause: either side may demand appraisal over the **amount** of loss (not coverage); each picks an appraiser; the appraisers pick an umpire; an award agreed by two is binding on amount (policy language controls).
* RCV vs ACV: ACV = replacement cost minus depreciation; under RC policies the insurer typically pays ACV first and releases recoverable depreciation after repairs (deadline in policy). Some Texas roof coverage is ACV-only or uses roof payment schedules.
* Ordinance or law coverage pays (up to its limit) for increased costs to comply with codes; often a separate, limited coverage.
* Many Texas policies carry separate wind/hail and named-storm/hurricane deductibles, often a **percentage of Coverage A** (e.g., 1%, 2%, 5%). Always "check your declarations page".

### TWIA (Texas Windstorm Insurance Association) — important for Port Arthur
* **Jefferson County is a TWIA first-tier coastal county** (with Aransas, Brazoria, Calhoun, Cameron, Chambers, Galveston, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio, Willacy, and parts of Harris County east of SH 146: La Porte, Morgan's Point, Pasadena, Seabrook, Shoreacres). Source: tdi.texas.gov/wind/generalquestio.html. **Orange County is not** in the TWIA catastrophe area.
* TWIA is the insurer of last resort for **wind and hail** in that area; many Port Arthur homeowners carry a homeowners policy that excludes wind/hail plus a separate TWIA policy, plus a separate flood policy. A single hurricane can therefore involve **two or three claims** with different adjusters and deductibles.
* TDI Windstorm Inspection Program: structures, additions and **repairs including re-roofs and roof repairs** in the catastrophe area must be built and inspected to TDI's specifications to be eligible for TWIA coverage; TDI issues a **WPI-8 Certificate of Compliance** (tdi.texas.gov/wind/). Proof of TDI inspection enrollment (WPI-1) may be required before a building permit in cities that adopted TDI's standard.
* TWIA claim timelines (Tex. Ins. Code Ch. 2210, Subch. L-1 — verify on twia.org before citing specific numbers): claims generally must be filed within one year of the date of loss (extension possible for good cause); TWIA has set deadlines to accept or deny; disputes over the amount can go to appraisal; litigation is restricted with special notice rules. Recommend a Texas attorney for disputes about coverage denials.
* Texas FAIR Plan Association offers limited homeowners coverage for people who can't find it elsewhere (texasfairplan.org).

### City of Port Arthur building codes (verified 2026-10-20 at portarthurtx.gov/502/Inspections-and-Permitting)
* The Building Inspections Division operates under the **2021 International Residential Code, 2021 International Building Code, 2021 International Plumbing Code, 2021 International Mechanical Code, and the 2020 National Electrical Code**.
* Permit techs: **(409) 983-8261**. City Hall: **444 4th Street, Port Arthur, TX 77640**; main line (409) 983-8100; hours 8:00 am–5:00 pm. Online permit portal (Tyler EnerGov): https://portarthurtx-energovweb.tylerhost.net/apps/SelfService#/home . The division does not accept online payments; don't email plans directly to the building official.
* Re-roofing and structural repairs generally need a city permit — tell readers to confirm scope with the Building Inspections Division. In Jefferson County, windstorm (TDI/WPI-8) requirements also apply for TWIA eligibility. Do not quote fees or design wind speeds.
* Code compliance does **not** automatically mean the insurer pays for upgrades — depends on ordinance or law coverage.

### Storm history (verified)
* **Hurricane Rita** — landfall September 24, 2005 near the Texas/Louisiana border (Sabine Pass / Johnson's Bayou area) as a Category 3; widespread wind damage across Southeast Texas including Port Arthur. (NHC Tropical Cyclone Report AL182005.)
* **Hurricane Humberto** — September 13, 2007, landfall near High Island; wind damage in the Port Arthur/Beaumont area.
* **Hurricane Ike** — landfall September 13, 2008 at Galveston (Category 2); large storm surge along the upper Texas coast including Sabine Pass and low-lying Jefferson County; wind damage across the region.
* **Hurricane Harvey (2017)** — per NWS Lake Charles (weather.gov/lch/2017Harvey): heavy rain over Jefferson County from August 24–31, 2017; widespread storm totals over **40 inches**; the highest storm total reported from Harvey was **60.58 inches near Nederland**, a U.S. tropical cyclone rainfall record at the time; **more than 64,000 homes flooded in Jefferson County**; Port Arthur, Groves and northeast Beaumont among the hardest hit; record crests on Pine Island Bayou and the lower Neches River.
* **Tropical Storm Imelda** — September 17–19, 2019; extreme rainfall (more than 40 inches in parts of Jefferson County, preliminary) and widespread flash flooding across Southeast Texas, including Port Arthur and Beaumont areas. Ranked by NWS Houston among the wettest tropical cyclones in Texas.
* **Hurricane Laura** — landfall August 27, 2020 near Cameron, Louisiana (Category 4), ~30 miles east of the Texas border; damaging winds in eastern Jefferson and Orange counties. **Hurricane Delta** — October 9, 2020 near Creole, Louisiana.
* **February 2021 winter storm** — prolonged freeze across Texas; burst pipes statewide.
* Hurricane season: June 1–November 30 (NHC); peak activity mid-August through September.
* Storm-history counts (hail/wind reports) come live from the site's NOAA dataset — don't quote counts in prose.

## URL inventory (link only to these)

Pages: `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/free-claim-review/`, `/faq/`, `/privacy-policy/`, `/terms-of-use/`, `/author/joseph-dittman/`, `/local-building-codes/`, `/storm-history/`, `/weather-events/`, `/weather/`, `/hurricane-tracker/`, `/hurricane-deductible-calculator/`, `/claim-tools/`, `/claim-calculator/`, `/claim-documentation-checklist/`, `/storm-lookup/`, `/service-areas/`, `/service-areas/beaumont/`, `/service-areas/nederland/`, `/service-areas/groves/`, `/service-areas/port-neches/`, `/service-areas/sabine-pass/`, `/service-areas/orange/`

Services: `/services/hurricane-damage-claims/`, `/services/twia-windstorm-claims/`, `/services/wind-damage-claims/`, `/services/flood-damage-claims/`, `/services/storm-damage-claims/`, `/services/roof-damage-insurance-claims/`, `/services/hail-damage-claims/`, `/services/water-damage-claims/`, `/services/mold-damage-claims/`, `/services/fire-damage-claims/`, `/services/smoke-damage-claims/`, `/services/residential-property-claims/`, `/services/commercial-property-claims/`, `/services/denied-insurance-claims/`, `/services/underpaid-insurance-claims/`, `/services/delayed-insurance-claims/`, `/services/insurance-claim-supplements/`, `/services/insurance-appraisal/`, `/services/insurance-estimate-review/`

Articles (all by Joseph Dittman):
* `/are-insurance-adjusters-honest/` — ORIGINAL article, keep URL; date 2026-02-20, updated 2026-10-20.
* `/public-adjuster-pros-and-cons/`
* `/when-is-it-too-late-to-hire-a-public-adjuster/`
* `/twia-windstorm-claim-guide-port-arthur/`
* `/hurricane-damage-insurance-claim-port-arthur/`
* `/wind-vs-flood-damage-port-arthur-insurance/`
* `/hurricane-deductible-texas-explained/`
* `/port-arthur-hurricane-history-insurance-lessons/`
* `/how-to-document-storm-damage-port-arthur/`
* `/denied-insurance-claim-port-arthur/`

Post categories (use exactly): Hurricane Claims, TWIA & Windstorm, Flood & Water Claims, Roof Claims, Claim Process, Hiring a Public Adjuster, Weather Records, Building Codes, Commercial Claims, Fire Claims.

## Images

* Existing article `/are-insurance-adjusters-honest/`: `'image' => '/wp-content/uploads/2026/02/Are-Insurance-Adjusters-Honest.webp'`.
* `/public-adjuster-pros-and-cons/`: `'/wp-content/uploads/2026/02/Public-Adjuster-Pros-and-Cons.webp'`; `/when-is-it-too-late-to-hire-a-public-adjuster/`: `'/wp-content/uploads/2026/02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp'`.
* Other articles: `'image' => '/assets/img/featured/<slug>.webp'`.
* Service pages: `'/assets/img/featured/service-<slug>.webp'`.
* Pages: `'/assets/img/featured/page-<name>.webp'` (name = filename with `__` → `-`, e.g. `page-service-areas-beaumont.webp`). Generated separately; just use the path.

## Length targets

* Rewritten original article: **1,800–2,500 words** (keep topic and useful original points, improve accuracy, remove unsupported claims).
* New articles: **1,600–2,500 words**.
* Service pages: **900–1,400 words** body + 5–7 FAQs.
* Area pages: **700–1,100 words** of genuinely local content + 4–5 FAQs.
* Every article: 4–7 FAQs, at least one table, key-takeaways box, `[[cta]]` once mid-article, `sources` array with 2–5 authoritative links.
