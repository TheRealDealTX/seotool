<?php
// Katy Roofer - form settings. This file is PHP, so its contents are never
// sent to browsers; the recipient address below is not exposed on the site.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === basename(__FILE__)) { http_response_code(404); exit; }

return [
    // Where website form submissions are delivered.
    'to'        => 'teamwriteforus.today@gmail.com',

    // Sender shown on the notification email. Must be an address on your own
    // domain (create it in hPanel > Emails if mail() deliveries go missing).
    'from'      => 'no-reply@rooferkaty.com',
    'from_name' => 'Katy Roofer Website',
    'subject'   => 'New roof inspection request - rooferkaty.com',

    // Optional SMTP (recommended on Hostinger for best deliverability).
    // Leave 'smtp_user' empty to use PHP mail() instead.
    'smtp_host' => 'smtp.hostinger.com',
    'smtp_port' => 465,              // 465 = SSL
    'smtp_user' => '',               // e.g. no-reply@rooferkaty.com
    'smtp_pass' => '',

    // Every submission is also appended here as a backup (not web-readable).
    'log_file'  => __DIR__ . '/submissions-log.php',
];
