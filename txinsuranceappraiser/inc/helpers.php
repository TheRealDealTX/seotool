<?php
declare(strict_types=1);

/** HTML-escape. */
function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Absolute canonical URL on the production origin. */
function abs_url(string $path): string
{
    return SITE['origin'] . $path;
}

/** True when the request is served from the production domain (not the staging/temporary domain). */
function is_production(): bool
{
    $host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
    return $host === SITE['prod_host'] || $host === 'www.' . SITE['prod_host'];
}

/** Cache-busted asset URL. */
function asset(string $path): string
{
    $file = ROOT . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return $path . '?v=' . $v;
}

function tel_link(string $class = '', string $label = ''): string
{
    return '<a class="' . e($class) . '" href="tel:' . SITE['phone_href'] . '">' . ($label ?: e(SITE['phone'])) . '</a>';
}

/** Deterministic pseudo-random pick, so each city page always renders the same variant. */
function pick(array $options, string $seed, int $salt = 0)
{
    $i = crc32($seed . '|' . $salt) % count($options);
    return $options[$i];
}

function json_file(string $path): array
{
    static $cache = [];
    if (!isset($cache[$path])) {
        $cache[$path] = is_file($path) ? (json_decode((string) file_get_contents($path), true) ?: []) : [];
    }
    return $cache[$path];
}

/* ------------------------------------------------------------------ cities */

function cities(): array
{
    static $map = null;
    if ($map === null) {
        $map = [];
        foreach (json_file(ROOT . '/data/cities.json') as $c) {
            $map[$c['slug']] = $c;
        }
        $local = [];
        foreach (glob(ROOT . '/content/cities/*.json') ?: [] as $f) {
            $local += json_file($f);
        }
        foreach ($map as $slug => &$c) {
            $c['local'] = $local[$slug] ?? [];
        }
        unset($c);
    }
    return $map;
}

function city_url(string $slug): string
{
    return '/areas/' . $slug . '-insurance-appraiser/';
}

function city_image(array $c): string
{
    $f = '/assets/img/cities/' . $c['slug'] . '.webp';
    if (is_file(ROOT . $f)) {
        return $f;
    }
    return '/assets/img/site/' . (str_contains($c['region'], 'Gulf') ? 'Hurricane-Loss-Insurance.webp' : 'TX-Insurance-Appraiser-Background.webp');
}

/* ------------------------------------------------------------------- posts */

function posts(): array
{
    static $posts = null;
    if ($posts === null) {
        $posts = [];
        foreach (glob(ROOT . '/content/posts/*.json') ?: [] as $f) {
            $p = json_file($f);
            if (!empty($p['slug']) && !empty($p['body_html'])) {
                $posts[$p['slug']] = $p;
            }
        }
        uasort($posts, fn($a, $b) => strcmp($b['published'] ?? '', $a['published'] ?? ''));
    }
    return $posts;
}

function post_image(array $p): string
{
    $f = '/assets/img/blog/' . ($p['image'] ?? '');
    return (!empty($p['image']) && is_file(ROOT . $f)) ? $f : SITE['og_default'];
}

function reading_minutes(string $html): int
{
    return max(3, (int) round(str_word_count(strip_tags($html)) / 225));
}

function nice_date(string $iso): string
{
    $t = strtotime($iso);
    return $t ? date('F j, Y', $t) : '';
}

/* ------------------------------------------------------------------- icons */

function icon(string $name, int $size = 24): string
{
    static $paths = [
        'phone'    => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
        'mail'     => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        'clock'    => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'pin'      => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
        'scale'    => '<path d="M12 3v18M5 21h14M3 7h18M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
        'shield'   => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        'cube'     => '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
        'calc'     => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h4"/>',
        'doc'      => '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
        'gavel'    => '<path d="m14 13-7.5 7.5a2.1 2.1 0 0 1-3-3L11 10M16 16l6-6M8 8l6-6M9 7l8 8M21 11l-8-8"/>',
        'check'    => '<path d="M20 6 9 17l-5-5"/>',
        'arrow'    => '<path d="M5 12h14M12 5l7 7-7 7"/>',
        'star'     => '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
        'roof'     => '<path d="m2 12 10-8 10 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'percent'  => '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
        'calendar' => '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        'storm'    => '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.2"/><path d="m13 11-4 6h6l-4 6"/>',
        'wind'     => '<path d="M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2M17.5 8a2.5 2.5 0 1 1 2 4H2"/>',
        'flame'    => '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.4 1.4 1.4 2.5 2.5 2.8z"/>',
        'drop'     => '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5S12.5 5.5 12 2.5c-.5 3-2 5.4-4 7S5 13 5 15a7 7 0 0 0 7 7z"/>',
        'snow'     => '<path d="M2 12h20M12 2v20M20 16l-4-4 4-4M4 8l4 4-4 4M16 4l-4 4-4-4M8 20l4-4 4 4"/>',
        'building' => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
        'home'     => '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
        'search'   => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        'users'    => '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
        'camera'   => '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
        'chat'     => '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
        'menu'     => '<path d="M3 12h18M3 6h18M3 18h18"/>',
        'x'        => '<path d="M18 6 6 18M6 6l12 12"/>',
        'chev'     => '<path d="m6 9 6 6 6-6"/>',
        'hail'     => '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.2"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="21" r="1"/><circle cx="16" cy="19" r="1"/>',
        'award'    => '<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>',
        'map'      => '<path d="m1 6 7-4 8 4 7-4v16l-7 4-8-4-7 4z"/><path d="M8 2v16M16 6v16"/>',
        'zap'      => '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    ];
    $p = $paths[$name] ?? $paths['check'];
    return '<svg class="ico" width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}
