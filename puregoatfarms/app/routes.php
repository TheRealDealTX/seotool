<?php
// URL routing, legacy WordPress redirects and machine-readable endpoints.
defined('PGF') || exit;

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

function page_file(string $name, array $vars = []): string
{
    extract($vars);
    ob_start();
    include APP . "/pages/$name.php";
    return ob_get_clean();
}

function not_found(): never
{
    http_response_code(404);
    echo page_file('404');
    exit;
}

// Static pages: path => template in app/pages/.
const PAGES = [
    '/'                     => 'home',
    '/about/'               => 'about',
    '/contact/'             => 'contact',
    '/blog/'                => 'blog',
    '/tools/'               => 'tools',
    '/faq/'                 => 'faq',
    '/start-here/'          => 'start-here',
    '/privacy-policy/'      => 'privacy-policy',
    '/terms-of-use/'        => 'terms-of-use',
    '/affiliate-disclosure/' => 'affiliate-disclosure',
    '/sitemap/'             => 'sitemap',
];

function dispatch(string $method, string $uri): void
{
    $host = strtolower($_SERVER['HTTP_HOST'] ?? '');
    $path = parse_url($uri, PHP_URL_PATH) ?: '/';
    $path = '/' . ltrim(rawurldecode($path), '/');

    // Canonical scheme + host (TLS terminates upstream, so trust X-Forwarded-Proto).
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($host === 'www.' . SITE_HOST || ($insecure && str_ends_with($host, SITE_HOST))) {
        redirect($uri);
    }

    // WordPress query-string URLs (?p=, ?page_id=, ?s=, ?feed=).
    if ($path === '/' && isset($_GET['feed'])) redirect('/feed/');
    if ($path === '/' && isset($_GET['s'])) redirect('/blog/');
    if ($path === '/' && (isset($_GET['p']) || isset($_GET['page_id']) || isset($_GET['cat']))) redirect('/');

    if ($path === '/index.php') $path = '/';

    // Machine-readable endpoints.
    switch ($path) {
        case '/sitemap_index.xml':    xml_sitemap_index(); return;
        case '/post-sitemap.xml':     xml_urlset(urls_posts()); return;
        case '/page-sitemap.xml':     xml_urlset(urls_pages()); return;
        case '/category-sitemap.xml': xml_urlset(urls_categories()); return;
        case '/tool-sitemap.xml':     xml_urlset(urls_tools()); return;
        case '/sitemap.xml':
        case '/wp-sitemap.xml':       redirect('/sitemap_index.xml');
        case '/feed/':                rss_feed(); return;
    }

    // Legacy WordPress paths -> closest equivalent.
    $legacy = [
        '#^/(comments/)?feed(/.*)?$#'                           => '/feed/',
        '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-signup\.php|wp-cron\.php)(/.*)?$#' => '/',
        '#^/category/uncategorized(/.*)?$#'                     => '/blog/',
        '#^/(blog/)?page/\d+/?$#'                               => '/blog/',
        '#^/author/[^/]+(/.*)?$#'                               => '/about/',
        '#^/tag/[^/]+(/.*)?$#'                                  => '/blog/',
        '#^/20\d\d(/\d\d)?(/\d\d)?/?$#'                         => '/blog/',
        '#^/home/?$#'                                           => '/',
        '#^/about-us/?$#'                                       => '/about/',
        '#^/contact-us/?$#'                                     => '/contact/',
        '#^/sitemap_index\.xml/?$#'                             => '/sitemap_index.xml',
    ];
    foreach ($legacy as $re => $to) {
        if (preg_match($re, $path)) redirect($to);
    }
    // /category/<slug>/page/2/ and /category/<slug>/feed/
    if (preg_match('#^/category/([a-z-]+)/(page/\d+|feed)/?$#', $path, $m)) redirect("/category/$m[1]/");
    // /<post>/amp/, /<post>/feed/, /<post>/embed/
    if (preg_match('#^/([a-z0-9-]+)/(amp|feed|embed|comment-page-\d+)/?$#', $path, $m) && isset(POSTS[$m[1]])) redirect("/$m[1]/");

    // Every page URL ends with a slash, like the WordPress original.
    if (!str_ends_with($path, '/') && !str_contains(basename($path), '.')) {
        redirect($path . '/' . (($q = parse_url($uri, PHP_URL_QUERY)) ? "?$q" : ''));
    }

    if ($method === 'POST') {
        if ($path === '/contact/') { handle_contact(); return; }
        if ($path === '/subscribe/') { handle_subscribe(); return; }
    }
    if ($path === '/subscribe/') redirect('/');

    if (isset(PAGES[$path])) {
        echo page_file(PAGES[$path]);
        return;
    }
    if (preg_match('#^/category/([a-z-]+)/$#', $path, $m) && isset(CATEGORIES[$m[1]])) {
        echo page_file('category', ['slug' => $m[1]]);
        return;
    }
    if (preg_match('#^/tools/([a-z-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
        echo page_file('tool', ['slug' => $m[1]]);
        return;
    }
    if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && isset(POSTS[$m[1]])) {
        echo page_file('post', ['slug' => $m[1]]);
        return;
    }
    not_found();
}

