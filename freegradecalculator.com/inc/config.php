<?php
// Site-wide settings. Secrets (mailbox password) live OUTSIDE public_html in
// fgc-secrets.php — see README. Never commit the password.
define('SITE_URL', 'https://freegradecalculator.com');
define('SITE_NAME', 'Free Grade Calculator');
define('SITE_SHORT', 'FreeGradeCalculator');
define('SITE_TAGLINE', 'Every grade, GPA & study calculator in one place');
define('SITE_EMAIL', 'info@freegradecalculator.com');
define('AMAZON_TAG', 'freegradecalculator-20');
define('ASSET_VER', '20261128');
define('ROOT', dirname(__DIR__));

// SMTP (Hostinger mail). Password is read from the secrets file.
define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 465);              // SSL
define('SMTP_USER', SITE_EMAIL);
$__secret = [];
foreach ([ROOT . '/../fgc-secrets.php', ROOT . '/../../fgc-secrets.php', ROOT . '/inc/secrets.local.php'] as $__f) {
    if (is_file($__f)) { $__secret = (array) include $__f; break; }
}
define('SMTP_PASS', $__secret['smtp_pass'] ?? '');
unset($__secret, $__f);
