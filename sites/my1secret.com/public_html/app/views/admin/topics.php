<?php defined('M1S') || exit; ?>
<h1>Blog topics</h1>
<?= view('admin/_nav') ?>
<?php foreach (array_merge($topics, [null]) as $t): ?>
  <form class="form card-pad" method="post" action="/admin/topics/">
    <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)($t['id'] ?? 0) ?>">
    <h2><?= $t ? e($t['name']) . ' <span class="muted small">/blog/topic/' . e($t['slug']) . '/</span>' : 'New topic' ?></h2>
    <?php if (!$t): ?><label>URL slug<input name="slug" maxlength="60"></label><?php endif; ?>
    <div class="form-cols">
      <div><label>Name<input name="name" required maxlength="80" value="<?= e($t['name'] ?? '') ?>"></label></div>
      <div><label>Sort<input name="sort" type="number" value="<?= (int)($t['sort'] ?? 0) ?>"></label></div>
    </div>
    <label>SEO title (H1)<input name="seo_title" maxlength="120" value="<?= e($t['seo_title'] ?? '') ?>"></label>
    <label>Description<textarea name="description" rows="2"><?= e($t['description'] ?? '') ?></textarea></label>
    <div class="form-row"><button class="btn btn-accent btn-sm">Save</button></div>
  </form>
<?php endforeach; ?>
