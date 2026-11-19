<?php defined('SNW') || (http_response_code(404) && exit);
/*
 * Site-wide settings. Edit here; nothing else needs to change.
 */
return [
    'name'        => 'Seattle Northwest Homes',
    'url'         => 'https://seattlenorthwesthomes.com',   // canonical origin, no trailing slash
    'email'       => 'info@seattlenorthwesthomes.com',      // shown on the site and receives form leads (SMTP login in app/secrets.php)
    'phone'       => '',                                     // e.g. '(206) 555-0100' — leave blank to hide
    'agent'       => 'Selena',
    // Washington advertising rules require the licensed brokerage firm's name on
    // real estate ads. Fill this in before launch; it prints in the footer and on listings.
    'brokerage'   => '',
    'city'        => 'Seattle',
    'region'      => 'WA',
    'geo'         => ['lat' => 47.6062, 'lng' => -122.3321],
    'tagline'     => 'Seattle homes for sale, neighborhood guides and local real estate advice.',
    'social'      => [],
    // Google Tag Manager container. Set to '' to remove the tag from every page.
    'gtm_id'      => 'GTM-PSCQN66D',                                     // ['https://www.facebook.com/…', …]
    // Shown under every listing until the data comes from a live MLS/IDX feed.
    // Set to '' once app/data/listings.php holds real, current inventory.
    'listing_note' => 'Featured homes are representative of properties we help clients buy and sell across Seattle. Availability, pricing and details change quickly — contact us for current status before making plans.',
    // Canonical host enforcement: 301 http:// and any other hostname (www., preview) to 'url'.
    'force_canonical_host' => true,
    // Where form submissions are stored: beside the web root when PHP may write there,
    // otherwise app/storage (every file there is a .php that exits immediately).
    'storage_dir' => dirname(PUBLIC_DIR) . '/snw-storage',
];
