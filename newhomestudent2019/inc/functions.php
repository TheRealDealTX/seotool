<?php defined('NHS') || exit;

function e(?string $s): string { return htmlspecialchars($s ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function url(string $path = '/'): string { return SITE['origin'] . $path; }

function asset(string $path): string {
    $file = APP_ROOT . '/assets/' . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return '/assets/' . $path . '?v=' . $v;
}

function redirect(string $to, int $code = 301): never {
    // Root-relative Location keeps preview hosts on themselves; production host is enforced in index.php.
    header('Location: ' . $to, true, $code);
    exit;
}

function human_date(string $ymd): string { return date('F j, Y', strtotime($ymd)); }

function reading_minutes(string $html): int {
    return max(3, (int) round(str_word_count(strip_tags($html)) / 230));
}

/* ---------- Posts ---------- */

function post_slugs(): array {
    static $slugs = null;
    if ($slugs === null) {
        $slugs = [];
        foreach (glob(APP_ROOT . '/content/posts/*.php') as $f) $slugs[] = basename($f, '.php');
    }
    return $slugs;
}

function get_post(string $slug): ?array {
    static $cache = [];
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) return null;
    if (array_key_exists($slug, $cache)) return $cache[$slug];
    $file = APP_ROOT . '/content/posts/' . $slug . '.php';
    if (!is_file($file)) return $cache[$slug] = null;
    $p = require $file;
    if (!is_array($p)) return $cache[$slug] = null;
    $p['slug'] = $slug;
    $p['url'] = '/' . $slug . '/';
    $p += ['updated' => $p['date'] ?? '', 'faq' => [], 'excerpt' => '', 'image_alt' => $p['title'] ?? ''];
    $img = '/assets/img/posts/' . $slug . '.webp';
    $p['image'] = is_file(APP_ROOT . $img) ? $img : null;
    return $cache[$slug] = $p;
}

/** All posts, newest first. */
function all_posts(): array {
    static $all = null;
    if ($all === null) {
        $all = array_values(array_filter(array_map('get_post', post_slugs())));
        usort($all, fn($a, $b) => strcmp($b['date'], $a['date']) ?: strcmp($a['slug'], $b['slug']));
    }
    return $all;
}

function posts_in(string $cat): array {
    return array_values(array_filter(all_posts(), fn($p) => ($p['category'] ?? '') === $cat));
}

/** Related posts: same category first, then most recent, excluding the current one. */
function related_posts(array $post, int $n = 3): array {
    $same = array_filter(posts_in($post['category']), fn($p) => $p['slug'] !== $post['slug']);
    // Prefer posts this one does not already link to heavily; keep deterministic order by slug hash.
    usort($same, fn($a, $b) => crc32($post['slug'] . $a['slug']) <=> crc32($post['slug'] . $b['slug']));
    $out = array_slice($same, 0, $n);
    if (count($out) < $n) {
        foreach (all_posts() as $p) {
            if (count($out) >= $n) break;
            if ($p['slug'] !== $post['slug'] && !in_array($p, $out, true)) $out[] = $p;
        }
    }
    return $out;
}

/* ---------- Content rendering ---------- */

/** Expand product markers and harden outbound links in article HTML. */
function render_body(string $html): string {
    // <!--products:key1,key2|Heading-->
    $html = preg_replace_callback('/<!--products:([a-z0-9_,\s]+)(?:\|(.*?))?-->/', function ($m) {
        $keys = array_filter(array_map('trim', explode(',', $m[1])));
        return product_grid($keys, isset($m[2]) ? trim($m[2]) : '');
    }, $html);
    // <!--product:key-->
    $html = preg_replace_callback('/<!--product:([a-z0-9_]+)-->/', fn($m) => product_grid([$m[1]]), $html);
    // [[amz:key|anchor]]
    $html = preg_replace_callback('/\[\[amz:([a-z0-9_]+)\|(.*?)\]\]/', function ($m) {
        $p = product($m[1]);
        if (!$p) return $m[2];
        return '<a href="' . e($p['url']) . '" rel="sponsored nofollow noopener" target="_blank" class="amz-inline">' . $m[2] . '</a>';
    }, $html);
    // External links: open in new tab, noopener. Affiliate links already carry their own rel.
    $html = preg_replace_callback('/<a\s+href="(https?:\/\/[^"]+)"(?![^>]*\brel=)([^>]*)>/i', function ($m) {
        $host = parse_url(html_entity_decode($m[1]), PHP_URL_HOST) ?: '';
        if ($host === parse_url(SITE['origin'], PHP_URL_HOST)) return $m[0];
        return '<a href="' . $m[1] . '"' . $m[2] . ' target="_blank" rel="noopener">';
    }, $html);
    // Wrap tables for horizontal scroll on phones.
    $html = preg_replace('/<table>(.*?)<\/table>/s', '<div class="table-wrap"><table>$1</table></div>', $html);
    return $html;
}

/** Build a table of contents from h2s and add ids to them. Returns [html, toc]. */
function add_toc(string $html): array {
    $toc = [];
    $used = [];
    $html = preg_replace_callback('/<h2>(.*?)<\/h2>/s', function ($m) use (&$toc, &$used) {
        $text = trim(strip_tags($m[1]));
        $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(html_entity_decode($text))), '-') ?: 'section';
        $base = $id; $i = 2;
        while (isset($used[$id])) $id = $base . '-' . $i++;
        $used[$id] = true;
        $toc[] = [$id, $text];
        return '<h2 id="' . $id . '">' . $m[1] . '</h2>';
    }, $html);
    return [$html, $toc];
}

