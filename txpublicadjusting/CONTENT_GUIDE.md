# TX Public Adjusting rebuild: content guide

This is the brief for everyone who writes page content for the rebuilt
txpublicadjusting.com. Read all of it before writing.

## Why the site is being rebuilt

The old WordPress site was demoted sitewide by Google's spam systems on
2026-06-26 (impressions fell 85% overnight). The causes:

- **Scaled content / doorway pages:** 411 near-identical city pages, 45 templated
  commercial pages ("Texas Public Adjuster for Ski Lodge"), and roughly 30 hail posts
  published within two days, all saying the same things in slightly different words.
- **No visible expert behind the content:** posts were credited to "txpublicadjusting",
  the testimonials were anonymous, and there were no author credentials.
- **Filler:** generic weather paragraphs, invented "near La Plaza Mall" landmark
  name-dropping, and long intros that say nothing.

So every page we write has to be **useful, specific, and clearly different from every
other page**. If a paragraph could be pasted onto another page by swapping one word,
delete it.

## Business facts (use exactly these; never invent others)

- Brand: **TX Public Adjusting**
- Legal entity: **Rise Public Adjusting LLC**
- Licensed public adjuster: **Joseph Dittman**, Texas Public Adjuster License **#3356839**
  (licensed by the Texas Department of Insurance, TDI)
- Phone: **+1 (832) 503-5866** (call or text)
- Based in **Belton, Texas (Bell County)**; serves property owners **statewide**: every
  Texas county, residential and commercial.
- Tools used: **Xactimate** estimating software, **Matterport 3D** scans, drone or
  roof-level photo documentation, moisture meters for water losses.
- Fee: **contingency**, a percentage of the claim payment. **No upfront fee; free claim
  review.** Texas law caps public adjuster fees at **10%** of the settlement.

**Do NOT invent:** years in business, number of claims handled, dollar amounts
recovered, success rates, client names, testimonials, awards, office addresses in other
cities, staff names other than Joseph, or "local teams" in cities. Don't claim an office
in any city other than Belton.

**Allowed:** "we", "our firm", "Joseph", and statements about how we work (inspect,
document, write an Xactimate estimate, negotiate, attend re-inspections, invoke or
advise on appraisal, coordinate with contractors and mitigation companies, work with
attorneys when a claim needs one).

## Verified Texas law (cite these; don't add other legal claims)

| Topic | Rule | Source |
| --- | --- | --- |
| PA fee cap | A public adjuster's total commission may not exceed **10%** of the settlement. If the insurer pays (or commits in writing to pay) policy limits on a total fire loss within 72 hours of the claim being reported, a percentage fee isn't allowed (only reasonable time-based compensation). | Tex. Ins. Code §4102.104 |
| Contract | Must be on a TDI-approved form; must let the client **rescind within 72 hours** of signing; must say "WE REPRESENT THE INSURED ONLY." | §4102.103 |
| Checks | The insured must be a payee on every claim check, and a PA may never sign or endorse a check for the insured. | §4102.104(c),(e) |
| Conflicts | A PA may not take part in repairing or reconstructing property on a claim they adjust, or take money from repair or salvage firms on it. | §4102.158 |
| Contractors | A contractor may not act as a public adjuster, or advertise to adjust claims, for property they are or may be repairing, even with a license or power of attorney. | §4102.163 |
| Licensing | Anyone acting as a public adjuster in Texas must be licensed by TDI. | Ch. 4102 |
| Acknowledge claim | Insurer must acknowledge the claim, **begin its investigation, and request needed items within 15 days** of notice (surplus lines: 30 business days). | §542.055 |
| Accept or reject | Within **15 business days** after receiving all requested items (30 days if arson is suspected). If it needs more time it must say why, then decide within **45 days** of that notice. | §542.056 |
| Payment | Within **5 business days** after notifying acceptance (surplus lines: 20 business days). | §542.057 |
| Catastrophes | After a weather-related catastrophe or major natural disaster declared by the commissioner, these deadlines are **extended by 15 days**. | §542.059 |
| Late payment | Penalty interest (18%/yr, or judgment rate plus 5% for weather claims under Ch. 542A) plus attorney's fees. | §542.060 |
| Pre-suit notice | For weather-related property claims, the policyholder must give written notice **at least 61 days before filing suit**, stating the amount owed. | §542A.003 |
| TWIA | Texas Windstorm Insurance Association claims must be filed **within one year** of the date of damage (the commissioner may extend this up to 180 days for good cause). TWIA generally has **60 days** to accept or deny after receiving the claim and requested information. | §2210.205, §2210.573 |

Statements you may make without a citation, but phrase carefully:

- Many private Texas homeowners policies **also** set a one-year (or similar) deadline
  to report wind and hail damage. Always tell readers to check their own policy's
  "Duties after loss" and "Suit against us" conditions. **Never state a single universal
  private-policy deadline.**
