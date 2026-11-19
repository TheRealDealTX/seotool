<?php
declare(strict_types=1);
defined('M1S') || exit;

function login_page(): void
{
    if (current_user()) {
        redirect(safe_next(input('next')));
    }
    if (is_post()) {
        csrf_check();
        $name = input('username');
        $pass = (string)($_POST['password'] ?? '');
        $next = safe_next(input('next'));
        if (!throttle('login', 10, 900) || !throttle('login-user', 8, 900, strtolower($name))) {
            flash('error', 'Too many sign-in attempts. Wait 15 minutes and try again.');
            redirect('/login/');
        }
        $u = one('SELECT * FROM users WHERE username = ? OR email = ?', [$name, strtolower($name)]);
        if (!$u || !password_verify($pass, $u['pass_hash'])) {
            remember_input(['username']);
            flash('error', 'That username and password do not match.');
            redirect('/login/?next=' . rawurlencode($next));
        }
        if ((int)$u['banned']) {
            flash('error', 'This account is suspended.');
            redirect('/login/');
        }
        if (password_needs_rehash($u['pass_hash'], PASSWORD_DEFAULT)) {
            q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash($pass, PASSWORD_DEFAULT), $u['id']]);
        }
        login_user($u);
        redirect($next);
    }
    render('auth_login', ['next' => safe_next(input('next'))], ['title' => 'Log in', 'robots' => 'noindex, follow']);
}

function register_page(): void
{
    if (current_user()) {
        redirect('/');
    }
    if (is_post()) {
        csrf_check();
        $name = input('username');
        $email = strtolower(input('email'));
        $pass = (string)($_POST['password'] ?? '');
        $errors = [];
        if (!bot_check_passes()) $errors[] = 'Something looked automated about that sign-up. Please try again.';
        if (!valid_username($name)) $errors[] = 'Usernames are 3 to 20 letters, numbers, dashes or underscores.';
        elseif (one('SELECT id FROM users WHERE LOWER(username) = ?', [strtolower($name)])) $errors[] = 'That username is taken.';
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Enter a valid email address (used only for password resets).';
        elseif (one('SELECT id FROM users WHERE email = ?', [$email])) $errors[] = 'An account with that email already exists. Try logging in.';
        if (strlen($pass) < 10) $errors[] = 'Use a password of at least 10 characters.';
        if (empty($_POST['agree'])) $errors[] = 'Please agree to the community guidelines.';
        if (!$errors && !throttle('register', 4, 3600)) $errors[] = 'Too many sign-ups from your network. Try again later.';
        if ($errors) {
            remember_input(['username', 'email']);
            foreach ($errors as $err) flash('error', $err);
            redirect('/register/');
        }
        $id = insert('users', [
            'username' => $name, 'email' => $email, 'pass_hash' => password_hash($pass, PASSWORD_DEFAULT),
            'role' => 'member', 'created_at' => now(), 'last_seen_at' => now(),
        ]);
        login_user(one('SELECT * FROM users WHERE id = ?', [$id]));
        flash('ok', 'Welcome to My 1 Secret, ' . $name . '! Say hi or share your one secret.');
        redirect(safe_next(input('next'), '/forum/'));
    }
    render('auth_register', ['next' => safe_next(input('next'), '')], ['title' => 'Join the community', 'robots' => 'noindex, follow',
        'description' => 'Create a free My 1 Secret account to post, comment and vote in the community.']);
}

function logout_action(): void
{
    logout_user();
    redirect('/');
}

function forgot_page(): void
{
    if (is_post()) {
        csrf_check();
        $email = strtolower(input('email'));
        if (throttle('forgot', 5, 3600) && filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $u = one('SELECT * FROM users WHERE email = ? AND banned = 0', [$email]);
            if ($u) {
                $token = bin2hex(random_bytes(24));
                update('users', ['reset_hash' => hash('sha256', $token), 'reset_expires' => gmdate('Y-m-d H:i:s', time() + 3600)], 'id = :id', ['id' => $u['id']]);
                $link = abs_url('/reset-password/?u=' . $u['id'] . '&t=' . $token);
                send_mail($u['email'], 'Reset your My 1 Secret password',
                    "Hi {$u['username']},\n\nSomeone (hopefully you) asked to reset your My 1 Secret password.\n\n"
                    . "Choose a new password here (the link works for one hour):\n$link\n\n"
                    . "If you did not ask for this, you can ignore this email.\n\n- My 1 Secret");
            }
        }
        flash('ok', 'If that email belongs to an account, a reset link is on its way. Check your spam folder too.');
        redirect('/login/');
    }
    render('auth_forgot', [], ['title' => 'Reset your password', 'robots' => 'noindex']);
}

function reset_page(): void
{
    $id = (int)input('u');
    $token = input('t');
    $u = $id ? one('SELECT * FROM users WHERE id = ?', [$id]) : null;
    $valid = $u && $u['reset_hash'] && hash_equals($u['reset_hash'], hash('sha256', $token))
        && strtotime($u['reset_expires'] . ' UTC') > time();
    if (!$valid) {
        flash('error', 'That reset link is invalid or expired. Request a new one.');
        redirect('/forgot-password/');
    }
    if (is_post()) {
        csrf_check();
        $pass = (string)($_POST['password'] ?? '');
        if (strlen($pass) < 10) {
            flash('error', 'Use a password of at least 10 characters.');
            redirect('/reset-password/?u=' . $id . '&t=' . rawurlencode($token));
        }
        update('users', ['pass_hash' => password_hash($pass, PASSWORD_DEFAULT), 'reset_hash' => null, 'reset_expires' => null,
            'session_epoch' => (int)$u['session_epoch'] + 1], 'id = :id', ['id' => $u['id']]);
        login_user(one('SELECT * FROM users WHERE id = ?', [$u['id']]));
        flash('ok', 'Password updated. You are logged in.');
        redirect('/');
    }
    render('auth_reset', ['uid' => $id, 'token' => $token], ['title' => 'Choose a new password', 'robots' => 'noindex']);
}

