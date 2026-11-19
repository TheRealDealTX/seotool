# Content spec — newhomestudent2019.com rebuild

Site: **New Home Investing Knowledge** (newhomestudent2019.com) — an online platform that
gives people building a new home (owner-builders, people hiring a general contractor,
future home-building pros) training, resources and guidance. We do NOT sell our own
products: we recommend other people's resources (books, tools, smart-home gear,
apartment/moving gear) through **Amazon affiliate links**, and we publish practical tips.
Author / founder: **Jonathon**. Base: Texas (Houston/Austin readers are common).
Phone (832) 720-7978. Email info@newhomestudent2019.com.

Audience framing for off-topic legacy posts (apartments, students, renting): many readers
rent while they save for, plan, or wait on a home build. Tie those posts back to that
journey (one natural paragraph + a link to a building/buying post), but keep the post
genuinely useful for the search intent its URL targets.

## File format — one PHP file per post

Path: `content/posts/<slug>.php` (slug = exact URL slug, no slashes). The file must be
valid PHP and look exactly like this:

```php
<?php defined('NHS') || exit;
return [
  'title'       => 'H1 shown on the page (natural, keyword-led, may differ from seo_title)',
  'seo_title'   => 'Title tag, 50-60 chars, primary keyword near the front',
  'description' => 'Meta description, 120-145 chars (hard max 145), includes the keyword, ends with a reason to click.',
  'keyword'     => 'primary keyword phrase',
  'category'    => 'building-tips',   // one of: building-tips | tips | real-estate-investing | apartment-living
  'date'        => '2023-09-06',      // ORIGINAL publish date for legacy posts (given to you); new posts: 2026-11-19
  'updated'     => '2026-11-19',
  'excerpt'     => 'One or two sentence summary for blog cards (max ~200 chars).',
  'image_alt'   => 'Descriptive alt text for the featured image',
  'faq'         => [
    ['Question?', 'Answer in 1-3 plain sentences (no HTML).'],
    // 3-5 FAQs
  ],
  'body'        => <<<'HTML'
<p>Intro...</p>
<h2>...</h2>
...
HTML,
];
```

Use a **nowdoc** (`<<<'HTML'`) for the body so `$` and quotes need no escaping. The closing
`HTML,` must be on its own line. Single-quoted PHP strings elsewhere: escape `'` as `\'`.
Run `php -l content/posts/<slug>.php` on every file you write (php is installed) and fix
any syntax error.

## Body rules

- Do not repeat the H1 in the body. Start with a 2-3 sentence intro that answers the
  search intent straight away and uses the primary keyword once.
- 900-1,400 words. Use `<h2>` sections (4-7) and `<h3>` where useful; short paragraphs,
  `<ul>/<ol>` lists, and at most one `<table>` where a comparison genuinely helps.
- Allowed HTML: p, h2, h3, ul, ol, li, strong, em, a, table, thead, tbody, tr, th, td,
  blockquote. No inline styles, no classes, no images, no h1, no scripts.
- Include a `<div class="callout"><p><strong>Pro tip:</strong> ...</p></div>` once where it fits.
- Do NOT include the FAQ in the body (it is rendered from the `faq` array automatically).
- Accuracy: no invented statistics, studies, prices-as-fact, or quotes. Use ranges and
  hedged language ("often", "typically"), and tell readers to confirm code versions, fees
  and rules with the local permitting office / official source. Do not state specific
  code-edition adoption years unless you are confident; prefer "the city adopts the
  International Residential Code (IRC) with local amendments — check the current edition".
  Dates: it is November 2026; don't call 2023/2024 "this year". If the URL slug contains a
  year, keep the content evergreen and frame it as "updated" guidance (e.g. title
  "Is Building a Tiny Home in Texas Worth It? (Updated Guide)").
- Voice: experienced, plain-spoken, practical Texas home-building mentor. Second person.
  No fluff openers ("In today's fast-paced world"), no "In conclusion".
- End with a short "Next steps" section that points to one or two internal links and,
  where it fits, the free training at `/free-training/`.

## Internal links

Link 3-5 related posts with root-relative URLs, e.g. `<a href="/budgeting-for-your-texas-home-build-tips-for-staying-on-track/">budgeting guide</a>`.
Only link to slugs in the master list below or these pages:
`/free-training/`, `/build-a-home-yourself/`, `/our-products/` (recommended resources hub),
`/resources/`, `/blog/`, `/about-us/`, `/contact/`.

