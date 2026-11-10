<?php
// Copy to app/config.php on the server. Never commit config.php.
return [
    'db_host' => '127.0.0.1',
    'db_port' => 3306,
    'db_name' => 'u000000000_roommates',
    'db_user' => 'u000000000_roommates',
    'db_pass' => 'change-me',
    'base_url' => 'https://roommate.riseapartments.com',
    'mail_from' => 'no-reply@riseapartments.com',
    // Optional SMTP (recommended on Hostinger): smtp.hostinger.com, port 465, mailbox address + password
    'smtp_host' => '',
    'smtp_port' => 465,
    'smtp_user' => '',
    'smtp_pass' => '',
    'timezone' => 'America/Chicago',
    'debug' => false,
    // Token for setup.php (one-time install). Remove setup.php after use.
    'setup_token' => '',
];
