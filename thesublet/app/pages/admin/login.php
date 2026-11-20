<?php defined('APP') || exit;

cache_private();
header('X-Robots-Tag: noindex, nofollow');
$err = null;
if (is_post()) {
    if ($g = form_guard()) $err = $g;
    elseif (!rate_limit('adminlogin', 8, 900)) $err = 'Too many attempts. Wait 15 minutes.';
    else {
        $hash = admin_pass_hash();
        $userOk = hash_equals((string)cfg('admin_user', 'admin'), post('user'));
        if ($hash !== '' && $userOk && password_verify(post('pass'), $hash)) {
            session_boot();
            session_regenerate_id(true);
            $_SESSION['admin'] = 1;
            $_SESSION['admin_ip'] = client_ip();
            redirect('/admin/');
        }
        $err = 'Incorrect username or password.';
        usleep(400000);
    }
}
page(['title' => 'Admin sign-in · The Sublet', 'robots' => 'noindex, nofollow', 'body' =>
    '<div class="wrap narrow section"><h1>Admin sign-in</h1>' . ($err ? '<div class="flash flash-err">' . e($err) . '</div>' : '')
    . '<form method="post" class="stack">' . csrf_field() . honeypot_field()
    . '<label>Username<input name="user" required autocomplete="username"></label><label>Password<input type="password" name="pass" required autocomplete="current-password"></label>'
    . '<button class="btn" type="submit">Sign in</button></form></div>']);
