<?php
// Shared setup: config, catalog, helpers. Included by index.php and search.php.
defined('GAP') || exit;

$CFG = require __DIR__ . '/config.php';
$CAT = require dirname(__DIR__) . '/data/catalog.php';
$AFF = is_file(dirname(__DIR__) . '/data/affiliates.json')
    ? (json_decode(file_get_contents(dirname(__DIR__) . '/data/affiliates.json'), true) ?: []) : [];

const ASSET_V = '1';

function e(?string $s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

// Paragraph text from the content files: escaped, except internal <a href="/x/">links</a>.
function rich(string $s): string {
    $s = e($s);
    return preg_replace('#&lt;a href=&quot;(/[A-Za-z0-9\-/]*)&quot;&gt;(.*?)&lt;/a&gt;#', '<a href="$1">$2</a>', $s);
}

function abs_url(string $path): string { global $CFG; return rtrim($CFG['origin'], '/') . $path; }
function money(int $n): string { return '$' . number_format($n); }
function kind_img(string $kind): string { return '/assets/img/kinds/' . preg_replace('/[^a-z\-]/', '', $kind) . '.svg'; }
function product(string $path): ?array { global $CAT; return $CAT['products'][$path] ?? null; }
function category(string $path): ?array { global $CAT; return $CAT['categories'][$path] ?? null; }

function aff_url(array $p): string {
    global $CFG, $AFF;
    if (!empty($AFF[$p['path']])) return $AFF[$p['path']];
    $u = str_replace('{q}', rawurlencode($p['name']), $CFG['affiliate_fallback']);
    if ($CFG['amazon_tag'] && str_contains($u, 'amazon.')) $u .= (str_contains($u, '?') ? '&' : '?') . 'tag=' . rawurlencode($CFG['amazon_tag']);
    return $u;
}

// Breadcrumb trail of [label, path] for a category path (inclusive).
function cat_trail(string $path): array {
    global $CAT;
    $t = [];
    for ($q = $path; $q && isset($CAT['categories'][$q]); $q = $CAT['categories'][$q]['parent']) {
        array_unshift($t, [$CAT['categories'][$q]['name'], $q]);
    }
    return $t;
}

function redirect(string $to, int $code = 301): never {
    header('Location: ' . $to, true, $code);
    exit;
}

// Picks products for a listing, most-searched first.
function pick(array $paths, int $n = 0, array $exclude = []): array {
    $out = [];
    foreach ($paths as $p) if (!in_array($p, $exclude, true) && ($x = product($p))) $out[] = $x;
    return $n ? array_slice($out, 0, $n) : $out;
}

// Fuzzy match an old-platform slug ("Arbortec-Scafell-Lite-Chainsaw-Boots") to a page.
function fuzzy_target(string $text): string {
    global $CAT;
    $tok = fn(string $s) => array_values(array_filter(preg_split('/[^a-z0-9]+/', strtolower($s)), fn($w) => strlen($w) > 1 && !in_array($w, ['image', 'item', 'folder', 'shop', 'product', 'size', 'thumbnail', 'the', 'and', 'for', 'with'], true)));
    $want = array_unique($tok($text));
    if (!$want) return '/shop-all/';
    $best = ['/shop-all/', 0.0];
    foreach (['products', 'categories'] as $set) {
        foreach ($CAT[$set] as $path => $x) {
            $have = array_unique(array_merge($tok($path), $tok($x['name'])));
            $hit = count(array_intersect($want, $have));
            $score = $hit / max(count($want), 1) - ($set === 'categories' ? 0.05 : 0);
            if ($hit >= 2 && $score > $best[1]) $best = [$path, $score];
        }
    }
    return $best[1] >= 0.5 ? $best[0] : '/shop-all/';
}

function search_catalog(string $q, int $limit = 60): array {
    global $CAT;
    $words = array_filter(preg_split('/\s+/', strtolower(trim($q))), fn($w) => $w !== '');
    if (!$words) return [];
    $hits = [];
    foreach ($CAT['products'] as $path => $p) {
        $hay = strtolower($p['name'] . ' ' . ($p['brand_name'] ?? '') . ' ' . ($p['keyword'] ?? '') . ' ' . ($p['tagline'] ?? '') . ' ' . str_replace('-', ' ', $path));
        $score = 0;
        foreach ($words as $w) {
            $w2 = rtrim($w, 's');
            if (str_contains(strtolower($p['name']), $w2)) $score += 3;
            elseif (str_contains($hay, $w2)) $score += 1;
            else { $score = 0; break; }
        }
        if ($score) $hits[] = [$score, $p];
    }
    usort($hits, fn($a, $b) => $b[0] <=> $a[0]);
    return array_slice(array_column($hits, 1), 0, $limit);
}

// Render a view inside the layout. $meta: title, desc, canonical, jsonld[], noindex, body_class.
function render(string $view, array $vars = [], int $status = 200): never {
    global $CFG, $CAT;
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    extract($vars);
    ob_start();
    include __DIR__ . "/views/$view.php";
    $content = ob_get_clean();
    include __DIR__ . '/views/layout.php';
    exit;
}

// ---- small view partials ---------------------------------------------------------

function product_card(array $p, string $extra = ''): string {
    $img = kind_img($p['kind']);
    $data = e(json_encode(['p' => $p['path'], 'n' => $p['name'], 'pr' => $p['price'], 'k' => $p['kind']], JSON_UNESCAPED_SLASHES));
    return '<article class="card tilt reveal ' . $extra . '" data-product="' . $data . '" data-brand="' . e($p['brand'] ?? '') . '" data-price="' . (int)$p['price'] . '" data-name="' . e(strtolower($p['name'])) . '">'
        . '<a class="card-media" href="' . e($p['path']) . '" tabindex="-1" aria-hidden="true"><span class="rings"></span><img src="' . $img . '" alt="" loading="lazy" width="160" height="160"></a>'
        . '<button class="heart" type="button" aria-label="Save ' . e($p['name']) . '" data-save><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8 3.2 4 7 4c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6.1 4 4.6 7.7C19.5 16.4 12 21 12 21z"/></svg></button>'
        . '<div class="card-body"><p class="card-brand">' . e($p['brand_name'] ?? '') . '</p>'
        . '<h3 class="card-title"><a href="' . e($p['path']) . '">' . e($p['name']) . '</a></h3>'
        . '<p class="card-tag">' . e($p['tagline'] ?? '') . '</p>'
        . '<div class="card-foot"><span class="price"><small>Typical</small> ' . money((int)$p['price']) . '</span>'
        . '<span class="card-actions"><label class="compare-tog" title="Compare"><input type="checkbox" data-compare> <span>Compare</span></label>'
        . '<button class="btn btn-sm btn-cart" type="button" data-add>Add</button></span></div></div></article>';
}

function faq_block(array $faq, string $heading = 'Common questions'): string {
    if (!$faq) return '';
    $h = '<section class="faq reveal"><h2>' . e($heading) . '</h2>';
    foreach ($faq as $f) $h .= '<details><summary>' . e($f['q']) . '</summary><p>' . rich($f['a']) . '</p></details>';
    return $h . '</section>';
}

function sections_block(array $sections): string {
    $h = '';
    foreach ($sections as $s) {
        $h .= '<h2>' . e($s['h']) . '</h2>';
        foreach ($s['p'] ?? [] as $p) $h .= '<p>' . rich($p) . '</p>';
        if (!empty($s['list'])) { $h .= '<ul>'; foreach ($s['list'] as $li) $h .= '<li>' . rich($li) . '</li>'; $h .= '</ul>'; }
    }
    return $h;
}

function crumbs(array $trail): string {
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>';
    $last = count($trail) - 1;
    foreach ($trail as $i => [$label, $path]) {
        $h .= $i === $last ? '<li aria-current="page">' . e($label) . '</li>' : '<li><a href="' . e($path) . '">' . e($label) . '</a></li>';
    }
    return $h . '</ol></nav>';
}

function crumbs_ld(array $trail): array {
    $items = [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => abs_url('/')]];
    foreach ($trail as $i => [$label, $path]) $items[] = ['@type' => 'ListItem', 'position' => $i + 2, 'name' => $label, 'item' => abs_url($path)];
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function faq_ld(array $faq): ?array {
    if (!$faq) return null;
    return ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])]], $faq)];
}

