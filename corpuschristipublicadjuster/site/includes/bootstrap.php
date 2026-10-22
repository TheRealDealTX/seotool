<?php
declare(strict_types=1);
defined('CCPA_ROOT') || exit;

if (!defined('CCPA_ROOT')) {
    define('CCPA_ROOT', dirname(__DIR__));
}

// Never show PHP errors to visitors; log them privately instead.
ini_set('display_errors', '0');
ini_set('log_errors', '1');
$ccpaErrLog = CCPA_ROOT . '/data/logs/php-errors.log.php';
if (!is_file($ccpaErrLog) && is_dir(dirname($ccpaErrLog))) {
    @file_put_contents($ccpaErrLog, "<?php http_response_code(404); exit; ?>\n");
}
ini_set('error_log', $ccpaErrLog);
error_reporting(E_ALL);

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/seo.php';
require_once __DIR__ . '/form.php';
require_once __DIR__ . '/render.php';

function send_security_headers(): void
{
    if (headers_sent()) {
        return;
    }
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('Permissions-Policy: geolocation=(), camera=(), microphone=()');
}
send_security_headers();
