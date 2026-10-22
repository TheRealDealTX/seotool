<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// Shared helpers: escaping, Amazon links, content loading, shortcodes and schema.

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

function abs_url(string $path): string
{
    return preg_match('#^https?://#', $path) ? $path : SITE_URL . $path;
}

function fmt_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

/** [width, height] of a local image (path from the site root), or [0, 0] if unknown. */
function img_dims(?string $path): array
{
    static $cache = [];
    if (!$path || preg_match('#^https?://#', $path)) {
        return [0, 0];
    }
    return $cache[$path] ??= (($s = @getimagesize(ROOT . $path)) ? [$s[0], $s[1]] : [0, 0]);
}

// ---------------------------------------------------------------- Amazon

function product(string $key): array
{
    if (!isset(PRODUCTS[$key])) {
        throw new RuntimeException("Unknown product key: $key");
    }
    return PRODUCTS[$key] + ['key' => $key];
}

/** Tagged Amazon URL for a catalog product (direct /dp/ link, or a tagged search). */
function amz_url(string $key): string
{
    $p = product($key);
    if (!empty($p['asin'])) {
        return 'https://www.amazon.com/dp/' . $p['asin'] . '/?tag=' . AMAZON_TAG;
    }
    return amz_search_url($p['search'] ?? $p['name']);
}

function amz_search_url(string $query): string
{
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . AMAZON_TAG;
}

/** Attributes every affiliate link carries (Google requires rel=sponsored on paid links). */
function amz_attrs(): string
{
    return 'target="_blank" rel="sponsored nofollow noopener"';
}

function amz_link(string $key, ?string $text = null): string
{
    $text ??= product($key)['name'];
    return '<a class="amz" href="' . e(amz_url($key)) . '" ' . amz_attrs() . '>' . e($text) . '</a>';
}

function amz_button(string $key, string $label = 'Check Price on Amazon', string $extra = ''): string
{
    return '<a class="btn btn-amz ' . e($extra) . '" href="' . e(amz_url($key)) . '" ' . amz_attrs() . '>' . e($label) . ' <span aria-hidden="true">&rarr;</span></a>';
}

function thumb(?string $img): ?string
{
    if (!$img) {
        return null;
    }
    $t = '/assets/img/thumbs/' . basename($img);
    return is_file(ROOT . $t) ? $t : $img;
}

function product_card(string $key, int $rank = 0): string
{
    $p = product($key);
    $img = thumb($p['image']);
    $type = PRODUCT_TYPES[$p['type']] ?? '';
    $h = '<div class="pcard">';
    if ($rank) {
        $h .= '<span class="pcard-rank">#' . $rank . '</span>';
    }
    if ($img) {
        $h .= '<a class="pcard-img" href="' . e(amz_url($key)) . '" ' . amz_attrs() . '><img src="' . e($img) . '" alt="' . e($p['name']) . ' under desk elliptical" loading="lazy" width="768" height="512"></a>';
    }
    $h .= '<div class="pcard-body"><p class="pcard-badge">' . e($p['best_for']) . '</p>';
    $h .= '<h3 class="pcard-title">' . e($p['name']) . '</h3>';
    $h .= '<p class="pcard-meta">' . e($type) . ($p['noise'] ? ' &middot; ' . e($p['noise']) : '') . '</p>';
    $h .= '<p>' . e($p['summary']) . '</p><div class="proscons"><ul class="pros">';
    foreach ($p['pros'] as $x) {
        $h .= '<li>' . e($x) . '</li>';
    }
    $h .= '</ul><ul class="cons">';
    foreach ($p['cons'] as $x) {
        $h .= '<li>' . e($x) . '</li>';
    }
    $h .= '</ul></div><div class="pcard-actions">' . amz_button($key);
    if (!empty($p['review']) && $p['review'] !== CURRENT_PATH) {
        $h .= ' <a class="btn btn-ghost" href="' . e($p['review']) . '">Read our guide</a>';
    }
    return $h . '</div></div></div>';
}

