<?php
// Local preview only: mimics the host (serve real files, else index.php).
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '/' && is_file(__DIR__ . '/public_html' . $p)) return false;
require __DIR__ . '/public_html/index.php';
