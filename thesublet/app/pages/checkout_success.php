<?php defined('APP') || exit;

cache_private();
$sid = get('session_id');
$l = null; $done = false;
if (preg_match('/^cs_[A-Za-z0-9_]+$/', $sid) && stripe_ready()) {
    try {
        $s = stripe_api('GET', 'checkout/sessions/' . $sid);
        $ownerId = fulfil_checkout($s);   // idempotent; the webhook does the same
        $done = $ownerId !== null;
        $l = listing_get((int)($s['metadata']['listing_id'] ?? 0));
    } catch (Throwable $e) {
        error_log('[stripe success] ' . $e->getMessage());
    }
}
ob_start(); ?>
<div class="wrap narrow section center">
<?php if ($done && $l): ?>
  <h1>🎉 You’re verified — your listing is live</h1>
  <p>“<?= e($l['title']) ?>” is published on The Sublet with a Verified host badge.</p>
  <p>We’ve emailed <strong><?= e($l['contact_email']) ?></strong> a secure sign-in link. Click it to <strong>verify your email</strong> — that switches on your public contact details and opens your dashboard, where you can edit the listing, add photos, renew it or mark it rented.</p>
  <p><a class="btn" href="<?= e(listing_url($l)) ?>">View your listing</a> <a class="btn btn-ghost" href="/login/">Send me a sign-in link</a></p>
<?php else: ?>
  <h1>Thanks — we’re confirming your payment</h1>
  <p>Stripe is finishing up. Your listing will go live within a minute or two and we’ll email you a sign-in link. If nothing arrives in 15 minutes, <a href="/contact/">contact us</a>.</p>
<?php endif; ?>
</div>
<?php
page(['title' => 'Payment received | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
