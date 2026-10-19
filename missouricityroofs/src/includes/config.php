<?php
// Missouri City Roofers - form settings. This file is PHP, so its contents are
// never sent to browsers.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === basename(__FILE__)) { http_response_code(404); exit; }

return [
    // Where website form submissions are delivered.
    'to'        => 'info@missouricityroofs.com',

    // Sender shown on the notification email. Must be a mailbox on this domain
    // (create it in hPanel > Emails). Using the same mailbox keeps setup to one.
    'from'      => 'info@missouricityroofs.com',
    'from_name' => 'Missouri City Roofers Website',
    'subject'   => 'New roof inspection request - missouricityroofs.com',

    // Optional SMTP (recommended on Hostinger for best deliverability).
    // Leave 'smtp_user' empty to use PHP mail() instead.
    'smtp_host' => 'smtp.hostinger.com',
    'smtp_port' => 465,              // 465 = SSL
    'smtp_user' => '',               // e.g. info@missouricityroofs.com
    'smtp_pass' => '',

    // Every submission is also appended here as a backup (not web-readable).
    'log_file'  => __DIR__ . '/submissions-log.php',
];
