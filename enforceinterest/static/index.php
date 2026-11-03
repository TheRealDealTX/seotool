<?php
// enforceinterest.com - front controller for every page.
//
// The host serves existing files directly and ignores .htaccess, so the HTML pages live
// in _pages/ (blocked in robots.txt, linked from nowhere) and every page URL reaches this
// script. That lets us force https://enforceinterest.com, add trailing slashes, 301 the
// old WordPress URLs and return real 404s. Assets, icons and contact.php are served directly.
$home  = 'https://enforceinterest.com';
$uri   = $_SERVER['REQUEST_URI'] ?? '/';
$path  = rawurldecode(strtok($uri, '?'));
$qs    = (strpos($uri, '?') !== false) ? substr($uri, strpos($uri, '?')) : '';
$host  = strtolower($_SERVER['HTTP_HOST'] ?? '');
$pages = __DIR__ . '/_pages';

function send_redirect($to) {
    header('Location: ' . $to, true, 301);
    header('Cache-Control: public, max-age=86400');
    exit;
}

// Canonical scheme and host (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.enforceinterest.com' || ($insecure && $host === 'enforceinterest.com')) {
    send_redirect($home . $uri);
}

// WordPress-era URLs -> new equivalents.
$redirects = [
    '/index.php/' => '/',
    '/texas-60-day-rule/' => '/',
    '/home/' => '/',
    '/topic/general/' => '/blog/',
    '/blog/page/2/' => '/blog/',
    '/contact-us/' => '/contact/',
    '/about/' => '/about-us/',
    '/calculator/' => '/statutory-damages-calculator/',
    '/interest-calculator/' => '/statutory-damages-calculator/',
    '/statutory-interest-calculator/' => '/statutory-damages-calculator/',
    '/appraisal/' => '/post-appraisal-interest-recovery/',
    '/supplements/' => '/long-term-claim-supplements/',
    '/the-60-day-rule/' => '/texas-prompt-payment-act/',
    '/60-day-rule/' => '/texas-prompt-payment-act/',
    '/blog/18-standard-rate-explained/18-standard-rate-explained/' => '/blog/18-standard-rate-explained/',
    '/blog/act-of-god-floating-rate/act-of-god-floating-rate/' => '/blog/act-of-god-floating-rate/',
    '/enforce-interest-logo/' => '/',
    '/enforce-interest-site-image/' => '/',
    '/enforce-interest-site-icon/' => '/',
    '/enforce-interest-site-icon/cropped-enforce-interest-site-icon-webp/' => '/',
    '/privacy/' => '/privacy-policy/',
    '/terms/' => '/terms-of-use/',
    '/comments/feed/' => '/feed/',
    '/blog/feed/' => '/feed/',
];
$key = rtrim($path, '/') . '/';
if (isset($redirects[$key])) {
    send_redirect($home . $redirects[$key]);
}
// Old Yoast sitemaps.
if (preg_match('#^/(sitemap_index|page-sitemap|post-sitemap|category-sitemap|wp-sitemap)\.xml$#', $path)) {
    send_redirect($home . '/sitemap.xml');
}
// Old media library URLs that search engines or other sites may have indexed.
$media = [
    '18-Standard-Rate-Explained' => '/assets/img/18-standard-rate-explained.webp',
    'Act-of-God-Floating-Rate' => '/assets/img/act-of-god-floating-rate.webp',
    'Enforce-Interest-Logo' => '/assets/img/enforce-interest-logo.png',
    'Enforce-Interest-Site-Image' => '/assets/img/og-default.jpg',
    'Enforce-Interest-Site-Icon' => '/web-app-manifest-512x512.png',
    'cropped-Enforce-Interest-Site-Icon' => '/web-app-manifest-512x512.png',
];
if (preg_match('#^/wp-content/uploads/\d{4}/\d{2}/([A-Za-z0-9-]+?)(-\d+x\d+)?\.(webp|png|jpe?g)$#', $path, $m)) {
    send_redirect($home . ($media[$m[1]] ?? '/'));
}
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php|wp-cron\.php)(/|$)#', $path)) {
    send_redirect($home . '/');
}
if (preg_match('#^/(page|author|tag|category|topic)/#', $path) || preg_match('#^/[^/]+/(feed|amp|embed)/?$#', $path)) {
    send_redirect($home . '/blog/');
}
if ($key === '/' && isset($_GET['p'])) {
    send_redirect($home . '/');
}

function serve($file, $type) {
    $mtime = filemtime($file);
    $etag  = '"' . md5($mtime . filesize($file)) . '"';
    header('Content-Type: ' . $type);
    header('Cache-Control: public, max-age=600');
    header('Last-Modified: ' . gmdate('D, d M Y H:i:s', $mtime) . ' GMT');
    header('ETag: ' . $etag);
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    if (($_SERVER['HTTP_IF_NONE_MATCH'] ?? '') === $etag) {
        http_response_code(304);
        exit;
    }
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'HEAD') {
        readfile($file);
    }
    exit;
}

if ($key === '/feed/' && is_file($pages . '/feed.xml')) {
    if (substr($path, -1) !== '/') send_redirect($home . '/feed/');
    serve($pages . '/feed.xml', 'application/rss+xml; charset=utf-8');
}

// Only plain slug paths map to pages; anything with dots or traversal is a 404.
if (preg_match('#^/([a-z0-9-]+/)*$#', $key)) {
    $file = $pages . ($key === '/' ? '/index.html' : $key . 'index.html');
    if (is_file($file)) {
        if (substr($path, -1) !== '/') send_redirect($home . $key . $qs);
        serve($file, 'text/html; charset=utf-8');
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache');
header('X-Robots-Tag: noindex');
readfile(is_file($pages . '/404.html') ? $pages . '/404.html' : __DIR__ . '/404.html');
