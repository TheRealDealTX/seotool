<?php
declare(strict_types=1);

/*
 * Application bootstrap. Called from public_html/index.php after it has
 * defined FR_APP (this folder) and FR_PUBLIC (the web root).
 */

if (PHP_VERSION_ID < 80100) {
    http_response_code(500);
    exit('Friendswood Roofers requires PHP 8.1 or newer. Select it in hPanel > Advanced > PHP Configuration.');
}

ini_set('display_errors', '0');
ini_set('log_errors', '1');
if (is_dir(FR_APP . '/storage/logs') && is_writable(FR_APP . '/storage/logs')) {
    ini_set('error_log', FR_APP . '/storage/logs/php-error.log');
}
error_reporting(E_ALL);

$GLOBALS['FR_CONFIG'] = require FR_APP . '/config/site.php';
date_default_timezone_set((string) ($GLOBALS['FR_CONFIG']['timezone'] ?? 'America/Chicago'));

require FR_APP . '/vendor/autoload.php';
require FR_APP . '/src/helpers.php';
require FR_APP . '/src/content.php';
require FR_APP . '/src/seo.php';
require FR_APP . '/src/security.php';
require FR_APP . '/src/mailer.php';
require FR_APP . '/src/estimate.php';
require FR_APP . '/src/router.php';

send_security_headers();
dispatch(request_path(), $_SERVER['REQUEST_METHOD'] ?? 'GET');
