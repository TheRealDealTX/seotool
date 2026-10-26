<?php
// Front controller. Existing files are served directly by the web server;
// every other request lands here (the host routes misses to index.php and
// ignores .htaccess, so all redirects live in this file).
require __DIR__ . '/app/bootstrap.php';
require HA_APP . '/lib/Listings.php';

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));

function redirect(string $to, int $code = 301): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

function not_found(): void
{
    http_response_code(404);
    render('404', [], ['title' => 'Page Not Found | Houston Apartments', 'noindex' => true]);
    exit;
}

// Canonical scheme (TLS terminates upstream)
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http') {
    redirect('https://' . ($_SERVER['HTTP_HOST'] ?? '') . $uri);
}

// Old WordPress plumbing → nearest equivalent
if (preg_match('#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(feed|comments/feed|post/feed)/?$#', $path) || preg_match('#^/post/[^/]+/feed/?$#', $path)) {
    redirect('/houston-apartments-blog/');
}
if (preg_match('#^/(author|tag)/#', $path)) {
    redirect('/houston-apartments-blog/');
}
if ($path === '/home/' || $path === '/index.php') {
    redirect('/');
}

// Trailing slash for page URLs (WordPress style)
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.\w{2,5}$#', $path) && !str_starts_with($path, '/api/')) {
    redirect($path . '/' . (($q = parse_url($uri, PHP_URL_QUERY)) ? "?$q" : ''));
}

$routes = [
    '#^/$#'                                      => fn () => page_home(),
    '#^/apartments/$#'                           => fn () => page_search(),
    '#^/apartment/([a-z0-9-]+)/$#'               => fn ($m) => page_property($m[1]),
    '#^/houston-apartments-neighborhoods/$#'     => fn () => page_neighborhoods(),
    '#^/houston-apartments-blog/(?:page/(\d+)/)?$#' => fn ($m) => page_blog((int) ($m[1] ?? 1)),
    '#^/post/category/blog/(?:page/(\d+)/)?$#'   => fn ($m) => page_blog((int) ($m[1] ?? 1), '/post/category/blog/'),
    '#^/post/([a-z0-9-]+)/$#'                    => fn ($m) => page_post($m[1]),
    '#^/contact-houston-apartments/$#'           => fn () => page_contact(),
    '#^/api/search$#'                            => fn () => api_search(),
    '#^/api/lead$#'                              => fn () => api_lead(),
    '#^/robots\.txt$#'                           => fn () => robots(),
    '#^/(sitemap|sitemap_index|post-sitemap|page-sitemap|category-sitemap|apartment-sitemap)\.xml$#' => fn ($m) => sitemap($m[1]),
    '#^/admin/(sync|leads)/$#'                   => fn ($m) => admin($m[1]),
    '#^/([a-z0-9-]+)/$#'                         => fn ($m) => page_generic($m[1]),
];
foreach ($routes as $re => $handler) {
    if (preg_match($re, $path, $m)) {
        $handler($m);
        exit;
    }
}
not_found();

/* ---------------------------------------------------------------- pages */

function page_home(): void
{
    $stats = Listings::stats();
    $featured = Listings::featured(8);
    $posts = array_slice(content('posts'), 0, 3);
    render('home', compact('stats', 'featured', 'posts'), [
        'title'       => 'Houston Apartments for Rent | Free Apartment Locator – Houston Apartments',
        'description' => 'Search Houston apartments for rent on an interactive map. Draw your area, filter by price, beds and amenities, and get up to $500 back when you lease with Houston Apartments.',
        'canonical'   => '/',
        'body_class'  => 'home',
        'schema'      => schema_org_business(),
    ]);
}

function page_search(): void
{
    $areaKey = $_GET['area'] ?? '';
    $area = AREAS[$areaKey] ?? null;
    render('search', ['area' => $area, 'areaKey' => $area ? $areaKey : ''], [
        'title'       => ($area ? $area['name'] . ' ' : '') . 'Houston Apartments for Rent – Map Search | Houston Apartments',
        'description' => 'Search Houston apartments on a live map. Draw your own search area, filter by rent, bedrooms, pets and amenities, and compare floor plans side by side.',
        'canonical'   => '/apartments/',
        'body_class'  => 'search-page',
        'full'        => true,
    ]);
}

function page_property(string $slug): void
{
    $p = Listings::bySlug($slug);
    if (!$p) {
        not_found();
    }
    $nearby = Listings::nearby($p, 6);
    $areaKey = Listings::areaKeyFor($p);
    render('property', compact('p', 'nearby', 'areaKey'), [
        'title'       => $p['name'] . ' Apartments – ' . ($p['city'] ?: 'Houston') . ', TX ' . $p['zip'] . ' | Houston Apartments',
        'description' => Listings::metaDescription($p),
        'canonical'   => '/apartment/' . $p['slug'] . '/',
        'image'       => $p['photo'],
        'body_class'  => 'property-page',
        'schema'      => Listings::schema($p),
    ]);
}

