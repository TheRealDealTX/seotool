<?php
// my1secret.com configuration. On Hostinger this lives OUTSIDE the web root at
//   /home/<user>/websites/<uid>/.h5g/my1secret-config.php
// Never commit the real file.
return [
    'base_url'       => 'https://my1secret.com',      // canonical origin, no trailing slash
    'db'             => [
        'dsn'  => 'mysql:host=localhost;dbname=DBNAME;charset=utf8mb4',
        'user' => 'DBUSER',
        'pass' => 'DBPASS',
    ],
    'secret'         => 'long-random-string',         // signs anti-bot form fields
    'install_token'  => '',                           // set to run /install/?token=..., then clear it
    'admin_email'    => null,                         // email for the my1secret admin account (password resets)
    'contact_email'  => null,                         // shown on /contact/ when set
    'mail_from'      => 'no-reply@my1secret.com',
    'allow_indexing' => true,                         // false = noindex everything (staging)
    'enforce_host'   => true,                         // 301 www/http to base_url
    'debug'          => false,
];
