<?php
defined('SLT') || exit;

/** Static pages: path => [file, title, description, extra meta] */
const PAGES = [
    '/'                  => ['home',      'Spring Landscape Lighting | Landscape Lighting Design & Installation in Spring, TX', 'Spring Landscape Lighting designs, installs and repairs custom low-voltage LED landscape lighting for homes in Spring, TX, Klein and North Houston. Free lighting plan.'],
    '/about-us/'         => ['about',     'About Us | Spring Landscape Lighting', 'Meet Spring Landscape Lighting: a design-led outdoor lighting company for Spring, TX homes. How we plan, install and stand behind every system.'],
    '/services/'         => ['services',  'Landscape Lighting Services in Spring, TX | Spring Landscape Lighting', 'Architectural, pathway, tree, patio and pool lighting, smart controls, repairs and LED upgrades for homes in Spring, TX and North Houston.'],
    '/our-process/'      => ['process',   'Our Landscape Lighting Process | Spring Landscape Lighting', 'From consultation to the final nighttime adjustment: how Spring Landscape Lighting designs and installs a custom outdoor lighting system.'],
    '/faq/'              => ['faq',       'Landscape Lighting FAQ | Spring Landscape Lighting', 'Answers to common landscape lighting questions: cost, LED, low voltage, timers, repairs, installation, HOAs and maintenance in Spring, TX.'],
    '/service-areas/'    => ['areas',     'Service Areas | Landscape Lighting in Spring, Klein & North Houston', 'Spring Landscape Lighting serves Spring, Klein, Champion Forest, Gleannloch Farms, Augusta Pines, The Woodlands and nearby North Houston communities.'],
    '/tools/'            => ['tools',     'Free Landscape Lighting Tools & Calculators | Spring Landscape Lighting', 'Free landscape lighting tools: lighting visualizer, energy cost calculator, fixture estimator, transformer sizing, LED savings, color temperature and sunset timer planner.'],
    '/inspiration/'      => ['inspiration','Landscape Lighting Ideas & Inspiration | Spring Landscape Lighting', 'Landscape lighting ideas for Spring, TX homes: facades, entries, trees, paths, patios and pools, with the techniques behind each look.'],
    '/contact/'          => ['contact',   'Contact Us | Spring Landscape Lighting', 'Contact Spring Landscape Lighting in Spring, TX. Call (281) 704-7210 or send a message to schedule a complimentary lighting consultation.'],
    '/quote/'            => ['quote',     'Request a Free Landscape Lighting Quote | Spring Landscape Lighting', 'Request a complimentary landscape lighting consultation and quote from Spring Landscape Lighting for your home in Spring, TX or nearby communities.'],
    '/thank-you/'        => ['thanks',    'Thank You | Spring Landscape Lighting', 'Thanks for contacting Spring Landscape Lighting.', ['noindex' => true]],
    '/privacy-policy/'   => ['privacy',   'Privacy Policy | Spring Landscape Lighting', 'How Spring Landscape Lighting collects, uses and protects information submitted through springlandscapelighting.com.'],
    '/terms-of-service/' => ['terms',     'Terms of Service | Spring Landscape Lighting', 'The terms that govern use of springlandscapelighting.com and its free planning tools.'],
];

const REDIRECTS = [
    '/process/' => '/our-process/', '/services-2/' => '/services/', '/about/' => '/about-us/',
    '/contact-us/' => '/contact/', '/faqs/' => '/faq/', '/get-a-quote/' => '/quote/',
    '/sitemap.xml' => '/sitemap_index.xml', '/wp-sitemap.xml' => '/sitemap_index.xml',
    '/home/' => '/', '/index.php' => '/', '/comments/feed/' => '/feed/',
    '/category/uncategorized/' => '/blog/', '/tools/landscape-lighting-calculator/' => '/tools/energy-cost-calculator/',
];

