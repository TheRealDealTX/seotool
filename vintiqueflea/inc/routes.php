<?php
/** Route tables and the legacy (WordPress) URL map. Keys have no leading/trailing slash. */

const STATIC_PAGES = [
    'about'                => 'about',
    'contact'              => 'contact',
    'vendors'              => 'vendors',
    'food-trucks'          => 'food-trucks',
    'affiliate-disclosure' => 'disclosure',
    'privacy-policy'       => 'privacy',
];

/** Old URLs worth keeping → rewritten, keyword-focused URLs (301). */
const LEGACY_REDIRECTS = [
    // Pages
    'about-us'    => '/about/',
    'our-events'  => '/events/',
    'contact-us'  => '/contact/',
    'write-for-us' => '/vendors/',
    // Event posts
    'vintique-flea-houston-summer-edition' => '/events/summer-vintage-market-houston/',
    'vintique-flea-summer-edition-2'       => '/events/summer-vintage-market-houston/',
    'vintique-flea-houston-fall-edition'   => '/events/fall-vintage-market-houston/',
    'vintique-flea-houston-winter-edition' => '/events/winter-vintage-market-houston/',
    // Relevant posts, rewritten as guides
    'houstons-shopping-scene-from-boutiques-to-malls' => '/guides/houston-vintage-shopping-guide/',
    'exploring-houston-your-weekend-guide-to-fun-and-adventure' => '/guides/things-to-do-in-houston-this-weekend/',
    'houstons-seasonal-delights-festivals-and-events-year-round' => '/guides/houston-markets-festivals-calendar/',
    'apartment-living-near-farmers-markets-access-to-fresh-produce-and-more' => '/guides/houston-markets-festivals-calendar/',
    'houstons-thriving-arts-and-entertainment-scene' => '/guides/washington-avenue-arts-district/',
    'mixing-patterns-and-textures-in-small-spaces' => '/guides/mixing-vintage-patterns-textures/',
    'how-to-display-your-travel-souvenirs-in-small-apartments' => '/guides/display-vintage-collectibles-small-spaces/',
    'creating-a-cozy-apartment-entryway-first-impressions-matter' => '/guides/vintage-entryway-decor-ideas/',
    'top-budget-friendly-restaurants-in-houston-for-2023' => '/food-trucks/',
    '10-smart-upgrades-that-instantly-boost-your-homes-value' => '/shop/architectural-salvage-industrial/',
    'exploring-houston-what-the-city-is-known-for-and-worth-visiting' => '/guides/things-to-do-in-houston-this-weekend/',
    'why-you-should-live-in-houston-a-hub-of-first-class-attractions-and-endless-entertainment' => '/guides/things-to-do-in-houston-this-weekend/',
    // Categories
    'category/events'                      => '/events/',
    'category/this-weekend'                => '/guides/things-to-do-in-houston-this-weekend/',
    'category/top-things-this-week'        => '/guides/things-to-do-in-houston-this-weekend/',
    'category/best-things-to-do-in-houston' => '/guides/things-to-do-in-houston-this-weekend/',
    'category/things-to-do-with-kids'      => '/guides/things-to-do-in-houston-this-weekend/',
    'category/uncategorized'               => '/guides/',
    'category/top-concerts-this-week'      => '/events/',
    'category/get-a-nightlife-this-week'   => '/events/',
    'author/allen'                         => '/about/',
    // Common WP leftovers
    'feed'          => '/guides/',
    'comments/feed' => '/guides/',
    'blog'          => '/guides/',
    'home'          => '/',
    'shop-amazon'   => '/shop/',
    'wp-sitemap.xml' => '/sitemap.xml',
    'sitemap_index.xml' => '/sitemap.xml',
];

/** Off-topic posts removed in the rebuild: answered with 410 Gone so search engines drop them fast. */
const LEGACY_GONE = [
    'navigating-the-houston-housing-market-how-easy-is-it-to-find-an-apartment-in-houston',
    'navigating-employment-opportunities-in-texas-a-2023-overview',
    'cost-of-living-in-houston-texas-in-2023',
    'making-the-most-of-your-stay-in-houston-a-comprehensive-guide',
    'top-vacation-spots-in-houston-for-2023',
    'apartment-prices-in-houston-a-2023-guide',
    'savoring-perfection-the-top-steakhouse-in-houston-for-2023',
    'houston-vs-dallas-why-houston-takes-the-lead-as-the-preferred-place-to-live',
    'houstons-average-salary-and-its-distinct-advantage-in-texas',
    'first-things-to-do-when-youve-moved-into-an-apartment-in-texas',
    'houstons-commitment-to-sustainability-eco-friendly-initiatives',
    'houstons-energy-hub-a-look-at-the-oil-and-gas-industry',
    'explore-houstons-high-rise-apartments-elevating-urban-living',
    'discover-luxury-living-at-pearl-rosemont-in-houstons-montrose-district',
    'welcome-home-to-prose-franz-apartments-katys-premier-living-destination',
    'where-to-rent-in-katy-a-comprehensive-look-at-top-apartment-communities',
    'living-well-in-a-noisy-world-creating-tranquil-spaces-in-busy-apartment-complexes',
    'convenience-at-your-doorstep-stafford-apartments-with-on-site-property-managers',
    'dealing-with-apartment-pests-prevention-and-solutions',
    'living-with-a-partner-in-an-apartment-tips-for-harmony',
    'average-salary-in-the-woodlands-tx-a-guide-to-earnings-and-job-market-trends',
    'whats-the-average-salary-in-piney-point-village-tx-a-deep-dive-into-income-economy-and-opportunities',
    'whats-the-average-salary-in-katy-tx-a-deep-dive-into-income-trends-and-opportunities',
    'whats-the-average-salary-in-sugar-land-tx-a-2025-update',
    'how-much-do-people-earn-in-pasadena-tx-a-look-at-the-average-salary-in-houstons-industrial-hub',
    'your-roof-looks-fine-but-could-still-be-damaged-heres-what-to-check',
    'city-living-redefined-top-apartments-near-westgate-center-houston',
    'do-amenities-really-matter-a-look-at-common-apartment-myths',
    'dont-buy-blind-why-every-real-estate-deal-should-include-a-public-adjuster-review',
    'how-insurance-appraisals-can-affect-your-apartment-investment-returns',
    'how-to-calculate-true-rent-affordability',
    'the-future-of-apartment-real-estate-in-a-remote-work-world',
    'top-challenges-for-real-estate-investors-in-high-risk-weather-zones',
    'can-apartment-living-fuel-your-real-estate-career',
    'your-real-estate-path-to-freedom-and-fulfillment',
    '10-terms-every-real-estate-rookie-should-know',
];

/** WordPress system paths and sitemaps. */
const LEGACY_GONE_PATTERN = '~^(wp-(admin|includes|content|json)(/.*)?|wp-[a-z-]+\.php|xmlrpc\.php|wp-sitemap.*\.xml|readme\.html|license\.txt|page/\d+|tag/.+|category/.+)$~i';
