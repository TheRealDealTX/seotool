<?php
// beltonbanners.com - front controller for the Hostinger H5G host.
// The platform serves existing files directly and routes "/" and every
// unknown path here. See README, "Hosting note".
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://beltonbanners.com';

// Canonical scheme and host. TLS terminates upstream, so look at the forwarded proto.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.beltonbanners.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress-only URLs -> nearest equivalent.
$redirects = [
    '#^/(feed|comments/feed|category/general/feed)/?$#' => '/blog/',
    '#^/banner-type/hand-painted-banners/?$#' => '/gallery/',
    '#^/creation/?$#' => '/gallery/',
    '#^/(post|page|creation|category)-sitemap\.xml$#' => '/sitemap.xml',
    '#^/wp-sitemap.*\.xml$#' => '/sitemap.xml',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
    '#^/\?p=\d+$#' => '/blog/',
];
foreach ($redirects as $pattern => $target) {
    if (preg_match($pattern, $path)) {
        header('Location: ' . $home . $target, true, 301);
        exit;
    }
}
// Attachment pages lived under /creation/<slug>/<attachment>/ - send them to the creation.
if (preg_match('#^/creation/([a-z0-9-]+)/[a-z0-9-]+/?$#', $path, $m) && is_dir(__DIR__ . '/creation/' . $m[1])) {
    header('Location: ' . $home . '/creation/' . $m[1] . '/', true, 301);
    exit;
}
// Old media library URLs. The originals are kept at their original paths under
// wp-content/uploads/2026/03/ (served directly by the host); WordPress's resized
// variants (name-300x200.webp) were not carried over, so map them to the original.
if (preg_match('#^/wp-content/uploads/(\d{4}/\d{2})/([A-Za-z0-9._-]+?)(?:-\d+x\d+)?\.(webp|png|jpe?g)$#', $path, $m)) {
    $file = __DIR__ . '/wp-content/uploads/' . $m[1] . '/' . $m[2] . '.' . $m[3];
    if (is_file($file)) {
        $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
        $types = ['webp' => 'image/webp', 'png' => 'image/png', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg'];
        header('Content-Type: ' . ($types[$ext] ?? 'application/octet-stream'));
        header('Cache-Control: public, max-age=31536000');
        readfile($file);
        exit;
    }
}
// Directory requested without a trailing slash -> canonical slash form.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
