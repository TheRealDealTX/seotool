<?php defined('BO') || exit;
// Shared helpers: escaping, Amazon affiliate links, content components and schema.

function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8', false); }

function img_url($file) { return UPLOADS . $file; }

function fmt_date($ymd) { return date('F j, Y', strtotime($ymd)); }

/** Amazon search URL carrying the Associates tag. */
function amz_url($query) {
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . AMAZON_TAG;
}

/** Inline Amazon affiliate text link. */
function amz($query, $label = null) {
    $label = $label ?? $query;
    return '<a class="amz" href="' . e(amz_url($query)) . '" target="_blank" rel="nofollow sponsored noopener">' . e($label) . '</a>';
}

/** Amazon call-to-action button. */
function amz_btn($query, $label = 'Check Price on Amazon') {
    return '<a class="btn btn-amz" href="' . e(amz_url($query)) . '" target="_blank" rel="nofollow sponsored noopener"><i class="fa-brands fa-amazon" aria-hidden="true"></i> ' . e($label) . '</a>';
}

/**
 * Product card. $p keys: name, q (Amazon search), blurb, icon (Font Awesome
 * name), badge (optional), pros (array, optional).
 */
function product_card(array $p) {
    $h = '<div class="product-card reveal">';
    if (!empty($p['badge'])) $h .= '<span class="badge">' . e($p['badge']) . '</span>';
    $h .= '<div class="product-icon"><i class="fa-solid ' . e($p['icon'] ?? 'fa-bullseye') . '" aria-hidden="true"></i></div>';
    $h .= '<div class="product-body"><h4>' . e($p['name']) . '</h4><p>' . $p['blurb'] . '</p>';
    if (!empty($p['pros'])) {
        $h .= '<ul class="checks">';
        foreach ($p['pros'] as $pro) $h .= '<li>' . e($pro) . '</li>';
        $h .= '</ul>';
    }
    $h .= amz_btn($p['q']) . '</div></div>';
    return $h;
}

/** A grid of product cards with an optional heading line. */
function product_grid(array $items, $title = null) {
    $h = '<div class="product-block">';
    if ($title) $h .= '<p class="product-block-title"><i class="fa-solid fa-cart-shopping" aria-hidden="true"></i> ' . e($title) . '</p>';
    $h .= '<div class="product-grid">';
    foreach ($items as $p) $h .= product_card($p);
    return $h . '</div><p class="aff-note">As an Amazon Associate, Better Outdoors earns from qualifying purchases.</p></div>';
}

/** Spec table: [['Label','Value'], ...]. */
function spec_table(array $rows, $caption = null) {
    $h = '<div class="table-wrap"><table class="spec-table">';
    if ($caption) $h .= '<caption>' . e($caption) . '</caption>';
    foreach ($rows as $r) $h .= '<tr><th scope="row">' . e($r[0]) . '</th><td>' . e($r[1]) . '</td></tr>';
    return $h . '</table></div>';
}

/** Generic table with a header row. */
function data_table(array $head, array $rows, $caption = null) {
    $h = '<div class="table-wrap"><table class="data-table">';
    if ($caption) $h .= '<caption>' . e($caption) . '</caption>';
    $h .= '<thead><tr>';
    foreach ($head as $c) $h .= '<th scope="col">' . e($c) . '</th>';
    $h .= '</tr></thead><tbody>';
    foreach ($rows as $r) {
        $h .= '<tr>';
        foreach ($r as $c) $h .= '<td>' . e($c) . '</td>';
        $h .= '</tr>';
    }
    return $h . '</tbody></table></div>';
}

/** Callout box. $type: tip | warn | note | key. Body is trusted HTML. */
function callout($type, $title, $body) {
    $icons = ['tip' => 'fa-lightbulb', 'warn' => 'fa-triangle-exclamation', 'note' => 'fa-circle-info', 'key' => 'fa-key'];
    return '<aside class="callout callout-' . e($type) . ' reveal"><i class="fa-solid ' . ($icons[$type] ?? 'fa-circle-info') . '" aria-hidden="true"></i><div><strong>' . e($title) . '</strong><p>' . $body . '</p></div></aside>';
}

/** Pros / cons pair. */
function pros_cons(array $pros, array $cons) {
    $h = '<div class="pros-cons reveal"><div class="pros"><h4><i class="fa-solid fa-circle-check" aria-hidden="true"></i> Pros</h4><ul>';
    foreach ($pros as $p) $h .= '<li>' . e($p) . '</li>';
    $h .= '</ul></div><div class="cons"><h4><i class="fa-solid fa-circle-xmark" aria-hidden="true"></i> Cons</h4><ul>';
    foreach ($cons as $c) $h .= '<li>' . e($c) . '</li>';
    return $h . '</ul></div></div>';
}

