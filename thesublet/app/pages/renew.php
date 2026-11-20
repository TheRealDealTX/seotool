<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
$t = get('t');
if (!$l || !sign_ok('renew:' . $l['id'] . ':' . $l['contact_email'], $t)) not_found('That renew link is invalid.');
$msg = null; $ok = false;
if (is_post()) {
    if ($g = form_guard()) $msg = $g;
    elseif (!in_array($l['status'], ['active', 'expired'], true)) $msg = 'This listing can’t be renewed (status: ' . listing_status_label($l['status']) . ').';
    elseif ($l['available_to'] && $l['available_to'] < date('Y-m-d', time() + 86400)) $msg = 'Your “available until” date has passed. ' . ($l['tier'] === 'paid' ? 'Sign in to your dashboard to update the dates, then renew.' : 'Please submit a new listing with updated dates, or contact us.');
    else {
        update('listings', ['status' => 'active', 'expires_at' => compute_expiry($l['available_to']), 'reminder_sent_at' => null, 'updated_at' => now()], 'id = ?', [(int)$l['id']]);
        $l = listing_get((int)$l['id']);
        $ok = true;
        $msg = 'Renewed! Your listing now runs until ' . fmt_date($l['expires_at']) . '.';
    }
}
ob_start(); ?>
<div class="wrap narrow section">
  <h1>Renew your listing</h1>
  <p class="lead">“<?= e($l['title']) ?>”</p>
  <?php if ($msg): ?><div class="flash <?= $ok ? 'flash-ok' : 'flash-err' ?>"><?= e($msg) ?></div><?php endif; ?>
  <p>Status: <strong><?= e(listing_status_label($l['status'])) ?></strong><?= $l['expires_at'] ? ' · expires ' . e(fmt_date($l['expires_at'])) : '' ?></p>
  <?php if (!$ok): ?>
  <form method="post"><?= csrf_field() ?><button class="btn" type="submit">Renew for up to <?= LISTING_DAYS ?> more days</button></form>
  <?php else: ?><p><a class="btn" href="<?= e(listing_url($l)) ?>">View listing</a></p><?php endif; ?>
  <p class="small muted">Already rented? Reply to the reminder email or <a href="/contact/">contact us</a> and we’ll take it down.</p>
</div>
<?php
page(['title' => 'Renew listing | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
