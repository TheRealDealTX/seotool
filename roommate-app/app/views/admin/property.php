<a class="backlink" href="/admin/properties"><?= icon('back') ?> Properties</a>
<h1><?= $isNew ? 'New property' : 'Edit ' . e($p['name']) ?></h1>
<?php if ($errors): ?><div class="alert alert-error"><ul><?php foreach ($errors as $er): ?><li><?= e($er) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
<form method="post" enctype="multipart/form-data" class="card form form-section narrow-lg">
  <?= csrf_field() ?>
  <label>Name<input type="text" name="name" value="<?= e($p['name']) ?>" required maxlength="150"></label>
  <?php if (!$isNew): ?><label>URL slug<div class="input-prefix"><span>/properties/</span><input type="text" name="slug" value="<?= e($p['slug']) ?>" pattern="[a-z0-9-]+"></div></label><?php endif; ?>
  <label>Street address<input type="text" name="address" value="<?= e($p['address']) ?>"></label>
  <div class="row-3">
    <label>City<input type="text" name="city" value="<?= e($p['city']) ?>"></label>
    <label>State<input type="text" name="state" value="<?= e($p['state']) ?>"></label>
    <label>ZIP<input type="text" name="zip" value="<?= e($p['zip']) ?>"></label>
  </div>
  <div class="row-2">
    <label>Rent from<input type="number" name="rent_min" value="<?= e($p['rent_min']) ?>" min="0" step="25"></label>
    <label>Rent to<input type="number" name="rent_max" value="<?= e($p['rent_max']) ?>" min="0" step="25"></label>
  </div>
  <label>Website<input type="text" name="website" value="<?= e($p['website']) ?>" placeholder="https://"></label>
  <label>Amenities <small class="muted">(comma separated)</small><input type="text" name="amenities" value="<?= e($p['amenities']) ?>" placeholder="Pool, Gym, In-unit laundry, Pet park"></label>
  <label>Description<textarea name="description" rows="6"><?= e($p['description']) ?></textarea></label>
  <div class="avatar-edit">
    <?php if (property_image($p)): ?><img src="<?= e(property_image($p)) ?>" alt="" class="thumb"><?php endif; ?>
    <div>
      <label>Photo<input type="file" name="image" accept="image/*"></label>
      <?php if ($p['image']): ?><label class="check small"><input type="checkbox" name="remove_image" value="1"> Remove photo</label><?php endif; ?>
    </div>
  </div>
  <div class="row-2">
    <label>Status<select name="status"><?php foreach (['approved', 'pending', 'rejected'] as $st): ?><option value="<?= $st ?>"<?= $p['status'] === $st ? ' selected' : '' ?>><?= ucfirst($st) ?></option><?php endforeach; ?></select></label>
    <label class="check check-pad"><input type="checkbox" name="is_featured" value="1"<?= $p['is_featured'] ? ' checked' : '' ?>> Featured property</label>
  </div>
  <div class="form-actions"><a class="btn btn-ghost" href="/admin/properties">Cancel</a><button class="btn btn-primary">Save property</button></div>
</form>
