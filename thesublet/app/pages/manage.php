<?php defined('APP') || exit;

// "Add Photos" entry point for a listing: owners go to their edit page; others verify by email.
cache_private();
$l = listing_get((int)$params[0]);
if (!$l) not_found();
$owner = current_owner();
if ($owner && (int)$l['owner_id'] === (int)$owner['id']) redirect('/account/listing/' . $l['id'] . '/#photos');
if (is_admin()) redirect('/admin/listing/' . $l['id'] . '/');
$sent = false; $err = null;
if (is_post()) {
    if ($g = form_guard()) $err = $g;
    elseif (!rate_limit('manage', 5, 3600)) $err = 'Too many attempts. Try again later.';
    else {
        $email = strtolower(post('email'));
        if ($email === strtolower($l['contact_email'])) {
            if ($l['tier'] === 'paid' && $l['owner_id']) {
                send_mail($email, 'Your sign-in link for The Sublet', view('emails/login', ['link' => magic_link_create((int)$l['owner_id'])]));
            } else {
                send_mail($email, 'Add photos to your listing on The Sublet', view('emails/upgrade', ['l' => $l]));
            }
        }
        $sent = true; // same response either way, so emails can't be probed
    }
}
ob_start(); ?>
<div class="wrap narrow section">
  <h1>Add photos to this listing</h1>
  <p class="lead">“<?= e($l['title']) ?>”</p>
  <?php if ($sent): ?>
    <div class="flash flash-ok">If that email matches the listing, we’ve sent instructions to it. Check your inbox (and spam folder).</div>
  <?php else: ?>
    <?php if ($err): ?><div class="flash flash-err"><?= e($err) ?></div><?php endif; ?>
    <p>Are you the host? Enter the email address you used for this listing. <?= $l['tier'] === 'paid' ? 'We’ll send you a sign-in link to your dashboard, where you can upload photos.' : 'Photo uploads and editing come with a verified listing (' . e(price_label()) . ' one-time). We’ll email you a link to upgrade, after which you can add photos from your dashboard.' ?></p>
    <form method="post" class="stack"><?= csrf_field() ?><?= honeypot_field() ?>
      <label>Listing email<input type="email" name="email" required autocomplete="email"></label>
      <button class="btn" type="submit">Email me a link</button>
    </form>
    <p class="small muted">Not the host? Photos can only be added by the person who posted the listing. If something looks wrong, use “Report listing” on the listing page.</p>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Add photos | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
