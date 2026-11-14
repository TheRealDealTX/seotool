<?php
// Mimics the Hostinger setup: real files served directly, a directory's index.php executed,
// everything else (/ and unknown paths) goes to the root index.php.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$full = $root . $path;
if ($path !== '/' && is_dir($full) && substr($path, -1) === '/' && is_file($full . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $full . 'index.php';
    chdir($full); require $full . 'index.php'; return true;
}
if ($path !== '/' && is_file($full)) {
    if (substr($full, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = realpath($full); chdir(dirname($full)); require $full; return true; }
    return false;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
