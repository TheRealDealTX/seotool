<?php
// Local preview: php -S localhost:8080 -t public tools/dev-router.php
$f = $_SERVER['DOCUMENT_ROOT'] . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($_SERVER['REQUEST_URI'] !== '/' && is_file($f) && !str_ends_with($f, '.php')) return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
