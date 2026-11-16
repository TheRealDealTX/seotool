<?php
// Local stand-in for the Hostinger H5G platform, for `php -S`: existing files are served directly,
// everything else goes through wp-content/db.php exactly as WordPress's index.php would load it.
$root = dirname(__DIR__);
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$file = realpath($root . $path);
if ($file && is_file($file) && str_starts_with($file, $root . DIRECTORY_SEPARATOR) && !str_contains($path, 'wp-content/db.php')) {
    return false; // let the built-in server serve it
}
$_SERVER['SCRIPT_NAME'] = '/index.php';
$_SERVER['HTTPS'] = 'on';
$_SERVER['HTTP_HOST'] = 'conversepublicadjuster.com';
define('ABSPATH', $root . '/');
require $root . '/wp-content/db.php';
