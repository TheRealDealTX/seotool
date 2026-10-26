<?php
// Copy to config.local.php (never committed) and fill in. On Hostinger the
// file lives at public_html/app/config.local.php; it only returns an array,
// so a direct request to it prints nothing.
return [
    'site_url'    => 'https://houstonapartments.com',
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
    'lead_email'  => '',
    // Search-engine indexing; keep false on the temporary domain
    'indexable'   => false,
    // Vector map style (OpenFreeMap: free, no key, commercial use allowed)
    'map_style'   => 'https://tiles.openfreemap.org/styles/liberty',
    'map_attr'    => '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',
];
