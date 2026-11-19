<?php defined('M1S') || exit; ?>
<h1>Amazon products</h1>
<?= view('admin/_nav') ?>
<p class="muted">Affiliate tag <strong><?= e(amazon_tag()) ?></strong> is added to every link automatically. Leave <em>Amazon link</em> empty to link to an Amazon search for the <em>search terms</em>, or paste a product URL / ASIN for a specific item.
Tags (comma-separated): <code>article:&lt;article-slug&gt;</code> shows it on one article, <code>topic:&lt;topic-slug&gt;</code> on every article in a topic and on the Shop page (topics: <?= e(implode(', ', array_column(topics(), 'slug'))) ?>).</p>
<form method="get" class="search-big"><input type="search" name="f" value="<?= e($f) ?>" placeholder="Filter by tag or name" aria-label="Filter"><button class="btn btn-accent">Filter</button></form>
<?php foreach (array_merge([null], $products) as $p): ?>
  <form class="form card-pad" method="post" action="/admin/products/">
    <?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)($p['id'] ?? 0) ?>"><input type="hidden" name="f" value="<?= e($f) ?>">
    <h2><?= $p ? e($p['name']) . ($p['active'] ? '' : ' <span class="badge">hidden</span>') : 'Add a product' ?></h2>
    <div class="form-cols">
      <div><label>Name<input name="name" required maxlength="160" value="<?= e($p['name'] ?? '') ?>"></label></div>
      <div><label>Search terms<input name="query" maxlength="200" value="<?= e($p['query'] ?? '') ?>"></label></div>
      <div><label>Amazon link or ASIN (optional)<input name="url" maxlength="500" value="<?= e($p['url'] ?? '') ?>" placeholder="https://www.amazon.com/dp/…"></label></div>
    </div>
    <label>Why it helps<input name="blurb" maxlength="300" value="<?= e($p['blurb'] ?? '') ?>"></label>
    <div class="form-cols">
      <div><label>Tags<input name="tags" maxlength="1000" value="<?= e($p['tags'] ?? '') ?>" placeholder="article:my-slug, topic:renting"></label></div>
      <div><label>Image URL (optional, https)<input name="image" maxlength="500" value="<?= e($p['image'] ?? '') ?>"></label></div>
      <div><label>Sort<input name="sort" type="number" value="<?= (int)($p['sort'] ?? 0) ?>"></label></div>
    </div>
    <label class="check"><input type="checkbox" name="active" value="1"<?= ($p['active'] ?? 1) ? ' checked' : '' ?>> Show on site</label>
    <div class="form-row">
      <?php if ($p): ?><a href="<?= e(amazon_url($p)) ?>" target="_blank" rel="noopener">Test link ↗</a><?php endif; ?>
      <button class="btn btn-accent btn-sm" name="action" value="save">Save</button>
      <?php if ($p): ?><button class="btn btn-ghost btn-sm danger" name="action" value="delete" data-confirm-click="Delete this product?">Delete</button><?php endif; ?>
    </div>
  </form>
<?php endforeach; ?>
