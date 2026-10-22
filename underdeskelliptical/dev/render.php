<?php
// CLI renderer for local checks: php dev/render.php /some-path/  -> prints status + HTML.
// Example: php dev/render.php /flex-fitness-under-desk-elliptical/ > /tmp/out.html
$path = $argv[1] ?? '/';
$_SERVER['REQUEST_URI'] = $path;
$_SERVER['HTTP_HOST'] = 'underdeskelliptical.com';
$_SERVER['HTTP_X_FORWARDED_PROTO'] = 'https';
parse_str((string) parse_url($path, PHP_URL_QUERY), $_GET);
register_shutdown_function(function () {
    fwrite(STDERR, 'STATUS ' . (http_response_code() ?: 200) . "\n");
});
require __DIR__ . '/../index.php';
