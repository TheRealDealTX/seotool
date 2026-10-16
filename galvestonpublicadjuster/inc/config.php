<?php
// Site-wide constants. Everything business-specific lives here.
const SITE_NAME   = 'Galveston Public Adjuster';
const SITE_URL    = 'https://galvestonpublicadjuster.com';
const PHONE       = '(832) 503-5866';
const PHONE_TEL   = '+18325035866';
const LEAD_EMAIL  = 'jditt@risepublicadjusting.com';
const MAIL_FROM   = 'noreply@galvestonpublicadjuster.com';
const AUTHOR      = 'Joseph Dittman';
const AUTHOR_ROLE = 'Licensed Texas Public Adjuster';
const AUTHOR_PHOTO = '/assets/img/joseph-dittman.webp';
// Firm details (from txpublicadjusting.com). TDI requires address + license number on advertising.
const FIRM        = 'Rise Public Adjusting LLC';
const LICENSE_NO  = '3356839';
const STREET      = '5514 Imogen Dr.';
const ADDR_CITY   = 'Belton';
const ZIP         = '76513';
const HOURS       = 'Mon–Fri 9 AM–6 PM';
const SISTER_SITE = 'https://txpublicadjusting.com/';
const CITY        = 'Galveston';
const REGION      = 'TX';
const GEO_LAT     = 29.3013;
const GEO_LNG     = -94.7977;

// Weather-event threshold: sustained wind or gust at or above this (mph).
const WIND_EVENT_MPH = 70;

define('ROOT', dirname(__DIR__));
define('DATA', ROOT . '/data');
// Private dir one level above the web root (leads log, API key). Falls back to data/private.
define('PRIVATE_DIR', is_writable(dirname(ROOT)) ? dirname(ROOT) . '/gpa-private' : DATA . '/private');

// Main navigation: path => label
const NAV = [
    '/twia-claims-expert/'       => 'TWIA Claims',
    '/galveston-fire-claims/'    => 'Fire Claims',
    '/calculators/'              => 'Calculators',
    '/texas-windstorm-rules/'    => 'Windstorm Rules',
    '/galveston-local-code/'     => 'Local Code',
    '/galveston-storm-history/'  => 'Storm History',
    '/weather-events/'           => 'Weather',
    '/blog/'                     => 'Blog',
    '/about/'                    => 'About',
];

const AREAS = ['Galveston Island', 'Jamaica Beach', 'Bolivar Peninsula', 'Tiki Island', 'Texas City',
    'La Marque', 'Hitchcock', 'Santa Fe', 'Dickinson', 'League City', 'Kemah', 'Friendswood', 'Bacliff', 'San Leon'];

// Launch date, and the last material edit of each static page (pages/<name>.php). The sitemap's
// <lastmod> comes from here, not from file mtimes (every deploy rewrites every mtime). Bump a
// page's date when you change its content; pages that list runtime data (home, blog, weather)
// also take the newest item they show.
const LAUNCH_DATE  = '2026-09-28';
const PAGE_UPDATED = [
    'home'            => '2026-10-16',
    'about'           => '2026-10-16',
    'twia'            => '2026-10-16',
    'fire'            => '2026-10-16',
    'calculators'     => '2026-10-16',
    'windstorm-rules' => '2026-10-16',
    'local-code'      => '2026-10-16',
    'storm-history'   => '2026-10-16',
    'weather-events'  => '2026-10-16',
    'blog'            => '2026-10-16',
    'contact'         => '2026-10-16',
    'privacy'         => '2026-09-28',
];
