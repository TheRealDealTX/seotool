<?php defined('APP') || exit;
/** @var array $d values; @var array $err; @var string $mode submit|owner|admin|new; @var array $photos; @var string $action */
$v = fn($k, $def = '') => e($d[$k] ?? $def);
$sel = fn($k, $val, $def = '') => (string)($d[$k] ?? $def) === (string)$val ? ' selected' : '';
$amSel = array_filter(explode(',', (string)($d['amenities'] ?? '')));
if (isset($d['amenities']) && is_array($d['amenities'])) $amSel = $d['amenities'];
$errCls = fn($k) => isset($err[$k]) ? ' class="has-err"' : '';
$errMsg = fn($k) => isset($err[$k]) ? '<span class="err">' . e($err[$k]) . '</span>' : '';
$photos = $photos ?? [];
?>
<form class="listing-form" method="post" action="<?= e($action) ?>" enctype="multipart/form-data" novalidate>
  <?= csrf_field() ?><?= honeypot_field() ?>
  <?= form_errors($err) ?>
  <?= $tierHtml ?? '' ?>

  <fieldset>
    <legend>The basics</legend>
    <label<?= $errCls('title') ?>>Listing title <small>e.g. “Sunny furnished room near campus, June–August”</small>
      <input type="text" name="title" value="<?= $v('title') ?>" maxlength="120" required><?= $errMsg('title') ?></label>
    <div class="row3">
      <label<?= $errCls('property_type') ?>>Property type
        <select name="property_type" required><option value="">Choose…</option>
          <?php foreach (property_types() as $k => $t): ?><option value="<?= e($k) ?>"<?= $sel('property_type', $k) ?>><?= e($t) ?></option><?php endforeach; ?>
        </select><?= $errMsg('property_type') ?></label>
      <label>Furnished?
        <select name="furnished"><option value="1"<?= $sel('furnished', 1, 1) ?>>Yes, furnished</option><option value="0"<?= $sel('furnished', 0, 1) ?>>No, unfurnished</option></select></label>
      <label>Pets
        <select name="pets"><?php foreach (pet_options() as $k => $t): ?><option value="<?= e($k) ?>"<?= $sel('pets', $k, 'no') ?>><?= e($t) ?></option><?php endforeach; ?></select></label>
    </div>
    <div class="row3">
      <label>Bedrooms
        <select name="beds"><?php foreach (['studio' => 'Studio', '1' => '1', '2' => '2', '3' => '3', '4' => '4', '5+' => '5+'] as $k => $t): ?><option value="<?= e($k) ?>"<?= $sel('beds', $k, '1') ?>><?= e($t) ?></option><?php endforeach; ?></select></label>
      <label>Bathrooms
        <select name="baths"><?php foreach (['shared' => 'Shared', '1' => '1', '1.5' => '1.5', '2' => '2', '2.5' => '2.5', '3+' => '3+'] as $k => $t): ?><option value="<?= e($k) ?>"<?= $sel('baths', $k, '1') ?>><?= e($t) ?></option><?php endforeach; ?></select></label>
      <label>Minimum stay
        <select name="min_stay"><?php for ($i = 1; $i <= 12; $i++): ?><option value="<?= $i ?>"<?= $sel('min_stay', $i, 1) ?>><?= $i ?> month<?= $i > 1 ? 's' : '' ?></option><?php endfor; ?></select></label>
    </div>
  </fieldset>

  <fieldset>
    <legend>Location</legend>
    <div class="row3">
      <label<?= $errCls('city') ?>>City<input type="text" name="city" value="<?= $v('city') ?>" maxlength="80" required list="city-suggest" autocomplete="address-level2"><?= $errMsg('city') ?></label>
      <label<?= $errCls('state') ?>>State
        <select name="state" required><option value="">Choose…</option><?php foreach (states() as $k => $t): ?><option value="<?= e($k) ?>"<?= $sel('state', $k) ?>><?= e($t) ?></option><?php endforeach; ?></select><?= $errMsg('state') ?></label>
      <label<?= $errCls('zip') ?>>ZIP code<input type="text" name="zip" value="<?= $v('zip') ?>" inputmode="numeric" maxlength="5" autocomplete="postal-code"><?= $errMsg('zip') ?></label>
    </div>
    <datalist id="city-suggest"><?php foreach (city_content() as $c): ?><option value="<?= e($c['name']) ?>"><?php endforeach; ?></datalist>
    <label>Neighborhood <small>(optional)</small><input type="text" name="neighborhood" value="<?= $v('neighborhood') ?>" maxlength="80"></label>
    <div class="pin-picker">
      <p><strong>Approximate map pin</strong> <small>(optional) — tap near your street. We blur it to within a few blocks; your exact address is never shown.</small></p>
      <div id="pinmap" class="map map-sm" data-lat="<?= $v('lat') ?>" data-lng="<?= $v('lng') ?>"></div>
      <input type="hidden" name="lat" value="<?= $v('lat') ?>"><input type="hidden" name="lng" value="<?= $v('lng') ?>">
      <button type="button" class="btn btn-sm btn-ghost" data-pin-clear>Clear pin</button>
    </div>
  </fieldset>

  <fieldset>
    <legend>Price &amp; dates</legend>
    <div class="row3">
      <label<?= $errCls('rent') ?>>Monthly rent ($)<input type="number" name="rent" value="<?= $v('rent') ?>" min="100" max="50000" step="1" inputmode="numeric" required><?= $errMsg('rent') ?></label>
      <label>Security deposit ($)<input type="number" name="deposit" value="<?= $v('deposit') ?>" min="0" step="1" inputmode="numeric"></label>
      <label class="chk"><input type="checkbox" name="utilities_included" value="1"<?= !empty($d['utilities_included']) ? ' checked' : '' ?>> Utilities included</label>
    </div>
    <div class="row3">
      <label<?= $errCls('available_from') ?>>Available from<input type="date" name="available_from" value="<?= $v('available_from') ?>" required><?= $errMsg('available_from') ?></label>
      <label<?= $errCls('available_to') ?>>Available until <small>(optional)</small><input type="date" name="available_to" value="<?= $v('available_to') ?>"><?= $errMsg('available_to') ?></label>
    </div>
    <p class="small muted">Listings expire automatically after the “available until” date or after 60 days — we’ll email you a renew link before that happens.</p>
  </fieldset>

  <fieldset>
    <legend>Details</legend>
    <label<?= $errCls('description') ?>>Description <small>What’s included, the space, the building, the area, who it suits.</small>
      <textarea name="description" rows="8" maxlength="6000" required><?= $v('description') ?></textarea><?= $errMsg('description') ?></label>
    <div class="amen-pick">
      <p><strong>Amenities</strong></p>
      <?php foreach (amenity_options() as $k => $t): ?><label class="chk"><input type="checkbox" name="amenities[]" value="<?= e($k) ?>"<?= in_array($k, $amSel, true) ? ' checked' : '' ?>> <?= e($t) ?></label><?php endforeach; ?>
    </div>
    <label>House rules <small>(quiet hours, smoking, guests, cleaning…)</small><textarea name="house_rules" rows="4" maxlength="2000"><?= $v('house_rules') ?></textarea></label>
    <p class="small muted">Describe the place, not the person you want. Listings can’t state preferences based on race, color, religion, sex, disability, familial status, national origin or other protected traits. <a href="/fair-housing/" target="_blank">Fair housing guide</a>.</p>
  </fieldset>

  <fieldset>
    <legend>Photos</legend>
    <?php if ($photos): ?>
      <div class="photo-admin">
        <?php foreach ($photos as $p): ?>
          <label class="ph-item"><img src="/photo/<?= (int)$p['id'] ?>.webp" alt="" width="160" height="110" loading="lazy"><span><input type="checkbox" name="delete_photos[]" value="<?= (int)$p['id'] ?>"> Delete</span></label>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
    <label>Add photos <small>JPG, PNG, WebP or GIF · up to <?= MAX_PHOTOS ?> photos · 15 MB each. Only upload photos you took yourself.</small>
      <input type="file" name="photos[]" accept="image/jpeg,image/png,image/webp,image/gif" multiple></label>
  </fieldset>

  <?php if ($mode !== 'owner' && $mode !== 'new'): ?>
  <fieldset>
    <legend>Your contact details</legend>
    <div class="row3">
      <label<?= $errCls('contact_name') ?>>Your name<input type="text" name="contact_name" value="<?= $v('contact_name') ?>" maxlength="120" required autocomplete="name"><?= $errMsg('contact_name') ?></label>
      <label<?= $errCls('contact_email') ?>>Email<input type="email" name="contact_email" value="<?= $v('contact_email') ?>" maxlength="190" required autocomplete="email"><?= $errMsg('contact_email') ?></label>
      <label>Phone <small>(optional, shown on verified listings only)</small><input type="tel" name="contact_phone" value="<?= $v('contact_phone') ?>" maxlength="40" autocomplete="tel"></label>
    </div>
    <p class="small muted">On free listings your email and phone are never shown — renters message you through The Sublet’s relay.</p>
  </fieldset>
  <?php else: ?>
  <fieldset>
    <legend>Contact details shown on your verified listing</legend>
    <div class="row3">
      <label>Name<input type="text" name="contact_name" value="<?= $v('contact_name') ?>" maxlength="120"></label>
      <label>Phone <small>(optional)</small><input type="tel" name="contact_phone" value="<?= $v('contact_phone') ?>" maxlength="40"></label>
    </div>
    <p class="small muted">Messages are sent to your account email.</p>
  </fieldset>
  <?php endif; ?>

  <?php if ($mode === 'submit' || $mode === 'new'): ?>
  <label class="chk agree"><input type="checkbox" name="agree" value="1" required<?= !empty($d['agree']) ? ' checked' : '' ?>> I have the right to rent this place (my lease or landlord allows it), I’ll follow local short-term-rental laws and fair housing rules, and I accept the <a href="/terms/" target="_blank">terms</a>.</label>
  <?= isset($err['agree']) ? '<p class="err">' . e($err['agree']) . '</p>' : '' ?>
  <?php endif; ?>
  <div class="form-actions">
    <button class="btn btn-lg" type="submit"><?= e($submitLabel ?? 'Save') ?></button>
  </div>
</form>
