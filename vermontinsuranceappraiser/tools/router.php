<?php
// Local test router that mimics the Hostinger Agency host:
// real files are served directly (a .php file is executed), a directory URL with a trailing slash runs
// that directory's index.php, and everything else goes to the root index.php front controller.
// Usage: php -S 127.0.0.1:8080 -t public tools/router.php
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $root . $path;
if ($path !== '/' && is_file($file)) {
    if (substr($file, -4) === '.php') {
        $_SERVER['SCRIPT_FILENAME'] = $file;
        chdir(dirname($file));
        include $file;
        return true;
    }
    return false; // static file, served as-is
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($file . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $file . 'index.php';
    include $file . 'index.php';
    return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
include $root . '/index.php';
return true;
