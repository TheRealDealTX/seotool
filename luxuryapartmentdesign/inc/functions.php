<?php
// Content loading, rendering helpers and schema builders.

function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function url(string $path = '/'): string
{
    return SITE_ORIGIN . $path;
}

function asset(string $path): string
{
    return '/assets/' . ltrim($path, '/') . '?v=' . ASSET_VER;
}

function img_url(string $stem, bool $small = false): string
{
    return '/assets/img/articles/' . $stem . ($small ? '-600' : '') . '.webp';
}

function fmt_date(string $ymd): string
{
    $t = strtotime($ymd);
    return $t ? date('F j, Y', $t) : $ymd;
}

// Where form submissions are written. Prefers a folder outside public_html.
function data_dir(): string
{
    $outside = dirname(__DIR__, 2) . '/lad-data';
    if (is_dir($outside) || @mkdir($outside, 0750, true)) {
        if (is_writable($outside)) {
            return $outside;
        }
    }
    $inside = dirname(__DIR__) . '/data';
    if (!is_dir($inside)) {
        @mkdir($inside, 0750, true);
    }
    return $inside;
}

// --------------------------------------------------------------------------
// Content
// --------------------------------------------------------------------------

function content_dir(string $type): string
{
    return dirname(__DIR__) . '/content/' . $type;
}

/** All articles keyed by slug, newest first. */
function articles(): array
{
    static $all = null;
    if ($all !== null) {
        return $all;
    }
    $all = [];
    foreach (glob(content_dir('articles') . '/*.json') as $file) {
        $meta = json_decode(file_get_contents($file), true);
        if (!is_array($meta) || empty($meta['slug'])) {
            continue;
        }
        $body = content_dir('articles') . '/' . $meta['slug'] . '.html';
        if (!is_file($body)) {
            continue;
        }
        $meta['words'] = str_word_count(strip_tags(file_get_contents($body)));
        $meta['minutes'] = max(1, (int) round($meta['words'] / 230));
        $all[$meta['slug']] = $meta;
    }
    uasort($all, fn($a, $b) => [$b['updated'] ?? '', $b['published'] ?? ''] <=> [$a['updated'] ?? '', $a['published'] ?? '']);
    return $all;
}

function article(string $slug): ?array
{
    return articles()[$slug] ?? null;
}

function article_body(string $slug): string
{
    return file_get_contents(content_dir('articles') . '/' . $slug . '.html');
}

function articles_in(string $category): array
{
    return array_filter(articles(), fn($a) => ($a['category'] ?? '') === $category);
}

function tool(string $slug): ?array
{
    if (!isset(TOOLS[$slug])) {
        return null;
    }
    $file = content_dir('tools') . '/' . $slug . '.json';
    $meta = is_file($file) ? (json_decode(file_get_contents($file), true) ?: []) : [];
    return array_merge([
        'slug' => $slug,
        'title' => TOOLS[$slug]['name'],
        'h1' => TOOLS[$slug]['name'],
        'description' => TOOLS[$slug]['short'],
        'intro' => '',
        'faq' => [],
        'related' => [],
        'how_to' => [],
    ], $meta, TOOLS[$slug]);
}

function tool_body(string $slug): string
{
    $file = content_dir('tools') . '/' . $slug . '.html';
    return is_file($file) ? file_get_contents($file) : '';
}

/**
 * Give every <h2> in an article body an id and return [html, toc].
 */
function add_heading_ids(string $html): array
{
    $toc = [];
    $seen = [];
    $html = preg_replace_callback('#<h2([^>]*)>(.*?)</h2>#s', function ($m) use (&$toc, &$seen) {
        $text = trim(html_entity_decode(strip_tags($m[2]), ENT_QUOTES, 'UTF-8'));
        if (preg_match('/id="([^"]+)"/', $m[1], $idm)) {
            $id = $idm[1];
            $attrs = $m[1];
        } else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-') ?: 'section';
            $id = substr($id, 0, 60);
            $base = $id;
            $n = 2;
            while (isset($seen[$id])) {
                $id = $base . '-' . $n++;
            }
            $attrs = $m[1] . ' id="' . $id . '"';
        }
        $seen[$id] = true;
        $toc[] = [$id, $text];
        return '<h2' . $attrs . '>' . $m[2] . '</h2>';
    }, $html);
    return [$html, $toc];
}

// --------------------------------------------------------------------------
// Schema
// --------------------------------------------------------------------------

function schema_org(): array
{
    return [
        '@type' => 'Organization',
        '@id' => url('/#organization'),
        'name' => SITE_NAME,
        'url' => url('/'),
        'logo' => [
            '@type' => 'ImageObject',
            'url' => url('/assets/img/logo.webp'),
            'width' => 600,
            'height' => 191,
        ],
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => url('/#website'),
        'url' => url('/'),
        'name' => SITE_NAME,
        'description' => SITE_TAGLINE,
        'publisher' => ['@id' => url('/#organization')],
        'inLanguage' => 'en-US',
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => ['@type' => 'EntryPoint', 'urlTemplate' => url('/search/?q={search_term_string}')],
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach (array_values($crumbs) as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faq): ?array
{
    if (!$faq) {
        return null;
    }
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ], $faq),
    ];
}

