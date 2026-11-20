<?php defined('WCA') || exit; $l = $l ?? []; $photosRaw = !empty($l['id']) ? (json_decode(db()->query('SELECT photos FROM listings WHERE id = ' . (int)$l['id'])->fetchColumn() ?: '[]', true) ?: []) : []; ?>
<div class="wrap section-tight admin-page">
  <p><a href="/admin/listings/">← All listings</a></p>
  <div class="section-head"><h1 class="h2"><?= !empty($l['id']) ? 'Edit: ' . e($l['name']) : 'New listing' ?></h1>
    <?php if (!empty($l['id'])): ?><a href="/apartments/<?= e($l['slug']) ?>/" target="_blank">View on site ↗</a><?php endif; ?></div>
  <?php if ($errors): ?><div class="alert alert-error"><?php foreach ($errors as $er): ?><div><?= e($er) ?></div><?php endforeach; ?></div><?php endif; ?>
  <?php if (!empty($l['submitter_email'])): ?><div class="alert alert-info">Submitted by <?= e($l['submitter_name']) ?> &lt;<?= e($l['submitter_email']) ?>&gt; (<?= e($l['source']) ?> listing)</div><?php endif; ?>
  <form method="post" enctype="multipart/form-data" class="form">
    <?= csrf_field() ?>
    <fieldset>
      <legend>Admin controls</legend>
      <div class="grid-4">
        <label>Status<select name="status"><?php foreach (['published', 'pending', 'awaiting_payment', 'draft', 'rejected'] as $s): ?><option <?= ($l['status'] ?? 'published') === $s ? 'selected' : '' ?>><?= $s ?></option><?php endforeach; ?></select></label>
        <label>URL slug<input name="slug" value="<?= e($l['slug'] ?? '') ?>" placeholder="auto from name"></label>
        <label>Latitude<input name="lat" value="<?= e($l['lat'] ?? '') ?>"></label>
        <label>Longitude<input name="lng" value="<?= e($l['lng'] ?? '') ?>"></label>
      </div>
      <div class="grid-3">
        <label>Owner account email<input type="email" name="owner_email" value="<?= e($owner['email'] ?? '') ?>" placeholder="blank = unclaimed"></label>
        <label class="check"><input type="checkbox" name="contact_visible" value="1" <?= !empty($l['contact_visible']) ? 'checked' : '' ?>> Show contact details (requires owner)</label>
        <label class="check"><input type="checkbox" name="featured" value="1" <?= !empty($l['featured']) ? 'checked' : '' ?>> Featured / Popular</label>
      </div>
    </fieldset>
    <?php partial('partials/listing_form', ['l' => $l, 'showContact' => true]); ?>
    <fieldset>
      <legend>Photos</legend>
      <?php if ($photosRaw): ?>
      <div class="photo-manage"><?php foreach ($photosRaw as $p): ?><label><img src="<?= e(photo_url($p, true)) ?>" alt="" width="160" height="107"><span><input type="checkbox" name="remove_photos[]" value="<?= e($p) ?>"> Remove</span></label><?php endforeach; ?></div>
      <?php else: ?><p class="small muted">Using automatic representative stock photos.</p><?php endif; ?>
      <label>Upload photos<input type="file" name="photos[]" accept="image/jpeg,image/png,image/webp" multiple></label>
      <label>Import photos from URLs (one per line; JPG/PNG/WebP). Only use photos you own or have the owner's permission to use.<textarea name="photo_urls" rows="3" placeholder="https://example.com/photo1.jpg"></textarea></label>
      <label>Or stock photo keys, comma separated (e.g. ext-2, liv-5, kit-1) <input name="stock_photos" placeholder="ext-1, liv-3, kit-2, bed-4, bath-1"></label>
    </fieldset>
    <button class="btn btn-accent" type="submit">Save listing</button>
  </form>
  <?php if (!empty($l['id'])): ?>
  <div class="danger-zone card">
    <h2 class="h5">Quick actions</h2>
    <form method="post" action="/admin/listings/action/" class="inline"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$l['id'] ?>">
      <?php if (!empty($l['owner_id'])): ?><button class="btn btn-ghost btn-sm" name="action" value="revoke" onclick="return confirm('Remove owner access and hide contact details?')">Revoke owner</button><?php endif; ?>
      <button class="btn btn-ghost btn-sm" name="action" value="unpublish">Unpublish</button>
      <button class="btn btn-danger btn-sm" name="action" value="delete" onclick="return confirm('Permanently delete this listing?')">Delete</button>
    </form>
  </div>
  <?php endif; ?>
</div>
