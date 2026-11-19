<?php
/*
 * Seattle Northwest Homes — application bootstrap.
 * Loaded by public_html/index.php. Every other file in app/ starts with
 * `defined('SNW') || (http_response_code(404) && exit);` so nothing can be executed by requesting it directly.
 */
define('SNW', true);
define('APP', __DIR__);

$GLOBALS['CFG'] = require APP . '/config.php';

function cfg(string $k, $default = null) { return $GLOBALS['CFG'][$k] ?? $default; }

/* ---------- output helpers ---------- */

function e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function abs_url(string $path = '/'): string { return rtrim(cfg('url'), '/') . $path; }

/** Versioned asset URL so CSS/JS changes bust the CDN cache. */
function asset(string $path): string
{
    $file = PUBLIC_DIR . '/assets/' . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return '/assets/' . $path . '?v=' . $v;
}

function photo(string $name, bool $small = false): string
{
    return '/assets/img/photos/' . $name . ($small ? '-sm' : '') . '.webp';
}

/** Blog image path: legacy images live in /img/blog/, new ones reuse /img/photos/. */
function post_image(array $p, bool $small = false): string
{
    $img = $p['image'] ?? '';
    if ($img === '') return '/assets/img/brand/og-default.jpg';
    $stem = preg_replace('/\.webp$/', '', $img);
    if (is_file(PUBLIC_DIR . '/assets/img/blog/' . $stem . '.webp')) {
        return '/assets/img/blog/' . $stem . ($small ? '-sm' : '') . '.webp';
    }
    return photo($stem, $small);
}

function money(int $n): string { return '$' . number_format($n); }

function fmt_baths($b): string { return rtrim(rtrim(number_format((float) $b, 2), '0'), '.'); }

function fmt_date(string $ymd): string { return date('F j, Y', strtotime($ymd)); }

function reading_time(string $html): int { return max(2, (int) round(str_word_count(strip_tags($html)) / 230)); }

function excerpt(string $html, int $len = 160): string
{
    $t = trim(preg_replace('/\s+/', ' ', html_entity_decode(strip_tags($html), ENT_QUOTES, 'UTF-8')));
    if (mb_strlen($t) <= $len) return $t;
    $cut = mb_substr($t, 0, $len);
    return rtrim(mb_substr($cut, 0, (int) mb_strrpos($cut, ' ')), ',;:.—-') . '…';
}

/* ---------- data access ---------- */

function data(string $name): array
{
    static $cache = [];
    return $cache[$name] ??= require APP . '/data/' . $name . '.php';
}

function listings(): array { return data('listings'); }

function listing(string $slug): ?array
{
    foreach (listings() as $l) if ($l['slug'] === $slug) return $l;
    return null;
}

function neighborhoods(): array { return data('neighborhoods'); }

function categories(): array { return data('categories'); }

/** All blog posts, newest first. */
function posts(): array
{
    static $posts = null;
    if ($posts !== null) return $posts;
    $posts = [];
    foreach (glob(APP . '/content/posts/*.php') as $f) {
        $p = require $f;
        if (!is_array($p) || empty($p['slug'])) continue;
        $p['modified'] = $p['modified'] ?? $p['date'];
        $posts[$p['slug']] = $p;
    }
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']) ?: strcmp($a['title'], $b['title']));
    return $posts;
}

function post(string $slug): ?array { return posts()[$slug] ?? null; }

/** Old WordPress slug => new blog slug, built from the 'legacy_slug' field on imported posts. */
function legacy_post_map(): array
{
    $m = [];
    foreach (posts() as $p) if (!empty($p['legacy_slug'])) $m[$p['legacy_slug']] = $p['slug'];
    return $m;
}

function related_posts(array $post, int $n = 3): array
{
    $same = array_filter(posts(), fn($p) => $p['category'] === $post['category'] && $p['slug'] !== $post['slug']);
    $out = array_slice($same, 0, $n);
    if (count($out) < $n) {
        foreach (posts() as $p) {
            if ($p['slug'] !== $post['slug'] && !isset($out[$p['slug']])) $out[$p['slug']] = $p;
            if (count($out) >= $n) break;
        }
    }
    return $out;
}

/* ---------- rendering ---------- */

/**
 * Render a view inside the layout.
 * $meta keys: title, description, canonical (path), image, type, noindex, schema (array of nodes), breadcrumbs.
 */
function render(string $view, array $vars = [], array $meta = [], int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    extract($vars, EXTR_SKIP);
    ob_start();
    require APP . '/views/' . $view . '.php';
    $content = ob_get_clean();
    require APP . '/views/layout.php';
}

function partial(string $name, array $vars = []): void
{
    extract($vars, EXTR_SKIP);
    require APP . '/views/partials/' . $name . '.php';
}

function redirect(string $to, int $code = 301): void
{
    // Root-relative targets stay on the current host, so the preview domain works too;
    // canonical-host enforcement in index.php handles the production domain.
    header('Location: ' . $to, true, $code);
    exit;
}

function not_found(): void
{
    render('404', [], ['title' => 'Page Not Found | ' . cfg('name'), 'description' => 'The page you were looking for could not be found.', 'noindex' => true], 404);
}

require APP . '/lib/schema.php';
require APP . '/lib/forms.php';
