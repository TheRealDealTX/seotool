# Blog post format

One file per post: `content/posts/<slug>.php`. The slug is the URL: `/blog/<slug>/`.
The file returns a PHP array. Use a nowdoc (`<<<'HTML'`) for the body so `$` and quotes need no escaping.

```php
<?php defined('ERE') or exit;
return [
    'title'       => 'What to Do After a House Fire: A Step-by-Step Recovery Checklist',  // H1, natural, contains keyword
    'seo_title'   => 'What to Do After a House Fire: Checklist',                         // <title>: 40-51 chars (hard max 51 so the ' | ERE540' brand fits in Google's ~580px), keyword at the front
    'description' => '...',            // meta description: 120-145 chars (hard max 145), includes the keyword, ends with a reason to click
    'keyword'     => 'what to do after a house fire',
    'category'    => 'insurance-claims', // one of: buying, selling, investing, homeownership, insurance-claims, houston
    'date'        => '2026-11-12',       // publish date, YYYY-MM-DD (use the date given in your brief)
    'excerpt'     => '...',              // 1-2 sentences for cards, max 200 chars
    'faq'         => [                   // 4-6 real questions people search; answers 40-90 words, plain text
        ['Question?', 'Answer.'],
    ],
    'products'    => ['first-alert-smoke-co', 'sentrysafe-fireproof'], // 2-4 keys from content/products.php shown in a "Recommended gear" box at the end; [] if none fit
    'tools'       => ['insurance-claim-depreciation-calculator'],      // 1-2 tool slugs shown as a callout (list below)
    'related'     => ['public-adjuster-vs-insurance-adjuster'],        // 2-3 slugs of other posts (list below)
    'body'        => <<<'HTML'
<p>Intro paragraph ...</p>
<h2>...</h2>
...
HTML,
];
```

## Body rules

- Plain semantic HTML only: `<p> <h2> <h3> <ul> <ol> <li> <strong> <em> <a> <table> <thead> <tbody> <tr> <th> <td> <blockquote>`. No `<h1>` (the template prints it), no inline styles, no classes, no images, no scripts.
- 1,400-2,000 words. Keyword in the first 100 words and in at least one `<h2>`. Use related variations naturally - never stuff.
- Open with a 2-3 sentence intro that answers the search intent directly. Then 5-9 `<h2>` sections, `<h3>` where useful. At least one list and, where it fits, one comparison `<table>`.
- Write for Houston / Texas homeowners, buyers, sellers and investors. Specific, practical, honest. Active voice, short paragraphs (2-4 sentences). No fluff, no "In today's fast-paced world", no "In conclusion". End with a short "Bottom line" `<h2>`.
- Facts must be accurate as of late 2026. Verify every Texas-specific number, law, deadline or program with a web search before using it, and prefer stating ranges or "as of 2026" over false precision. Do not invent statistics, studies, quotes or named experts. If you are not sure of a figure, leave it out.
- Not legal, tax or financial advice: where relevant, say to confirm with a licensed professional (attorney, CPA, lender, licensed public adjuster), in one sentence, not repeated.
- Internal links (2-5 per post, natural anchor text, root-relative):
  - other posts: `/blog/<slug>/`
  - tools: `/tools/<tool-slug>/`
  - category pages: `/category/<category>/`
- Inline product mentions (optional, max 2 per post): write a placeholder on its own line, `[[product:key]]`, where a product genuinely helps the reader. It renders as a product card with an Amazon link. Do not write Amazon URLs yourself.
- Inline tool callout (optional, max 1): `[[tool:tool-slug]]` on its own line.
- No external links except authoritative sources (.gov, TDI, HCAD, FEMA, NFIP, IRS, Texas Comptroller, Texas Real Estate Commission) - max 3, and only to URLs you have confirmed exist.

## Tool slugs
mortgage-calculator, home-affordability-calculator, rent-vs-buy-calculator, closing-cost-calculator, seller-net-proceeds-calculator, rental-property-calculator, refinance-calculator, extra-payment-calculator, dti-calculator, texas-property-tax-calculator, insurance-claim-depreciation-calculator, hurricane-prep-checklist

## All post slugs (for related / internal links)
buying: first-time-home-buyer-texas, closing-costs-in-texas, buying-a-house-in-a-flood-zone-houston, home-inspection-checklist, down-payment-assistance-texas, fha-loan-requirements-texas
selling: sell-fire-damaged-house-texas, texas-seller-disclosure-notice, selling-a-house-as-is-texas, capital-gains-tax-on-home-sale, selling-a-house-with-foundation-problems, sell-house-by-owner-texas
investing: how-to-analyze-a-rental-property, house-hacking-texas, brrrr-method-explained, texas-eviction-process, 1031-exchange-texas, short-term-rental-houston
homeownership: texas-homestead-exemption, houston-home-maintenance-checklist, protest-property-taxes-harris-county, homeowners-insurance-texas, mud-tax-texas, texas-hoa-laws
insurance-claims: what-to-do-after-a-house-fire, hurricane-damage-insurance-claim-texas, public-adjuster-vs-insurance-adjuster, water-damage-claim-denied, loss-of-use-coverage, how-to-file-a-home-insurance-claim, hail-damage-roof-insurance-claim, appraisal-clause-insurance
houston: best-houston-suburbs-for-families, moving-to-houston, cost-of-living-in-houston, best-neighborhoods-in-houston, houston-property-tax-rate

## Product keys
See `content/products.php` (keys are the array keys).