function compare_table(array $keys): string
{
    $h = '<div class="table-wrap"><table class="compare"><thead><tr><th>Model</th><th>Type</th><th>Best for</th><th>Noise</th><th>Seniors</th><th>Standing</th><th></th></tr></thead><tbody>';
    foreach ($keys as $k) {
        $p = product(trim($k));
        $h .= '<tr><td><strong>' . e($p['name']) . '</strong></td><td>' . e(PRODUCT_TYPES[$p['type']] ?? '') . '</td><td>' . e($p['best_for']) . '</td><td>' . e($p['noise'] ?? '—') . '</td><td>' . ($p['seniors'] ? '✔' : '—') . '</td><td>' . ($p['standing'] ? '✔' : '✘') . '</td><td>' . amz_button($p['key'], 'View', 'btn-sm') . '</td></tr>';
    }
    return $h . '</tbody></table></div>';
}

// ---------------------------------------------------------------- shortcodes

/**
 * Expands the shortcodes used in post bodies:
 *   [[amazon:key]] / [[amazon:key|anchor]]   inline affiliate link
 *   [[button:key]] / [[button:key|label]]   affiliate button
 *   [[product:key]] / [[product:key|rank]]  product card
 *   [[compare:key1,key2,...]]               comparison table
 *   [[search:query|anchor]]                 tagged Amazon search link
 *   [[tool:name]]                           interactive tool widget
 *   [[toc]]                                 table of contents (auto-inserted otherwise)
 */
function render_shortcodes(string $html): string
{
    return preg_replace_callback('/\[\[(\w+):([^\]|]+)(?:\|([^\]]*))?\]\]/', function ($m) {
        [$all, $code, $arg] = $m;
        // Option text is HTML in the source (authors write &amp;); decode it because the link builders escape.
        $opt = isset($m[3]) ? html_entity_decode($m[3], ENT_QUOTES | ENT_HTML5, 'UTF-8') : null;
        $arg = trim($arg);
        switch ($code) {
            case 'amazon':  return amz_link($arg, $opt ?: null);
            case 'button':  return '<p class="cta-line">' . amz_button($arg, $opt ?: 'Check Price on Amazon') . '</p>';
            case 'product': return product_card($arg, (int) $opt);
            case 'compare': return compare_table(explode(',', $arg));
            case 'search':  return '<a class="amz" href="' . e(amz_search_url($arg)) . '" ' . amz_attrs() . '>' . e($opt ?: $arg) . '</a>';
            case 'tool':    return tool_widget($arg);
        }
        return $all;
    }, $html);
}

/** Adds id attributes to h2/h3 and returns [html, toc entries]. */
function add_heading_ids(string $html): array
{
    $toc = [];
    $seen = [];
    $html = preg_replace_callback('#<h([23])(\s[^>]*)?>(.*?)</h\1>#s', function ($m) use (&$toc, &$seen) {
        $attrs = $m[2] ?? '';
        $text = trim(strip_tags($m[3]));
        if (preg_match('/\sid="([^"]+)"/', $attrs, $idm)) {
            $id = $idm[1];
        } else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(html_entity_decode($text))), '-');
            $base = $id;
            $n = 2;
            while (isset($seen[$id])) {
                $id = $base . '-' . $n++;
            }
            $attrs .= ' id="' . $id . '"';
        }
        $seen[$id] = true;
        if ($m[1] === '2') {
            $toc[] = [$id, $text];
        }
        return '<h' . $m[1] . $attrs . '>' . $m[3] . '</h' . $m[1] . '>';
    }, $html);
    return [$html, $toc];
}

function toc_html(array $toc): string
{
    if (count($toc) < 3) {
        return '';
    }
    $h = '<nav class="toc" aria-label="Table of contents"><details open><summary>In this guide</summary><ol>';
    foreach ($toc as [$id, $text]) {
        $h .= '<li><a href="#' . e($id) . '">' . e(html_entity_decode($text)) . '</a></li>';
    }
    return $h . '</ol></details></nav>';
}

// ---------------------------------------------------------------- content

