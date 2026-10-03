<?php
/**
 * Content loaders: services, service areas, blog posts and their
 * date-based publishing rules.
 */
defined('TR_ROOT') || exit;

function load_content_file(string $file): ?array
{
    if (!is_file($file)) {
        return null;
    }
    $data = require $file;
    return is_array($data) ? $data : null;
}

/* ---------- Services ---------- */

function services(): array
{
    static $all = null;
    if ($all === null) {
        $all = [];
        foreach (catalog('services') as $slug) {
            $s = load_content_file(TR_CONTENT . '/services/' . $slug . '.php');
            if ($s) {
                $s['slug'] = $slug;
                $s['url'] = '/services/' . $slug . '/';
                $all[$slug] = $s;
            }
        }
    }
    return $all;
}

function service(string $slug): ?array
{
    return services()[$slug] ?? null;
}

/* ---------- Service areas ---------- */

/** Published service areas only, in catalog order. */
function areas(): array
{
    static $all = null;
    if ($all === null) {
        $all = [];
        foreach (catalog('areas') as $slug => $meta) {
            if (empty($meta['published'])) {
                continue;
            }
            $a = load_content_file(TR_CONTENT . '/areas/' . $slug . '.php');
            if ($a) {
                $a['slug'] = $slug;
                $a['url'] = '/service-areas/' . $slug . '/';
                $all[$slug] = $a;
            }
        }
    }
    return $all;
}

function area(string $slug): ?array
{
    return areas()[$slug] ?? null;
}

/* ---------- Blog ---------- */

/**
 * Every post with its computed publication date. Post N is published
 * on blog_launch_date + (N-1) * blog_interval_days, at 00:00 America/Chicago.
 * Sorted newest first.
 */
function all_posts(): array
{
    static $all = null;
    if ($all !== null) {
        return $all;
    }
    $tz = new DateTimeZone(cfg('timezone'));
    $launch = new DateTimeImmutable(cfg('blog_launch_date') . ' 00:00:00', $tz);
    $interval = (int) cfg('blog_interval_days', 3);
    $now = tr_now();
    $all = [];
    foreach (glob(TR_CONTENT . '/blog/*.php') ?: [] as $file) {
        $p = load_content_file($file);
        if (!$p || empty($p['slug'])) {
            continue;
        }
        $order = (int) ($p['order'] ?? 1);
        $p['date'] = $launch->modify('+' . (($order - 1) * $interval) . ' days');
        $p['published'] = $now >= $p['date'];
        $p['url'] = '/blog/' . $p['slug'] . '/';
        $p['minutes'] = reading_minutes($p['body'] ?? '');
        $all[$p['slug']] = $p;
    }
    uasort($all, fn ($a, $b) => $b['date'] <=> $a['date'] ?: ($b['order'] <=> $a['order']));
    return $all;
}

/** Publicly visible posts, newest first. */
function posts(?string $category = null): array
{
    return array_filter(all_posts(), fn ($p) => $p['published'] && ($category === null || ($p['category'] ?? '') === $category));
}

function post(string $slug): ?array
{
    $p = all_posts()[$slug] ?? null;
    return ($p && $p['published']) ? $p : null;
}

/** Posts that exist but are not public yet. */
function scheduled_post_slugs(): array
{
    return array_keys(array_filter(all_posts(), fn ($p) => !$p['published']));
}

function category_name(string $slug): string
{
    return catalog('blog_categories')[$slug] ?? 'Roofing';
}

/* ---------- Other pages ---------- */

function page_content(string $name): array
{
    return load_content_file(TR_CONTENT . '/pages/' . $name . '.php') ?? [];
}

/**
 * Turn links that point at not-yet-published posts or unpublished service
 * areas into plain text, so scheduled content is never linked or leaked.
 */
function guard_links(string $html): string
{
    $hidden = [];
    foreach (scheduled_post_slugs() as $slug) {
        $hidden[] = '/blog/' . $slug . '/';
    }
    foreach (catalog('areas') as $slug => $meta) {
        if (empty($meta['published'])) {
            $hidden[] = '/service-areas/' . $slug . '/';
        }
    }
    if (!$hidden) {
        return $html;
    }
    $alts = implode('|', array_map(fn ($u) => preg_quote($u, '~'), $hidden));
    $abs = preg_quote(rtrim(cfg('base_url'), '/'), '~');
    return preg_replace(
        '~<a\b[^>]*\bhref="(?:' . $abs . ')?(?:' . $alts . ')(?:#[^"]*)?"[^>]*>(.*?)</a>~s',
        '<span class="pending-link">$1</span>',
        $html
    );
}
