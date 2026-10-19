<?php
// Front controller: serves the homepage and handles every request that has no file of its own
// (old WordPress URLs, sitemap.xml, robots.txt, 404s).
require __DIR__ . '/inc/config.php';

$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$path = '/' . ltrim(rawurldecode($path), '/');

// Enforce https + bare domain once the real domain is live (TLS terminates upstream).
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.' . CANONICAL_HOST) {
    $target = str_starts_with($host, 'www.') ? substr($host, 4) : $host;
    header('Location: https://' . $target . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    require __DIR__ . '/inc/home.php';
    exit;
}

// Legacy WordPress URLs -> closest new page
$redirects = [
    '/the-art-of-claim-evaluation-how-adjusters-determine-payouts/'       => BLOG_BASE . 'how-do-insurance-adjusters-get-paid/',
    '/the-role-of-an-insurance-adjuster-what-to-expect-during-the-claims-process/' => BLOG_BASE . 'claims-adjuster-salary/',
    '/author/kara/'              => BLOG_BASE,
    '/category/uncategorized/'   => BLOG_BASE,
    '/feed/'                     => BLOG_BASE,
    '/comments/feed/'            => BLOG_BASE,
    '/sitemap_index.xml'         => '/sitemap.xml',
    '/wp-sitemap.xml'            => '/sitemap.xml',
];
$key = rtrim($path, '/') . (str_contains(basename($path), '.') ? '' : '/');
if (isset($redirects[$key])) {
    header('Location: ' . $redirects[$key], true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php|wp-sitemap)#', $path)) {
    header('Location: /', true, 301);
    exit;
}

if ($path === '/sitemap.xml') {
    header('Content-Type: application/xml; charset=utf-8');
    require __DIR__ . '/inc/sitemap.php';
    exit;
}
if ($path === '/robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    if (is_temporary_host()) {
        echo "User-agent: *\nDisallow: /\n";
    } else {
        echo "User-agent: *\nAllow: /\n\nSitemap: " . base_url() . "/sitemap.xml\n";
    }
    exit;
}

// Directory requested without trailing slash
if (!str_ends_with($path, '/') && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.php')) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}

http_response_code(404);
require __DIR__ . '/inc/404.php';
