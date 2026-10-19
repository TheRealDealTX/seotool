# Blog post file format

One file per post: `content/posts/<slug>.php`. It must be valid PHP that only returns an array:

```php
<?php
return [
    'slug'        => 'claims-adjuster-salary',          // = filename, = URL /insurance-adjuster-advice/<slug>/
    'title'       => 'Claims Adjuster Salary in 2026: What Staff, Field & Desk Adjusters Earn', // H1 + <title>, <= 65 chars ideally
    'meta_title'  => 'Claims Adjuster Salary (2026): Pay by Role & Experience', // <= 60 chars, keyword first
    'description' => '...',                               // meta description 140-158 chars, contains keyword
    'keyword'     => 'claims adjuster salary',
    'date'        => '2026-09-30',                        // published
    'updated'     => '2026-09-30',
    'author'      => 'Insurance Adjuster Salary Editorial Team',
    'category'    => 'Salary Guides',                     // one of: Salary Guides, Pay & Compensation, Career Advice, State Guides
    'image'       => 'office.webp',                       // given to you, lives in /assets/img/
    'image_alt'   => '...',                               // descriptive alt containing keyword naturally
    'excerpt'     => '...',                               // 1-2 sentences for cards
    'read_time'   => 8,                                   // minutes
    'faqs'        => [                                    // 4-5 Q&As, rendered as accordion + FAQPage schema
        ['q' => '...?', 'a' => 'Plain text answer, 1-3 sentences.'],
    ],
    'body'        => <<<'HTML'
<p class="lead">...</p>
...
HTML,
];
```

Body HTML rules (the template already renders H1, hero image, date, author, table of contents, FAQs and a CTA — do NOT repeat those):
- Start with `<p class="lead">` intro paragraph that contains the exact keyword in the first sentence.
- Use `<h2 id="kebab-id">` for sections (the TOC is built from h2 ids, so every h2 needs a unique id), `<h3>` for sub-sections. 6-9 h2 sections. Exact keyword in at least two h2s.
- 1,100-1,500 words of body. US English. Confident, practical, specific, written for someone considering or working in adjusting. No fluff, no "In today's world", no "In conclusion". Short paragraphs.
- Include at least one data table: `<div class="table-wrap"><table class="data-table"><thead>...</thead><tbody>...</tbody></table></div>`.
- Include one or two callouts: `<div class="callout"><strong>Quick answer:</strong> ...</div>` (first one near top answering the search query directly in 40-60 words - featured-snippet bait) and optionally `<div class="callout callout-tip"><strong>Pro tip:</strong> ...</div>`.
- Include bulleted or numbered lists where useful.
- Internal links (root-relative, use 3-6 per post, natural anchors):
  - `/` (anchor like "insurance adjuster salary" guide)
  - `/salary-calculator/` (Adjuster Salary Calculator)
  - `/cat-deployment-calculator/` (CAT Deployment Earnings Calculator)
  - `/public-adjuster-fee-calculator/` (Public Adjuster Fee Calculator)
  - `/salary-by-state/` (Insurance adjuster salary by state)
  - `/insurance-adjuster-advice/<other-slug>/` for sibling posts (list below)
- Optional one outbound link to the BLS Occupational Outlook Handbook page: https://www.bls.gov/ooh/business-and-financial/claims-adjusters-appraisers-examiners-and-investigators.htm (rel="noopener" target="_blank").
- No inline styles, no scripts, no images in body, no emoji. Escape `&` as `&amp;` in HTML text. Never use a raw `<<<` or the string `HTML,` at line start inside the body.
- Do not invent precise statistics attributed to named sources beyond the FACTS below. Ranges for specialties are fine if phrased as typical ranges / industry estimates ("commonly", "typically", "most job postings we track fall between").