function settings_page(): void
{
    $u = require_login();
    if (is_post()) {
        $section = input('section');
        if ($section === 'profile') {
            $display = mb_substr(trim(strip_tags(input('display_name'))), 0, 60);
            $bio = mb_substr(trim(input('bio')), 0, 500);
            update('users', ['display_name' => $display ?: null, 'bio' => $bio ?: null], 'id = :id', ['id' => $u['id']]);
            flash('ok', 'Profile saved.');
        } elseif ($section === 'email') {
            $email = strtolower(input('email'));
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
                flash('error', 'Enter a valid email address.');
            } elseif (one('SELECT id FROM users WHERE email = ? AND id <> ?', [$email, $u['id']])) {
                flash('error', 'That email is used by another account.');
            } elseif (!password_verify((string)($_POST['current_password'] ?? ''), $u['pass_hash'])) {
                flash('error', 'Your current password is not correct.');
            } else {
                update('users', ['email' => $email], 'id = :id', ['id' => $u['id']]);
                flash('ok', 'Email updated.');
            }
        } elseif ($section === 'password') {
            $new = (string)($_POST['new_password'] ?? '');
            if (!password_verify((string)($_POST['current_password'] ?? ''), $u['pass_hash'])) {
                flash('error', 'Your current password is not correct.');
            } elseif (strlen($new) < 10) {
                flash('error', 'Use a new password of at least 10 characters.');
            } else {
                $epoch = (int)$u['session_epoch'] + 1;
                update('users', ['pass_hash' => password_hash($new, PASSWORD_DEFAULT), 'session_epoch' => $epoch], 'id = :id', ['id' => $u['id']]);
                login_user(one('SELECT * FROM users WHERE id = ?', [$u['id']]));
                flash('ok', 'Password changed. Other devices were signed out.');
            }
        }
        redirect('/settings/');
    }
    render('settings', ['u' => $u], ['title' => 'Account settings', 'robots' => 'noindex']);
}

function profile_page(string $username): void
{
    $p = one('SELECT * FROM users WHERE username = ?', [$username]);
    if (!$p) {
        $p = one('SELECT * FROM users WHERE LOWER(username) = ?', [strtolower($username)]);
        $p ? redirect(user_url($p), 301) : not_found();
    }
    $tab = ($_GET['tab'] ?? '') === 'comments' ? 'comments' : 'posts';
    $page = page_num();
    $per = 20;
    if ($tab === 'posts') {
        $items = all(THREAD_SELECT . ' WHERE t.user_id = :u AND t.removed = 0 AND t.status = \'live\' AND t.deleted = 0 ORDER BY t.created_at DESC LIMIT :l OFFSET :o',
            ['u' => $p['id'], 'l' => $per + 1, 'o' => ($page - 1) * $per]);
    } else {
        $items = all("SELECT c.*, t.title AS thread_title, t.slug AS thread_slug, t.id AS thread_id, cm.slug AS community_slug,
                a.title AS article_title, a.slug AS article_slug
            FROM comments c
            LEFT JOIN threads t ON c.target_type = 'thread' AND t.id = c.target_id
            LEFT JOIN communities cm ON cm.id = t.community_id
            LEFT JOIN articles a ON c.target_type = 'article' AND a.id = c.target_id
            WHERE c.user_id = :u AND c.removed = 0 AND c.deleted = 0 ORDER BY c.created_at DESC LIMIT :l OFFSET :o",
            ['u' => $p['id'], 'l' => $per + 1, 'o' => ($page - 1) * $per]);
    }
    $hasNext = count($items) > $per;
    $items = array_slice($items, 0, $per);
    $counts = [
        'posts' => (int)val('SELECT COUNT(*) FROM threads WHERE user_id = ? AND status = \'live\' AND removed = 0 AND deleted = 0', [$p['id']]),
        'comments' => (int)val('SELECT COUNT(*) FROM comments WHERE user_id = ? AND removed = 0 AND deleted = 0', [$p['id']]),
        'articles' => (int)val("SELECT COUNT(*) FROM articles WHERE author_id = ? AND status = 'published'", [$p['id']]),
    ];
    $votes = $tab === 'posts' ? my_votes('thread', array_column($items, 'id')) : [];
    $name = $p['display_name'] ?: $p['username'];
    // Profiles with real activity can be indexed; empty ones are thin pages.
    $indexable = !$p['banned'] && ($counts['posts'] + $counts['comments'] >= 5 || $counts['articles'] > 0) && $page === 1 && $tab === 'posts';
    render('profile', compact('p', 'tab', 'items', 'hasNext', 'page', 'counts', 'votes'), [
        'title' => "$name (u/{$p['username']})",
        'description' => $p['bio'] ? excerpt($p['bio'], 145) : "u/{$p['username']} on My 1 Secret: " . plural($counts['posts'], 'post') . ', ' . plural($counts['comments'], 'comment') . '.',
        'canonical' => abs_url(user_url($p)),
        'robots' => $indexable ? null : 'noindex, follow',
        'jsonld' => [['@type' => 'ProfilePage', 'url' => abs_url(user_url($p)), 'dateCreated' => iso_date($p['created_at']),
            'mainEntity' => ['@type' => 'Person', 'name' => $name, 'alternateName' => $p['username'], 'description' => $p['bio'],
                'interactionStatistic' => [['@type' => 'InteractionCounter', 'interactionType' => 'https://schema.org/WriteAction', 'userInteractionCount' => $counts['posts'] + $counts['comments']]]]]],
    ]);
}
