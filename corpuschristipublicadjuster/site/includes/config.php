<?php
/**
 * Site configuration — Corpus Christi Public Adjuster.
 *
 * Do NOT put passwords in this file. Secrets (SMTP password, cron key) belong in
 * one of these private override files, which are loaded in this order:
 *
 *   1. ../ccpa-config.php            (one level ABOVE public_html — recommended)
 *   2. includes/config.local.php    (inside public_html, blocked by .htaccess)
 *
 * Copy includes/config.local.sample.php to either location and fill it in.
 */

declare(strict_types=1);

if (!defined('CCPA_ROOT')) {
    define('CCPA_ROOT', dirname(__DIR__));
}

$CCPA_CONFIG = [
    // ---- Site identity -------------------------------------------------
    'site_url'        => 'https://corpuschristipublicadjuster.com', // no trailing slash
    'site_name'       => 'Corpus Christi Public Adjuster',
    'company'         => 'Rise Public Adjusting LLC',
    'license'         => '3356839',            // Texas Department of Insurance license number
    'phone_display'   => '+1 (832) 503-5866',
    'phone_short'     => '(832) 503-5866',
    'phone_e164'      => '+18325035866',
    'public_email'    => 'info@corpuschristipublicadjuster.com',
    'author_name'     => 'Joseph Dittman',
    'author_title'    => 'Licensed Public Adjuster',
    'author_email'    => 'jditt@risepublicadjusting.com',   // shown for direct contact with Joseph
    'service_area'    => 'Corpus Christi, Nueces County, and surrounding Coastal Bend communities',
    'lat'             => 27.8006,
    'lon'             => -97.3964,
    'timezone'        => 'America/Chicago',

    // ---- Free Claim Review form ---------------------------------------
    // Every form submission is emailed here.
    'mail_to'         => 'info@corpuschristipublicadjuster.com',
    'mail_from'       => 'info@corpuschristipublicadjuster.com',   // must be a mailbox on your SMTP account
    'mail_from_name'  => 'Corpus Christi Public Adjuster Website',
    'smtp_host'       => 'smtp.hostinger.com',
    'smtp_port'       => 465,
    'smtp_secure'     => 'ssl',            // 'ssl' for 465, 'tls' for 587
    'smtp_user'       => 'info@corpuschristipublicadjuster.com',
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
    'nws_user_agent'  => 'CorpusChristiPublicAdjuster.com weather page (info@corpuschristipublicadjuster.com)',
    'nws_station'     => 'KCRP',       // Corpus Christi International Airport
    'county_name'     => 'Nueces',      // primary county (stats, headlines)
    // Counties included in storm history, storm reports and the lookup tool.
    'event_counties'  => ['Nueces', 'San Patricio', 'Aransas', 'Kleberg'],
    'county_fips'     => '355',
    'state_abbr'      => 'TX',
    'state_name'      => 'TEXAS',
    'nws_office'      => 'CRP',        // NWS Corpus Christi
    'cache_ttl_current'  => 600,       // 10 minutes
    'cache_ttl_forecast' => 1800,      // 30 minutes
    'cache_ttl_alerts'   => 300,       // 5 minutes
    'http_timeout'       => 8,

    // Secret for running cron scripts over HTTP (CLI does not need it).
    'cron_key'        => '',

    'analytics_id'    => '',           // e.g. G-XXXXXXX; empty = no analytics loaded
];

foreach ([dirname(CCPA_ROOT) . '/ccpa-config.php', __DIR__ . '/config.local.php'] as $override) {
    if (is_file($override)) {
        $local = require $override;
        if (is_array($local)) {
            $CCPA_CONFIG = array_replace($CCPA_CONFIG, $local);
        }
        break;
    }
}

date_default_timezone_set($CCPA_CONFIG['timezone']);

function cfg(string $key, $default = null)
{
    global $CCPA_CONFIG;
    return $CCPA_CONFIG[$key] ?? $default;
}
