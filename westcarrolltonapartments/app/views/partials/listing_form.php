<?php defined('WCA') || exit;
/** Shared listing fields. $l = current values (array), $showContact = bool */
$v = fn($k) => e(is_array($l[$k] ?? null) ? implode("\n", $l[$k]) : ($l[$k] ?? ''));
$sel = fn($k, $val) => (string)($l[$k] ?? '') === (string)$val ? 'selected' : '';
?>
<fieldset>
  <legend>Property</legend>
  <div class="grid-2">
    <label>Property name *<input name="name" required maxlength="160" value="<?= $v('name') ?>"></label>
    <label>Property type
      <select name="type"><?php foreach (LISTING_TYPES as $k => $n): ?><option value="<?= $k ?>" <?= $sel('type', $k) ?>><?= e($n) ?></option><?php endforeach; ?></select>
    </label>
  </div>
  <div class="grid-3">
    <label class="span-2">Street address *<input name="address" required maxlength="190" value="<?= $v('address') ?>" placeholder="123 Main St"></label>
    <label>ZIP<input name="zip" maxlength="10" value="<?= $v('zip') ?: '45449' ?>"></label>
  </div>
  <label>City<input name="city" maxlength="80" value="<?= $v('city') ?: 'West Carrollton' ?>"></label>
</fieldset>
<fieldset>
  <legend>Units &amp; pricing</legend>
  <div class="grid-4">
    <label>Min beds (0 = studio)<input type="number" min="0" max="6" name="beds_min" value="<?= $v('beds_min') ?>"></label>
    <label>Max beds<input type="number" min="0" max="6" name="beds_max" value="<?= $v('beds_max') ?>"></label>
    <label>Baths<input name="baths" maxlength="20" value="<?= $v('baths') ?>" placeholder="1–2"></label>
    <label>Total units<input type="number" min="1" name="units" value="<?= $v('units') ?>"></label>
    <label>Rent from ($/mo)<input type="number" min="0" name="rent_min" value="<?= $v('rent_min') ?>"></label>
    <label>Rent to ($/mo)<input type="number" min="0" name="rent_max" value="<?= $v('rent_max') ?>"></label>
    <label>Sq ft from<input type="number" min="0" name="sqft_min" value="<?= $v('sqft_min') ?>"></label>
    <label>Sq ft to<input type="number" min="0" name="sqft_max" value="<?= $v('sqft_max') ?>"></label>
  </div>
  <div class="grid-4">
    <label>Year built<input type="number" min="1850" max="2100" name="year_built" value="<?= $v('year_built') ?>"></label>
    <label>Cats
      <select name="cats"><option value="">Unknown</option><option value="1" <?= $sel('cats', '1') ?>>Allowed</option><option value="0" <?= $sel('cats', '0') ?>>Not allowed</option></select></label>
    <label>Dogs
      <select name="dogs"><option value="">Unknown</option><option value="1" <?= $sel('dogs', '1') ?>>Allowed</option><option value="0" <?= $sel('dogs', '0') ?>>Not allowed</option></select></label>
    <label>Age restriction
      <select name="age_restriction"><option value="">None</option><option <?= $sel('age_restriction', '55+') ?>>55+</option><option <?= $sel('age_restriction', '62+') ?>>62+</option></select></label>
  </div>
  <label>Pet policy notes<input name="pet_notes" maxlength="255" value="<?= $v('pet_notes') ?>" placeholder="e.g. 2 pets max, $35/mo pet rent, 40 lb limit"></label>
  <label class="check"><input type="checkbox" name="income_restricted" value="1" <?= !empty($l['income_restricted']) ? 'checked' : '' ?>> Income-restricted / affordable housing program</label>
</fieldset>
<fieldset>
  <legend>Description &amp; amenities</legend>
  <label>Description *<textarea name="description" rows="6" required minlength="40" maxlength="5000"><?= $v('description') ?></textarea></label>
  <label>Amenities (one per line)<textarea name="amenities" rows="6" placeholder="Swimming pool&#10;Fitness center&#10;In-unit washer/dryer"><?= $v('amenities') ?></textarea></label>
</fieldset>
<fieldset>
  <legend>Contact details <?= empty($showContact) ? '<small class="muted">(hidden on free listings until claimed)</small>' : '' ?></legend>
  <div class="grid-2">
    <label>Phone<input name="phone" maxlength="60" value="<?= $v('phone') ?>"></label>
    <label>Leasing email<input type="email" name="email" maxlength="190" value="<?= $v('email') ?>"></label>
    <label>Website<input type="url" name="website" maxlength="255" value="<?= $v('website') ?>" placeholder="https://"></label>
    <label>Office hours<input name="office_hours" maxlength="190" value="<?= $v('office_hours') ?>" placeholder="Mon–Fri 9–5, Sat 10–2"></label>
  </div>
</fieldset>
