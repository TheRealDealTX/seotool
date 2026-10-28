<?php
// php -S localhost:8000 router-dev.php  — local preview that mimics .htaccess.
$f = __DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (is_file($f) && !preg_match('#/(inc|pages)/#', $f)) return false;
require __DIR__ . '/index.php';
