<?php
// POST /order/checkout/ - start a Stripe Checkout Session for one plan and redirect to it.
require_once __DIR__ . '/../../inc/store.php';
$slug = (string)($_POST['plan'] ?? '');
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !isset($PLANS[$slug])) redirect('/tiny-house-plans/', 303);
$p = $PLANS[$slug];
if (!store_ready($slug)) redirect('/contact/?plan=' . urlencode($p['name']) . '#form', 303);
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
http_response_code(503);
page_start(['robots' => 'noindex,nofollow', 'title' => 'Checkout | ' . SITE_NAME]);
?>
<section class="section"><div class="narrow panel">
  <h1 style="font-size:2rem">Checkout is unavailable</h1>
  <p><?= e($error) ?> Your card has not been charged.</p>
  <p>You can try again, or order <?= e($p['name']) ?> by phone at <a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a> and we will send a secure payment link.</p>
  <p><a class="btn" href="/plans/<?= e($slug) ?>/#order">Back to <?= e($p['name']) ?></a></p>
</div></section>
<?php page_end(); ?>
