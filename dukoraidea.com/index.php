<?php
// dukoraidea.com front controller.
// Pages are pre-rendered by build.py into _pages/<path>.html; this file maps the
// clean, Shopify-style URLs of the original site (no trailing slash) onto them,
// 301s legacy Shopify paths, handles the contact form and serves real 404s.
// Static files (assets, sitemap.xml, robots.txt, icons) are served directly by the host.

// Local preview (`php -S localhost:8000 index.php`): let the dev server serve real files.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) {
    return false;
}

$home = 'https://dukoraidea.com';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$qpos = strpos($uri, '?');
$qs   = $qpos === false ? '' : substr($uri, $qpos);
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

function go($to, $code = 301) {
    header('Location: ' . $to, true, $code);
    exit;
}

function page($file, $status = 200) {
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    if ($status === 200) header('Cache-Control: public, max-age=600');
    readfile($file);
    exit;
}

// Canonical host and scheme: www and plain http go to https://dukoraidea.com.
// (TLS terminates upstream, so X-Forwarded-Proto is the only reliable signal.)
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.dukoraidea.com' || ($insecure && $host === 'dukoraidea.com')) {
    go($home . $uri);
}

// Contact form.
if ($path === '/contact' && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $name  = trim(substr((string)($_POST['name'] ?? ''), 0, 100));
    $email = trim(substr((string)($_POST['email'] ?? ''), 0, 150));
    $topic = trim(substr((string)($_POST['topic'] ?? ''), 0, 80));
    $msg   = trim(substr((string)($_POST['message'] ?? ''), 0, 5000));
    $trap  = (string)($_POST['website'] ?? '');
    if ($trap !== '') go('/pages/contact?status=sent', 303);          // bot: pretend success
    $ok = $name !== '' && $msg !== '' && filter_var($email, FILTER_VALIDATE_EMAIL);
    if ($ok) {
        $clean = function ($s) { return str_replace(["\r", "\n"], ' ', $s); };
        $subject = 'Dukora Idea contact: ' . $clean($topic ?: 'Message');
        $body = "Name: {$name}\nEmail: {$email}\nTopic: {$topic}\n\n{$msg}\n";
        $headers = "From: Dukora Idea <info@dukoraidea.com>\r\n"
                 . 'Reply-To: ' . $clean($name) . ' <' . $clean($email) . ">\r\n"
                 . "Content-Type: text/plain; charset=utf-8\r\n";
        $ok = @mail('info@dukoraidea.com', $subject, $body, $headers);
    }
    go('/pages/contact?status=' . ($ok ? 'sent' : 'error'), 303);
}
if ($path === '/contact') go('/pages/contact');

// Home.
if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    if ($path !== '/') go('/' . $qs);
    page(__DIR__ . '/_pages/home.html');
}

// Normalise: lowercase, no trailing slash.
$norm = rtrim(strtolower($path), '/');
if ($norm === '') go('/' . $qs);
if ($norm !== $path) {
    // Only redirect when the normalised URL exists or is itself a legacy redirect.
    $path = $norm;
    $redirect_after = true;
}

// Legacy Shopify URLs from the original store.
$legacy = [
    '#^/collections/[^/]+/products/([a-z0-9\-]+)$#' => '/products/$1',
    '#^/collections/frontpage$#'                   => '/',
    '#^/collections$#'                             => '/collections/all',
    '#^/products$#'                                => '/collections/all',
    '#^/blogs$#'                                   => '/blogs/blog',
    '#^/blogs/(news|blog)/tagged/.*$#'             => '/blogs/blog',
    '#^/blogs/news(/.*)?$#'                        => '/blogs/blog',
    '#^/blogs/blog\.atom$#'                        => '/blogs/blog',
    '#^/pages/(contact-us|contact-information)$#'  => '/pages/contact',
    '#^/pages/(about|our-story)$#'                 => '/pages/about-us',
    '#^/policies/privacy$#'                        => '/policies/privacy-policy',
    '#^/policies/terms$#'                          => '/policies/terms-of-service',
    '#^/policies/(refund-policy|shipping-policy)$#'=> '/pages/contact',
    '#^/(cart|checkout|account|search)(/.*)?$#'    => '/',
    '#^/sitemap(_[a-z0-9_]+)?\.xml$#'              => '/sitemap.xml',
    '#^/(feed|rss)/?$#'                            => '/blogs/blog',
];
foreach ($legacy as $re => $to) {
    if ($path !== '/sitemap.xml' && preg_match($re, $path)) {
        go(preg_replace($re, $to, $path));
    }
}

// Pre-rendered page?
if (preg_match('#^/[a-z0-9][a-z0-9\-/]*$#', $path) && strpos($path, '..') === false) {
    $file = __DIR__ . '/_pages' . $path . '.html';
    if (is_file($file)) {
        if (!empty($redirect_after)) go($path . $qs);
        page($file);
    }
}

// Unknown product or collection handles from the old store -> all light guides.
if (preg_match('#^/(products|collections)/[a-z0-9\-]+$#', $path)) go('/collections/all');

page(__DIR__ . '/_pages/404.html', 404);
