<?php
// underdeskelliptical.com front controller.
//
// The site is hosted on a Hostinger Agency (h5g) website, which serves files that exist
// directly and sends every other request here (it ignores .htaccess). So this file is
// the whole URL map: every post, page, category (/topic/), tag, tool and sitemap, plus
// 301s for leftover WordPress URLs so nothing that Google knows about returns a 404.

declare(strict_types=1);
define('ROOT', __DIR__);

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');

require ROOT . '/inc/config.php';

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

// Canonical scheme + host (TLS terminates upstream, so trust X-Forwarded-Proto).
$host = strtolower($_SERVER['HTTP_HOST'] ?? SITE_HOST);
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || $host === 'www.' . SITE_HOST) {
    redirect(SITE_URL . $uri);
}

// Normalise: collapse slashes, drop index.php.
$norm = preg_replace('#/+#', '/', $path);
if ($norm === '/index.php') {
    $norm = '/';
}

define('CURRENT_PATH', $norm);
require ROOT . '/inc/products.php';
require ROOT . '/inc/functions.php';
require ROOT . '/inc/tools.php';
require ROOT . '/inc/layout.php';
require ROOT . '/inc/contact.php';

$pages = ['about-us', 'contact', 'affiliate-disclosure', 'privacy-policy', 'terms-of-use'];

// ---- XML sitemaps (the Yoast URLs Google already has, all served live) ----
$sitemaps = ['sitemap.xml', 'sitemap_index.xml', 'wp-sitemap.xml', 'post-sitemap.xml', 'page-sitemap.xml', 'category-sitemap.xml', 'post_tag-sitemap.xml'];
if (preg_match('#^/([a-z_-]+\.xml)$#', $norm, $m) && in_array($m[1], $sitemaps)) {
    require ROOT . '/templates/sitemap-xml.php';
    exit;
}

if ($norm === '/llms.txt') {
    require ROOT . '/templates/llms.php';
    exit;
}

// ---- WordPress leftovers ----
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-signup\.php|wp-cron\.php)(/|$)#', $norm)) {
    redirect('/');
}
if ($norm === '/feed/' || $norm === '/feed') {
    require ROOT . '/templates/feed.php';
    exit;
}
if (preg_match('#^/comments/feed/?$#', $norm)) {
    redirect('/feed/');
}
if (preg_match('#^/(.+?)/feed/?$#', $norm, $m)) {
    redirect('/' . $m[1] . '/');
}
if (preg_match('#^/author/#', $norm)) {
    redirect('/about-us/');
}
if (preg_match('#^/category/([a-z0-9-]+)#', $norm, $m)) {
    redirect(isset(CATEGORIES[$m[1]]) ? '/topic/' . $m[1] . '/' : '/blog/');
}
if (preg_match('#^/(blog|topic/[a-z0-9-]+|tag/[a-z0-9-]+)/page/\d+/?$#', $norm, $m)) {
    redirect('/' . $m[1] . '/');
}
if (preg_match('#^/\d{4}/\d{2}(/\d{2})?/([a-z0-9-]+)/?$#', $norm, $m) && is_file(ROOT . "/content/posts/{$m[2]}.php")) {
    redirect('/' . $m[2] . '/');
}
if (preg_match('#^/(wp-content/uploads/.+)-\d+x\d+(\.\w+)$#', $norm, $m)) {
    // Old WordPress thumbnail sizes -> the full-size image we kept.
    foreach ([$m[2], '.webp', '.jpg', '.png'] as $ext) {
        if (is_file(ROOT . '/' . $m[1] . $ext)) {
            redirect('/' . $m[1] . $ext);
        }
    }
}
if (isset($_GET['p']) || isset($_GET['page_id'])) {
    redirect('/');
}

// ---- Trailing slash ----
if ($norm !== '/' && !str_ends_with($norm, '/') && !preg_match('#\.\w{2,12}$#', $norm)) {
    redirect($norm . '/' . (isset($_GET['s']) ? '?s=' . rawurlencode((string) $_GET['s']) : ''));
}

// ---- Routes ----
header('Content-Type: text/html; charset=utf-8');
$seg = trim($norm, '/');

if ($seg === '' && isset($_GET['s'])) {
    require ROOT . '/templates/search.php';
} elseif ($seg === '') {
    require ROOT . '/templates/home.php';
} elseif ($seg === 'blog') {
    $archive = ['type' => 'blog'];
    require ROOT . '/templates/archive.php';
} elseif (preg_match('#^topic/([a-z0-9-]+)$#', $seg, $m) && isset(CATEGORIES[$m[1]])) {
    $archive = ['type' => 'topic', 'slug' => $m[1]];
    require ROOT . '/templates/archive.php';
} elseif (preg_match('#^tag/([a-z0-9-]+)$#', $seg, $m) && isset(TAGS[$m[1]])) {
    $archive = ['type' => 'tag', 'slug' => $m[1]];
    require ROOT . '/templates/archive.php';
} elseif ($seg === 'tools') {
    require ROOT . '/templates/tools-hub.php';
} elseif (preg_match('#^tools/([a-z0-9-]+)$#', $seg, $m) && isset(TOOLS[$m[1]])) {
    $toolSlug = $m[1];
    require ROOT . '/templates/tool.php';
} elseif ($seg === 'sitemap') {
    require ROOT . '/templates/sitemap-html.php';
} elseif (in_array($seg, $pages, true)) {
    $page = require ROOT . "/content/pages/$seg.php";
    require ROOT . '/templates/page.php';
} elseif (preg_match('#^[a-z0-9-]+$#', $seg) && isset(all_posts()[$seg])) {
    $post = all_posts()[$seg];
    require ROOT . '/templates/post.php';
} else {
    http_response_code(404);
    require ROOT . '/templates/404.php';
}
