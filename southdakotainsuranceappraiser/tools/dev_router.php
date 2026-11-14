<?php
// Local stand-in for the Hostinger host: php -S 127.0.0.1:8080 -t public tools/dev_router.php
// Real files are served directly (a .php file is executed), a directory URL runs its index.php,
// and "/" or unknown paths fall through to the root index.php front controller. .htaccess is ignored.
$root = realpath(__DIR__ . '/../public');
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $root . $path;
$run = function ($f) { $_SERVER['SCRIPT_FILENAME'] = $f; $_SERVER['SCRIPT_NAME'] = substr($f, strlen(realpath(__DIR__ . '/../public'))); chdir(dirname($f)); require $f; };
if ($path !== '/' && is_file($file)) {
    if (substr($file, -4) === '.php') { $run($file); return true; }
    return false; // static file
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($file . 'index.php')) { $run($file . 'index.php'); return true; }
$run($root . '/index.php');
return true;
