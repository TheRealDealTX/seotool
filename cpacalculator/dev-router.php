<?php
/* Local preview only: php -S 127.0.0.1:8099 -t . dev-router.php */
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '/' && is_file(__DIR__ . $p) && strpos($p, '/app/') !== 0) return false;
require __DIR__ . '/index.php';
