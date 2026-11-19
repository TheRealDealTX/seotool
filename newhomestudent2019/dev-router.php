<?php
// Mimic Hostinger: serve real files, else index.php
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = $_SERVER['DOCUMENT_ROOT'] . $p;
if ($p !== '/' && is_file($f) && !str_ends_with($f, '.php')) return false;
if (is_file($f) && str_ends_with($f,'.php') && $p !== '/index.php') { require $f; return true; }
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
