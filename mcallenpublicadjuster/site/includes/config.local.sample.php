<?php
/**
 * Private configuration override.
 *
 * 1. Copy this file to  ../mpa-config.php  (the folder ABOVE public_html; best)
 *    or to  includes/config.local.php  (blocked from the web by .htaccess).
 * 2. Fill in the values below. Only keys you set here override includes/config.php.
 */
return [
    // Hostinger email account used to send the Free Claim Review notifications.
    'smtp_host'   => 'smtp.hostinger.com',
    'smtp_port'   => 465,
    'smtp_secure' => 'ssl',
    'smtp_user'   => 'info@mcallenpublicadjuster.com',
    'smtp_pass'   => 'PUT-THE-MAILBOX-PASSWORD-HERE',
    'mail_from'   => 'info@mcallenpublicadjuster.com',

    // Long random string; only needed if you trigger cron scripts by URL.
    'cron_key'    => 'CHANGE-ME-to-a-long-random-string',
];
