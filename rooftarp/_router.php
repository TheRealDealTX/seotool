<?php
// Emulates the H5G platform for local testing: existing files are served
// directly; everything else goes to the front controller.
$p = strtok($_SERVER['REQUEST_URI'], '?');
$f = __DIR__ . '/' . ltrim($p, '/');
if ($p !== '/' && (is_file($f) || is_file(rtrim($f,'/') . '/index.html'))) {
    if (is_dir($f) && substr($p,-1)==='/') { readfile(rtrim($f,'/').'/index.html'); return true; }
    return false;
}
require __DIR__ . '/index.php';
