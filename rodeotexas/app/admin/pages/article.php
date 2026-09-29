<?php
declare(strict_types=1);

use RT\Db;

$idParam = (string) ($_GET['id'] ?? 'new');
$id = ctype_digit($idParam) ? (int) $idParam : null;
$a = $id ? Db::one('SELECT * FROM articles WHERE id = ?', [$id]) : null;
if ($id && !$a) {
    redirect(admin_url('articles'));
}
$reserved = ['rodeos', 'past-events', 'blog', 'category', 'about', 'contact', 'privacy-policy', 'submit-event', 'favorites', 'admin', 'api', 'assets', 'includes', 'pages', 'wp-content'];
$errors = [];
if (is_post()) {
    $d = [
        'title' => post_str('title'),
        'slug' => post_str('slug', 190) ?? slugify((string) post_str('title')),
        'seo_title' => post_str('seo_title'),
        'meta_description' => post_str('meta_description', 320),
        'excerpt' => clean_text($_POST['excerpt'] ?? null, 1000),
        'content_html' => trim((string) ($_POST['content_html'] ?? '')),
        'featured_image' => post_str('featured_image', 500),
        'featured_alt' => post_str('featured_alt'),
        'status' => in_array($_POST['status'] ?? '', ['draft', 'published', 'archived'], true) ? $_POST['status'] : 'draft',
        'published_at' => valid_date(substr((string) ($_POST['published_date'] ?? ''), 0, 10)) ? $_POST['published_date'] . ' 12:00:00' : null,
    ];
    if (!$d['title']) { $errors[] = 'Title is required.'; }
    if (!preg_match('/^[a-z0-9-]{3,190}$/', (string) $d['slug']) || in_array($d['slug'], $reserved, true)) { $errors[] = 'Slug must be lowercase letters, numbers and hyphens, and not a reserved path.'; }
    if (Db::val('SELECT id FROM articles WHERE slug = ? AND id <> ?', [$d['slug'], $id ?? 0])) { $errors[] = 'Another article already uses that slug.'; }
    if ($d['content_html'] === '') { $errors[] = 'Content is required.'; }
    if ($d['featured_image'] && !preg_match('~^(/|https://)~', $d['featured_image'])) { $errors[] = 'Featured image must be a site path (/wp-content/…) or https URL.'; }
    if ($d['status'] === 'published' && !$d['published_at']) { $d['published_at'] = gmdate('Y-m-d H:i:s'); }
    if (!$errors) {
        $now = now_utc();
        $d['updated_at'] = $now;
        Db::tx(function () use (&$id, $a, $d, $now) {
            if ($a) {
                if ($a['slug'] !== $d['slug']) {
                    Db::q('INSERT INTO redirects (from_path, to_path, code, created_at) VALUES (?, ?, 301, ?) ON DUPLICATE KEY UPDATE to_path = VALUES(to_path)', ['/' . $a['slug'] . '/', '/' . $d['slug'] . '/', $now]);
                }
                Db::update('articles', $d, 'id = :id', ['id' => $id]);
            } else {
                $d['created_at'] = $now;
                $id = Db::insert('articles', $d);
            }
            Db::q('DELETE FROM article_categories WHERE article_id = ?', [$id]);
            foreach ((array) ($_POST['categories'] ?? []) as $c) {
                if (ctype_digit((string) $c)) {
                    Db::q('INSERT IGNORE INTO article_categories (article_id, category_id) VALUES (?, ?)', [$id, (int) $c]);
                }
            }
            $newCat = clean_str($_POST['new_category'] ?? null, 80);
            if ($newCat) {
                Db::q('INSERT IGNORE INTO categories (slug, name) VALUES (?, ?)', [slugify($newCat), $newCat]);
                Db::q('INSERT IGNORE INTO article_categories (article_id, category_id) SELECT ?, id FROM categories WHERE slug = ?', [$id, slugify($newCat)]);
            }
        });
        flash('Article saved.');
        redirect(admin_url('article', ['id' => $id]), 303);
    }
    $a = array_merge($a ?? [], $d);
}
$a = $a ?? ['title' => '', 'slug' => '', 'seo_title' => '', 'meta_description' => '', 'excerpt' => '', 'content_html' => '', 'featured_image' => '', 'featured_alt' => '', 'status' => 'draft', 'published_at' => null];
$cats = Db::all('SELECT * FROM categories ORDER BY name');
$sel = $id ? array_column(Db::all('SELECT category_id FROM article_categories WHERE article_id = ?', [$id]), 'category_id') : [];
admin_header($id ? 'Edit article' : 'New article');
?>
<?php if ($errors): ?><div class="alert alert--danger"><?= e(implode(' ', $errors)) ?></div><?php endif; ?>
<?php if ($id): ?><p><a href="/<?= e($a['slug']) ?>/" target="_blank" rel="noopener">View article ↗</a></p><?php endif; ?>
<form method="post" class="card">
  <?= RT\Auth::csrfField() ?>
  <?= f_text('title', 'Title', $a['title'], ['required' => true]) ?>
  <div class="row2"><?= f_text('slug', 'URL slug (the article lives at /slug/)', $a['slug'], ['help' => 'Changing it creates a 301 redirect from the old URL.']) ?>
    <?= f_select('status', 'Status', $a['status'], ['draft' => 'Draft', 'published' => 'Published', 'archived' => 'Archived (hidden)'], false) ?></div>
  <div class="row2"><?= f_text('seo_title', 'SEO title (optional)', $a['seo_title'], ['maxlength' => 255]) ?><?= f_text('published_date', 'Publish date', substr((string) $a['published_at'], 0, 10), ['type' => 'date']) ?></div>
  <?= f_text('meta_description', 'Meta description (~155 characters)', $a['meta_description'], ['maxlength' => 320]) ?>
  <?= f_area('excerpt', 'Excerpt', $a['excerpt'], ['rows' => 2]) ?>
  <?= f_area('content_html', 'Content (HTML)', $a['content_html'], ['rows' => 22, 'mono' => true, 'help' => 'Headings <h2>/<h3>, paragraphs <p>, lists, links and images. Only administrators can edit this HTML.']) ?>
  <div class="row2"><?= f_text('featured_image', 'Featured image path or URL', $a['featured_image']) ?><?= f_text('featured_alt', 'Featured image alt text', $a['featured_alt']) ?></div>
  <fieldset><legend>Categories</legend><div class="checks"><?php foreach ($cats as $c): ?><label class="check"><input type="checkbox" name="categories[]" value="<?= (int) $c['id'] ?>"<?= in_array($c['id'], $sel) ? ' checked' : '' ?>> <?= e($c['name']) ?></label><?php endforeach; ?></div>
    <?= f_text('new_category', 'Add a new category', '') ?></fieldset>
  <button class="btn btn--primary" type="submit">Save article</button>
</form>
<?php
admin_footer();
