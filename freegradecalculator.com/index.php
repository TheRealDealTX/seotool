<?php
// freegradecalculator.com front controller
// Local dev server: let real files through (Apache/LiteSpeed does this via .htaccess)
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) return false;
require __DIR__ . '/inc/functions.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$qs   = ($q = parse_url($uri, PHP_URL_QUERY)) ? '?' . $q : '';

function redirect(string $to, int $code = 301): never {
    header('Location: ' . SITE_URL . $to, true, $code);
    exit;
}

// Canonical host (https/www are also handled in .htaccess / hPanel)
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if (str_starts_with($host, 'www.')) redirect($path . $qs);
// Preview hosts (e.g. *.hostingersite.com) must never be indexed
if ($host !== '' && $host !== 'freegradecalculator.com' && PHP_SAPI !== 'cli-server') header('X-Robots-Tag: noindex, nofollow');
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http') redirect($path . $qs);

// ---- Legacy URLs (old static site used .html) ----
$legacy = [
    '/index.html' => '/', '/index.php' => '/', '/home' => '/',
    '/blog.html' => '/blog', '/about.html' => '/about-us', '/about' => '/about-us',
    '/contact-us' => '/contact', '/contact-us.html' => '/contact',
    '/grade-calculator' => '/', '/grade-to-gpa' => '/gpa-converter', '/gpa-scale' => '/gpa-converter',
    '/ez-grader' => '/easy-grader', '/blog/index.html' => '/blog',
];
if (isset($legacy[$path])) redirect($legacy[$path] . $qs);
if (str_ends_with($path, '.html')) redirect(substr($path, 0, -5) . $qs);
if ($path !== '/' && str_ends_with($path, '/')) redirect(rtrim($path, '/') . $qs);
if ($path !== strtolower($path)) redirect(strtolower($path) . $qs);

// ---- Routes ----
$static = [
    '/'                     => 'home',
    '/tools'                => 'tools-index',
    '/blog'                 => 'blog-index',
    '/about-us'             => 'about',
    '/contact'              => 'contact',
    '/privacy-policy'       => 'privacy',
    '/terms-of-use'         => 'terms',
    '/disclaimer'           => 'disclaimer',
    '/affiliate-disclosure' => 'affiliate',
    '/study-supplies'       => 'supplies',
    '/sitemap'              => 'sitemap-html',
    '/sitemap.xml'          => 'sitemap-xml',
];
if (isset($static[$path])) {
    include ROOT . '/templates/' . $static[$path] . '.php';
    exit;
}
if (preg_match('#^/blog/([a-z0-9-]+)$#', $path, $m) && isset(articles()[$m[1]])) {
    $article = articles()[$m[1]];
    include ROOT . '/templates/article.php';
    exit;
}
if (preg_match('#^/([a-z0-9-]+)$#', $path, $m) && tool_meta($m[1])) {
    $tool = tool_meta($m[1]);
    include ROOT . '/templates/tool.php';
    exit;
}

http_response_code(404);
include ROOT . '/templates/404.php';
