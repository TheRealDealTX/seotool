<?php
// Local preview only: php -S localhost:8000 -t public tools/dev-router.php
// Mimics the host: existing files are served directly, everything else goes to index.php.
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = $_SERVER['DOCUMENT_ROOT'] . $p;
if ($p !== '/' && is_file($f) && substr($f, -4) !== '.php') return false;
if (substr($p, -12) === '/contact.php') { require $_SERVER['DOCUMENT_ROOT'] . '/contact.php'; return true; }
$_SERVER['HTTP_HOST'] = 'enforceinterest.com';
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
