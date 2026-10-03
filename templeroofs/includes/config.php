<?php
/**
 * Temple Roofers — public site configuration.
 *
 * Edit business details here. Nothing in this file is secret: the private
 * mail settings (lead recipient + SMTP) live in a separate private config —
 * see README.txt, "Configure email delivery".
 */
defined('TR_ROOT') || exit;

return [
    'site_name'     => 'Temple Roofers',
    'base_url'      => 'https://templeroofs.com',   // no trailing slash
    'phone_display' => '(512) 297-7580',
    'phone_intl'    => '+1 (512) 297-7580',
    'phone_e164'    => '+15122977580',
    'city'          => 'Temple',
    'region'        => 'TX',
    'county'        => 'Bell County',
    'timezone'      => 'America/Chicago',

    // Temple, TX city centre — used for weather + structured data.
    'lat' => 31.0982,
    'lng' => -97.3428,

    // NWS county code for Bell County, TX (used for active weather alerts).
    'nws_county_zone' => 'TXC027',

    // Blog scheduling: article #1 goes live on this date (America/Chicago),
    // each following article goes live every N days after it.
    'blog_launch_date'    => '2026-10-03',
    'blog_interval_days'  => 3,

    // Weather cache lifetimes (seconds) and the oldest cached data we will
    // ever show (clearly labelled as cached) when the live service is down.
    'weather_ttl'         => 600,
    'alerts_ttl'          => 300,
    'weather_max_stale'   => 21600,

    // Lead form: max submissions per visitor (hashed IP) per window.
    'rate_limit_max'      => 5,
    'rate_limit_window'   => 900,
];
