<?php
/**
 * RodeoTexas.org configuration — EXAMPLE (no real credentials).
 *
 * Copy to app/config.php (one level ABOVE public_html, so it is never web
 * accessible) and fill in the values. Keep file permissions at 600 or 640.
 */
return [
    // Public URL, no trailing slash. Used for canonical links, sitemaps, e-mails.
    'base_url'  => 'https://rodeotexas.org',
    'site_name' => 'Rodeo Texas',

    // Hostinger: the app connects to MySQL on the same server.
    // hPanel → Databases → Management shows the database name and user.
    'db' => [
        'host'    => '127.0.0.1',
        'port'    => 3306,
        'name'    => 'u000000000_rodeo',
        'user'    => 'u000000000_rodeo',
        'pass'    => 'CHANGE-ME',
        'charset' => 'utf8mb4',
    ],

    // Receives form submissions, correction reports and import-failure alerts.
    // Never printed on the public site.
    'admin_email' => 'you@example.com',
    // Sender address for outgoing mail. Use an address on your own domain.
    'mail_from'   => 'no-reply@rodeotexas.org',

    // 64 random hex characters, e.g. output of: php -r "echo bin2hex(random_bytes(32));"
    // Used to hash visitor IPs (rate limiting) and sign public-form tokens.
    'app_secret' => 'CHANGE-ME-TO-64-RANDOM-HEX-CHARACTERS',

    'import' => [
        // The weekly import runs when cron fires AND it is this hour on this
        // weekday in America/Chicago (1 = Monday). See docs/DEPLOYMENT.md.
        'weekly_weekday'    => 1,
        'weekly_hour_local' => 7,
        // Optional daily re-check of events in the next 7 days (cron must also call --daily).
        'daily_enabled'     => false,
        'daily_hour_local'  => 6,
        // Identify ourselves honestly to source websites.
        'user_agent'        => 'RodeoTexasBot/1.0 (+https://rodeotexas.org/about/)',
        'max_geocodes_per_run' => 40,
        'alert_on_failure'  => true,
    ],

    // OpenStreetMap Nominatim (free, no key; max 1 request/second, results cached).
    'geocoder' => [
        'enabled'  => true,
        'endpoint' => 'https://nominatim.openstreetmap.org/search',
    ],

    // Leaflet map tiles (free OpenStreetMap tiles; attribution required).
    'map' => [
        'tile_url'    => 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        'attribution' => '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    ],

    // Show PHP errors in the browser. Keep false in production.
    'debug' => false,
];
