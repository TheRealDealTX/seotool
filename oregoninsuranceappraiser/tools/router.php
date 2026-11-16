<?php
// Local test router that mimics the Hostinger Agency host:
//   real files are served directly (.php files executed), a directory URL runs that directory's index.php,
//   and everything else goes to the root index.php front controller. .htaccess is ignored.
// usage: php -S 127.0.0.1:8080 -t public tools/router.php
$root = realpath(__DIR__ . '/../public');
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $root . $path;
if (is_file($file)) {
    if (substr($file, -4) === '.php') {
        $_SERVER['SCRIPT_FILENAME'] = $file;
        require $file;
        return true;
    }
    return false;
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($file . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $file . 'index.php';
    require $file . 'index.php';
    return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
return true;
