<?php
// Local dev router that mimics the Hostinger Agency host:
//   php -S 127.0.0.1:8099 -t public tools/router.php
// - real files are served directly (a .php file is executed, as the host does)
// - a directory URL runs that directory's index.php
// - everything else goes to the root index.php front controller.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = $root . $path;
if ($path !== '/' && is_file($file)) {
    if (substr($file, -4) === '.php') {
        $_SERVER['SCRIPT_FILENAME'] = $file;
        chdir(dirname($file));
        require $file;
        return true;
    }
    return false; // static file: let the built-in server send it
}
if (substr($path, -1) === '/' && $path !== '/' && is_file($file . 'index.php')) {
    $_SERVER['SCRIPT_FILENAME'] = $file . 'index.php';
    chdir($file);
    require $file . 'index.php';
    return true;
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
chdir($root);
require $root . '/index.php';
return true;
