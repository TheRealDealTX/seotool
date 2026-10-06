<?php
// Spring Landscape Lighting — front controller.
// Loaded by /index.php. The host serves real files directly and sends every other
// request to index.php (it ignores .htaccess), so all routing, redirects and 404s live here.
if (!defined('SLT')) define('SLT', 1);
define('PUB', dirname(__DIR__));
define('APP', __DIR__);
require APP . '/config.php';
require APP . '/icons.php';
require APP . '/helpers.php';
require APP . '/layout.php';
require APP . '/routes.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';

// Canonical scheme + host (TLS terminates upstream, so trust X-Forwarded-Proto).
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.springlandscapelighting.com' || ($insecure && $host === 'springlandscapelighting.com')) {
    redirect(SITE_URL . $uri);
}

route($path, $qs);
exit;