/** All posts keyed by slug, newest first. Each post file returns an array. */
function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(ROOT . '/content/posts/*.php') as $f) {
        $slug = basename($f, '.php');
        $p = require $f;
        $p['slug'] = $slug;
        $p['url'] = '/' . $slug . '/';
        $p['updated'] ??= SITE_UPDATED;
        $p['tags'] ??= [];
        $posts[$slug] = $p;
    }
    uasort($posts, fn($a, $b) => [$b['featured'] ?? 0, $b['published']] <=> [$a['featured'] ?? 0, $a['published']]);
    return $posts;
}

/** Card for a post. $h is the heading level: 2 on archive pages (cards sit right under the H1), 3 in sub-sections. */
function post_card(array $p, int $h = 3): string
{
    $img = thumb($p['image'] ?? null) ?? DEFAULT_IMAGE;
    $cat = CATEGORIES[$p['category']][0] ?? '';
    return '<article class="card" data-cat="' . e($p['category']) . '"><a href="' . e($p['url']) . '" class="card-img"><img src="' . e($img) . '" alt="' . e($p['image_alt'] ?? $p['h1']) . '" loading="lazy" width="768" height="512"></a><div class="card-body"><p class="card-cat">' . e($cat) . '</p><h' . $h . ' class="card-title"><a href="' . e($p['url']) . '">' . e($p['h1']) . '</a></h' . $h . '><p>' . e($p['excerpt'] ?? $p['description']) . '</p></div></article>';
}

function related_posts(array $post, int $n = 3): array
{
    $scores = [];
    $words = array_filter(explode(' ', strtolower($post['keyword'] ?? '')), fn($w) => strlen($w) > 3 && !in_array($w, ['under', 'desk', 'elliptical']));
    foreach (all_posts() as $slug => $p) {
        if ($slug === $post['slug']) {
            continue;
        }
        $s = 0;
        if (in_array($slug, $post['related'] ?? [])) {
            $s += 10;
        }
        if ($p['category'] === $post['category']) {
            $s += 2;
        }
        $s += count(array_intersect($p['tags'], $post['tags']));
        foreach ($words as $w) {
            if (str_contains(strtolower($p['keyword'] ?? ''), $w)) {
                $s += 2;
            }
        }
        $scores[$slug] = $s + (crc32($slug . $post['slug']) % 100) / 1000;
    }
    arsort($scores);
    return array_map(fn($s) => all_posts()[$s], array_slice(array_keys($scores), 0, $n));
}

// ---------------------------------------------------------------- schema

function schema_org(): array
{
    return [
        '@type' => 'Organization', '@id' => SITE_URL . '/#org', 'name' => SITE_NAME, 'url' => SITE_URL . '/',
        'logo' => ['@type' => 'ImageObject', 'url' => abs_url(SITE_LOGO), 'width' => 1026, 'height' => 150],
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'name' => SITE_NAME, 'url' => SITE_URL . '/',
        'publisher' => ['@id' => SITE_URL . '/#org'],
        'potentialAction' => ['@type' => 'SearchAction', 'target' => SITE_URL . '/?s={search_term_string}', 'query-input' => 'required name=search_term_string'],
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
    return ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => [
        '@type' => 'Question', 'name' => $f['q'],
        'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])],
    ], $faq)];
}

function faq_html(array $faq, string $heading = 'Frequently Asked Questions'): string
{
    $h = '<section class="faq"><h2 id="faq">' . e($heading) . '</h2>';
    foreach ($faq as $f) {
        $h .= '<details><summary>' . e($f['q']) . '</summary><div>' . render_shortcodes($f['a']) . '</div></details>';
    }
    return $h . '</section>';
}

function breadcrumbs_html(array $crumbs): string
{
    $parts = [];
    foreach ($crumbs as $i => [$name, $url]) {
        $parts[] = $i === count($crumbs) - 1 ? '<span aria-current="page">' . e($name) . '</span>' : '<a href="' . e($url) . '">' . e($name) . '</a>';
    }
    return '<nav class="crumbs" aria-label="Breadcrumb">' . implode(' <span aria-hidden="true">/</span> ', $parts) . '</nav>';
}
