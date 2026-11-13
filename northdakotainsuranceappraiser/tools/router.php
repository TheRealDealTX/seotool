<?php
// Local test router that mimics the Hostinger Agency host:
//   - real files are served directly (a .php file is executed),
//   - a directory URL with an index.php runs that index.php,
//   - everything else goes to the root index.php front controller.
// Usage: cd public && php -S 127.0.0.1:8080 ../tools/router.php
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$file = realpath($root . $path);
if ($file !== false && strpos($file, realpath($root)) === 0) {
    if (is_file($file)) {
        if (substr($file, -4) === '.php') {
            $_SERVER['SCRIPT_FILENAME'] = $file;
            chdir(dirname($file));
            require $file;
            return true;
        }
        return false; // static file: let the built-in server send it
    }
    if (is_dir($file) && substr($path, -1) === '/' && is_file($file . '/index.php')) {
        $_SERVER['SCRIPT_FILENAME'] = $file . '/index.php';
        chdir($file);
        require $file . '/index.php';
        return true;
    }
}
$_SERVER['SCRIPT_FILENAME'] = $root . '/index.php';
require $root . '/index.php';
return true;
