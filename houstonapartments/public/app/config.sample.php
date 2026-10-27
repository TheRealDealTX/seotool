<?php
// Copy to config.local.php (never committed) and fill in. On Hostinger the
// file lives at public_html/app/config.local.php; it only returns an array,
// so a direct request to it prints nothing.
return [
    'site_url'    => 'https://houstonapartments.com',
    // When requests arrive on this host (or www.), site_url switches to it and
    // indexing turns on automatically; set force_noindex => true to keep it hidden.
    'live_host'   => 'houstonapartments.com',
    // MySQL on the same server: host "localhost" (socket), not the hstgr.io host.
    'db_dsn'      => 'mysql:host=localhost;dbname=DBNAME;charset=utf8mb4',
    'db_user'     => 'DBUSER',
    'db_pass'     => 'DBPASS',
    // Local development: 'db_dsn' => 'sqlite:' . __DIR__ . '/data/dev.sqlite',

    // riseapartments.com WordPress application password (user: riseapartments)
    'rise_user'   => 'riseapartments',
    'rise_pass'   => '',
    // Rise "city" taxonomy IDs to import (21 = Houston Apartments)
    'rise_cities' => [21],

    // Secret for /admin/* (sync trigger, leads list): ?key=...
    'admin_key'   => '',
    // Lead notifications; empty = store in the database only
    'lead_email'  => 'info@houstonapartments.com',
    // Outgoing mail for lead notifications (the domain's own mailbox; password only in config.local.php)
    'smtp_host'   => 'smtp.hostinger.com',
    'smtp_port'   => 465,
    'smtp_user'   => 'info@houstonapartments.com',
    'smtp_pass'   => '',
    // How rents appear to visitors: 'starts_at' ("Starts at $1,480") or
    // 'hidden' (always "Check for availability"). Filters use the real numbers either way.
    'price_display' => 'hidden',
    // Search-engine indexing; keep false on the temporary domain
    'indexable'   => false,
    // Vector map style (OpenFreeMap: free, no key, commercial use allowed)
    'map_style'   => 'https://tiles.openfreemap.org/styles/liberty',
    'map_attr'    => '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',
];
