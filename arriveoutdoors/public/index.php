<?php
// Static site: serve the homepage; anything else routed here is a 404.
$p = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
if ($p === '/' || $p === '/index.php') { header('Content-Type: text/html; charset=utf-8'); readfile(__DIR__ . '/index.html'); exit; }
http_response_code(404); header('Content-Type: text/html; charset=utf-8'); readfile(__DIR__ . '/404.html');
