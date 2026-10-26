<?php defined('BO') || exit;
// XML sitemaps. sitemap.xml and the old Yoast URLs (sitemap_index.xml etc.) all resolve here.

function render_sitemap($name) {
    global $POSTS, $TOOLS;
    header('Content-Type: application/xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $sets = [
        'post-sitemap' => function () use ($POSTS) {
            $u = [['/blog/', max(array_column($POSTS, 'updated')), null]];
            foreach ($POSTS as $s => $p) $u[] = ['/' . $s . '/', $p['updated'], img_url($p['image'])];
            return $u;
        },
        'page-sitemap' => fn() => [
            ['/', '2026-10-26', img_url('Better-Outdoors-BG.webp')], ['/about-us/', '2026-10-26', null], ['/contact-us/', '2026-10-26', null],
            ['/privacy-policy/', '2026-10-26', null], ['/terms-of-use/', '2026-10-26', null],
        ],
        'category-sitemap' => fn() => [['/category/tips/', '2026-10-26', null]],
        'tool-sitemap' => function () use ($TOOLS) {
            $u = [['/tools/', '2026-10-26', null]];
            foreach ($TOOLS as $s => $_) $u[] = ['/tools/' . $s . '/', '2026-10-26', null];
            return $u;
        },
    ];
    if (!isset($sets[$name])) {
        echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
        foreach (array_keys($sets) as $k) echo "  <sitemap><loc>" . SITE_URL . "/{$k}.xml</loc><lastmod>2026-10-26</lastmod></sitemap>\n";
        echo '</sitemapindex>';
        return;
    }
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach ($sets[$name]() as [$loc, $mod, $img]) {
        echo '  <url><loc>' . SITE_URL . e($loc) . '</loc><lastmod>' . e($mod) . '</lastmod>';
        if ($img) echo '<image:image><image:loc>' . SITE_URL . e($img) . '</image:loc></image:image>';
        echo "</url>\n";
    }
    echo '</urlset>';
}
