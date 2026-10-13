<?php
/**
 * Site-wide settings. This is the only file to edit when the site moves domains.
 *
 * The site runs unchanged on any host. On a host that isn't PRODUCTION_HOST
 * (e.g. the *.hostingersite.com preview) every response is sent with
 * X-Robots-Tag: noindex and robots.txt disallows crawling, so the preview never
 * competes with the live domain in Google.
 */

const PRODUCTION_HOST = 'txpublicadjusting.com';
// Optional: Google Search Console HTML-tag verification code and GA4 measurement ID.
const GOOGLE_SITE_VERIFICATION = '';
const GA4_ID = '';
const CANONICAL_ORIGIN = 'https://txpublicadjusting.com';

const BIZ = [
    'name'          => 'TX Public Adjusting',
    'legal_name'    => 'Rise Public Adjusting LLC',
    'adjuster'      => 'Joseph Dittman',
    'license'       => '3356839',
    'license_url'   => 'https://www.tdi.texas.gov/agent/index.html',
    'phone_display' => '(832) 503-5866',
    'phone_e164'    => '+18325035866',
    'city'          => 'Belton',
    'region'        => 'TX',
    'postal'        => '76513',
    // Street address is kept for schema/GBP consistency but not printed on pages.
    'street'        => '5514 Imogen Dr.',
    'show_street'   => false,
    'lat'           => 31.0560,
    'lng'           => -97.4645,
];

// Where contact-form leads are emailed. Leave empty to only log them to the
// private leads CSV (see leads_file() in lib.php). Better: set it in app/config.local.php (not committed).
$LEAD_EMAIL = '';
$LEAD_FROM  = 'no-reply@' . PRODUCTION_HOST;

if (is_file(__DIR__ . '/config.local.php')) {
    require __DIR__ . '/config.local.php';
}

const NAV = [
    ['Services', '/services/', [
        ['Roof & hail claims', '/services/roof-hail-damage-claims/'],
        ['Water damage claims', '/services/water-damage-claims/'],
        ['Fire & smoke claims', '/services/fire-smoke-damage-claims/'],
        ['Hurricane & wind claims', '/services/hurricane-windstorm-claims/'],
        ['Denied & underpaid claims', '/services/denied-underpaid-claims/'],
        ['Commercial claims', '/commercial-claims/'],
    ]],
    ['Free tools', '/tools/', [
        ['Settlement calculator', '/tools/claim-settlement-calculator/'],
        ['Claim deadline calculator', '/tools/texas-claim-deadline-calculator/'],
        ['Documentation checklist', '/tools/claim-documentation-checklist/'],
        ['Contents inventory builder', '/tools/contents-inventory-builder/'],
        ['Storm report lookup', '/tools/storm-report-lookup/'],
        ['Do I need a public adjuster?', '/tools/do-i-need-a-public-adjuster/'],
    ]],
    ['Service areas', '/areas/', null],
    ['Guides', '/blog/', null],
    ['About', '/about-us/', null],
];

const CATEGORIES = [
    'Public Adjusters 101' => 'public-adjusters-101',
    'Claim Process'        => 'claim-process',
    'Hail & Roof'          => 'hail-roof',
    'Fire, Water & Storm'  => 'fire-water-storm',
];
