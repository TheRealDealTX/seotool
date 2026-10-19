<?php
// Site-wide settings and helpers. Every page includes this first.

const SITE_NAME    = 'Insurance Adjuster Salary';
const SITE_TAGLINE = 'Real pay data, calculators and career guides for insurance adjusters';
const COURSE_URL   = 'https://www.adjustingonline.com/courses/';
const PROMO_CODE   = 'joe20';
const CANONICAL_HOST = 'insuranceadjustersalary.com';
const BLOG_BASE    = '/insurance-adjuster-advice/';
const ASSET_VER    = '20261019b';

define('SITE_ROOT', dirname(__DIR__));

/** Scheme + host the site is being served from (works on the temporary domain and after the move). */
function base_url(): string
{
    $host = $_SERVER['HTTP_HOST'] ?? CANONICAL_HOST;
    $host = preg_replace('/[^a-z0-9.\-:]/i', '', $host);
    return 'https://' . $host;
}

/** True while the site is on a Hostinger preview/temporary domain - keeps it out of Google until the real domain moves over. */
function is_temporary_host(): bool
{
    $host = strtolower($_SERVER['HTTP_HOST'] ?? '');
    return $host === '' || str_ends_with($host, '.hostingersite.com') || str_contains($host, 'localhost') || str_starts_with($host, '127.');
}

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function asset(string $path): string
{
    return '/assets/' . ltrim($path, '/') . (preg_match('/\.(css|js)$/', $path) ? '?v=' . ASSET_VER : '');
}

function fmt_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

/** Primary navigation: label => path */
function nav_items(): array
{
    return [
        'Texas Pay'      => '/#texas',
        'Salary Guide'   => '/#salary-guide',
        'Tools'          => '/tools/',
        'By State'       => '/salary-by-state/',
        'Advice'         => BLOG_BASE,
        'About'          => '/about/',
    ];
}

/** All tools, used by the tools hub, footer and cross-links. */
function tools(): array
{
    return [
        [
            'path' => '/salary-calculator/',
            'name' => 'Adjuster Salary Calculator',
            'icon' => 'calc',
            'blurb' => 'Estimate your insurance adjuster salary by role, line of business, experience and state.',
        ],
        [
            'path' => '/cat-deployment-calculator/',
            'name' => 'CAT Deployment Earnings Calculator',
            'icon' => 'storm',
            'blurb' => 'Model what a catastrophe deployment pays after fee splits, expenses and taxes.',
        ],
        [
            'path' => '/public-adjuster-fee-calculator/',
            'name' => 'Public Adjuster Fee Calculator',
            'icon' => 'percent',
            'blurb' => 'See what a public adjuster earns on a settlement, with Texas and Florida fee caps built in.',
        ],
        [
            'path' => '/salary-by-state/',
            'name' => 'Salary by State Explorer',
            'icon' => 'map',
            'blurb' => 'Search and sort estimated adjuster pay for all 50 states and D.C.',
        ],
    ];
}

/** Inline SVG icons (stroke style, inherit currentColor). */
function icon(string $name, int $size = 24): string
{
    $paths = [
        'shield'  => '<path d="M12 2 4 5v6c0 5.25 3.4 9.74 8 11 4.6-1.26 8-5.75 8-11V5l-8-3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
        'calc'    => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v3M8 18h4"/>',
        'storm'   => '<path d="M17.5 17H18a4 4 0 0 0 0-8h-1.26A6 6 0 1 0 6 15.7"/><path d="m13 11-3 5h4l-3 5"/>',
        'percent' => '<circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/><path d="M19 5 5 19"/>',
        'map'     => '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z"/><path d="M9 4v14M15 6v14"/>',
        'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'check'   => '<path d="m5 12 4.5 4.5L19 7"/>',
        'x'       => '<path d="M6 6l12 12M18 6 6 18"/>',
        'clock'   => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'dollar'  => '<path d="M12 2v20M17 6.5C17 4.6 14.8 3.5 12 3.5S7 4.7 7 7s2.2 3.2 5 3.9 5 1.7 5 4.1-2.2 3.5-5 3.5-5-1.1-5-3"/>',
        'brief'   => '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
        'home'    => '<path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'car'     => '<path d="M5 17h14M3 17v-4l2-5h14l2 5v4"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/>',
        'hard'    => '<path d="M3 18h18M5 18v-3a7 7 0 0 1 14 0v3"/><path d="M10 8V5h4v3"/>',
        'user'    => '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        'trend'   => '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
        'book'    => '<path d="M4 4h10a4 4 0 0 1 4 4v12H8a4 4 0 0 1-4-4V4Z"/><path d="M8 20a4 4 0 0 1 0-8h10"/>',
        'star'    => '<path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4 6.4 20.3l1.1-6.2L3 9.7l6.2-.9L12 3Z"/>',
        'menu'    => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'up'      => '<path d="M12 19V5M6 11l6-6 6 6"/>',
        'tag'     => '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9-9-9Z"/><circle cx="8" cy="8" r="1.5"/>',
        'bolt'    => '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>',
    ];
    $p = $paths[$name] ?? $paths['shield'];
    return '<svg class="ico" width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}

/** Load every blog post (newest first). */
function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(SITE_ROOT . '/content/posts/*.php') as $file) {
        $p = require $file;
        if (is_array($p) && !empty($p['slug'])) {
            $posts[$p['slug']] = $p;
        }
    }
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $posts;
}

