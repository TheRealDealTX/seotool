<?php
/**
 * Site configuration — Port Arthur Public Adjuster.
 *
 * Do NOT put passwords in this file. Secrets (SMTP password, cron key) belong in
 * one of these private override files, which are loaded in this order:
 *
 *   1. ../papa-config.php           (one level ABOVE public_html — recommended)
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
    'site_url'        => 'https://portarthurpublicadjuster.com', // no trailing slash
    'site_name'       => 'Port Arthur Public Adjuster',
    'company'         => 'Rise Public Adjusting LLC',
    'license'         => '3356839',            // Texas Department of Insurance license number
    'phone_display'   => '+1 (832) 503-5866',
    'phone_short'     => '(832) 503-5866',
    'phone_e164'      => '+18325035866',
    'public_email'    => 'info@portarthurpublicadjuster.com',
    'author_name'     => 'Joseph Dittman',
    'author_title'    => 'Licensed Public Adjuster',
    'service_area'    => 'Port Arthur, Jefferson County, and surrounding Southeast Texas communities',
    'lat'             => 29.8850,
    'lon'             => -93.9399,
    'timezone'        => 'America/Chicago',

    // ---- Free Claim Review form ---------------------------------------
    // Every Free Claim Review / contact / popup submission is emailed here.
    'mail_to'         => 'info@portarthurpublicadjuster.com',
    'mail_from'       => 'info@portarthurpublicadjuster.com',   // must be a mailbox on your SMTP account
    'mail_from_name'  => 'Port Arthur Public Adjuster Website',
    'smtp_host'       => 'smtp.hostinger.com',
    'smtp_port'       => 465,
    'smtp_secure'     => 'ssl',            // 'ssl' for 465, 'tls' for 587
    'smtp_user'       => 'info@portarthurpublicadjuster.com',
    'smtp_pass'       => '',               // set in a private override file
    'smtp_debug'      => 0,                // 0 in production
    'allow_mail_fallback' => true,         // use Hostinger's PHP mail() until an SMTP password is set (SMTP is preferred)

    'uploads_enabled'     => true,
    'upload_max_files'    => 3,
    'upload_max_bytes'    => 8 * 1024 * 1024,   // per file
    'upload_total_bytes'  => 20 * 1024 * 1024,
    'rate_limit_max'      => 5,      // submissions per IP per window
    'rate_limit_window'   => 3600,   // seconds
    'min_fill_seconds'    => 3,      // reject forms submitted faster than a human can

    // ---- Weather + storm data -----------------------------------------
    // api.weather.gov requires a User-Agent that identifies the app and a contact.
    'nws_user_agent'  => 'PortArthurPublicAdjuster.com weather page (info@portarthurpublicadjuster.com)',
    'nws_station'     => 'KBPT',       // Jack Brooks Regional Airport (Beaumont/Port Arthur)
    'county_name'     => 'Jefferson',
    'county_fips'     => '245',
    'state_abbr'      => 'TX',
    'state_name'      => 'TEXAS',
    'nws_office'      => 'LCH',        // NWS Lake Charles (covers Southeast Texas)
    'cache_ttl_current'  => 600,       // 10 minutes
    'cache_ttl_forecast' => 1800,      // 30 minutes
    'cache_ttl_alerts'   => 300,       // 5 minutes
    'http_timeout'       => 8,

    // Secret for running cron scripts over HTTP (CLI does not need it).
    'cron_key'        => '',

    // Map/zone settings used by the storm tools and NWS/IEM storm-report filters.
    'map_center'      => [29.92, -94.08],
    'map_zoom'        => 10,
    'event_bbox'      => [29.45, 30.25, -94.50, -93.70], // lat min, lat max, lon min, lon max (Jefferson County + margin)
    'nhc_feed'        => 'https://www.nhc.noaa.gov/CurrentStorms.json',
    'cache_ttl_tropics' => 900,

    'analytics_id'    => '',           // e.g. G-XXXXXXX; empty = no analytics loaded
];

foreach ([dirname(MPA_ROOT) . '/papa-config.php', __DIR__ . '/config.local.php'] as $override) {
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
