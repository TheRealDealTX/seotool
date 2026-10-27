<?php
// Front controller. Existing files are served directly by the web server;
// every other request lands here (the host routes misses to index.php and
// ignores .htaccess, so all redirects live in this file).
require __DIR__ . '/app/bootstrap.php';
require HA_APP . '/lib/Listings.php';
require HA_APP . '/lib/Filters.php';
require HA_APP . '/tools.php';

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

// Canonical scheme (TLS terminates upstream) and bare domain (www → houstonapartments.com)
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if (config('live_host') && $host === 'www.' . config('live_host')) {
    redirect('https://' . config('live_host') . $uri);
}
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http') {
    redirect('https://' . $host . $uri);
}

// Old WordPress plumbing → nearest equivalent
if (preg_match('#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(feed|comments/feed|post/feed)/?$#', $path) || preg_match('#^/post/[^/]+/feed/?$#', $path)) {
    redirect('/houston-apartments-blog/');
}
if (preg_match('#^/wp-content/uploads/.*Houston-Apartments-(Site-)?Logo#', $path)) {
    redirect('/assets/img/logo.png');
}
if (preg_match('#^/(author|tag)/#', $path)) {
    redirect('/houston-apartments-blog/');
}
if ($path === '/apartment') {
    redirect('/apartments/');
}
if ($path === '/home/' || $path === '/index.php') {
    redirect('/');
}

// Trailing slash for page URLs (WordPress style)
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.\w{2,12}$#', $path) && !str_starts_with($path, '/api/')) {
    redirect($path . '/' . (($q = parse_url($uri, PHP_URL_QUERY)) ? "?$q" : ''));
}

$routes = [
    '#^/$#'                                      => fn () => page_home(),
    '#^/apartments/$#'                           => fn () => page_search([]),
    '#^/apartments/([a-z0-9-]+)/(?:([a-z0-9-]+)/)?$#' => fn ($m) => page_search(array_values(array_filter([$m[1], $m[2] ?? '']))),
    '#^/apartment/$#'                            => fn () => redirect('/apartments/'),
    '#^/apartment/([a-z0-9-]+)/$#'               => fn ($m) => page_property($m[1]),
    '#^/houston-apartments-neighborhoods/$#'     => fn () => page_neighborhoods(),
    '#^/houston-apartments-blog/(?:page/(\d+)/)?$#' => fn ($m) => page_blog((int) ($m[1] ?? 1)),
    '#^/post/category/blog/(?:page/(\d+)/)?$#'   => fn ($m) => page_blog((int) ($m[1] ?? 1), '/post/category/blog/'),
    '#^/post/([a-z0-9-]+)/$#'                    => fn ($m) => page_post($m[1]),
    '#^/contact-houston-apartments/$#'           => fn () => page_contact(),
    '#^/houston-apartment-tools/$#'              => fn () => page_tools(),
    '#^/houston-apartment-tools/([a-z0-9-]+)/$#' => fn ($m) => page_tool($m[1]),
    '#^/api/geocode$#'                           => fn () => api_geocode(),
    '#^/api/search$#'                            => fn () => api_search(),
    '#^/api/lead$#'                              => fn () => api_lead(),
    '#^/robots\.txt$#'                           => fn () => robots(),
    '#^/site\.webmanifest$#'                     => function () {
        header('Content-Type: application/manifest+json; charset=utf-8');
        header('Cache-Control: public, max-age=86400');
        readfile(HA_APP . '/site.webmanifest.json');
    },
    '#^/(sitemap|sitemap_index|post-sitemap|page-sitemap|category-sitemap|apartment-sitemap|search-sitemap)\.xml$#' => fn ($m) => sitemap($m[1]),
    '#^/admin(/.*)?$#'                           => function () use ($path) { require HA_APP . '/admin.php'; admin_route($path); },
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
    $posts = array_slice(content('posts'), 0, 12);
    render('home', compact('stats', 'featured', 'posts'), [
        'title'       => 'Houston Apartments for Rent | Free Apartment Locator – Houston Apartments',
        'description' => 'Search Houston apartments for rent on an interactive map. Draw your area, filter by price, beds and amenities, and get up to $500 back when you lease with Houston Apartments.',
        'canonical'   => '/',
        'body_class'  => 'home',
        'schema'      => schema_org_business(),
    ]);
}

