<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/icons.php';
require_once __DIR__ . '/tools.php';
require_once __DIR__ . '/products.php';
require_once ROOT . '/widgets/_lib.php';

function e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
function abs_url(string $path): string { return SITE_URL . ($path === '/' ? '/' : $path); }
function asset(string $p): string { return '/assets/' . $p . '?v=' . ASSET_VER; }

function photo(string $name, string $alt, string $cls = '', bool $lazy = true, string $sizes = '(max-width: 760px) 100vw, 760px'): string {
    $f = ROOT . '/assets/img/photos/' . $name . '.webp';
    [$w, $h] = is_file($f) ? (getimagesize($f) ?: [1200, 800]) : [1200, 800];
    return '<img src="/assets/img/photos/' . e($name) . '.webp" srcset="/assets/img/photos/' . e($name) . '-sm.webp 600w, /assets/img/photos/' . e($name) . '.webp 1200w" sizes="' . e($sizes) . '" width="' . $w . '" height="' . $h . '" alt="' . e($alt) . '"' . ($cls ? ' class="' . e($cls) . '"' : '') . ($lazy ? ' loading="lazy" decoding="async"' : ' fetchpriority="high"') . '>';
}

/* ---------- content loading ---------- */
function load_content(string $type, string $slug): ?array {
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) return null;
    $f = ROOT . "/content/$type/$slug.php";
    return is_file($f) ? (array) include $f : null;
}
function articles(): array {
    static $all = null;
    if ($all !== null) return $all;
    $all = [];
    foreach (glob(ROOT . '/content/articles/*.php') as $f) {
        $a = (array) include $f;
        $a['slug'] = $a['slug'] ?? basename($f, '.php');
        if (($a['date'] ?? '9999') > date('Y-m-d')) continue;   // scheduled
        $all[$a['slug']] = $a;
    }
    uasort($all, fn($x, $y) => strcmp($y['date'], $x['date']));
    return $all;
}
function word_count(string $html): int { return str_word_count(strip_tags($html)); }
function read_time(string $html): int { return max(1, (int) round(word_count($html) / 230)); }
function nice_date(string $d): string { return date('F j, Y', strtotime($d)); }

/* ---------- body processing ---------- */
function slugify(string $s): string { return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(strip_tags($s))), '-'); }

// Ensure every <h2> has an id; return [html, toc]
function add_heading_ids(string $html): array {
    $toc = [];
    $html = preg_replace_callback('#<h2([^>]*)>(.*?)</h2>#s', function ($m) use (&$toc) {
        $attrs = $m[1];
        if (preg_match('/id="([^"]+)"/', $attrs, $mm)) $id = $mm[1];
        else { $id = slugify($m[2]); $attrs .= ' id="' . $id . '"'; }
        $toc[] = [$id, trim(strip_tags($m[2]))];
        return "<h2$attrs>{$m[2]}</h2>";
    }, $html);
    return [$html, $toc];
}

function render_shortcodes(string $html): string {
    $html = preg_replace_callback('#(?:<p>\s*)?\[\[tool:([a-z0-9-]+)\]\](?:\s*</p>)?#', fn($m) => tool_cta($m[1]), $html);
    $html = preg_replace_callback('#(?:<p>\s*)?\[\[product:([a-z0-9-]+)\]\](?:\s*</p>)?#', fn($m) => product_grid([$m[1]], true), $html);
    $html = preg_replace_callback('#(?:<p>\s*)?\[\[products:([a-z0-9,\- ]+)\]\](?:\s*</p>)?#', fn($m) => product_grid(array_map('trim', explode(',', $m[1]))), $html);
    // lazy-load any body image without loading attr
    $html = preg_replace('#<img(?![^>]*loading=)#', '<img loading="lazy" decoding="async"', $html);
    return $html;
}

function tool_cta(string $slug): string {
    $m = tool_meta($slug);
    if (!$m) return '';
    return '<a class="tool-cta reveal" href="/' . e($slug) . '"><span class="tool-cta-ic">' . icon($m['icon']) . '</span><span class="tool-cta-txt"><small>Free tool</small><strong>' . e($m['name']) . '</strong><span>' . e($m['short']) . '</span></span><span class="tool-cta-go">Open ' . icon('arrow') . '</span></a>';
}

function product_card(string $key): string {
    $p = products()[$key] ?? null;
    if (!$p) return '';
    [$title, $why, $ic, $badge, $q] = $p;
    return '<div class="product-card reveal"><div class="product-art pa-' . e($ic) . '">' . icon($ic, 'ic product-ic') . '<span class="product-badge">' . e($badge) . '</span></div>'
        . '<div class="product-body"><h4>' . e($title) . '</h4><p>' . e($why) . '</p>'
        . '<a class="btn btn-amazon" href="' . e(amazon_url($q)) . '" target="_blank" rel="nofollow sponsored noopener">' . icon('cart') . ' Check price on Amazon</a></div></div>';
}
function product_grid(array $keys, bool $single = false): string {
    $cards = implode('', array_map('product_card', $keys));
    if ($cards === '') return '';
    return '<div class="products' . ($single ? ' products-single' : '') . '">' . $cards . '</div><p class="aff-note">As an Amazon Associate we earn from qualifying purchases, at no extra cost to you.</p>';
}

/* ---------- schema ---------- */
function json_ld(array $data): string {
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>';
}
function faq_schema(array $faqs): array {
    return ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => strip_tags($f[0]), 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f[1])]], $faqs)];
}
function breadcrumb_schema(array $crumbs): array {
    $items = []; $i = 1;
    foreach ($crumbs as [$name, $path]) $items[] = ['@type' => 'ListItem', 'position' => $i++, 'name' => $name, 'item' => abs_url($path)];
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}
function breadcrumbs_html(array $crumbs): string {
    $out = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $out[] = $i === count($crumbs) - 1 ? '<span aria-current="page">' . e($name) . '</span>' : '<a href="' . e($path) . '">' . e($name) . '</a>';
    }
    return '<nav class="crumbs" aria-label="Breadcrumb">' . implode(icon('chev', 'ic ic-xs'), $out) . '</nav>';
}

function faqs_html(array $faqs, string $title = 'Frequently asked questions'): string {
    if (!$faqs) return '';
    $h = '<section class="faq" id="faq"><h2>' . e($title) . '</h2>';
    foreach ($faqs as $i => $f) {
        $h .= '<details class="faq-item reveal"' . ($i === 0 ? ' open' : '') . '><summary>' . e(strip_tags($f[0])) . '<span class="faq-plus"></span></summary><div class="faq-a">' . (str_contains($f[1], '<') ? $f[1] : '<p>' . e($f[1]) . '</p>') . '</div></details>';
    }
    return $h . '</section>';
}

/* ---------- layout ---------- */
function page_start(array $o): void {
    $GLOBALS['__page'] = $o;
    include ROOT . '/templates/header.php';
}
function page_end(): void {
    include ROOT . '/templates/footer.php';
}

function nav_items(): array {
    return [
        ['Grade Tools', '/tools#grades'],
        ['GPA', '/tools#gpa'],
        ['Teachers', '/tools#teachers'],
        ['All Tools', '/tools'],
        ['Blog', '/blog'],
    ];
}
