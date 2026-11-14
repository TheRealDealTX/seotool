<?php
// Local router that mimics the Hostinger host:  php -S 127.0.0.1:8080 -t public tools/dev_router.php
// - real files are served directly (a .php file is executed), so the front controller doesn't run for them
// - a directory URL with an index.php executes that file
// - "/" and everything else goes to the root index.php front controller
$docroot = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $docroot . $path;
if ($path !== '/' && is_file($file)) {
    return false;
}
if ($path !== '/' && substr($path, -1) === '/' && is_file($file . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $file . 'index.php';
    chdir($file);
    require $file . 'index.php';
    return true;
}
$_SERVER['SCRIPT_FILENAME'] = $docroot . '/index.php';
require $docroot . '/index.php';
