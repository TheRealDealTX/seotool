<?php
// Local router that mimics the Hostinger host for `php -S`:
//   cd public && php -S 127.0.0.1:8099 ../dev-router.php
// Real files are served directly (a directory's index.php is executed, as the host does);
// "/" and unknown paths go to the root index.php front controller. Not deployed.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if ($path !== '/' && substr($path, -1) === '/' && is_file($root . $path . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $root . $path . 'index.php';
    chdir($root . $path);
    require $root . $path . 'index.php';
    return true;
}
if ($path !== '/' && is_file($root . $path)) {
    if (substr($path, -4) === '.php') {
        $_SERVER['SCRIPT_FILENAME'] = realpath($root . $path);
        chdir(dirname($root . $path));
        require $root . $path;
        return true;
    }
    return false; // static file: let the built-in server send it
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
return true;
