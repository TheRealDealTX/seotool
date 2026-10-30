<?php
// Cowboy Tiny Homes — site-wide settings. Edit business details here only.

const SITE_NAME   = 'Cowboy Tiny Homes';
const SITE_URL    = 'https://cowboytinyhomes.com';
const SITE_HOST   = 'cowboytinyhomes.com';
const PHONE       = '210-903-9471';
const PHONE_HREF  = 'tel:+12109039471';
const EMAIL       = 'contact@cowboytinyhomes.com';
const LEAD_TO     = 'contact@cowboytinyhomes.com';   // where contact-form leads are emailed
const MAIL_FROM   = 'contact@cowboytinyhomes.com';   // sender; SMTP login comes from inc/secrets.php (server only, not in git)
const GA_ID       = 'G-JJPQXF3CVT';                  // Google Analytics 4 measurement ID (tag is in inc/layout.php <head>)
const ASSET_VER   = '20261030b';                     // bump to bust browser caches for CSS/JS

// Plan store (inc/store.php, shared with tinyhomesblueprint.com). Stripe keys, paid plan
// files and order records live one level above public_html in PRIVATE_DIR:
//   cth-secrets.php  cth-plan-files/  cth-data/
// Until cth-secrets.php has a Stripe key (and a plan's zip is uploaded) plan pages show
// the quote / contact form instead of checkout.
define('PRIVATE_DIR', getenv('CTH_PRIVATE_DIR') ?: dirname(__DIR__, 2));
const STORE_PREFIX = 'cth';
const ORDER_PREFIX = 'CTH';
const SITE_EMAIL   = EMAIL;          // names the shared store code uses
const SITE_PHONE   = PHONE;
const SITE_TEL     = '+12109039471';
const SMTP_FALLBACK_FILE = __DIR__ . '/secrets.php';   // existing contact-form SMTP login (host/port/user/pass)
// Credit offered on every plan page and in the order email.
const PLAN_CREDIT  = 'Build it with us: if Cowboy Tiny Homes builds this home for you under a contract signed within 12 months of your purchase, we credit the full plan price toward the build.';

// Texas cost factors against 2026 US national-average prices. The plan-set generator uses the
// same table (generator/profile.json "cost_regions"); validate.php checks they match.
const TX_REGIONS = [
    ['Austin metro', 1.00], ['Dallas metro', 0.95], ['Houston metro', 0.94], ['Fort Worth metro', 0.93],
    ['San Antonio metro', 0.92], ['Rural Texas', 0.87],
];

/** URL of a plan page. Gonzales Modern Living keeps the URL it has ranked at since the WordPress site. */
function plan_url(string $slug): string {
    return $slug === 'gonzales-modern-living' ? '/gonzales-modern-living/' : "/home-designs/$slug/";
}

// Cities the old site's forms offered, and the area pages built for them.
const SERVICE_CITIES = [
    'san-antonio' => 'San Antonio',
    'austin'      => 'Austin',
    'dallas'      => 'Dallas',
    'fort-worth'  => 'Fort Worth',
    'houston'     => 'Houston',
];

// Primary navigation: label => path, with optional dropdown children.
const NAV = [
    ['Home Builds', '/custom-tiny-homes-texas/', [
        ['Custom Tiny Homes', '/custom-tiny-homes-texas/'],
        ['ADUs, Casitas & Granny Flats', '/adu-builders-texas/'],
        ['Tiny Homes on Wheels', '/tiny-homes-on-wheels-texas/'],
        ['Park Model Homes', '/park-model-homes-texas/'],
        ['Tiny House Design Services', '/tiny-house-design-services/'],
        ['Home Remodel Design', '/home-remodel-design-texas/'],
    ]],
    ['House Plans', '/home-designs/', [
        ['All Texas House Plans', '/home-designs/'],
        ['Small Homes', '/home-designs/#single'],
        ['ADUs & Casitas', '/home-designs/#adu'],
        ['Park Models', '/home-designs/#park'],
        ['Tiny Homes on Wheels', '/home-designs/#thow'],
        ['Studios & Offices', '/home-designs/#studio'],
        ['Gonzales Modern Living', '/gonzales-modern-living/'],
    ]],
    ['Service Areas', '/service-areas/', [
        ['San Antonio', '/tiny-home-builders-san-antonio/'],
        ['Austin', '/tiny-home-builders-austin/'],
        ['Dallas', '/tiny-home-builders-dallas/'],
        ['Fort Worth', '/tiny-home-builders-fort-worth/'],
        ['Houston', '/tiny-home-builders-houston/'],
    ]],
    ['Tools', '/tools/', [
        ['Tiny Home Cost Calculator', '/tools/tiny-home-cost-calculator/'],
        ['Which Tiny Home Fits Me? (Quiz)', '/tools/which-tiny-home-is-right-for-me/'],
        ['Tiny House Size Planner', '/tools/tiny-house-size-planner/'],
        ['ADU Rental Income Calculator', '/tools/adu-rental-income-calculator/'],
        ['Tiny Home Loan Calculator', '/tools/tiny-home-loan-calculator/'],
    ]],
    ['Guides', '/guides/', [
        ['Tiny House Laws in Texas', '/guides/tiny-house-laws-texas/'],
        ['Cost to Build a Tiny House in Texas', '/guides/cost-to-build-a-tiny-house-in-texas/'],
        ['ADU vs Park Model vs Tiny Home on Wheels', '/guides/adu-vs-park-model-vs-tiny-house-on-wheels/'],
        ['How to Choose a Tiny Home Builder', '/guides/how-to-choose-a-tiny-home-builder-in-texas/'],
        ['Tiny Home Financing in Texas', '/guides/tiny-home-financing-texas/'],
        ['FAQs', '/faqs/'],
    ]],
    ['Blog', '/blog/', null],
];

require __DIR__ . '/plans.php';
