<?php
// Local preview that mimics Hostinger: existing files are served as-is, everything else goes to index.php.
$p = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if ($p !== '/' && file_exists(__DIR__ . '/public' . $p)) return false;  // dirs too, like nginx
chdir(__DIR__ . '/public');
require __DIR__ . '/public/index.php';
