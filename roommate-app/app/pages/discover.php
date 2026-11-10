<?php

function discover_index(): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $f = [
        'q' => mb_substr(input('q'), 0, 60),
        'property' => (int)input('property'),
        'city' => mb_substr(input('city'), 0, 60),
        'looking_for' => in_array(input('looking_for'), ['need_place', 'have_place', 'either'], true) ? input('looking_for') : '',
        'budget' => (int)input('budget'),
        'gender' => in_array(input('gender'), ['male', 'female', 'nonbinary'], true) ? input('gender') : '',
        'pets' => input('pets') === 'ok' ? 'ok' : '',
        'nonsmoker' => input('nonsmoker') === '1' ? '1' : '',
        'sort' => in_array(input('sort'), ['match', 'newest', 'active'], true) ? input('sort') : 'match',
    ];

    $where = ["u.status = 'active'", 'u.profile_visible = 1', 'u.id <> ?'];
    $params = [$myId];
    $blocked = blocked_ids($myId);
    if ($blocked) $where[] = 'u.id NOT IN (' . implode(',', $blocked) . ')';
    if ($f['q'] !== '') {
        $where[] = '(u.name LIKE ? OR u.username LIKE ? OR u.occupation LIKE ? OR u.interests LIKE ?)';
        $like = '%' . $f['q'] . '%';
        array_push($params, $like, $like, $like, $like);
    }
    if ($f['property']) {
        $where[] = 'u.id IN (SELECT user_id FROM user_properties WHERE property_id = ?)';
        $params[] = $f['property'];
    }
    if ($f['city'] !== '') { $where[] = 'u.city LIKE ?'; $params[] = '%' . $f['city'] . '%'; }
    if ($f['looking_for']) { $where[] = 'u.looking_for = ?'; $params[] = $f['looking_for']; }
    if ($f['budget']) { $where[] = '(u.budget_min IS NULL OR u.budget_min <= ?)'; $params[] = $f['budget']; }
    if ($f['gender']) { $where[] = 'u.gender = ?'; $params[] = $f['gender']; }
    if ($f['pets']) { $where[] = "u.pets IN ('none','ok')"; }
    if ($f['nonsmoker']) { $where[] = "u.smoking = 'no'"; }

    $order = match ($f['sort']) {
        'newest' => 'u.id DESC',
        default => 'u.last_seen DESC',
    };
    $rows = all('SELECT u.* FROM users u WHERE ' . implode(' AND ', $where) . " ORDER BY $order LIMIT 500", $params);

    $shared = shared_property_counts($myId);
    $results = [];
    foreach ($rows as $u) {
        $results[] = ['u' => $u, 'm' => match_score($me, $u, $shared[(int)$u['id']] ?? 0)];
    }
    if ($f['sort'] === 'match') {
        usort($results, fn($a, $b) => $b['m']['score'] <=> $a['m']['score']);
    }
    $total = count($results);
    [$page, $pages, $offset] = paginate($total, 24);
    $results = array_slice($results, $offset, 24);

    $properties = all("SELECT p.id, p.name FROM properties p WHERE p.status = 'approved'
        AND (p.id IN (SELECT DISTINCT property_id FROM user_properties) OR p.id = ?) ORDER BY p.name", [$f['property']]);
    $hasProps = (bool)val('SELECT 1 FROM user_properties WHERE user_id = ? LIMIT 1', [$myId]);

    render('discover', compact('f', 'results', 'total', 'page', 'pages', 'properties', 'hasProps') + ['title' => 'Discover roommates', 'mainClass' => 'main-wide']);
}
