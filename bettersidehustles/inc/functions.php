<?php
// Helpers shared by every template.

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return preg_match('#^https?://#', $path) ? $path : SITE_URL . $path;
}

function asset(string $path): string
{
    return $path . '?v=' . ASSET_VERSION;
}

function nice_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

/* ---------------------------------------------------------------- content */

function content_path(string $slug): ?string
{
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) {
        return null;
    }
    foreach (['posts', 'pages'] as $dir) {
        $f = BASE_DIR . "/content/$dir/$slug.php";
        if (is_file($f)) {
            return $f;
        }
    }
    return null;
}

function content_load(string $slug): ?array
{
    static $cache = [];
    if (array_key_exists($slug, $cache)) {
        return $cache[$slug];
    }
    $f = content_path($slug);
    if (!$f) {
        return $cache[$slug] = null;
    }
    $c = include $f;
    $c['slug'] = $slug;
    $c['type'] = str_contains($f, '/content/posts/') ? 'post' : 'page';
    $c['url'] = "/$slug/";
    return $cache[$slug] = $c;
}

/** Every article, newest first. */
function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(BASE_DIR . '/content/posts/*.php') as $f) {
        $p = content_load(basename($f, '.php'));
        if ($p) {
            $posts[] = $p;
        }
    }
    usort($posts, fn($a, $b) => [$b['published'], $a['slug']] <=> [$a['published'], $b['slug']]);
    return $posts;
}

function all_pages(): array
{
    $pages = [];
    foreach (glob(BASE_DIR . '/content/pages/*.php') as $f) {
        $p = content_load(basename($f, '.php'));
        if ($p && empty($p['noindex'])) {
            $pages[] = $p;
        }
    }
    return $pages;
}

function category_slug(string $cat): string
{
    return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($cat)), '-');
}

function reading_minutes(string $html): int
{
    return max(1, (int) round(str_word_count(strip_tags($html)) / 230));
}

/* --------------------------------------------------------------- rendering */

/**
 * Turn stored body HTML into page HTML: shortcodes, heading ids, external
 * link attributes. Returns [html, toc] where toc is a list of [id, text].
 */
function render_body(string $html): array
{
    $html = preg_replace_callback('/\[\[tool:([a-z-]+)\]\]/', fn($m) => tool_html($m[1], 'inline'), $html);
    $html = preg_replace_callback('/\[\[gear:([a-z0-9,\s-]+)(?:\|([^\]]+))?\]\]/', function ($m) {
        return gear_box(array_map('trim', explode(',', $m[1])), $m[2] ?? null);
    }, $html);
    $html = preg_replace_callback('/\[\[amazon:([a-z0-9-]+)\|([^\]]+)\]\]/', function ($m) {
        $item = amazon_item($m[1]);
        return $item ? '<a class="amz" href="' . e(amazon_url($item[1])) . '" rel="sponsored nofollow noopener" target="_blank">' . e($m[2]) . '</a>' : e($m[2]);
    }, $html);
    $html = preg_replace_callback('/\[\[amazon-search:([^|\]]+)\|([^\]]+)\]\]/', function ($m) {
        return '<a class="amz" href="' . e(amazon_url($m[1])) . '" rel="sponsored nofollow noopener" target="_blank">' . e($m[2]) . '</a>';
    }, $html);

    // Wide tables scroll sideways on phones instead of breaking the layout.
    $html = preg_replace('/<table\b/', '<div class="table-wrap"><table', $html);
    $html = str_replace('</table>', '</table></div>', $html);

    // External links open in a new tab.
    $html = preg_replace_callback('/<a\s+href="(https?:\/\/(?!bettersidehustles\.com)[^"]+)"(?![^>]*\brel=)([^>]*)>/i', function ($m) {
        return '<a href="' . $m[1] . '"' . $m[2] . ' rel="noopener" target="_blank">';
    }, $html);

    $toc = [];
    $used = [];
    $html = preg_replace_callback('/<h2([^>]*)>(.*?)<\/h2>/is', function ($m) use (&$toc, &$used) {
        $attrs = $m[1];
        $text = trim(html_entity_decode(strip_tags($m[2]), ENT_QUOTES, 'UTF-8'));
        if (preg_match('/\bid="([^"]+)"/', $attrs, $idm)) {
            $id = $idm[1];
        } else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-') ?: 'section';
            $base = $id;
            for ($i = 2; isset($used[$id]); $i++) {
                $id = "$base-$i";
            }
            $attrs .= ' id="' . $id . '"';
        }
        $used[$id] = true;
        $toc[] = [$id, $text];
        return "<h2$attrs>{$m[2]}</h2>";
    }, $html);

    return [$html, $toc];
}