// ---- Sitemaps & feed ---------------------------------------------------------

function urls_posts(): array
{
    $u = [['/blog/', max(array_column(POSTS, 'modified'))]];
    foreach (posts_sorted() as $slug => $p) {
        $u[] = ["/$slug/", $p['modified'], $p['image'][0], $p['alt']];
    }
    return $u;
}

function urls_pages(): array
{
    $latest = max(array_column(POSTS, 'modified'));
    return [
        ['/', $latest, IMG['hero'], 'Dairy goats on pasture at Pure Goat Farms'],
        ['/about/', '2026-10-14', IMG['story'], 'The Pure Goat Farms herd resting in the field'],
        ['/start-here/', '2026-10-14'],
        ['/faq/', '2026-10-14'],
        ['/contact/', '2026-10-14'],
        ['/privacy-policy/', '2026-10-14'],
        ['/terms-of-use/', '2026-10-14'],
        ['/affiliate-disclosure/', '2026-10-14'],
        ['/sitemap/', '2026-10-14'],
    ];
}

function urls_categories(): array
{
    $u = [];
    foreach (CATEGORIES as $slug => $c) {
        $dates = array_column(posts_in($slug), 'modified');
        $u[] = ["/category/$slug/", $dates ? max($dates) : '2026-10-14'];
    }
    return $u;
}

function urls_tools(): array
{
    $u = [['/tools/', '2026-10-14']];
    foreach (TOOLS as $slug => $t) {
        $u[] = ["/tools/$slug/", '2026-10-14'];
    }
    return $u;
}

function xml_sitemap_index(): void
{
    header('Content-Type: application/xml; charset=utf-8');
    $maps = [
        'post-sitemap.xml' => urls_posts(),
        'page-sitemap.xml' => urls_pages(),
        'category-sitemap.xml' => urls_categories(),
        'tool-sitemap.xml' => urls_tools(),
    ];
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($maps as $file => $urls) {
        $last = max(array_column($urls, 1));
        echo "\t<sitemap>\n\t\t<loc>" . SITE_URL . "/$file</loc>\n\t\t<lastmod>" . iso_date($last) . "</lastmod>\n\t</sitemap>\n";
    }
    echo '</sitemapindex>';
}

function xml_urlset(array $urls): void
{
    header('Content-Type: application/xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n"
        . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach ($urls as $u) {
        echo "\t<url>\n\t\t<loc>" . e(SITE_URL . $u[0]) . "</loc>\n\t\t<lastmod>" . iso_date($u[1]) . "</lastmod>\n";
        if (!empty($u[2])) {
            echo "\t\t<image:image>\n\t\t\t<image:loc>" . e(abs_url($u[2])) . "</image:loc>\n\t\t</image:image>\n";
        }
        echo "\t</url>\n";
    }
    echo '</urlset>';
}

function rss_feed(): void
{
    header('Content-Type: application/rss+xml; charset=utf-8');
    $posts = posts_sorted();
    $first = reset($posts);
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">' . "\n<channel>\n";
    echo '<title>' . e(SITE_NAME) . "</title>\n<atom:link href=\"" . SITE_URL . "/feed/\" rel=\"self\" type=\"application/rss+xml\" />\n";
    echo '<link>' . SITE_URL . "/</link>\n<description>" . e(SITE_TAGLINE) . "</description>\n";
    echo '<lastBuildDate>' . date(DATE_RSS, strtotime($first['modified'])) . "</lastBuildDate>\n<language>en-US</language>\n";
    foreach ($posts as $slug => $p) {
        $link = SITE_URL . "/$slug/";
        echo "<item>\n<title>" . e($p['title']) . "</title>\n<link>$link</link>\n<guid isPermaLink=\"true\">$link</guid>\n";
        echo '<pubDate>' . date(DATE_RSS, strtotime($p['date'] . ' 08:00 UTC')) . "</pubDate>\n";
        foreach ($p['cats'] as $c) {
            echo '<category>' . e(CATEGORIES[$c]['name']) . "</category>\n";
        }
        echo '<description>' . e($p['desc']) . "</description>\n</item>\n";
    }
    echo "</channel>\n</rss>";
}
