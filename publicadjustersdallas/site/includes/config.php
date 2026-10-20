<?php
/**
 * Site configuration — Dallas Public Adjuster (publicadjustersdallas.com).
 *
 * Do NOT put passwords in this file. Secrets (SMTP password, cron key) belong in
 * one of these private override files, which are loaded in this order:
 *
 *   1. ../pad-config.php            (one level ABOVE public_html — recommended)
 *   2. includes/config.local.php    (inside public_html, blocked by .htaccess)
 *
 * Copy includes/config.local.sample.php to either location and fill it in.
 */

declare(strict_types=1);

if (!defined('MPA_ROOT')) {
    define('MPA_ROOT', dirname(__DIR__));
}

$MPA_CONFIG = [
    // ---- Site identity -------------------------------------------------
    'site_url'        => 'https://publicadjustersdallas.com', // no trailing slash
    'site_name'       => 'Dallas Public Adjuster',
    'company'         => 'Rise Public Adjusting LLC',
    'license'         => '3356839',            // Texas Department of Insurance license number
    'phone_display'   => '+1 (832) 503-5866',
    'phone_short'     => '(832) 503-5866',
    'phone_e164'      => '+18325035866',
    'public_email'    => 'info@publicadjustersdallas.com',
    'author_name'     => 'Joseph Dittman',
    'author_title'    => 'Licensed Texas Public Adjuster',
    // Direct line to Joseph Dittman (shown on contact, author, and about pages).
    'author_email'    => 'jditt@risepublicadjusting.com',
    'service_area'    => 'Dallas, Dallas County, and surrounding North Texas communities',
    'lat'             => 32.7767,
    'lon'             => -96.7970,
    'timezone'        => 'America/Chicago',

    // ---- Free Claim Review form ---------------------------------------
    // Every form on the site (popup, contact, Free Claim Review) is delivered here.
    'mail_to'         => 'info@publicadjustersdallas.com',
    'mail_from'       => 'info@publicadjustersdallas.com',   // must be a mailbox on your SMTP account
    'mail_from_name'  => 'Dallas Public Adjuster Website',
    'smtp_host'       => 'smtp.hostinger.com',
    'smtp_port'       => 465,
    'smtp_secure'     => 'ssl',            // 'ssl' for 465, 'tls' for 587
    'smtp_user'       => 'info@publicadjustersdallas.com',
    'smtp_pass'       => '',               // set in a private override file
    'smtp_debug'      => 0,                // 0 in production
    'allow_mail_fallback' => true,         // use PHP mail() until the SMTP password is set (set false once SMTP works)

    'uploads_enabled'     => true,
    'upload_max_files'    => 3,
    'upload_max_bytes'    => 8 * 1024 * 1024,   // per file
    'upload_total_bytes'  => 20 * 1024 * 1024,
    'rate_limit_max'      => 5,      // submissions per IP per window
    'rate_limit_window'   => 3600,   // seconds
    'min_fill_seconds'    => 3,      // reject forms submitted faster than a human can

    // ---- Weather + storm data -----------------------------------------
    // api.weather.gov requires a User-Agent that identifies the app and a contact.
    'nws_user_agent'  => 'PublicAdjustersDallas.com weather page (info@publicadjustersdallas.com)',
    'nws_station'     => 'KDAL',       // Dallas Love Field
    'county_name'     => 'Dallas',
    'county_fips'     => '113',
    'state_abbr'      => 'TX',
    'state_name'      => 'TEXAS',
    'nws_office'      => 'FWD',        // NWS Fort Worth/Dallas
    // Storm reports outside this box (lat/lon) are ignored: Dallas County plus a small margin.
    'event_bbox'      => [32.50, 33.06, -97.08, -96.46],
    'cache_ttl_current'  => 600,       // 10 minutes
    'cache_ttl_forecast' => 1800,      // 30 minutes
    'cache_ttl_alerts'   => 300,       // 5 minutes
    'http_timeout'       => 8,

    // Secret for running cron scripts over HTTP (CLI does not need it).
    'cron_key'        => '',

    'analytics_id'    => '',           // e.g. G-XXXXXXX; empty = no analytics loaded
];

foreach ([dirname(MPA_ROOT) . '/pad-config.php', __DIR__ . '/config.local.php'] as $override) {
    if (is_file($override)) {
        $local = require $override;
        if (is_array($local)) {
            $MPA_CONFIG = array_replace($MPA_CONFIG, $local);
        }
        break;
    }
}

date_default_timezone_set($MPA_CONFIG['timezone']);

function cfg(string $key, $default = null)
{
    global $MPA_CONFIG;
    return $MPA_CONFIG[$key] ?? $default;
}
