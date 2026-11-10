<?php

function admin_dashboard(): void
{
    require_admin();
    $stats = [
        'users' => (int)val('SELECT COUNT(*) FROM users'),
        'active7' => (int)val('SELECT COUNT(*) FROM users WHERE last_seen > (NOW() - INTERVAL 7 DAY)'),
        'new7' => (int)val('SELECT COUNT(*) FROM users WHERE created_at > (NOW() - INTERVAL 7 DAY)'),
        'suspended' => (int)val("SELECT COUNT(*) FROM users WHERE status = 'suspended'"),
        'properties' => (int)val("SELECT COUNT(*) FROM properties WHERE status = 'approved'"),
        'pending' => (int)val("SELECT COUNT(*) FROM properties WHERE status = 'pending'"),
        'reports' => (int)val("SELECT COUNT(*) FROM reports WHERE status = 'open'"),
        'posts' => (int)val('SELECT COUNT(*) FROM posts'),
        'messages' => (int)val('SELECT COUNT(*) FROM messages'),
        'messages7' => (int)val('SELECT COUNT(*) FROM messages WHERE created_at > (NOW() - INTERVAL 7 DAY)'),
        'friendships' => (int)val("SELECT COUNT(*) FROM friendships WHERE status = 'accepted'"),
        'interests' => (int)val('SELECT COUNT(*) FROM user_properties'),
    ];
    $signups = [];
    foreach (all('SELECT DATE(created_at) d, COUNT(*) n FROM users WHERE created_at > (CURDATE() - INTERVAL 29 DAY) GROUP BY DATE(created_at)') as $r) {
        $signups[$r['d']] = (int)$r['n'];
    }
    $series = [];
    for ($i = 29; $i >= 0; $i--) {
        $d = date('Y-m-d', strtotime("-$i day"));
        $series[] = ['d' => $d, 'n' => $signups[$d] ?? 0];
    }
    $recentUsers = all('SELECT * FROM users ORDER BY id DESC LIMIT 8');
    $topProps = all("SELECT p.id, p.name, p.slug, COUNT(up.user_id) n FROM properties p LEFT JOIN user_properties up ON up.property_id = p.id
        WHERE p.status = 'approved' GROUP BY p.id ORDER BY n DESC LIMIT 8");
    render('admin/dashboard', compact('stats', 'series', 'recentUsers', 'topProps') + ['title' => 'Admin']);
}

function admin_users(): void
{
    require_admin();
    if (is_post()) {
        $ids = array_map('intval', (array)($_POST['ids'] ?? []));
        $act = input('bulk');
        $ids = array_filter($ids, fn($i) => $i !== uid());
        if ($act === 'delete_demo') {
            require_once APP_DIR . '/pages/profile.php';
            $demo = array_map('intval', array_column(all('SELECT id FROM users WHERE is_demo = 1'), 'id'));
            foreach ($demo as $d) delete_user_completely($d);
            audit('users.delete_demo', count($demo) . ' demo accounts');
            flash('success', 'Deleted ' . count($demo) . ' demo accounts.');
            back('/admin/users');
        }
        if ($ids && in_array($act, ['suspend', 'activate', 'verify'], true)) {
            $in = implode(',', $ids);
            if ($act === 'suspend') q("UPDATE users SET status = 'suspended' WHERE id IN ($in) AND role <> 'admin'");
            if ($act === 'activate') q("UPDATE users SET status = 'active' WHERE id IN ($in)");
            if ($act === 'verify') q("UPDATE users SET is_verified = 1 WHERE id IN ($in)");
            audit("users.bulk_$act", 'ids: ' . $in);
            flash('success', 'Updated ' . count($ids) . ' member(s).');
        }
        back('/admin/users');
    }
    $s = mb_substr(input('q'), 0, 80);
    $role = in_array(input('role'), ['user', 'admin', 'demo'], true) ? input('role') : '';
    $status = in_array(input('status'), ['active', 'suspended'], true) ? input('status') : '';
    $where = ['1'];
    $params = [];
    if ($s !== '') { $where[] = '(name LIKE ? OR email LIKE ? OR username LIKE ? OR city LIKE ?)'; $l = "%$s%"; array_push($params, $l, $l, $l, $l); }
    if ($role === 'demo') { $where[] = 'is_demo = 1'; }
    elseif ($role) { $where[] = 'role = ?'; $params[] = $role; }
    if ($status) { $where[] = 'status = ?'; $params[] = $status; }
    $w = implode(' AND ', $where);
    $total = (int)val("SELECT COUNT(*) FROM users WHERE $w", $params);
    [$page, $pages, $offset] = paginate($total, 30);
    $users = all("SELECT u.*, (SELECT COUNT(*) FROM reports r WHERE r.target_type = 'user' AND r.target_id = u.id) AS report_count
        FROM users u WHERE $w ORDER BY u.id DESC LIMIT 30 OFFSET $offset", $params);
    if (input('export') === 'csv') {
        header('Content-Type: text/csv');
        header('Content-Disposition: attachment; filename="members-' . date('Y-m-d') . '.csv"');
        $out = fopen('php://output', 'w');
        fputcsv($out, ['id', 'name', 'username', 'email', 'role', 'status', 'city', 'looking_for', 'budget_min', 'budget_max', 'move_in_date', 'created_at', 'last_seen']);
        foreach (all("SELECT id, name, username, email, role, status, city, looking_for, budget_min, budget_max, move_in_date, created_at, last_seen FROM users WHERE $w ORDER BY id", $params) as $r) {
            fputcsv($out, $r);
        }
        audit('users.export', "rows matching '$s'");
        exit;
    }
    $demoCount = (int)val('SELECT COUNT(*) FROM users WHERE is_demo = 1');
    render('admin/users', compact('users', 'total', 'page', 'pages', 's', 'role', 'status', 'demoCount') + ['title' => 'Members']);
}

function admin_user(string $id): void
{
    require_admin();
    $u = one('SELECT * FROM users WHERE id = ?', [(int)$id]);
    if (!$u) not_found();
    if (is_post()) {
        $act = input('action');
        $self = (int)$u['id'] === uid();
        switch ($act) {
            case 'save':
                $email = strtolower(input('email'));
                $username = strtolower(input('username'));
                if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { flash('error', 'Invalid email.'); break; }
                if (!preg_match('/^[a-z0-9_]{3,30}$/', $username)) { flash('error', 'Invalid username.'); break; }
                if (val('SELECT 1 FROM users WHERE (email = ? OR username = ?) AND id <> ?', [$email, $username, $u['id']])) { flash('error', 'Email or username already in use.'); break; }
                $role = in_array(input('role'), ['user', 'admin'], true) ? input('role') : 'user';
                if ($self && $role !== 'admin') { flash('error', 'You can’t remove your own admin role.'); break; }
                q('UPDATE users SET name = ?, email = ?, username = ?, role = ?, is_verified = ?, city = ? WHERE id = ?', [
                    mb_substr(input('name'), 0, 80), $email, $username, $role, input('is_verified') ? 1 : 0, mb_substr(input('city'), 0, 100) ?: null, $u['id'],
                ]);
                audit('user.update', "user #{$u['id']} ({$u['username']}) role=$role");
                flash('success', 'Member updated.');
                break;
            case 'suspend':
                if ($self) { flash('error', 'You can’t suspend yourself.'); break; }
                q("UPDATE users SET status = 'suspended' WHERE id = ?", [$u['id']]);
                audit('user.suspend', "user #{$u['id']} ({$u['username']})");
                flash('success', 'Member suspended.');
                break;
            case 'activate':
                q("UPDATE users SET status = 'active' WHERE id = ?", [$u['id']]);
                audit('user.activate', "user #{$u['id']} ({$u['username']})");
                flash('success', 'Member reactivated.');
                break;
            case 'password':
                $pw = (string)($_POST['new_password'] ?? '');
                if (strlen($pw) < 8) { flash('error', 'Password must be at least 8 characters.'); break; }
                q('UPDATE users SET password_hash = ? WHERE id = ?', [password_hash($pw, PASSWORD_DEFAULT), $u['id']]);
                audit('user.password_reset', "user #{$u['id']} ({$u['username']})");
                flash('success', 'Password changed. Share it with the member securely.');
                break;
            case 'delete':
                if ($self) { flash('error', 'You can’t delete yourself here.'); break; }
                require_once APP_DIR . '/pages/profile.php';
                delete_user_completely((int)$u['id']);
                audit('user.delete', "user #{$u['id']} ({$u['username']}, {$u['email']})");
                flash('success', 'Member deleted.');
                redirect('/admin/users');
        }
        redirect('/admin/users/' . $u['id']);
    }
    $info = [
        'posts' => (int)val('SELECT COUNT(*) FROM posts WHERE user_id = ?', [$u['id']]),
        'comments' => (int)val('SELECT COUNT(*) FROM comments WHERE user_id = ?', [$u['id']]),
        'friends' => count(friend_ids((int)$u['id'])),
        'messages' => (int)val('SELECT COUNT(*) FROM messages WHERE sender_id = ?', [$u['id']]),
        'blocked_by' => (int)val('SELECT COUNT(*) FROM blocks WHERE blocked_id = ?', [$u['id']]),
    ];
    $reports = all("SELECT r.*, u.username AS reporter FROM reports r LEFT JOIN users u ON u.id = r.reporter_id WHERE r.target_type = 'user' AND r.target_id = ? ORDER BY r.id DESC LIMIT 20", [$u['id']]);
    $props = all('SELECT p.name, p.slug FROM properties p JOIN user_properties up ON up.property_id = p.id WHERE up.user_id = ?', [$u['id']]);
    render('admin/user', compact('u', 'info', 'reports', 'props') + ['title' => 'Member: ' . $u['name']]);
}

function admin_properties(): void
{
    require_admin();
    if (is_post()) {
        $p = one('SELECT * FROM properties WHERE id = ?', [(int)input('id')]);
        if ($p) {
            $act = input('action');
            if ($act === 'approve') {
                q("UPDATE properties SET status = 'approved' WHERE id = ?", [$p['id']]);
                if ($p['created_by']) {
                    q('INSERT IGNORE INTO user_properties (user_id, property_id) VALUES (?, ?)', [$p['created_by'], $p['id']]);
                    notify((int)$p['created_by'], 'property_approved', null, (int)$p['id']);
                }
            } elseif ($act === 'reject') {
                q("UPDATE properties SET status = 'rejected' WHERE id = ?", [$p['id']]);
            } elseif ($act === 'feature') {
                q('UPDATE properties SET is_featured = 1 - is_featured WHERE id = ?', [$p['id']]);
            } elseif ($act === 'delete') {
                delete_upload('properties', $p['image']);
                q('DELETE FROM properties WHERE id = ?', [$p['id']]);
            }
            audit("property.$act", "#{$p['id']} {$p['name']}");
            flash('success', 'Property updated.');
        }
        back('/admin/properties');
    }
    $status = in_array(input('status'), ['approved', 'pending', 'rejected'], true) ? input('status') : '';
    $s = mb_substr(input('q'), 0, 80);
    $where = ['1'];
    $params = [];
    if ($status) { $where[] = 'p.status = ?'; $params[] = $status; }
    if ($s !== '') { $where[] = '(p.name LIKE ? OR p.city LIKE ?)'; array_push($params, "%$s%", "%$s%"); }
    $w = implode(' AND ', $where);
    $total = (int)val("SELECT COUNT(*) FROM properties p WHERE $w", $params);
    [$page, $pages, $offset] = paginate($total, 30);
    $props = all("SELECT p.*, u.username AS creator, (SELECT COUNT(*) FROM user_properties up WHERE up.property_id = p.id) AS interested
        FROM properties p LEFT JOIN users u ON u.id = p.created_by WHERE $w
        ORDER BY FIELD(p.status, 'pending', 'approved', 'rejected'), p.id DESC LIMIT 30 OFFSET $offset", $params);
    render('admin/properties', compact('props', 'status', 's', 'page', 'pages', 'total') + ['title' => 'Properties']);
}

function admin_property(string $id): void
{
    require_admin();
    $isNew = $id === 'new';
    $p = $isNew ? ['id' => 0, 'name' => '', 'address' => '', 'city' => '', 'state' => 'TX', 'zip' => '', 'description' => '', 'website' => '',
        'image' => null, 'image_url' => null, 'external_url' => null, 'rent_min' => '', 'rent_max' => '', 'amenities' => '', 'is_featured' => 0, 'status' => 'approved', 'slug' => '']
        : one('SELECT * FROM properties WHERE id = ?', [(int)$id]);
    if (!$p) not_found();
    $errors = [];
    if (is_post()) {
        $d = [];
        foreach (['name', 'address', 'city', 'state', 'zip', 'website', 'amenities'] as $k) $d[$k] = mb_substr(input($k), 0, $k === 'amenities' ? 500 : 200);
        $d['description'] = mb_substr(input('description'), 0, 5000);
        $d['rent_min'] = (int)input('rent_min') ?: null;
        $d['rent_max'] = (int)input('rent_max') ?: null;
        $d['is_featured'] = input('is_featured') ? 1 : 0;
        $d['status'] = in_array(input('status'), ['approved', 'pending', 'rejected'], true) ? input('status') : 'approved';
        if (mb_strlen($d['name']) < 2) $errors[] = 'Name is required.';
        if ($d['website'] && !preg_match('~^https?://~i', $d['website'])) $d['website'] = 'https://' . $d['website'];
        try {
            $img = save_upload('image', 'properties', 1600, 1000);
            if ($img) { delete_upload('properties', $p['image']); $d['image'] = $img; }
            elseif (input('remove_image')) { delete_upload('properties', $p['image']); $d['image'] = null; }
        } catch (RuntimeException $e) {
            $errors[] = $e->getMessage();
        }
        if (!$errors) {
            foreach (['address', 'city', 'state', 'zip', 'website', 'amenities', 'description'] as $k) $d[$k] = $d[$k] !== '' ? $d[$k] : null;
            if ($isNew) {
                $d['slug'] = unique_slug($d['name']);
                $d['created_by'] = uid();
                $cols = implode(',', array_keys($d));
                q("INSERT INTO properties ($cols) VALUES (" . implode(',', array_fill(0, count($d), '?')) . ')', array_values($d));
                $newId = (int)db()->lastInsertId();
                audit('property.create', "#$newId {$d['name']}");
            } else {
                $d['slug'] = input('slug') !== '' ? unique_slug(input('slug'), (int)$p['id']) : $p['slug'];
                $sets = implode(', ', array_map(fn($k) => "$k = ?", array_keys($d)));
                q("UPDATE properties SET $sets WHERE id = ?", array_merge(array_values($d), [$p['id']]));
                audit('property.update', "#{$p['id']} {$d['name']}");
            }
            flash('success', 'Property saved.');
            redirect('/admin/properties');
        }
        $p = array_merge($p, $d);
    }
    render('admin/property', ['title' => $isNew ? 'New property' : 'Edit property', 'p' => $p, 'isNew' => $isNew, 'errors' => $errors]);
}

function admin_reports(): void
{
    require_admin();
    if (is_post()) {
        $r = one('SELECT * FROM reports WHERE id = ?', [(int)input('id')]);
        if ($r) {
            $act = input('action');
            $note = mb_substr(input('note'), 0, 500) ?: null;
            if ($act === 'remove_content') {
                if ($r['target_type'] === 'post') q("UPDATE posts SET status = 'hidden' WHERE id = ?", [$r['target_id']]);
                if ($r['target_type'] === 'comment') q('DELETE FROM comments WHERE id = ?', [$r['target_id']]);
                if ($r['target_type'] === 'property') q("UPDATE properties SET status = 'rejected' WHERE id = ?", [$r['target_id']]);
                $act = 'resolved';
            } elseif ($act === 'suspend_user') {
                $uidT = report_target_user($r);
                if ($uidT && $uidT !== uid()) q("UPDATE users SET status = 'suspended' WHERE id = ? AND role <> 'admin'", [$uidT]);
                $act = 'resolved';
            }
            if (in_array($act, ['resolved', 'dismissed', 'open'], true)) {
                q('UPDATE reports SET status = ?, admin_note = COALESCE(?, admin_note), resolved_by = ? WHERE id = ?', [$act, $note, uid(), $r['id']]);
            }
            audit('report.' . input('action'), "report #{$r['id']} on {$r['target_type']} #{$r['target_id']}");
            flash('success', 'Report updated.');
        }
        back('/admin/reports');
    }
    $status = in_array(input('status'), ['open', 'resolved', 'dismissed'], true) ? input('status') : 'open';
    $reports = all("SELECT r.*, u.username AS reporter FROM reports r LEFT JOIN users u ON u.id = r.reporter_id WHERE r.status = ? ORDER BY r.id DESC LIMIT 100", [$status]);
    foreach ($reports as &$r) $r['target'] = report_target_summary($r);
    unset($r);
    render('admin/reports', compact('reports', 'status') + ['title' => 'Reports']);
}

function report_target_user(array $r): ?int
{
    $v = match ($r['target_type']) {
        'user' => $r['target_id'],
        'post' => val('SELECT user_id FROM posts WHERE id = ?', [$r['target_id']]),
        'comment' => val('SELECT user_id FROM comments WHERE id = ?', [$r['target_id']]),
        'property' => val('SELECT created_by FROM properties WHERE id = ?', [$r['target_id']]),
        default => null,
    };
    return $v ? (int)$v : null;
}

function report_target_summary(array $r): array
{
    switch ($r['target_type']) {
        case 'user':
            $u = one('SELECT id, name, username, status FROM users WHERE id = ?', [$r['target_id']]);
            return $u ? ['label' => "{$u['name']} (@{$u['username']})" . ($u['status'] === 'suspended' ? ' — suspended' : ''), 'link' => '/admin/users/' . $u['id'], 'text' => ''] : ['label' => 'Deleted member', 'link' => '', 'text' => ''];
        case 'post':
            $p = one('SELECT p.*, u.username FROM posts p JOIN users u ON u.id = p.user_id WHERE p.id = ?', [$r['target_id']]);
            return $p ? ['label' => "Post by @{$p['username']}" . ($p['status'] === 'hidden' ? ' — hidden' : ''), 'link' => '/post/' . $p['id'], 'text' => $p['body']] : ['label' => 'Deleted post', 'link' => '', 'text' => ''];
        case 'comment':
            $c = one('SELECT c.*, u.username FROM comments c JOIN users u ON u.id = c.user_id WHERE c.id = ?', [$r['target_id']]);
            return $c ? ['label' => "Comment by @{$c['username']}", 'link' => '/post/' . $c['post_id'] . '#comment-' . $c['id'], 'text' => $c['body']] : ['label' => 'Deleted comment', 'link' => '', 'text' => ''];
        case 'property':
            $p = one('SELECT * FROM properties WHERE id = ?', [$r['target_id']]);
            return $p ? ['label' => 'Property: ' . $p['name'], 'link' => '/admin/properties/' . $p['id'], 'text' => ''] : ['label' => 'Deleted property', 'link' => '', 'text' => ''];
    }
    return ['label' => '?', 'link' => '', 'text' => ''];
}

function admin_posts(): void
{
    require_admin();
    if (is_post()) {
        $p = one('SELECT * FROM posts WHERE id = ?', [(int)input('id')]);
        if ($p) {
            $act = input('action');
            if ($act === 'hide') q("UPDATE posts SET status = 'hidden' WHERE id = ?", [$p['id']]);
            if ($act === 'show') q("UPDATE posts SET status = 'visible' WHERE id = ?", [$p['id']]);
            if ($act === 'delete') { delete_upload('posts', $p['image']); q('DELETE FROM posts WHERE id = ?', [$p['id']]); }
            audit("post.$act", "post #{$p['id']} by user #{$p['user_id']}");
            flash('success', 'Post updated.');
        }
        back('/admin/posts');
    }
    $status = in_array(input('status'), ['visible', 'hidden'], true) ? input('status') : '';
    $s = mb_substr(input('q'), 0, 80);
    $where = ['1'];
    $params = [];
    if ($status) { $where[] = 'p.status = ?'; $params[] = $status; }
    if ($s !== '') { $where[] = '(p.body LIKE ? OR u.username LIKE ?)'; array_push($params, "%$s%", "%$s%"); }
    $w = implode(' AND ', $where);
    $total = (int)val("SELECT COUNT(*) FROM posts p JOIN users u ON u.id = p.user_id WHERE $w", $params);
    [$page, $pages, $offset] = paginate($total, 30);
    $posts = all("SELECT p.*, u.name, u.username, pr.name AS property_name,
        (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.id) likes, (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) comments
        FROM posts p JOIN users u ON u.id = p.user_id LEFT JOIN properties pr ON pr.id = p.property_id
        WHERE $w ORDER BY p.id DESC LIMIT 30 OFFSET $offset", $params);
    render('admin/posts', compact('posts', 'status', 's', 'page', 'pages', 'total') + ['title' => 'Posts']);
}

function admin_settings(): void
{
    require_admin();
    $keys = ['site_name', 'tagline', 'announcement', 'admin_email', 'messaging_friends_only', 'allow_property_submissions', 'require_property_approval', 'registration_open'];
    if (is_post() && input('test_email') !== '') {
        $to = filter_var(input('test_to'), FILTER_VALIDATE_EMAIL) ?: current_user()['email'];
        $err = null;
        $ok = send_mail($to, 'Test email from ' . setting('site_name'), "This is a test email from the admin panel. If you can read this, email delivery works.", $err);
        audit('settings.test_email', "to $to: " . ($ok ? 'sent' : "failed $err"));
        flash($ok ? 'success' : 'error', $ok ? "Test email sent to $to." : "Email failed: $err");
        redirect('/admin/settings');
    }
    if (is_post()) {
        foreach ($keys as $k) {
            $v = in_array($k, ['messaging_friends_only', 'allow_property_submissions', 'require_property_approval', 'registration_open'], true)
                ? (input($k) ? '1' : '0') : mb_substr(input($k), 0, 500);
            q('INSERT INTO settings (k, v) VALUES (?, ?) ON DUPLICATE KEY UPDATE v = VALUES(v)', [$k, $v]);
        }
        audit('settings.update', '');
        flash('success', 'Settings saved.');
        redirect('/admin/settings');
    }
    $vals = [];
    foreach ($keys as $k) $vals[$k] = setting($k, '');
    render('admin/settings', ['title' => 'Site settings', 'v' => $vals]);
}

function admin_audit(): void
{
    require_admin();
    $total = (int)val('SELECT COUNT(*) FROM audit_log');
    [$page, $pages, $offset] = paginate($total, 50);
    $rows = all("SELECT a.*, u.username FROM audit_log a LEFT JOIN users u ON u.id = a.admin_id ORDER BY a.id DESC LIMIT 50 OFFSET $offset");
    render('admin/audit', compact('rows', 'page', 'pages') + ['title' => 'Audit log']);
}

function admin_sync(): void
{
    require_admin();
    if (is_post()) {
        if (input('save_source') !== '') {
            $src = rtrim(input('sync_source'), '/');
            if (filter_var($src, FILTER_VALIDATE_URL)) {
                q('INSERT INTO settings (k, v) VALUES (?, ?) ON DUPLICATE KEY UPDATE v = VALUES(v)', ['sync_source', $src]);
                flash('success', 'Source saved.');
            }
            redirect('/admin/sync');
        }
        @set_time_limit(120);
        $page = max(1, (int)input('page'));
        try {
            $r = sync_rise_page($page);
        } catch (Throwable $e) {
            json_out(['error' => $e->getMessage()], 502);
        }
        if ($page >= $r['total_pages']) {
            $count = (int)val('SELECT COUNT(*) FROM properties WHERE external_id IS NOT NULL');
            q('INSERT INTO settings (k, v) VALUES (?, ?) ON DUPLICATE KEY UPDATE v = VALUES(v)', ['last_sync', date('c') . " (manual: $count listings)"]);
            audit('properties.sync', "$count listings from " . setting('sync_source'));
        }
        json_out($r);
    }
    $stats = [
        'synced' => (int)val('SELECT COUNT(*) FROM properties WHERE external_id IS NOT NULL'),
        'manual' => (int)val('SELECT COUNT(*) FROM properties WHERE external_id IS NULL'),
    ];
    render('admin/sync', ['title' => 'Sync listings', 'stats' => $stats, 'source' => setting('sync_source'), 'last' => setting('last_sync')]);
}