/* ------------------------------------------------------------------ amazon */

function amazon_catalog(): array
{
    static $cat = null;
    return $cat ??= require BASE_DIR . '/data/amazon.php';
}

function amazon_item(string $key): ?array
{
    return amazon_catalog()[$key] ?? null;
}

function amazon_url(string $query): string
{
    $GLOBALS['uses_amazon'] = true;
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . AMAZON_TAG;
}

function gear_box(array $keys, ?string $heading = null): string
{
    $cards = '';
    foreach ($keys as $k) {
        $it = amazon_item($k);
        if (!$it) {
            continue;
        }
        [$title, $q, $why, $ic] = $it;
        $cards .= '<a class="gear-card" href="' . e(amazon_url($q)) . '" rel="sponsored nofollow noopener" target="_blank">'
            . '<span class="gear-ic">' . icon($ic) . '</span>'
            . '<span class="gear-txt"><b>' . e($title) . '</b><span>' . e($why) . '</span></span>'
            . '<span class="gear-cta">View on Amazon ' . icon('arrow') . '</span></a>';
    }
    if ($cards === '') {
        return '';
    }
    return '<aside class="gear-box reveal"><div class="gear-head"><span class="pill">Recommended gear</span><h3>'
        . e($heading ?: 'Tools that make this side hustle easier') . '</h3></div><div class="gear-grid">' . $cards
        . '</div><p class="gear-note">Amazon affiliate links — we may earn a small commission at no extra cost to you.</p></aside>';
}

/* ------------------------------------------------------------------- icons */

