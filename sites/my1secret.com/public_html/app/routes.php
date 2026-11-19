<?php
declare(strict_types=1);
defined('M1S') || exit;

foreach (glob(M1S_APP . '/controllers/*.php') as $f) {
    require $f;
}

function m1s_routes(): array
{
    $c = '([a-z0-9-]+)';
    return [
        // [methods, regex, handler]
        ['GET',  '#^/$#', 'home_page'],
        ['GET',  '#^/blog/$#', 'blog_index'],
        ['GET',  "#^/blog/topic/$c/$#", 'blog_topic'],
        ['GET',  "#^/blog/$c/$#", 'article_page'],
        ['GET',  '#^/author/([A-Za-z0-9_-]+)/$#', 'author_page'],
        ['GET',  '#^/forum/$#', 'forum_index'],
        ['GET',  "#^/forum/$c/$#", 'community_page'],
        ['GET',  "#^/forum/$c/(\d+)-([a-z0-9-]*)/$#", 'thread_page'],
        ['GET|POST', "#^/forum/$c/(\d+)-([a-z0-9-]*)/edit/$#", 'thread_edit'],
        ['GET|POST', '#^/submit/$#', 'submit_page'],
        ['POST', '#^/thread/(\d+)/delete/$#', 'thread_delete'],
        ['POST', '#^/thread/(\d+)/mod/$#', 'thread_mod'],
        ['POST', '#^/comment/$#', 'comment_create'],
        ['POST', '#^/comment/(\d+)/edit/$#', 'comment_edit'],
        ['POST', '#^/comment/(\d+)/delete/$#', 'comment_delete'],
        ['POST', '#^/comment/(\d+)/mod/$#', 'comment_mod'],
        ['POST', '#^/vote/$#', 'vote_action'],
        ['GET',  '#^/confirm/$#', 'guest_confirm'],
        ['GET',  '#^/confirm/sent/$#', 'guest_confirm_sent'],
        ['GET',  '#^/shop/$#', 'shop_page'],
        ['GET|POST', '#^/report/$#', 'report_action'],
        ['GET',  '#^/u/([A-Za-z0-9_-]+)/$#', 'profile_page'],
        ['GET|POST', '#^/login/$#', 'login_page'],
        ['GET|POST', '#^/register/$#', 'register_page'],
        ['POST', '#^/logout/$#', 'logout_action'],
        ['GET|POST', '#^/forgot-password/$#', 'forgot_page'],
        ['GET|POST', '#^/reset-password/$#', 'reset_page'],
        ['GET|POST', '#^/settings/$#', 'settings_page'],
        ['GET',  '#^/search/$#', 'search_page'],
        ['GET',  '#^/(about|privacy-policy|terms|community-guidelines|contact)/$#', 'static_page'],
        ['GET',  '#^/sitemap\.xml$#', 'sitemap_xml'],
        ['GET',  '#^/robots\.txt$#', 'robots_txt'],
        ['GET',  '#^/site\.webmanifest$#', 'web_manifest'],
        ['GET',  '#^/feed/$#', 'rss_feed'],
        ['GET',  '#^/admin/$#', 'admin_dashboard'],
        ['GET',  '#^/admin/articles/$#', 'admin_articles'],
        ['GET|POST', '#^/admin/articles/(new|\d+)/$#', 'admin_article_edit'],
        ['POST', '#^/admin/articles/(\d+)/delete/$#', 'admin_article_delete'],
        ['GET|POST', '#^/admin/reports/$#', 'admin_reports'],
        ['GET|POST', '#^/admin/users/$#', 'admin_users'],
        ['GET|POST', '#^/admin/communities/$#', 'admin_communities'],
        ['GET|POST', '#^/admin/topics/$#', 'admin_topics'],
        ['GET|POST', '#^/admin/products/$#', 'admin_products'],
        ['GET',  '#^/install/$#', 'install_page'],
    ];
}