// Interactive tools: slug => [name, blurb, kind, related kinds]
const TOOLS = [
    'climbing-kit-builder'    => ['Climbing Kit Builder', 'Pick your climbing system and budget, get a complete, compatible kit list you can add to your cart in one click.', 'saddle', ['saddle', 'rope', 'friction-device', 'lanyard', 'carabiner', 'helmet', 'throw-line', 'ascender']],
    'rigging-load-calculator' => ['Rigging Load Calculator', 'Estimate the weight of a log by species and size, see the shock load of a drop, and size your rope and sling with a working-load margin.', 'rigging-device', ['rigging-device', 'sling', 'rope', 'pulley']],
    'rope-length-calculator'  => ['Tree Height & Rope Length', 'Measure a tree from the ground with an angle and a distance, then see how much rope a doubled or single-line climb needs.', 'rope', ['rope', 'throw-line']],
    'fuel-mix-calculator'     => ['2-Stroke Fuel Mix Calculator', 'Exactly how much 2-stroke oil to add for any can size and ratio, in ounces and milliliters.', 'fluid', ['fluid', 'chainsaw', 'top-handle', 'power-tool', 'pole-saw']],
    'spark-plug-decoder'      => ['Spark Plug Decoder & Reader', 'Decode an NGK part number letter by letter, then diagnose your saw from the color of the plug tip.', 'spark-plug', ['spark-plug', 'parts']],
    'chain-file-finder'       => ['Chain & File Size Finder', 'Match chain pitch to the right round file and depth gauge, and estimate drive links for your bar length.', 'chain-bar', ['chain-bar', 'wrench-file', 'chainsaw', 'top-handle']],
];
