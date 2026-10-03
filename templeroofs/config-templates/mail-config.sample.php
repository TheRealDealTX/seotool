<?php
/**
 * Temple Roofers — PRIVATE mail configuration (template).
 *
 * Copy this file to ONE of these locations and fill it in:
 *   1. RECOMMENDED: one level ABOVE public_html, e.g.
 *        /home/uXXXXXXXX/domains/templeroofs.com/templeroofs-private/mail-config.php
 *      (public_html and templeroofs-private sit side by side)
 *   2. Or: public_html/includes/private/mail-config.php  (blocked from the web by .htaccess)
 *
 * This file is never sent to browsers. Do not paste these values into any
 * page, script or stylesheet.
 */
return [
    // Where website leads are delivered.
    'recipient'  => 'you@example.com',

    // "From" address. With SMTP this should be the mailbox you log in with.
    // Must be an address on your own domain for reliable delivery.
    'from_email' => 'no-reply@templeroofs.com',
    'from_name'  => 'Temple Roofers Website',

    // Authenticated SMTP (recommended). Leave username/password empty to
    // fall back to PHP mail(), which Hostinger supports but which is more
    // likely to land in spam.
    'smtp' => [
        'host'     => 'smtp.hostinger.com',
        'port'     => 465,          // 465 = SSL, 587 = TLS
        'secure'   => 'ssl',        // 'ssl' or 'tls'
        'username' => '',           // e.g. no-reply@templeroofs.com
        'password' => '',           // that mailbox's password
    ],

    // Optional: a long random string used to sign form tokens. Leave empty
    // and the site will generate one automatically in /storage.
    'app_secret' => '',
];
