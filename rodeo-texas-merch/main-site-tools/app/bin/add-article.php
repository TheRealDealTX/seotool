<?php
/**
 * Add one article from a JSON file (same format as an entry in app/data/articles.json).
 *
 *   php app/bin/add-article.php app/data/article-<slug>.json            add (skips if the slug exists)
 *   php app/bin/add-article.php app/data/article-<slug>.json --update   replace that article's text fields
 *
 * Command line only. Without --update it never duplicates or overwrites anything edited in the admin.
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}

require_once dirname(__DIR__) . '/bootstrap.php';

use RT\Db;

$file = $argv[1] ?? '';
$a = json_decode((string) @file_get_contents($file), true);
if (!is_array($a) || empty($a['slug']) || empty($a['title']) || empty($a['content_html'])) {
    fwrite(STDERR, "Usage: php app/bin/add-article.php <article.json>\n");
    exit(1);
}
$now = now_utc();
$existing = Db::val('SELECT id FROM articles WHERE slug = ?', [$a['slug']]);
if ($existing && in_array('--update', $argv, true)) {
    Db::update('articles', [
        'title' => $a['title'], 'seo_title' => $a['seo_title'] ?? $a['title'],
        'meta_description' => $a['meta_description'] ?? null, 'excerpt' => $a['excerpt'] ?? null, 'content_html' => $a['content_html'],
        'featured_image' => $a['featured_image'] ?? null, 'featured_alt' => $a['featured_alt'] ?? null,
        'featured_width' => $a['featured_width'] ?? null, 'featured_height' => $a['featured_height'] ?? null, 'updated_at' => $now,
    ], 'id = :id', ['id' => $existing]);
    echo "Updated: /{$a['slug']}/ (id {$existing})\n";
    exit(0);
}
if ($existing) {
    echo "Skipped: /{$a['slug']}/ already exists\n";
    exit(0);
}
$id = Db::insert('articles', [
    'slug' => $a['slug'], 'title' => $a['title'], 'seo_title' => $a['seo_title'] ?? $a['title'],
    'meta_description' => $a['meta_description'] ?? null, 'excerpt' => $a['excerpt'] ?? null, 'content_html' => $a['content_html'],
    'featured_image' => $a['featured_image'] ?? null, 'featured_alt' => $a['featured_alt'] ?? null,
    'featured_width' => $a['featured_width'] ?? null, 'featured_height' => $a['featured_height'] ?? null,
    'status' => 'published', 'published_at' => $a['published_at'] ?? $now, 'updated_at' => $a['updated_at'] ?? $now, 'created_at' => $now,
]);
foreach ($a['categories'] ?? [] as $c) {
    Db::q('INSERT IGNORE INTO categories (slug, name) VALUES (?, ?)', [$c['slug'], $c['name']]);
    Db::q('INSERT IGNORE INTO article_categories (article_id, category_id) SELECT ?, id FROM categories WHERE slug = ?', [$id, $c['slug']]);
}
echo "Added: /{$a['slug']}/ (id {$id})\n";
