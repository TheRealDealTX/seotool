<?php

function conversation_list(int $me): array
{
    $blocked = blocked_ids($me);
    $blk = $blocked ? ' AND u.id NOT IN (' . implode(',', $blocked) . ')' : '';
    return all("SELECT c.id, c.last_message_at, u.id AS uid, u.name, u.username, u.avatar, u.last_seen,
            (SELECT CASE WHEN m.deleted_at IS NOT NULL THEN '🚫 Message unsent' WHEN m.body = '' AND m.gif_url IS NOT NULL THEN 'GIF' ELSE m.body END FROM messages m WHERE m.conversation_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_body,
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
        $msgs = load_messages($cid, (int)$me['id'], '1', [], 100, true);
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
        $gif = clean_gif_url((string)($_POST['gif'] ?? ''));
        if ($body === '' && !$gif) json_out(['error' => 'Message is empty'], 422);
        $recent = (int)val('SELECT COUNT(*) FROM messages WHERE sender_id = ? AND created_at > (NOW() - INTERVAL 1 MINUTE)', [$myId]);
        if ($recent >= 30) json_out(['error' => 'Slow down a little — try again in a minute.'], 429);
        $cid = find_conversation($myId, $oid, true);
        $replyTo = (int)($_POST['reply_to'] ?? 0) ?: null;
        if ($replyTo && !val('SELECT 1 FROM messages WHERE id = ? AND conversation_id = ?', [$replyTo, $cid])) $replyTo = null;
        q('INSERT INTO messages (conversation_id, sender_id, body, gif_url, reply_to, updated_at) VALUES (?, ?, ?, ?, ?, NOW(6))', [$cid, $myId, $body, $gif, $replyTo]);
        $mid = (int)db()->lastInsertId();
        q('UPDATE users SET typing_at = NULL WHERE id = ?', [$myId]);
        q('UPDATE conversations SET last_message_at = NOW() WHERE id = ?', [$cid]);
        if (!val("SELECT 1 FROM notifications WHERE user_id = ? AND actor_id = ? AND type = 'message' AND is_read = 0", [$oid, $myId])) {
            notify($oid, 'message', $myId, $cid);
        }
        json_out(['message' => load_messages($cid, $myId, 'm.id = ?', [$mid])[0] ?? null]);
    }

    $cid = find_conversation($myId, $oid);
    $after = (int)($_GET['after'] ?? 0);
    $since = (string)($_GET['since'] ?? '');
    $now = (string)val('SELECT NOW(6)');
    $out = $updated = [];
    $lastRead = 0;
    if ($cid) {
        $out = load_messages($cid, $myId, 'm.id > ?', [$after], 200);
        if ($since !== '' && preg_match('/^[\d\- :.]+$/', $since)) {
            $updated = load_messages($cid, $myId, 'm.id <= ? AND m.updated_at > ?', [$after, $since], 200);
        }
        q('UPDATE messages SET read_at = NOW() WHERE conversation_id = ? AND sender_id <> ? AND read_at IS NULL', [$cid, $myId]);
        $lastRead = (int)val('SELECT MAX(id) FROM messages WHERE conversation_id = ? AND sender_id = ? AND read_at IS NOT NULL', [$cid, $myId]);
    }
    $typing = (bool)val('SELECT 1 FROM users WHERE id = ? AND typing_to = ? AND typing_at > (NOW() - INTERVAL 6 SECOND)', [$oid, $myId]);
    json_out(['messages' => $out, 'updated' => $updated, 'now' => $now, 'last_read' => $lastRead, 'typing' => $typing, 'counts' => unread_counts($myId)]);
}

/** Edit, unsend or react to a single message. */
function messages_action(string $id): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $m = one('SELECT m.*, c.user_a, c.user_b FROM messages m JOIN conversations c ON c.id = m.conversation_id WHERE m.id = ?', [(int)$id]);
    if (!$m || ((int)$m['user_a'] !== $myId && (int)$m['user_b'] !== $myId)) json_out(['error' => 'Message not found'], 404);
    $mine = (int)$m['sender_id'] === $myId;
    $act = input('action');
    if ($act === 'edit') {
        if (!$mine || $m['deleted_at']) json_out(['error' => 'You can only edit your own messages.'], 403);
        if (strtotime($m['created_at']) < time() - 86400) json_out(['error' => 'Messages can be edited for 24 hours.'], 403);
        $body = mb_substr(trim((string)($_POST['body'] ?? '')), 0, 4000);
        if ($body === '') json_out(['error' => 'Message can’t be empty — unsend it instead.'], 422);
        if ($body !== $m['body']) q('UPDATE messages SET body = ?, edited_at = NOW(), updated_at = NOW(6) WHERE id = ?', [$body, $m['id']]);
    } elseif ($act === 'unsend') {
        if (!$mine) json_out(['error' => 'You can only unsend your own messages.'], 403);
        q("UPDATE messages SET body = '', gif_url = NULL, deleted_at = NOW(), updated_at = NOW(6) WHERE id = ?", [$m['id']]);
        q('DELETE FROM message_reactions WHERE message_id = ?', [$m['id']]);
    } elseif ($act === 'react') {
        if ($m['deleted_at']) json_out(['error' => 'Message was unsent.'], 422);
        $emoji = mb_substr((string)input('emoji'), 0, 8);
        $current = val('SELECT emoji FROM message_reactions WHERE message_id = ? AND user_id = ?', [$m['id'], $myId]);
        if ($emoji === '' || $emoji === $current) {
            q('DELETE FROM message_reactions WHERE message_id = ? AND user_id = ?', [$m['id'], $myId]);
        } else {
            q('INSERT INTO message_reactions (message_id, user_id, emoji) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE emoji = VALUES(emoji)', [$m['id'], $myId, $emoji]);
        }
        q('UPDATE messages SET updated_at = NOW(6) WHERE id = ?', [$m['id']]);
    } else {
        json_out(['error' => 'Unknown action'], 400);
    }
    json_out(['message' => load_messages((int)$m['conversation_id'], $myId, 'm.id = ?', [$m['id']])[0]]);
}