function page_search(array $segments): void
{
    $state = [];
    if ($segments) {
        $state = Filters::parse($segments);
        if ($state === null) {
            not_found();
        }
    }
    $state = Filters::normalize(array_merge($state, $_GET));
    $canonical = Filters::url($state);
    $requested = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
    $q = array_intersect_key($_GET, array_flip(Filters::knownKeys()));   // utm_* etc. are ignored
    ksort($q);
    if (!same_query($canonical, $requested, $q)) {
        redirect($canonical);
    }
    $res = Listings::search($state + ['per' => 24]);
    $desc = Filters::describe($state);
    $area = isset($state['area']) ? AREAS[$state['area']] : null;
    $index = Filters::indexable($state, $res['total']);
    $onlyArea = $area && count($state) === 1;
    $page = (int) ($state['page'] ?? 1);
    render('search', compact('state', 'res', 'desc', 'area'), [
        'title'       => $desc['h1'] . ($page > 1 ? " – Page $page" : '') . ' | Houston Apartments',
        'description' => search_description($desc, $res['total']),
        'canonical'   => $onlyArea ? '/' . $state['area'] . '/' : Filters::url($state, false) . ($page > 1 ? "?page=$page" : ''),
        'noindex'     => !$index,
        'body_class'  => 'search-page',
        'full'        => true,
        'schema'      => search_schema($desc, $res),
    ]);
}

/** Same URL apart from query-string ordering. */
function same_query(string $canonical, string $path, array $q): bool
{
    [$cp, $cq] = array_pad(explode('?', $canonical, 2), 2, '');
    parse_str($cq, $cqa);
    ksort($cqa);
    return $cp === $path && $cqa == $q;
}

function search_description(array $d, int $total): string
{
    $what = $d['noun'] . ' for rent in ' . $d['place'] . $d['tail'] . ($d['price'] ? ' (' . $d['price'] . ')' : '');
    $n = $total ? 'Compare ' . number_format($total) . ' communit' . ($total === 1 ? 'y' : 'ies') . ' with' : 'See';
    return mb_substr("$what: $n photos, floor plans and amenities on a live map, draw your own search area, and get up to \$" . SITE['cashback'] . ' back when you lease with Houston Apartments.', 0, 300);
}

function lcfirst_safe(string $s): string
{
    return strtolower($s);
}

