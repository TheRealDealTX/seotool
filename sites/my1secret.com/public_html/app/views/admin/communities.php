<?php defined('M1S') || exit; ?>
<h1>Communities</h1>
<?= view('admin/_nav') ?>
<?php foreach (array_merge($communities, [null]) as $c): ?>
  <form class="form card-pad" method="post" action="/admin/communities/">
    <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)($c['id'] ?? 0) ?>">
    <h2><?= $c ? e($c['name']) . ' <span class="muted small">/forum/' . e($c['slug']) . '/</span>' : 'New community' ?></h2>
    <?php if (!$c): ?><label>URL slug<input name="slug" maxlength="40"></label><?php endif; ?>
    <div class="form-cols">
      <div><label>Name<input name="name" required maxlength="60" value="<?= e($c['name'] ?? '') ?>"></label></div>
      <div><label>Color<input name="color" type="color" value="<?= e($c['color'] ?? '#1f8fcf') ?>"></label></div>
      <div><label>Sort<input name="sort" type="number" value="<?= (int)($c['sort'] ?? 0) ?>"></label></div>
    </div>
    <label>SEO title (H1 and &lt;title&gt;)<input name="title" required maxlength="120" value="<?= e($c['title'] ?? '') ?>"></label>
    <label>Description (meta description and sidebar)<textarea name="description" rows="2" required><?= e($c['description'] ?? '') ?></textarea></label>
    <div class="form-row"><button class="btn btn-accent btn-sm">Save</button></div>
  </form>
<?php endforeach; ?>
