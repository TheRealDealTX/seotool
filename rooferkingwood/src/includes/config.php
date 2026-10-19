<?php
// Kingwood Roofers - form settings. This file is PHP, so its contents are never
// sent to browsers.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === basename(__FILE__)) { http_response_code(404); exit; }

return [
    // Where website form submissions are delivered.
    'to'        => 'info@rooferkingwood.com',

    // Sender shown on the notification email. Must be an address on this
    // domain; the same mailbox works (create it in hPanel > Emails).
    'from'      => 'info@rooferkingwood.com',
    'from_name' => 'Kingwood Roofers Website',
    'subject'   => 'New roof inspection request - rooferkingwood.com',

    // Optional SMTP (recommended on Hostinger for best deliverability).
    // Leave 'smtp_user' empty to use PHP mail() instead.
    'smtp_host' => 'smtp.hostinger.com',
    'smtp_port' => 465,              // 465 = SSL
    'smtp_user' => '',               // e.g. info@rooferkingwood.com
    'smtp_pass' => '',

    // Every submission is also appended here as a backup (not web-readable).
    'log_file'  => __DIR__ . '/submissions-log.php',
];