function page_neighborhoods(): void
{
    $counts = Listings::areaCounts();
    render('neighborhoods', compact('counts'), [
        'title'       => 'Houston Apartments by Neighborhood | Houston Apartments',
        'description' => 'Explore Houston apartments by neighborhood – from the Heights, Montrose and Downtown to Katy, Sugar Land and The Woodlands.',
        'canonical'   => '/houston-apartments-neighborhoods/',
    ]);
}

function page_blog(int $page, string $base = '/houston-apartments-blog/'): void
{
    $all = content('posts');
    $per = 12;
    $pages = max(1, (int) ceil(count($all) / $per));
    if ($page < 1 || $page > $pages) {
        not_found();
    }
    $posts = array_slice($all, ($page - 1) * $per, $per);
    $meta = find_content('pages', '/houston-apartments-blog/');
    render('blog', compact('posts', 'page', 'pages', 'base'), [
        'title'       => 'Houston Apartments Blog – Guides, Reviews & Renter Tips' . ($page > 1 ? " – Page $page" : ''),
        'description' => $meta['description'] ?? 'Guides, reviews and renter tips from the Houston Apartments team.',
        'canonical'   => $base . ($page > 1 ? "page/$page/" : ''),
    ]);
}

function page_post(string $slug): void
{
    $post = find_content('posts', "/post/$slug/");
    if (!$post) {
        not_found();
    }
    $related = array_slice(array_values(array_filter(content('posts'), fn ($x) => $x['slug'] !== $slug)), 0, 3);
    $featured = Listings::featured(3);
    render('post', compact('post', 'related', 'featured'), [
        'title'       => $post['seo_title'] ?: $post['title'],
        'description' => $post['description'],
        'canonical'   => $post['path'],
        'image'       => $post['image'],
        'type'        => 'article',
        'schema'      => [
            '@context' => 'https://schema.org', '@type' => 'BlogPosting',
            'headline' => $post['title'], 'datePublished' => $post['date'], 'dateModified' => $post['modified'],
            'image' => $post['image'] ? site_url($post['image']) : null,
            'author' => ['@type' => 'Organization', 'name' => SITE['name']],
            'publisher' => ['@type' => 'Organization', 'name' => SITE['name'], 'logo' => ['@type' => 'ImageObject', 'url' => site_url('/assets/img/Houston-Apartments-Site-Logo.webp')]],
            'mainEntityOfPage' => site_url($post['path']),
        ],
    ]);
}

function page_contact(): void
{
    render('contact', [], [
        'title'       => 'Contact Houston Apartments | Free Apartment Locating',
        'description' => 'Tell us what you need and a Houston Apartments locator will send personalized listings – plus up to $500 back when you lease.',
        'canonical'   => '/contact-houston-apartments/',
    ]);
}

function page_generic(string $slug): void
{
    if (isset(AREAS[$slug])) {
        $area = AREAS[$slug] + ['slug' => $slug];
        $page = find_content('pages', "/$slug/");
        $listings = Listings::inArea($area, 24);
        render('area', compact('area', 'page', 'listings'), [
            'title'       => ($page['seo_title'] ?? '') ?: $area['name'] . ' Apartments for Rent | Houston Apartments',
            'description' => ($page['description'] ?? '') ?: "Browse {$area['name']} apartments for rent with Houston Apartments.",
            'canonical'   => "/$slug/",
            'image'       => $page['image'] ?? '',
        ]);
        return;
    }
    $page = find_content('pages', "/$slug/");
    if (!$page || $slug === 'home') {
        not_found();
    }
    render('page', compact('page'), [
        'title'       => $page['seo_title'] ?: $page['title'],
        'description' => $page['description'],
        'canonical'   => $page['path'],
        'image'       => $page['image'],
    ]);
}

/* ------------------------------------------------------------------ api */

function api_search(): void
{
    $res = Listings::search($_GET);
    header('Cache-Control: public, max-age=60');
    json_out($res);
}