FACTS (use consistently; these are the only hard numbers to cite as BLS):
- BLS OOH, May 2024: claims adjusters, appraisers, examiners & investigators median pay $76,790/yr ($36.92/hr). 365,300 jobs in 2024. Employment projected to decline 5% 2024-34 (automation of simple claims), but ~20,000+ openings a year from retirements/turnover (say "thousands of openings each year").
- Typical staff/company adjuster ranges (industry estimates): trainee/entry-level $45k-$60k; auto/material damage $50k-$72k; desk property $55k-$75k; field property $62k-$90k; workers comp $55k-$82k; bodily injury/casualty $60k-$88k; senior/complex/large loss $85k-$120k+. Company car, gas card, laptop, phone and benefits often add $8k-$15k of value for field staff roles.
- Independent adjusters (1099): paid per claim on a fee schedule tied to gross loss (e.g. ~$350-$600 for small claims under $5k, ~$1,000-$2,000 at $25k-$50k, $3,000+ for large losses), or a daily rate ($400-$700/day typical for desk/daily CAT, $500-$800+ for experienced field/commercial). IA firms usually split fees with the adjuster, commonly 65/35 to 75/25 in the adjuster's favor. No benefits, pay own expenses (travel, lodging, ladder, tools, software like Xactimate ~$300+/mo... phrase "Xactimate subscription"), self-employment tax. Annual income swings: slow years $30k-$60k, average active years $70k-$120k, big storm years $150k-$250k+ for experienced CAT adjusters (rare, not typical).
- CAT adjusters: deploy 2 weeks to several months after hurricanes, hail, wildfire, tornado; 7-day workweeks, 12-hour days common; can close 2-5 claims/day on simple hail claims; earnings per deployment commonly $15k-$60k+.
- Public adjusters represent policyholders, paid a contingency fee, typically 10%-20% of the claim settlement (some charge 5%-15%); many states cap fees. Texas caps public adjuster fees at 10% of the settlement. Florida caps at 20% generally and 10% for claims tied to a declared state of emergency during the year after it is declared. Public adjuster annual income: commonly $50k-$100k; established PAs with steady commercial/large loss flow can earn $150k+.
- Licensing: most states require a license. Texas all-lines adjuster license is widely used as a "designated home state" (DHS) license by non-residents because Texas has broad reciprocity; pre-licensing course + exam, fingerprints. Florida 6-20 (all lines) license; Florida also issues emergency licenses after declared disasters. Continuing education required to renew.
- Adjusters are not paid bonuses for denying claims at reputable carriers; unfair claim settlement practices laws in every state prohibit misrepresenting coverage or failing to pay valid claims; performance metrics usually focus on cycle time, file quality, customer satisfaction and accuracy ("leakage") - be balanced: acknowledge metrics/incentives exist at some carriers, and that policyholders who suspect bad faith can contact their state insurance department.
- Texas: one of the largest adjuster markets (hail, hurricanes on the Gulf Coast, tornadoes); Texas staff adjuster pay roughly in line with national median, Houston/Dallas-Fort Worth slightly higher; frame state numbers as estimates.
- Florida: hurricane-heavy market, huge demand for property & CAT adjusters; staff pay roughly near national median; IAs can earn far more in active hurricane seasons.

Course CTA (the template adds it; you may mention once naturally in text): an online adjuster pre-licensing course at AdjustingOnline, promo code "joe20" for 20% off. Link https://www.adjustingonline.com/courses/ with rel="sponsored noopener" target="_blank".

ALL POSTS (slug - keyword):
- how-much-do-insurance-adjusters-make - how much do insurance adjusters make
- claims-adjuster-salary - claims adjuster salary
- insurance-adjuster-pay-rate - insurance adjuster pay rate
- how-do-insurance-adjusters-get-paid - how do insurance adjusters get paid
- public-adjuster-salary - public adjuster salary
- property-adjuster-salary - property adjuster salary
- independent-adjuster-salary - independent adjuster salary
- cat-adjuster-salary - cat adjuster salary
- workers-comp-adjuster-salary - workers comp adjuster salary
- auto-adjuster-salary - auto adjuster salary
- insurance-adjuster-salary-texas - insurance adjuster salary texas
- insurance-adjuster-salary-florida - insurance adjuster salary florida
- entry-level-claims-adjuster-salary - entry level claims adjuster salary
- do-insurance-adjusters-make-good-money - do insurance adjusters make good money

After writing each file, run `php -l <file>` and `php -r 'var_dump(count((require "<file>")));'` to confirm it parses and returns an array (if php isn't installed, check carefully by eye). Word count check: `php -r '$p=require "<file>"; echo str_word_count(strip_tags($p["body"]));'`.