function icon(string $name, string $class = 'ic'): string
{
    static $p = [
        'arrow'      => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'car'        => '<path d="M5 17h14M6 17v2M18 17v2M3 13l2-6h14l2 6v4H3z"/><circle cx="7.5" cy="14" r="1"/><circle cx="16.5" cy="14" r="1"/>',
        'camera'     => '<path d="M4 7h3l2-3h6l2 3h3v13H4z"/><circle cx="12" cy="13" r="4"/>',
        'bag'        => '<path d="M5 8h14l-1 13H6zM9 8V6a3 3 0 0 1 6 0v2"/>',
        'bolt'       => '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        'book'       => '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3"/><path d="M20 4v14h-7"/>',
        'box'        => '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
        'sun'        => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'mic'        => '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
        'headphones' => '<path d="M3 18v-6a9 9 0 0 1 18 0v6"/><rect x="3" y="14" width="4" height="7" rx="1"/><rect x="17" y="14" width="4" height="7" rx="1"/>',
        'pen'        => '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
        'laptop'     => '<rect x="4" y="4" width="16" height="11" rx="1"/><path d="M2 19h20"/>',
        'printer'    => '<path d="M6 9V3h12v6M6 18H4v-7h16v7h-2"/><rect x="6" y="14" width="12" height="7"/>',
        'scissors'   => '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
        'shirt'      => '<path d="M8 3 3 6l2 5 2-1v11h10V10l2 1 2-5-5-3a4 4 0 0 1-8 0z"/>',
        'sparkle'    => '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
        'drop'       => '<path d="M12 3s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/>',
        'wrench'     => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
        'leaf'       => '<path d="M11 20A7 7 0 0 1 4 13C4 7 10 4 20 4c0 10-3 16-9 16zM4 20c4-4 7-6 11-9"/>',
        'snow'       => '<path d="M12 2v20M4.9 7l14.2 10M19.1 7 4.9 17M9 4l3 2 3-2M9 20l3-2 3 2"/>',
        'paw'        => '<circle cx="5" cy="10" r="2"/><circle cx="9" cy="5" r="2"/><circle cx="15" cy="5" r="2"/><circle cx="19" cy="10" r="2"/><path d="M12 11c-3 0-6 4-6 7 0 2 2 3 3 3h6c1 0 3-1 3-3 0-3-3-7-6-7z"/>',
        'cards'      => '<rect x="3" y="6" width="11" height="15" rx="2"/><path d="M10 3h9a2 2 0 0 1 2 2v13"/>',
        'wave'       => '<path d="M2 12c2-2 4-2 6 0s4 2 6 0 4-2 6 0M2 17c2-2 4-2 6 0s4 2 6 0 4-2 6 0M2 7c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
        'calendar'   => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        'target'     => '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
        'chart'      => '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 6-7"/>',
        'receipt'    => '<path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
        'play'       => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9l5 3-5 3z"/>',
        'briefcase'  => '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
        'cart'       => '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12h11l2-8H6.2"/>',
        'link'       => '<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
        'pin'        => '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        'phone'      => '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>',
        'search'     => '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
        'menu'       => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close'      => '<path d="M6 6l12 12M18 6 6 18"/>',
        'check'      => '<path d="M4 12l5 5L20 6"/>',
        'clock'      => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'dollar'     => '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
        'chev'       => '<path d="M6 9l6 6 6-6"/>',
        'mail'       => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        'rocket'     => '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2M9 12a12 12 0 0 1 11-9 12 12 0 0 1-9 11l-2 1-2-2z"/><circle cx="15" cy="9" r="1.5"/>',
        'users'      => '<circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6M16 4a3.5 3.5 0 0 1 0 7M18 15c2.5.5 4 2.5 4 6"/>',
        'globe'      => '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
        'shield'     => '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    ];
    return '<svg class="' . $class . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . ($p[$name] ?? $p['dollar']) . '</svg>';
}

/* ------------------------------------------------------------------ schema */

function schema_org(): array
{
    return [
        '@type' => 'Organization',
        '@id' => SITE_URL . '/#org',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'logo' => ['@type' => 'ImageObject', 'url' => abs_url(SITE_ORG_LOGO), 'width' => 827, 'height' => 827],
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => SITE_URL . '/#website',
        'url' => SITE_URL . '/',
        'name' => SITE_NAME,
        'description' => SITE_TAGLINE,
        'publisher' => ['@id' => SITE_URL . '/#org'],
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => SITE_URL . '/blog/?q={search_term_string}',
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $url]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($url)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faq): ?array
{
    $faq = array_filter($faq, fn($f) => !empty($f['q']) && !empty($f['a']));
    if (!$faq) {
        return null;
    }
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_values(array_map(fn($f) => [
            '@type' => 'Question',
            'name' => strip_tags($f['q']),
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])],
        ], $faq)),
    ];
}

function json_ld(array $graph): string
{
    $graph = array_values(array_filter($graph));
    return '<script type="application/ld+json">'
        . json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG)
        . '</script>';
}

/* --------------------------------------------------------------- partials */

function post_card(array $p, bool $lazy = true): string
{
    $img = $p['image'] ?? SITE_IMAGE;
    return '<article class="card post-card reveal" data-cat="' . e(category_slug($p['category'] ?? 'Guides')) . '" data-title="' . e(strtolower($p['h1'] . ' ' . ($p['city'] ?? ''))) . '">'
        . '<a href="' . e($p['url']) . '" class="card-img"><img src="' . e($img) . '" alt="' . e($p['image_alt'] ?? $p['h1']) . '" width="600" height="400"' . ($lazy ? ' loading="lazy" decoding="async"' : '') . '></a>'
        . '<div class="card-body"><span class="pill">' . e($p['category'] ?? 'Guides') . '</span>'
        . '<h3><a href="' . e($p['url']) . '">' . e($p['h1']) . '</a></h3>'
        . '<p>' . e(mb_strimwidth($p['description'], 0, 120, '…')) . '</p>'
        . '<span class="card-meta">' . icon('clock') . reading_minutes($p['body']) . ' min read</span></div></article>';
}

function render(string $template, array $vars = []): void
{
    extract($vars);
    require BASE_DIR . "/inc/templates/$template.php";
}

function not_found(): void
{
    http_response_code(404);
    render('404', ['page' => [
        'title' => 'Page Not Found | ' . SITE_NAME,
        'description' => 'That page does not exist. Browse side hustle guides, city guides and free calculators instead.',
        'url' => '/404/',
        'noindex' => true,
    ]]);
}
