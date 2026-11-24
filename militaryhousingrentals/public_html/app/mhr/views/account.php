<?php
// Owner accounts: passwordless sign-in by one-time email link, a dashboard of the
// owner's listings, and a listing editor.
$owner = mhr_current_owner();
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($sub === '/verify/') {
    $tok = mhr_token_consume((string)($_GET['t'] ?? ''));
    $o = $tok ? mhr_owner($tok['owner_id']) : null;
    if (!$o || $o['status'] !== 'active') {
        mhr_flash('That sign-in link is invalid or has expired. Enter your email to get a new one.', 'err');
        mhr_redirect('/account/');
    }
    if (!$o['email_verified_at']) mhr_q('UPDATE mhr_owners SET email_verified_at = ? WHERE id = ?', [mhr_now(), $o['id']]);
    mhr_owner_login($o['id']);
    mhr_flash($tok['purpose'] === 'verify' ? 'Thanks! Your email is confirmed and you are signed in.' : 'You are signed in.');
    mhr_redirect('/account/');
}

if ($sub === '/logout/') {
    if ($method === 'POST' && !mhr_guard_check(false)) {
        unset($_SESSION['mhr_owner']);
        session_regenerate_id(true);
    }
    mhr_redirect('/account/');
}

if ($sub === '/' && !$owner) {
    $sent = false; $errors = [];
    if ($method === 'POST') {
        $g = mhr_guard_check();
        $email = mb_strtolower(mhr_line('email', 190));
        if ($g && $g !== 'honeypot') $errors[] = $g;
        elseif (!$g) {
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
            else {
                $ip = mhr_client_ip();
                $recent = (int)mhr_row("SELECT COUNT(*) c FROM mhr_login_attempts WHERE scope = 'magic' AND (ip = ? OR ident = ?) AND created_at > ?",
                    [$ip, $email, gmdate('Y-m-d H:i:s', time() - 3600)])['c'];
                mhr_q("INSERT INTO mhr_login_attempts (scope, ip, ident, success, created_at) VALUES ('magic', ?, ?, 1, ?)", [$ip, $email, mhr_now()]);
                if ($recent < 8 && ($o = mhr_owner_by_email($email)) && $o['status'] === 'active') mhr_send_login_link($o, 'login');
                $sent = true;
            }
        } else $sent = true;
    }
    mhr_page_start('Owner sign in', '/account/');
    ?>
<section class="section">
  <div class="wrap mhr-narrow">
    <div class="card form-card">
      <h1>Owner sign in</h1>
      <?= mhr_flash() ?>
      <?php if ($sent): ?>
        <div class="notice notice-ok" role="status"><?= icon('mail') ?> If an owner account exists for that address, we've emailed a sign-in link. It expires in 30 minutes.</div>
        <p class="fineprint">No email? Check your spam folder, or <a href="/account/">try again</a>.</p>
      <?php else: ?>
        <p>Enter the email you used to claim or list your property. We'll send you a one-time sign-in link. There's no password to remember.</p>
        <?= mhr_errors_html($errors) ?>
        <form method="post" action="/account/" class="form" data-form novalidate>
          <?= mhr_guard_fields() ?>
          <label class="field" for="a-email"><span>Email</span><input id="a-email" type="email" name="email" required autocomplete="email" maxlength="190"></label>
          <button class="btn btn-primary btn-lg btn-block" type="submit"><?= icon('mail') ?> Email me a sign-in link</button>
        </form>
        <p class="fineprint">Don't have an account yet? <a href="/submit-property/">List your property</a> or use <strong>Claim this listing</strong> on your property's page.</p>
      <?php endif; ?>
    </div>
  </div>
</section>
<?php
    layout_end();
    return;
}

if (!$owner) mhr_redirect('/account/');

if (preg_match('#^/listing/([a-z0-9-]+)/$#', $sub, $m)) {
    $slug = $m[1];
    [$l, $row] = mhr_listing_full($slug);
    if (!$l || !$row || (int)$row['owner_id'] !== (int)$owner['id'] || $row['status'] === 'deleted') not_found();
    $errors = [];
    if ($method === 'POST') {
        $g = mhr_guard_check(false);
        if ($g) $errors[] = $g === 'honeypot' ? 'Please try again.' : $g;
        else {
            $errors = mhr_editor_save($slug, $l, false);
            if (!$errors || str_starts_with($errors[0], 'Your changes were saved')) {
                foreach ($errors as $i => $x) if ($i) mhr_flash($x, 'err');
                mhr_flash('Your listing was updated.');
                mhr_redirect('/account/listing/' . $slug . '/');
            }
        }
        [$l] = mhr_listing_full($slug);
    }
    mhr_page_start('Edit ' . $l['title'], '/account/listing/' . $slug . '/');
    ?>
<section class="section section-tight">
  <div class="wrap mhr-wide">
    <p><a class="link-arrow" href="/account/">&larr; Back to your dashboard</a></p>
    <div class="card form-card">
      <div class="mhr-head-row">
        <h1>Edit <?= e($l['title']) ?></h1>
        <?php if ($row['status'] === 'published'): ?><a class="btn btn-light btn-sm" href="/properties/<?= e($slug) ?>/" target="_blank" rel="noopener">View listing</a><?php endif; ?>
      </div>
      <?= mhr_flash() ?><?= mhr_errors_html($errors) ?>
      <?= mhr_editor_form($l, '/account/listing/' . $slug . '/', false) ?>
    </div>
  </div>
</section>
<?php
    layout_end();
    return;
}

