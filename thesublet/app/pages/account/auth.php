<?php defined('APP') || exit;

// Two-step: GET shows a button (so email link scanners can't burn the token), POST signs in.
cache_private();
$token = $params[0];
$next = preg_match('#^/account/[a-z0-9/]*$#', get('next')) ? get('next') : '/account/';
if (is_post()) {
    if ($g = form_guard()) { flash($g, 'err'); redirect('/login/'); }
    $o = magic_link_consume($token);
    if (!$o) { flash('That sign-in link has expired or was already used. Request a new one below.', 'err'); redirect('/login/'); }
    owner_login($o);
    flash('Signed in. Your email is verified.', 'ok');
    redirect($next, 303);
}
$valid = magic_token_valid($token);
ob_start(); ?>
<div class="wrap narrow section center">
  <?php if ($valid): ?>
    <h1>Sign in to The Sublet</h1>
    <p>Click below to confirm your email and open your host dashboard.</p>
    <form method="post"><?= csrf_field() ?><button class="btn btn-lg" type="submit">Sign in &amp; verify email</button></form>
  <?php else: ?>
    <h1>This link has expired</h1>
    <p>Sign-in links work once and expire after 60 minutes.</p>
    <p><a class="btn" href="/login/">Send a new link</a></p>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Sign in | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