/** Verdict box with a 0-10 score per category. */
function verdict($summary, array $scores) {
    $total = round(array_sum($scores) / max(count($scores), 1), 1);
    $h = '<div class="verdict reveal"><div class="verdict-score"><span class="score-ring" style="--score:' . ($total * 10) . '"><b>' . $total . '</b><small>/10</small></span><span class="verdict-label">Better Outdoors Score</span></div><div class="verdict-body"><p>' . $summary . '</p><ul class="score-bars">';
    foreach ($scores as $label => $v) {
        $h .= '<li><span>' . e($label) . '</span><span class="bar"><span style="--w:' . ($v * 10) . '%"></span></span><b>' . e($v) . '</b></li>';
    }
    return $h . '</ul></div></div>';
}

/** FAQ accordion; the page template turns $GLOBALS['FAQS'] into FAQPage schema. */
function faq_block(array $faqs, $id = 'h-frequently-asked-questions', $title = 'Frequently Asked Questions') {
    $GLOBALS['FAQS'] = array_merge($GLOBALS['FAQS'] ?? [], $faqs);
    $h = '<h2 id="' . e($id) . '">' . e($title) . '</h2><div class="faq">';
    foreach ($faqs as $q => $a) {
        $h .= '<details class="faq-item"><summary>' . e($q) . '</summary><div class="faq-a"><p>' . $a . '</p></div></details>';
    }
    return $h . '</div>';
}

/** Embed a compact tool teaser card inside an article. */
function tool_cta($slug) {
    global $TOOLS;
    $t = $TOOLS[$slug];
    return '<a class="tool-cta reveal" href="/tools/' . e($slug) . '/"><i class="fa-solid ' . e($t['icon']) . '" aria-hidden="true"></i><span><strong>Try the free ' . e($t['h1']) . '</strong><small>' . e($t['short']) . '</small></span><i class="fa-regular fa-circle-right" aria-hidden="true"></i></a>';
}

/** Article figure using an original upload. */
function figure($file, $alt, $caption = null) {
    $h = '<figure class="post-figure reveal"><img src="' . e(img_url($file)) . '" alt="' . e($alt) . '" loading="lazy" decoding="async" width="1200" height="800">';
    if ($caption) $h .= '<figcaption>' . e($caption) . '</figcaption>';
    return $h . '</figure>';
}

/** Internal link to another post by slug. */
function post_link($slug, $label = null) {
    global $POSTS;
    $label = $label ?? $POSTS[$slug]['h1'];
    return '<a href="/' . e($slug) . '/">' . e($label) . '</a>';
}

/** Build a table of contents from h2 ids in rendered HTML. */
function build_toc($html) {
    preg_match_all('#<h2 id="([^"]+)"[^>]*>(.*?)</h2>#s', $html, $m, PREG_SET_ORDER);
    if (count($m) < 3) return '';
    $h = '<nav class="toc" aria-label="Table of contents"><p class="toc-title"><i class="fa-solid fa-list" aria-hidden="true"></i> In this guide</p><ol>';
    foreach ($m as $x) $h .= '<li><a href="#' . e($x[1]) . '">' . strip_tags($x[2]) . '</a></li>';
    return $h . '</ol></nav>';
}

function reading_minutes($html) {
    return max(1, (int)round(str_word_count(strip_tags($html)) / 230));
}

function post_card($slug, array $p, $lazy = true) {
    return '<article class="post-card reveal" data-cat="' . e($p['cat']) . '" data-text="' . e(strtolower($p['h1'] . ' ' . $p['excerpt'] . ' ' . $p['kw'])) . '">'
        . '<a class="post-card-img" href="/' . e($slug) . '/"><img src="' . e(img_url($p['thumb'])) . '" alt="' . e($p['h1']) . '" ' . ($lazy ? 'loading="lazy" ' : '') . 'decoding="async" width="768" height="512"><span class="chip">' . e($p['cat']) . '</span></a>'
        . '<div class="post-card-body"><h3><a href="/' . e($slug) . '/">' . e($p['h1']) . '</a></h3><p>' . e($p['excerpt']) . '</p>'
        . '<p class="post-card-meta"><i class="fa-regular fa-calendar" aria-hidden="true"></i> Updated ' . e(fmt_date($p['updated'])) . '</p></div></article>';
}

function json_ld(array $data) {
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>';
}

function org_schema() {
    return [
        '@type' => 'Organization',
        '@id' => SITE_URL . '/#organization',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'email' => SITE_EMAIL,
        'logo' => ['@type' => 'ImageObject', 'url' => SITE_URL . img_url('Better-Outdoors-Logo.webp'), 'width' => 991, 'height' => 245],
    ];
}

function breadcrumb_schema(array $crumbs) {
    $items = [];
    foreach ($crumbs as $i => [$name, $url]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => SITE_URL . $url];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function breadcrumbs_html(array $crumbs) {
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $url]) {
        $h .= $i === $last ? '<li aria-current="page">' . e($name) . '</li>' : '<li><a href="' . e($url) . '">' . e($name) . '</a></li>';
    }
    return $h . '</ol></nav>';
}
