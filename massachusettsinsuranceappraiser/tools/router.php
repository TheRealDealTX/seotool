<?php
// Local test router: mimic the host (serve real files directly, everything else to index.php).
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = $_SERVER['DOCUMENT_ROOT'] . $p;
if ($p !== '/' && is_file($f) && substr($f, -4) !== '.php') return false;
if ($p !== '/' && is_file($f)) { require $f; return true; }
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
