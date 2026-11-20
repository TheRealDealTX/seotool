<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page narrow">
  <h1 class="h2">Settings</h1>
  <form method="post" class="form card">
    <?= csrf_field() ?><input type="hidden" name="action" value="save">
    <h2 class="h4">Stripe payments</h2>
    <p class="small">Get keys at <a href="https://dashboard.stripe.com/apikeys" target="_blank" rel="noopener">dashboard.stripe.com/apikeys</a>. Use a <code>sk_test_…</code> key to test, then switch to <code>sk_live_…</code>.</p>
    <label>Secret key <?= $stripe_key_hint ? '<small class="muted">(current: ' . e($stripe_key_hint) . ')</small>' : '' ?><input name="stripe_secret_key" type="password" autocomplete="off" placeholder="<?= $stripe_key_hint ? 'leave blank to keep' : 'sk_live_...' ?>"></label>
    <label>Webhook signing secret <?= $webhook_set ? '<small class="muted">(set)</small>' : '' ?><input name="stripe_webhook_secret" type="password" autocomplete="off" placeholder="whsec_..."></label>
    <p class="small muted">In Stripe → Developers → Webhooks, add endpoint <code><?= e(url('/stripe/webhook')) ?></code> for the event <code>checkout.session.completed</code>, then paste its signing secret here. (Payments also confirm when the buyer returns to the site, the webhook is a backup.)</p>
    <label>Listing / claim price (USD)<input name="price" type="number" step="0.01" min="0.5" value="<?= e($price) ?>"></label>
    <label class="check"><input type="checkbox" name="clear_stripe" value="1"> Disconnect Stripe (clear keys)</label>
    <button class="btn">Save settings</button>
  </form>
  <div class="card">
    <h2 class="h4">Diagnostics</h2>
    <form method="post" class="inline"><?= csrf_field() ?>
      <button class="btn btn-ghost btn-sm" name="action" value="test_email">Send test email</button>
      <button class="btn btn-ghost btn-sm" name="action" value="test_stripe">Test Stripe connection</button>
    </form>
  </div>
</div>
