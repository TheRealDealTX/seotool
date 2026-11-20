<?php
define('WCA', true);
define('APP_DIR', __DIR__);
define('ROOT_DIR', dirname(__DIR__));

$cfgFile = APP_DIR . '/config.php';
if (!is_file($cfgFile)) {
    http_response_code(503);
    exit('Site is being configured.');
}
$GLOBALS['CFG'] = require $cfgFile;

if (!empty($GLOBALS['CFG']['debug'])) {
    ini_set('display_errors', '1');
    error_reporting(E_ALL);
} else {
    ini_set('display_errors', '0');
}
date_default_timezone_set('America/New_York');

require APP_DIR . '/helpers.php';
require APP_DIR . '/db.php';
require APP_DIR . '/mailer.php';
require APP_DIR . '/stripe.php';
require APP_DIR . '/listings.php';
require APP_DIR . '/content.php';

$secure = (($_SERVER['HTTPS'] ?? '') === 'on') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https')
    || str_starts_with(cfg('site_url'), 'https://');
session_name('wca_sess');
session_set_cookie_params([
    'lifetime' => 0,
    'path'     => '/',
    'secure'   => $secure,
    'httponly' => true,
    'samesite' => 'Lax',
]);
