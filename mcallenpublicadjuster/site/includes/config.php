<?php
/**
 * Site configuration — McAllen Public Adjuster.
 *
 * Do NOT put passwords in this file. Secrets (SMTP password, cron key) belong in
 * one of these private override files, which are loaded in this order:
 *
 *   1. ../mpa-config.php            (one level ABOVE public_html — recommended)
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
    'site_url'        => 'https://mcallenpublicadjuster.com', // no trailing slash
    'site_name'       => 'McAllen Public Adjuster',
    'company'         => 'Rise Public Adjusting LLC',
    'license'         => '3356839',            // Texas Department of Insurance license number
    'phone_display'   => '+1 (832) 503-5866',
    'phone_short'     => '(832) 503-5866',
    'phone_e164'      => '+18325035866',
    'public_email'    => 'info@mcallenpublicadjuster.com',
    'author_name'     => 'Joseph Dittman',
    'author_title'    => 'Public Adjuster',
    'service_area'    => 'McAllen, Hidalgo County, and surrounding Rio Grande Valley communities',
    'lat'             => 26.2034,
    'lon'             => -98.2300,
    'timezone'        => 'America/Chicago',

    // ---- Free Claim Review form ---------------------------------------
    // Internal recipient. Never printed on any page.
    'mail_to'         => 'jditt@risepublicadjusting.com',
    'mail_from'       => 'info@mcallenpublicadjuster.com',   // must be a mailbox on your SMTP account
    'mail_from_name'  => 'McAllen Public Adjuster Website',
    'smtp_host'       => 'smtp.hostinger.com',
    'smtp_port'       => 465,
    'smtp_secure'     => 'ssl',            // 'ssl' for 465, 'tls' for 587
    'smtp_user'       => 'info@mcallenpublicadjuster.com',
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
    'nws_user_agent'  => 'McAllenPublicAdjuster.com weather page (info@mcallenpublicadjuster.com)',
    'nws_station'     => 'KMFE',       // McAllen Miller International Airport
    'county_name'     => 'Hidalgo',
    'county_fips'     => '215',
    'state_abbr'      => 'TX',
    'state_name'      => 'TEXAS',
    'nws_office'      => 'BRO',        // NWS Brownsville/Rio Grande Valley
    'cache_ttl_current'  => 600,       // 10 minutes
    'cache_ttl_forecast' => 1800,      // 30 minutes
    'cache_ttl_alerts'   => 300,       // 5 minutes
    'http_timeout'       => 8,

    // Secret for running cron scripts over HTTP (CLI does not need it).
    'cron_key'        => '',

    'analytics_id'    => '',           // e.g. G-XXXXXXX; empty = no analytics loaded
];

foreach ([dirname(MPA_ROOT) . '/mpa-config.php', __DIR__ . '/config.local.php'] as $override) {
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
