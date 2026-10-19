<?php
// Local dev router mimicking the host: existing files are served directly, everything else hits index.php.
$f = $_SERVER['DOCUMENT_ROOT'] . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (is_file($f)) return false;
if (is_dir($f) && is_file(rtrim($f, '/') . '/index.html') && str_ends_with($f, '/')) return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
