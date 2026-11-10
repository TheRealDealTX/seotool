<?php

function profile_show(string $username): void
{
    $me = require_login();
    $u = one('SELECT * FROM users WHERE username = ?', [strtolower($username)]);
    $isMe = $u && (int)$u['id'] === (int)$me['id'];
    if (!$u || ($u['status'] !== 'active' && !is_admin())) not_found();
    if (!$isMe && !is_admin() && is_blocked_between((int)$me['id'], (int)$u['id'])) {
        $iBlocked = (bool)val('SELECT 1 FROM blocks WHERE blocker_id = ? AND blocked_id = ?', [$me['id'], $u['id']]);
        render('profile_blocked', ['title' => $u['name'], 'u' => $u, 'iBlocked' => $iBlocked]);
        return;
    }
    if (!$isMe && !$u['profile_visible'] && !is_admin() && friend_status((int)$me['id'], (int)$u['id']) !== 'friends') {
        render('error', ['title' => 'Private profile', 'message' => 'This member has hidden their profile.']);
        return;
    }
    $props = all("SELECT p.*, EXISTS(SELECT 1 FROM user_properties x WHERE x.user_id = ? AND x.property_id = p.id) AS shared
        FROM properties p JOIN user_properties up ON up.property_id = p.id
        WHERE up.user_id = ? AND p.status = 'approved' ORDER BY p.name", [$me['id'], $u['id']]);
    $sharedCount = count(array_filter($props, fn($p) => $p['shared']));
    $match = $isMe ? null : match_score($me, $u, $sharedCount);
    $friendCount = count(friend_ids((int)$u['id']));
    $mutual = $isMe ? [] : array_values(array_intersect(friend_ids((int)$me['id']), friend_ids((int)$u['id'])));
    $mutualUsers = $mutual ? all('SELECT id, name, username, avatar FROM users WHERE id IN (' . implode(',', array_slice($mutual, 0, 6)) . ')') : [];

    require_once APP_DIR . '/pages/feed.php';
    $posts = load_posts('p.user_id = ?', [(int)$u['id']], 10);

    render('profile', [
        'title' => $u['name'], 'u' => $u, 'isMe' => $isMe, 'props' => $props, 'match' => $match,
        'fstatus' => $isMe ? 'self' : friend_status((int)$me['id'], (int)$u['id']),
        'friendCount' => $friendCount, 'mutualUsers' => $mutualUsers, 'mutualCount' => count($mutual),
        'posts' => $posts, 'canMessage' => !$isMe && can_message((int)$me['id'], (int)$u['id']),
        'mainClass' => 'main-wide',
    ]);
}

function profile_edit(): void
{
    $me = require_login();
    $errors = [];
    if (is_post()) {
        $d = [
            'name' => mb_substr(input('name'), 0, 80),
            'bio' => mb_substr(input('bio'), 0, 1500),
            'birth_year' => (int)input('birth_year') ?: null,
            'gender' => array_key_exists(input('gender'), LABELS['gender']) ? input('gender') : '',
            'occupation' => mb_substr(input('occupation'), 0, 100) ?: null,
            'city' => mb_substr(input('city'), 0, 100) ?: null,
            'budget_min' => (int)input('budget_min') ?: null,
            'budget_max' => (int)input('budget_max') ?: null,
            'move_in_date' => preg_match('/^\d{4}-\d{2}-\d{2}$/', input('move_in_date')) ? input('move_in_date') : null,
            'lease_months' => (int)input('lease_months') ?: null,
            'looking_for' => array_key_exists(input('looking_for'), LABELS['looking_for']) ? input('looking_for') : 'either',
            'cleanliness' => max(1, min(5, (int)input('cleanliness') ?: 3)),
            'sleep_schedule' => array_key_exists(input('sleep_schedule'), LABELS['sleep_schedule']) ? input('sleep_schedule') : 'normal',
            'smoking' => array_key_exists(input('smoking'), LABELS['smoking']) ? input('smoking') : 'no',
            'pets' => array_key_exists(input('pets'), LABELS['pets']) ? input('pets') : 'ok',
            'guests' => array_key_exists(input('guests'), LABELS['guests']) ? input('guests') : 'sometimes',
            'work_from_home' => input('work_from_home') ? 1 : 0,
            'gender_pref' => array_key_exists(input('gender_pref'), LABELS['gender_pref']) ? input('gender_pref') : 'any',
            'interests' => mb_substr(implode(', ', array_slice(array_filter(array_map('trim', explode(',', input('interests')))), 0, 12)), 0, 255) ?: null,
            'instagram' => preg_replace('/[^A-Za-z0-9_.]/', '', ltrim(input('instagram'), '@')) ?: null,
        ];
        if (mb_strlen($d['name']) < 2) $errors[] = 'Enter your name.';
        $y = (int)date('Y');
        if ($d['birth_year'] && ($d['birth_year'] > $y - 18 || $d['birth_year'] < $y - 100)) $errors[] = 'Birth year must make you 18 or older.';
        if ($d['budget_min'] && $d['budget_max'] && $d['budget_min'] > $d['budget_max']) $errors[] = 'Minimum budget is higher than maximum.';
        try {
            $avatar = save_upload('avatar', 'avatars', 500, 500, true);
            if ($avatar) {
                delete_upload('avatars', $me['avatar']);
                $d['avatar'] = $avatar;
            } elseif (input('remove_avatar')) {
                delete_upload('avatars', $me['avatar']);
                $d['avatar'] = null;
            }
        } catch (RuntimeException $e) {
            $errors[] = $e->getMessage();
        }
        if (!$errors) {
            $sets = implode(', ', array_map(fn($k) => "$k = ?", array_keys($d)));
            q("UPDATE users SET $sets WHERE id = ?", array_merge(array_values($d), [$me['id']]));
            // Preferred properties
            $chosen = array_map('intval', (array)($_POST['properties'] ?? []));
            q('DELETE FROM user_properties WHERE user_id = ?', [$me['id']]);
            foreach (array_slice(array_unique($chosen), 0, 25) as $pid) {
                if (val("SELECT 1 FROM properties WHERE id = ? AND status = 'approved'", [$pid])) {
                    q('INSERT IGNORE INTO user_properties (user_id, property_id) VALUES (?, ?)', [$me['id'], $pid]);
                }
            }
            flash('success', 'Profile saved.');
            redirect(input('welcome') ? '/discover' : '/u/' . $me['username']);
        }
        $me = array_merge($me, $d);
    }
    $mine = array_map('intval', array_column(all('SELECT property_id FROM user_properties WHERE user_id = ?', [$me['id']]), 'property_id'));
    if (is_post()) $mine = array_map('intval', (array)($_POST['properties'] ?? []));
    // Show the member's picks plus the most popular properties; the rest are reachable through search.
    $ids = $mine ? implode(',', array_map('intval', $mine)) : '0';
    $properties = all("SELECT p.id, p.name, p.city FROM properties p
        WHERE p.status = 'approved' AND (p.id IN ($ids) OR p.id IN (SELECT id FROM (SELECT property_id AS id FROM user_properties GROUP BY property_id ORDER BY COUNT(*) DESC LIMIT 12) t)
          OR p.is_featured = 1)
        ORDER BY p.id IN ($ids) DESC, p.name LIMIT 60");
    render('profile_edit', ['title' => 'Edit profile', 'u' => $me, 'errors' => $errors, 'properties' => $properties, 'mine' => $mine, 'welcome' => (bool)input('welcome')]);
}

function profile_settings(): void
{
    $me = require_login();
    if (is_post()) {
        $action = input('action');
        if ($action === 'password') {
            if (!password_verify((string)($_POST['current'] ?? ''), $me['password_hash'])) {
                flash('error', 'Your current password is incorrect.');
            } elseif (strlen((string)($_POST['new'] ?? '')) < 8) {
                flash('error', 'New password must be at least 8 characters.');
            } else {
                q('UPDATE users SET password_hash = ? WHERE id = ?', [password_hash((string)$_POST['new'], PASSWORD_DEFAULT), $me['id']]);
                flash('success', 'Password changed.');
            }
        } elseif ($action === 'email') {
            $email = strtolower(input('email'));
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) flash('error', 'Enter a valid email.');
            elseif (!password_verify((string)($_POST['password'] ?? ''), $me['password_hash'])) flash('error', 'Password is incorrect.');
            elseif (val('SELECT 1 FROM users WHERE email = ? AND id <> ?', [$email, $me['id']])) flash('error', 'That email is already in use.');
            else { q('UPDATE users SET email = ? WHERE id = ?', [$email, $me['id']]); flash('success', 'Email updated.'); }
        } elseif ($action === 'privacy') {
            q('UPDATE users SET profile_visible = ?, email_notifications = ? WHERE id = ?', [input('profile_visible') ? 1 : 0, input('email_notifications') ? 1 : 0, $me['id']]);
            flash('success', 'Privacy settings saved.');
        } elseif ($action === 'delete') {
            if (!password_verify((string)($_POST['password'] ?? ''), $me['password_hash'])) {
                flash('error', 'Password is incorrect — account not deleted.');
            } elseif ($me['role'] === 'admin' && (int)val("SELECT COUNT(*) FROM users WHERE role = 'admin'") <= 1) {
                flash('error', 'You are the only administrator. Promote someone else before deleting this account.');
            } else {
                delete_user_completely((int)$me['id']);
                $_SESSION = [];
                session_destroy();
                session_start();
                flash('success', 'Your account has been deleted.');
                redirect('/');
            }
        }
        redirect('/settings');
    }
    $blocked = all('SELECT u.id, u.name, u.username, u.avatar FROM blocks b JOIN users u ON u.id = b.blocked_id WHERE b.blocker_id = ? ORDER BY b.created_at DESC', [$me['id']]);
    render('settings', ['title' => 'Settings', 'u' => $me, 'blocked' => $blocked]);
}

function delete_user_completely(int $id): void
{
    $u = one('SELECT avatar FROM users WHERE id = ?', [$id]);
    if (!$u) return;
    delete_upload('avatars', $u['avatar']);
    foreach (all('SELECT image FROM posts WHERE user_id = ? AND image IS NOT NULL', [$id]) as $p) {
        delete_upload('posts', $p['image']);
    }
    q('DELETE FROM users WHERE id = ?', [$id]);
}
