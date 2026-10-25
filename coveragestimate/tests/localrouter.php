<?php
// php -S router emulating a server WITHOUT .htaccess: real files are served, everything else goes to index.php.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($path !== '/' && is_file($root . $path)) { return false; }
if (is_dir($root . $path) && substr($path, -1) === '/' && is_file($root . $path . 'index.html') && empty($_SERVER['QUERY_STRING'])) { return false; }
require $root . '/index.php';
