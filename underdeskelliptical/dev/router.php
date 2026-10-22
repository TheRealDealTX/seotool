<?php
// Local preview that mimics Hostinger: real files are served as-is, everything else hits index.php.
//   php -S localhost:8080 dev/router.php
$f = realpath(__DIR__ . '/..' . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if ($f && is_file($f) && !str_ends_with($f, '.php')) {
    return false;
}
$_SERVER['HTTP_X_FORWARDED_PROTO'] = 'https';
$_SERVER['HTTP_HOST'] = 'underdeskelliptical.com';
require __DIR__ . '/../index.php';
