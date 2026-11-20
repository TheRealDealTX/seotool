<?php defined('APP') || exit;

header('Content-Type: application/xml; charset=utf-8');
cache_public(3600);
$urls = [];
$add = function (string $path, ?string $lastmod = null, string $freq = 'weekly', string $prio = '0.6') use (&$urls) {
    $urls[] = [base_url($path), $lastmod, $freq, $prio];
};
$add('/', date('Y-m-d'), 'daily', '1.0');
$add('/sublets/', date('Y-m-d'), 'daily', '0.9');
$add('/post-a-sublet/', null, 'monthly', '0.8');
foreach (['pricing', 'safety', 'about', 'fair-housing', 'contact', 'terms', 'privacy', 'credits'] as $s) $add("/$s/", null, 'monthly', '0.3');
$add('/blog/', null, 'weekly', '0.7');
foreach (blog_posts() as $p) $add('/blog/' . $p['slug'] . '/', $p['updated'] ?? $p['date'], 'monthly', '0.6');
$add('/tools/', null, 'monthly', '0.6');
foreach (array_keys(tools_list()) as $t) $add("/tools/$t/", null, 'monthly', '0.5');

// Only cities with listings or real guide content (and states that contain them)
$states = [];
foreach (known_cities() as $k => $c) {
    [$st, $slug] = explode('/', $k);
    $states[$st] = true;
    $add(city_url($st, $slug), null, 'daily', $c['guide'] ? '0.8' : '0.6');
}
foreach (array_keys($states) as $st) $add(state_url($st), null, 'weekly', '0.6');
// filtered city pages that have at least one listing
foreach (cities_with_listings() as $k => $c) {
    [$st, $slug] = explode('/', $k);
    foreach (city_filters() as $fk => $fd) {
        if (listing_search(['state' => $st, 'city' => $slug] + $fd['where'], 1)['total'] > 0) $add(city_url($st, $slug) . $fk . '/', null, 'daily', '0.5');
    }
}
foreach (rows("SELECT id, slug, city_slug, state, updated_at FROM listings WHERE status = 'active' ORDER BY id DESC LIMIT 40000") as $l) {
    $add(listing_url($l), substr($l['updated_at'], 0, 10), 'weekly', '0.7');
}
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$loc, $mod, $freq, $prio]) {
    echo '<url><loc>' . e($loc) . '</loc>' . ($mod ? '<lastmod>' . e($mod) . '</lastmod>' : '') . '<changefreq>' . $freq . '</changefreq><priority>' . $prio . '</priority></url>' . "\n";
}
echo '</urlset>';
