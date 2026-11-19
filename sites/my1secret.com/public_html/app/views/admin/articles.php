<?php defined('M1S') || exit; ?>
<h1>Articles</h1>
<?= view('admin/_nav') ?>
<p><a class="btn btn-accent" href="/admin/articles/new/">+ New article</a></p>
<table class="table"><thead><tr><th>Title</th><th>Topic</th><th>Status</th><th>Published</th><th>Comments</th></tr></thead><tbody>
<?php foreach ($articles as $a): ?>
  <tr><td><a href="/admin/articles/<?= (int)$a['id'] ?>/"><?= e($a['title']) ?></a><br><a class="muted small" href="<?= e(article_url($a)) ?>"><?= e(article_url($a)) ?></a></td>
  <td><?= e((string)$a['topic_name']) ?></td><td><?= e($a['status']) ?></td><td><?= e(substr($a['published_at'], 0, 10)) ?></td><td><?= (int)$a['comment_count'] ?></td></tr>
<?php endforeach; ?>
</tbody></table>
