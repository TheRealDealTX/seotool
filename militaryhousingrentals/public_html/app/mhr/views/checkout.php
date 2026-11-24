<?php
// /checkout/success/?session_id=… and /checkout/cancel/?p=…&s=…
$ok = null; $msg = ''; $p = null; $paid_now = false;

if ($sub === '/success/') {
    $sid = (string)($_GET['session_id'] ?? '');
    if (preg_match('/^cs_[A-Za-z0-9_]{10,250}$/', $sid)) {
        $s = mhr_stripe('GET', '/v1/checkout/sessions/' . $sid, [], $err);
        if ($s && mhr_session_paid($s)) {
            $p = mhr_fulfil($s);
            $paid_now = (bool)$p;
        } elseif ($s) {
            $p = mhr_row('SELECT * FROM mhr_payments WHERE stripe_session_id = ?', [$sid]);
        }
    }
    if ($p) {
        mhr_session_start();
        // Sign in the browser that started this checkout.
        if (in_array((int)$p['id'], array_map('intval', $_SESSION['mhr_checkout'] ?? []), true) && $p['status'] === 'fulfilled') mhr_owner_login($p['owner_id']);
    }
    $title = 'Payment received';
} elseif ($sub === '/cancel/') {
    $pid = (int)($_GET['p'] ?? 0);
    if ($pid && hash_equals(substr(mhr_hmac('cancel|' . $pid), 0, 20), (string)($_GET['s'] ?? ''))) {
        $p = mhr_row('SELECT * FROM mhr_payments WHERE id = ?', [$pid]);
        if ($p && $p['status'] === 'pending') {
            mhr_q("UPDATE mhr_payments SET status = 'cancelled' WHERE id = ?", [$pid]);
            if ($p['kind'] === 'submit') {
                $row = mhr_row_for($p['listing_slug']);
                if ($row && $row['status'] === 'pending' && $row['plan'] === 'paid') {
                    mhr_set_cols($p['listing_slug'], ['plan' => 'free']);
                    [$l] = mhr_listing_full($p['listing_slug']);
                    mhr_mail($p['email'], 'We received your property: ' . ($l['title'] ?? ''), mhr_free_received_email($p['name'], $l['title'] ?? ''));
                }
            }
        }
    }
    $title = 'Checkout cancelled';
} else {
    not_found();
}

[$l] = $p ? mhr_listing_full($p['listing_slug']) : [null];
mhr_page_start($title, '/checkout' . $sub);
?>
<section class="section">
  <div class="wrap mhr-narrow">
    <div class="card form-card">
<?php if ($sub === '/success/'): ?>
  <?php if ($p && $p['status'] === 'fulfilled'): ?>
      <div class="mhr-big-icon mhr-ok"><?= icon('check') ?></div>
      <h1>Thank you, you're verified!</h1>
      <?php if ($p['note']): ?>
        <p>Your payment for <strong><?= e($l['title'] ?? '') ?></strong> was received. Our team will review the listing and get back to you shortly.</p>
      <?php else: ?>
        <p><strong><?= e($l['title'] ?? '') ?></strong> now shows your contact details and a <span class="mhr-badge"><?= icon('check') ?> Verified owner</span> badge.</p>
      <?php endif; ?>
      <p>We've emailed your receipt to <strong><?= e($p['email']) ?></strong>, along with a link to confirm your email address.</p>
      <div class="btn-row">
        <?php if (!$p['note']): ?><a class="btn btn-primary" href="/properties/<?= e($p['listing_slug']) ?>/">View your listing</a><?php endif; ?>
        <a class="btn btn-outline" href="/account/">Go to your owner dashboard</a>
      </div>
  <?php elseif ($p): ?>
      <h1>We're confirming your payment</h1>
      <p>Stripe hasn't confirmed this payment yet. That usually takes a few seconds. We'll email <strong><?= e($p['email']) ?></strong> as soon as it's done.</p>
      <p><a class="btn btn-outline" href="">Refresh</a></p>
  <?php else: ?>
      <h1>We couldn't find that payment</h1>
      <p>If you were charged, don't worry: you'll get an email receipt and your listing will update automatically. Questions? <a href="/contact-us/">Contact us</a>.</p>
  <?php endif; ?>
<?php else: ?>
      <h1>Checkout cancelled</h1>
      <?php if ($p && $p['kind'] === 'submit'): ?>
        <p>No payment was taken. We've kept your property <strong><?= e($l['title'] ?? '') ?></strong> as a <strong>free listing</strong>: our team will review it, and once approved it's published with contact details hidden.</p>
        <p>You can upgrade for <?= e(mhr_price_label()) ?> at any time from the link we'll email you.</p>
      <?php else: ?>
        <p>No payment was taken. You can claim the listing any time.</p>
        <?php if ($p): ?><p><a class="btn btn-primary" href="/claim/<?= e($p['listing_slug']) ?>/">Try again</a> <a class="btn btn-light" href="/properties/<?= e($p['listing_slug']) ?>/">Back to the listing</a></p><?php endif; ?>
      <?php endif; ?>
<?php endif; ?>
    </div>
  </div>
</section>
<?php layout_end();
