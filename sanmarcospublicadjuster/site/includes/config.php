<?php
/**
 * Site configuration — San Marcos Public Adjuster.
 *
 * Do NOT put passwords in this file. Secrets (SMTP password, cron key) belong in
 * one of these private override files, which are loaded in this order:
 *
 *   1. ../smpa-config.php           (one level ABOVE public_html — recommended)
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
    'site_url'        => 'https://sanmarcospublicadjuster.com', // no trailing slash
    'site_name'       => 'San Marcos Public Adjuster',
    'company'         => 'Rise Public Adjusting LLC',
    'license'         => '3356839',            // Texas Department of Insurance license number
    'phone_display'   => '+1 (832) 503-5866',
    'phone_short'     => '(832) 503-5866',
    'phone_e164'      => '+18325035866',
    'public_email'    => 'info@sanmarcospublicadjuster.com',
    'author_name'     => 'Joseph Dittman',
    'author_title'    => 'Licensed Texas Public Adjuster',
    'service_area'    => 'San Marcos, Hays County, and surrounding Central Texas communities',
    'lat'             => 29.8833,
    'lon'             => -97.9414,
    'timezone'        => 'America/Chicago',

    // ---- Free Claim Review form ---------------------------------------
    // Every form on the site (5-second popup, homepage, contact, Free Claim Review) is delivered here.
    'mail_to'         => 'info@sanmarcospublicadjuster.com',
    'mail_from'       => 'info@sanmarcospublicadjuster.com',   // must be a mailbox on your SMTP account
    'mail_from_name'  => 'San Marcos Public Adjuster Website',
    'smtp_host'       => 'smtp.hostinger.com',
    'smtp_port'       => 465,
    'smtp_secure'     => 'ssl',            // 'ssl' for 465, 'tls' for 587
    'smtp_user'       => 'info@sanmarcospublicadjuster.com',
    'smtp_pass'       => '',               // set in a private override file
    'smtp_debug'      => 0,                // 0 in production
    'allow_mail_fallback' => false,        // true = use PHP mail() when SMTP password is not set

    'uploads_enabled'     => true,
    'upload_max_files'    => 3,
    'upload_max_bytes'    => 8 * 1024 * 1024,   // per file
    'upload_total_bytes'  => 20 * 1024 * 1024,
    'rate_limit_max'      => 5,      // submissions per IP per window
    'rate_limit_window'   => 3600,   // seconds
    'min_fill_seconds'    => 3,      // reject forms submitted faster than a human can

    // ---- Weather + storm data -----------------------------------------
    // api.weather.gov requires a User-Agent that identifies the app and a contact.
    'nws_user_agent'  => 'SanMarcosPublicAdjuster.com weather page (info@sanmarcospublicadjuster.com)',
    'nws_station'     => 'KHYI',       // San Marcos Regional Airport
    'county_name'     => 'Hays',
    'county_fips'     => '209',
    'state_abbr'      => 'TX',
    'state_name'      => 'TEXAS',
    'nws_office'      => 'EWX',        // NWS Austin/San Antonio (New Braunfels)
    // Storm reports outside this box (lat/lon) are ignored: Hays County plus a small margin.
    'event_bbox'      => [29.70, 30.40, -98.35, -97.65],
    'cache_ttl_current'  => 600,       // 10 minutes
    'cache_ttl_forecast' => 1800,      // 30 minutes
    'cache_ttl_alerts'   => 300,       // 5 minutes
    'http_timeout'       => 8,

    // Secret for running cron scripts over HTTP (CLI does not need it).
    'cron_key'        => '',

    'analytics_id'    => '',           // e.g. G-XXXXXXX; empty = no analytics loaded
];

foreach ([dirname(MPA_ROOT) . '/smpa-config.php', __DIR__ . '/config.local.php'] as $override) {
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
