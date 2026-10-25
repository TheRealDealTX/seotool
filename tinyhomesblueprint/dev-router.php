<?php
$f = $_SERVER['DOCUMENT_ROOT'] . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (is_file($f) && basename($f) !== 'index.php') return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
