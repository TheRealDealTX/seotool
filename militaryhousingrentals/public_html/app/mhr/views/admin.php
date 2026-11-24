<?php
// Admin panel. Own minimal layout (no ads/analytics), noindex, no-store.
mhr_private_headers();
header("Content-Security-Policy: frame-ancestors 'none'");
$A = mhr_admin_path();
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
mhr_session_start();

function adm_current() {
    $id = $_SESSION['mhr_admin'] ?? 0;
    if (!$id) return null;
    if (time() - ($_SESSION['mhr_admin_at'] ?? 0) > 7200) { unset($_SESSION['mhr_admin']); return null; }
    $_SESSION['mhr_admin_at'] = time();
    return mhr_row('SELECT id, username FROM mhr_admins WHERE id = ?', [$id]);
}

function adm_start($title, $active = '') {
    $A = mhr_admin_path();
    $nav = ['' => 'Dashboard', 'submissions/' => 'Submissions', 'listings/' => 'Listings', 'owners/' => 'Owners', 'payments/' => 'Payments', 'messages/' => 'Messages', 'settings/' => 'Settings'];
    $pending = 0;
    try { $pending = (int)mhr_row("SELECT COUNT(*) c FROM mhr_listings WHERE status = 'pending'")['c']; } catch (Throwable $e) {}
    ?><!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title><?= e($title) ?> · Admin · <?= e(cfg('name')) ?></title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= asset_ver('css/site.css') ?>"><?= mhr_css_link() ?>
<script>try{var t=localStorage.getItem('mhr-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
</head><body class="mhr-admin">
<header class="mhr-admin-bar"><div class="wrap mhr-admin-bar-in">
  <a class="mhr-admin-brand" href="<?= e($A) ?>"><?= e(cfg('name')) ?> <span>Admin</span></a>
  <?php if (!empty($_SESSION['mhr_admin'])): ?>
  <nav aria-label="Admin"><?php foreach ($nav as $href => $label): ?><a href="<?= e($A . $href) ?>"<?= $active === $href ? ' aria-current="page"' : '' ?>><?= e($label) ?><?php if ($href === 'submissions/' && $pending): ?> <span class="mhr-count"><?= $pending ?></span><?php endif; ?></a><?php endforeach; ?>
    <a href="/" target="_blank" rel="noopener">View site ↗</a>
    <form method="post" action="<?= e($A) ?>logout/" class="mhr-inline"><?= mhr_guard_fields(false) ?><button type="submit" class="mhr-linkbtn">Sign out</button></form></nav>
  <?php endif; ?>
</div></header>
<main class="wrap mhr-admin-main">
<?php
}
function adm_end() { echo "</main></body></html>"; }
function adm_post_ok() {
    $g = mhr_guard_check(false);
    if ($g) { mhr_flash($g === 'honeypot' ? 'Request blocked.' : $g, 'err'); return false; }
    return true;
}
function adm_money($cents, $cur = 'usd') { return $cents === null ? '—' : '$' . number_format($cents / 100, 2) . ($cur && $cur !== 'usd' ? ' ' . strtoupper($cur) : ''); }
function adm_status_chip($s) {
    $c = ['published' => 'ok', 'pending' => 'warn', 'rejected' => 'bad', 'unpublished' => 'muted', 'deleted' => 'bad', 'fulfilled' => 'ok', 'cancelled' => 'muted', 'failed' => 'bad'][$s] ?? 'muted';
    return '<span class="mhr-st mhr-st-' . $c . '">' . e($s) . '</span>';
}

// ---------------------------------------------------------------- login / logout

if ($sub === '/logout/') {
    if ($method === 'POST' && adm_post_ok()) { unset($_SESSION['mhr_admin'], $_SESSION['mhr_admin_at']); session_regenerate_id(true); }
    mhr_redirect($A . 'login/');
}

$admin = adm_current();
if (!$admin) {
    if ($sub !== '/login/') mhr_redirect($A . 'login/');
    $error = '';
    if ($method === 'POST') {
        $ip = mhr_client_ip();
        $user = mb_substr(trim((string)($_POST['username'] ?? '')), 0, 64);
        $since = gmdate('Y-m-d H:i:s', time() - 900);
        $fails_ip = (int)mhr_row("SELECT COUNT(*) c FROM mhr_login_attempts WHERE scope = 'admin' AND success = 0 AND ip = ? AND created_at > ?", [$ip, $since])['c'];
        $fails_user = (int)mhr_row("SELECT COUNT(*) c FROM mhr_login_attempts WHERE scope = 'admin' AND success = 0 AND ident = ? AND created_at > ?", [$user, $since])['c'];
        $g = mhr_guard_check(false);
        if ($g) $error = $g === 'honeypot' ? 'Sign-in failed.' : $g;
        elseif ($fails_ip >= 5 || $fails_user >= 10) $error = 'Too many failed attempts. Please wait 15 minutes and try again.';
        else {
            $row = mhr_row('SELECT * FROM mhr_admins WHERE username = ?', [$user]);
            $ok = password_verify((string)($_POST['password'] ?? ''), $row['pass_hash'] ?? '$2y$10$1jo4KDgRQAj7WMA3uoACquqtFROl7wuS.v5/idX74abB6hEVx9mSm');
            mhr_q("INSERT INTO mhr_login_attempts (scope, ip, ident, success, created_at) VALUES ('admin', ?, ?, ?, ?)", [$ip, $user, $ok && $row ? 1 : 0, mhr_now()]);
            if ($ok && $row) {
                session_regenerate_id(true);
                $_SESSION['mhr_admin'] = (int)$row['id'];
                $_SESSION['mhr_admin_at'] = time();
                mhr_q('UPDATE mhr_admins SET last_login_at = ? WHERE id = ?', [mhr_now(), $row['id']]);
                if (password_needs_rehash($row['pass_hash'], PASSWORD_DEFAULT)) mhr_q('UPDATE mhr_admins SET pass_hash = ? WHERE id = ?', [password_hash($_POST['password'], PASSWORD_DEFAULT), $row['id']]);
                mhr_redirect($A);
            }
            usleep(400000);
            $error = 'Wrong username or password.';
        }
    }
    adm_start('Sign in'); ?>
  <div class="card form-card mhr-narrow mhr-login">
    <h1>Admin sign in</h1>
    <?php if ($error): ?><div class="notice notice-err" role="alert"><?= e($error) ?></div><?php endif; ?>
    <form method="post" action="<?= e($A) ?>login/" class="form">
      <?= mhr_guard_fields(false) ?>
      <label class="field"><span>Username</span><input name="username" required autocomplete="username" maxlength="64" autofocus></label>
      <label class="field"><span>Password</span><input type="password" name="password" required autocomplete="current-password"></label>
      <button class="btn btn-primary btn-block btn-lg" type="submit">Sign in</button>
    </form>
  </div>
<?php adm_end(); return; }

if ($sub === '/login/') mhr_redirect($A);

// ---------------------------------------------------------------- listing actions

function adm_listing_action($slug, $do) {
    $A = mhr_admin_path();
    [$l, $row, $origin] = mhr_listing_full($slug);
    if (!$l) { mhr_flash('Listing not found.', 'err'); return; }
    $title = $l['title'];
    switch ($do) {
        case 'approve':
        case 'publish':
            $was_pending = $row && $row['status'] === 'pending';
            mhr_set_cols($slug, ['status' => 'published', 'published_at' => $row['published_at'] ?? mhr_now()]);
            if ($origin === 'db' && $was_pending) mhr_save_fields($slug, ['date' => gmdate('Y-m-d')]);
            if ($was_pending && $row['submitter_email'] && !$row['owner_id']) {
                mhr_mail($row['submitter_email'], 'Your listing is live: ' . $title,
                    "Hi " . ($row['submitter_name'] ?: 'there') . ",\n\nGood news: \"$title\" is now published on " . cfg('name') . ":\n" . abs_url('/properties/' . $slug . '/') . "\n\n"
                    . "Your contact details are hidden for now. Verify the listing for " . mhr_price_label() . " to show your phone, email and website, add a Verified owner badge, and get an owner dashboard to edit details and photos:\n"
                    . abs_url('/claim/' . $slug . '/') . "\n\n— " . cfg('name'));
            }
            mhr_flash(($was_pending ? 'Approved and published: ' : 'Published: ') . $title);
            break;
        case 'reject':
            mhr_set_cols($slug, ['status' => 'rejected']);
            if (!empty($_POST['notify']) && $row && $row['submitter_email']) {
                $why = mhr_post('reason', 1000);
                mhr_mail($row['submitter_email'], 'About your listing: ' . $title, "Hi " . ($row['submitter_name'] ?: 'there') . ",\n\nThanks for submitting \"$title\". We weren't able to publish it" . ($why !== '' ? ":\n\n$why" : '.') . "\n\nReply to this email if you have questions.\n\n— " . cfg('name'));
            }
            mhr_flash('Rejected: ' . $title);
            break;
        case 'unpublish': mhr_set_cols($slug, ['status' => 'unpublished']); mhr_flash('Unpublished: ' . $title); break;
        case 'delete': mhr_set_cols($slug, ['status' => 'deleted']); mhr_flash('Deleted (hidden from the site; can be restored): ' . $title); break;
        case 'restore': mhr_set_cols($slug, ['status' => $origin === 'json' ? 'published' : 'unpublished']); mhr_flash('Restored: ' . $title); break;
        case 'purge':
            if ($origin !== 'db' || empty($_POST['confirm'])) { mhr_flash('Tick "confirm" to permanently delete a submitted listing.', 'err'); return; }
            foreach ($l['images'] as $img) mhr_delete_image($img['src']);
            mhr_q('DELETE FROM mhr_listings WHERE slug = ?', [$slug]);
            mhr_flash('Permanently deleted: ' . $title);
            mhr_redirect($A . 'listings/');
        case 'contact_on': mhr_set_cols($slug, ['contact_visible' => 1]); mhr_flash('Contact details are now shown.'); break;
        case 'contact_off': mhr_set_cols($slug, ['contact_visible' => 0]); mhr_flash('Contact details are now hidden.'); break;
        case 'verified_on': mhr_set_cols($slug, ['verified' => 1]); mhr_flash('Verified badge on.'); break;
        case 'verified_off': mhr_set_cols($slug, ['verified' => 0]); mhr_flash('Verified badge off.'); break;
        case 'assign':
            $email = mb_strtolower(mhr_line('owner_email', 190));
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { mhr_flash('Enter a valid owner email.', 'err'); return; }
            $o = mhr_owner_find_or_create(mhr_line('owner_name', 120), $email);
            $cols = ['owner_id' => $o['id']];
            if (!empty($_POST['verify'])) $cols += ['verified' => 1, 'contact_visible' => 1];
            mhr_set_cols($slug, $cols);
            if (!empty($_POST['send_link'])) mhr_send_login_link($o, $o['email_verified_at'] ? 'login' : 'verify');
            mhr_flash('Owner assigned: ' . $o['email']);
            break;
        case 'revoke': mhr_set_cols($slug, ['owner_id' => null, 'verified' => 0, 'contact_visible' => 0]); mhr_flash('Owner removed; contact details hidden.'); break;
        case 'note': mhr_set_cols($slug, ['admin_note' => mhr_post('admin_note', 2000)]); mhr_flash('Note saved.'); break;
    }
}

// ---------------------------------------------------------------- pages

$parts = array_values(array_filter(explode('/', $sub)));
$page = $parts[0] ?? '';

if ($page === '') {
    $c = fn($sql, $a = []) => (int)mhr_row($sql, $a)['c'];
    $stats = [
        'Pending submissions' => [$c("SELECT COUNT(*) c FROM mhr_listings WHERE status = 'pending'"), 'submissions/'],
        'Verified listings' => [$c('SELECT COUNT(*) c FROM mhr_listings WHERE owner_id IS NOT NULL AND status = ?', ['published']), 'listings/?f=verified'],
        'Owners' => [$c('SELECT COUNT(*) c FROM mhr_owners'), 'owners/'],
        'Payments' => [$c("SELECT COUNT(*) c FROM mhr_payments WHERE status = 'fulfilled'"), 'payments/'],
        'Messages (7 days)' => [$c('SELECT COUNT(*) c FROM mhr_messages WHERE created_at > ?', [gmdate('Y-m-d H:i:s', time() - 7 * 86400)]), 'messages/'],
    ];
    $revenue = (int)(mhr_row("SELECT COALESCE(SUM(amount_total),0) c FROM mhr_payments WHERE status = 'fulfilled'")['c']);
    adm_start('Dashboard', ''); ?>
  <h1>Dashboard</h1>
  <?= mhr_flash() ?>
  <?php if (!mhr_stripe_configured()): ?><div class="notice notice-err">Stripe isn't set up yet: claims and paid listings can't be bought. <a href="<?= e($A) ?>settings/">Add your Stripe keys</a>.</div><?php endif; ?>
  <?php if (!mhr_cfg('smtp.pass')): ?><div class="notice notice-err">The SMTP password isn't set in the private config, so emails (sign-in links, receipts) can't be sent.</div><?php endif; ?>
  <div class="mhr-stats">
    <?php foreach ($stats as $label => [$n, $href]): ?><a class="card mhr-stat" href="<?= e($A . $href) ?>"><strong><?= $n ?></strong><span><?= e($label) ?></span></a><?php endforeach; ?>
    <div class="card mhr-stat"><strong><?= e(adm_money($revenue)) ?></strong><span>Revenue</span></div>
  </div>
  <div class="card form-card"><h2>Recent payments</h2>
    <?php $rows = mhr_all('SELECT * FROM mhr_payments ORDER BY id DESC LIMIT 8'); if (!$rows): ?><p class="muted">None yet.</p><?php else: ?>
    <div class="mhr-scroll"><table class="mhr-table"><thead><tr><th>Date</th><th>Kind</th><th>Listing</th><th>Email</th><th>Amount</th><th>Status</th></tr></thead><tbody>
    <?php foreach ($rows as $p): ?><tr><td><?= e(substr($p['created_at'], 0, 16)) ?></td><td><?= e($p['kind']) ?></td><td><a href="<?= e($A . 'listings/' . $p['listing_slug'] . '/') ?>"><?= e($p['listing_slug']) ?></a></td><td><?= e($p['email']) ?></td><td><?= e(adm_money($p['amount_total'], $p['currency'])) ?></td><td><?= adm_status_chip($p['status']) ?></td></tr><?php endforeach; ?>
    </tbody></table></div><?php endif; ?>
  </div>
<?php adm_end(); return; }

if ($page === 'submissions') {
    if ($method === 'POST' && adm_post_ok()) { adm_listing_action((string)($_POST['slug'] ?? ''), (string)($_POST['do'] ?? '')); mhr_redirect($A . 'submissions/'); }
    $rows = mhr_all("SELECT * FROM mhr_listings WHERE status = 'pending' ORDER BY created_at ASC");
    adm_start('Submissions', 'submissions/'); ?>
  <h1>Pending submissions</h1>
  <?= mhr_flash() ?>
  <?php if (!$rows): ?><div class="card form-card"><p class="muted">Nothing waiting for review.</p></div><?php endif; ?>
  <?php foreach ($rows as $r): [$l] = mhr_listing_full($r['slug'], $r); if (!$l) continue; $b = base($l['base']); ?>
  <article class="card form-card mhr-sub">
    <div class="mhr-sub-head">
      <?php if ($l['images']): ?><img src="<?= e($l['images'][0]['src']) ?>" alt="" width="160" height="110"><?php endif; ?>
      <div>
        <h2><?= e($l['title']) ?></h2>
        <p class="muted"><?= e($l['address']) ?> · <?= e($b['name'] ?? $l['base']) ?> · <?= e(price_label($l)) ?> · <?= count($l['images']) ?> photo(s)</p>
        <p>Submitted <?= e(substr($r['created_at'], 0, 16)) ?> UTC by <strong><?= e($r['submitter_name']) ?></strong> &lt;<?= e($r['submitter_email']) ?>&gt; <?= e($r['submitter_phone']) ?> · plan: <strong><?= e($r['plan']) ?></strong>
        <?php if ($r['plan'] === 'paid'): ?><br><small class="muted">Paid checkout not completed yet: it publishes automatically if they pay.</small><?php endif; ?></p>
        <?php if ($r['admin_note']): ?><p class="fineprint"><?= e($r['admin_note']) ?></p><?php endif; ?>
      </div>
    </div>
    <details><summary>Description &amp; details</summary><div class="prose"><?= $l['description'] ?></div>
      <p class="fineprint">Pets: <?= e($l['pets']) ?> · Utilities: <?= e($l['utilities']) ?> · Amenities: <?= e(implode(', ', $l['amenities'])) ?> · Nearby: <?= e(implode(', ', $l['nearby'])) ?> · Public phone: <?= e($l['phone']) ?> · Website: <?= e($l['website']) ?></p></details>
    <div class="btn-row">
      <form method="post" class="mhr-inline"><?= mhr_guard_fields(false) ?><input type="hidden" name="slug" value="<?= e($r['slug']) ?>"><button class="btn btn-primary btn-sm" name="do" value="approve">Approve &amp; publish</button></form>
      <a class="btn btn-light btn-sm" href="<?= e($A . 'listings/' . $r['slug'] . '/') ?>">Edit first</a>
      <form method="post" class="mhr-inline mhr-reject"><?= mhr_guard_fields(false) ?><input type="hidden" name="slug" value="<?= e($r['slug']) ?>">
        <input name="reason" placeholder="Reason (optional, emailed)" maxlength="1000"><label class="mhr-check"><input type="checkbox" name="notify" value="1" checked> email submitter</label>
        <button class="btn btn-outline btn-sm" name="do" value="reject">Reject</button></form>
    </div>
  </article>
  <?php endforeach;
    adm_end(); return; }

if ($page === 'listings' && isset($parts[1])) {
    $slug = $parts[1];
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) not_found();
    [$l, $row, $origin] = mhr_listing_full($slug);
    if (!$l) not_found();
    $errors = [];
    if ($method === 'POST' && adm_post_ok()) {
        $do = (string)($_POST['do'] ?? '');
        if ($do === 'save') {
            $errors = mhr_editor_save($slug, $l, true);
            if (!$errors || str_starts_with($errors[0], 'Your changes were saved')) { foreach ($errors as $i => $x) if ($i) mhr_flash($x, 'err'); mhr_flash('Listing saved.'); mhr_redirect($A . 'listings/' . $slug . '/'); }
        } else { adm_listing_action($slug, $do); mhr_redirect($A . 'listings/' . $slug . '/'); }
        [$l, $row, $origin] = mhr_listing_full($slug);
    }
    $owner = $row ? mhr_owner($row['owner_id']) : null;
    $status = $row['status'] ?? 'published';
    $pays = mhr_all('SELECT * FROM mhr_payments WHERE listing_slug = ? ORDER BY id DESC', [$slug]);
    $hidden_btn = fn($do, $label, $cls = 'btn-light') => '<form method="post" class="mhr-inline">' . mhr_guard_fields(false) . '<button class="btn ' . $cls . ' btn-sm" name="do" value="' . $do . '">' . e($label) . '</button></form>';
    adm_start($l['title'], 'listings/'); ?>
  <p><a href="<?= e($A) ?>listings/">&larr; All listings</a></p>
  <div class="mhr-head-row"><h1><?= e($l['title']) ?></h1><?php if ($status === 'published'): ?><a class="btn btn-light btn-sm" href="/properties/<?= e($slug) ?>/" target="_blank" rel="noopener">View on site ↗</a><?php endif; ?></div>
  <?= mhr_flash() ?><?= mhr_errors_html($errors) ?>
  <div class="mhr-admin-grid">
    <div class="card form-card">
      <h2>Status</h2>
      <p><?= adm_status_chip($status) ?> · source: <?= $origin === 'json' ? 'original listing' : 'submitted (' . e($row['plan'] ?? '') . ')' ?>
        <?php if ($row && $row['submitter_email']): ?><br><small>Submitted by <?= e($row['submitter_name']) ?> &lt;<?= e($row['submitter_email']) ?>&gt; <?= e($row['submitter_phone']) ?></small><?php endif; ?></p>
      <div class="btn-row">
        <?php if ($status === 'pending') echo $hidden_btn('approve', 'Approve & publish', 'btn-primary') . $hidden_btn('reject', 'Reject');
        elseif (in_array($status, ['unpublished', 'rejected'], true)) echo $hidden_btn('publish', 'Publish', 'btn-primary');
        if ($status === 'published') echo $hidden_btn('unpublish', 'Unpublish');
        if ($status === 'deleted') echo $hidden_btn('restore', 'Restore', 'btn-primary'); else echo $hidden_btn('delete', 'Delete'); ?>
      </div>
      <?php if ($origin === 'db'): ?>
      <form method="post" class="mhr-inline mhr-danger"><?= mhr_guard_fields(false) ?><label class="mhr-check"><input type="checkbox" name="confirm" value="1"> confirm</label><button class="btn btn-outline btn-sm" name="do" value="purge">Delete permanently</button></form>
      <?php endif; ?>
      <h2>Contact visibility</h2>
      <p>Contact details are <strong><?= $row && $row['contact_visible'] ? 'shown' : 'hidden' ?></strong>; verified badge is <strong><?= $row && $row['verified'] ? 'on' : 'off' ?></strong>.</p>
      <div class="btn-row"><?= $row && $row['contact_visible'] ? $hidden_btn('contact_off', 'Hide contact details') : $hidden_btn('contact_on', 'Show contact details') ?>
        <?= $row && $row['verified'] ? $hidden_btn('verified_off', 'Remove verified badge') : $hidden_btn('verified_on', 'Add verified badge') ?></div>
      <h2>Owner</h2>
      <?php if ($owner): ?>
        <p><strong><?= e($owner['name']) ?></strong> &lt;<?= e($owner['email']) ?>&gt; <?= $owner['email_verified_at'] ? '· email confirmed' : '· email not confirmed' ?></p>
        <?= $hidden_btn('revoke', 'Revoke owner') ?>
      <?php else: ?><p class="muted">No owner.</p><?php endif; ?>
      <form method="post" class="form mhr-assign"><?= mhr_guard_fields(false) ?>
        <div class="form-grid"><label class="field"><span>Owner email</span><input type="email" name="owner_email" required maxlength="190"></label><label class="field"><span>Name</span><input name="owner_name" maxlength="120"></label></div>
        <label class="mhr-check"><input type="checkbox" name="verify" value="1" checked> mark verified &amp; show contact details</label>
        <label class="mhr-check"><input type="checkbox" name="send_link" value="1" checked> email them a sign-in link</label>
        <button class="btn btn-outline btn-sm" name="do" value="assign"><?= $owner ? 'Reassign owner' : 'Assign owner' ?></button></form>
      <h2>Admin note</h2>
      <form method="post" class="form"><?= mhr_guard_fields(false) ?><textarea name="admin_note" rows="3" maxlength="2000"><?= e($row['admin_note'] ?? '') ?></textarea><button class="btn btn-light btn-sm" name="do" value="note">Save note</button></form>
      <?php if ($pays): ?><h2>Payments</h2><ul class="plain small"><?php foreach ($pays as $p): ?><li><?= e(substr($p['created_at'], 0, 10)) ?> · <?= e($p['kind']) ?> · <?= e($p['email']) ?> · <?= e(adm_money($p['amount_total'], $p['currency'])) ?> · <?= adm_status_chip($p['status']) ?><?= $p['note'] ? ' · ' . e($p['note']) : '' ?></li><?php endforeach; ?></ul><?php endif; ?>
    </div>
    <div class="card form-card"><h2>Edit listing</h2><?= mhr_editor_form($l, $A . 'listings/' . $slug . '/', true) ?></div>
  </div>
<?php adm_end(); return; }

if ($page === 'listings') {
    $q = mb_strtolower(trim((string)($_GET['q'] ?? '')));
    $f = (string)($_GET['f'] ?? '');
    $rows = array_filter(mhr_admin_listing_index(), function ($x) use ($q, $f) {
        $r = $x['row'];
        if ($q !== '' && !str_contains(mb_strtolower($x['title'] . ' ' . $x['slug'] . ' ' . $x['base']), $q)) return false;
        return match ($f) {
            'verified' => $r && $r['owner_id'], 'unclaimed' => !$r || !$r['owner_id'], 'visible' => $r && $r['contact_visible'],
            'submitted' => $x['origin'] === 'db', 'pending', 'published', 'unpublished', 'rejected', 'deleted' => $x['status'] === $f,
            default => $x['status'] !== 'deleted',
        };
    });
    usort($rows, fn($a, $b) => strcmp($b['date'], $a['date']));
    adm_start('Listings', 'listings/'); ?>
  <h1>Listings <small class="muted">(<?= count($rows) ?>)</small></h1>
  <?= mhr_flash() ?>
  <form class="mhr-filter" method="get"><input type="search" name="q" value="<?= e($q) ?>" placeholder="Search title, slug or base">
    <select name="f"><?php foreach (['' => 'All (not deleted)', 'unclaimed' => 'Unclaimed', 'verified' => 'Has owner', 'visible' => 'Contact shown', 'submitted' => 'Submitted', 'pending' => 'Pending', 'published' => 'Published', 'unpublished' => 'Unpublished', 'rejected' => 'Rejected', 'deleted' => 'Deleted'] as $k => $lab): ?><option value="<?= e($k) ?>"<?= $f === $k ? ' selected' : '' ?>><?= e($lab) ?></option><?php endforeach; ?></select>
    <button class="btn btn-light btn-sm">Filter</button></form>
  <div class="card mhr-scroll"><table class="mhr-table"><thead><tr><th>Listing</th><th>Base</th><th>Status</th><th>Owner</th><th>Contact</th><th>Added</th></tr></thead><tbody>
  <?php foreach ($rows as $x): $r = $x['row']; ?>
    <tr><td><a href="<?= e($A . 'listings/' . $x['slug'] . '/') ?>"><?= e($x['title']) ?></a><?= $x['origin'] === 'db' ? ' <small class="muted">submitted</small>' : '' ?></td>
      <td><?= e(base($x['base'])['short'] ?? $x['base']) ?></td><td><?= adm_status_chip($x['status']) ?></td>
      <td><?= $r && $r['owner_id'] ? '<span class="mhr-badge">' . icon('check') . ' owner</span>' : '<span class="muted">—</span>' ?></td>
      <td><?= $r && $r['contact_visible'] ? 'shown' : '<span class="muted">hidden</span>' ?></td><td><?= e($x['date']) ?></td></tr>
  <?php endforeach; ?>
  </tbody></table></div>
<?php adm_end(); return; }

if ($page === 'owners') {
    if ($method === 'POST' && adm_post_ok()) {
        $o = mhr_owner((int)($_POST['id'] ?? 0));
        $do = (string)($_POST['do'] ?? '');
        if ($o && $do === 'disable') { mhr_q("UPDATE mhr_owners SET status = 'disabled' WHERE id = ?", [$o['id']]); mhr_flash('Disabled ' . $o['email']); }
        if ($o && $do === 'enable') { mhr_q("UPDATE mhr_owners SET status = 'active' WHERE id = ?", [$o['id']]); mhr_flash('Enabled ' . $o['email']); }
        if ($o && $do === 'link') { mhr_send_login_link($o, $o['email_verified_at'] ? 'login' : 'verify') ? mhr_flash('Sign-in link sent to ' . $o['email']) : mhr_flash('Email could not be sent; check SMTP settings.', 'err'); }
        mhr_redirect($A . 'owners/');
    }
    $rows = mhr_all("SELECT o.*, (SELECT GROUP_CONCAT(slug SEPARATOR ' ') FROM mhr_listings l WHERE l.owner_id = o.id) AS slugs,
        (SELECT COALESCE(SUM(amount_total),0) FROM mhr_payments p WHERE p.owner_id = o.id AND p.status = 'fulfilled') AS paid FROM mhr_owners o ORDER BY o.id DESC");
    adm_start('Owners', 'owners/'); ?>
  <h1>Owner accounts <small class="muted">(<?= count($rows) ?>)</small></h1>
  <?= mhr_flash() ?>
  <div class="card mhr-scroll"><table class="mhr-table"><thead><tr><th>Name</th><th>Email</th><th>Listings</th><th>Paid</th><th>Joined</th><th>Last sign-in</th><th></th></tr></thead><tbody>
  <?php foreach ($rows as $o): ?>
    <tr><td><?= e($o['name']) ?></td><td><?= e($o['email']) ?><?= $o['email_verified_at'] ? '' : ' <small class="muted">(unconfirmed)</small>' ?><?= $o['status'] !== 'active' ? ' ' . adm_status_chip($o['status']) : '' ?></td>
      <td><?php foreach (array_filter(explode(' ', (string)$o['slugs'])) as $s): ?><a href="<?= e($A . 'listings/' . $s . '/') ?>"><?= e($s) ?></a><br><?php endforeach; ?></td>
      <td><?= e(adm_money((int)$o['paid'])) ?></td><td><?= e(substr($o['created_at'], 0, 10)) ?></td><td><?= e(substr((string)$o['last_login_at'], 0, 16)) ?></td>
      <td><form method="post" class="mhr-inline"><?= mhr_guard_fields(false) ?><input type="hidden" name="id" value="<?= (int)$o['id'] ?>">
        <button class="btn btn-light btn-sm" name="do" value="link">Send sign-in link</button>
        <?= $o['status'] === 'active' ? '<button class="btn btn-light btn-sm" name="do" value="disable">Disable</button>' : '<button class="btn btn-light btn-sm" name="do" value="enable">Enable</button>' ?></form></td></tr>
  <?php endforeach; ?>
  </tbody></table></div>
<?php adm_end(); return; }

if ($page === 'payments') {
    $rows = mhr_all('SELECT * FROM mhr_payments ORDER BY id DESC LIMIT 500');
    adm_start('Payments', 'payments/'); ?>
  <h1>Payments</h1>
  <div class="card mhr-scroll"><table class="mhr-table"><thead><tr><th>Ref</th><th>Created</th><th>Kind</th><th>Listing</th><th>Name / email</th><th>Amount</th><th>Stripe</th><th>Status</th><th>Note</th></tr></thead><tbody>
  <?php foreach ($rows as $p): ?>
    <tr><td>MHR-<?= (int)$p['id'] ?></td><td><?= e(substr($p['created_at'], 0, 16)) ?></td><td><?= e($p['kind']) ?></td><td><a href="<?= e($A . 'listings/' . $p['listing_slug'] . '/') ?>"><?= e($p['listing_slug']) ?></a></td>
      <td><?= e($p['name']) ?><br><small><?= e($p['email']) ?></small></td><td><?= e(adm_money($p['amount_total'], $p['currency'])) ?></td>
      <td><small><?= e($p['payment_status'] ?? '') ?><br><?= e(substr((string)$p['stripe_session_id'], 0, 24)) ?>…</small></td><td><?= adm_status_chip($p['status']) ?></td><td><small><?= e($p['note'] ?? '') ?></small></td></tr>
  <?php endforeach; ?>
  </tbody></table><?php if (!$rows): ?><p class="muted mhr-pad">No payments yet.</p><?php endif; ?></div>
<?php adm_end(); return; }

if ($page === 'messages') {
    $rows = mhr_all('SELECT * FROM mhr_messages ORDER BY created_at DESC, id DESC LIMIT 300');
    adm_start('Messages', 'messages/'); ?>
  <h1>Messages</h1>
  <p class="muted">Contact-form messages and property submissions (including those received before this panel existed).</p>
  <?php foreach ($rows as $m): $b = json_decode((string)$m['body'], true) ?: []; ?>
  <details class="card mhr-msg">
    <summary><span class="mhr-st mhr-st-muted"><?= e($m['kind']) ?></span> <strong><?= e($m['name']) ?></strong> · <?= e($m['subject'] ?: '(no subject)') ?> <small class="muted">· <?= e(substr($m['created_at'], 0, 16)) ?> UTC</small></summary>
    <p><a href="mailto:<?= e($m['email']) ?>"><?= e($m['email']) ?></a> <?= e($m['phone']) ?> <small class="muted">IP <?= e($m['ip'] ?? '') ?></small></p>
    <dl class="mhr-dl"><?php foreach ($b as $k => $val): if ($val === '' || $val === null) continue; ?><dt><?= e($k) ?></dt><dd><?= nl2br(e(is_array($val) ? json_encode($val) : $val)) ?></dd><?php endforeach; ?></dl>
  </details>
  <?php endforeach; if (!$rows): ?><div class="card form-card"><p class="muted">No messages yet.</p></div><?php endif;
    adm_end(); return; }

if ($page === 'settings') {
    $result = null;
    if ($method === 'POST' && adm_post_ok()) {
        $do = (string)($_POST['do'] ?? '');
        if ($do === 'save') {
            $sk = trim((string)($_POST['stripe_secret'] ?? ''));
            $wh = trim((string)($_POST['stripe_webhook_secret'] ?? ''));
            $price = (float)str_replace(['$', ','], '', (string)($_POST['price'] ?? '10'));
            $err = [];
            if ($sk !== '' && !preg_match('/^(sk|rk)_(live|test)_[A-Za-z0-9]{10,}$/', $sk)) $err[] = 'The Stripe secret key should start with sk_live_ or sk_test_ (or rk_ for a restricted key).';
            if ($wh !== '' && !preg_match('/^whsec_[A-Za-z0-9]{10,}$/', $wh)) $err[] = 'The webhook signing secret should start with whsec_.';
            if ($price < 0.5 || $price > 10000) $err[] = 'Price must be between $0.50 and $10,000.';
            $notify = trim((string)($_POST['notify_email'] ?? ''));
            if ($notify !== '' && !filter_var($notify, FILTER_VALIDATE_EMAIL)) $err[] = 'Notification email is not valid.';
            if ($err) foreach ($err as $x) mhr_flash($x, 'err');
            else {
                if ($sk !== '') mhr_setting_set('stripe_secret', mhr_encrypt($sk));
                if ($wh !== '') mhr_setting_set('stripe_webhook_secret', mhr_encrypt($wh));
                if (!empty($_POST['clear_stripe'])) { mhr_setting_set('stripe_secret', ''); mhr_setting_set('stripe_webhook_secret', ''); }
                mhr_setting_set('price_cents', (int)round($price * 100));
                mhr_setting_set('notify_email', $notify);
                mhr_flash('Settings saved.');
            }
        } elseif ($do === 'test_stripe') {
            $bal = mhr_stripe('GET', '/v1/balance', [], $err);
            $bal ? mhr_flash('Stripe connection OK (' . (!empty($bal['livemode']) ? 'LIVE' : 'TEST') . ' mode).') : mhr_flash('Stripe test failed: ' . $err, 'err');
        } elseif ($do === 'test_email') {
            $to = trim((string)($_POST['test_to'] ?? '')) ?: mhr_notify_email();
            mhr_mail($to, 'Test email from ' . cfg('name'), "This is a test email sent from the admin panel at " . gmdate('Y-m-d H:i') . " UTC.\n\nIf you can read this, SMTP is working.", null, $err)
                ? mhr_flash('Test email sent to ' . $to . '.') : mhr_flash('Test email failed: ' . $err, 'err');
        } elseif ($do === 'password') {
            $row = mhr_row('SELECT * FROM mhr_admins WHERE id = ?', [$admin['id']]);
            $new = (string)($_POST['new_password'] ?? '');
            if (!password_verify((string)($_POST['current_password'] ?? ''), $row['pass_hash'])) mhr_flash('Current password is wrong.', 'err');
            elseif (strlen($new) < 12) mhr_flash('Use at least 12 characters.', 'err');
            elseif ($new !== ($_POST['new_password2'] ?? '')) mhr_flash('The new passwords do not match.', 'err');
            else { mhr_q('UPDATE mhr_admins SET pass_hash = ? WHERE id = ?', [password_hash($new, PASSWORD_DEFAULT), $admin['id']]); session_regenerate_id(true); mhr_flash('Password changed.'); }
        }
        mhr_redirect($A . 'settings/');
    }
    $sk = mhr_secret_setting('stripe_secret'); $wh = mhr_secret_setting('stripe_webhook_secret');
    $mask = fn($s) => $s === '' ? 'not set' : substr($s, 0, 8) . '…' . substr($s, -4);
    adm_start('Settings', 'settings/'); ?>
  <h1>Settings</h1>
  <?= mhr_flash() ?>
  <div class="mhr-admin-grid">
    <div class="card form-card">
      <h2>Stripe</h2>
      <form method="post" class="form" autocomplete="off"><?= mhr_guard_fields(false) ?>
        <label class="field"><span>Secret key <small>(currently: <?= e($mask($sk)) ?>)</small></span><input type="password" name="stripe_secret" placeholder="sk_live_… (leave blank to keep)" autocomplete="new-password"></label>
        <label class="field"><span>Webhook signing secret <small>(currently: <?= e($mask($wh)) ?>)</small></span><input type="password" name="stripe_webhook_secret" placeholder="whsec_… (leave blank to keep)" autocomplete="new-password"></label>
        <label class="field"><span>Price (USD)</span><span class="field-money"><input type="number" name="price" min="0.5" step="0.01" value="<?= e(number_format(mhr_price_cents() / 100, 2, '.', '')) ?>"></span></label>
        <label class="field"><span>Admin notification email</span><input type="email" name="notify_email" value="<?= e(mhr_setting('notify_email', '')) ?>" placeholder="<?= e(mhr_notify_email()) ?>"></label>
        <label class="mhr-check"><input type="checkbox" name="clear_stripe" value="1"> remove saved Stripe keys</label>
        <button class="btn btn-primary" name="do" value="save">Save settings</button>
      </form>
      <p class="fineprint">Keys are stored encrypted. Webhook URL to add in Stripe (event <code>checkout.session.completed</code>):<br><code><?= e(abs_url('/stripe/webhook')) ?></code></p>
      <div class="btn-row">
        <form method="post" class="mhr-inline"><?= mhr_guard_fields(false) ?><button class="btn btn-outline btn-sm" name="do" value="test_stripe">Test Stripe connection</button></form>
      </div>
    </div>
    <div class="card form-card">
      <h2>Email</h2>
      <p>Sending as <strong><?= e(mhr_cfg('smtp.from') ?: cfg('email')) ?></strong> via <?= e(mhr_cfg('smtp.host') ?: 'smtp.hostinger.com') ?>:<?= (int)(mhr_cfg('smtp.port') ?: 465) ?>.
        SMTP password: <strong><?= mhr_cfg('smtp.pass') ? 'set' : 'NOT SET' ?></strong> <small class="muted">(in the private config file, not here)</small></p>
      <form method="post" class="form"><?= mhr_guard_fields(false) ?><label class="field"><span>Send a test email to</span><input type="email" name="test_to" placeholder="<?= e(mhr_notify_email()) ?>"></label>
        <button class="btn btn-outline btn-sm" name="do" value="test_email">Send test email</button></form>
      <h2>Change admin password</h2>
      <form method="post" class="form" autocomplete="off"><?= mhr_guard_fields(false) ?>
        <label class="field"><span>Current password</span><input type="password" name="current_password" required autocomplete="current-password"></label>
        <label class="field"><span>New password (12+ characters)</span><input type="password" name="new_password" required minlength="12" autocomplete="new-password"></label>
        <label class="field"><span>Repeat new password</span><input type="password" name="new_password2" required minlength="12" autocomplete="new-password"></label>
        <button class="btn btn-light btn-sm" name="do" value="password">Change password</button></form>
    </div>
  </div>
<?php adm_end(); return; }

not_found();
