# Blog post file spec (westcarrolltonapartments.com)

Each post is ONE file: `content/posts/<slug>.php` that returns a PHP array:

```php
<?php return [
  'slug'        => 'apartment-budget-guide',            // must equal filename
  'title'       => 'H1 title (natural, keyword-led)',
  'meta_title'  => '<= 60 chars, include primary keyword',
  'description' => '<= 155 chars meta description',
  'date'        => '2026-11-20',                         // publish date
  'category'    => 'Renter Tips',  // one of: Renter Tips | Budgeting | Moving | Home & Decor | Local Guide
  'image'       => 'liv-3',        // one photo key (see list below)
  'excerpt'     => '1-2 sentence teaser',
  'old_urls'    => ['/old-wordpress-slug/'],            // given to you; copy exactly
  'faq'         => [ ['q'=>'...','a'=>'...'], ... ],    // 3-4 FAQs (rendered + FAQPage schema)
  'products'    => [                                     // 4-6 Amazon products relevant to the post
     ['name'=>'Command Picture Hanging Strips','query'=>'command picture hanging strips','why'=>'One line on why it helps','icon'=>'🖼️'],
  ],
  'body'        => <<<'HTML'
<p>Intro...</p>
<h2>...</h2>
...
<!--products-->
...
HTML
];
```

Rules
- 900-1300 words of original body copy, written fresh (do not copy from anywhere). Plain, helpful, specific; US spelling.
- Localize to West Carrollton, Ohio (Montgomery County, south of Dayton, along the Great Miami River, I-75 / SR-725 corridor) where it fits naturally; don't force it. NEVER mention Texas/Houston.
- Only state facts you are confident are true. For Ohio law cite Ohio Revised Code chapter 5321 sections only where you are sure (e.g. 5321.16 security deposit itemization within 30 days; 5321.04(A)(8) 24-hour notice before entry; 5321.07 rent escrow). Add "this is not legal advice" where law is discussed. Don't invent local business names, prices or statistics.
- Body HTML: only <p>, <h2>, <h3>, <ul>, <ol>, <li>, <strong>, <em>, <a>, <blockquote>, <table>/<thead>/<tbody>/<tr>/<th>/<td>. No <h1>, no inline styles, no scripts.
- Put the marker `<!--products-->` exactly once, at a natural midpoint or near the end.
- Internal links (use these exact paths where relevant, 2-4 per post): /apartments/ , /apartments/pet-friendly/ , /apartments/under-1000/ , /apartments/1-bedroom/ , /apartments/2-bedroom/ , /apartments/townhomes/ , /tools/rent-affordability-calculator/ , /tools/roommate-rent-splitter/ , /tools/moving-cost-estimator/ , /tools/moving-checklist/ , /tools/apartment-match-quiz/ , /tools/room-planner/ , /west-carrollton-living-guide/ , and other posts as /blog/<slug>/ (slugs listed below).
- Products: generic, widely-available item types or well-known brands (search query based, no ASINs, no prices).
- Photo keys available: ext-1..ext-8 (building exteriors), liv-1..liv-16 (living rooms), kit-1..kit-4 (kitchens), bed-1..bed-7 (bedrooms), bath-1..bath-3, gym-1..gym-2, pool-1, lounge-1.
- Use PHP nowdoc (<<<'HTML') exactly as shown so no escaping is needed. File must pass `php -l`.

All post slugs on the site (for cross-linking):
renting-an-apartment-checklist, living-near-work-dayton-commute, can-you-renovate-a-rental-apartment-ohio,
living-with-roommates-pros-cons, best-floor-to-live-on-apartment, hidden-costs-of-renting-an-apartment,
apartment-budget-guide, ohio-tenant-rights-guide, lower-utility-bills-apartment-ohio, apartment-vs-house-west-carrollton,
cozy-apartment-self-care-ideas, small-apartment-storage-ideas, seasonal-apartment-cleaning-ohio,
apartment-amenities-worth-paying-for, pet-friendly-apartment-setup, furnish-apartment-on-a-budget,
getting-to-know-your-neighbors, new-vs-older-apartments, moving-to-west-carrollton-checklist,
when-to-upsize-your-apartment, hang-art-in-a-rental-without-damage, work-from-home-apartment-setup,
renter-maintenance-checklist, renters-insurance-claims-guide
