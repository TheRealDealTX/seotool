<?php
/**
 * TX Public Adjusting: front controller. Every request that isn't a real
 * file (see .htaccess) lands here and is routed by app/router.php.
 */
declare(strict_types=1);

define('SITE_ROOT', __DIR__);

// PHP's built-in server (local preview): serve real files directly.
if (PHP_SAPI === 'cli-server') {
    $file = __DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    if (is_file($file) && !preg_match('#^' . preg_quote(__DIR__, '#') . '/(app|content|storage)/#', $file) && substr($file, -4) !== '.php') {
        return false;
    }
}

require __DIR__ . '/app/config.php';
require __DIR__ . '/app/lib.php';
require __DIR__ . '/app/icons.php';
require __DIR__ . '/app/schema.php';
require __DIR__ . '/app/views.php';
require __DIR__ . '/app/pages.php';
require __DIR__ . '/app/router.php';

header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('X-Frame-Options: SAMEORIGIN');

route();
