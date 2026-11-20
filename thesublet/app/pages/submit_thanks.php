<?php defined('APP') || exit;

cache_private();
session_boot();
$l = !empty($_SESSION['last_submit']) ? listing_get((int)$_SESSION['last_submit']) : null;
ob_start(); ?>
<div class="wrap narrow section center">
  <?= flashes() ?>
  <h1>Thanks — your listing is in the review queue</h1>
  <?php if ($l): ?><p>“<?= e($l['title']) ?>” will be checked by a member of The Sublet team, usually within one to two days. We’ve emailed <strong><?= e($l['contact_email']) ?></strong> a confirmation.</p><?php endif; ?>
  <p>Once it’s approved, it goes live with your contact details hidden — renters reach you through our message relay.</p>
  <div class="tier tier-hi" style="max-width:520px;margin:2rem auto;text-align:left">
    <h2 class="h3">Want it live right now?</h2>
    <p>Upgrade to a verified listing for <?= e(price_label()) ?>: published instantly, contact details shown, a “Verified host” badge and a dashboard to manage photos and dates.</p>
    <?php if ($l && stripe_ready()): ?>
      <form method="post" action="/checkout/start/<?= (int)$l['id'] ?>/"><?= csrf_field() ?><input type="hidden" name="kind" value="upgrade"><input type="hidden" name="t" value="<?= e(sign('upgrade:' . $l['id'] . ':' . $l['contact_email'])) ?>"><button class="btn" type="submit">Upgrade for <?= e(price_label()) ?></button></form>
    <?php else: ?>
      <p class="small muted">We’ll include an upgrade link in your approval email.</p>
    <?php endif; ?>
  </div>
  <p><a href="/">Back to The Sublet</a></p>
</div>
<?php
page(['title' => 'Listing received | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
