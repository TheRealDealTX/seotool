<?php
// Local dev router for `php -S` (mimics .htaccess): serve real files, else index.php
$f = realpath(__DIR__ . '/..' . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if ($f && is_file($f) && !str_ends_with($f, '.php')) return false;
require __DIR__ . '/../index.php';