function load_messages(int $cid, int $me, string $where, array $params, int $limit = 100, bool $latest = false): array
{
    $order = $latest ? 'DESC' : 'ASC';
    $rows = all("SELECT m.*, r.body AS r_body, r.sender_id AS r_sender, r.deleted_at AS r_deleted, r.gif_url AS r_gif
        FROM messages m LEFT JOIN messages r ON r.id = m.reply_to
        WHERE m.conversation_id = ? AND $where ORDER BY m.id $order LIMIT $limit", array_merge([$cid], $params));
    if ($latest) $rows = array_reverse($rows);
    $reacts = [];
    if ($rows) {
        $ids = implode(',', array_map(fn($r) => (int)$r['id'], $rows));
        foreach (all("SELECT message_id, user_id, emoji FROM message_reactions WHERE message_id IN ($ids)") as $x) {
            $reacts[$x['message_id']][] = $x;
        }
    }
    return array_map(fn($m) => format_msg($m, $me, $reacts[$m['id']] ?? []), $rows);
}

function format_msg(array $m, int $me, array $reactions = []): array
{
    $agg = [];
    foreach ($reactions as $r) {
        $agg[$r['emoji']] ??= ['emoji' => $r['emoji'], 'count' => 0, 'mine' => false];
        $agg[$r['emoji']]['count']++;
        if ((int)$r['user_id'] === $me) $agg[$r['emoji']]['mine'] = true;
    }
    $reply = null;
    if (!empty($m['reply_to'])) {
        $reply = ['id' => (int)$m['reply_to'], 'mine' => (int)$m['r_sender'] === $me,
            'body' => $m['r_deleted'] ? 'Message unsent' : ($m['r_body'] !== '' && $m['r_body'] !== null ? mb_strimwidth($m['r_body'], 0, 120, '…') : ($m['r_gif'] ? 'GIF' : ''))];
    }
    return [
        'id' => (int)$m['id'],
        'mine' => (int)$m['sender_id'] === $me,
        'body' => $m['deleted_at'] ? '' : $m['body'],
        'gif' => $m['deleted_at'] ? null : ($m['gif_url'] ?? null),
        'deleted' => (bool)$m['deleted_at'],
        'edited' => (bool)($m['edited_at'] ?? null),
        'can_edit' => (int)$m['sender_id'] === $me && !$m['deleted_at'] && strtotime($m['created_at']) > time() - 86400,
        'reply' => $reply,
        'reactions' => array_values($agg),
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
