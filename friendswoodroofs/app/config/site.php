<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/**
 * Public site settings for Friendswood Roofers.
 *
 * Everything in this file is safe to publish: no email addresses, passwords or
 * SMTP details. Mail settings live in config/mail.php (see mail.example.php).
 */
return [
    'name'         => 'Friendswood Roofers',
    'base_url'     => 'https://friendswoodroofs.com', // no trailing slash
    'city'         => 'Friendswood',
    'state'        => 'TX',
    'state_name'   => 'Texas',

    // Phone shown on the site and used for every tel: link.
    'phone_display' => '+1 (512) 297-7580',
    'phone_tel'     => '+15122977580',

    // Map centre used for the weather embed and structured data (City of Friendswood).
    'geo' => ['lat' => 29.5294, 'lng' => -95.2010],

    /*
     * Blog publication schedule.
     * The newest article is dated on this launch date; the others are dated
     * 3, 6, 9 and 12 days earlier (see content/articles.php). Change it to the
     * owner-approved launch date before going live. Format: YYYY-MM-DD.
     */
    'launch_date' => '2026-10-01',
    'timezone'    => 'America/Chicago',

    /*
     * Cities served. Only Friendswood is listed until the owner confirms more.
     * Adding a city here adds it to the Service Area page and structured data.
     */
    'service_cities' => ['Friendswood'],

    // Weather map (RainViewer embed). See README "Weather map".
    'weather' => [
        'enabled'  => true,
        'zoom'     => 8,
        'provider' => 'RainViewer',
        'provider_url' => 'https://www.rainviewer.com/',
    ],

    // Set to false only on a staging copy to send "noindex" on every page.
    'indexable' => true,
];
