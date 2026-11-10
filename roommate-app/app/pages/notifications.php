<?php

function notifications_index(): void
{
    $me = require_login();
    $items = all("SELECT n.*, u.name, u.username, u.avatar FROM notifications n
        LEFT JOIN users u ON u.id = n.actor_id
        WHERE n.user_id = ? AND (u.id IS NULL OR u.status = 'active') ORDER BY n.id DESC LIMIT 60", [$me['id']]);
    q('UPDATE notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0', [$me['id']]);
    q('DELETE FROM notifications WHERE user_id = ? AND created_at < (NOW() - INTERVAL 90 DAY)', [$me['id']]);
    render('notifications', ['title' => 'Notifications', 'items' => $items]);
}

function notification_text(array $n): array
{
    // [text, link]
    $who = '<strong>' . e($n['name'] ?? 'Someone') . '</strong>';
    return match ($n['type']) {
        'friend_request' => ["$who sent you a friend request.", '/friends?tab=requests'],
        'friend_accept' => ["$who accepted your friend request.", '/u/' . ($n['username'] ?? '')],
        'message' => ["$who sent you a message.", '/messages/' . ($n['username'] ?? '')],
        'like' => ["$who liked your post.", '/post/' . (int)$n['entity_id']],
        'comment' => ["$who commented on your post.", '/post/' . (int)$n['entity_id']],
        'property_approved' => ['A property you submitted was approved.', '/properties'],
        default => ['You have a new notification.', '/home'],
    };
}
