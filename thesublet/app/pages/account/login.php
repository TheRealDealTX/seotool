<?php defined('APP') || exit;

cache_private();
if (current_owner()) redirect('/account/');
$sent = false; $err = null;
$next = get('next');
if (is_post()) {
    if ($g = form_guard()) $err = $g;
    elseif (!rate_limit('login', 5, 900)) $err = 'Too many sign-in requests. Please wait a few minutes.';
    else {
        $email = strtolower(post('email'));
        if (!valid_email($email)) $err = 'Enter a valid email address.';
        else {
            $o = row("SELECT * FROM owners WHERE email = ? AND status = 'active'", [$email]);
            if ($o) {
                $link = magic_link_create((int)$o['id']);
                if (preg_match('#^/account/[a-z0-9/]*$#', post('next'))) $link .= '?next=' . rawurlencode(post('next'));
                send_mail($email, 'Your sign-in link for The Sublet', view('emails/login', ['link' => $link]));
            }
            $sent = true;
        }
    }
}
ob_start(); ?>
<div class="wrap narrow section">
  <h1>Host sign-in</h1>
  <?= flashes() ?>
  <?php if ($sent): ?>
    <div class="flash flash-ok">If there’s a host account for that email, a sign-in link is on its way. It works once and expires in 60 minutes.</div>
    <p class="small muted">No email? Check spam, or make sure you use the address you paid with. Host accounts are created when you buy a verified listing.</p>
  <?php else: ?>
    <?php if ($err): ?><div class="flash flash-err"><?= e($err) ?></div><?php endif; ?>
    <p>No passwords — enter your email and we’ll send you a secure one-time sign-in link.</p>
    <form method="post" class="stack"><?= csrf_field() ?><?= honeypot_field() ?>
      <input type="hidden" name="next" value="<?= e($next) ?>">
      <label>Email<input type="email" name="email" required autocomplete="email" autofocus></label>
      <button class="btn" type="submit">Email me a sign-in link</button>
    </form>
    <p class="small muted">Host accounts come with verified listings. Posted a free listing? Use the upgrade link in your approval email, or <a href="/post-a-sublet/">post a verified listing</a>.</p>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Host sign-in | The Sublet', 'robots' => 'noindex', 'canonical' => '/login/', 'body' => ob_get_clean()]);
