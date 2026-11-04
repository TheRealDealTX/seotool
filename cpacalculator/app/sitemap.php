<?php
defined('CPA') or exit;
header('Content-Type: application/xml; charset=utf-8');
$pg = SITE_ROOT . '/app/pages';
$m = fn($f) => is_file($f) ? date('Y-m-d', filemtime($f)) : date('Y-m-d');
$urls = [['/', $m("$pg/home.php"), '1.0'], ['/calculators/', $m("$pg/calculators/index.php"), '0.9']];
foreach (TOOLS as $s => $_) $urls[] = [tool_url($s), $m("$pg/calculators/$s.php"), in_array($s, ['federal-income-tax', '1099-tax-calculator']) ? '0.9' : '0.8'];
foreach (SALARY_PAGES as $a) $urls[] = ["/calculators/federal-income-tax/$a/", $m("$pg/calculators/salary.php"), '0.6'];
$urls[] = ['/blog/', POSTS[live_posts()[0]][2], '0.7'];
$urls[] = ['/topic/guides/', $m("$pg/blog/index.php"), '0.4'];
foreach (live_posts() as $s) $urls[] = [post_url($s), POSTS[$s][2], '0.7'];
foreach (['about-us', 'our-methodology', 'contact', 'disclaimer', 'privacy-policy', 'terms-of-use'] as $s) $urls[] = ["/$s/", $m("$pg/$s.php"), '0.3'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as [$u, $d, $p]) echo "  <url><loc>" . SITE_ORIGIN . "$u</loc><lastmod>$d</lastmod><priority>$p</priority></url>\n";
echo "</urlset>\n";
