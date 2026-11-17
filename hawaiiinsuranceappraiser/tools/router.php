<?php
// Mimics the Hostinger H5G behaviour: real files served directly (PHP files executed),
// a directory URL runs that directory's index.php, everything else goes to the root index.php.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = $root . $path;
if ($path !== '/' && is_file($f)) {
    if (substr($f, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = $f; chdir(dirname($f)); require $f; return true; }
    return false; // static file served as-is
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($f . 'index.php')) { $_SERVER['SCRIPT_FILENAME'] = $f . 'index.php'; require $f . 'index.php'; return true; }
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
