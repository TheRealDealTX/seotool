<?php
// Listing editor used by the owner dashboard and the admin panel.

function mhr_editor_save($slug, array $l, $admin) {
    [$fields, $err] = mhr_read_editor($admin ? MHR_EDITABLE + MHR_ADMIN_EDITABLE : MHR_EDITABLE);
    if ($err) return $err;
    // Photos: remove, choose cover, add new ones.
    $images = $l['images'];
    $remove = array_map('intval', (array)($_POST['remove_img'] ?? []));
    $kept = [];
    foreach ($images as $i => $img) {
        if (in_array($i, $remove, true)) { mhr_delete_image($img['src']); continue; }
        $kept[$i] = $img;
    }
    $cover = (int)($_POST['cover'] ?? -1);
    if (isset($kept[$cover])) $kept = [$cover => $kept[$cover]] + $kept;
    $kept = array_values($kept);
    [$new, $up_err] = mhr_handle_uploads('photo_files', $fields['title'] ?? $l['title'], max(0, MHR_MAX_PHOTOS - count($kept)));
    $kept = array_merge($kept, $new);
    if ($kept !== $l['images']) $fields['images'] = $kept;
    if (!empty($_POST['photo_credit_clear'])) $fields['photo_note'] = '';
    mhr_save_fields($slug, $fields);
    return $up_err ? array_merge(['Your changes were saved, but some photos were not added:'], $up_err) : [];
}

