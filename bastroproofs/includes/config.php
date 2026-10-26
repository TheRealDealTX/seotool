<?php
/**
 * Bastrop Roofing — business details, navigation and shared constants.
 * Every page includes this through includes/bootstrap.php, so the phone
 * number, address data and service lists are defined exactly once.
 */

const SITE = [
    'name'          => 'Bastrop Roofing',
    'domain'        => 'bastroproofs.com',
    'origin'        => 'https://bastroproofs.com',
    'phone_display' => '+1 (512) 297-7580',
    'phone_short'   => '(512) 297-7580',
    'phone_href'    => '+15122977580',
    'email'         => 'info@bastroproofs.com',
    'city'          => 'Bastrop',
    'state'         => 'TX',
    'state_long'    => 'Texas',
    'zip'           => '78602',
    'county'        => 'Bastrop County',
    'region'        => 'Central Texas',
    'latitude'      => '30.1105',
    'longitude'     => '-97.3153',
    'hours'         => 'Mon–Sat 7:00 AM – 7:00 PM · Storm calls 24/7',
];

/** Google Analytics 4 measurement ID (gtag.js is loaded on every page by page_start()). */
const GA_ID = 'G-79KFXCNSM4';

/** Where estimate-form submissions are emailed (see contact/send.php). */
const FORM_RECIPIENT = 'info@bastroproofs.com';

const NAV = [
    ['label' => 'Services',      'href' => '/services/', 'children' => 'services'],
    ['label' => 'Metal Roofing', 'href' => '/services/metal-roofing-bastrop-tx/'],
    ['label' => 'Service Areas', 'href' => '/service-areas/', 'children' => 'areas'],
    ['label' => 'Roof Tools',    'href' => '/roofing-tools/', 'children' => 'tools'],
    ['label' => 'Blog',          'href' => '/blog/'],
    ['label' => 'About',         'href' => '/about/'],
];

/** Bastrop neighborhoods and landmarks used across local copy. */
const NEIGHBORHOODS = [
    'Tahitian Village', 'Pine Forest', 'Hunters Crossing', 'ColoVista',
    'The Colony', 'Piney Ridge', 'Pecan Park', 'Downtown Main Street',
    'Lake Bastrop', 'Hills of Bastrop', 'Bastrop Highlands', 'Lost Pines',
];

const SERVING = 'Bastrop, Elgin, Smithville, Cedar Creek, Paige, McDade &amp; Red Rock';
