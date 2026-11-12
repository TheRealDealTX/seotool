<?php
// Mimics the Hostinger host: real files served directly (a .php file or a directory's index.php is executed),
// everything else goes to the root index.php front controller.
$docroot = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$f = realpath($docroot . $path);
$run = function ($file) { $_SERVER['SCRIPT_FILENAME'] = $file; chdir(dirname($file)); include $file; };
if ($f && strpos($f, realpath($docroot)) === 0) {
    if (is_file($f)) {
        if (substr($f, -4) === '.php') { $run($f); return true; }
        return false;
    }
    if (is_dir($f) && substr($path, -1) === '/' && is_file($f . '/index.php') && $path !== '/') { $run($f . '/index.php'); return true; }
}
$run(realpath($docroot . '/index.php'));
return true;
