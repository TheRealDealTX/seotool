<?php
// Site-wide constants and helpers. Loaded by index.php only.
defined('SS_APP') || exit;

const SITE_NAME   = 'Saffron Supplement';
const SITE_ORIGIN = 'https://saffronsupplement.com';
const SITE_EMAIL  = 'info@saffronsupplement.com';
const GA_ID       = 'G-J76LEX8DPZ';
const AMZ_TAG     = 'saffronsupplement-20';
const SITE_YEAR   = '2026';
const UPDATED     = '2026-10-23';
const UPDATED_HUMAN = 'October 23, 2026';

/** A route's publish/modified date (blog posts carry their own). */
function route_date(array $r) { return $r['date'] ?? UPDATED; }
function human_date($ymd) { return date('F j, Y', strtotime($ymd)); }

/** Blog posts (routes with a 'date' under /blog/), newest first. */
function blog_posts() {
    $posts = array_filter(ROUTES, fn($r) => ($r['parent'] ?? null) === '/blog/' && isset($r['date']));
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $posts;
}

/** "More from the blog" links, excluding the current post. */
function more_posts($current, $n = 3) {
    $h = '<section class="more-posts"><h2>More from the Blog</h2><ul>';
    foreach (array_slice(array_diff_key(blog_posts(), [$current => 1]), 0, $n, true) as $p => $r) {
        $h .= '<li><a href="' . e($p) . '">' . e($r['h1']) . '</a> <span class="small">&middot; ' . human_date($r['date']) . '</span></li>';
    }
    return $h . '</ul></section>';
}

/** HTML-escape. */
function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_HTML5, 'UTF-8'); }

/** Amazon product URL carrying the Associates tag. */
function amz_url($asin) { return 'https://www.amazon.com/dp/' . rawurlencode($asin) . '/?tag=' . AMZ_TAG; }

/** Amazon search URL carrying the Associates tag. */
function amz_search_url($q) { return 'https://www.amazon.com/s?k=' . rawurlencode($q) . '&tag=' . AMZ_TAG; }

/** Affiliate anchor. $target is an ASIN (10 chars, starts with B0/digit) or a search phrase. */
function amz($target, $label, $class = '') {
    $url = preg_match('/^[A-Z0-9]{10}$/', $target) ? amz_url($target) : amz_search_url($target);
    $cls = $class ? ' class="' . e($class) . '"' : '';
    return '<a href="' . e($url) . '"' . $cls . ' rel="sponsored nofollow noopener" target="_blank">' . $label . '</a>';
}

/** Big "Check price on Amazon" button for a product. */
function amz_btn($asin, $label = 'Check Price on Amazon') {
    return amz($asin, e($label) . ' <span aria-hidden="true">&rarr;</span>', 'btn btn-amz');
}

/** Internal link helper. */
function a($href, $label, $class = '') {
    $cls = $class ? ' class="' . e($class) . '"' : '';
    return '<a href="' . e($href) . '"' . $cls . '>' . $label . '</a>';
}

/** Medical-claim disclaimer box shown on health pages. */
function med_note() {
    return '<aside class="note note-med" role="note"><strong>Health note:</strong> This page is educational and is not medical advice. '
        . 'Talk to your doctor or pharmacist before starting saffron, especially if you are pregnant, breastfeeding, have bipolar disorder, '
        . 'or take antidepressants, blood thinners or blood-pressure medication. ' . a('/medical-disclaimer/', 'Full medical disclaimer') . '.</aside>';
}

/** Short Amazon Associates disclosure shown above affiliate content. */
function aff_note() {
    return '<p class="aff-note">As an Amazon Associate, ' . SITE_NAME . ' earns from qualifying purchases at no extra cost to you. '
        . a('/affiliate-disclosure/', 'How we make money') . '.</p>';
}

/** FAQ block that also feeds FAQPage JSON-LD via $GLOBALS['faq']. */
function faq_block(array $items, $heading = 'Frequently Asked Questions') {
    $GLOBALS['faq'] = array_merge($GLOBALS['faq'] ?? [], $items);
    static $n = 0;
    $id = $n++ ? 'faq-' . $n : 'faq';
    $h = '<section class="faq" id="' . $id . '"><h2>' . e($heading) . '</h2>';
    foreach ($items as [$q, $ans]) {
        $h .= '<details><summary>' . e($q) . '</summary><div class="faq-a">' . $ans . '</div></details>';
    }
    return $h . '</section>';
}

/** "Sources" list of clinical references. */
function sources(array $refs) {
    $h = '<section class="sources"><h2>Research &amp; Sources</h2><ol>';
    foreach ($refs as $r) $h .= '<li>' . $r . '</li>';
    return $h . '</ol></section>';
}

/** Card linking to an internal page. */
function card($href, $title, $text, $icon = '') {
    return '<a class="card" href="' . e($href) . '">' . ($icon ? '<span class="card-ic" aria-hidden="true">' . $icon . '</span>' : '')
        . '<h3>' . e($title) . '</h3><p>' . e($text) . '</p><span class="card-more">Read more &rarr;</span></a>';
}

/** Table-of-contents for long pages. */
function toc(array $items) {
    $h = '<nav class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>';
    foreach ($items as $id => $label) $h .= '<li><a href="#' . e($id) . '">' . e($label) . '</a></li>';
    return $h . '</ol></nav>';
}
