<?php
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=600');
readfile(__DIR__ . '/.page.html');