if ($sub !== '/') not_found();

$mine = mhr_all('SELECT * FROM mhr_listings WHERE owner_id = ? AND status <> ? ORDER BY updated_at DESC', [$owner['id'], 'deleted']);
$submitted = mhr_all("SELECT * FROM mhr_listings WHERE submitter_email = ? AND (owner_id IS NULL OR owner_id <> ?) AND status IN ('pending','published') ORDER BY created_at DESC", [$owner['email'], $owner['id']]);
$payments = mhr_all("SELECT * FROM mhr_payments WHERE owner_id = ? AND status = 'fulfilled' ORDER BY id DESC LIMIT 20", [$owner['id']]);
$status_label = ['published' => 'Live', 'pending' => 'Pending review', 'unpublished' => 'Unpublished', 'rejected' => 'Not approved'];
mhr_page_start('Owner dashboard', '/account/');
?>
<section class="section section-tight">
  <div class="wrap mhr-wide">
    <div class="mhr-head-row">
      <div><p class="eyebrow">Owner dashboard</p><h1>Hi <?= e($owner['name'] ?: $owner['email']) ?></h1></div>
      <form method="post" action="/account/logout/"><?= mhr_guard_fields(false) ?><button class="btn btn-light btn-sm" type="submit">Sign out</button></form>
    </div>
    <?= mhr_flash() ?>
    <?php if (!$owner['email_verified_at']): ?><div class="notice notice-err" role="alert">Please confirm your email using the link we sent you.</div><?php endif; ?>
    <div class="card form-card">
      <h2>Your listings</h2>
      <?php if (!$mine): ?>
        <p>You don't have any verified listings yet. Find your property and choose <strong>Claim this listing</strong>, or <a href="/submit-property/">list a new property</a>.</p>
      <?php else: ?>
        <ul class="mhr-list">
          <?php foreach ($mine as $r): [$l] = mhr_listing_full($r['slug'], $r); if (!$l) continue; $img = listing_image($l); ?>
          <li>
            <img src="<?= e($img['src']) ?>" alt="" width="96" height="64" loading="lazy">
            <div><strong><?= e($l['title']) ?></strong><br><small class="muted"><?= e($l['address']) ?></small><br>
              <span class="chip"><?= e($status_label[$r['status']] ?? $r['status']) ?></span>
              <?php if ($r['verified']): ?><span class="mhr-badge"><?= icon('check') ?> Verified owner</span><?php endif; ?></div>
            <div class="btn-row">
              <a class="btn btn-primary btn-sm" href="/account/listing/<?= e($r['slug']) ?>/">Edit details &amp; photos</a>
              <?php if ($r['status'] === 'published'): ?><a class="btn btn-light btn-sm" href="/properties/<?= e($r['slug']) ?>/">View</a><?php endif; ?>
            </div>
          </li>
          <?php endforeach; ?>
        </ul>
      <?php endif; ?>
    </div>
    <?php if ($submitted): ?>
    <div class="card form-card">
      <h2>Your free submissions</h2>
      <ul class="mhr-list">
        <?php foreach ($submitted as $r): [$l] = mhr_listing_full($r['slug'], $r); if (!$l) continue; ?>
        <li><div><strong><?= e($l['title']) ?></strong><br><span class="chip"><?= e($status_label[$r['status']] ?? $r['status']) ?></span>
          <?php if ($r['status'] === 'published'): ?><small class="muted">Contact details hidden</small><?php endif; ?></div>
          <div class="btn-row"><?php if ($r['status'] === 'published' && !$r['owner_id']): ?><a class="btn btn-accent btn-sm" href="/claim/<?= e($r['slug']) ?>/">Verify for <?= e(mhr_price_label()) ?></a><?php endif; ?></div></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <?php endif; ?>
    <?php if ($payments): ?>
    <div class="card form-card">
      <h2>Receipts</h2>
      <table class="mhr-table"><thead><tr><th>Date</th><th>Listing</th><th>Amount</th><th>Ref</th></tr></thead><tbody>
      <?php foreach ($payments as $p): ?><tr><td><?= e(substr($p['fulfilled_at'], 0, 10)) ?></td><td><?= e($p['listing_slug']) ?></td><td>$<?= e(number_format(($p['amount_total'] ?? 0) / 100, 2)) ?></td><td>MHR-<?= (int)$p['id'] ?></td></tr><?php endforeach; ?>
      </tbody></table>
    </div>
    <?php endif; ?>
  </div>
</section>
<?php layout_end();
