<?php
// Thought Changer — shared bootstrap: config, data access, helpers.
declare(strict_types=1);

// Staging copy (staging.thoughtchangerblog.com) uses its own host and is never indexed.
define('IS_STAGING', str_starts_with(strtolower($_SERVER['HTTP_HOST'] ?? ''), 'staging.'));
define('SITE_URL', IS_STAGING ? 'https://staging.thoughtchangerblog.com' : 'https://thoughtchangerblog.com');
if (IS_STAGING && !headers_sent()) header('X-Robots-Tag: noindex, nofollow');
const SITE_NAME = 'Thought Changer';
const SITE_TAGLINE = 'One Thought at a Time.';
const SITE_EMAIL = 'info@thoughtchangerblog.com';
const GA_ID = 'G-BJ6HPX7KCP';
const AMAZON_TAG = 'thoughtchangerblog-20';
const LOGO = '/wp-content/uploads/2026/01/Thought-Changer-Logo.webp';
const LOGO_WHITE = '/wp-content/uploads/2026/01/Thought-Changer-Logo-Wh.webp';
const SITE_ICON = '/wp-content/uploads/2026/01/cropped-Thought-Changer-Site-Icon-270x270.webp';
const ASSET_VER = '20261119c';

define('APP', __DIR__);
define('WEBROOT', dirname(__DIR__));

