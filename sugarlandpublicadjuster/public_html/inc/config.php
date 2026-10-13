<?php
/**
 * Sugar Land Public Adjuster — site-wide constants and helpers.
 * Every page includes this file (via inc/layout.php).
 */

const SITE = [
    'name'          => 'Sugar Land Public Adjuster',
    'origin'        => 'https://sugarlandpublicadjuster.com',
    'phone_display' => '+1 (832) 503-5866',
    'phone_short'   => '(832) 503-5866',
    'phone_href'    => '+18325035866',
    'email'         => 'jditt@risepublicadjusting.com',
    'lead_to'       => 'jditt@risepublicadjusting.com',
    'mail_from'     => 'noreply@sugarlandpublicadjuster.com',
    'city'          => 'Sugar Land',
    'state'         => 'TX',
    'county'        => 'Fort Bend County',
    'lat'           => '29.6197',
    'lng'           => '-95.6349',
    'firm'          => 'Rise Public Adjusting LLC',
    'firm_license'  => '3356839',
    'logo'          => '/wp-content/uploads/2026/02/Sugar-Land-Public-Adjuster-Site-Logo-1.webp',
    'logo_white'    => '/wp-content/uploads/2026/02/Sugar-Land-Public-Adjuster-Site-Logo-White-1.webp',
    'og_image'      => '/wp-content/uploads/2026/02/Sugar-Land-Public-Adjuster-Site-Image-1.webp',
];

const AUTHOR = [
    'name'     => 'Joseph Dittman',
    'slug'     => 'joseph-dittman',
    'url'      => '/author/joseph-dittman/',
    'title'    => 'Licensed Texas Public Adjuster',
    'image'    => '/assets/img/joseph-dittman-public-adjuster.webp',
    'short'    => 'Joseph Dittman is a licensed Texas public adjuster with Rise Public Adjusting LLC, the firm behind TX Public Adjusting. He represents Sugar Land and Fort Bend County homeowners and business owners on hail, wind, hurricane, water and fire claims—working for the policyholder, never the insurance company.',
    'sameAs'   => ['https://txpublicadjusting.com/about-us/'],
];

/** Main navigation: label => [href, children]. */
const NAV = [
    ['Home', '/', []],
    ['About Us', '/about-us/', [
        ['About Our Team', '/about-us/'],
        ['Joseph Dittman, Public Adjuster', '/author/joseph-dittman/'],
        ['Service Areas', '/service-areas/'],
        ['FAQ', '/faq/'],
    ]],
    ['Services', '/services/', [
        ['All Claim Services', '/services/'],
        ['Hurricane & Wind Damage', '/services/hurricane-wind-damage-claims/'],
        ['Hail Damage', '/services/hail-damage-claims/'],
        ['Water Damage & Burst Pipes', '/services/water-damage-claims/'],
        ['Fire & Smoke Damage', '/services/fire-smoke-damage-claims/'],
        ['Flood Claims', '/services/flood-damage-claims/'],
        ['Commercial Property', '/services/commercial-property-claims/'],
        ['Denied & Underpaid Claims', '/services/denied-underpaid-claims/'],
    ]],
    ['Tools', '/tools/', [
        ['All Tools & Calculators', '/tools/'],
        ['Claim Settlement Calculator', '/tools/insurance-claim-settlement-calculator/'],
        ['Depreciation (ACV) Calculator', '/tools/depreciation-calculator/'],
        ['Public Adjuster Fee Calculator', '/tools/public-adjuster-fee-calculator/'],
        ['Hurricane Deductible Calculator', '/tools/hurricane-deductible-calculator/'],
        ['Texas Claim Deadline Calculator', '/tools/claim-deadline-calculator/'],
        ['Home Inventory Builder', '/tools/home-inventory-checklist/'],
    ]],
    ['Storm Center', '/sugar-land-weather/', [
        ['Live Sugar Land Weather', '/sugar-land-weather/'],
        ['Sugar Land Storm History', '/sugar-land-storm-history/'],
        ['Hurricane Prep Checklist', '/hurricane-preparedness-checklist/'],
    ]],
    ['Blog', '/blog/', []],
    ['Contact', '/contact/', []],
];

const DAMAGE_TYPES = [
    'Hurricane / wind', 'Hail', 'Water / burst pipe', 'Roof leak', 'Fire / smoke',
    'Flood', 'Commercial property', 'Denied or underpaid claim', 'Other',
];

function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

function abs_url(string $path): string
{
    return preg_match('#^https?://#', $path) ? $path : SITE['origin'] . $path;
}

function tel_link(string $label = null, string $class = ''): string
{
    $label = $label ?? SITE['phone_display'];
    return '<a href="tel:' . SITE['phone_href'] . '"' . ($class ? ' class="' . e($class) . '"' : '') . '>' . e($label) . '</a>';
}

function sms_link(string $label = null, string $class = ''): string
{
    $label = $label ?? 'Text ' . SITE['phone_display'];
    return '<a href="sms:' . SITE['phone_href'] . '"' . ($class ? ' class="' . e($class) . '"' : '') . '>' . e($label) . '</a>';
}

function current_path(): string
{
    $p = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
    return $p ?: '/';
}
