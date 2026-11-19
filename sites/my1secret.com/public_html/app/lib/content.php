<?php
declare(strict_types=1);
defined('M1S') || exit;

/* ---------- URLs ---------- */
function article_url(array $a): string { return '/blog/' . $a['slug'] . '/'; }
function topic_url(array|string $t): string { return '/blog/topic/' . (is_array($t) ? $t['slug'] : $t) . '/'; }
function community_url(array|string $c): string { return '/forum/' . (is_array($c) ? $c['slug'] : $c) . '/'; }

function thread_url(array $t): string
{
    $cslug = $t['community_slug'] ?? val('SELECT slug FROM communities WHERE id = ?', [$t['community_id']]);
    return '/forum/' . $cslug . '/' . (int)$t['id'] . '-' . $t['slug'] . '/';
}

/* ---------- ranking ---------- */

/** Reddit-style hot score: log of net votes plus a time bonus (12.5h per 10x votes). */
function hot_score(int $score, string $createdAt): float
{
    $order = log10(max(abs($score), 1));
    $sign = $score > 0 ? 1 : ($score < 0 ? -1 : 0);
    $seconds = strtotime($createdAt . ' UTC') - 1700000000;
    return round($sign * $order + $seconds / 45000, 7);
}

const M1S_VOTE_TYPES = ['thread' => 'threads', 'comment' => 'comments', 'article' => 'articles'];

/**
 * Cast, change or clear a vote. $value: 1, -1 or 0.
 * Returns ['score' => int, 'vote' => int].
 */
