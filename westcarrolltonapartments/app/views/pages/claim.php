<?php defined('WCA') || exit; $price = listing_price_cents() / 100; ?>
<div class="wrap narrow section">
  <h1>Claim <?= e($l['name']) ?></h1>
  <p class="lead">Owners and property managers can claim this listing for a one-time <strong>$<?= $price ?></strong>.</p>
  <div class="claim-grid">
    <div class="card">
      <?php if ($l['claimed']): ?>
        <div class="alert alert-info">This listing has already been claimed by a verified owner. If you believe this is an error, <a href="/contact/?subject=<?= rawurlencode('Claim dispute: ' . $l['name']) ?>">contact us</a>.</div>
      <?php else: ?>
      <?php if ($errors): ?><div class="alert alert-error"><?php foreach ($errors as $er): ?><div><?= e($er) ?></div><?php endforeach; ?></div><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?><?= honeypot_field() ?>
        <label>Your name *<input name="name" required maxlength="120" value="<?= e(post('name')) ?>" autocomplete="name"></label>
        <label>Email *<input type="email" name="email" required maxlength="190" value="<?= e(post('email')) ?>" autocomplete="email"><small class="muted">We'll send a verification link here to activate your owner account.</small></label>
        <label class="check"><input type="checkbox" name="confirm" value="1" required> I am the owner, manager or an authorized representative of <?= e($l['name']) ?>.</label>
        <button class="btn btn-accent btn-block" type="submit">Continue to secure payment – $<?= $price ?></button>
        <p class="small muted center">Have a promo code? Enter it on the secure Stripe payment page. Payments are processed by Stripe; we never see your card number.</p>
      </form>
      <?php endif; ?>
    </div>
    <div>
      <h2 class="h4">What you get</h2>
      <ul class="checks">
        <li>Your phone, email, website and office hours shown on the listing</li>
        <li>An owner account (sign in by email link, no password to remember)</li>
        <li>Edit rents, floor plans, amenities, pet policy and description anytime</li>
        <li>Upload up to 12 real photos to replace the stock images</li>
        <li>"Verified owner" badge and higher placement in results</li>
      </ul>
      <p class="small muted">One-time fee, no subscription. We may contact you to confirm you represent the property; listings claimed by someone without authority are removed and refunded.</p>
      <div class="card mini-listing">
        <img src="<?= e(photo_url($l['photos'][0], true)) ?>" alt="" width="320" height="213">
        <div><strong><?= e($l['name']) ?></strong><br><span class="muted small"><?= e($l['address']) ?>, <?= e($l['city']) ?></span></div>
      </div>
    </div>
  </div>
</div>
