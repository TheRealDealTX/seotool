<?php
defined('ERE') or exit;

function cfg(?string $key = null)
{
    static $c = null;
    if ($c === null) {
        $c = require __DIR__ . '/config.php';
    }
    return $key === null ? $c : ($c[$key] ?? null);
}

function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return rtrim(cfg('url'), '/') . $path;
}

function asset(string $path): string
{
    $file = ROOT . '/assets/' . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return '/assets/' . $path . '?v=' . $v;
}

/* ------------------------------------------------------------------ posts */

function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(ROOT . '/content/posts/*.php') as $file) {
        $slug = basename($file, '.php');
        $p = require $file;
        if (!is_array($p) || empty($p['title'])) {
            continue;
        }
        $p['slug'] = $slug;
        $p['url'] = '/blog/' . $slug . '/';
        $p['updated'] = $p['updated'] ?? $p['date'];
        $words = str_word_count(strip_tags($p['body'] ?? ''));
        $p['words'] = $words;
        $p['read_minutes'] = max(3, (int) round($words / 230));
        $posts[$slug] = $p;
    }
    uasort($posts, fn($a, $b) => strcmp($b['date'] . $b['slug'], $a['date'] . $a['slug']));
    return $posts;
}

function get_post(string $slug): ?array
{
    return all_posts()[$slug] ?? null;
}

function posts_in(string $cat): array
{
    return array_filter(all_posts(), fn($p) => $p['category'] === $cat);
}

function category(string $slug): ?array
{
    $c = cfg('categories')[$slug] ?? null;
    if ($c) {
        $c['slug'] = $slug;
        $c['url'] = '/category/' . $slug . '/';
    }
    return $c;
}

function fmt_date(string $d): string
{
    return date('F j, Y', strtotime($d));
}

/* --------------------------------------------------------------- products */

function products(): array
{
    static $p = null;
    if ($p === null) {
        $p = require ROOT . '/content/products.php';
    }
    return $p;
}

function amazon_url(string $query): string
{
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . rawurlencode(cfg('amazon_tag'));
}

function product_card(string $key, bool $compact = false): string
{
    $p = products()[$key] ?? null;
    if (!$p) {
        return '';
    }
    [$name, $group, $blurb, $query] = $p;
    $url = amazon_url($query);
    $ic = icon(['storm' => 'cloud', 'safety' => 'shield', 'maintenance' => 'wrench', 'smart' => 'bolt', 'moving' => 'box', 'books' => 'book'][$group] ?? 'tag');
    return '<div class="product' . ($compact ? ' product--compact' : '') . '">'
        . '<div class="product__icon" aria-hidden="true">' . $ic . '</div>'
        . '<div class="product__body"><h3 class="product__name">' . e($name) . '</h3>'
        . '<p class="product__blurb">' . e($blurb) . '</p>'
        . '<a class="btn btn--amazon" href="' . e($url) . '" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a>'
        . '</div></div>';
}

/* ------------------------------------------------------------------ tools */

function tools(): array
{
    static $t = null;
    if ($t === null) {
        $t = require __DIR__ . '/tools.php';
        foreach ($t as $slug => &$tool) {
            $tool['slug'] = $slug;
            $tool['url'] = '/tools/' . $slug . '/';
        }
    }
    return $t;
}

function tool_card(string $slug, string $class = 'tool-card'): string
{
    $t = tools()[$slug] ?? null;
    if (!$t) {
        return '';
    }
    return '<a class="' . $class . '" href="' . $t['url'] . '">'
        . '<span class="tool-card__icon" aria-hidden="true">' . icon($t['icon']) . '</span>'
        . '<span class="tool-card__text"><strong>' . e($t['name']) . '</strong><span>' . e($t['short']) . '</span></span>'
        . '<span class="tool-card__go" aria-hidden="true">' . icon('arrow') . '</span></a>';
}

/* ------------------------------------------------------------ post bodies */

function render_body(string $html): string
{
    $html = preg_replace_callback('#(?:<p>\s*)?\[\[product:([a-z0-9-]+)\]\](?:\s*</p>)?#', fn($m) => product_card($m[1], true), $html);
    $html = preg_replace_callback('#(?:<p>\s*)?\[\[tool:([a-z0-9-]+)\]\](?:\s*</p>)?#', fn($m) => '<div class="callout callout--tool"><p class="callout__label">Free tool</p>' . tool_card($m[1]) . '</div>', $html);
    // Give every h2 an id for the table of contents.
    $html = preg_replace_callback('#<h2>(.*?)</h2>#s', function ($m) {
        $id = slugify(strip_tags($m[1]));
        return '<h2 id="' . $id . '">' . $m[1] . '</h2>';
    }, $html);
    // Responsive tables.
    $html = str_replace(['<table>', '</table>'], ['<div class="table-wrap"><table>', '</table></div>'], $html);
    // External links open in a new tab.
    $html = preg_replace('#<a href="(https?://(?!exitrealestate540\.com)[^"]+)"#', '<a href="$1" target="_blank" rel="noopener"', $html);
    return $html;
}

function toc(string $html): array
{
    preg_match_all('#<h2>(.*?)</h2>#s', $html, $m);
    $out = [];
    foreach ($m[1] as $h) {
        $t = trim(strip_tags($h));
        $out[] = [slugify($t), $t];
    }
    return $out;
}

