<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
if (!$l || !is_directory($l)) not_found('That listing can’t be claimed.');
$err = []; $done = null;
$d = ['role' => 'owner', 'choice' => stripe_ready() ? 'paid' : 'free'];
$host = $l['website'] ? strtolower(preg_replace('#^www\.#', '', (string)parse_url($l['website'], PHP_URL_HOST))) : '';

if (!is_unclaimed($l)) {
    $done = 'claimed';
} elseif (is_post()) {
    $d = array_merge($d, $_POST);
    if ($g = form_guard()) $err['form'] = $g;
    elseif (!rate_limit('claim', 5, 3600)) $err['form'] = 'Too many attempts. Please try again later.';
    else {
        $name = mb_substr(post('name'), 0, 120);
        $email = strtolower(mb_substr(post('email'), 0, 190));
        $phone = preg_replace('/[^0-9+()\-. ]/', '', mb_substr(post('phone'), 0, 40));
        $role = in_array(post('role'), ['owner', 'manager', 'leasing', 'corporate', 'other'], true) ? post('role') : 'other';
        $msg = mb_substr(post('message'), 0, 2000);
        $choice = post('choice') === 'paid' && stripe_ready() ? 'paid' : 'free';
        if (mb_strlen($name) < 2) $err['name'] = 'Enter your name.';
        if (!valid_email($email)) $err['email'] = 'Enter a valid email address.';
        if (empty($_POST['authorized'])) $err['authorized'] = 'Please confirm you’re authorized to manage this property’s listing.';
        if ($choice === 'free' && mb_strlen($msg) < 10 && !$host) $err['message'] = 'Tell us briefly how you’re connected to the property.';
        if (!$err) {
            $edomain = substr(strrchr($email, '@'), 1);
            $match = $host && ($edomain === $host || str_ends_with($host, '.' . $edomain) || str_ends_with($edomain, '.' . $host)) ? 1 : 0;
            $cid = insert('claims', ['listing_id' => (int)$l['id'], 'name' => $name, 'email' => $email, 'phone' => $phone, 'role' => $role,
                'message' => $msg, 'domain_match' => $match, 'status' => $choice === 'paid' ? 'pending_payment' : 'pending', 'ip' => client_ip(), 'created_at' => now()]);
            if ($choice === 'paid') {
                try {
                    redirect(stripe_checkout($l, 'claim', $email, $name, ['claim_id' => (string)$cid]), 303);
                } catch (Throwable $e) {
                    error_log('[stripe claim] ' . $e->getMessage());
                    update('claims', ['status' => 'pending'], 'id = ?', [$cid]);
                }
            }
            notify_admin('Claim request for #' . $l['id'] . ($match ? ' (email domain matches website)' : ''),
                '<p><strong>' . e($l['title']) . '</strong> — ' . e($l['city'] . ', ' . $l['state']) . '</p><p>' . e($name) . ' &lt;' . e($email) . '&gt; ' . e($phone) . ' · ' . e($role) . '</p><p>' . nl2br(e($msg)) . '</p><p><a href="' . e(base_url('/admin/claims/')) . '">Review claims</a></p>');
            send_mail($email, 'We received your claim for ' . $l['title'], '<p>Hi ' . e($name) . ',</p><p>Thanks for claiming <strong>' . e($l['title']) . '</strong> on The Sublet. Our team verifies every claim — usually within one to two business days — and we’ll email you a sign-in link once it’s approved.</p><p>Want it done instantly? You can verify with a one-time ' . e(price_label()) . ' payment from the claim page.</p>');
            $done = 'pending';
        }
    }
}

