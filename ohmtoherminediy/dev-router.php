<?php
// Local preview only: `php -S 127.0.0.1:8098 -t public dev-router.php`
// Emulates the host: existing files are served directly, everything else goes to index.php.
$root = $_SERVER['DOCUMENT_ROOT']; $p = strtok($_SERVER['REQUEST_URI'], '?');
if ($p !== '/' && (is_file($root . $p) || (substr($p, -1) === '/' && is_file($root . $p . 'index.html')))) {
    if (substr($p, -4) === '.php') { require $root . $p; return true; }
    return false;
}
require $root . '/index.php';
