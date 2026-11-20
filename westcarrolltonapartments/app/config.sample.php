<?php defined('WCA') || exit;
// Copy to app/config.php on the server and fill in. app/config.php is git-ignored.
return [
    'site_url'   => 'https://westcarrolltonapartments.com',
    'site_name'  => 'West Carrollton Apartments',
    'debug'      => false,

    'db' => [
        'host' => 'localhost',
        'name' => 'wcadir',
        'user' => 'wcadir',
        'pass' => 'CHANGE_ME',
    ],

    // Admin login (/admin/). Generate the hash with: php -r "echo password_hash('your-password', PASSWORD_DEFAULT);"
    'admin_user'          => 'admin',
    'admin_password_hash' => '',

    // Outgoing mail (Hostinger mailbox)
    'smtp' => [
        'host'      => 'smtp.hostinger.com',
        'port'      => 465,          // SSL
        'user'      => 'info@westcarrolltonapartments.com',
        'pass'      => 'CHANGE_ME',
        'from'      => 'info@westcarrolltonapartments.com',
        'from_name' => 'West Carrollton Apartments',
    ],
    'admin_email' => 'info@westcarrolltonapartments.com',

    // Stripe (these can also be set from /admin/settings/, which override these values)
    'stripe_secret_key'     => '',
    'stripe_webhook_secret' => '',
    'listing_price_cents'   => 1000,

    'amazon_tag' => 'riseapartments-20',

    // Random string used to sign tokens
    'app_key' => 'CHANGE_ME_TO_A_LONG_RANDOM_STRING',
];
