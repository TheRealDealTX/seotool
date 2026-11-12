<?php
// Local router for `php -S` that mimics the Hostinger Agency host:
// real files are served directly (a .php file is executed), a directory URL runs that
// directory's index.php, and "/" or anything unknown goes to the root index.php front controller.
//   cd public && php -S 127.0.0.1:8099 ../tools/router.php
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = realpath($root . $path);
if ($file !== false && strpos($file, realpath($root)) === 0) {
    if (is_dir($file) && $path !== '/' && is_file($file . '/index.php') && substr($path, -1) === '/') {
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
        return false; // static file: let the built-in server send it
    }
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
return true;
