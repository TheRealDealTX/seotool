<?php

function conversation_list(int $me): array
{
    $blocked = blocked_ids($me);
    $blk = $blocked ? ' AND u.id NOT IN (' . implode(',', $blocked) . ')' : '';
    return all("SELECT c.id, c.last_message_at, u.id AS uid, u.name, u.username, u.avatar, u.last_seen,
            (SELECT body FROM messages m WHERE m.conversation_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_body,
            (SELECT sender_id FROM messages m WHERE m.conversation_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_sender,
            (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.id AND m.sender_id <> ? AND m.read_at IS NULL) AS unread
        FROM conversations c
        JOIN users u ON u.id = IF(c.user_a = ?, c.user_b, c.user_a)
        WHERE (c.user_a = ? OR c.user_b = ?) AND u.status = 'active' $blk
          AND EXISTS (SELECT 1 FROM messages m WHERE m.conversation_id = c.id)
        ORDER BY c.last_message_at DESC LIMIT 100", [$me, $me, $me, $me]);
}

function find_conversation(int $a, int $b, bool $create = false): ?int
{
    [$x, $y] = $a < $b ? [$a, $b] : [$b, $a];
    $id = val('SELECT id FROM conversations WHERE user_a = ? AND user_b = ?', [$x, $y]);
    if (!$id && $create) {
        q('INSERT IGNORE INTO conversations (user_a, user_b) VALUES (?, ?)', [$x, $y]);
        $id = val('SELECT id FROM conversations WHERE user_a = ? AND user_b = ?', [$x, $y]);
    }
    return $id ? (int)$id : null;
}

function messages_index(): void
{
    $me = require_login();
    render('messages', ['title' => 'Messages', 'convos' => conversation_list((int)$me['id']), 'other' => null, 'mainClass' => 'main-wide main-chat', 'bodyClass' => 'chat-page']);
}

function messages_thread(string $username): void
{
    $me = require_login();
    $other = one("SELECT * FROM users WHERE username = ? AND status = 'active'", [strtolower($username)]);
    if (!$other || (int)$other['id'] === (int)$me['id']) not_found();
    if (is_blocked_between((int)$me['id'], (int)$other['id'])) {
        flash('error', 'You can’t message this member.');
        redirect('/messages');
    }
    $cid = find_conversation((int)$me['id'], (int)$other['id']);
    $msgs = [];
    if ($cid) {
        $msgs = array_reverse(all('SELECT id, sender_id, body, created_at, read_at FROM messages WHERE conversation_id = ? ORDER BY id DESC LIMIT 100', [$cid]));
        q('UPDATE messages SET read_at = NOW() WHERE conversation_id = ? AND sender_id <> ? AND read_at IS NULL', [$cid, $me['id']]);
        q("UPDATE notifications SET is_read = 1 WHERE user_id = ? AND actor_id = ? AND type = 'message'", [$me['id'], $other['id']]);
    }
    render('messages', [
        'title' => 'Chat with ' . $other['name'], 'convos' => conversation_list((int)$me['id']), 'other' => $other, 'msgs' => $msgs,
        'canMessage' => can_message((int)$me['id'], (int)$other['id']), 'fstatus' => friend_status((int)$me['id'], (int)$other['id']),
        'mainClass' => 'main-wide main-chat', 'bodyClass' => 'chat-page chat-open',
    ]);
}

function messages_api(string $otherId): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $other = one("SELECT id, name FROM users WHERE id = ? AND status = 'active'", [(int)$otherId]);
    if (!$other) json_out(['error' => 'Member not found'], 404);
    $oid = (int)$other['id'];

    if (is_post()) {
        if (!can_message($myId, $oid)) {
            json_out(['error' => setting('messaging_friends_only') === '1' ? 'You can only message friends.' : 'You can’t message this member.'], 403);
        }
        $body = mb_substr(trim((string)($_POST['body'] ?? '')), 0, 4000);
        if ($body === '') json_out(['error' => 'Message is empty'], 422);
        $recent = (int)val('SELECT COUNT(*) FROM messages WHERE sender_id = ? AND created_at > (NOW() - INTERVAL 1 MINUTE)', [$myId]);
        if ($recent >= 30) json_out(['error' => 'Slow down a little — try again in a minute.'], 429);
        $cid = find_conversation($myId, $oid, true);
        q('INSERT INTO messages (conversation_id, sender_id, body) VALUES (?, ?, ?)', [$cid, $myId, $body]);
        $mid = (int)db()->lastInsertId();
        q('UPDATE conversations SET last_message_at = NOW() WHERE id = ?', [$cid]);
        // One unread "message" notification per sender at a time.
        if (!val("SELECT 1 FROM notifications WHERE user_id = ? AND actor_id = ? AND type = 'message' AND is_read = 0", [$oid, $myId])) {
            notify($oid, 'message', $myId, $cid);
        }
        $m = one('SELECT id, sender_id, body, created_at, read_at FROM messages WHERE id = ?', [$mid]);
        json_out(['message' => format_msg($m, $myId)]);
    }

    $cid = find_conversation($myId, $oid);
    $after = (int)($_GET['after'] ?? 0);
    $out = [];
    $lastRead = 0;
    if ($cid) {
        foreach (all('SELECT id, sender_id, body, created_at, read_at FROM messages WHERE conversation_id = ? AND id > ? ORDER BY id ASC LIMIT 200', [$cid, $after]) as $m) {
            $out[] = format_msg($m, $myId);
        }
        q('UPDATE messages SET read_at = NOW() WHERE conversation_id = ? AND sender_id <> ? AND read_at IS NULL', [$cid, $myId]);
        $lastRead = (int)val('SELECT MAX(id) FROM messages WHERE conversation_id = ? AND sender_id = ? AND read_at IS NOT NULL', [$cid, $myId]);
    }
    json_out(['messages' => $out, 'last_read' => $lastRead, 'counts' => unread_counts($myId)]);
}

function format_msg(array $m, int $me): array
{
    return [
        'id' => (int)$m['id'],
        'mine' => (int)$m['sender_id'] === $me,
        'body' => $m['body'],
        'time' => date('g:i A', strtotime($m['created_at'])),
        'date' => date('M j, Y', strtotime($m['created_at'])),
        'read' => $m['read_at'] !== null,
    ];
}

function messages_counts(): void
{
    $me = require_login();
    json_out(unread_counts((int)$me['id']));
}
