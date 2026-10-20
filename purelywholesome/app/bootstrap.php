<?php
// Purely Wholesome Farm - shared configuration and helpers.
declare(strict_types=1);

const SITE_NAME = 'Purely Wholesome Farm';
const SITE_TAGLINE = 'Grow Better, Live Simpler';
const SITE_ORIGIN = 'https://purelywholesome.com';   // canonical origin, whatever host serves the page
const SITE_EMAIL = 'info@purelywholesome.com';
const ASSET_VERSION = '20261020';
const ROOT = __DIR__ . '/..';

// Only the real domain may be indexed; the temporary preview host is noindexed so
// it never competes with purelywholesome.com in search.
function is_production_host(): bool
{
    $host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
    return $host === 'purelywholesome.com' || $host === 'www.purelywholesome.com';
}

function e(?string $s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function canonical(string $path): string
{
    return SITE_ORIGIN . $path;
}

function asset(string $path): string
{
    return '/assets/' . $path . '?v=' . ASSET_VERSION;
}

function posts_index(): array
{
    static $index = null;
    return $index ??= require ROOT . '/content/index.php';
}

/** Indexable posts, newest first. */
function live_posts(): array
{
    return array_filter(posts_index(), fn($p) => $p['indexable']);
}

function load_post(string $slug): ?array
{
    if (!preg_match('/^[a-z0-9-]+$/', $slug)) {
        return null;
    }
    $file = ROOT . '/content/posts/' . $slug . '.php';
    return is_file($file) ? require $file : null;
}

function post_url(string $slug): string
{
    return '/' . $slug . '/';
}

function fmt_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

/** The posts that carried the site's search traffic (Search Console, Aug 2025 - Oct 2026). */
const POPULAR = [
    'sides-for-lamb-chops', 'pumpkin-pie-filling', 'best-sauce-for-lamb-chops', 'how-to-brine-a-chicken',
    'how-to-brine-your-own-brisket', 'what-to-do-with-a-rooster', 'how-to-keep-livestock-water-from-freezing',
    'frozen-eggs-for-dinner', 'best-brining-container', 'goat-pregnancy', 'how-to-sterilize-mason-jars-for-canning',
    'sweet-pickle-recipe',
];

const TOPICS = [
    'lamb' => ['Lamb Recipes', 'Chops, roasts, sauces and the sides that make them sing.', 'sides-for-lamb-chops'],
    'brining' => ['Brining', 'Salt ratios, timing and containers for juicy chicken, turkey and brisket.', 'how-to-brine-a-chicken'],
    'baking' => ['Pumpkin, Pies & Baking', 'Pumpkin pie fixes, sourdough, crackers and scratch desserts.', 'pumpkin-pie-filling'],
    'canning' => ['Canning & Preserving', 'Water bath basics, pickles, salsa and safe jar prep.', 'how-to-sterilize-mason-jars-for-canning'],
    'goats' => ['Raising Goats', 'Breeds, kidding, milking and keeping a healthy herd.', 'goat-pregnancy'],
    'chickens-eggs' => ['Chickens & Eggs', 'Coops, flock care, roosters and farm fresh eggs.', 'farm-fresh-eggs'],
    'homestead' => ['Homestead & Garden', 'Garden beds, winter chores, tools and farm know-how.', 'how-to-keep-livestock-water-from-freezing'],
    'crafts' => ['Farmhouse Crafts', 'Dish cloths, towels, yarn and handmade home goods.', 'bernat-handicrafter-cotton-yarn'],
    'kitchen' => ['From the Farm Kitchen', 'Everyday scratch cooking from the farmhouse table.', 'herb-goat-cheese-stuffed-chicken-breast'],
];

const CATEGORIES = [
    'recipes' => ['Recipes', 'Scratch cooking from the Purely Wholesome Farm kitchen.'],
    'livestock-farming' => ['Livestock Farming', 'Goats, chickens and cattle: practical care from the barn.'],
    'farming-tips' => ['Farming Tips', 'Hands-on homestead and kitchen know-how.'],
    'smart-agriculture' => ['Smart Agriculture', 'Gardening, growing and smarter ways to work the land.'],
    'farm-machinery' => ['Farm Machinery', 'Equipment that earns its keep on a small farm.'],
    'general' => ['General', 'Crafts and odds and ends from around the farmhouse.'],
];

function category_slug(string $name): string
{
    return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($name)), '-');
}

