<?php
// huttoroofs.com is a static site. This file only exists because the
// hosting platform keeps index.php and prefers it; it serves index.html.
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/index.html');
