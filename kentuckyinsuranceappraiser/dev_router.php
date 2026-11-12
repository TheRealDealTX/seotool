<?php
// Mimics the Hostinger host: real files are served directly (a directory's index.php is executed),
// everything else goes to the root index.php front controller.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = $root . $path;
if ($path !== '/' && is_file($f)) {
    if (substr($f, -4) === '.php') { chdir(dirname($f)); $_SERVER['SCRIPT_FILENAME'] = $f; require $f; return true; }
    return false;
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($f . 'index.php')) { $_SERVER['SCRIPT_FILENAME'] = $f . 'index.php'; require $f . 'index.php'; return true; }
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