- Texas has **no statute** that forces insurers to replace matching materials. Matching
  depends on the policy's wording ("like kind and quality", "reasonable uniform
  appearance") and the facts. Don't claim Texas has a matching law.
- Many Texas policies carry **cosmetic damage exclusions** (common on metal roofs) and
  **ACV (actual cash value) roof schedules or endorsements**. Coverage depends on the
  endorsements.
- **Appraisal** settles disputes over the *amount* of loss, not coverage. Each side
  picks an appraiser, and the two appraisers pick an umpire.
- Wind and hail deductibles in Texas are often a **percentage of dwelling coverage**
  (1–2%), especially in coastal counties and hail-prone areas.
- Named storms you may mention: Hurricane Ike (2008, Galveston and Houston),
  Hurricane Harvey (Aug 2017, Houston and Coastal Bend flooding, Rockport landfall),
  Winter Storm Uri (Feb 2021, statewide freeze and burst pipes), Hurricane Beryl
  (July 2024, Houston wind damage and outages), Hurricane Hanna (July 2020, Rio Grande
  Valley). Don't quote damage dollar figures.
- Flood: standard homeowners policies exclude flood; that needs an NFIP or private flood
  policy. Wind-driven rain and storm-created openings are a different coverage question.

## Voice and style

- Write for a stressed property owner with a damaged roof or a flooded kitchen. Plain
  English and short paragraphs. Use second person ("you") for the reader and "we" for
  the firm.
- **Answer the main question in the first two or three sentences.** No throat-clearing
  ("When disaster strikes…", "Navigating the complex world of…", "In today's…").
- Be concrete: name the document, the form, the deadline, the roof component, the line
  item on the estimate.
- Banned words and phrases: "navigate/navigating", "landscape", "delve", "in today's",
  "it's important to note", "peace of mind", "game-changer", "unlock", "empower",
  "seamless", "rest assured", "look no further", "battlefield", "journey", "maze".
  No emoji. No exclamation marks.
- US spelling. Sentence-case headings. Don't keyword-stuff city names: a city name
  appears where it's natural, not in every paragraph.
