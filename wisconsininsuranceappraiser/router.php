<?php
// Mimics the host: real files are served directly, a directory's index.php is executed,
// everything else goes to the root index.php front controller.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = $root . $path;
if ($path !== '/' && is_file($f)) {
    if (substr($f, -4) === '.php') { $_SERVER['SCRIPT_FILENAME'] = $f; chdir(dirname($f)); include $f; return true; }
    return false;   // static file served by the built-in server
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($f . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $f . 'index.php'; include $f . 'index.php'; return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
include $root . '/index.php';
return true;
