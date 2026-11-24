<?php
// Copy to /home/<user>/domains/militaryhousingrentals.com/private/config.php
// (one level ABOVE public_html, so the web server can never serve it).
// Never commit the real file. Stripe keys are NOT here: they are entered in the
// admin panel (Settings) and stored encrypted with app_secret.
return [
    'db' => [
        'host' => '127.0.0.1',          // MySQL runs on the same server
        'port' => 3306,
        'name' => 'u401386392_mhr',      // Hostinger prefixes names with the account username
        'user' => 'u401386392_mhr',
        'pass' => 'CHANGE_ME',
    ],
    'smtp' => [
        'host' => 'smtp.hostinger.com',
        'port' => 465,                   // implicit TLS
        'user' => 'info@militaryhousingrentals.com',
        'pass' => '',                    // <- mailbox password goes here (never in git)
        'from' => 'info@militaryhousingrentals.com',
        'from_name' => 'Military Housing Rentals',
    ],
    // 64 random hex chars: php -r 'echo bin2hex(random_bytes(32));'
    // Encrypts the Stripe keys stored in the database; changing it means re-entering them.
    'app_secret' => 'CHANGE_ME_64_HEX_CHARS',
    'admin_path' => '/admin/',
    'notify_email' => 'info@militaryhousingrentals.com',
    // First admin account, created when the admins table is empty.
    // php -r 'echo password_hash("your-password", PASSWORD_DEFAULT);'
    'bootstrap_admin' => ['username' => 'admin', 'password_hash' => ''],
    // Local development only:
    // 'dev' => true,
    // 'stripe_api_base' => 'http://127.0.0.1:8099',   // mock Stripe
    // 'smtp' => ['capture_dir' => '/tmp/mhr-mail', ...] // write emails to files
];
