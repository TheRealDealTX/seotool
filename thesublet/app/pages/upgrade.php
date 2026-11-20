<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
$t = get('t');
if (!$l || !sign_ok('upgrade:' . $l['id'] . ':' . $l['contact_email'], $t)) not_found('That upgrade link is invalid or has expired.');
ob_start(); ?>
<div class="wrap narrow section">
  <h1>Upgrade to a verified listing</h1>
  <p class="lead">“<?= e($l['title']) ?>” — <?= e($l['city'] . ', ' . $l['state']) ?></p>
  <?php if ($l['tier'] === 'paid'): ?>
    <p>This listing is already verified. <a href="/login/">Sign in to your dashboard</a>.</p>
  <?php else: ?>
  <ul class="ticks">
    <li>Published immediately<?= $l['status'] === 'pending' ? ' — skip the review queue' : '' ?></li>
    <li>Your contact details shown to renters</li>
    <li>“Verified host” badge and higher placement in search</li>
    <li>An owner dashboard: edit details, upload photos, renew, mark rented</li>
  </ul>
  <p>One-time fee: <strong><?= e(price_label()) ?></strong>. Promo codes can be entered at checkout.</p>
  <?php if (stripe_ready()): ?>
  <form method="post" action="/checkout/start/<?= (int)$l['id'] ?>/"><?= csrf_field() ?><input type="hidden" name="kind" value="upgrade"><input type="hidden" name="t" value="<?= e($t) ?>"><button class="btn btn-lg" type="submit">Continue to secure checkout</button></form>
  <?php else: ?><p class="flash flash-warn">Card payments aren’t switched on yet — please check back soon.</p><?php endif; ?>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Upgrade your listing | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
