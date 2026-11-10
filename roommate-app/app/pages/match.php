<?php

function match_deck(array $me, int $limit = 20): array
{
    $myId = (int)$me['id'];
    $exclude = array_unique(array_merge([$myId], blocked_ids($myId), friend_ids($myId),
        array_map('intval', array_column(all('SELECT target_id FROM swipes WHERE user_id = ?', [$myId]), 'target_id'))));
    $rows = all("SELECT * FROM users WHERE status = 'active' AND profile_visible = 1 AND id NOT IN (" . implode(',', $exclude) . ") ORDER BY last_seen DESC LIMIT 400");
    $shared = shared_property_counts($myId);
    $out = [];
    foreach ($rows as $u) {
        $m = match_score($me, $u, $shared[(int)$u['id']] ?? 0);
        $props = array_column(all("SELECT p.name FROM properties p JOIN user_properties up ON up.property_id = p.id WHERE up.user_id = ? AND p.status = 'approved' LIMIT 3", [$u['id']]), 'name');
        $out[] = [
            'id' => (int)$u['id'], 'name' => $u['name'], 'username' => $u['username'], 'age' => age_of($u),
            'avatar' => avatar_url($u), 'initials' => mb_strtoupper(mb_substr($u['name'], 0, 1)), 'hue' => crc32($u['name']) % 360,
            'city' => (string)$u['city'], 'occupation' => (string)$u['occupation'], 'bio' => mb_strimwidth((string)$u['bio'], 0, 220, '…'),
            'looking_for' => label('looking_for', $u['looking_for']), 'budget' => budget_label($u),
            'move_in' => $u['move_in_date'] ? date('M j', strtotime($u['move_in_date'])) : '',
            'chips' => [label('cleanliness', $u['cleanliness']), label('sleep_schedule', $u['sleep_schedule']), label('smoking', $u['smoking']), label('pets', $u['pets'])],
            'type' => $u['quiz_type'] ? (QUIZ_TYPES[$u['quiz_type']]['name'] ?? '') : '',
            'props' => $props, 'score' => $m['score'], 'reasons' => array_slice($m['reasons'], 0, 3),
        ];
    }
    usort($out, fn($a, $b) => $b['score'] <=> $a['score']);
    return array_slice($out, 0, $limit);
}

function match_index(): void
{
    $me = require_login();
    require_once APP_DIR . '/pages/quiz.php';
    $deck = match_deck($me);
    $matches = (int)val("SELECT COUNT(*) FROM swipes s JOIN swipes t ON t.user_id = s.target_id AND t.target_id = s.user_id AND t.liked = 1 WHERE s.user_id = ? AND s.liked = 1", [$me['id']]);
    $likedMe = (int)val("SELECT COUNT(*) FROM swipes s WHERE s.target_id = ? AND s.liked = 1 AND NOT EXISTS (SELECT 1 FROM swipes t WHERE t.user_id = ? AND t.target_id = s.user_id)", [$me['id'], $me['id']]);
    render('match', ['title' => 'Match', 'deck' => $deck, 'matches' => $matches, 'likedMe' => $likedMe, 'bodyClass' => 'match-page']);
}

function match_swipe(): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $tid = (int)input('target');
    $liked = input('liked') === '1' ? 1 : 0;
    if (input('undo') === '1') {
        q('DELETE FROM swipes WHERE user_id = ? AND target_id = ?', [$myId, $tid]);
        json_out(['ok' => true]);
    }
    $t = one("SELECT id, name, username, avatar FROM users WHERE id = ? AND status = 'active'", [$tid]);
    if (!$t || $tid === $myId || is_blocked_between($myId, $tid)) json_out(['error' => 'Member not found'], 404);
    q('INSERT INTO swipes (user_id, target_id, liked) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE liked = VALUES(liked), created_at = NOW()', [$myId, $tid, $liked]);
    $mutual = $liked && val('SELECT 1 FROM swipes WHERE user_id = ? AND target_id = ? AND liked = 1', [$tid, $myId]);
    if ($mutual) {
        $f = one('SELECT * FROM friendships WHERE (requester_id = ? AND addressee_id = ?) OR (requester_id = ? AND addressee_id = ?)', [$myId, $tid, $tid, $myId]);
        if (!$f) q("INSERT INTO friendships (requester_id, addressee_id, status) VALUES (?, ?, 'accepted')", [$tid, $myId]);
        elseif ($f['status'] !== 'accepted') q("UPDATE friendships SET status = 'accepted', updated_at = NOW() WHERE id = ?", [$f['id']]);
        notify($tid, 'match', $myId);
        notify($myId, 'match', $tid);
    }
    json_out(['ok' => true, 'match' => (bool)$mutual, 'user' => $mutual ? ['name' => $t['name'], 'username' => $t['username'], 'avatar' => avatar_url($t)] : null]);
}

function match_list(): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $matches = all("SELECT u.* FROM swipes s JOIN swipes t ON t.user_id = s.target_id AND t.target_id = s.user_id AND t.liked = 1
        JOIN users u ON u.id = s.target_id AND u.status = 'active' WHERE s.user_id = ? AND s.liked = 1 ORDER BY GREATEST(s.created_at, t.created_at) DESC", [$myId]);
    $likedMe = all("SELECT u.* FROM swipes s JOIN users u ON u.id = s.user_id AND u.status = 'active'
        WHERE s.target_id = ? AND s.liked = 1 AND NOT EXISTS (SELECT 1 FROM swipes t WHERE t.user_id = ? AND t.target_id = s.user_id) ORDER BY s.created_at DESC", [$myId, $myId]);
    $shared = shared_property_counts($myId);
    foreach ([&$matches, &$likedMe] as &$list) foreach ($list as &$u) $u['_m'] = match_score($me, $u, $shared[(int)$u['id']] ?? 0);
    unset($list, $u);
    render('matches', ['title' => 'Your matches', 'matches' => $matches, 'likedMe' => $likedMe]);
}