## Existing outbound links — KEEP THEM

For legacy posts you'll be given the outbound links the old post had. Keep every
non-junk one (same URL, natural anchor text, once or twice — no need to repeat 4x).
These are partner/network sites (e.g. txpublicadjusting.com, txinsuranceappraiser.com,
riseapartments.com, houstonapartments.com, txrealbuyer.com, txhighrisers.com) and
official sources. Strip any `?utm_source=...`/`gclid` tracking parameters. Drop links
whose anchor text was garbage (e.g. "San Mateo County+10Graystone...") unless the URL is an
authoritative source, in which case relink with clean anchor text. Write external links
as plain `<a href="https://...">text</a>` — the renderer adds rel/target attributes.
For apartment-listing posts, keep the listed communities and their links, but rewrite the
descriptions in your own words and avoid claims you can't know (exact rents, amenities
that may have changed) — say "check current pricing and availability".

## Amazon affiliate products

Insert products with these markers (they are rendered into product cards / links with
the affiliate tag automatically — never write Amazon URLs yourself):

- Product grid (2-4 items, put it right after the paragraph that motivates it):
  `<!--products:key1,key2,key3|Short heading, e.g. Tools we recommend for your site walk-->`
- Inline text link inside a sentence: `[[amz:key|anchor text]]`

Use 1-2 grids and 1-4 inline links per post, only where a product genuinely helps the
reader do the thing the paragraph describes. Never claim you personally tested a product;
say "popular", "well-reviewed", "a solid pick for…". Don't mention prices.

Available product keys:

books_heldmann (Be Your Own House Contractor), books_contracting_guide (Complete Guide to
Contracting Your Home), books_dummies (Building Your Custom Home For Dummies),
books_code_check (Code Check: illustrated building code guide), books_code_check_electrical,
books_not_so_big (The Not So Big House), books_pattern_language (A Pattern Language),
books_get_house_right (Get Your House Right), books_rental_property (The Book on Rental
Property Investing), books_house_hacking (The House Hacking Strategy), books_set_for_life,
books_millionaire_re (The Millionaire Real Estate Investor), books_estimating (estimating
residential building costs), books_tiny_house, books_first_time_buyer, books_home_maintenance,
home_planner (house-building planner journal), graph_paper_notebook,
laser_measure, tape_measure, moisture_meter, stud_finder, outlet_tester, ir_thermometer,
thermal_camera, drill_combo, level, headlamp, hard_hat, safety_glasses, tool_bag, tool_set,
first_aid, site_camera, smart_thermostat, nest_thermostat, smart_lock, video_doorbell,
water_leak, radon_detector, smoke_co, fire_extinguisher, kill_a_watt, smart_plug,
led_bulbs, weatherstrip, caulk_gun, dehumidifier, air_purifier, water_filter,
surge_protector, blackout_curtains, white_noise, acoustic_panels, door_sweep, area_rug,
command_strips, under_bed_storage, folding_desk, futon, storage_ottoman, shower_curtain,
furniture_sliders, balcony_planter, grow_light, string_lights, outdoor_rug, pool_bag,
pet_gate, pet_carrier, moving_boxes, moving_blankets, label_maker, fireproof_safe,
document_organizer, ev_charger, portable_ev_charger

## Master list of post slugs (for internal linking)