function cast_vote(int $userId, string $type, int $id, int $value): array
{
    $table = M1S_VOTE_TYPES[$type] ?? null;
    if (!$table) {
        throw new InvalidArgumentException('bad vote type');
    }
    $value = max(-1, min(1, $value));
    if ($type === 'article') {
        $value = max(0, $value);   // articles only take "helpful" upvotes
    }
    $target = one("SELECT * FROM $table WHERE id = ?", [$id]);
    if (!$target) {
        throw new RuntimeException('not found');
    }
    $authorId = (int)($target['author_id'] ?? $target['user_id'] ?? 0);

    $pdo = db();
    $pdo->beginTransaction();
    try {
        $prev = (int)(val('SELECT value FROM votes WHERE user_id = ? AND target_type = ? AND target_id = ?', [$userId, $type, $id]) ?? 0);
        if ($prev === $value) {
            $pdo->commit();
            return ['score' => (int)$target['score'], 'vote' => $value];
        }
        if ($value === 0) {
            q('DELETE FROM votes WHERE user_id = ? AND target_type = ? AND target_id = ?', [$userId, $type, $id]);
        } elseif ($prev === 0) {
            insert('votes', ['user_id' => $userId, 'target_type' => $type, 'target_id' => $id, 'value' => $value, 'created_at' => now()]);
        } else {
            q('UPDATE votes SET value = ?, created_at = ? WHERE user_id = ? AND target_type = ? AND target_id = ?', [$value, now(), $userId, $type, $id]);
        }
        $up = ($value === 1 ? 1 : 0) - ($prev === 1 ? 1 : 0);
        $down = ($value === -1 ? 1 : 0) - ($prev === -1 ? 1 : 0);
        $delta = $value - $prev;
        q("UPDATE $table SET upvotes = upvotes + ?, downvotes = downvotes + ?, score = score + ? WHERE id = ?", [$up, $down, $delta, $id]);
        if ($type === 'thread') {
            $score = (int)$target['score'] + $delta;
            q('UPDATE threads SET hot = ? WHERE id = ?', [hot_score($score, $target['created_at']), $id]);
        }
        if ($authorId && $authorId !== $userId) {
            q('UPDATE users SET karma = karma + ? WHERE id = ?', [$delta, $authorId]);
        }
        $pdo->commit();
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
    return ['score' => (int)$target['score'] + ($value - $prev), 'vote' => $value];
}

/** Map of target_id => vote value for the current user. */
function my_votes(string $type, array $ids): array
{
    $u = uid();
    $ids = array_values(array_unique(array_map('intval', $ids)));
    if (!$u || !$ids) {
        return [];
    }
    $in = implode(',', array_fill(0, count($ids), '?'));
    $rows = all("SELECT target_id, value FROM votes WHERE user_id = ? AND target_type = ? AND target_id IN ($in)", array_merge([$u, $type], $ids));
    $out = [];
    foreach ($rows as $r) {
        $out[(int)$r['target_id']] = (int)$r['value'];
    }
    return $out;
}

/* ---------- threads ---------- */
const THREAD_SELECT = 'SELECT t.*, c.slug AS community_slug, c.name AS community_name, c.color AS community_color,
    u.username, u.role, u.display_name
    FROM threads t JOIN communities c ON c.id = t.community_id LEFT JOIN users u ON u.id = t.user_id';

/**
 * $sort: hot | new | top | comments.  $period for top: day|week|month|year|all
 */
function thread_list(?int $communityId, string $sort, int $page, int $per = 20, string $period = 'all', bool $withPinned = true): array
{
    $where = ['t.removed = 0 AND t.status = \'live\''];
    $p = [];
    if ($communityId) {
        $where[] = 't.community_id = :cid';
        $p['cid'] = $communityId;
    }
    if ($sort === 'top' && $period !== 'all') {
        $secs = ['day' => 86400, 'week' => 604800, 'month' => 2592000, 'year' => 31536000][$period] ?? 0;
        if ($secs) {
            $where[] = 't.created_at > :since';
            $p['since'] = gmdate('Y-m-d H:i:s', time() - $secs);
        }
    }
    $order = match ($sort) {
        'new' => 't.created_at DESC',
        'top' => 't.score DESC, t.created_at DESC',
        'comments' => 't.comment_count DESC, t.created_at DESC',
        'active' => 't.last_activity_at DESC',
        default => 't.hot DESC',
    };
    if ($withPinned && $communityId && $page === 1 && $sort === 'hot') {
        $order = 't.pinned DESC, ' . $order;
    }
    $p['lim'] = $per + 1;
    $p['off'] = ($page - 1) * $per;
    $rows = all(THREAD_SELECT . ' WHERE ' . implode(' AND ', $where) . " ORDER BY $order LIMIT :lim OFFSET :off", $p);
    $hasNext = count($rows) > $per;
    return [array_slice($rows, 0, $per), $hasNext];
}

function find_thread(int $id): ?array
{
    return one(THREAD_SELECT . ' WHERE t.id = ?', [$id]);
}

/** Thread pages worth indexing: not removed, and with some substance or discussion. */
function thread_indexable(array $t): bool
{
    if ($t['removed'] || $t['deleted']) {
        return false;
    }
    return (int)$t['comment_count'] >= 1 || mb_strlen(trim((string)$t['body'])) >= 280 || (int)$t['pinned'] === 1;
}

/* ---------- comments ---------- */

/** Comments for a thread/article as a nested tree, best-first. */
function comment_tree(string $type, int $targetId, string $baseUrl, string $sort = 'best'): array
{
    $order = $sort === 'new' ? 'c.created_at DESC' : ($sort === 'old' ? 'c.created_at ASC' : 'c.score DESC, c.created_at ASC');
    $rows = all('SELECT c.*, u.username, u.role, u.display_name FROM comments c LEFT JOIN users u ON u.id = c.user_id
                 WHERE c.target_type = ? AND c.target_id = ? AND c.status = \'live\' ORDER BY ' . $order, [$type, $targetId]);
    $byId = [];
    foreach ($rows as $r) {
        $r['children'] = [];
        $r['_url'] = $baseUrl . '#c' . $r['id'];
        $byId[(int)$r['id']] = $r;
    }
    $tree = [];
    foreach ($rows as $r) {
        $id = (int)$r['id'];
        $pid = (int)($r['parent_id'] ?? 0);
        if ($pid && isset($byId[$pid])) {
            $byId[$pid]['children'][] = &$byId[$id];
        } else {
            $tree[] = &$byId[$id];
        }
    }
    return prune_dead_comments($tree);
}

/** Drop removed/deleted comments that have no live replies. */
function prune_dead_comments(array $tree): array
{
    $out = [];
    foreach ($tree as $c) {
        $c['children'] = prune_dead_comments($c['children']);
        if (($c['removed'] || $c['deleted']) && !$c['children']) {
            continue;
        }
        $out[] = $c;
    }
    return $out;
}

function flatten_ids(array $tree): array
{
    $ids = [];
    foreach ($tree as $c) {
        $ids[] = (int)$c['id'];
        $ids = array_merge($ids, flatten_ids($c['children']));
    }
    return $ids;
}

function refresh_comment_count(string $type, int $id): void
{
    $n = (int)val('SELECT COUNT(*) FROM comments WHERE target_type = ? AND target_id = ? AND removed = 0 AND deleted = 0 AND status = \'live\'', [$type, $id]);
    $table = $type === 'thread' ? 'threads' : 'articles';
    q("UPDATE $table SET comment_count = ? WHERE id = ?", [$n, $id]);
}

/* ---------- communities / topics ---------- */
function communities(): array
{
    static $c = null;
    return $c ??= all('SELECT * FROM communities ORDER BY sort, name');
}

function find_community(string $slug): ?array
{
    foreach (communities() as $c) {
        if ($c['slug'] === $slug) {
            return $c;
        }
    }
    return null;
}

function topics(): array
{
    static $t = null;
    return $t ??= all('SELECT t.*, (SELECT COUNT(*) FROM articles a WHERE a.topic_id = t.id AND a.status = \'published\') AS article_count FROM topics t ORDER BY sort, name');
}

function find_topic_by_id(int $id): ?array
{
    foreach (topics() as $t) {
        if ((int)$t['id'] === $id) {
            return $t;
        }
    }
    return null;
}

const ARTICLE_SELECT = "SELECT a.*, t.slug AS topic_slug, t.name AS topic_name, u.username AS author_username, u.display_name AS author_name
    FROM articles a LEFT JOIN topics t ON t.id = a.topic_id LEFT JOIN users u ON u.id = a.author_id";

function article_list(?int $topicId, int $page, int $per = 12, ?int $authorId = null): array
{
    $where = ["a.status = 'published'", 'a.published_at <= :now'];
    $p = ['now' => now()];
    if ($topicId) { $where[] = 'a.topic_id = :tid'; $p['tid'] = $topicId; }
    if ($authorId) { $where[] = 'a.author_id = :aid'; $p['aid'] = $authorId; }
    $p['lim'] = $per + 1;
    $p['off'] = ($page - 1) * $per;
    $rows = all(ARTICLE_SELECT . ' WHERE ' . implode(' AND ', $where) . ' ORDER BY a.published_at DESC LIMIT :lim OFFSET :off', $p);
    return [array_slice($rows, 0, $per), count($rows) > $per];
}

/* ---------- uploads ---------- */

/**
 * Validate and re-encode an uploaded image (strips metadata and anything that
 * is not pixels). Returns [path, w, h] or an error string.
 */
function store_upload_image(array $file): array|string
{
    if (($file['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) {
        return 'none';
    }
    if ($file['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($file['tmp_name'])) {
        return 'The image did not upload. Try a smaller file.';
    }
    if ($file['size'] > 8 * 1024 * 1024) {
        return 'Images must be under 8 MB.';
    }
    $info = @getimagesize($file['tmp_name']);
    if (!$info || !in_array($info[2], [IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_GIF, IMAGETYPE_WEBP], true)) {
        return 'Only JPG, PNG, GIF or WebP images are allowed.';
    }
    [$w, $h] = $info;
    if ($w < 50 || $h < 50 || $w * $h > 40_000_000) {
        return 'That image size is not supported.';
    }
    $src = match ($info[2]) {
        IMAGETYPE_JPEG => @imagecreatefromjpeg($file['tmp_name']),
        IMAGETYPE_PNG  => @imagecreatefrompng($file['tmp_name']),
        IMAGETYPE_GIF  => @imagecreatefromgif($file['tmp_name']),
        IMAGETYPE_WEBP => @imagecreatefromwebp($file['tmp_name']),
    };
    if (!$src) {
        return 'That image could not be read.';
    }
    if ($info[2] === IMAGETYPE_JPEG && function_exists('exif_read_data')) {
        $o = (int)(@exif_read_data($file['tmp_name'])['Orientation'] ?? 1);
        $src = match ($o) { 3 => imagerotate($src, 180, 0), 6 => imagerotate($src, -90, 0), 8 => imagerotate($src, 90, 0), default => $src };
        [$w, $h] = [imagesx($src), imagesy($src)];
    }
    $max = 1600;
    if ($w > $max) {
        $nh = (int)round($h * $max / $w);
        $dst = imagecreatetruecolor($max, $nh);
        imagealphablending($dst, false);
        imagesavealpha($dst, true);
        imagecopyresampled($dst, $src, 0, 0, 0, 0, $max, $nh, $w, $h);
        $src = $dst;
        [$w, $h] = [$max, $nh];
    } else {
        imagepalettetotruecolor($src);
        imagesavealpha($src, true);
    }
    $dir = '/uploads/' . gmdate('Y/m');
    if (!is_dir(M1S_ROOT . $dir) && !mkdir(M1S_ROOT . $dir, 0755, true)) {
        return 'Uploads are not available right now.';
    }
    $name = $dir . '/' . bin2hex(random_bytes(10)) . '.webp';
    if (!imagewebp($src, M1S_ROOT . $name, 82)) {
        return 'That image could not be saved.';
    }
    return [$name, $w, $h];
}
