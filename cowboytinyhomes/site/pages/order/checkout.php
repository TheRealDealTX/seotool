<?php
// POST /order/checkout/ - start a Stripe Checkout Session for one plan and redirect to it.
// Until Stripe and the plan's files are set up, the buyer goes to the contact form instead.
require_once __DIR__ . '/../../inc/store.php';
global $PLANS;
$slug = (string)($_POST['plan'] ?? '');
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST' || !isset($PLANS[$slug])) redirect('/home-designs/', 303);
$p = $PLANS[$slug];
if (!store_ready($slug)) {
    redirect('/contact-us/?' . http_build_query(['project' => 'Plan purchase: ' . $p['name'], 'ptype' => 'Design / plans only',
        'note' => 'I would like to buy ' . $p['ref'] . ' plan set.']) . '#form', 303);
}
if (rate_limited('checkout', 20, 600)) {
    $error = 'Too many checkout attempts from your connection. Please wait a few minutes and try again.';
} else {
    try {
        header('Location: ' . create_checkout($slug, $p, (string)($_POST['email'] ?? '')), true, 303);
        exit;
    } catch (Throwable $e) {
        error_log('checkout: ' . $e->getMessage());
        $error = 'We could not start the secure checkout just now.';
    }
}
$GLOBALS['status'] = 503;
?>
<section class="section"><div class="wrap wrap--narrow"><div class="card order-card">
  <h1>Checkout is unavailable</h1>
  <p><?= e($error) ?> Your card has not been charged.</p>
  <p>You can try again, or order <?= e($p['name']) ?> by phone at <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a> and we will send a secure payment link.</p>
  <p><a class="btn btn--gold" href="<?= e($p['url']) ?>#order">Back to <?= e($p['name']) ?></a></p>
</div></div></section>