function has_affiliate_links(string $html): bool {
    return (bool) preg_match('/<!--products?:|\[\[amz:/', $html);
}

/* ---------- JSON-LD ---------- */

function org_schema(): array {
    return [
        '@type' => 'Organization',
        '@id' => url('/#organization'),
        'name' => SITE['name'],
        'url' => url('/'),
        'logo' => url('/assets/img/logo-512.png'),
        'email' => SITE['email'],
        'telephone' => SITE['phone_href'],
        'founder' => ['@id' => url('/author/jonathon/#person')],
    ];
}

function person_schema(): array {
    return [
        '@type' => 'Person',
        '@id' => url('/author/jonathon/#person'),
        'name' => SITE['author'],
        'url' => url('/author/jonathon/'),
        'worksFor' => ['@id' => url('/#organization')],
    ];
}

function breadcrumb_schema(array $crumbs): array {
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function faq_schema(array $faq): ?array {
    if (!$faq) return null;
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($q) => [
            '@type' => 'Question',
            'name' => $q[0],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $q[1]],
        ], $faq),
    ];
}

function json_ld(array $nodes): string {
    $graph = array_values(array_filter($nodes));
    return '<script type="application/ld+json">' .
        json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) .
        '</script>';
}

/* ---------- Small view helpers ---------- */

function post_card(array $p, bool $showCat = true): string {
    $cat = CATEGORIES[$p['category']]['name'] ?? '';
    $img = $p['image']
        ? '<img src="' . e($p['image']) . '" alt="' . e($p['image_alt']) . '" loading="lazy" width="600" height="338">'
        : '<span class="card-placeholder" aria-hidden="true">' . icon('house') . '</span>';
    return '<article class="card">'
        . '<a class="card-media" href="' . e($p['url']) . '" tabindex="-1" aria-hidden="true">' . $img . '</a>'
        . '<div class="card-body">'
        . ($showCat && $cat ? '<a class="eyebrow" href="/category/' . e($p['category']) . '/">' . e($cat) . '</a>' : '')
        . '<h3><a href="' . e($p['url']) . '">' . e($p['title']) . '</a></h3>'
        . '<p>' . e($p['excerpt']) . '</p>'
        . '<span class="meta">' . e(human_date($p['updated'])) . ' · ' . reading_minutes($p['body']) . ' min read</span>'
        . '</div></article>';
}

function pagination(int $page, int $pages, string $base): string {
    if ($pages <= 1) return '';
    $h = '<nav class="pagination" aria-label="Pagination">';
    if ($page > 1) $h .= '<a href="' . e($page === 2 ? $base : $base . 'page/' . ($page - 1) . '/') . '" rel="prev">&larr; Newer</a>';
    $h .= '<span>Page ' . $page . ' of ' . $pages . '</span>';
    if ($page < $pages) $h .= '<a href="' . e($base . 'page/' . ($page + 1) . '/') . '" rel="next">Older &rarr;</a>';
    return $h . '</nav>';
}

function icon(string $name): string {
    static $paths = [
        'house'   => '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'book'    => '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6"/>',
        'tool'    => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
        'chip'    => '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
        'shield'  => '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
        'bolt'    => '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        'sofa'    => '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M2 13a2 2 0 0 1 4 0v2h12v-2a2 2 0 0 1 4 0v5H2z"/><path d="M5 18v2M19 18v2"/>',
        'leaf'    => '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
        'box'     => '<path d="M3 7 12 3l9 4-9 4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>',
        'paw'     => '<circle cx="7" cy="9" r="2"/><circle cx="12" cy="6" r="2"/><circle cx="17" cy="9" r="2"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5c0 2-2 2-4 2s-4 0-4-2z"/>',
        'chart'   => '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        'check'   => '<path d="m5 12 5 5 9-10"/>',
        'phone'   => '<path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A18 18 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
        'mail'    => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'play'    => '<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',
        'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'clip'    => '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h4"/>',
    ];
    $p = $paths[$name] ?? $paths['house'];
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}
