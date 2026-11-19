<?php
/* Content validator: php validate.php  (exit 1 on errors) */
const NHS = true;
define('APP_ROOT', __DIR__);
require 'inc/config.php'; require 'inc/functions.php'; require 'inc/products.php'; require 'inc/views.php';
$err = []; $warn = [];
$slugs = post_slugs();
$pages = array_map(fn($f) => basename($f, '.php'), glob('content/pages/*.php'));
$valid = array_merge(['', 'blog', 'free-training', 'our-products', 'author/jonathon', 'feed', 'sitemap.xml'], $slugs, $pages, array_map(fn($c) => "category/$c", array_keys(CATEGORIES)));
$titles = []; $descs = [];
$keys = array_keys(products());
foreach ($slugs as $s) {
    $p = get_post($s);
    foreach (['title','seo_title','description','keyword','category','date','updated','excerpt','body','faq'] as $k) if (empty($p[$k])) $err[] = "$s: missing $k";
    if (!isset(CATEGORIES[$p['category'] ?? ''])) $err[] = "$s: bad category {$p['category']}";
    $tl = mb_strlen($p['seo_title'] ?? ''); if ($tl > 65 || $tl < 30) $warn[] = "$s: seo_title length $tl";
    $dl = mb_strlen($p['description'] ?? ''); if ($dl > 145) $err[] = "$s: description $dl chars (max 145)"; elseif ($dl < 110) $warn[] = "$s: description only $dl chars";
    if (isset($titles[$p['seo_title']])) $err[] = "$s: duplicate seo_title"; $titles[$p['seo_title']] = 1;
    if (isset($descs[$p['description']])) $err[] = "$s: duplicate description"; $descs[$p['description']] = 1;
    $b = $p['body'];
    if (preg_match('/<h1/i', $b)) $err[] = "$s: h1 in body";
    if (preg_match('#amazon\.com|amzn\.to#i', $b)) $err[] = "$s: raw amazon link";
    preg_match_all('/<!--products?:([a-z0-9_,\s]+)/', $b, $m1); preg_match_all('/\[\[amz:([a-z0-9_]+)\|/', $b, $m2);
    foreach (array_merge(...array_map(fn($x) => array_map('trim', explode(',', $x)), $m1[1] ?: [''])) as $k) if ($k !== '' && !in_array($k, $keys)) $err[] = "$s: unknown product $k";
    foreach ($m2[1] as $k) if (!in_array($k, $keys)) $err[] = "$s: unknown product $k";
    preg_match_all('/href="(\/[^"#?]*)/', $b, $m);
    foreach ($m[1] as $h) { $t = trim($h, '/'); if (!in_array($t, $valid)) $err[] = "$s: broken internal link $h"; }
    if (preg_match('/utm_source|gclid|gad_source/', $b)) $err[] = "$s: tracking params left in links";
    $wc = str_word_count(strip_tags($b)); if ($wc < 750) $warn[] = "$s: only $wc words";
}
foreach ($pages as $s) { $p = get_page($s); preg_match_all('/href="(\/[^"#?]*)/', $p['body'], $m); foreach ($m[1] as $h) { $t = trim($h, '/'); if (!in_array($t, $valid)) $err[] = "page $s: broken internal link $h"; } }
$missing = array_diff($keys, array_keys(is_file('data/asins.php') ? require 'data/asins.php' : []));
if ($missing) $warn[] = count($missing) . ' products have no ASIN (fall back to Amazon search links): ' . implode(', ', $missing);
foreach ($warn as $w) echo "WARN  $w\n";
foreach ($err as $e) echo "ERROR $e\n";
echo count($slugs) . " posts, " . count($pages) . " pages, " . count($err) . " errors, " . count($warn) . " warnings\n";
exit($err ? 1 : 0);