function search_schema(array $d, array $res): array
{
    return [
        '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => $d['h1'],
        'numberOfItems' => $res['total'],
        'itemListElement' => array_map(fn ($c, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => site_url($c['url']), 'name' => $c['name']],
            $res['items'], array_keys($res['items'])),
    ];
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
        'canonical'   => listing_url($p['slug']),
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
    $related = array_slice(array_values(array_filter(content('posts'), fn ($x) => $x['slug'] !== $slug)), 0, 12);
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
            'author' => founder_schema(),
            'publisher' => ['@type' => 'Organization', 'name' => SITE['name'], 'logo' => ['@type' => 'ImageObject', 'url' => site_url('/assets/img/logo.png')]],
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

function page_tools(): void
{
    render('tools-hub', [], [
        'title'       => 'Free Renter Tools & Calculators for Houston Apartments | Houston Apartments',
        'description' => 'Free tools for Houston renters: rent affordability and move-in cost calculators, roommate rent split, true-cost apartment comparison, commute finder and checklists.',
        'canonical'   => TOOLS_BASE,
        'schema'      => ['@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'Houston renter tools',
            'itemListElement' => array_map(fn ($k, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => site_url(TOOLS_BASE . $k . '/'), 'name' => TOOLS[$k]['name']],
                array_keys(TOOLS), array_keys(array_keys(TOOLS)))],
    ]);
}

function page_tool(string $slug): void
{
    $tool = TOOLS[$slug] ?? null;
    if (!$tool) {
        not_found();
    }
    render('tool', compact('tool', 'slug'), [
        'title'       => $tool['h1'] . ' | Houston Apartments',
        'description' => $tool['meta'],
        'canonical'   => TOOLS_BASE . $slug . '/',
        'map'         => $slug === 'commute-apartment-finder',
        'scripts'     => ['js/tools.js'],
        'schema'      => [
            ['@context' => 'https://schema.org', '@type' => 'WebApplication', 'name' => $tool['name'], 'applicationCategory' => 'FinanceApplication',
             'operatingSystem' => 'Any', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'url' => site_url(TOOLS_BASE . $slug . '/'),
             'publisher' => ['@type' => 'Organization', 'name' => SITE['name']]],
            ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map(fn ($f) => ['@type' => 'Question', 'name' => $f[0],
             'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f[1]]], $tool['faqs'])],
        ],
    ]);
}

/** Public geocoder for the commute tool (US Census, cached; Houston-area results only). */
function api_geocode(): void
{
    require_once HA_APP . '/lib/Rise.php';
    $q = mb_substr(trim((string) ($_GET['q'] ?? '')), 0, 160);
    if (strlen($q) < 4) {
        json_out(['lat' => null, 'lng' => null], 422);
        return;
    }
    db_migrate();
    [$lat, $lng] = Geocoder::locate($q);
    // Keep to greater Houston so the endpoint isn't a general-purpose geocoder
    if ($lat === null || abs($lat - 29.76) > 1.2 || abs($lng + 95.37) > 1.4) {
        json_out(['lat' => null, 'lng' => null]);
        return;
    }
    header('Cache-Control: public, max-age=86400');
    json_out(['lat' => $lat, 'lng' => $lng]);
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
        'schema'      => $slug === 'about-houston-apartments' ? ['@context' => 'https://schema.org'] + founder_schema() : [],
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
    $state = Filters::normalize($_GET);
    unset($state['page']);
    $d = Filters::describe($state);
    $page = max(1, (int) ($_GET['page'] ?? 1));
    $res['url'] = Filters::url($state + ($page > 1 ? ['page' => $page] : []));
    $res['h1'] = $d['h1'];
    $res['title'] = $d['h1'] . ' | Houston Apartments';
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
    if (preg_match('/^\d{4}-\d{2}-\d{2}$/', $lead['move_in']) && ($t = strtotime($lead['move_in']))) {
        $lead['move_in'] = date('M j, Y', $t);
    }
    if ($lead['budget'] !== '' && ($b = (int) preg_replace('/\D/', '', $lead['budget']))) {
        $lead['budget'] = '$' . number_format($b);
    }
    if ($lead['name'] === '') {
        json_out(['ok' => false, 'error' => 'Please add your name.'], 422);
        return;
    }
    $phone = us_phone($lead['phone']);
    if ($phone === null) {
        json_out(['ok' => false, 'error' => 'Please enter a valid US phone number.'], 422);
        return;
    }
    $lead['phone'] = $phone;
    if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
        json_out(['ok' => false, 'error' => 'Please enter a valid email address.'], 422);
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
        $property = '';
        if ($lead['property_id']) {
            $st = db()->prepare('SELECT name, slug FROM properties WHERE id = ?');
            $st->execute([$lead['property_id']]);
            $property = ($r = $st->fetch()) ? $r['name'] . ' – ' . site_url(listing_url($r['slug'])) : '';
        }
        lead_email($to, $lead, $property);
    }
    json_out(['ok' => true]);
}

/** Notification for a new lead. Reply-To is the renter, so "Reply" answers them directly. */
function lead_email(string $to, array $lead, string $property = ''): bool
{
    require_once HA_APP . '/lib/Mailer.php';
    $rows = array_filter([
        'Name' => $lead['name'], 'Phone' => $lead['phone'], 'Email' => $lead['email'], 'Property' => $property,
        'Move-in' => $lead['move_in'], 'Bedrooms' => $lead['beds'], 'Budget' => $lead['budget'],
        'Message' => $lead['message'], 'Page' => $lead['page'] ? site_url($lead['page']) : '', 'Received' => date('M j, Y g:i a T'),
    ]);
    $text = "New request from houstonapartments.com\n\n";
    $html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#10272b"><h2 style="margin:0 0 12px;color:#0f766e">New apartment request</h2><table cellpadding="6" style="border-collapse:collapse">';
    foreach ($rows as $k => $v) {
        $text .= str_pad($k . ':', 11) . $v . "\n";
        $val = e($v);
        if ($k === 'Phone') {
            $val = '<a href="tel:' . e(preg_replace('/[^\d+]/', '', $v)) . '">' . $val . '</a>';
        } elseif ($k === 'Email') {
            $val = '<a href="mailto:' . $val . '">' . $val . '</a>';
        }
        $html .= '<tr><td style="color:#66797d;vertical-align:top"><b>' . e($k) . '</b></td><td>' . nl2br($val) . '</td></tr>';
    }
    $text .= "\nManage leads: " . site_url('/admin/leads/') . "\n";
    $html .= '</table><p><a href="' . e(site_url('/admin/leads/')) . '" style="background:#0f766e;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none">Open leads in admin</a></p></div>';
    return Mailer::send($to, 'New lead: ' . $lead['name'] . ($property ? ' – ' . strtok($property, '–') : ''), $text, $lead['email'], $html);
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
        foreach (['page', 'post', 'category', 'apartment', 'search'] as $s) {
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
        $urls[] = [TOOLS_BASE, date('c')];
        foreach (array_keys(TOOLS) as $k) {
            $urls[] = [TOOLS_BASE . $k . '/', date('c')];
        }
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
    } elseif ($which === 'search-sitemap') {
        $seen = [];
        foreach (array_merge([null], array_keys(AREAS)) as $area) {
            foreach (Filters::popular($area) as $state) {
                $u = Filters::url($state, false);
                if (isset($seen[$u])) {
                    continue;
                }
                $seen[$u] = true;
                if (Listings::search($state + ['per' => 6])['total'] > 0) {
                    $urls[] = [$u, date('c')];
                }
            }
        }
    } else {
        foreach (Listings::allSlugs() as $r) {
            $urls[] = [listing_url($r['slug']), $r['synced_at']];
        }
    }
    $x .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    foreach ($urls as [$u, $mod]) {
        $x .= '<url><loc>' . e(site_url($u)) . '</loc><lastmod>' . e(date('c', strtotime($mod))) . '</lastmod></url>';
    }
    echo $x . '</urlset>';
}

function founder_schema(): array
{
    return ['@type' => 'Person', 'name' => FOUNDER['name'], 'jobTitle' => FOUNDER['title'],
            'image' => site_url(FOUNDER['photo']), 'url' => site_url('/about-houston-apartments/#joseph-dittman'),
            'worksFor' => ['@type' => 'RealEstateAgent', 'name' => SITE['name'], 'url' => site_url('/')]];
}

function schema_org_business(): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'RealEstateAgent',
        'name' => SITE['name'],
        'legalName' => SITE['legal'],
        'url' => site_url('/'),
        'logo' => site_url('/assets/img/logo.png'),
        'telephone' => SITE['phone_raw'],
        'email' => SITE['email'],
        'foundingDate' => (string) SITE['founded'],
        'areaServed' => ['@type' => 'City', 'name' => 'Houston, TX'],
        'founder' => founder_schema(),
        'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Houston', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
    ];
}
