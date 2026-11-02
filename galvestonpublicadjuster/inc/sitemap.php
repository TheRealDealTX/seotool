<?php
// Dynamic sitemap: static routes plus every published blog post.
//
// <lastmod> has to mean "the content changed on this date". File mtimes cannot provide that here:
// deploy.sh re-uploads every file, so mtime-based dates would claim the whole site changed on
// every deploy, and Google ignores lastmod once it sees that pattern. Static pages use the
// explicit dates in PAGE_UPDATED; pages that list runtime data move with their newest item.
header('Content-Type: application/xml; charset=utf-8');

$posts = blog_posts();
$latestPost = $posts ? max(array_column($posts, 'date')) : LAUNCH_DATE;

$status = weather_status();
$latestWeather = !empty($status['last_checked']) ? date('Y-m-d', strtotime($status['last_checked'])) : LAUNCH_DATE;
foreach (weather_events() as $ev) $latestWeather = max($latestWeather, $ev['detected'] ?? LAUNCH_DATE);

$today = date('Y-m-d');
$urls = [];
foreach (ROUTES as $p => $page) {
    if ($page === 'thank-you') continue;                       // noindex, and disallowed in robots.txt
    $d = PAGE_UPDATED[$page] ?? LAUNCH_DATE;
    if ($page === 'home' || $page === 'blog') $d = max($d, $latestPost);   // both list the newest posts
    if ($page === 'weather-events') $d = max($d, $latestWeather);
    $urls[] = [$p, min($d, $today)];
}
foreach ($posts as $post) $urls[] = ['/blog/' . $post['slug'] . '/', min($post['date'], $today)];

echo '<?xml version="1.0" encoding="UTF-8"?>', "\n", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', "\n";
foreach ($urls as [$p, $d]) echo '  <url><loc>', SITE_URL, e($p), '</loc><lastmod>', e($d), "</lastmod></url>\n";
echo "</urlset>\n";
