<?php

function friends_index(): void
{
    $me = require_login();
    $id = (int)$me['id'];
    $friends = all("SELECT u.*, f.updated_at AS since FROM friendships f
        JOIN users u ON u.id = IF(f.requester_id = ?, f.addressee_id, f.requester_id)
        WHERE f.status = 'accepted' AND (f.requester_id = ? OR f.addressee_id = ?) AND u.status = 'active'
        ORDER BY u.name", [$id, $id, $id]);
    $incoming = all("SELECT u.*, f.created_at AS requested_at FROM friendships f JOIN users u ON u.id = f.requester_id
        WHERE f.addressee_id = ? AND f.status = 'pending' AND u.status = 'active' ORDER BY f.id DESC", [$id]);
    $outgoing = all("SELECT u.*, f.created_at AS requested_at FROM friendships f JOIN users u ON u.id = f.addressee_id
        WHERE f.requester_id = ? AND f.status = 'pending' AND u.status = 'active' ORDER BY f.id DESC", [$id]);
    $shared = shared_property_counts($id);
    foreach ([&$friends, &$incoming] as &$list) {
        foreach ($list as &$u) $u['_match'] = match_score($me, $u, $shared[(int)$u['id']] ?? 0);
    }
    unset($list, $u);
    $tab = in_array($_GET['tab'] ?? '', ['requests', 'sent'], true) ? $_GET['tab'] : ($incoming && !$friends ? 'requests' : 'all');
    render('friends', compact('friends', 'incoming', 'outgoing', 'tab') + ['title' => 'Friends']);
}

function friends_action(string $otherId, string $action): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $other = one("SELECT * FROM users WHERE id = ? AND status = 'active'", [(int)$otherId]);
    if (!$other || (int)$other['id'] === $myId) not_found();
    $oid = (int)$other['id'];
    $status = friend_status($myId, $oid);
    $msg = null;

    switch ($action) {
        case 'add':
            if (is_blocked_between($myId, $oid)) { flash('error', 'You can’t add this member.'); break; }
            if ($status === 'received') {
                q("UPDATE friendships SET status = 'accepted', updated_at = NOW() WHERE requester_id = ? AND addressee_id = ?", [$oid, $myId]);
                notify($oid, 'friend_accept', $myId);
                $msg = "You and {$other['name']} are now friends.";
            } elseif ($status === 'none') {
                $today = (int)val('SELECT COUNT(*) FROM friendships WHERE requester_id = ? AND created_at > (NOW() - INTERVAL 1 DAY)', [$myId]);
                if ($today >= 50) { flash('error', 'You’ve sent a lot of requests today. Try again tomorrow.'); break; }
                q('INSERT INTO friendships (requester_id, addressee_id) VALUES (?, ?)', [$myId, $oid]);
                notify($oid, 'friend_request', $myId);
                $msg = 'Friend request sent.';
            }
            break;
        case 'accept':
            if ($status === 'received') {
                q("UPDATE friendships SET status = 'accepted', updated_at = NOW() WHERE requester_id = ? AND addressee_id = ?", [$oid, $myId]);
                notify($oid, 'friend_accept', $myId);
                q("UPDATE notifications SET is_read = 1 WHERE user_id = ? AND actor_id = ? AND type = 'friend_request'", [$myId, $oid]);
                $msg = "You and {$other['name']} are now friends.";
            }
            break;
        case 'decline':
            q("DELETE FROM friendships WHERE requester_id = ? AND addressee_id = ? AND status = 'pending'", [$oid, $myId]);
            q("UPDATE notifications SET is_read = 1 WHERE user_id = ? AND actor_id = ? AND type = 'friend_request'", [$myId, $oid]);
            $msg = 'Request declined.';
            break;
        case 'cancel':
            q("DELETE FROM friendships WHERE requester_id = ? AND addressee_id = ? AND status = 'pending'", [$myId, $oid]);
            q("DELETE FROM notifications WHERE user_id = ? AND actor_id = ? AND type = 'friend_request'", [$oid, $myId]);
            $msg = 'Request cancelled.';
            break;
        case 'remove':
            q('DELETE FROM friendships WHERE (requester_id = ? AND addressee_id = ?) OR (requester_id = ? AND addressee_id = ?)', [$myId, $oid, $oid, $myId]);
            $msg = "Removed {$other['name']} from your friends.";
            break;
    }
    if (is_ajax()) json_out(['ok' => true, 'status' => friend_status($myId, $oid), 'message' => $msg]);
    if ($msg) flash('success', $msg);
    back('/u/' . $other['username']);
}

function friends_block(string $otherId): void
{
    $me = require_login();
    $oid = (int)$otherId;
    if ($oid === (int)$me['id'] || !val('SELECT 1 FROM users WHERE id = ?', [$oid])) not_found();
    q('INSERT IGNORE INTO blocks (blocker_id, blocked_id) VALUES (?, ?)', [$me['id'], $oid]);
    q('DELETE FROM friendships WHERE (requester_id = ? AND addressee_id = ?) OR (requester_id = ? AND addressee_id = ?)', [$me['id'], $oid, $oid, $me['id']]);
    flash('success', 'Member blocked. They can no longer see your profile or message you.');
    redirect('/home');
}

function friends_unblock(string $otherId): void
{
    $me = require_login();
    q('DELETE FROM blocks WHERE blocker_id = ? AND blocked_id = ?', [$me['id'], (int)$otherId]);
    flash('success', 'Member unblocked.');
    back('/settings');
}
