<?php
// /submit-property/: free listing (admin review, contact hidden) or paid
// verified listing (published at once with contact details). Handling lives in
// app/mhr/submit.php.
$res = mhr_submit_handle();
$v = $res['values'];
$val = fn($k) => e($v[$k] ?? '');
$plan = $v['plan'] ?? 'free';
$price = mhr_price_label();
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Submit Property', null]]);
header('Cache-Control: no-store, no-cache, must-revalidate');
layout_start(['title' => 'Submit Your Military Housing Rental Property', 'description' => 'List your rental property on Military Housing Rentals and reach service members and military families looking for housing near base.',
    'path' => '/submit-property/', 'nav' => '/submit-property/', 'schema' => [$crumb_schema], 'head_extra' => mhr_css_link()]);
$field = function ($name, $label, $type = 'text', $req = false, $extra = '', $hint = '') use ($val) {
    $star = $req ? ' <span class="req" aria-hidden="true">*</span>' : '';
    return '<label class="field" for="f-' . $name . '"><span>' . e($label) . $star . '</span><input id="f-' . $name . '" type="' . $type . '" name="' . $name . '" value="' . $val($name) . '"' . ($req ? ' required' : '') . ' ' . $extra . '>'
        . ($hint ? '<small class="muted">' . e($hint) . '</small>' : '') . '</label>';
};
?>
<section class="page-hero">
  <div class="wrap"><?= $crumbs ?><p class="eyebrow">For landlords, owners &amp; agents</p><h1>Submit your property for listing</h1>
  <p class="lead">Have a rental that would be a great fit for service members and military families? Submit it here to be featured on Military Housing Rentals.</p></div>
