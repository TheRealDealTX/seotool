<?php

function properties_index(): void
{
    $me = require_login();
    $qstr = mb_substr(input('q'), 0, 80);
    $city = mb_substr(input('city'), 0, 60);
    $sort = in_array(input('sort'), ['popular', 'name', 'newest', 'rent'], true) ? input('sort') : 'popular';
    $mineOnly = input('mine') === '1';
    $where = ["p.status = 'approved'"];
    $params = [];
    if ($qstr !== '') { $where[] = '(p.name LIKE ? OR p.address LIKE ? OR p.zip LIKE ?)'; $l = "%$qstr%"; array_push($params, $l, $l, $l); }
    if ($city !== '') { $where[] = 'p.city = ?'; $params[] = $city; }
    if ($mineOnly) { $where[] = 'p.id IN (SELECT property_id FROM user_properties WHERE user_id = ?)'; $params[] = $me['id']; }
    $order = match ($sort) {
        'name' => 'p.name ASC',
        'newest' => 'p.id DESC',
        'rent' => 'p.rent_min IS NULL, p.rent_min ASC',
        default => 'p.is_featured DESC, interested DESC, p.name ASC',
    };
    $total = (int)val('SELECT COUNT(*) FROM properties p WHERE ' . implode(' AND ', $where), $params);
    [$page, $pages, $offset] = paginate($total, 24);
    $props = all("SELECT p.*, (SELECT COUNT(*) FROM user_properties up JOIN users u ON u.id = up.user_id AND u.status = 'active' WHERE up.property_id = p.id) AS interested
        FROM properties p WHERE " . implode(' AND ', $where) . " ORDER BY $order LIMIT 24 OFFSET $offset", $params);
    $cities = array_column(all("SELECT DISTINCT city FROM properties WHERE status = 'approved' AND city IS NOT NULL AND city <> '' ORDER BY city"), 'city');
    $interestedIn = array_map('intval', array_column(all('SELECT property_id FROM user_properties WHERE user_id = ?', [$me['id']]), 'property_id'));
    render('properties', compact('props', 'cities', 'interestedIn', 'qstr', 'city', 'sort', 'mineOnly', 'page', 'pages', 'total') + ['title' => 'Apartment properties', 'mainClass' => 'main-wide']);
}

function properties_show(string $slug): void
{
    $me = require_login();
    $p = one('SELECT * FROM properties WHERE slug = ?', [$slug]);
    if (!$p || ($p['status'] !== 'approved' && !is_admin() && (int)$p['created_by'] !== (int)$me['id'])) not_found();
    $myId = (int)$me['id'];
    $blocked = blocked_ids($myId);
    $blk = $blocked ? ' AND u.id NOT IN (' . implode(',', $blocked) . ')' : '';
    $renters = all("SELECT u.* FROM users u JOIN user_properties up ON up.user_id = u.id
        WHERE up.property_id = ? AND u.status = 'active' AND u.profile_visible = 1 AND u.id <> ? $blk", [$p['id'], $myId]);
    $shared = shared_property_counts($myId);
    $list = [];
    foreach ($renters as $u) $list[] = ['u' => $u, 'm' => match_score($me, $u, max(1, $shared[(int)$u['id']] ?? 0))];
    usort($list, fn($a, $b) => $b['m']['score'] <=> $a['m']['score']);
    $interested = (bool)val('SELECT 1 FROM user_properties WHERE user_id = ? AND property_id = ?', [$myId, $p['id']]);
    $count = (int)val("SELECT COUNT(*) FROM user_properties up JOIN users u ON u.id = up.user_id AND u.status = 'active' WHERE up.property_id = ?", [$p['id']]);
    require_once APP_DIR . '/pages/feed.php';
    $posts = load_posts('p.property_id = ?', [(int)$p['id']], 10);
    render('property', ['title' => $p['name'], 'p' => $p, 'list' => $list, 'interested' => $interested, 'count' => $count, 'posts' => $posts, 'mainClass' => 'main-wide']);
}

function properties_toggle(string $id): void
{
    $me = require_login();
    $p = one("SELECT * FROM properties WHERE id = ? AND status = 'approved'", [(int)$id]);
    if (!$p) is_ajax() ? json_out(['error' => 'Property not found'], 404) : not_found();
    if (val('SELECT 1 FROM user_properties WHERE user_id = ? AND property_id = ?', [$me['id'], $p['id']])) {
        q('DELETE FROM user_properties WHERE user_id = ? AND property_id = ?', [$me['id'], $p['id']]);
        $on = false;
    } else {
        if ((int)val('SELECT COUNT(*) FROM user_properties WHERE user_id = ?', [$me['id']]) >= 25) {
            is_ajax() ? json_out(['error' => 'You can follow up to 25 properties.'], 422) : flash('error', 'You can follow up to 25 properties.');
            back();
        }
        q('INSERT IGNORE INTO user_properties (user_id, property_id) VALUES (?, ?)', [$me['id'], $p['id']]);
        $on = true;
    }
    $count = (int)val("SELECT COUNT(*) FROM user_properties up JOIN users u ON u.id = up.user_id AND u.status = 'active' WHERE up.property_id = ?", [$p['id']]);
    if (is_ajax()) json_out(['on' => $on, 'count' => $count]);
    flash('success', $on ? "Added {$p['name']} to your properties. Here are renters interested in it." : "Removed {$p['name']} from your properties.");
    $on ? redirect('/properties/' . $p['slug']) : back();
}

function properties_new(): void
{
    $me = require_login();
    if (setting('allow_property_submissions', '1') !== '1' && !is_admin()) {
        render('error', ['title' => 'Submissions closed', 'message' => 'Adding properties is currently turned off. Contact us to suggest one.']);
        return;
    }
    $errors = [];
    $d = ['name' => '', 'address' => '', 'city' => '', 'state' => 'TX', 'zip' => '', 'website' => '', 'description' => '', 'rent_min' => '', 'rent_max' => ''];
    if (is_post()) {
        foreach ($d as $k => $_) $d[$k] = mb_substr(input($k), 0, $k === 'description' ? 2000 : 200);
        if (mb_strlen($d['name']) < 3) $errors[] = 'Enter the property name.';
        if ($d['city'] === '') $errors[] = 'Enter the city.';
        if ($d['website'] && !preg_match('~^https?://~i', $d['website'])) $d['website'] = 'https://' . $d['website'];
        if ($d['website'] && !filter_var($d['website'], FILTER_VALIDATE_URL)) $errors[] = 'Website URL looks invalid.';
        $dupe = one('SELECT slug, status FROM properties WHERE name = ? AND city = ?', [$d['name'], $d['city']]);
        if ($dupe) $errors[] = 'That property is already listed' . ($dupe['status'] === 'pending' ? ' and waiting for approval.' : '.');
        $pending = (int)val("SELECT COUNT(*) FROM properties WHERE created_by = ? AND status = 'pending'", [$me['id']]);
        if ($pending >= 5 && !is_admin()) $errors[] = 'You have several properties awaiting review already.';
        if (!$errors) {
            $status = (setting('require_property_approval', '1') === '1' && !is_admin()) ? 'pending' : 'approved';
            q('INSERT INTO properties (name, slug, address, city, state, zip, website, description, rent_min, rent_max, status, created_by) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', [
                $d['name'], unique_slug($d['name']), $d['address'] ?: null, $d['city'], $d['state'] ?: null, $d['zip'] ?: null,
                $d['website'] ?: null, $d['description'] ?: null, (int)$d['rent_min'] ?: null, (int)$d['rent_max'] ?: null, $status, $me['id'],
            ]);
            $pid = (int)db()->lastInsertId();
            if ($status === 'approved') {
                q('INSERT IGNORE INTO user_properties (user_id, property_id) VALUES (?, ?)', [$me['id'], $pid]);
                flash('success', 'Property added and saved to your list.');
                redirect('/properties/' . val('SELECT slug FROM properties WHERE id = ?', [$pid]));
            }
            try { email_admins('Property awaiting approval: ' . $d['name'], "@{$me['username']} submitted {$d['name']} ({$d['city']}).\n\nReview: " . base_url() . '/admin/properties?status=pending'); } catch (Throwable $e) {}
            flash('success', 'Thanks! The property will appear once our team reviews it (usually within a day).');
            redirect('/properties');
        }
    }
    render('property_new', ['title' => 'Add a property', 'd' => $d, 'errors' => $errors]);
}

function properties_search(): void
{
    require_login();
    $qs = mb_substr(input('q'), 0, 80);
    if (mb_strlen($qs) < 2) json_out(['results' => []]);
    $l = '%' . $qs . '%';
    $rows = all("SELECT id, name, city FROM properties WHERE status = 'approved' AND (name LIKE ? OR city LIKE ? OR address LIKE ? OR zip LIKE ?)
        ORDER BY (name LIKE ?) DESC, name LIMIT 20", [$l, $l, $l, $l, $qs . '%']);
    json_out(['results' => array_map(fn($r) => ['id' => (int)$r['id'], 'name' => $r['name'], 'city' => (string)$r['city']], $rows)]);
}

function properties_lounge(string $id): void
{
    $me = require_login();
    $p = one("SELECT id, name FROM properties WHERE id = ? AND status = 'approved'", [(int)$id]);
    if (!$p) json_out(['error' => 'Property not found'], 404);
    $member = (bool)val('SELECT 1 FROM user_properties WHERE user_id = ? AND property_id = ?', [$me['id'], $p['id']]);
    if (is_post()) {
        if (!$member) json_out(['error' => 'Mark yourself as interested in this property to join the lounge.'], 403);
        $body = mb_substr(trim((string)($_POST['body'] ?? '')), 0, 1000);
        if ($body === '') json_out(['error' => 'Message is empty'], 422);
        if ((int)val('SELECT COUNT(*) FROM property_messages WHERE user_id = ? AND created_at > (NOW() - INTERVAL 1 MINUTE)', [$me['id']]) >= 10) {
            json_out(['error' => 'Slow down a little.'], 429);
        }
        q('INSERT INTO property_messages (property_id, user_id, body) VALUES (?, ?, ?)', [$p['id'], $me['id'], $body]);
    }
    $after = (int)($_GET['after'] ?? 0);
    $blocked = blocked_ids((int)$me['id']);
    $blk = $blocked ? ' AND m.user_id NOT IN (' . implode(',', $blocked) . ')' : '';
    $rows = $after
        ? all("SELECT m.*, u.name, u.username, u.avatar FROM property_messages m JOIN users u ON u.id = m.user_id AND u.status = 'active' WHERE m.property_id = ? AND m.id > ? $blk ORDER BY m.id ASC LIMIT 100", [$p['id'], $after])
        : array_reverse(all("SELECT m.*, u.name, u.username, u.avatar FROM property_messages m JOIN users u ON u.id = m.user_id AND u.status = 'active' WHERE m.property_id = ? $blk ORDER BY m.id DESC LIMIT 60", [$p['id']]));
    $online = (int)val("SELECT COUNT(*) FROM user_properties up JOIN users u ON u.id = up.user_id WHERE up.property_id = ? AND u.last_seen > (NOW() - INTERVAL 5 MINUTE)", [$p['id']]);
    json_out(['member' => $member, 'online' => $online, 'messages' => array_map(fn($m) => [
        'id' => (int)$m['id'], 'mine' => (int)$m['user_id'] === (int)$me['id'], 'name' => $m['name'], 'username' => $m['username'],
        'avatar' => avatar_url($m), 'initials' => mb_strtoupper(mb_substr($m['name'], 0, 1)), 'hue' => crc32($m['name']) % 360,
        'body' => $m['body'], 'time' => time_ago($m['created_at']),
    ], $rows)]);
}