Building (category building-tips):
building-a-new-home-why-its-a-decision-worth-considering ·
build-a-home-or-buy-an-already-built-one-weighing-the-pros-and-cons ·
budgeting-for-your-texas-home-build-tips-for-staying-on-track ·
choosing-the-right-location-for-your-texas-dream-home ·
the-pros-and-cons-of-building-in-urban-vs-rural-texas ·
energy-efficient-home-building-in-the-texas-heat ·
crafting-comfort-and-joy-the-6-keys-to-a-great-home ·
building-your-texan-haven-choosing-the-ideal-home-for-a-family-of-four ·
is-it-worth-building-tiny-homes-in-texas-in-2023-exploring-the-trend-and-practicality ·
the-art-of-home-design-where-passion-meets-comfort ·
navigating-texas-building-codes-what-you-need-to-know ·
requirements-when-building-a-new-house-in-austin-texas ·
understanding-building-codes-in-austin-tx-what-you-need-to-know ·
understanding-building-codes-in-dallas-tx-what-you-need-to-know ·
understanding-building-codes-in-houston-tx-what-you-need-to-know ·
understanding-building-codes-in-san-antonio-tx-what-you-need-to-know ·
how-to-be-your-own-general-contractor (new) ·
new-home-construction-timeline (new) ·
how-to-hire-and-manage-subcontractors (new) ·
essential-tools-for-owner-builders (new) ·
new-construction-inspection-checklist (new) ·
best-books-on-building-your-own-home (new) ·
how-much-does-it-cost-to-build-a-house-in-texas (new) ·
smart-home-features-to-add-during-new-construction (new) ·
how-to-finance-building-a-house (new) ·
how-to-choose-a-floor-plan-for-your-new-home (new)

Buying, moving & homeowner tips (category tips):
recognizing-the-signs-is-it-time-for-a-full-house-renovation ·
what-beginners-should-look-for-when-buying-a-house ·
how-to-find-the-best-deal-on-a-home-in-texas-as-a-christian-buyer ·
should-i-buy-a-home-or-rent-an-apartment-in-austin ·
relocating-to-austin-texas-in-2023-is-it-worth-it ·
the-booming-real-estate-market-in-austin-a-2023-overview ·
moving-in-texas-with-a-pet-in-2023-a-comprehensive-guide ·
can-you-get-monetized-even-if-youre-still-a-starting-influencer ·
first-things-to-buy-for-a-new-home (new) ·
new-construction-walkthrough-punch-list (new)

Real-estate investing (category real-estate-investing):
house-hacking-how-to-live-for-free-while-investing ·
how-to-find-off-market-new-home-investment-opportunities ·
the-smart-renters-guide-to-building-wealth-through-home-investing-knowledge ·
how-to-turn-your-first-apartment-into-a-stepping-stone-for-home-investments ·
why-new-homes-are-a-great-starting-point-for-real-estate-investors ·
public-adjusters-and-investment-planning-an-unexpected-connection ·
how-property-condition-reports-impact-investment-value ·
rebuilding-apartment-units-appraisal-for-total-loss-claims ·
how-rental-property-investors-can-use-appraisals-to-increase-equity ·
why-millennials-and-gen-z-are-choosing-apartments-over-home-ownership

Renting & apartment living (category apartment-living):
requirements-for-apartment-rental-in-austin ·
can-you-stay-in-your-apartment-during-repairs-what-renters-need-to-know ·
why-high-rise-apartments-in-houston-are-the-ultimate-living-experience ·
discover-the-charm-of-allure-hermann-park-apartments ·
discover-the-unrivaled-comforts-of-villas-del-paseo-apartments ·
unlock-your-dream-2-bedroom-apartment-in-lewisville-tx-a-guide-to-exceptional-living-spaces ·
why-urban-living-in-2024-is-the-best-choice-for-your-lifestyle ·
houstons-hottest-apartments-your-guide-to-stylish-city-living ·
live-well-on-a-budget-1-bedroom-houston-apartments-under-1000 ·
charge-up-and-chill-ev-friendly-apartments-in-katy-and-houston ·
find-the-perfect-summer-apartment-for-students-in-houston ·
apartments-for-families-finding-kid-friendly-features ·
living-in-modular-apartments-whats-the-appeal ·
how-to-personalize-your-rental-without-losing-your-deposit-8-pro-tips-for-a-stylish-secure-space ·
multi-purpose-furniture-ideas-for-studio-apartments-maximize-space-with-style ·
fall-decorating-tips-for-your-apartment-balcony ·
apartment-pools-rules-etiquette-safety ·
turning-an-apartment-balcony-into-a-mini-garden ·
affordable-furniture-ideas-for-student-housing ·
student-housing-hacks-to-save-you-time-and-money ·
how-to-soundproof-your-student-room-without-breaking-the-rules

## Legacy source text

`backup/posts-clean.json` holds every old post keyed by slug: `title`, `date`, `links`
(outbound links to keep) and `text` (old body). Read the old post for its intent and any
facts/links worth keeping, then write a fresh, better article — don't paraphrase it
sentence by sentence.