</section>
<section class="section section-tight">
  <div class="wrap contact-layout">
    <div class="card form-card">
      <ol class="form-steps" aria-hidden="true"><li class="on">Your details</li><li>Property</li><li>Rent &amp; features</li><li>Description &amp; photos</li></ol>
      <?php if ($res['state'] === 'free'): ?>
        <div class="notice notice-ok" role="status"><?= icon('check') ?> Thank you! We received your property. Our team will review it and email you once it's live.</div>
        <?php if ($res['errors']): ?><div class="notice notice-err" role="alert"><ul><?php foreach ($res['errors'] as $x): ?><li><?= e($x) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
      <?php elseif ($res['state'] === 'error'): ?>
        <?= mhr_errors_html($res['errors']) ?>
      <?php endif; ?>
      <form method="post" action="/submit-property/" class="form" enctype="multipart/form-data" novalidate data-form data-steps>
        <?= mhr_guard_fields() ?>
        <fieldset data-step>
          <legend>Your details</legend>
          <div class="form-grid">
            <?= $field('name', 'Your name', 'text', true, 'autocomplete="name" maxlength="120"') ?>
            <?= $field('email', 'Your email', 'email', true, 'autocomplete="email" maxlength="190"') ?>
            <?= $field('phone', 'Your phone', 'tel', true, 'autocomplete="tel" maxlength="40"') ?>
          </div>
          <div class="mhr-plans" role="radiogroup" aria-label="Listing type">
            <label class="mhr-plan">
              <input type="radio" name="plan" value="free"<?= $plan !== 'paid' ? ' checked' : '' ?>>
              <span class="mhr-plan-body"><strong>Free listing</strong><span class="mhr-plan-price">$0</span>
                <span class="muted">Reviewed by our team, then published with contact details hidden. Upgrade any time.</span></span>
            </label>
            <label class="mhr-plan">
              <input type="radio" name="plan" value="paid"<?= $plan === 'paid' ? ' checked' : '' ?>>
              <span class="mhr-plan-body"><strong>Verified listing</strong><span class="mhr-plan-price"><?= e($price) ?> <small>one-time</small></span>
                <span class="muted">Published instantly as a Featured listing (shown first in search) with your phone, email and website, a Verified owner badge and an owner dashboard.</span></span>
            </label>
          </div>
          <label class="mhr-check mhr-paid-only"><input type="checkbox" name="authorized" value="1"> <span>For a verified listing: I'm the owner, property manager or an authorized representative.</span></label>
        </fieldset>
        <fieldset data-step>
          <legend>Property</legend>
          <div class="form-grid">
            <?= $field('pname', 'Property name', 'text', true, 'maxlength="150"') ?>
            <?= $field('address', 'Address', 'text', true, 'autocomplete="street-address" maxlength="250"', 'Street, city, state and ZIP') ?>
            <label class="field" for="f-base"><span>Nearest installation <span class="req" aria-hidden="true">*</span></span>
              <select id="f-base" name="base" required>
                <option value="">Choose a base…</option>
                <?php foreach (bases() as $b): ?><option value="<?= e($b['slug']) ?>"<?= in_array($v['base'] ?? '', [$b['slug'], $b['name']], true) ? ' selected' : '' ?>><?= e($b['name']) ?></option><?php endforeach; ?>
              </select>
            </label>
            <?= $field('proximity', 'Distance to base', 'text', false, 'maxlength="80" placeholder="e.g. 10 minutes / 4 miles"', 'How far to the main gate') ?>
            <?= $field('operator', 'Managed by', 'text', false, 'maxlength="150" placeholder="Owner, property manager or company"') ?>
          </div>
        </fieldset>
        <fieldset data-step>
          <legend>Rent &amp; features</legend>
          <div class="form-grid">
            <?= $field('price', 'Starting rent ($/mo)', 'text', false, 'inputmode="numeric" maxlength="12" placeholder="1800"') ?>
            <?= $field('beds', 'Bedrooms', 'number', false, 'min="0" max="12"') ?>
            <?= $field('bath', 'Bathrooms', 'number', false, 'min="0" max="12" step="0.5"') ?>
            <?= $field('area', 'Area (sq ft)', 'number', false, 'min="0"') ?>
            <?= $field('pets', 'Pet policy', 'text', false, 'maxlength="250" placeholder="e.g. 2 pets, no breed restrictions"') ?>
            <?= $field('utilities', 'Utilities', 'text', false, 'maxlength="250" placeholder="e.g. Water and trash included"') ?>
            <?= $field('eligibility', 'Who can rent', 'text', false, 'maxlength="250" placeholder="e.g. Active duty, veterans, DoD civilians"') ?>
            <?= $field('rent_note', 'BAH notes', 'text', false, 'maxlength="250" placeholder="e.g. Rent at or below E-5 BAH, SCRA military clause"') ?>
          </div>
          <label class="mhr-check"><input type="checkbox" name="bah" value="1"<?= !empty($v['bah']) ? ' checked' : '' ?>> <span>BAH-friendly: rent fits within the local BAH</span></label>
          <label class="field" for="f-amenities"><span>Property amenities</span><textarea id="f-amenities" name="amenities" rows="4" maxlength="5000" placeholder="Garage, fenced yard, washer/dryer…"><?= $val('amenities') ?></textarea></label>
          <p class="fineprint">Public contact details (shown once the listing is verified):</p>
          <div class="form-grid">
            <?= $field('listing_phone', 'Listing phone', 'tel', false, 'maxlength="40"', 'Leave blank to use your phone') ?>
            <?= $field('listing_email', 'Listing email', 'email', false, 'maxlength="190"') ?>
            <?= $field('website', 'Website', 'text', false, 'inputmode="url" autocomplete="url" maxlength="250" placeholder="https://"') ?>
          </div>
        </fieldset>
        <fieldset data-step>
          <legend>Description &amp; photos</legend>
          <label class="field" for="f-description"><span>Property description <span class="req" aria-hidden="true">*</span></span><textarea id="f-description" name="description" rows="6" required maxlength="5000"><?= $val('description') ?></textarea></label>
          <label class="field" for="f-files"><span>Photos</span><input id="f-files" type="file" name="photo_files[]" accept="image/jpeg,image/png,image/webp,image/gif" multiple>
            <small class="muted">Up to <?= MHR_MAX_PHOTOS ?> JPEG, PNG, WebP or GIF photos, 10 MB each. The first photo is the cover.</small></label>
          <?= $field('photos', 'Or a link to your photos (Google Drive etc.)', 'url', false, 'placeholder="https://drive.google.com/…"') ?>
        </fieldset>
        <div class="step-nav">
          <button class="btn btn-light" type="button" data-step-prev hidden>Back</button>
          <button class="btn btn-primary" type="button" data-step-next>Next <?= icon('arrow') ?></button>
          <button class="btn btn-accent btn-lg" type="submit" data-step-submit><?= icon('check') ?> Submit property</button>
        </div>
      </form>
    </div>
    <aside class="contact-aside">
      <div class="card">
        <h3>How it works</h3>
        <ol class="mini-steps">
          <li>Submit your property details and photos.</li>
          <li><strong>Free:</strong> our team reviews it and publishes it with contact details hidden. Upgrade for <?= e($price) ?> any time.</li>
          <li><strong>Verified (<?= e($price) ?>):</strong> pay securely via Stripe and your listing goes live instantly as a Featured listing with your contact details.</li>
        </ol>
        <p class="fineprint">Your contact details are used only for verification, confirmation and communication about your listing, never for anything else.</p>
        <p>Already listed? <a href="/account/">Owner login</a>. Need help? <a href="/contact-us/">Contact us</a> or call <a href="<?= e(cfg('phone_href')) ?>"><?= e(cfg('phone')) ?></a>.</p>
      </div>
      <?= sidebar_listings() ?>
    </aside>
  </div>
</section>
<?php layout_end();
