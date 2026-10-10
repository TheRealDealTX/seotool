<?php
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '/' && is_file($_SERVER['DOCUMENT_ROOT'] . $p)) return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
