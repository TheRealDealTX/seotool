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
const ASSET_VER   = '20261028b';                     // bump to bust browser caches for CSS/JS

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
    ['House Designs', '/home-designs/', null],
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
