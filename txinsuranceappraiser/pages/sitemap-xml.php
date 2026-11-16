<?php
/** XML sitemap built from the same data the router uses, so it can never drift. */
header('Content-Type: application/xml; charset=utf-8');
$today = date('Y-m-d', filemtime(ROOT . '/index.php'));
$urls = [];
$add = function (string $path, string $lastmod, string $freq, string $pri, string $img = '') use (&$urls) {
    $urls[] = [$path, $lastmod, $freq, $pri, $img];
};
$add('/', $today, 'weekly', '1.0', SITE['og_default']);
foreach (['/about-us/', '/what-is-an-appraisal/', '/services/', '/areas/', '/blog/', '/contact-us/', '/tools/'] as $p) {
    $add($p, $today, 'monthly', '0.8');
}
foreach (['appraisal', 'umpire', 'matterport', 'xactimate-estimate', 'symbility-estimate'] as $s) {
    $add('/services/' . $s . '/', $today, 'monthly', '0.9');
}
foreach (array_keys(TOOLS) as $t) {
    $add('/tools/' . $t . '/', $today, 'monthly', '0.7');
}
foreach (cities() as $c) {
    $add(city_url($c['slug']), $today, 'monthly', '0.7', city_image($c));
}
foreach (posts() as $p) {
    $add('/' . $p['slug'] . '/', substr($p['updated'] ?? $p['published'] ?? $today, 0, 10), 'monthly', '0.6', post_image($p));
}
foreach (['/privacy-policy/', '/terms-conditions/'] as $p) {
    $add($p, $today, 'yearly', '0.2');
}
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as [$p, $lm, $fq, $pr, $img]) {
    echo '<url><loc>' . e(abs_url($p)) . '</loc><lastmod>' . e($lm) . '</lastmod><changefreq>' . $fq . '</changefreq><priority>' . $pr . '</priority>';
    if ($img) {
        echo '<image:image><image:loc>' . e(abs_url($img)) . '</image:loc></image:image>';
    }
    echo "</url>\n";
}
echo '</urlset>';
