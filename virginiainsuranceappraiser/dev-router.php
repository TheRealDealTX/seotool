<?php
// Local stand-in for the Hostinger php-fpm host:  php -S 127.0.0.1:8080 -t public dev-router.php
// Real files are served directly (.php files are executed), a directory's index.php is executed,
// and everything else goes to the root index.php front controller. Mirrors the production behaviour.
$root = __DIR__ . '/public';
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = realpath($root . $path);
if ($file !== false && strpos($file, $root) === 0) {
    if (is_dir($file) && is_file($file . '/index.php') && substr($path, -1) === '/') {
        $_SERVER['SCRIPT_FILENAME'] = $file . '/index.php';
        chdir($file);
        require $file . '/index.php';
        return true;
    }
    if (is_file($file)) {
        if (substr($file, -4) === '.php') {
            $_SERVER['SCRIPT_FILENAME'] = $file;
            chdir(dirname($file));
            require $file;
            return true;
        }
        return false; // static file
    }
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
chdir($root);
require $root . '/index.php';
return true;
