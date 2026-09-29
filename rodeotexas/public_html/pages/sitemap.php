<?php
/** XML sitemaps: /sitemap.xml (index) and /sitemap-{pages|events|articles}.xml */
defined('RT_APP') || exit;

use RT\Db;

header('Content-Type: application/xml; charset=utf-8');
header('Cache-Control: public, max-age=3600');
$xml = static fn($s) => htmlspecialchars((string) $s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

if ($part === 'index') {
    $lastEvent = (string) Db::val("SELECT MAX(updated_at) FROM events WHERE publish_state = 'published'");
    $lastArticle = (string) Db::val("SELECT MAX(updated_at) FROM articles WHERE status = 'published'");
    echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (['pages' => $lastEvent, 'events' => $lastEvent, 'articles' => $lastArticle] as $p => $mod) {
        echo '<sitemap><loc>' . $xml(abs_url('/sitemap-' . $p . '.xml')) . '</loc>' . ($mod ? '<lastmod>' . gmdate('c', strtotime($mod . ' UTC')) . '</lastmod>' : '') . "</sitemap>\n";
    }
    echo '</sitemapindex>';
    exit;
}

echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
$url = static function (string $loc, ?string $mod = null) use ($xml): void {
    echo '<url><loc>' . $xml(abs_url($loc)) . '</loc>' . ($mod ? '<lastmod>' . gmdate('c', strtotime($mod . ' UTC')) . '</lastmod>' : '') . "</url>\n";
};
if ($part === 'pages') {
    foreach (['/', '/rodeos/', '/past-events/', '/blog/', '/about/', '/contact/', '/submit-event/', '/privacy-policy/'] as $p) {
        $url($p);
    }
    foreach (Db::all('SELECT slug FROM regions ORDER BY sort') as $r) {
        $url('/rodeos/region/' . $r['slug'] . '/');
    }
    foreach (Db::all("SELECT DISTINCT a.slug FROM associations a JOIN events e ON e.association_id = a.id AND e.publish_state = 'published' AND e.is_legacy = 0") as $r) {
        $url('/rodeos/association/' . $r['slug'] . '/');
    }
    foreach (Db::all("SELECT DISTINCT t.slug FROM event_types t JOIN events e ON e.event_type_id = t.id AND e.publish_state = 'published' AND e.is_legacy = 0") as $r) {
        $url('/rodeos/type/' . $r['slug'] . '/');
    }
    foreach (Db::all("SELECT DISTINCT c.slug FROM categories c JOIN article_categories ac ON ac.category_id = c.id") as $r) {
        $url('/category/' . $r['slug'] . '/');
    }
} elseif ($part === 'events') {
    // Legacy (unverified) and archived pages are noindex, so they are left out.
    foreach (Db::all("SELECT slug, updated_at FROM events WHERE publish_state = 'published' AND is_legacy = 0 ORDER BY start_date DESC LIMIT 45000") as $r) {
        $url('/rodeos/' . $r['slug'] . '/', $r['updated_at']);
    }
} else {
    foreach (Db::all("SELECT slug, updated_at FROM articles WHERE status = 'published' ORDER BY published_at DESC") as $r) {
        $url('/' . $r['slug'] . '/', $r['updated_at']);
    }
}
echo '</urlset>';
