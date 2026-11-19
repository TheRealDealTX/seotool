<?php defined('M1S') || exit; ?>
<h1><?= $a ? 'Edit article' : 'New article' ?></h1>
<?= view('admin/_nav') ?>
<?php if ($a): ?><p><a href="<?= e(article_url($a)) ?>" target="_blank">View on site ↗</a></p><?php endif; ?>
<form class="form card-pad wide-form" method="post" action="/admin/articles/<?= $a ? (int)$a['id'] : 'new' ?>/" enctype="multipart/form-data">
  <?= csrf_field() ?>
  <label for="title">Headline (H1)</label>
  <input id="title" name="title" required maxlength="200" value="<?= e($a['title'] ?? '') ?>">
  <label for="slug">URL slug <span class="muted">(/blog/<em>slug</em>/; leave blank to generate. Changing it on a live article breaks old links.)</span></label>
  <input id="slug" name="slug" maxlength="100" value="<?= e($a['slug'] ?? '') ?>">
  <label for="seo_title">SEO title <span class="muted">(the &lt;title&gt; tag, ~60 characters)</span></label>
  <input id="seo_title" name="seo_title" maxlength="120" value="<?= e($a['seo_title'] ?? '') ?>" data-count>
  <label for="meta_description">Meta description <span class="muted">(~150 characters)</span></label>
  <textarea id="meta_description" name="meta_description" rows="2" maxlength="200" data-count><?= e($a['meta_description'] ?? '') ?></textarea>
  <div class="form-cols">
    <div><label for="topic_id">Topic</label>
      <select id="topic_id" name="topic_id"><option value="">None</option>
      <?php foreach ($topics as $t): ?><option value="<?= (int)$t['id'] ?>"<?= (int)($a['topic_id'] ?? 0) === (int)$t['id'] ? ' selected' : '' ?>><?= e($t['name']) ?></option><?php endforeach; ?>
      </select></div>
    <div><label for="status">Status</label>
      <select id="status" name="status"><option value="published">Published</option><option value="draft"<?= ($a['status'] ?? '') === 'draft' ? ' selected' : '' ?>>Draft</option></select></div>
    <div><label for="published_at">Publish date (UTC)</label>
      <input id="published_at" name="published_at" type="datetime-local" value="<?= e(isset($a['published_at']) ? str_replace(' ', 'T', substr($a['published_at'], 0, 16)) : '') ?>"></div>
  </div>
  <label for="image">Featured image <?= !empty($a['image']) ? '<span class="muted">(current: ' . e($a['image']) . ')</span>' : '' ?></label>
  <input id="image" name="image" type="file" accept="image/*">
  <label for="image_alt">Image alt text</label>
  <input id="image_alt" name="image_alt" maxlength="255" value="<?= e($a['image_alt'] ?? '') ?>">
  <div class="form-cols">
    <div><label for="image_credit">Photo credit <span class="muted">(required for CC BY photos, e.g. "Photo: Jane Doe / Flickr (CC BY 2.0)")</span></label>
      <input id="image_credit" name="image_credit" maxlength="300" value="<?= e($a['image_credit'] ?? '') ?>"></div>
    <div><label for="image_credit_url">Credit link (photo's source page)</label>
      <input id="image_credit_url" name="image_credit_url" type="url" maxlength="500" value="<?= e($a['image_credit_url'] ?? '') ?>"></div>
  </div>
  <label for="body_html">Body (HTML: use &lt;h2&gt;, &lt;h3&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;a&gt;, &lt;img&gt;)</label>
  <textarea id="body_html" name="body_html" rows="24" class="mono"><?= e($a['body_html'] ?? '') ?></textarea>
  <div class="form-row"><button class="btn btn-accent" type="submit">Save article</button></div>
</form>
<?php if ($a): ?>
<form method="post" action="/admin/articles/<?= (int)$a['id'] ?>/delete/" data-confirm="Delete this article permanently?"><?= csrf_field() ?><button class="btn btn-ghost danger">Delete article</button></form>
<?php endif; ?>
