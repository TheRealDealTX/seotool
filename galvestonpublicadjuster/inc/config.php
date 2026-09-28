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
