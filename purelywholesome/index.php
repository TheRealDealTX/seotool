<?php
// Purely Wholesome Farm - front controller. Every URL that is not a real file lands here.
declare(strict_types=1);
// Local preview (php -S): let the built-in server hand out real files itself.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)))) {
    return false;
}
require __DIR__ . '/app/bootstrap.php';

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$query = $_GET;

// On the real domain: force https and the bare host (TLS terminates upstream).
if (is_production_host()) {
    $host = strtolower($_SERVER['HTTP_HOST'] ?? '');
    if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || str_starts_with($host, 'www.')) {
        redirect(SITE_ORIGIN . $uri);
    }
}
if (!is_production_host()) {
    header('X-Robots-Tag: noindex, nofollow');
}

// ---- Old WordPress URLs ----------------------------------------------------
if (isset($query['s']) && $path === '/') {
    $q = trim((string)$query['s']);
    render('search', ['q' => $q, 'results' => search_posts($q)], [
        'title' => ($q === '' ? 'Search' : 'Search results for “' . $q . '”') . ' | ' . SITE_NAME,
        'desc' => 'Search the Purely Wholesome Farm recipes and homestead guides.', 'path' => '/', 'robots' => 'noindex, follow']);
    exit;
}
if (isset($query['p']) || isset($query['page_id'])) {
    redirect('/');
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content/plugins|wp-content/themes)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(comments/)?feed/?$#', $path) || preg_match('#^/[a-z0-9-]+/feed/?$#', $path)) {
    require __DIR__ . '/app/feed.php';
    exit;
}
// Resized WordPress image variants (foo-300x200.webp) -> the original upload.
if (preg_match('#^(/wp-content/uploads/.+)-\d+x\d+(\.\w+)$#', $path, $m) && is_file(__DIR__ . $m[1] . $m[2])) {
    redirect($m[1] . $m[2]);
}
if (str_starts_with($path, '/wp-content/')) {
    not_found();
}
$legacy = require __DIR__ . '/app/redirects.php';
$key = trim($path, '/');
if (isset($legacy[$key])) {
    redirect($legacy[$key]);
}
if (preg_match('#^/(blog|category/[a-z0-9-]+)/page/\d+/?$#', $path, $m)) {
    redirect('/' . $m[1] . '/');
}
if (preg_match('#^/page/\d+/?$#', $path) || preg_match('#^/(author|tag)/#', $path)) {
    redirect(str_starts_with($path, '/author/') ? '/about-us/' : '/blog/');
}

// ---- Machine-readable files ------------------------------------------------
switch ($path) {
    case '/robots.txt':
        header('Content-Type: text/plain; charset=utf-8');
        if (!is_production_host()) {
            echo "User-agent: *\nDisallow: /\n";
        } else {
            echo "User-agent: *\nDisallow: /app/\nDisallow: /content/\nDisallow: /_build/\nDisallow: /?s=\n\nSitemap: " . SITE_ORIGIN . "/sitemap_index.xml\n";
        }
        exit;
    case '/sitemap.xml':
    case '/sitemap_index.xml':
    case '/post-sitemap.xml':
    case '/page-sitemap.xml':
    case '/category-sitemap.xml':
        require __DIR__ . '/app/sitemap.php';
        exit;
    case '/search-index.json':
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: public, max-age=3600');
        $items = [];
        foreach (live_posts() as $p) {
            $items[] = ['t' => $p['h1'] ?: $p['title'], 'u' => post_url($p['slug']), 'd' => $p['desc'], 'c' => TOPICS[$p['topic']][0] ?? '', 'i' => $p['image']];
        }
        foreach (tools() as $slug => $t) {
            $items[] = ['t' => $t['name'], 'u' => '/tools/' . $slug . '/', 'd' => $t['short'], 'c' => 'Interactive tool', 'i' => ''];
        }
        echo json_encode($items, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
}

// Directory-style URLs end in a slash, as they did on WordPress.
if ($path !== '/' && !str_ends_with($path, '/')) {
    if (preg_match('#^/[a-z0-9/_-]+$#i', $path)) {
        redirect($path . '/' . (($qs = parse_url($uri, PHP_URL_QUERY)) ? '?' . $qs : ''));
    }
    not_found();
}

// ---- Pages -----------------------------------------------------------------
$parts = array_values(array_filter(explode('/', $path), 'strlen'));

if (!$parts) {
    require __DIR__ . '/app/controllers/home.php';
    exit;
}

switch ($parts[0]) {
    case 'blog':
        if (count($parts) === 1) {
            render('archive', ['heading' => 'The Farm Journal', 'intro' => 'Every recipe, how-to and homestead guide from Purely Wholesome Farm. Filter by topic or search as you type.', 'posts' => live_posts(), 'filters' => true, 'crumbs' => [['Home', '/'], ['Blog', '/blog/']]], [
                'title' => 'The Farm Journal: Recipes & Homestead Guides | ' . SITE_NAME,
                'desc' => 'Browse every Purely Wholesome Farm recipe and homestead guide: lamb, brining, pumpkin pie, canning, goats, chickens and more.', 'path' => '/blog/']);
            exit;
        }
        break;
    case 'category':
        if (count($parts) === 2 && isset(CATEGORIES[$parts[1]])) {
            [$name, $intro] = CATEGORIES[$parts[1]];
            $posts = array_filter(live_posts(), fn($p) => in_array($parts[1], array_map('category_slug', $p['categories']), true));
            render('archive', ['heading' => $name, 'intro' => $intro, 'posts' => $posts, 'filters' => count($posts) > 12, 'crumbs' => [['Home', '/'], ['Blog', '/blog/'], [$name, $path]]], [
                'title' => $name . ' | ' . SITE_NAME, 'desc' => $intro, 'path' => $path]);
            exit;
        }
        break;
    case 'topics':
        if (count($parts) === 2 && isset(TOPICS[$parts[1]])) {
            require __DIR__ . '/app/controllers/topic.php';
            exit;
        }
        if (count($parts) === 1) {
            redirect('/blog/');
        }
        break;
    case 'tools':
        if (count($parts) === 1) {
            render('tools', [], ['title' => 'Free Farm & Kitchen Calculators | ' . SITE_NAME,
                'desc' => 'Free interactive tools from Purely Wholesome Farm: brine calculator, lamb cooking times, goat due dates, canning altitude adjustments, egg planner and more.', 'path' => '/tools/']);
            exit;
        }
        if (count($parts) === 2 && isset(tools()[$parts[1]])) {
            $tool = tools()[$parts[1]];
            render('tool', ['slug' => $parts[1], 'tool' => $tool], ['title' => $tool['title'] . ' | ' . SITE_NAME, 'desc' => $tool['desc'], 'path' => $path]);
            exit;
        }
        break;
    case 'about-us':
    case 'contact-us':
    case 'privacy-policy':
    case 'terms-of-use':
    case 'editorial-policy':
        if (count($parts) === 1) {
            require __DIR__ . '/app/controllers/page.php';
            exit;
        }
        break;
    case 'subscribe':
        if (count($parts) === 1) {
            require __DIR__ . '/app/controllers/subscribe.php';
            exit;
        }
        break;
}

if (count($parts) === 1 && ($post = load_post($parts[0]))) {
    require __DIR__ . '/app/controllers/post.php';
    exit;
}

not_found();
