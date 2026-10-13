<?php
// Houston Public Adjusters — site-wide constants. Every page includes this via inc/layout.php.

const SITE_NAME   = 'Houston Public Adjusters';
const SITE_URL    = 'https://houstonpublicadjusting.com';
const LEGAL_NAME  = 'Rise Public Adjusting LLC';
const LICENSE_NO  = '3356839';
const PHONE_DISPLAY = '(832) 503-5866';
const PHONE_E164  = '+18325035866';
const EMAIL       = 'jditt@risepublicadjusting.com';
const HOURS_TEXT  = 'Mon–Fri 9 AM–6 PM · call or text anytime';
const GEO_LAT     = '29.7604';
const GEO_LNG     = '-95.3698';

// Where lead-form submissions are delivered.
const LEAD_TO     = 'jditt@risepublicadjusting.com';
// The "From" address on lead emails. On Hostinger this must be a mailbox on a
// domain hosted in the same account (create it in hPanel > Emails), otherwise
// mail() output is likely to be rejected or land in spam.
const LEAD_FROM   = 'noreply@houstonpublicadjusting.com';

// Optional authenticated SMTP (recommended). Leave SMTP_HOST empty to use PHP mail().
// Hostinger: smtp.hostinger.com, port 465, user = the full mailbox address.
const SMTP_HOST   = '';
const SMTP_PORT   = 465;
const SMTP_USER   = '';
const SMTP_PASS   = '';

const AUTHOR = [
    'name'   => 'Joseph Dittman',
    'slug'   => 'joseph-dittman',
    'url'    => '/author/joseph-dittman/',
    'title'  => 'Licensed Texas Public Adjuster',
    'photo'  => '/assets/img/joseph-dittman-public-adjuster.webp',
    'short'  => 'Joseph Dittman is a licensed Texas public adjuster with Rise Public Adjusting LLC (TDI license #3356839) and the adjuster behind Houston Public Adjusters and TX Public Adjusting. He represents homeowners and business owners — never insurance companies — on hurricane, hail, wind, water, fire and commercial property claims across Houston and the rest of Texas.',
    'sameAs' => ['https://txpublicadjusting.com/about-us/'],
];

const NAV = [
    ['Services', '/services/'],
    ['Tools', '/tools/'],
    ['Weather', '/houston-weather/'],
    ['Storm History', '/houston-storm-history/'],
    ['Blog', '/blog/'],
    ['About', '/about-us/'],
    ['Contact', '/contact/'],
];

// Greater Houston communities served (also used by the weather tracker).
const AREAS = [
    ['Houston',        29.7604, -95.3698, 'Harris'],
    ['Katy',           29.7858, -95.8245, 'Harris / Fort Bend / Waller'],
    ['Sugar Land',     29.6197, -95.6349, 'Fort Bend'],
    ['The Woodlands',  30.1658, -95.4613, 'Montgomery'],
    ['Cypress',        29.9691, -95.6972, 'Harris'],
    ['Spring',         30.0799, -95.4172, 'Harris'],
    ['Pearland',       29.5636, -95.2860, 'Brazoria'],
    ['Pasadena',       29.6911, -95.2091, 'Harris'],
    ['Humble',         29.9988, -95.2622, 'Harris'],
    ['Kingwood',       30.0500, -95.1872, 'Harris'],
    ['League City',    29.5075, -95.0949, 'Galveston'],
    ['Baytown',        29.7355, -94.9774, 'Harris / Chambers'],
    ['Missouri City',  29.6186, -95.5377, 'Fort Bend'],
    ['Friendswood',    29.5294, -95.2010, 'Galveston / Harris'],
    ['Bellaire',       29.7058, -95.4588, 'Harris'],
    ['Tomball',        30.0972, -95.6161, 'Harris'],
    ['Conroe',         30.3119, -95.4561, 'Montgomery'],
    ['Galveston',      29.3013, -94.7977, 'Galveston'],
];