function schema_graph(array $nodes): string
{
    $nodes = array_values(array_filter(array_merge([schema_org(), schema_website()], $nodes)));
    $json = json_encode(['@context' => 'https://schema.org', '@graph' => $nodes], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    return '<script type="application/ld+json">' . str_replace('</', '<\/', $json) . '</script>';
}

// --------------------------------------------------------------------------
// Small UI pieces
// --------------------------------------------------------------------------

function icon(string $name): string
{
    $p = [
        'sparkle' => '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
        'palette' => '<path d="M12 3a9 9 0 100 18c1.1 0 1.6-.8 1.6-1.6 0-.5-.2-.9-.5-1.2-.3-.3-.5-.7-.5-1.2 0-.9.7-1.6 1.6-1.6H16a5 5 0 005-5c0-4-4-7.4-9-7.4z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
        'rug' => '<rect x="4" y="5" width="16" height="14" rx="1"/><rect x="7.5" y="8.5" width="9" height="7"/><path d="M4 8H2M4 12H2M4 16H2M22 8h-2M22 12h-2M22 16h-2"/>',
        'frame' => '<rect x="4" y="6" width="16" height="14" rx="1"/><path d="M9 6l3-3 3 3"/><path d="M7 17l4-5 3 3 2-2 2 4"/>',
        'layout' => '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 10h8v11M11 14h10"/>',
        'roller' => '<rect x="3" y="3" width="15" height="6" rx="1"/><path d="M18 6h3v5h-9v3"/><rect x="10.5" y="14" width="3" height="7" rx="1"/>',
        'bulb' => '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 00-3.6 10.8c.6.5 1 1.2 1.1 2.2h5c.1-1 .5-1.7 1.1-2.2A6 6 0 0012 3z"/>',
        'curtain' => '<path d="M3 3h18"/><path d="M5 3c0 6 1 12 4 18H5zM19 3c0 6-1 12-4 18h4z"/>',
        'budget' => '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/><circle cx="16" cy="14.5" r="1.5"/>',
        'search' => '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
        'menu' => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close' => '<path d="M6 6l12 12M18 6L6 18"/>',
        'arrow' => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'check' => '<path d="M5 12l5 5 9-10"/>',
    ][$name] ?? '';
    return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' . $p . '</svg>';
}

function article_card(array $a, bool $large = false): string
{
    $cat = CATEGORIES[$a['category']]['name'] ?? '';
    $href = '/' . $a['slug'] . '/';
    return '<article class="card' . ($large ? ' card--large' : '') . '">'
        . '<a class="card__media" href="' . $href . '" tabindex="-1" aria-hidden="true">'
        . '<img src="' . img_url($a['image'], !$large) . '" alt="' . e($a['image_alt'] ?? $a['title']) . '" loading="lazy" decoding="async" width="600" height="400"></a>'
        . '<div class="card__body">'
        . '<a class="eyebrow" href="/category/' . e($a['category']) . '/">' . e($cat) . '</a>'
        . '<h3 class="card__title"><a href="' . $href . '">' . e($a['h1_short'] ?? $a['title']) . '</a></h3>'
        . '<p class="card__excerpt">' . e($a['excerpt'] ?? '') . '</p>'
        . '<span class="card__meta">' . icon('clock') . ' ' . $a['minutes'] . ' min read</span>'
        . '</div></article>';
}

function tool_card(string $slug): string
{
    $t = TOOLS[$slug];
    return '<a class="tool-card" href="/tools/' . $slug . '/">'
        . '<span class="tool-card__icon">' . icon($t['icon']) . '</span>'
        . '<span class="tool-card__name">' . e($t['name']) . '</span>'
        . '<span class="tool-card__short">' . e($t['short']) . '</span>'
        . '<span class="tool-card__go">Open tool ' . icon('arrow') . '</span></a>';
}

function faq_block(array $faq, string $heading = 'Frequently Asked Questions'): string
{
    if (!$faq) {
        return '';
    }
    $out = '<section class="faq" id="faq"><h2>' . e($heading) . '</h2>';
    foreach ($faq as $i => $f) {
        $out .= '<details class="faq__item"' . ($i === 0 ? ' open' : '') . '><summary>' . e($f['q']) . '</summary><p>' . e($f['a']) . '</p></details>';
    }
    return $out . '</section>';
}

function breadcrumbs_html(array $crumbs): string
{
    $out = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach (array_values($crumbs) as $i => [$name, $path]) {
        $out .= $i === $last
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

function newsletter_block(): string
{
    return '<section class="newsletter" aria-labelledby="nl-title"><div class="container newsletter__inner">'
        . '<div><p class="eyebrow">The Luxury Apartment Design Letter</p>'
        . '<h2 id="nl-title">One beautiful idea for your apartment, every other week</h2>'
        . '<p>Designer measurements, renter-friendly upgrades and new tools. No spam, unsubscribe anytime.</p></div>'
        . '<form class="newsletter__form" method="post" action="/subscribe/" data-ajax>'
        . '<label class="sr-only" for="nl-email">Email address</label>'
        . '<input id="nl-email" type="email" name="email" placeholder="you@example.com" required autocomplete="email">'
        . '<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
        . '<button class="btn btn--gold" type="submit">Subscribe</button>'
        . '<p class="form-status" role="status" aria-live="polite"></p>'
        . '</form></div></section>';
}
