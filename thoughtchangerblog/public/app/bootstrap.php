<?php
// Thought Changer — shared bootstrap: config, data access, helpers.
declare(strict_types=1);

const SITE_URL  = 'https://thoughtchangerblog.com';
const SITE_NAME = 'Thought Changer';
const SITE_TAGLINE = 'One Thought at a Time.';
const SITE_EMAIL = 'info@thoughtchangerblog.com';
const GA_ID = 'G-BJ6HPX7KCP';
const AMAZON_TAG = 'thoughtchangerblog-20';
const LOGO = '/wp-content/uploads/2026/01/Thought-Changer-Logo.webp';
const LOGO_WHITE = '/wp-content/uploads/2026/01/Thought-Changer-Logo-Wh.webp';
const SITE_ICON = '/wp-content/uploads/2026/01/cropped-Thought-Changer-Site-Icon-270x270.webp';
const ASSET_VER = '20261119';

define('APP', __DIR__);
define('WEBROOT', dirname(__DIR__));

/**
 * Secrets (SMTP password) live OUTSIDE the web root, never in git.
 * Looked up in order: ../tc-config.php (one level above public_html), app/config.local.php.
 */
function config(): array {
    static $cfg = null;
    if ($cfg !== null) return $cfg;
    $cfg = [
        'smtp_host' => 'smtp.hostinger.com',
        'smtp_port' => 465,
        'smtp_user' => SITE_EMAIL,
        'smtp_pass' => '',
        'mail_to'   => SITE_EMAIL,
    ];
    foreach ([dirname(WEBROOT) . '/tc-config.php', APP . '/config.local.php'] as $f) {
        if (is_file($f)) { $cfg = array_merge($cfg, (array) require $f); break; }
    }
    return $cfg;
}

function e(?string $s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function posts(): array {
    static $posts = null;
    if ($posts === null) {
        $posts = json_decode((string) file_get_contents(WEBROOT . '/content/posts.json'), true) ?: [];
        usort($posts, fn($a, $b) => strcmp($b['published'], $a['published']));
    }
    return $posts;
}

function post_by_slug(string $slug): ?array {
    foreach (posts() as $p) if ($p['slug'] === $slug) return $p;
    return null;
}

function posts_in(string $cat): array {
    return array_values(array_filter(posts(), fn($p) => in_array($cat, $p['categories'], true)));
}

function post_body(array $p): string {
    $f = WEBROOT . '/content/posts/' . basename($p['slug']) . '.html';
    return is_file($f) ? (string) file_get_contents($f) : '';
}

function primary_cat(array $p): string {
    foreach ($p['categories'] as $c) if ($c !== 'General') return $c;
    return 'Reflections';
}

function cat_url(string $c): string {
    return ['Mindset' => '/mindset/', 'Quotes' => '/quotes/'][$c] ?? '/category/general/';
}

function amazon_url(array $prod): string {
    if (!empty($prod['asin'])) return 'https://www.amazon.com/dp/' . rawurlencode($prod['asin']) . '/?tag=' . AMAZON_TAG;
    return 'https://www.amazon.com/s?k=' . urlencode($prod['q'] ?? $prod['title']) . '&tag=' . AMAZON_TAG;
}

function fmt_date(string $iso): string { return date('F j, Y', strtotime($iso)); }

function reading_time(array $p): int { return max(3, (int) round(((int) ($p['words'] ?? 1200)) / 230)); }

/** Responsive srcset from the WordPress-style size variants that exist on disk. */
function img_srcset(string $src): string {
    if (!preg_match('#^(/wp-content/uploads/.+?)(\.\w+)$#', $src, $m)) return '';
    $set = [];
    foreach ([300 => '300x200', 768 => '768x512', 1024 => '1024x683'] as $w => $dim) {
        $v = $m[1] . '-' . $dim . $m[2];
        if (is_file(WEBROOT . rawurldecode($v))) $set[] = $v . ' ' . $w . 'w';
    }
    if (is_file(WEBROOT . rawurldecode($src))) $set[] = $src . ' 1536w';
    return implode(', ', $set);
}

function thumb(string $src): string {
    if (preg_match('#^(/wp-content/uploads/.+?)(\.\w+)$#', $src, $m)) {
        $v = $m[1] . '-768x512' . $m[2];
        if (is_file(WEBROOT . rawurldecode($v))) return $v;
    }
    return $src;
}

function related_posts(array $post, int $n = 3): array {
    $scored = [];
    foreach (posts() as $p) {
        if ($p['slug'] === $post['slug']) continue;
        $s = count(array_intersect(array_diff($p['categories'], ['General']), $post['categories'])) * 3;
        $a = array_flip(array_filter(preg_split('/\W+/', strtolower($post['title'])), fn($w) => strlen($w) > 3));
        foreach (preg_split('/\W+/', strtolower($p['title'])) as $w) if (isset($a[$w])) $s += 2;
        $s += crc32($post['slug'] . $p['slug']) % 3; // stable variety
        $scored[] = [$s, $p];
    }
    usort($scored, fn($x, $y) => $y[0] <=> $x[0]);
    return array_map(fn($x) => $x[1], array_slice($scored, 0, $n));
}

function view(string $name, array $vars = []): void {
    extract($vars, EXTR_SKIP);
    require APP . '/views/' . $name . '.php';
}

function csrf_token(): string {
    // Stateless token: HMAC of a time bucket, so pages stay cacheable-friendly without sessions.
    $key = hash('sha256', (config()['smtp_pass'] ?: 'tc') . __FILE__);
    $t = (string) time();
    return $t . '.' . substr(hash_hmac('sha256', $t, $key), 0, 24);
}

function csrf_ok(string $tok): bool {
    $key = hash('sha256', (config()['smtp_pass'] ?: 'tc') . __FILE__);
    [$t, $h] = array_pad(explode('.', $tok, 2), 2, '');
    if (!ctype_digit($t)) return false;
    $age = time() - (int) $t;
    if ($age < 3 || $age > 86400) return false;          // too fast = bot; older than a day = stale
    return hash_equals(substr(hash_hmac('sha256', $t, $key), 0, 24), $h);
}

/** Every product used across the site, de-duplicated, most-recommended first (for the bookshelf). */
function bookshelf_items(): array {
    $seen = [];
    foreach (posts() as $p) foreach ($p['products'] ?? [] as $pr) {
        $k = strtolower($pr['title']);
        if (!isset($seen[$k])) $seen[$k] = $pr + ['count' => 0, 'from' => []];
        $seen[$k]['count']++;
        $seen[$k]['from'][] = $p['slug'];
    }
    $items = array_values($seen);
    usort($items, fn($a, $b) => [$b['count'], $a['title']] <=> [$a['count'], $b['title']]);
    return $items;
}
