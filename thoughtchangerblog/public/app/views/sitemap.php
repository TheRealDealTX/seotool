<?php
/** @var string $which index|post|page|category — same filenames Yoast used, so Search Console keeps working. */
header('Content-Type: application/xml; charset=UTF-8');
header('X-Robots-Tag: noindex, follow');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
$lastPost = max(array_map(fn($p) => $p['modified'] ?: $p['published'], posts()));
$w3 = fn($iso) => date('c', strtotime($iso));
if ($which === 'index'): ?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc><?= SITE_URL ?>/post-sitemap.xml</loc><lastmod><?= $w3($lastPost) ?></lastmod></sitemap>
<sitemap><loc><?= SITE_URL ?>/page-sitemap.xml</loc><lastmod><?= $w3($lastPost) ?></lastmod></sitemap>
<sitemap><loc><?= SITE_URL ?>/category-sitemap.xml</loc><lastmod><?= $w3($lastPost) ?></lastmod></sitemap>
</sitemapindex>
<?php elseif ($which === 'post'): ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
<url><loc><?= SITE_URL ?>/blog/</loc><lastmod><?= $w3($lastPost) ?></lastmod></url>
<?php foreach (posts() as $p): ?>
<url><loc><?= SITE_URL ?>/<?= e($p['slug']) ?>/</loc><lastmod><?= $w3($p['modified'] ?: $p['published']) ?></lastmod><image:image><image:loc><?= SITE_URL . e($p['image']) ?></image:loc></image:image></url>
<?php endforeach; ?>
</urlset>
<?php elseif ($which === 'page'): ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<?php foreach (['/' => $lastPost, '/about-us/' => '2026-11-19', '/contact-us/' => '2026-11-19', '/quotes/' => $lastPost, '/mindset/' => $lastPost,
                '/recommended-reads/' => $lastPost, '/privacy-policy/' => '2026-11-19', '/terms-of-use/' => '2026-01-24', '/affiliate-disclosure/' => '2026-11-19'] as $u => $d): ?>
<url><loc><?= SITE_URL . $u ?></loc><lastmod><?= $w3($d) ?></lastmod></url>
<?php endforeach; ?>
</urlset>
<?php else: ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc><?= SITE_URL ?>/category/general/</loc><lastmod><?= $w3($lastPost) ?></lastmod></url>
</urlset>
<?php endif;