function api_lead(): void
{
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        json_out(['ok' => false], 405);
        return;
    }
    $in = $_POST ?: (json_decode(file_get_contents('php://input'), true) ?? []);
    if (!empty($in['website'])) { // honeypot
        json_out(['ok' => true]);
        return;
    }
    $clean = fn ($k, $n = 190) => mb_substr(trim(strip_tags((string) ($in[$k] ?? ''))), 0, $n);
    $lead = [
        'created_at'  => gmdate('c'),
        'property_id' => ($pid = (int) ($in['property_id'] ?? 0)) ?: null,
        'name'        => $clean('name', 150),
        'email'       => $clean('email'),
        'phone'       => $clean('phone', 40),
        'move_in'     => $clean('move_in', 40),
        'beds'        => $clean('beds', 20),
        'budget'      => $clean('budget', 40),
        'message'     => $clean('message', 4000),
        'page'        => $clean('page', 255),
        'ip'          => mb_substr($_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '', 0, 64),
    ];
    if ($lead['name'] === '' || ($lead['phone'] === '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL))) {
        json_out(['ok' => false, 'error' => 'Please add your name and a phone number or email.'], 422);
        return;
    }
    try {
        db_migrate();
        $cols = array_keys($lead);
        db()->prepare('INSERT INTO leads (' . implode(',', $cols) . ') VALUES (' . implode(',', array_fill(0, count($cols), '?')) . ')')
            ->execute(array_values($lead));
    } catch (Throwable $e) {
        error_log('lead save failed: ' . $e->getMessage());
    }
    if ($to = config('lead_email')) {
        $body = '';
        foreach ($lead as $k => $v) {
            $body .= str_pad($k, 12) . ": $v\n";
        }
        @mail($to, 'New Houston Apartments lead: ' . $lead['name'], $body, 'From: no-reply@' . preg_replace('/^www\./', '', $_SERVER['HTTP_HOST'] ?? 'houstonapartments.com'));
    }
    json_out(['ok' => true]);
}

/* ------------------------------------------------------- seo / admin */

function robots(): void
{
    header('Content-Type: text/plain; charset=utf-8');
    if (!config('indexable')) {
        echo "User-agent: *\nDisallow: /\n";
        return;
    }
    echo "User-agent: *\nDisallow: /api/\nDisallow: /admin/\n\nSitemap: " . site_url('/sitemap_index.xml') . "\n";
}

function sitemap(string $which): void
{
    header('Content-Type: application/xml; charset=utf-8');
    $x = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    if ($which === 'sitemap' || $which === 'sitemap_index') {
        $x .= '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
        foreach (['page', 'post', 'category', 'apartment'] as $s) {
            $x .= '<sitemap><loc>' . e(site_url("/$s-sitemap.xml")) . '</loc></sitemap>';
        }
        echo $x . '</sitemapindex>';
        return;
    }
    $urls = [];
    if ($which === 'page-sitemap') {
        $urls[] = ['/', date('c')];
        $urls[] = ['/apartments/', date('c')];
        $urls[] = ['/houston-apartments-neighborhoods/', date('c')];
        foreach (content('pages') as $p) {
            if ($p['slug'] !== 'home') {
                $urls[] = [$p['path'], $p['modified']];
            }
        }
    } elseif ($which === 'post-sitemap') {
        foreach (content('posts') as $p) {
            $urls[] = [$p['path'], $p['modified']];
        }
    } elseif ($which === 'category-sitemap') {
        $urls[] = ['/post/category/blog/', content('posts')[0]['modified'] ?? date('c')];
    } else {
        foreach (Listings::allSlugs() as $r) {
            $urls[] = ['/apartment/' . $r['slug'] . '/', $r['synced_at']];
        }
    }
    $x .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    foreach ($urls as [$u, $mod]) {
        $x .= '<url><loc>' . e(site_url($u)) . '</loc><lastmod>' . e(date('c', strtotime($mod))) . '</lastmod></url>';
    }
    echo $x . '</urlset>';
}

function admin(string $what): void
{
    $key = config('admin_key');
    if (!$key || !hash_equals($key, (string) ($_GET['key'] ?? ''))) {
        not_found();
    }
    header('X-Robots-Tag: noindex');
    db_migrate();
    if ($what === 'sync') {
        require HA_APP . '/lib/Rise.php';
        set_time_limit(0);
        $imp = new RiseImporter();
        if (!empty($_GET['slugs'])) {
            $n = $imp->importSlugs(array_filter(explode(',', $_GET['slugs'])));
            $res = ['imported' => $n];
        } else {
            $res = $imp->sync((int) ($_GET['limit'] ?? 25), time() + 240);
        }
        json_out($res + ['log' => $imp->log]);
        return;
    }
    $rows = db()->query('SELECT l.*, p.name AS property FROM leads l LEFT JOIN properties p ON p.id = l.property_id ORDER BY l.id DESC LIMIT 500')->fetchAll();
    json_out($rows);
}

function schema_org_business(): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'RealEstateAgent',
        'name' => SITE['name'],
        'legalName' => SITE['legal'],
        'url' => site_url('/'),
        'logo' => site_url('/assets/img/Houston-Apartments-Site-Logo.webp'),
        'telephone' => SITE['phone_raw'],
        'foundingDate' => (string) SITE['founded'],
        'areaServed' => ['@type' => 'City', 'name' => 'Houston, TX'],
        'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Houston', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
        'sameAs' => ['https://www.instagram.com/riseapartmentshtx/'],
    ];
}