function topic_posts(string $topic): array
{
    return array_filter(live_posts(), fn($p) => $p['topic'] === $topic);
}

function tools(): array
{
    static $tools = null;
    return $tools ??= require ROOT . '/app/tools/registry.php';
}

function render_tool(string $slug, bool $compact = false): string
{
    $tool = tools()[$slug] ?? null;
    if (!$tool) {
        return '';
    }
    ob_start();
    include ROOT . '/app/tools/' . $slug . '.php';
    return ob_get_clean();
}

/** Render a view inside the shared layout. $page keys: title, desc, path, robots, schema, body_class, og_image, og_type. */
function render(string $view, array $vars = [], array $page = []): void
{
    extract($vars);
    ob_start();
    include ROOT . '/app/views/' . $view . '.php';
    $content = ob_get_clean();
    header('Content-Type: text/html; charset=utf-8');
    include ROOT . '/app/views/layout.php';
}

function not_found(): void
{
    http_response_code(404);
    render('404', [], ['title' => 'Page Not Found | ' . SITE_NAME, 'desc' => 'This page could not be found.', 'path' => '/404/', 'robots' => 'noindex, follow']);
    exit;
}

function redirect(string $path, int $code = 301): void
{
    header('Location: ' . $path, true, $code);
    exit;
}

function card(array $p, string $size = ''): string
{
    $img = $p['image'] ? '<img src="' . e($p['image']) . '" alt="" loading="lazy" decoding="async" width="' . (int)$p['image_w'] . '" height="' . (int)$p['image_h'] . '">' : '';
    $topic = TOPICS[$p['topic']][0] ?? '';
    return '<article class="card ' . $size . '" data-topic="' . e($p['topic']) . '" data-search="' . e(strtolower($p['title'] . ' ' . $p['excerpt'])) . '">'
        . '<a class="card__media" href="' . post_url($p['slug']) . '" tabindex="-1" aria-hidden="true">' . $img . '</a>'
        . '<div class="card__body"><span class="chip chip--' . e($p['topic']) . '">' . e($topic) . '</span>'
        . '<h3 class="card__title"><a href="' . post_url($p['slug']) . '">' . e($p['h1'] ?: $p['title']) . '</a></h3>'
        . '<p class="card__excerpt">' . e($p['desc']) . '</p>'
        . '<span class="card__meta">' . (int)$p['minutes'] . ' min read</span></div></article>';
}

function json_ld(array $data): string
{
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>';
}

function org_schema(): array
{
    return [
        '@type' => 'Organization', '@id' => SITE_ORIGIN . '/#organization', 'name' => SITE_NAME,
        'url' => SITE_ORIGIN . '/', 'email' => SITE_EMAIL,
        'logo' => ['@type' => 'ImageObject', 'url' => SITE_ORIGIN . '/assets/img/purely-wholesome-farm-logo.webp', 'width' => 600, 'height' => 81],
    ];
}

function breadcrumb_schema(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => canonical($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function breadcrumbs_html(array $crumbs): string
{
    $out = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $out[] = $i === count($crumbs) - 1 ? '<span aria-current="page">' . e($name) . '</span>' : '<a href="' . e($path) . '">' . e($name) . '</a>';
    }
    return '<nav class="crumbs" aria-label="Breadcrumb">' . implode('<span class="crumbs__sep" aria-hidden="true">/</span>', $out) . '</nav>';
}

function search_posts(string $q): array
{
    $terms = array_filter(preg_split('/\s+/', strtolower(trim($q))), fn($t) => strlen($t) > 1);
    if (!$terms) {
        return [];
    }
    $scored = [];
    foreach (live_posts() as $p) {
        $title = strtolower($p['title'] . ' ' . $p['h1']);
        $body = strtolower($p['desc'] . ' ' . $p['excerpt'] . ' ' . str_replace('-', ' ', $p['slug']));
        $score = 0;
        foreach ($terms as $t) {
            $score += substr_count($title, $t) * 3 + substr_count($body, $t);
        }
        if ($score > 0) {
            $scored[] = [$score, $p];
        }
    }
    usort($scored, fn($a, $b) => $b[0] <=> $a[0]);
    return array_column($scored, 1);
}

function icon(string $name): string
{
    static $icons = null;
    $icons ??= require ROOT . '/app/icons.php';
    return $icons[$name] ?? '';
}
