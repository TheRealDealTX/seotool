<?php
// Mimics the host: real files served directly, a directory's index.php executed, else root index.php.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = $root . $path;
if ($path !== '/' && is_file($f)) {
    if (substr($f, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = $f; chdir(dirname($f)); require $f; return true; }
    return false; // static file served directly
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($f . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $f . 'index.php'; chdir($f); require $f . 'index.php'; return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
