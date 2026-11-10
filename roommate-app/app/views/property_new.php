<div class="narrow">
  <a class="backlink" href="/properties"><?= icon('back') ?> Properties</a>
  <h1>Add an apartment property</h1>
  <p class="muted"><?= setting('require_property_approval', '1') === '1' && !is_admin() ? 'New properties are reviewed by our team before they appear.' : '' ?></p>
  <?php if ($errors): ?><div class="alert alert-error"><ul><?php foreach ($errors as $er): ?><li><?= e($er) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
  <form method="post" class="card form form-section">
    <?= csrf_field() ?>
    <label>Property name<input type="text" name="name" value="<?= e($d['name']) ?>" required maxlength="150" placeholder="e.g. The Grove at Riverside"></label>
    <label>Street address<input type="text" name="address" value="<?= e($d['address']) ?>" maxlength="200"></label>
    <div class="row-3">
      <label>City<input type="text" name="city" value="<?= e($d['city']) ?>" required maxlength="100"></label>
      <label>State<input type="text" name="state" value="<?= e($d['state']) ?>" maxlength="40"></label>
      <label>ZIP<input type="text" name="zip" value="<?= e($d['zip']) ?>" maxlength="15"></label>
    </div>
    <div class="row-2">
      <label>Rent from ($/mo)<input type="number" name="rent_min" value="<?= e($d['rent_min']) ?>" min="0" step="25"></label>
      <label>Rent to ($/mo)<input type="number" name="rent_max" value="<?= e($d['rent_max']) ?>" min="0" step="25"></label>
    </div>
    <label>Website<input type="url" name="website" value="<?= e($d['website']) ?>" placeholder="https://"></label>
    <label>Description<textarea name="description" rows="4" maxlength="2000"><?= e($d['description']) ?></textarea></label>
    <div class="form-actions"><a class="btn btn-ghost" href="/properties">Cancel</a><button class="btn btn-primary" type="submit">Submit property</button></div>
  </form>
</div>
