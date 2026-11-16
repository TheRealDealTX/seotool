<?php
// Local preview only: php -S 127.0.0.1:8000 -t public src/dev_router.php
// Mimics the host: existing files are served as-is, everything else goes to index.php.
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '/' && is_file($_SERVER['DOCUMENT_ROOT'] . $p)) { return false; }
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
