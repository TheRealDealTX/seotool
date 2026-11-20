<?php defined('WCA') || exit; $price = listing_price_cents() / 100; $l = $old; $plan = ($old['plan'] ?? 'free') === 'paid' ? 'paid' : 'free'; ?>
<section class="page-head"><div class="wrap">
  <h1>List your property in West Carrollton</h1>
  <p class="lead">Add your apartment community, townhomes or rental building to the directory. Choose a free reviewed listing or go live instantly with an owner listing.</p>
</div></section>
<div class="wrap section-tight">
  <?php if ($errors): ?><div class="alert alert-error"><?php foreach ($errors as $er): ?><div><?= e($er) ?></div><?php endforeach; ?></div><?php endif; ?>
  <form method="post" enctype="multipart/form-data" class="form submit-form" data-submit-form>
    <?= csrf_field() ?><?= honeypot_field() ?>
    <div class="plans" role="radiogroup" aria-label="Listing plan">
      <label class="plan">
        <input type="radio" name="plan" value="free" <?= $plan === 'free' ? 'checked' : '' ?>>
        <span class="plan-body">
          <span class="plan-name">Free listing</span>
          <span class="plan-price">$0</span>
          <ul><li>Reviewed by our team before publishing</li><li>Photos, details &amp; amenities shown</li><li>Contact details <strong>hidden</strong></li><li>Upgrade any time for $<?= $price ?></li></ul>
        </span>
      </label>
      <label class="plan plan-featured">
        <input type="radio" name="plan" value="paid" <?= $plan === 'paid' ? 'checked' : '' ?>>
        <span class="plan-body">
          <span class="plan-tag">Most popular</span>
          <span class="plan-name">Owner listing</span>
          <span class="plan-price">$<?= $price ?> <small>one-time</small></span>
          <ul><li><strong>Published instantly</strong></li><li>Phone, email &amp; website <strong>shown</strong></li><li>Owner account to edit &amp; manage</li><li>Verified owner badge</li></ul>
        </span>
      </label>
    </div>

    <fieldset>
      <legend>About you</legend>
      <div class="grid-2">
        <label>Your name *<input name="submitter_name" required maxlength="120" value="<?= e($old['submitter_name'] ?? '') ?>" autocomplete="name"></label>
        <label>Your email *<input type="email" name="submitter_email" required maxlength="190" value="<?= e($old['submitter_email'] ?? '') ?>" autocomplete="email"><small class="muted">Owner listings: we'll send an email verification link to create your account.</small></label>
      </div>
    </fieldset>
    <?php partial('partials/listing_form', ['l' => $l, 'showContact' => false]); ?>
    <fieldset>
      <legend>Photos</legend>
      <label>Upload up to 8 photos (JPG, PNG or WebP, max 6 MB each)<input type="file" name="photos[]" accept="image/jpeg,image/png,image/webp" multiple></label>
    </fieldset>
    <p class="small muted">By submitting you confirm the information is accurate and you have the right to share these photos. See our <a href="/terms-of-use/">terms</a>.</p>
    <button class="btn btn-accent" type="submit" data-submit-label>Submit listing</button>
  </form>
</div>
