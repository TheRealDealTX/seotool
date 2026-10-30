<?php
// GET /order/complete/?session_id=cs_... - Stripe sends the buyer here after paying.
require_once __DIR__ . '/../../inc/store.php';
global $PLANS;
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
$fmtBytes = fn($b) => $b > 1e6 ? number_format($b / 1e6, 1) . ' MB' : number_format(max(1, $b / 1e3)) . ' KB';
?>
<section class="section"><div class="wrap wrap--narrow"><div class="card order-card">
<?php if ($state === 'paid'): ?>
  <p class="eyebrow">Order <?= e($order['id']) ?></p>
  <h1>Thank you! Your plan set is ready.</h1>
  <p class="lead"><?= e($order['plan_name']) ?></p>
  <p><a class="btn btn--gold" href="<?= e(download_url($order)) ?>">Download the complete plan set<?= $set ? ' (' . $fmtBytes($set['zip_bytes']) . ' zip)' : '' ?></a></p>
  <p class="form-note">We also emailed this link to <strong><?= e($order['email']) ?></strong>. It works for <?= DOWNLOAD_DAYS ?> days and up to <?= DOWNLOAD_MAX ?> downloads; get a new one any time at <a href="/order/lookup/">Find my plan download</a>.</p>
  <?php if ($set): ?>
  <h2>What is in the zip</h2>
  <ul class="file-list">
    <?php foreach ($set['files'] as [$name, $bytes]): ?><li><span><?= e($name) ?></span><span class="muted"><?= $fmtBytes($bytes) ?></span></li><?php endforeach; ?>
  </ul>
  <?php endif; ?>
  <h2>Next steps</h2>
  <ol>
    <li>Open the drawing set PDF and read sheet A0.0: the Texas code, wind, soils and climate notes.</li>
    <li>Get a geotechnical report for your lot and ask your city (or county) what it needs for a permit. Many require a Texas-licensed engineer's or architect's seal.</li>
    <li>Take the materials list and cost estimate to suppliers and builders for quotes.</li>
    <li>Want us to build it? <?= e(PLAN_CREDIT) ?> <a href="/contact-us/?<?= e(http_build_query(['project' => 'Build ' . $p['ref'], 'note' => 'I bought the plan (order ' . $order['id'] . ') and would like a build quote.'])) ?>#form">Ask for a build quote</a>.</li>
  </ol>
<?php elseif ($state === 'processing'): ?>
  <h1>Payment processing</h1>
  <p>Your payment is still being confirmed by the bank. As soon as it clears we will email your download link. This page will also show it if you <a href="">refresh</a> in a minute.</p>
<?php elseif ($state === 'unpaid'): ?>
  <h1>Payment not completed</h1>
  <p>The checkout was not completed, so your card was not charged.</p>
  <p><a class="btn btn--gold" href="/home-designs/">Back to the plans</a></p>
<?php else: ?>
  <h1>We could not find that order</h1>
  <p>If you just paid, your download link is on its way to your email. You can also get it at <a href="/order/lookup/">Find my plan download</a>, or call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a>.</p>
<?php endif; ?>
</div></div></section>
