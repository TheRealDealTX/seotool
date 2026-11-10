<?php

function auth_login(): void
{
    if (current_user()) redirect('/home');
    $error = null;
    if (is_post()) {
        $email = strtolower(input('email'));
        $pass = (string)($_POST['password'] ?? '');
        if (too_many_attempts()) {
            $error = 'Too many login attempts. Please wait 15 minutes and try again.';
        } else {
            $u = one('SELECT * FROM users WHERE email = ? OR username = ?', [$email, $email]);
            if ($u && password_verify($pass, $u['password_hash'])) {
                if ($u['status'] !== 'active') {
                    $error = 'This account has been suspended. Contact support if you think this is a mistake.';
                } else {
                    if (password_needs_rehash($u['password_hash'], PASSWORD_DEFAULT)) {
                        q('UPDATE users SET password_hash = ? WHERE id = ?', [password_hash($pass, PASSWORD_DEFAULT), $u['id']]);
                    }
                    login_user($u);
                    $to = $_SESSION['after_login'] ?? '/home';
                    unset($_SESSION['after_login']);
                    redirect(str_starts_with($to, '/') && !str_starts_with($to, '//') ? $to : '/home');
                }
            } else {
                record_attempt($email);
                $error = 'That email and password don’t match.';
            }
        }
        $_SESSION['old'] = ['email' => $email];
    }
    render('auth/login', ['title' => 'Log in', 'error' => $error, 'bodyClass' => 'auth-page']);
}

function auth_register(): void
{
    if (current_user()) redirect('/home');
    $errors = [];
    if (setting('registration_open', '1') !== '1') {
        render('error', ['title' => 'Registration closed', 'message' => 'New sign-ups are paused right now. Please check back soon.']);
        return;
    }
    if (is_post()) {
        $name = mb_substr(input('name'), 0, 80);
        $email = strtolower(input('email'));
        $username = strtolower(input('username'));
        $pass = (string)($_POST['password'] ?? '');
        if (mb_strlen($name) < 2) $errors['name'] = 'Enter your name.';
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Enter a valid email address.';
        elseif (val('SELECT 1 FROM users WHERE email = ?', [$email])) $errors['email'] = 'An account with this email already exists.';
        if (!preg_match('/^[a-z0-9_]{3,30}$/', $username)) $errors['username'] = '3–30 letters, numbers or underscores.';
        elseif (in_array($username, ['admin', 'administrator', 'support', 'rise', 'moderator', 'root', 'system'], true)
            || val('SELECT 1 FROM users WHERE username = ?', [$username])) $errors['username'] = 'That username is taken.';
        if (strlen($pass) < 8) $errors['password'] = 'Use at least 8 characters.';
        if (empty($_POST['agree'])) $errors['agree'] = 'Please accept the terms to continue.';
        if (!empty($_POST['website'])) $errors['name'] = 'Something went wrong.'; // honeypot
        if (too_many_attempts()) $errors['email'] = 'Too many attempts. Please wait a few minutes.';

        if (!$errors) {
            q('INSERT INTO users (email, username, password_hash, name, looking_for) VALUES (?, ?, ?, ?, ?)', [
                $email, $username, password_hash($pass, PASSWORD_DEFAULT), $name,
                in_array(input('looking_for'), ['need_place', 'have_place', 'either'], true) ? input('looking_for') : 'either',
            ]);
            $u = one('SELECT * FROM users WHERE id = ?', [db()->lastInsertId()]);
            record_attempt($email);
            login_user($u);
            flash('success', 'Welcome to ' . setting('site_name') . '! Set up your profile so the right roommates can find you.');
            redirect('/profile/edit?welcome=1');
        }
        $_SESSION['old'] = compact('name', 'email', 'username');
    }
    render('auth/register', ['title' => 'Create your account', 'errors' => $errors, 'bodyClass' => 'auth-page']);
}

function auth_logout(): void
{
    $_SESSION = [];
    session_destroy();
    redirect('/');
}

function auth_forgot(): void
{
    $sent = false;
    if (is_post()) {
        $email = strtolower(input('email'));
        if (!too_many_attempts()) {
            record_attempt($email);
            $u = one('SELECT * FROM users WHERE email = ? AND status = ?', [$email, 'active']);
            if ($u) {
                $token = bin2hex(random_bytes(32));
                q('UPDATE users SET reset_token = ?, reset_expires = (NOW() + INTERVAL 1 HOUR) WHERE id = ?', [hash('sha256', $token), $u['id']]);
                $link = base_url() . '/reset?token=' . $token;
                send_mail($u['email'], 'Reset your ' . setting('site_name') . ' password',
                    "Hi {$u['name']},\n\nSomeone asked to reset the password for your account. If that was you, open this link within an hour:\n\n$link\n\nIf you didn't ask for this, you can ignore this email.\n\n— " . setting('site_name'));
            }
        }
        $sent = true;
    }
    render('auth/forgot', ['title' => 'Reset password', 'sent' => $sent, 'bodyClass' => 'auth-page']);
}

function auth_reset(): void
{
    $token = input('token');
    $u = $token ? one('SELECT * FROM users WHERE reset_token = ? AND reset_expires > NOW()', [hash('sha256', $token)]) : null;
    $error = null;
    if ($u && is_post()) {
        $pass = (string)($_POST['password'] ?? '');
        if (strlen($pass) < 8) {
            $error = 'Use at least 8 characters.';
        } else {
            q('UPDATE users SET password_hash = ?, reset_token = NULL, reset_expires = NULL WHERE id = ?', [password_hash($pass, PASSWORD_DEFAULT), $u['id']]);
            flash('success', 'Password updated. You can log in now.');
            redirect('/login');
        }
    }
    render('auth/reset', ['title' => 'Choose a new password', 'valid' => (bool)$u, 'token' => $token, 'error' => $error, 'bodyClass' => 'auth-page']);
}