function mhr_editor_form(array $l, $action, $admin) {
    $val = function ($k) use ($l) {
        $v = $l[$k] ?? '';
        if (is_array($v)) return implode("\n", $v);
        if ($k === 'description') return mhr_html_to_text($v);
        if (in_array($k, ['price', 'beds', 'baths', 'sqft'], true) && !$v) return '';
        return is_bool($v) ? ($v ? '1' : '') : (string)$v;
    };
    $in = function ($k, $label, $type = 'text', $extra = '', $hint = '') use ($val) {
        return '<label class="field" for="ed-' . $k . '"><span>' . e($label) . '</span><input id="ed-' . $k . '" type="' . $type . '" name="' . $k . '" value="' . e($val($k)) . '" ' . $extra . '>'
            . ($hint ? '<small class="muted">' . e($hint) . '</small>' : '') . '</label>';
    };
    $ta = function ($k, $label, $rows = 4, $hint = '', $extra = '') use ($val) {
        return '<label class="field" for="ed-' . $k . '"><span>' . e($label) . '</span><textarea id="ed-' . $k . '" name="' . $k . '" rows="' . $rows . '" ' . $extra . '>' . e($val($k)) . '</textarea>'
            . ($hint ? '<small class="muted">' . e($hint) . '</small>' : '') . '</label>';
    };
    ob_start(); ?>
<form method="post" action="<?= e($action) ?>" class="form mhr-editor" enctype="multipart/form-data">
  <?= mhr_guard_fields(false) ?>
  <input type="hidden" name="do" value="save">
  <fieldset><legend>Basics</legend>
    <div class="form-grid">
      <?= $in('title', 'Property name', 'text', 'required maxlength="150"') ?>
      <label class="field" for="ed-base"><span>Nearest installation</span><select id="ed-base" name="base">
        <?php foreach (bases() as $b): ?><option value="<?= e($b['slug']) ?>"<?= $b['slug'] === $l['base'] ? ' selected' : '' ?>><?= e($b['name']) ?></option><?php endforeach; ?>
      </select></label>
      <?= $in('address', 'Address', 'text', 'maxlength="250"') ?>
      <?= $in('operator', 'Managed by', 'text', 'maxlength="150"') ?>
    </div>
  </fieldset>
  <fieldset><legend>Rent &amp; homes</legend>
    <div class="form-grid">
      <?= $in('price', 'Starting rent ($/mo)', 'number', 'min="0" step="1"', 'Leave blank for BAH-based rent') ?>
      <?= $in('rent_note', 'Rent / BAH notes', 'text', 'maxlength="250"', 'e.g. Rent equals your BAH, utilities included') ?>
      <?= $in('beds', 'Bedrooms', 'number', 'min="0" max="12" step="0.5"') ?>
      <?= $in('baths', 'Bathrooms', 'number', 'min="0" max="12" step="0.5"') ?>
      <?= $in('sqft', 'Area (sq ft)', 'number', 'min="0"') ?>
      <?= $in('beds_range', 'Bedroom range', 'text', 'maxlength="20"', 'e.g. 2–4') ?>
      <?= $in('baths_range', 'Bathroom range', 'text', 'maxlength="20"') ?>
      <?= $in('sqft_range', 'Size range (sq ft)', 'text', 'maxlength="30"') ?>
      <?= $in('pets', 'Pet policy', 'text', 'maxlength="250"') ?>
      <?= $in('utilities', 'Utilities', 'text', 'maxlength="250"') ?>
      <?= $in('eligibility', 'Eligibility', 'text', 'maxlength="250"') ?>
      <?= $in('hours', 'Office hours', 'text', 'maxlength="200"') ?>
    </div>
  </fieldset>
  <fieldset><legend>Description &amp; features</legend>
    <?= $ta('description', 'Description', 8, 'Separate paragraphs with a blank line.', 'maxlength="8000"') ?>
    <div class="form-grid">
      <?= $ta('highlights', 'Highlights', 4, 'One per line') ?>
      <?= $ta('amenities', 'Home features / amenities', 4, 'One per line or comma-separated') ?>
      <?= $ta('nearby', 'Nearby (incl. distance to base)', 4, 'One per line') ?>
      <?= $ta('schools', 'Nearby schools', 4, 'One per line') ?>
    </div>
  </fieldset>
  <fieldset><legend>Contact details</legend>
    <p class="fineprint">Shown on the listing once it's verified.</p>
    <div class="form-grid">
      <?= $in('phone', 'Phone', 'tel', 'maxlength="40"') ?>
      <?= $in('email', 'Email', 'email', 'maxlength="190"') ?>
      <?= $in('website', 'Website', 'text', 'inputmode="url" maxlength="250"', 'https://…') ?>
    </div>
  </fieldset>
  <?php if ($admin): ?>
  <fieldset><legend>Map &amp; display (admin)</legend>
    <div class="form-grid">
      <?= $in('lat', 'Latitude', 'text', 'inputmode="decimal"') ?>
      <?= $in('lng', 'Longitude', 'text', 'inputmode="decimal"') ?>
      <label class="mhr-check"><input type="hidden" name="featured" value=""><input type="checkbox" name="featured" value="1"<?= !empty($l['featured']) ? ' checked' : '' ?>> <span>Featured</span></label>
    </div>
  </fieldset>
  <?php endif; ?>
  <fieldset><legend>Photos</legend>
    <?php if ($l['images']): ?>
    <div class="mhr-photos">
      <?php foreach ($l['images'] as $i => $img): ?>
        <figure class="mhr-photo">
          <img src="<?= e($img['src']) ?>" alt="" loading="lazy">
          <figcaption>
            <label><input type="radio" name="cover" value="<?= $i ?>"<?= $i === 0 ? ' checked' : '' ?>> Cover</label>
            <label><input type="checkbox" name="remove_img[]" value="<?= $i ?>"> Remove</label>
          </figcaption>
        </figure>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
    <label class="field" for="ed-photos"><span>Add photos</span><input id="ed-photos" type="file" name="photo_files[]" accept="image/jpeg,image/png,image/webp,image/gif" multiple>
      <small class="muted">JPEG, PNG, WebP or GIF, up to 10 MB each, <?= MHR_MAX_PHOTOS ?> photos max. Photos are resized and converted automatically.</small></label>
    <?php if (!empty($l['photo_note'])): ?><label class="mhr-check"><input type="checkbox" name="photo_credit_clear" value="1"> <span>Remove photo note: “<?= e($l['photo_note']) ?>”</span></label><?php endif; ?>
  </fieldset>
  <div class="btn-row"><button class="btn btn-primary btn-lg" type="submit"><?= icon('check') ?> Save changes</button></div>
</form>
<?php
    return ob_get_clean();
}
