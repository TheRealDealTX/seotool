<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/**
 * SMTP settings for the estimate form. COPY this file to mail.php in the same
 * folder and fill in the real values. mail.php is never committed to git and
 * should sit outside public_html (see README "Where the app folder goes").
 *
 * Alternatively, set the environment variable FR_MAIL_CONFIG to the absolute
 * path of a PHP file that returns this same array.
 */
return [
    // Where estimate requests are delivered. Never shown on the website.
    'recipient' => 'teamwriteforus.today@gmail.com',

    // Authenticated SMTP. Hostinger mailbox defaults shown.
    'host'       => 'smtp.hostinger.com',
    'port'       => 465,
    'encryption' => 'ssl',            // 'ssl' for 465 (SMTPS) or 'tls' for 587 (STARTTLS)
    'username'   => 'estimates@friendswoodroofs.com',
    'password'   => 'CHANGE-ME',

    // Sender must be a mailbox on friendswoodroofs.com so SPF/DKIM/DMARC align.
    // The visitor's email (if given) is only ever used as Reply-To.
    'from_email' => 'estimates@friendswoodroofs.com',
    'from_name'  => 'Friendswood Roofers Website',

    'timeout'    => 15,               // seconds
];
