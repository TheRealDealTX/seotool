<?php defined('APP') || exit;

error_reporting(E_ALL);
date_default_timezone_set('UTC');
mb_internal_encoding('UTF-8');

define('ROOT', dirname(__DIR__));
define('APPDIR', __DIR__);

$cfgFile = APPDIR . '/config.php';
if (!is_file($cfgFile)) {
    http_response_code(503);
    header('Content-Type: text/plain');
    echo "Site is being configured. (Missing app/config.php)";
    exit;
}
$GLOBALS['CFG'] = require $cfgFile;
ini_set('display_errors', (cfg('env') === 'dev') ? '1' : '0');

require APPDIR . '/lib/db.php';
require APPDIR . '/lib/helpers.php';
require APPDIR . '/lib/geo.php';
require APPDIR . '/lib/listings.php';
require APPDIR . '/lib/directory.php';
require APPDIR . '/lib/blog.php';
require APPDIR . '/lib/mail.php';
require APPDIR . '/lib/stripe.php';
require APPDIR . '/lib/images.php';
require APPDIR . '/lib/auth.php';
require APPDIR . '/lib/layout.php';
require APPDIR . '/lib/schema.php';

set_exception_handler(function (Throwable $e) {
    error_log('[thesublet] ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    if (!headers_sent()) {
        http_response_code(500);
        header('Cache-Control: no-store');
    }
    if (cfg('env') === 'dev') {
        echo '<pre>' . htmlspecialchars((string)$e) . '</pre>';
    } else {
        echo '<!doctype html><meta charset="utf-8"><title>Something went wrong</title><body style="font-family:system-ui;padding:3rem;text-align:center"><h1>Something went wrong</h1><p>Please try again in a moment. <a href="/">Back to The Sublet</a></p>';
    }
    exit;
});

function cfg(string $key, $default = null)
{
    $c = $GLOBALS['CFG'];
    foreach (explode('.', $key) as $k) {
        if (!is_array($c) || !array_key_exists($k, $c)) return $default;
        $c = $c[$k];
    }
    return $c;
}
