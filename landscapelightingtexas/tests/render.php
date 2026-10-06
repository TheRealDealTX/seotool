<?php
// Render one URL from the CLI:  php tests/render.php /about-us/  [> out.html]
// Exit code 1 if the page 404s or emits PHP warnings.
$path = $argv[1] ?? '/';
$_SERVER['REQUEST_URI'] = $path;
$_SERVER['HTTP_HOST'] = 'landscapelightingtexas.com';
$_SERVER['HTTP_X_FORWARDED_PROTO'] = 'https';
$_SERVER['REQUEST_METHOD'] = 'GET';
error_reporting(E_ALL);
set_error_handler(function ($no, $str, $file, $line) {
    fwrite(STDERR, "PHP warning: $str in $file:$line\n");
    register_shutdown_function(fn() => exit(1));
    return true;
});
register_shutdown_function(function () {
    $code = http_response_code();
    if ($code && $code >= 400) { fwrite(STDERR, "HTTP $code\n"); }
});
chdir(__DIR__ . '/..');
require __DIR__ . '/../index.php';
