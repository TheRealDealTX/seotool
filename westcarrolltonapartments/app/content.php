<?php defined('WCA') || exit;

function posts_all(): array
{
    static $posts = null;
    if ($posts !== null) return $posts;
    $posts = [];
    foreach (glob(ROOT_DIR . '/content/posts/*.php') as $f) {
        $p = include $f;
        if (is_array($p) && !empty($p['slug'])) $posts[$p['slug']] = $p;
    }
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']) ?: strcmp($a['title'], $b['title']));
    return $posts;
}

function post_by_slug(string $slug): ?array
{
    return posts_all()[$slug] ?? null;
}

function post_categories(): array
{
    return ['renter-tips' => 'Renter Tips', 'budgeting' => 'Budgeting', 'moving' => 'Moving', 'home-decor' => 'Home & Decor', 'local-guide' => 'Local Guide'];
}

function category_slug(string $name): string
{
    return array_search($name, post_categories(), true) ?: 'renter-tips';
}

/** Render the post body, swapping the <!--products--> marker for an Amazon product box. */
function post_body_html(array $p): string
{
    $box = '';
    if (!empty($p['products'])) {
        ob_start();
        partial('partials/products', ['products' => $p['products'], 'heading' => 'Products we recommend for this']);
        $box = ob_get_clean();
    }
    $body = $p['body'];
    if (str_contains($body, '<!--products-->')) return str_replace('<!--products-->', $box, $body);
    return $body . $box;
}

/** Old WordPress URLs -> new URLs (301). */
function legacy_redirects(): array
{
    $map = [
        '/about-us/' => '/about/',
        '/contact-us/' => '/contact/',
        '/meet-our-team/' => '/about/',
        '/write-for-us/' => '/contact/',
        '/newsletter/' => '/blog/',
        '/author/derrick/' => '/blog/',
        '/category/apartment-therapy/' => '/blog/category/home-decor/',
        '/category/style/' => '/blog/category/home-decor/',
        '/category/home-projects/' => '/blog/category/home-decor/',
        '/category/organize-clean/' => '/blog/category/home-decor/',
        '/category/best-deals/' => '/apartments/under-1000/',
        '/category/living/' => '/blog/category/renter-tips/',
        '/category/tours/' => '/apartments/',
        '/category/uncategorized/' => '/blog/',
        '/tag/apartments/' => '/apartments/',
        '/tag/resources-for-renters/' => '/blog/category/renter-tips/',
        '/tag/living/' => '/blog/category/renter-tips/',
        '/tag/houses/' => '/blog/apartment-vs-house-west-carrollton/',
        '/tag/first-time-home-buyers/' => '/blog/apartment-vs-house-west-carrollton/',
        '/tag/home-financing/' => '/blog/apartment-budget-guide/',
        '/tag/home-security/' => '/blog/renter-maintenance-checklist/',
        '/sitemap_index.xml' => '/sitemap.xml',
        '/wp-sitemap.xml' => '/sitemap.xml',
        '/page-sitemap.xml' => '/sitemap.xml',
        '/post-sitemap.xml' => '/sitemap.xml',
        '/category-sitemap.xml' => '/sitemap.xml',
        '/post_tag-sitemap.xml' => '/sitemap.xml',
        '/feed/' => '/blog/',
        '/apartments-for-rent/' => '/apartments/',
    ];
    foreach (posts_all() as $p) {
        foreach ($p['old_urls'] ?? [] as $old) $map[$old] = '/blog/' . $p['slug'] . '/';
    }
    return $map;
}

/** Old URLs unrelated to a West Carrollton directory: 410 Gone so search engines drop them. */
function legacy_gone(): array
{
    return [
        '/422-2/', '/418-2/', '/houston-culture-and-homes/', '/tag/houston/',
        '/the-top-neighborhoods-for-apartment-living-in-austin-texas/',
        '/the-evolving-rental-market-in-san-antonio-texas-what-to-expect-in-2023/',
        '/the-pros-and-cons-of-living-in-a-luxury-apartment-in-dallas-texas/',
        '/discover-high-rise-apartments-in-houston-luxury-living-elevated/',
        '/avasa-spring-branch-apartments-the-perfect-urban-living-experience-in-houston-tx/',
        '/welcome-to-pearl-rosemont-apartments-modern-living-in-houstons-montrose-district/',
        '/live-large-uncover-the-best-apartments-in-katy-tx/',
        '/modern-comforts-7-must-see-2-bedroom-apartments-in-houston-tx/',
        '/feature-packed-living-cypress-apartments-with-exceptional-in-unit-perks/',
        '/why-cypress-tx-is-a-fantastic-place-to-call-home/',
        '/xactimate-for-beginners-tips-for-getting-accurate-estimates-every-time/',
    ];
}
