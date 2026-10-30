<?php
// GET /order/complete/?session_id=cs_... - Stripe sends the buyer here after paying.
require_once __DIR__ . '/../../inc/store.php';
$sid = (string)($_GET['session_id'] ?? '');
$order = null;
$state = 'invalid';
if (preg_match('/^cs_[A-Za-z0-9_]{10,200}$/', $sid)) {
    $order = load_order($sid);
    if (!$order) {
        try {
            $session = stripe_api('GET', '/checkout/sessions/' . $sid);
            $order = fulfill_session($session);
            $state = $order ? 'paid' : (($session['status'] ?? '') === 'complete' ? 'processing' : 'unpaid');
        } catch (Throwable $e) {
            error_log('complete: ' . $e->getMessage());
            $state = 'error';
        }
    }
    if ($order) $state = 'paid';
}
$p = $order ? $PLANS[$order['plan']] : null;
$set = $order ? (plan_sets()[$order['plan']] ?? null) : null;
header('Cache-Control: private, no-store');
page_start(['robots' => 'noindex,nofollow', 'title' => ($state === 'paid' ? 'Your Plan Files' : 'Order Status') . ' | ' . SITE_NAME]);
?>
<section class="section"><div class="narrow">
<?php if ($state === 'paid'): ?>
  <div class="panel order-done">
    <p class="eyebrow">Order <?= e($order['id']) ?></p>
    <h1 style="font-size:2.1rem">Thank you! Your plan set is ready.</h1>
    <p class="lead"><?= e($order['plan_name']) ?></p>
    <p><a class="btn btn-wood" href="<?= e(download_url($order)) ?>"><?= icon('arrow') ?> Download the complete plan set<?= $set ? ' (' . number_format($set['zip_bytes'] / 1e6, 1) . ' MB zip)' : '' ?></a></p>
    <p class="form-note">We also emailed this link to <strong><?= e($order['email']) ?></strong>. It works for <?= DOWNLOAD_DAYS ?> days and up to <?= DOWNLOAD_MAX ?> downloads; you can get a new one any time at <a href="/order/lookup/">Find my plan download</a>.</p>
    <?php if ($set): ?>
    <h2 style="font-size:1.3rem;margin-top:1.4em">What is in the zip</h2>
    <ul class="file-list">
      <?php foreach ($set['files'] as [$name, $bytes]): ?>
        <li><span><?= e($name) ?></span><span class="muted"><?= $bytes > 1e6 ? number_format($bytes / 1e6, 1) . ' MB' : number_format(max(1, $bytes / 1e3)) . ' KB' ?></span></li>
      <?php endforeach; ?>
    </ul>
    <?php endif; ?>
    <h2 style="font-size:1.3rem;margin-top:1.4em">Next steps</h2>
    <ol>
      <li>Open the drawing set PDF and check sheet A0.0 for the design loads and code notes.</li>
      <li>Ask your building department what it needs for a permit. Many require an engineer's or architect's stamp.</li>
      <li>Take the materials list and cost estimate to local suppliers and builders for quotes.</li>
      <li>Need changes? Reply to your order email or call <a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a>.</li>
    </ol>
  </div>
<?php elseif ($state === 'processing'): ?>
  <div class="panel"><h1 style="font-size:2rem">Payment processing</h1>
    <p>Your payment is still being confirmed by the bank. As soon as it clears, we will email your download link. This page will also show it if you <a href="">refresh</a> in a minute.</p></div>
<?php elseif ($state === 'unpaid'): ?>
  <div class="panel"><h1 style="font-size:2rem">Payment not completed</h1>
    <p>The checkout was not completed, so your card was not charged.</p><p><a class="btn" href="/tiny-house-plans/">Back to the plans</a></p></div>
<?php else: ?>
  <div class="panel"><h1 style="font-size:2rem">We could not find that order</h1>
    <p>If you just paid, your download link is on its way to your email. You can also get it at <a href="/order/lookup/">Find my plan download</a>, or call <a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a>.</p></div>
<?php endif; ?>
</div></section>
<?php page_end(); ?>
