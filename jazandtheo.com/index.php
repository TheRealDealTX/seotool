<?php
// jazandtheo.com - front controller for the Hostinger plain-PHP host.
// The platform serves existing files directly and routes "/" and every
// unknown path here. See README, "Hosting note".
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? 'jazandtheo.com');

// Canonical scheme and host. TLS terminates upstream, so look at the forwarded proto.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.jazandtheo.com') {
    $host = 'jazandtheo.com';
    $insecure = true;
}
$home = 'https://' . $host;
if ($insecure) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep the temporary hosting domain out of search results.
if ($host !== 'jazandtheo.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php') {
    if (isset($_GET['p']) || isset($_GET['page_id'])) {
        header('Location: ' . $home . '/', true, 301);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$go = static function (string $to) use ($home): void {
    header('Location: ' . $home . $to, true, 301);
    exit;
};

// Old WordPress URLs -> nearest equivalent.
$redirects = [
    '#^/(feed|comments/feed|rss|atom)/?$#' => '/blog/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
    '#^/(post|page|category|post_tag|author)-sitemap\d*\.xml$#' => '/sitemap.xml',
    '#^/(wp-sitemap.*|sitemap_index)\.xml$#' => '/sitemap.xml',
    '#^/author(/.*)?$#' => '/about/',
    '#^/(contact-us|contact-me)/?$#' => '/contact/',
    '#^/(about-us|about-jaz-and-theo)/?$#' => '/about/',
    '#^/(engagements?|seniors?|families|family)/?$#' => '/portraits/',
    '#^/(home|design|business)/?$#' => '/lifestyle/',
    '#^/(store|products?)/?$#' => '/shop/',
];
foreach ($redirects as $pattern => $target) {
    if (preg_match($pattern, $path)) {
        $go($target);
    }
}
// /page/2/ -> /blog/page/2/ ; date archives -> journal.
if (preg_match('#^/page/(\d+)/?$#', $path, $m)) {
    $go(is_dir(__DIR__ . '/blog/page/' . $m[1]) ? '/blog/page/' . $m[1] . '/' : '/blog/');
}
if (preg_match('#^/blog/page/\d+/?$#', $path) || preg_match('#^/\d{4}(/\d{2}(/\d{2})?)?(/page/\d+)?/?$#', $path)) {
    $go('/blog/');
}
// Paged or feed variants of a category/tag/post -> the base page.
if (preg_match('#^/((?:category|tag)/[a-z0-9-]+)/(?:page/\d+|feed)/?$#', $path, $m)) {
    $go(is_dir(__DIR__ . '/' . $m[1]) ? '/' . $m[1] . '/' : '/blog/');
}
if (preg_match('#^/(?:category|tag)/[a-z0-9-]+/?$#', $path) && !is_dir(__DIR__ . rtrim($path, '/'))) {
    $go('/blog/');
}
// Post sub-paths (attachment pages, feeds, amp, comment pages) -> the post.
if (preg_match('#^/(\d{4}/\d{2}/[a-z0-9-]+)/.+$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) {
    $go('/' . $m[1] . '/');
}
// Old media library: resized variants (name-300x200.jpg) -> the original if we have it.
if (preg_match('#^/wp-content/uploads/(\d{4}/\d{2})/([A-Za-z0-9._-]+?)(?:-\d+x\d+|-scaled)?\.(jpe?g|png|webp)$#i', $path, $m)) {
    $file = __DIR__ . '/wp-content/uploads/' . $m[1] . '/' . $m[2] . '.' . $m[3];
    if (is_file($file)) {
        $types = ['webp' => 'image/webp', 'png' => 'image/png', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg'];
        header('Content-Type: ' . ($types[strtolower($m[3])] ?? 'application/octet-stream'));
        header('Cache-Control: public, max-age=31536000');
        readfile($file);
        exit;
    }
}
// Directory requested without a trailing slash -> canonical slash form.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    $go($path . '/');
}
// Trailing-slash-less old post URLs.
if (preg_match('#^/\d{4}/\d{2}/[a-z0-9-]+$#', $path) && is_dir(__DIR__ . $path)) {
    $go($path . '/');
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