$crumbs = [['The Sublet', '/'], ['Sublets', '/sublets/'], [$l['city'], city_url($l['state'], $l['city_slug'])], [$l['title'], listing_url($l)], ['Claim', '/claim/' . $l['id'] . '/']];
$v = fn($k) => e($d[$k] ?? '');
ob_start(); ?>
<div class="wrap narrow-lg section">
  <?= breadcrumbs_html($crumbs) ?>
  <?php if ($done === 'claimed'): ?>
    <h1>This listing has already been claimed</h1>
    <p>If you believe that’s a mistake, <a href="/contact/">contact us</a> with the listing link and proof of your connection to the property.</p>
  <?php elseif ($done === 'pending'): ?>
    <div class="claim-done reveal">
      <div class="big-check">✓</div>
      <h1>Claim received</h1>
      <p>We’ll verify your connection to <strong><?= e($l['title']) ?></strong> and email you a sign-in link — usually within one to two business days.</p>
      <p><a class="btn" href="<?= e(listing_url($l)) ?>">Back to the listing</a></p>
    </div>
  <?php else: ?>
    <header class="page-head">
      <p class="eyebrow">For property owners &amp; managers</p>
      <h1>Claim <?= e($l['title']) ?></h1>
      <p class="lead">Take control of your free listing on The Sublet: add photos, monthly rates, availability and house rules, and reach renters looking for furnished stays of one to twelve months.</p>
    </header>
    <?php if (isset($err['form'])): ?><div class="flash flash-err"><?= e($err['form']) ?></div><?php unset($err['form']); endif; ?>
    <?= form_errors($err) ?>
    <form method="post" class="listing-form claim-form">
      <?= csrf_field() ?><?= honeypot_field() ?>
      <fieldset class="tier-pick"><legend>How would you like to verify?</legend>
        <div class="tiers tiers-pick">
          <?php if (stripe_ready()): ?>
          <label class="tier tier-hi"><input type="radio" name="choice" value="paid"<?= ($d['choice'] ?? '') === 'paid' ? ' checked' : '' ?>><span class="tier-body"><strong>Instant verification — <?= e(price_label()) ?> one-time</strong><span>Card payment verifies you right away. You get the dashboard immediately, a “Verified host” badge, top placement and your contact details shown.</span></span></label>
          <?php endif; ?>
          <label class="tier"><input type="radio" name="choice" value="free"<?= ($d['choice'] ?? '') === 'free' ? ' checked' : '' ?>><span class="tier-body"><strong>Free claim — reviewed by our team</strong><span>We check your connection to the property (an email at <?= $host ? e($host) : 'the property’s domain' ?> speeds this up). Renters contact you through our private relay.</span></span></label>
        </div>
      </fieldset>
      <fieldset><legend>Your details</legend>
        <div class="row3">
          <label>Your name<input name="name" value="<?= $v('name') ?>" required maxlength="120" autocomplete="name"></label>
          <label>Work email<input type="email" name="email" value="<?= $v('email') ?>" required maxlength="190" autocomplete="email"></label>
          <label>Phone <small>(optional)</small><input type="tel" name="phone" value="<?= $v('phone') ?>" maxlength="40" autocomplete="tel"></label>
        </div>
        <label>Your role
          <select name="role"><?php foreach (['owner' => 'Owner', 'manager' => 'Property manager', 'leasing' => 'Leasing / front office', 'corporate' => 'Corporate housing operator', 'other' => 'Other'] as $k => $t): ?><option value="<?= $k ?>"<?= ($d['role'] ?? '') === $k ? ' selected' : '' ?>><?= e($t) ?></option><?php endforeach; ?></select></label>
        <label>How are you connected to the property? <small>(helps us verify free claims faster)</small><textarea name="message" rows="3" maxlength="2000"><?= $v('message') ?></textarea></label>
        <label class="chk agree"><input type="checkbox" name="authorized" value="1"<?= !empty($d['authorized']) ? ' checked' : '' ?>> I’m authorized to manage this property’s listing, and I agree to the <a href="/terms/" target="_blank">terms</a> and fair housing rules.</label>
      </fieldset>
      <div class="form-actions"><button class="btn btn-lg btn-glow" type="submit">Claim this listing</button></div>
    </form>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Claim ' . $l['title'] . ' | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