function redirect(string $to, int $code = 301): void {
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

function render_file(string $file, array $meta): void {
    $GLOBALS['USES_TOOLS'] = false;
    ob_start();
    include APP . '/' . $file . '.php';
    $body = ob_get_clean();
    if (!empty($GLOBALS['USES_TOOLS'])) $meta['tools_js'] = true;
    header('Content-Type: text/html; charset=utf-8');
    if (!empty($meta['status'])) http_response_code($meta['status']);
    render_page($meta, $body);
    exit;
}

function not_found(): void {
    render_file('pages/404', ['title' => 'Page Not Found | ' . BRAND, 'desc' => 'This page could not be found.', 'path' => '/404/', 'noindex' => true, 'status' => 404]);
}

function route(string $path, string $qs): void {
    // Lead submissions.
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && in_array($path, ['/quote/', '/contact/'], true)) {
        require APP . '/lead.php';
        exit;
    }

    if (isset(REDIRECTS[$path])) redirect(REDIRECTS[$path] . $qs);
    if (preg_match('#^/(wp-json|feed/atom|author/[^/]+)(/|$)#', $path)) redirect('/');
    if (preg_match('#^/(tag)/[^/]+/?$#', $path)) redirect('/blog/');

    // XML endpoints.
    switch ($path) {
        case '/sitemap_index.xml': require APP . '/sitemaps.php'; sitemap_index(); exit;
        case '/page-sitemap.xml':  require APP . '/sitemaps.php'; sitemap_pages(); exit;
        case '/post-sitemap.xml':  require APP . '/sitemaps.php'; sitemap_posts(); exit;
        case '/category-sitemap.xml': require APP . '/sitemaps.php'; sitemap_categories(); exit;
        case '/feed/': case '/feed': require APP . '/sitemaps.php'; rss_feed(); exit;
    }

    // Trailing slash for page-style URLs.
    if ($path !== '/' && substr($path, -1) !== '/' && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) redirect($path . '/' . $qs);
    if (preg_match('#\.[a-z0-9]{2,5}$#i', $path)) not_found();

    if (isset(PAGES[$path])) {
        [$file, $title, $desc] = PAGES[$path];
        $extra = PAGES[$path][3] ?? [];
        render_file('pages/' . $file, ['title' => $title, 'desc' => $desc, 'path' => $path, 'body_class' => 'pg-' . $file] + $extra);
    }

    if (preg_match('#^/services/([a-z0-9-]+)/$#', $path, $m) && isset(SERVICES[$m[1]])) {
        $s = SERVICES[$m[1]];
        $GLOBALS['SLUG'] = $m[1];
        render_file('pages/service', ['title' => $s['title'], 'desc' => $s['desc'], 'path' => $path, 'body_class' => 'pg-service', 'page_type' => 'WebPage']);
    }
    if (preg_match('#^/service-areas/([a-z0-9-]+)/$#', $path, $m) && isset(AREAS[$m[1]])) {
        $a = AREAS[$m[1]];
        $GLOBALS['SLUG'] = $m[1];
        render_file('pages/area', ['title' => 'Landscape Lighting in ' . $a['name'] . ' | Spring Landscape Lighting',
            'desc' => 'Custom landscape lighting design, installation and repair in ' . $a['name'] . '. Architectural, path, tree and patio lighting by Spring Landscape Lighting.',
            'path' => $path, 'body_class' => 'pg-area']);
    }
    if (preg_match('#^/tools/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
        $t = TOOLS[$m[1]];
        $GLOBALS['SLUG'] = $m[1];
        render_file('pages/tool', ['title' => $t['title'], 'desc' => $t['meta'], 'path' => $path, 'body_class' => 'pg-tool']);
    }

    // Blog index + pagination.
    if (preg_match('#^/blog/page/(\d+)/$#', $path, $m)) {
        $GLOBALS['PAGE_N'] = (int)$m[1];
        if ($GLOBALS['PAGE_N'] < 2) redirect('/blog/');
        render_file('pages/blog', ['title' => 'Blog – Page ' . $m[1] . ' | ' . BRAND, 'desc' => PAGES_BLOG_DESC, 'path' => $path, 'body_class' => 'pg-blog']);
    }
    if ($path === '/blog/') {
        $GLOBALS['PAGE_N'] = 1;
        render_file('pages/blog', ['title' => 'Landscape Lighting Blog: Ideas, Guides & Tips | ' . BRAND, 'desc' => PAGES_BLOG_DESC, 'path' => $path, 'body_class' => 'pg-blog']);
    }
    if (preg_match('#^/category/([a-z0-9-]+)/(?:page/(\d+)/)?$#', $path, $m) && isset(CATEGORIES[$m[1]])) {
        $GLOBALS['CAT'] = $m[1];
        $GLOBALS['PAGE_N'] = (int)($m[2] ?? 1) ?: 1;
        $c = CATEGORIES[$m[1]];
        render_file('pages/blog', ['title' => $c['name'] . ' Articles | ' . BRAND . ' Blog', 'desc' => $c['desc'], 'path' => $path, 'body_class' => 'pg-blog']);
    }

    // Posts at the root (original WordPress permalink structure).
    if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && isset(POSTS[$m[1]])) {
        $p = POSTS[$m[1]];
        $GLOBALS['SLUG'] = $m[1];
        render_file('pages/post', ['title' => $p['seo'] . ' | ' . BRAND, 'og_title' => $p['seo'], 'desc' => $p['desc'], 'path' => $path,
            'image' => $p['img'], 'og_type' => 'article', 'published' => $p['date'], 'modified' => $p['updated'] ?? $p['date'],
            'body_class' => 'pg-post', 'page_type' => 'WebPage']);
    }

    not_found();
}

const PAGES_BLOG_DESC = 'Landscape lighting ideas, planning guides, cost advice and maintenance tips for homeowners in Spring, TX from Spring Landscape Lighting.';