function slugify(string $s): string
{
    $s = strtolower(html_entity_decode($s, ENT_QUOTES, 'UTF-8'));
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    return trim($s, '-');
}

/* ----------------------------------------------------------------- schema */

function schema_org(): array
{
    return [
        '@type' => 'Organization',
        '@id' => abs_url('/#organization'),
        'name' => cfg('name'),
        'url' => abs_url('/'),
        'logo' => ['@type' => 'ImageObject', 'url' => abs_url('/assets/img/logo-512.png'), 'width' => 512, 'height' => 512],
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => abs_url('/#website'),
        'url' => abs_url('/'),
        'name' => cfg('name'),
        'description' => cfg('description'),
        'publisher' => ['@id' => abs_url('/#organization')],
        'inLanguage' => 'en-US',
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

function schema_faq(array $faq): array
{
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => $f[0],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f[1]],
        ], $faq),
    ];
}

function json_ld(array $nodes): string
{
    $doc = ['@context' => 'https://schema.org', '@graph' => array_values($nodes)];
    return '<script type="application/ld+json">' . json_encode($doc, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>';
}

/* ------------------------------------------------------------------ icons */

function icon(string $name): string
{
    $paths = [
        'key'    => '<circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 20 3m-3 3 3 3m-6 0 2 2"/>',
        'tag'    => '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
        'chart'  => '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-6"/>',
        'home'   => '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'shield' => '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
        'pin'    => '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
        'calc'   => '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2m3 0h3M8 15h2m3 0h3M8 18h2m3 0h3"/>',
        'percent'=> '<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
        'scale'  => '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 0 0 6 0zm12 0-3 7a3 3 0 0 0 6 0z"/>',
        'doc'    => '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
        'cash'   => '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/>',
        'refresh'=> '<path d="M20 11a8 8 0 0 0-14.9-3M4 4v4h4M4 13a8 8 0 0 0 14.9 3M20 20v-4h-4"/>',
        'rocket' => '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2m-1.5-3.5L10 18l8-8c2-2 3-5 3-7-2 0-5 1-7 3z"/><path d="M14 6l4 4"/>',
        'cloud'  => '<path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9a4.5 4.5 0 0 0 1 9z"/><path d="m10 21 1-2m3 2 1-2"/>',
        'wrench' => '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 6.7-6.7a4 4 0 0 1-5-5z" transform="rotate(0)"/><path d="M3 21l6-6"/>',
        'bolt'   => '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        'box'    => '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
        'book'   => '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
        'fire'   => '<path d="M12 22a7 7 0 0 0 7-7c0-4-3-6-4-9-1 2-2 3-4 3 1-3 0-5-2-7 0 4-4 7-4 13a7 7 0 0 0 7 7z"/>',
        'check'  => '<path d="m5 12 5 5L20 7"/>',
        'arrow'  => '<path d="M5 12h14m-6-6 6 6-6 6"/>',
        'menu'   => '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'close'  => '<path d="M6 6l12 12M18 6 6 18"/>',
        'clock'  => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'mail'   => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'search' => '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
        'list'   => '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3 6 1 1 2-2M3 12l1 1 2-2M3 18l1 1 2-2"/>',
    ];
    $p = $paths[$name] ?? $paths['home'];
    return '<svg class="icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $p . '</svg>';
}

/* ----------------------------------------------------------------- photos */

/** Photo registry (content/images.php): slot => [alt, source, license, landing]. */
function photos(): array
{
    static $p = null;
    if ($p === null) {
        $f = ROOT . '/content/images.php';
        $p = is_file($f) ? require $f : [];
    }
    return $p;
}

function has_photo(string $slot): bool
{
    return isset(photos()[$slot]) && is_file(ROOT . '/assets/img/photos/' . $slot . '-1600.jpg');
}

function photo_url(string $slot, int $w = 1600, string $ext = 'jpg'): string
{
    return '/assets/img/photos/' . $slot . '-' . $w . '.' . $ext;
}

/**
 * Responsive <picture>. Every photo exists at 480/800/1200/1600 px wide in WebP and JPEG.
 * $sizes is the CSS sizes attribute; $eager for above-the-fold images.
 */
function picture(string $slot, string $sizes, string $class = '', bool $eager = false, ?string $alt = null): string
{
    if (!has_photo($slot)) {
        return '';
    }
    $alt = $alt ?? photos()[$slot]['alt'];
    $set = fn(string $ext) => implode(', ', array_map(fn($w) => photo_url($slot, $w, $ext) . ' ' . $w . 'w', [480, 800, 1200, 1600]));
    [$w, $h] = [1600, 900];
    return '<picture' . ($class ? ' class="' . e($class) . '"' : '') . '>'
        . '<source type="image/webp" srcset="' . $set('webp') . '" sizes="' . e($sizes) . '">'
        . '<img src="' . photo_url($slot, 800) . '" srcset="' . $set('jpg') . '" sizes="' . e($sizes) . '" width="' . $w . '" height="' . $h . '" alt="' . e($alt) . '"'
        . ($eager ? ' fetchpriority="high"' : ' loading="lazy"') . ' decoding="async">'
        . '</picture>';
}

/**
 * Append the short brand to a page title only when the result still fits in
 * Google's ~580px title width (kept to 60 characters).
 */
function brand_title(string $t): string
{
    $full = $t . ' | ' . cfg('short');
    return mb_strlen($full) <= 60 ? $full : $t;
}
