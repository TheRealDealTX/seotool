<?php

function load_posts(string $where, array $params, int $limit = 20, int $offset = 0, int $commentsPer = 3): array
{
    $me = uid();
    $blocked = blocked_ids($me);
    if ($blocked) {
        $where .= ' AND p.user_id NOT IN (' . implode(',', $blocked) . ')';
    }
    $posts = all("SELECT p.*, u.name, u.username, u.avatar, pr.name AS property_name, pr.slug AS property_slug,
            (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.id) AS likes,
            (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) AS comments,
            (SELECT l.reaction FROM post_likes l WHERE l.post_id = p.id AND l.user_id = ?) AS my_reaction
        FROM posts p
        JOIN users u ON u.id = p.user_id AND u.status = 'active'
        LEFT JOIN properties pr ON pr.id = p.property_id
        WHERE p.status = 'visible' AND $where
        ORDER BY p.id DESC LIMIT $limit OFFSET $offset", array_merge([$me], $params));
    if ($posts) {
        $ids = implode(',', array_map(fn($p) => (int)$p['id'], $posts));
        $blk = $blocked ? ' AND c.user_id NOT IN (' . implode(',', $blocked) . ')' : '';
        $rows = all("SELECT c.*, u.name, u.username, u.avatar FROM comments c JOIN users u ON u.id = c.user_id AND u.status = 'active'
            WHERE c.post_id IN ($ids) $blk ORDER BY c.id ASC");
        $byPost = [];
        foreach ($rows as $c) $byPost[$c['post_id']][] = $c;
        $top = [];
        foreach (all("SELECT post_id, reaction, COUNT(*) n FROM post_likes WHERE post_id IN ($ids) GROUP BY post_id, reaction ORDER BY n DESC") as $r) {
            $top[$r['post_id']][] = $r['reaction'];
        }
        foreach ($posts as &$p) {
            $p['top_reactions'] = array_slice($top[$p['id']] ?? [], 0, 3);
            $list = $byPost[$p['id']] ?? [];
            $p['comment_list'] = $commentsPer ? array_slice($list, -$commentsPer) : $list;
        }
    }
    return $posts;
}

function feed_home(): void
{
    $me = require_login();
    $tab = in_array($_GET['tab'] ?? '', ['friends', 'properties'], true) ? $_GET['tab'] : 'all';
    $where = '1';
    $params = [];
    if ($tab === 'friends') {
        $ids = friend_ids((int)$me['id']);
        $ids[] = (int)$me['id'];
        $where = 'p.user_id IN (' . implode(',', $ids) . ')';
    } elseif ($tab === 'properties') {
        $where = 'p.property_id IN (SELECT property_id FROM user_properties WHERE user_id = ?)';
        $params[] = $me['id'];
    }
    $page = max(1, (int)($_GET['page'] ?? 1));
    $posts = load_posts($where, $params, 15, ($page - 1) * 15);

    $myProps = all("SELECT p.id, p.name, p.slug FROM properties p JOIN user_properties up ON up.property_id = p.id WHERE up.user_id = ? AND p.status = 'approved' ORDER BY p.name", [$me['id']]);

    // Sidebar: top matches.
    $shared = shared_property_counts((int)$me['id']);
    $blocked = blocked_ids((int)$me['id']);
    $friends = friend_ids((int)$me['id']);
    $exclude = array_merge([(int)$me['id']], $blocked, $friends);
    $cands = all("SELECT * FROM users WHERE status = 'active' AND profile_visible = 1 AND id NOT IN (" . implode(',', $exclude) . ") ORDER BY last_seen DESC LIMIT 200");
    $suggest = [];
    foreach ($cands as $c) {
        $m = match_score($me, $c, $shared[(int)$c['id']] ?? 0);
        $suggest[] = ['u' => $c, 'm' => $m];
    }
    usort($suggest, fn($a, $b) => $b['m']['score'] <=> $a['m']['score']);

    $viewers = all("SELECT u.id, u.name, u.username, u.avatar, v.viewed_at FROM profile_views v JOIN users u ON u.id = v.viewer_id AND u.status = 'active'
        WHERE v.viewed_id = ? ORDER BY v.viewed_at DESC LIMIT 6", [$me['id']]);
    $views7 = (int)val('SELECT COUNT(*) FROM profile_views WHERE viewed_id = ? AND viewed_at > (NOW() - INTERVAL 7 DAY)', [$me['id']]);
    $likedMe = (int)val("SELECT COUNT(*) FROM swipes s WHERE s.target_id = ? AND s.liked = 1 AND NOT EXISTS (SELECT 1 FROM swipes t WHERE t.user_id = ? AND t.target_id = s.user_id)", [$me['id'], $me['id']]);
    render('feed', [
        'viewers' => $viewers, 'views7' => $views7, 'likedMe' => $likedMe,
        'title' => 'Feed', 'posts' => $posts, 'tab' => $tab, 'page' => $page, 'myProps' => $myProps,
        'suggest' => array_slice($suggest, 0, 5), 'completeness' => profile_completeness($me),
        'mainClass' => 'main-wide',
    ]);
}

function feed_create(): void
{
    $me = require_login();
    $body = mb_substr(input('body'), 0, 3000);
    $propId = (int)input('property_id') ?: null;
    if ($propId && !val("SELECT 1 FROM properties WHERE id = ? AND status = 'approved'", [$propId])) $propId = null;
    try {
        $img = save_upload('image', 'posts', 1400, 1400);
    } catch (RuntimeException $e) {
        flash('error', $e->getMessage());
        back();
    }
    $gif = $img ? null : clean_gif_url((string)($_POST['gif'] ?? ''));
    if ($body === '' && !$img && !$gif) {
        flash('error', 'Write something to post.');
        back();
    }
    $recent = (int)val('SELECT COUNT(*) FROM posts WHERE user_id = ? AND created_at > (NOW() - INTERVAL 1 MINUTE)', [$me['id']]);
    if ($recent >= 3) {
        flash('error', 'You’re posting a bit fast. Try again in a minute.');
        back();
    }
    q('INSERT INTO posts (user_id, property_id, body, image, gif_url) VALUES (?, ?, ?, ?, ?)', [$me['id'], $propId, $body, $img, $gif]);
    flash('success', 'Posted!');
    back('/home');
}

function feed_show(string $id): void
{
    require_login();
    $posts = load_posts('p.id = ?', [(int)$id], 1, 0, 0);
    if (!$posts && is_admin()) {
        $posts = []; // hidden posts are reviewed in admin
    }
    if (!$posts) not_found();
    render('post_show', ['title' => 'Post', 'p' => $posts[0]]);
}

function feed_like(string $id): void
{
    $me = require_login();
    $post = one("SELECT * FROM posts WHERE id = ? AND status = 'visible'", [(int)$id]);
    if (!$post || is_blocked_between((int)$me['id'], (int)$post['user_id'])) {
        is_ajax() ? json_out(['error' => 'Post not found'], 404) : not_found();
    }
    $want = input('reaction');
    $want = array_key_exists($want, REACTIONS) ? $want : null;
    $current = val('SELECT reaction FROM post_likes WHERE post_id = ? AND user_id = ?', [$post['id'], $me['id']]);
    if ($current && (!$want || $want === $current)) {
        q('DELETE FROM post_likes WHERE post_id = ? AND user_id = ?', [$post['id'], $me['id']]);
        $mine = null;
    } else {
        $mine = $want ?: 'like';
        q('INSERT INTO post_likes (post_id, user_id, reaction) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE reaction = VALUES(reaction)', [$post['id'], $me['id'], $mine]);
        if (!$current && !val("SELECT 1 FROM notifications WHERE user_id = ? AND actor_id = ? AND type = 'like' AND entity_id = ?", [$post['user_id'], $me['id'], $post['id']])) {
            notify((int)$post['user_id'], 'like', (int)$me['id'], (int)$post['id']);
        }
    }
    $count = (int)val('SELECT COUNT(*) FROM post_likes WHERE post_id = ?', [$post['id']]);
    $top = array_column(all('SELECT reaction, COUNT(*) n FROM post_likes WHERE post_id = ? GROUP BY reaction ORDER BY n DESC LIMIT 3', [$post['id']]), 'reaction');
    if (is_ajax()) json_out(['reaction' => $mine, 'count' => $count, 'top' => array_map(fn($r) => REACTIONS[$r][0], $top)]);
    back();
}

/** GIF search, proxied through GIPHY with the key from Admin → Settings. */
function feed_gifs(): void
{
    require_login();
    $key = setting('giphy_key', '');
    if ($key === '') json_out(['enabled' => false, 'results' => []]);
    $q = mb_substr(trim((string)($_GET['q'] ?? '')), 0, 60);
    $url = 'https://api.giphy.com/v1/gifs/' . ($q === '' ? 'trending?' : 'search?q=' . rawurlencode($q) . '&') . 'limit=24&rating=pg-13&api_key=' . rawurlencode($key);
    $ctx = stream_context_create(['http' => ['timeout' => 8, 'ignore_errors' => true]]);
    $data = json_decode((string)@file_get_contents($url, false, $ctx), true);
    $out = [];
    foreach ($data['data'] ?? [] as $g) {
        $img = $g['images'] ?? [];
        $full = $img['downsized_medium']['url'] ?? $img['original']['url'] ?? null;
        $thumb = $img['fixed_width_small']['url'] ?? $img['fixed_width']['url'] ?? $full;
        if ($full && clean_gif_url($full)) $out[] = ['url' => $full, 'thumb' => $thumb, 'title' => $g['title'] ?? ''];
    }
    json_out(['enabled' => true, 'results' => $out]);
}

function feed_comment(string $id): void
{
    $me = require_login();
    $post = one("SELECT * FROM posts WHERE id = ? AND status = 'visible'", [(int)$id]);
    if (!$post || is_blocked_between((int)$me['id'], (int)$post['user_id'])) not_found();
    $body = mb_substr(input('body'), 0, 1000);
    $gif = clean_gif_url((string)($_POST['gif'] ?? ''));
    if ($body !== '' || $gif) {
        q('INSERT INTO comments (post_id, user_id, body, gif_url) VALUES (?, ?, ?, ?)', [$post['id'], $me['id'], $body, $gif]);
        notify((int)$post['user_id'], 'comment', (int)$me['id'], (int)$post['id']);
    }
    $ref = $_SERVER['HTTP_REFERER'] ?? '/post/' . $post['id'];
    redirect(strtok($ref, '#') . '#post-' . $post['id']);
}

function feed_delete(string $id): void
{
    $me = require_login();
    $post = one('SELECT * FROM posts WHERE id = ?', [(int)$id]);
    if (!$post) not_found();
    if ((int)$post['user_id'] !== (int)$me['id'] && !is_admin()) not_found();
    if ((int)$post['user_id'] !== (int)$me['id']) audit('post.delete', "post #{$post['id']} by user #{$post['user_id']}");
    delete_upload('posts', $post['image']);
    q('DELETE FROM posts WHERE id = ?', [$post['id']]);
    flash('success', 'Post deleted.');
    $ref = $_SERVER['HTTP_REFERER'] ?? '';
    redirect(str_contains($ref, '/post/') ? '/home' : ($ref ?: '/home'));
}

function feed_comment_delete(string $id): void
{
    $me = require_login();
    $c = one('SELECT c.*, p.user_id AS post_owner FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.id = ?', [(int)$id]);
    if (!$c) not_found();
    if ((int)$c['user_id'] !== (int)$me['id'] && (int)$c['post_owner'] !== (int)$me['id'] && !is_admin()) not_found();
    q('DELETE FROM comments WHERE id = ?', [$c['id']]);
    back();
}

function feed_report(): void
{
    $me = require_login();
    $type = input('type');
    $id = (int)input('id');
    $reason = mb_substr(input('reason'), 0, 500);
    if (!in_array($type, ['user', 'post', 'comment', 'property'], true) || !$id || $reason === '') {
        is_ajax() ? json_out(['error' => 'Please tell us what’s wrong.'], 422) : back();
    }
    if (!val('SELECT 1 FROM reports WHERE reporter_id = ? AND target_type = ? AND target_id = ? AND status = ?', [$me['id'], $type, $id, 'open'])) {
        q('INSERT INTO reports (reporter_id, target_type, target_id, reason) VALUES (?, ?, ?, ?)', [$me['id'], $type, $id, $reason]);
        try { email_admins("New report: $type #$id", "@{$me['username']} reported a $type.\n\nReason: $reason\n\nReview: " . base_url() . '/admin/reports'); } catch (Throwable $e) {}
    }
    if (is_ajax()) json_out(['ok' => true, 'message' => 'Thanks — our team will review this.']);
    flash('success', 'Thanks — our team will review this.');
    back();
}
