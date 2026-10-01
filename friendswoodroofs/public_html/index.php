<?php
/*
 * Friendswood Roofers - front controller.
 *
 * Locates the private "app" folder. Recommended: upload it NEXT TO
 * public_html (outside the web root). Fallback: public_html/app, which is
 * blocked from web access by public_html/app/.htaccess.
 */
define('FR_PUBLIC', __DIR__);

$candidates = [
    getenv('FR_APP_DIR') ?: null,
    dirname(__DIR__) . '/app',
    __DIR__ . '/app',
];
foreach ($candidates as $dir) {
    if ($dir && is_file($dir . '/bootstrap.php')) {
        define('FR_APP', realpath($dir));
        break;
    }
}
if (!defined('FR_APP')) {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    exit("Site configuration error: the 'app' folder was not found. See README.md (Deployment).");
}

require FR_APP . '/bootstrap.php';
