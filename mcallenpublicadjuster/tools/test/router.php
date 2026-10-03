<?php
// Local dev router for `php -S` that mimics the .htaccess rules
// (static files, blocked private folders, front controller).
$root = dirname(__DIR__, 2) . '/site';
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (preg_match('#^/(includes|templates|content|data|cron|tools)(/|$)#', $path) || preg_match('#(^|/)\.#', $path)) {
    http_response_code(403);
    echo 'Forbidden';
    return true;
}
$file = $root . $path;
if ($path !== '/' && is_file($file)) {
    if (substr($file, -4) === '.php') {
        chdir(dirname($file));
        require $file;
        return true;
    }
    return false; // built-in server sends static files
}
chdir($root);
require $root . '/index.php';