function m1s_dispatch(): void
{
    $uri = $_SERVER['REQUEST_URI'] ?? '/';
    $path = rawurldecode(strtok($uri, '?') ?: '/');
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    if ($method === 'HEAD') {
        $method = 'GET';
    }

    // Canonical scheme + host (TLS terminates upstream; the proxy sets X-Forwarded-Proto).
    $canonHost = parse_url(cfg('base_url'), PHP_URL_HOST);
    $host = strtolower($_SERVER['HTTP_HOST'] ?? '');
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if (cfg('enforce_host', true) && $method === 'GET' && ($insecure || ($host !== '' && $host !== $canonHost && $host === 'www.' . $canonHost))) {
        redirect(abs_url($uri), 301);
    }

    if ($path === '/index.php' && $method === 'GET') {
        redirect('/' . (($_SERVER['QUERY_STRING'] ?? '') !== '' ? '?' . $_SERVER['QUERY_STRING'] : ''), 301);
    }

    // Legacy WordPress URLs first: they must win over the new routes.
    legacy_wordpress($path);

    // Add the trailing slash to page URLs (not files like /sitemap.xml).
    if ($method === 'GET' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
        $qs = $_SERVER['QUERY_STRING'] ?? '';
        foreach (m1s_routes() as [$methods, $re]) {
            if (preg_match($re, $path . '/')) {
                redirect($path . '/' . ($qs !== '' ? '?' . $qs : ''), 301);
            }
        }
    }

    foreach (m1s_routes() as [$methods, $re, $handler]) {
        if (preg_match($re, $path, $m)) {
            if (!in_array($method, explode('|', $methods), true)) {
                http_response_code(405);
                header('Allow: ' . str_replace('|', ', ', $methods));
                exit('Method not allowed');
            }
            if ($method === 'POST' && !in_array($handler, ['login_page', 'register_page', 'forgot_page', 'reset_page'], true)) {
                if (in_array($handler, ['submit_page', 'comment_create'], true) && !current_user()) {
                    // guests have no session: stateless same-origin check instead of a session token
                    same_origin_check();
                } else {
                    // every state-changing request from a member needs a valid CSRF token
                    csrf_check();
                }
            }
            array_shift($m);
            $handler(...$m);
            return;
        }
    }
    not_found();
}

/** 301 / 410 handling for every URL the WordPress site ever exposed. */
function legacy_wordpress(string $path): void
{
    static $map = null;
    $map ??= require M1S_APP . '/seed/legacy.php';
    $norm = rtrim($path, '/') . '/';

    // ?p=123 style links
    if ($path === '/' && isset($_GET['p']) && ctype_digit((string)$_GET['p'])) {
        $to = $map['redirect']['/?p=' . (int)$_GET['p']] ?? null;
        $to ? redirect($to, 301) : gone();
    }
    if (isset($map['redirect'][$norm]) && $norm !== '/') {
        // articles may have been renamed in admin since the migration: follow the current slug
        if (preg_match('#^/blog/([a-z0-9-]+)/$#', $map['redirect'][$norm], $mm)) {
            $legacy = trim(preg_replace('#^/discussion/#', '/', $norm), '/');
            $cur = val('SELECT slug FROM articles WHERE legacy_slug = ?', [$legacy]);
            redirect('/blog/' . ($cur ?: $mm[1]) . '/', 301);
        }
        redirect($map['redirect'][$norm], 301);
    }
    if (in_array($norm, $map['gone'], true)) {
        gone();
    }
    if (str_starts_with($path, '/wp-content/uploads/')) {
        if (isset($map['media'][$path])) {
            redirect($map['media'][$path], 301);
        }
        gone();
    }
    if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php|wp-cron\.php|wp-signup\.php)(/|$)#', $path)) {
        gone();
    }
    if (preg_match('#^/(sitemap_index|post-sitemap|page-sitemap|category-sitemap|post_tag-sitemap|author-sitemap|wp-sitemap[\w-]*)\.xml$#', $path)) {
        redirect('/sitemap.xml', 301);
    }
    if (preg_match('#^/(discussion/)?(feed|comments/feed)/?$#', $path) && $path !== '/feed/') {
        redirect('/feed/', 301);
    }
    if (preg_match('#^/(?:discussion/)?page/(\d+)/?$#', $path, $m)) {
        redirect('/blog/' . ((int)$m[1] > 1 ? '?page=' . (int)$m[1] : ''), 301);
    }
    if (preg_match('#^/(topics|categories)/([a-z0-9-]+)/(page/\d+/|feed/)?$#', $path, $m)) {
        redirect($map['redirect']["/{$m[1]}/{$m[2]}/"] ?? '/blog/', 301);
    }
    if (preg_match('#^/discussion/([a-z0-9-]+)/(feed|amp|embed)/?$#', $path, $m)) {
        $to = $map['redirect']["/discussion/{$m[1]}/"] ?? null;
        $to ? redirect($to, 301) : gone();
    }
}