- No fake urgency, and no promises of results ("we guarantee", "maximize your
  settlement every time").

## Page file format

Each page is a PHP file that **returns an array**. Put body HTML in a **nowdoc**
(`<<<'HTML'`) so nothing inside is interpreted by PHP. The closing `HTML;` must be on
its own line. Run `php -l yourfile.php` after writing; it must print "No syntax errors".

```php
<?php
return [
    'title'       => 'Hail Damage Insurance Claim in Texas: A Step-by-Step Guide', // <title>, 45–62 chars, no phone numbers, no "|" brand suffix (added automatically)
    'description' => 'What to do in the first 72 hours after hail, how Texas insurers evaluate roofs, and when to push back on a low estimate.', // 120–158 chars
    'h1'          => 'Hail damage insurance claims in Texas',
    'eyebrow'     => 'Hail & roof claims',        // short label shown above the H1
    'lead'        => 'One or two plain sentences summarizing what the reader gets.',
    'updated'     => '2026-10-13',
    'body'        => <<<'HTML'
<p>…</p>
<h2>…</h2>
…
HTML,
    'faqs' => [
        ['q' => 'Question?', 'a' => 'Answer in 1–3 sentences. May contain <a href="/…/">links</a>.'],
    ],
    'related' => ['/post/denied-hail-damage-insurance-claim/', '/tools/claim-settlement-calculator/'],
];
```

Extra keys by page type:

- **Posts** (`content/posts/{slug}.php`): `'published' => 'YYYY-MM-DD'` (use the
  original publish date given in your assignment), `'category' => 'Hail & Roof' |
  'Public Adjusters 101' | 'Fire, Water & Storm' | 'Claim Process'`.
- **Areas** (`content/areas/{slug}.php`): `'city'`, `'region'` (e.g. "Upper Gulf
  Coast"), `'counties' => [...]` (county names you're sure of), `'nearby' => [...]`
  (6–15 towns and suburbs covered by this page; real places only), `'risks' =>
  [['title'=>'…','text'=>'…'], …]` (3–4 regional claim patterns), `'case_notes' => []`
  (leave empty; the firm fills these in later with real claims).
- **Commercial** (`content/commercial/{slug}.php`): `'property' => 'Office buildings'`.
- **Services** (`content/services/{slug}.php`): `'icon' => 'roof'|'water'|'fire'|'wind'|'shield'`.

### HTML you can use in `body`

Only use these elements and classes. The design system styles them; anything else
renders unstyled.

- `<h2>` (main sections; these make the table of contents) and `<h3>`. Never `<h1>`.
- `<p>`, `<ul>`, `<ol>`, `<strong>`, `<em>`, `<a href="/path/">` (root-relative internal
  links; external links only to `.gov` or statute sources, with `rel="noopener"
  target="_blank"`).
- `<div class="callout callout--tip"><p><strong>Tip:</strong> …</p></div>`, with
  variants `callout--tip`, `callout--warn`, `callout--law` (for a statute: start with
  `<strong>Texas law:</strong>`).
- `<ul class="checklist"><li>…</li></ul>`: a checklist with check icons.
- `<ol class="steps"><li><strong>Step title.</strong> Explanation.</li></ol>`: numbered
  step cards.
- `<div class="table-wrap"><table><thead>…</thead><tbody>…</tbody></table></div>`
- `<div class="compare"><div><h3>Left title</h3><ul>…</ul></div><div><h3>Right title</h3><ul>…</ul></div></div>`:
  side-by-side comparison.
- `<div class="keyfacts"><div><span>15 days</span><p>to acknowledge your claim</p></div>…</div>`:
  2–4 big-number facts. Only verified numbers from the law table.
- Shortcodes on their own line: `[[cta]]` (call-to-action box; use once, mid-page) and
  `[[tool:claim-settlement-calculator]]` (a teaser card for a tool; slugs are listed
  below).

Target lengths: posts 1,200–2,000 words, service pages 1,000–1,400, area pages
800–1,200, commercial pages 700–1,000, hubs 400–700. Use 3–6 FAQs per page, and make
them questions people actually type.

## Final URL inventory (link only to these)

Core: `/`, `/about-us/`, `/contact-us/`, `/services/`, `/commercial-claims/`, `/areas/`,
`/blog/`, `/tools/`

Services:
`/services/roof-hail-damage-claims/`, `/services/water-damage-claims/`,
`/services/fire-smoke-damage-claims/`, `/services/hurricane-windstorm-claims/`,
`/services/denied-underpaid-claims/`

Commercial (`/commercial-claims/texas-public-adjuster-for-{slug}/`): `office`,
`warehouse`, `apartment-complex`, `church`, `hotels`, `retail-store`, `restaurant`,
`self-storage-facility`, `car-dealership`, `school`

Areas (`/areas/public-insurance-adjuster-{slug}/`): `houston`, `beaumont`,
`corpus-christi`, `mcallen`, `san-antonio`, `austin`, `college-station`, `killeen`,
`dallas`, `fort-worth`, `waco`, `tyler`, `el-paso`, `midland`, `lubbock`, `amarillo`

Tools (`/tools/{slug}/`):
- `claim-settlement-calculator`: RCV, depreciation, deductible, ACV vs. RCV payout,
  and the effect of a public adjuster fee
- `texas-claim-deadline-calculator`: Chapter 542 prompt-payment dates from your claim dates
- `claim-documentation-checklist`: interactive and printable, by loss type
- `contents-inventory-builder`: room-by-room personal property list with CSV export
- `storm-report-lookup`: finds NOAA storm reports for a date and place
- `do-i-need-a-public-adjuster`: a short self-assessment quiz

Blog posts (`/post/{slug}/`):
`what-is-a-public-adjuster-a-complete-guide-for-property-owners`,
`public-adjuster-vs-independent-adjuster`, `should-i-use-a-public-adjuster`,
`when-is-it-too-late-to-hire-a-public-adjuster`,
`smart-property-owners-guide-to-choosing-the-right-public-adjuster`,
`the-truth-about-public-adjuster-fees`, `can-a-public-adjuster-work-for-a-contractor`,
`who-regulates-public-adjusters-and-why-it-matters-to-homeowners`,
`how-long-does-an-insurance-adjuster-have-to-contact-you`,
`common-property-insurance-claims-mistakes`, `hail-damage-insurance-claim`,
`how-long-do-you-have-to-file-a-hail-claim-in-texas`,
`how-to-identify-hail-damage-by-roof-type`, `cosmetic-vs-functional-hail-damage`,
`how-insurance-companies-evaluate-hail-damage`, `denied-hail-damage-insurance-claim`,
`underpaid-hail-damage-insurance-claim`, `hail-damage-supplement-claim`,
`matching-laws-for-roof-replacement-in-texas`, `appraisal-for-hail-damage-claim`,
`how-to-document-damage-for-your-claim`, `house-fire-debris-removal-cost`,
`fire-damage-insurance`, `dealing-with-insurance-adjuster-after-water-damage`,
`property-damage-after-a-hurricane`

Link generously but naturally: 3–8 internal links per page, using descriptive anchor
text (never "click here"). Each page should link to at least one service page or tool.

## Before you finish a file

1. `php -l` passes.
2. Nothing on the page is an invented fact (see the "Do NOT invent" list).
3. No banned phrases.
4. Every link points to a URL in the inventory above.
5. The page reads as clearly different from its siblings. Compare it with them.
