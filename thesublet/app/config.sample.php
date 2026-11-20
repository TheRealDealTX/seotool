<?php defined('APP') || exit;
// Copy to app/config.php ON THE SERVER ONLY (never commit it).
return [
    'env'       => 'production',            // 'production' or 'dev'
    'base_url'  => 'https://thesublet.com',  // no trailing slash
    'canonical_host' => 'thesublet.com',     // requests to other hosts (www.) are 301'd here; '' disables
    'app_secret'=> 'CHANGE-ME-64-random-hex-chars', // signs renew/upgrade links

    // Database. Hostinger Agency: name/user are prefixed u914589053_<websiteUID>_<name>
    'db' => [
        'driver' => 'mysql',                // 'mysql' or 'sqlite'
        'host'   => 'localhost',
        'name'   => 'u914589053_XXXX_sublet',
        'user'   => 'u914589053_XXXX_sublet',
        'pass'   => '',
        'path'   => '',                     // sqlite only: absolute file path
    ],

    // Outgoing mail via the info@thesublet.com mailbox
    'smtp' => [
        'host' => 'smtp.hostinger.com',
        'port' => 465,                      // implicit TLS
        'user' => 'info@thesublet.com',
        'pass' => '',
        'from' => 'info@thesublet.com',
        'from_name' => 'The Sublet',
    ],
    'admin_notify' => 'info@thesublet.com', // new submissions / reports go here

    // Admin panel login (/admin/). Hash with: php -r "echo password_hash('pw', PASSWORD_DEFAULT);"
    'admin_user'      => 'admin',
    'admin_pass_hash' => '',

    // Stripe can also be set in Admin → Settings (DB values win over these)
    'stripe_publishable' => '',
    'stripe_secret'      => '',
    'stripe_webhook_secret' => '',

    'cron_key' => 'CHANGE-ME-random', // GET /cron/run?key=... runs expiry jobs
];
