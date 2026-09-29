<?php
declare(strict_types=1);

use RT\Db;

$rows = Db::all('SELECT id, slug, title, status, published_at, updated_at FROM articles ORDER BY published_at DESC, id DESC');
admin_header('Articles');
?>
<p><a class="btn btn--primary" href="<?= e(admin_url('article', ['id' => 'new'])) ?>">+ New article</a></p>
<table class="table"><thead><tr><th>Title</th><th>URL</th><th>Status</th><th>Published</th><th>Updated</th></tr></thead><tbody>
<?php foreach ($rows as $a): ?><tr><td><a href="<?= e(admin_url('article', ['id' => $a['id']])) ?>"><?= e($a['title']) ?></a></td><td><a class="small" href="/<?= e($a['slug']) ?>/" target="_blank" rel="noopener">/<?= e($a['slug']) ?>/</a></td><td><?= status_pill($a['status']) ?></td><td class="nowrap small"><?= e(substr((string) $a['published_at'], 0, 10)) ?></td><td class="nowrap small"><?= e(substr((string) $a['updated_at'], 0, 10)) ?></td></tr><?php endforeach; ?>
</tbody></table>
<?php
admin_footer();
