<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
if (is_post()) {
    admin_guard_post();
    $do = post('do');
    if ($do === 'save') {
        $price = (float)post('price_usd');
        if ($price >= 0.5 && $price <= 1000) setting_set('price_usd', (string)round($price, 2));
        foreach (['stripe_publishable' => '/^(pk_(test|live)_[A-Za-z0-9]+)?$/', 'stripe_secret' => '/^((sk|rk)_(test|live)_[A-Za-z0-9]+)?$/',
                  'stripe_webhook_secret' => '/^(whsec_[A-Za-z0-9]+)?$/', 'gtm_id' => '/^(GTM-[A-Z0-9]+)?$/', 'gsc_meta' => '/^[A-Za-z0-9_\-]{0,100}$/'] as $k => $re) {
            $v = post($k);
            if ($v === '********') continue; // unchanged secret
            if (!preg_match($re, $v)) { flash("Invalid value for $k — not saved.", 'err'); continue; }
            setting_set($k, $v);
        }
        flash('Settings saved.');
    } elseif ($do === 'password') {
        $p1 = post('pass1');
        if (strlen($p1) < 12 || $p1 !== post('pass2')) flash('Passwords must match and be at least 12 characters.', 'err');
        else { setting_set('admin_pass_hash', password_hash($p1, PASSWORD_DEFAULT)); flash('Admin password changed.'); }
    } elseif ($do === 'test_email') {
        $to = post('to');
        if (!valid_email($to)) flash('Enter a valid address.', 'err');
        else {
            $ok = send_mail($to, 'Test email from The Sublet', '<p>This is a test email from the thesublet.com admin panel. SMTP is working 🎉</p>', null, $error);
            flash($ok ? "Test email sent to $to." : 'Sending failed: ' . $error, $ok ? 'ok' : 'err');
        }
    } elseif ($do === 'cron') {
        $r = run_expiry_jobs();
        flash("Expiry job ran: {$r['expired']} expired, {$r['reminders']} reminders sent.");
    }
    redirect('/admin/settings/');
}
$mask = fn($k) => setting($k) ? '********' : '';
$wh = base_url('/stripe/webhook');
ob_start(); ?>
<form method="post" class="stack settings"><?= csrf_field() ?><input type="hidden" name="do" value="save">
  <h2>Pricing</h2>
  <label>Verified listing price (USD)<input type="number" name="price_usd" step="0.01" min="0.5" value="<?= e(setting('price_usd', '10')) ?>"></label>
  <h2>Stripe</h2>
  <p class="small muted">Webhook endpoint: <code><?= e($wh) ?></code> — event <code>checkout.session.completed</code> (optionally also <code>checkout.session.async_payment_succeeded</code> and <code>checkout.session.expired</code>). Leave a secret field as ******** to keep it unchanged.</p>
  <label>Publishable key<input name="stripe_publishable" value="<?= e(setting('stripe_publishable', '')) ?>" placeholder="pk_live_…" autocomplete="off"></label>
  <label>Secret key<input name="stripe_secret" value="<?= e($mask('stripe_secret')) ?>" placeholder="sk_live_… or rk_live_…" autocomplete="off"></label>
  <label>Webhook signing secret<input name="stripe_webhook_secret" value="<?= e($mask('stripe_webhook_secret')) ?>" placeholder="whsec_…" autocomplete="off"></label>
  <p class="small">Status: <?= stripe_ready() ? '✔ payments enabled' : '✖ no secret key — verified listings fall back to the free review queue' ?></p>
  <h2>Tracking &amp; verification</h2>
  <label>Google Tag Manager container ID<input name="gtm_id" value="<?= e(setting('gtm_id', '')) ?>" placeholder="GTM-XXXXXXX"></label>
  <label>Google Search Console meta verification code <small>(content="…" value only; or upload the HTML file to the site root)</small><input name="gsc_meta" value="<?= e(setting('gsc_meta', '')) ?>"></label>
  <button class="btn" type="submit">Save settings</button>
</form>
<hr>
<form method="post" class="stack"><?= csrf_field() ?><input type="hidden" name="do" value="test_email">
  <h2>Send a test email</h2>
  <p class="small muted">Sends through <?= e(cfg('smtp.user')) ?> via <?= e(cfg('smtp.host')) ?>:<?= (int)cfg('smtp.port') ?>.</p>
  <label>To<input type="email" name="to" required value="<?= e(cfg('admin_notify')) ?>"></label>
  <button class="btn btn-ghost" type="submit">Send test email</button>
</form>
<hr>
<form method="post" class="stack"><?= csrf_field() ?><input type="hidden" name="do" value="password">
  <h2>Change admin password</h2>
  <label>New password<input type="password" name="pass1" minlength="12" required autocomplete="new-password"></label>
  <label>Repeat<input type="password" name="pass2" minlength="12" required autocomplete="new-password"></label>
  <button class="btn btn-ghost" type="submit">Change password</button>
</form>
<hr>
<form method="post"><?= csrf_field() ?><input type="hidden" name="do" value="cron"><h2>Maintenance</h2><p class="small muted">Expiry runs automatically about once an hour; last run: <?= setting('last_cron') ? e(gmdate('Y-m-d H:i', (int)setting('last_cron'))) . ' UTC' : 'never' ?>.</p><button class="btn btn-ghost btn-sm">Run expiry &amp; reminders now</button></form>
<?php
admin_page('Settings', ob_get_clean());
