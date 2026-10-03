<?php
defined('TR_ROOT') || exit;
header('Content-Type: application/xml; charset=utf-8');
header('Cache-Control: public, max-age=3600');
$x = fn ($s) => htmlspecialchars((string) $s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
$launch = cfg('blog_launch_date');
$urls = [];
$add = function (string $path, string $lastmod, string $freq, string $prio) use (&$urls) {
    $urls[] = [abs_url($path), $lastmod, $freq, $prio];
};
$posts = posts();
$latest = $posts ? reset($posts)['date']->format('Y-m-d') : $launch;
$add('/', $latest, 'weekly', '1.0');
$add('/free-roof-inspection/', $launch, 'monthly', '0.9');
$add('/services/', $launch, 'monthly', '0.9');
foreach (services() as $s) {
    $add($s['url'], $launch, 'monthly', '0.8');
}
$add('/service-areas/', $launch, 'monthly', '0.8');
foreach (areas() as $a) {
    $add($a['url'], $launch, 'monthly', $a['slug'] === 'temple-tx' ? '0.8' : '0.7');
}
$add('/tools/', $launch, 'monthly', '0.7');
foreach (array_keys(catalog('tools')) as $slug) {
    $add('/tools/' . $slug . '/', $launch, 'monthly', '0.7');
}
$add('/weather/', tr_now()->format('Y-m-d'), 'hourly', '0.6');
$add('/blog/', $latest, 'weekly', '0.7');
foreach (array_unique(array_column($posts, 'category')) as $cat) {
    $add('/blog/category/' . $cat . '/', $latest, 'weekly', '0.4');
}
foreach ($posts as $p) {
    $add($p['url'], $p['date']->format('Y-m-d'), 'yearly', '0.6');
}
foreach (['/about/', '/contact/', '/sitemap/', '/privacy-policy/', '/terms-of-use/'] as $path) {
    $add($path, $launch, 'yearly', '0.3');
}
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$loc, $mod, $freq, $prio]) {
    echo "  <url><loc>{$x($loc)}</loc><lastmod>{$x($mod)}</lastmod><changefreq>{$freq}</changefreq><priority>{$prio}</priority></url>\n";
}
echo "</urlset>\n";
exit;
