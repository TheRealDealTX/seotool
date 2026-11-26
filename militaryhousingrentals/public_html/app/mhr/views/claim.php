<?php
// /claim/{slug}/: the owner verifies a listing by paying the claim fee.
if (!preg_match('#^/([a-z0-9-]+)/$#', $sub, $m)) not_found();
$slug = $m[1];
$l = listing($slug) ?? not_found();
$row = mhr_row_for($slug);
$claimed = $row && $row['owner_id'];
$errors = [];
$v = ['name' => '', 'email' => ''];
if (($o = mhr_current_owner())) $v = ['name' => $o['name'], 'email' => $o['email']];

if (!$claimed && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $g = mhr_guard_check();
    if ($g === 'honeypot') mhr_redirect('/properties/' . $slug . '/');
    if ($g) $errors[] = $g;
    $v = ['name' => mhr_line('name', 120), 'email' => mb_strtolower(mhr_line('email', 190))];
    if ($v['name'] === '') $errors[] = 'Your name is required.';
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
    if (empty($_POST['authorized'])) $errors[] = 'Please confirm you are the owner, manager or an authorized representative.';
    if (!$errors && !mhr_stripe_configured()) $errors[] = 'Online payments are not available right now. Please contact us and we will verify your listing manually.';
    if (!$errors) {
        $owner = mhr_owner_find_or_create($v['name'], $v['email']);
        if ($owner['status'] !== 'active') $errors[] = 'This account is disabled. Please contact us.';
        else {
            $url = mhr_checkout_start('claim', $slug, $l['title'], $owner, $err);
            if ($url) mhr_redirect($url);
            $errors[] = 'We could not start the secure checkout. Please try again in a minute.';
        }
    }
}

mhr_page_start('Claim ' . $l['title'], '/claim/' . $slug . '/', ['nav' => '/properties/']);
[$crumbs] = breadcrumbs([['Home', '/'], [$l['title'], '/properties/' . $slug . '/'], ['Claim this listing', null]]);
?>
<section class="page-hero page-hero-sm">
  <div class="wrap"><?= $crumbs ?><p class="eyebrow">For owners &amp; managers</p><h1>Claim <?= e($l['title']) ?></h1>
  <p class="lead">Verify that you own or manage this property to feature it, show your phone, email and website, and get a Verified owner badge.</p></div>
</section>
<section class="section section-tight">
  <div class="wrap contact-layout">
    <div class="card form-card">
      <?php if ($claimed): ?>
        <div class="notice notice-ok" role="status"><?= icon('check') ?> This listing has already been claimed by a verified owner.</div>
        <p>If you manage this property and believe this is a mistake, please <a href="/contact-us/">contact us</a>. Owners can sign in at <a href="/account/">your owner account</a>.</p>
      <?php else: ?>
        <?= mhr_errors_html($errors) ?>
        <form method="post" action="/claim/<?= e($slug) ?>/" class="form" data-form novalidate>
          <?= mhr_guard_fields() ?>
          <div class="form-grid">
            <label class="field" for="c-name"><span>Your name <span class="req" aria-hidden="true">*</span></span><input id="c-name" name="name" value="<?= e($v['name']) ?>" required autocomplete="name" maxlength="120"></label>
            <label class="field" for="c-email"><span>Your email <span class="req" aria-hidden="true">*</span></span><input id="c-email" type="email" name="email" value="<?= e($v['email']) ?>" required autocomplete="email" maxlength="190"></label>
          </div>
          <label class="mhr-check"><input type="checkbox" name="authorized" value="1" required> <span>I'm the owner, property manager or an authorized representative of <strong><?= e($l['title']) ?></strong>.</span></label>
          <div class="mhr-price-row">
            <div><strong class="mhr-price"><?= e(mhr_price_label()) ?></strong> <span class="muted">one-time</span></div>
            <button class="btn btn-accent btn-lg" type="submit"><?= icon('shield') ?> Continue to secure payment</button>
          </div>
          <p class="fineprint">You'll pay on Stripe's secure checkout page. Have a promo code? Enter it there. After payment we email you a link to confirm your address and manage the listing. No password needed.</p>
        </form>
      <?php endif; ?>
    </div>
    <aside class="contact-aside">
      <div class="card">
        <h3>What you get</h3>
        <ul class="checks">
          <li><?= icon('check') ?> <strong>Featured</strong>: shown first in search results and in the Featured section</li>
          <li><?= icon('check') ?> Your phone, email and website shown on the listing</li>
          <li><?= icon('check') ?> A <span class="mhr-badge"><?= icon('check') ?> Verified owner</span> badge</li>
          <li><?= icon('check') ?> An owner dashboard to update details and photos</li>
        </ul>
        <p class="fineprint">Your details are used to verify and manage the listing, never sold or shared.</p>
        <p><a class="link-arrow" href="/properties/<?= e($slug) ?>/">Back to the listing <?= icon('arrow') ?></a></p>
      </div>
    </aside>
  </div>
</section>
<?php layout_end();