/**
 * Secrets (SMTP password) live OUTSIDE the web root, never in git.
 * Looked up in order: tc-config.php in private_dir() (the folder holding public_html), app/config.local.php.
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
    foreach ([private_dir() . '/tc-config.php', APP . '/config.local.php'] as $f) {
        if (is_file($f)) { $cfg = array_merge($cfg, (array) require $f); break; }
    }
    return $cfg;
}

/** First directory above the web root that is not itself web-served (handles staging inside public_html). */
function private_dir(): string {
    $d = dirname(WEBROOT);
    while (basename($d) === 'public_html' || str_contains($d . '/', '/public_html/')) $d = dirname($d);
    return $d;
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

/** Posts getting the most clicks + impressions in Search Console (May–Nov 2026), best first. */
const FEATURED = [
    'life-is-fleeting-5-ways-to-slow-it-down', 'heres-what-it-means-to-level-up', 'stick-to-your-lane',
    'becoming-seasoned', 'lessons-from-the-formative-teen-years', 'create-a-blind-side-vision-for-your-career-life',
    'how-rainbow-thinking-can-catapult-your-career-improve-your-life', 'flip_the_switch_to_reveal_the_2019_word_of_the_year',
    '11-signs-youre-stuck-in-complacency', 'how-to-love-the-rabbit-hole', 'meaning-begins-with-an-inkling',
    'life-lessons-from-an-albatross', 'the-power-of-your-own-light', 'i-had-an-epiphany-the-courtship-of-an-idea',
];

function featured_posts(): array { return array_values(array_filter(array_map('post_by_slug', FEATURED))); }

function search_terms(string $q): array {
    $q = mb_strtolower(trim($q));
    return array_values(array_filter(preg_split('/[^\p{L}\p{N}\']+/u', $q), fn($t) => mb_strlen($t) > 1));
}

/** Weighted search: every term must appear somewhere; title > headings > description > body. */
function search_posts(string $q): array {
    $terms = search_terms($q);
    if (!$terms) return [];
    $phrase = mb_strtolower(trim($q));
    $hits = [];
    foreach (posts() as $i => $p) {
        $title = mb_strtolower($p['title']);
        $desc = mb_strtolower($p['description'] . ' ' . implode(' ', $p['categories']));
        $body = null; $score = 0;
        foreach ($terms as $t) {
            $s = 0;
            if (preg_match('/\b' . preg_quote($t, '/') . '/u', $title)) $s += 10;
            elseif (str_contains($title, $t)) $s += 6;
            if (str_contains($desc, $t)) $s += 3;
            if (!$s) {
                $body ??= mb_strtolower(strip_tags(post_body($p)));
                $n = substr_count($body, $t);
                if ($n) $s += min(3, 1 + intdiv($n, 4));
            }
            if (!$s) { $score = 0; break; }
            $score += $s;
        }
        if (!$score) continue;
        if (count($terms) > 1 && str_contains($title, $phrase)) $score += 15;
        $rank = array_search($p['slug'], FEATURED, true);
        if ($rank !== false) $score += 2 - $rank * 0.1;           // gentle tie-break toward popular posts
        $hits[] = [$score, $i, $p];
    }
    usort($hits, fn($a, $b) => [$b[0], $a[1]] <=> [$a[0], $b[1]]);
    return array_map(fn($h) => $h[2], $hits);
}

/** Compact index for the as-you-type suggestions (fetched once by site.js). */
function search_index(): array {
    return array_map(function ($p) {
        preg_match_all('#<h[23][^>]*>(.*?)</h[23]>#s', post_body($p), $m);
        return ['t' => $p['title'], 'u' => '/' . $p['slug'] . '/', 'i' => str_replace('-768x512', '-300x200', thumb($p['image'])),
                'c' => primary_cat($p), 'd' => $p['description'],
                'h' => mb_substr(html_entity_decode(strip_tags(implode(' · ', $m[1])), ENT_QUOTES, 'UTF-8'), 0, 600),
                'f' => (int) (array_search($p['slug'], FEATURED, true) !== false)];
    }, posts());
}

/**
 * Contextual internal links. Scans paragraph/list text (never headings, existing links, captions,
 * tables or FAQ), collects every phrase match from content/interlinks.json, then links the best
 * candidates: popular posts first (FEATURED), then more specific phrases. One link per target,
 * one per paragraph, no self-links, nothing the article already links to, at most $max per article.
 */
function auto_interlink(string $html, string $selfSlug, int $max = 5): string {
    static $map = null;
    if ($map === null) {
        $map = [];
        foreach (json_decode((string) file_get_contents(WEBROOT . '/content/interlinks.json'), true) as $phrases => $slug) {
            foreach (explode('|', $phrases) as $ph) $map[] = [$ph, $slug];
        }
    }
    preg_match_all('#href="/([a-z0-9_-]+)/"#', $html, $m);
    $used = array_flip($m[1]);
    $used[$selfSlug] = true;
    $parts = preg_split('#(<[^>]+>)#', $html, -1, PREG_SPLIT_DELIM_CAPTURE);
    $stack = []; $block = -1; $blockId = 0; $cands = [];
    foreach ($parts as $i => $part) {
        if ($part === '') continue;
        if ($part[0] === '<') {
            if (preg_match('#^<(/?)(a|h[1-6]|p|li|figcaption|summary|table|blockquote)\b#i', $part, $t)) {
                $tag = strtolower($t[2]); $close = $t[1] === '/';
                if ($tag === 'p' || $tag === 'li') $block = $close ? -1 : ++$blockId;
                else $close ? array_pop($stack) : $stack[] = $tag;
            }
            continue;
        }
        if ($block < 0 || $stack) continue;
        foreach ($map as [$ph, $slug]) {
            if (isset($used[$slug])) continue;
            if (preg_match('/(?<![\p{L}\p{N}-])(' . preg_quote($ph, '/') . ')(?![\p{L}\p{N}-])/iu', $part, $mm, PREG_OFFSET_CAPTURE)) {
                $rank = array_search($slug, FEATURED, true);
                $prio = ($rank === false ? 0 : 30 - $rank) + mb_strlen($ph) / 2 - $i / 400;   // popular, specific, early
                $cands[] = ['slug' => $slug, 'part' => $i, 'block' => $block, 'off' => $mm[1][1], 'txt' => $mm[1][0], 'prio' => $prio];
            }
        }
    }
    usort($cands, fn($a, $b) => $b['prio'] <=> $a['prio']);
    $pick = []; $blocks = []; $parts_used = [];
    foreach ($cands as $c) {
        if (count($pick) >= $max) break;
        if (isset($used[$c['slug']]) || isset($blocks[$c['block']]) || isset($parts_used[$c['part']])) continue;
        if (!post_by_slug($c['slug'])) continue;
        $pick[] = $c; $used[$c['slug']] = true; $blocks[$c['block']] = true; $parts_used[$c['part']] = true;
    }
    foreach ($pick as $c) {
        $p = $parts[$c['part']]; $t = post_by_slug($c['slug']);
        $parts[$c['part']] = substr($p, 0, $c['off']) . '<a href="/' . $c['slug'] . '/" class="ilink" title="' . e($t['title']) . '">'
            . $c['txt'] . '</a>' . substr($p, $c['off'] + strlen($c['txt']));
    }
    return implode('', $parts);
}
