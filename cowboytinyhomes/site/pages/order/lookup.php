<?php
// /order/lookup/ - re-send download links for every order placed with an email address.
require_once __DIR__ . '/../../inc/store.php';
if (session_status() !== PHP_SESSION_ACTIVE) session_start();
if (empty($_SESSION['cth_csrf'])) $_SESSION['cth_csrf'] = bin2hex(random_bytes(16));
$done = false;
$error = '';
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    $email = trim((string)($_POST['email'] ?? ''));
    if (!hash_equals($_SESSION['cth_csrf'], (string)($_POST['csrf'] ?? '')) || !empty($_POST['website'])) {
        $error = 'Please reload the page and try again.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = 'Please enter the email address you used at checkout.';
    } elseif (rate_limited('lookup', 5, 3600)) {
        $error = 'Too many requests. Please try again in an hour, or contact us.';
    } else {
        $orders = orders_for_email($email);
        if ($orders) {
            $body = "Here are the download links for the plans bought with this email address:\n\n";
            foreach ($orders as $o) {
                if (time() > $o['expires'] || $o['downloads'] >= DOWNLOAD_MAX) {
                    // Refresh old links: a new token, expiry and download allowance.
                    $o['token'] = bin2hex(random_bytes(20));
                    $o['expires'] = time() + DOWNLOAD_DAYS * 86400;
                    $o['downloads'] = 0;
                    save_order($o);
                }
                $body .= "{$o['plan_name']} (order {$o['id']}, " . date('M j, Y', $o['created']) . ")\n" . download_url($o) . "\n\n";
            }
            $body .= "Questions? Reply to this email or call " . PHONE . ".\n\n" . SITE_NAME . "\n";
            send_mail($email, 'Your ' . SITE_NAME . ' download links', $body, EMAIL, SITE_NAME);
        }
        $done = true;   // same answer either way, so the form does not reveal who has bought
    }
}
?>
<section class="section"><div class="wrap wrap--narrow"><div class="card order-card">
  <h1>Find my plan download</h1>
  <?php if ($done): ?>
    <div class="alert alert--ok" role="status">If we have an order for that address, the download links are on their way. Check your inbox (and spam folder) in a few minutes.</div>
  <?php else: ?>
    <p>Lost your download email? Enter the address you used at checkout and we will send fresh links for every plan you bought.</p>
    <?php if ($error): ?><div class="alert alert--err" role="alert"><?= e($error) ?></div><?php endif; ?>
    <form class="form form--single" method="post" action="/order/lookup/">
      <input type="hidden" name="csrf" value="<?= e($_SESSION['cth_csrf']) ?>">
      <div class="hp" aria-hidden="true"><label for="f-website">Website</label><input type="text" id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="full"><label for="f-email">Email address</label><input type="email" id="f-email" name="email" required autocomplete="email"></div>
      <div class="full"><button class="btn btn--gold" type="submit">Email my download links</button></div>
    </form>
  <?php endif; ?>
  <p class="form-note">Still stuck? Email <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a> or call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a>.</p>
</div></div></section>
