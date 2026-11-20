<?php defined('WCA') || exit; $uploaded = array_filter($l['photos'], fn($p) => str_starts_with($p, '/uploads/')); ?>
<div class="wrap section-tight">
  <p><a href="/account/">← My account</a></p>
  <h1 class="h2">Edit <?= e($l['name']) ?></h1>
  <?php if ($errors): ?><div class="alert alert-error"><?php foreach ($errors as $er): ?><div><?= e($er) ?></div><?php endforeach; ?></div><?php endif; ?>
  <form method="post" enctype="multipart/form-data" class="form">
    <?= csrf_field() ?>
    <?php partial('partials/listing_form', ['l' => $l, 'showContact' => true]); ?>
    <fieldset>
      <legend>Photos</legend>
      <?php if ($uploaded): ?>
        <div class="photo-manage">
          <?php foreach ($uploaded as $p): ?><label><img src="<?= e($p) ?>" alt="" width="160" height="107"><span><input type="checkbox" name="remove_photos[]" value="<?= e($p) ?>"> Remove</span></label><?php endforeach; ?>
        </div>
      <?php else: ?><p class="small muted">Your listing currently shows representative stock photos. Upload your own to replace them.</p><?php endif; ?>
      <label>Add photos (JPG, PNG or WebP, up to 6 MB each, 12 max)<input type="file" name="photos[]" accept="image/jpeg,image/png,image/webp" multiple></label>
    </fieldset>
    <button class="btn btn-accent" type="submit">Save changes</button> <a href="<?= e($l['url']) ?>" target="_blank">Preview listing ↗</a>
  </form>
</div>