function get_post(string $slug): ?array
{
    return all_posts()[$slug] ?? null;
}

function post_url(array $p): string
{
    return BLOG_BASE . $p['slug'] . '/';
}

/** Renders a blog card (used on home, blog index and related posts). */
function post_card(array $p): string
{
    return '<article class="post-card reveal">'
        . '<a class="post-card-img" href="' . e(post_url($p)) . '" tabindex="-1" aria-hidden="true"><img src="/assets/img/' . e($p['image']) . '" alt="" loading="lazy" width="600" height="338"></a>'
        . '<div class="post-card-body">'
        . '<div class="post-meta"><span class="chip">' . e($p['category']) . '</span><time datetime="' . e($p['date']) . '">' . e(fmt_date($p['date'])) . '</time></div>'
        . '<h3><a href="' . e(post_url($p)) . '">' . e($p['title']) . '</a></h3>'
        . '<p>' . e($p['excerpt']) . '</p>'
        . '<a class="link-arrow" href="' . e(post_url($p)) . '">Read guide ' . icon('arrow', 16) . '</a>'
        . '</div></article>';
}

/** Promo line that must accompany every certification link (affiliate code). */
function promo_line(string $class = 'cert-code'): string
{
    return '<span class="' . $class . '">Use <strong class="code-pill" data-copy="' . PROMO_CODE . '">' . PROMO_CODE . '</strong> for 20% off</span>';
}

/** "Get Certified" button with the promo code attached underneath. */
function cert_btn(string $btnClass = 'btn btn-gold', string $label = 'Get Certified This Week'): string
{
    return '<span class="cert-wrap"><a class="' . e($btnClass) . '" href="' . COURSE_URL . '" target="_blank" rel="sponsored noopener">' . e($label) . ' ' . icon('arrow', 16) . '</a>' . promo_line() . '</span>';
}

/** Course call-to-action band (carried over from the original site). */
function course_cta(string $heading = 'Become a Texas Insurance Adjuster Within a Week'): string
{
    return '<section class="cta-band"><div class="container cta-inner reveal">'
        . '<div><span class="eyebrow">Get licensed fast</span><h2>' . e($heading) . '</h2>'
        . '<p>Take an online Texas all-lines pre-licensing course, get licensed and start applying for claims roles across Texas and every reciprocal state. Use code <strong class="code-pill" data-copy="' . PROMO_CODE . '">' . PROMO_CODE . '</strong> for 20% off.</p></div>'
        . cert_btn('btn btn-gold btn-lg')
        . '</div></section>';
}

/** Hero band for inner pages. $crumbs = [label => href|null] */
function page_hero(string $eyebrow, string $h1, string $lead, string $img, array $crumbs = []): string
{
    $c = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>';
    foreach ($crumbs as $label => $href) {
        $c .= '<span>/</span>' . ($href ? '<a href="' . e($href) . '">' . e($label) . '</a>' : e($label));
    }
    $c .= '</nav>';
    return '<section class="page-hero"><div class="hero-media"><img src="/assets/img/' . e($img) . '" alt="" width="1200" height="675"></div>'
        . '<div class="container">' . $c . '<span class="eyebrow">' . e($eyebrow) . '</span><h1>' . $h1 . '</h1><p>' . $lead . '</p></div></section>';
}

/** FAQ block + schema node. */
function faq_html(array $faqs): string
{
    $h = '<div class="faq">';
    foreach ($faqs as $f) {
        $h .= '<details><summary>' . e($f['q']) . '</summary><div class="faq-a"><p>' . e($f['a']) . '</p></div></details>';
    }
    return $h . '</div>';
}

function faq_schema(array $faqs): array
{
    return ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']]], $faqs)];
}

function tool_schema(string $name, string $path, string $desc): array
{
    return ['@type' => 'WebApplication', 'name' => $name, 'url' => base_url() . $path, 'description' => $desc,
        'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any',
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD']];
}

/** Grid of the other tools, for cross-linking at the bottom of tool pages. */
function other_tools(string $except): string
{
    $h = '<section class="section section-soft"><div class="container"><div class="section-head reveal"><span class="eyebrow">More free tools</span><h2>Keep running the numbers</h2></div><div class="grid-3">';
    foreach (tools() as $t) {
        if ($t['path'] === $except) continue;
        $h .= '<a class="card tool-card spotlight tilt reveal" href="' . e($t['path']) . '"><div class="icon-wrap">' . icon($t['icon'], 26) . '</div><h3>' . e($t['name']) . '</h3><p>' . e($t['blurb']) . '</p><span class="link-arrow">Open tool ' . icon('arrow', 16) . '</span></a>';
    }
    return $h . '</div></div></section>';
}
