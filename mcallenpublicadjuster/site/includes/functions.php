<?php
/**
 * Shared helpers: escaping, URLs, content loading, images, icons, shortcodes.
 */

declare(strict_types=1);

require_once __DIR__ . '/config.php';

/* ------------------------------------------------------------------ */
/* Escaping + small utilities                                         */
/* ------------------------------------------------------------------ */

function e($value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function url(string $path = '/'): string
{
    return rtrim(cfg('site_url'), '/') . $path;
}

function tel_link(): string
{
    return 'tel:' . cfg('phone_e164');
}

function format_date(?string $ymd, string $format = 'F j, Y'): string
{
    if (!$ymd) {
        return '';
    }
    $ts = strtotime($ymd);
    return $ts ? date($format, $ts) : '';
}

function iso_date(?string $ymd): string
{
    if (!$ymd) {
        return '';
    }
    $ts = strtotime($ymd);
    return $ts ? date('c', $ts) : '';
}

function reading_minutes(string $html): int
{
    $words = str_word_count(strip_tags($html));
    return max(1, (int) round($words / 230));
}

function data_path(string $rel): string
{
    return MPA_ROOT . '/data/' . ltrim($rel, '/');
}

function read_json_file(string $file, $default = [])
{
    if (!is_file($file)) {
        return $default;
    }
    $raw = @file_get_contents($file);
    if ($raw === false || $raw === '') {
        return $default;
    }
    $data = json_decode($raw, true);
    return $data === null ? $default : $data;
}

/** Atomic JSON write (temp file + rename) so readers never see half a file. */
function write_json_file(string $file, $data): bool
{
    $dir = dirname($file);
    if (!is_dir($dir) && !@mkdir($dir, 0755, true)) {
        return false;
    }
    $tmp = $file . '.' . bin2hex(random_bytes(4)) . '.tmp';
    $json = json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if ($json === false || @file_put_contents($tmp, $json, LOCK_EX) === false) {
        return false;
    }
    return @rename($tmp, $file);
}

function log_line(string $channel, string $message): void
{
    $file = data_path('logs/' . preg_replace('/[^a-z0-9_-]/i', '', $channel) . '.log');
    $dir = dirname($file);
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    // Keep logs small: rotate at ~512 KB.
    if (is_file($file) && filesize($file) > 512 * 1024) {
        @rename($file, $file . '.1');
    }
    @file_put_contents($file, '[' . date('Y-m-d H:i:s T') . '] ' . $message . "\n", FILE_APPEND | LOCK_EX);
}

/* ------------------------------------------------------------------ */
/* Content loading                                                    */
/* ------------------------------------------------------------------ */

/**
 * Content files live in content/{pages,posts,services}/<name>.php and return an array.
 * URL mapping:
 *   pages/home.php                 -> /
 *   pages/about-us.php             -> /about-us/
 *   pages/author__joseph-dittman.php -> /author/joseph-dittman/
 *   posts/<slug>.php               -> /<slug>/        (matches the original WordPress permalinks)
 *   services/<slug>.php            -> /services/<slug>/
 */
function content_path_for(string $type, string $name): string
{
    if ($type === 'pages') {
        return $name === 'home' ? '/' : '/' . str_replace('__', '/', $name) . '/';
    }
    if ($type === 'services') {
        return '/services/' . $name . '/';
    }
    return '/' . $name . '/';
}

function load_content_file(string $type, string $name): ?array
{
    static $cache = [];
    $key = $type . '/' . $name;
    if (array_key_exists($key, $cache)) {
        return $cache[$key];
    }
    if (!preg_match('/^[a-z0-9_-]+$/', $name)) {
        return $cache[$key] = null;
    }
    $file = MPA_ROOT . '/content/' . $type . '/' . $name . '.php';
    if (!is_file($file)) {
        return $cache[$key] = null;
    }
    $data = require $file;
    if (!is_array($data)) {
        return $cache[$key] = null;
    }
    $data['_type'] = rtrim($type, 's');          // page | post | service
    $data['_name'] = $name;
    $data['path']  = $data['path'] ?? content_path_for($type, $name);
    return $cache[$key] = $data;
}

/** Find a content item by URL path. */
function find_content(string $path): ?array
{
    if ($path === '/') {
        return load_content_file('pages', 'home');
    }
    $trim = trim($path, '/');
    if ($trim === '') {
        return null;
    }
    $parts = explode('/', $trim);
    if (count($parts) === 2 && $parts[0] === 'services') {
        return load_content_file('services', $parts[1]);
    }
    if (count($parts) === 1) {
        return load_content_file('posts', $parts[0]) ?? load_content_file('pages', $parts[0]);
    }
    return load_content_file('pages', implode('__', $parts));
}

/** All items of a type, sorted (posts newest first, others by 'order' then title). */
function all_content(string $type): array
{
    static $cache = [];
    if (isset($cache[$type])) {
        return $cache[$type];
    }
    $items = [];
    foreach (glob(MPA_ROOT . '/content/' . $type . '/*.php') ?: [] as $file) {
        $item = load_content_file($type, basename($file, '.php'));
        if ($item && empty($item['draft'])) {
            $items[] = $item;
        }
    }
    if ($type === 'posts') {
        usort($items, fn($a, $b) => strcmp($b['date'] ?? '', $a['date'] ?? ''));
    } else {
        usort($items, fn($a, $b) => [($a['order'] ?? 100), $a['title']] <=> [($b['order'] ?? 100), $b['title']]);
    }
    return $cache[$type] = $items;
}

/* ------------------------------------------------------------------ */
/* Images                                                             */
/* ------------------------------------------------------------------ */

function image_manifest(): array
{
    static $m = null;
    if ($m === null) {
        $m = read_json_file(MPA_ROOT . '/assets/img/media/manifest.json', []);
    }
    return $m;
}

/**
 * Responsive <img>. $src is a site path such as /wp-content/uploads/2026/04/x.webp.
 * When resized variants exist in assets/img/media (built by tools/build_images.py),
 * a srcset is emitted.
 */
function img(string $src, string $alt, array $opt = []): string
{
    $manifest = image_manifest();
    $key = basename($src);
    $sizes = $opt['sizes'] ?? '(max-width: 768px) 100vw, 768px';
    $attrs = '';
    $w = $opt['width'] ?? null;
    $h = $opt['height'] ?? null;
    $srcset = '';
    if (isset($manifest[$key])) {
        $info = $manifest[$key];
        $w = $w ?? $info['w'];
        $h = $h ?? $info['h'];
        $parts = [];
        foreach ($info['variants'] as $vw => $vpath) {
            $parts[] = $vpath . ' ' . $vw . 'w';
        }
        if ($parts) {
            $srcset = ' srcset="' . e(implode(', ', $parts)) . '" sizes="' . e($sizes) . '"';
            // Use a mid-size variant as the default src for faster loads.
            $mid = $info['variants'][960] ?? reset($info['variants']);
            $src = $mid;
        }
    }
    if ($w && $h) {
        $attrs .= ' width="' . (int) $w . '" height="' . (int) $h . '"';
    }
    $eager = !empty($opt['eager']);
    $attrs .= $eager ? ' fetchpriority="high"' : ' loading="lazy"';
    $attrs .= ' decoding="async"';
    if (!empty($opt['class'])) {
        $attrs .= ' class="' . e($opt['class']) . '"';
    }
    return '<img src="' . e($src) . '"' . $srcset . ' alt="' . e($alt) . '"' . $attrs . '>';
}

/* ------------------------------------------------------------------ */
/* Icons (inline SVG, stroke style)                                   */
/* ------------------------------------------------------------------ */

function icon(string $name, string $class = 'icon'): string
{
    $p = [
        'phone'    => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/>',
        'mail'     => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        'check'    => '<path d="M20 6 9 17l-5-5"/>',
        'shield'   => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
        'hail'     => '<path d="M17.5 17H7a5 5 0 1 1 1.4-9.8A6 6 0 0 1 20 10a3.5 3.5 0 0 1-2.5 7Z"/><circle cx="8" cy="21" r=".8"/><circle cx="12" cy="20" r=".8"/><circle cx="16" cy="21" r=".8"/>',
        'wind'     => '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
        'storm'    => '<path d="M6 16.3A5 5 0 1 1 8.4 7.2 6 6 0 0 1 20 10a3.5 3.5 0 0 1-1 6.8"/><path d="m13 12-3 5h4l-3 5"/>',
        'hurricane'=> '<path d="M12 12m-2 0a2 2 0 1 0 4 0a2 2 0 1 0-4 0"/><path d="M14.5 6.5C13 4 9 3 6 4c3 0 5 2 5.5 4"/><path d="M9.5 17.5C11 20 15 21 18 20c-3 0-5-2-5.5-4"/><path d="M6.5 9.5C4 11 3 15 4 18c0-3 2-5 4-5.5"/><path d="M17.5 14.5C20 13 21 9 20 6c0 3-2 5-4 5.5"/>',
        'fire'     => '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3a2.5 2.5 0 0 0 2.5 2.8Z"/>',
        'smoke'    => '<path d="M3 12h11a3 3 0 1 0-3-3"/><path d="M3 16h15a3 3 0 1 1-3 3"/><path d="M3 8h5"/>',
        'water'    => '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5S12.5 5.5 12 3c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7Z"/>',
        'home'     => '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M9 22V12h6v10"/>',
        'building' => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
        'doc'      => '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5Z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
        'x-doc'    => '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5Z"/><path d="M14 2v6h6"/><path d="m9.5 12.5 5 5M14.5 12.5l-5 5"/>',
        'dollar'   => '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
        'clock'    => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'layers'   => '<path d="m12 2 10 5-10 5L2 7Z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
        'scale'    => '<path d="M12 3v18M7 21h10M3 7h18"/><path d="m6 7-3 7a3 3 0 0 0 6 0Z"/><path d="m18 7-3 7a3 3 0 0 0 6 0Z"/>',
        'search'   => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        'calc'     => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h4"/>',
        'clipboard'=> '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
        'map'      => '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        'calendar' => '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        'arrow'    => '<path d="M5 12h14M12 5l7 7-7 7"/>',
        'menu'     => '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'close'    => '<path d="M18 6 6 18M6 6l12 12"/>',
        'alert'    => '<path d="m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3Z"/><path d="M12 9v4M12 17h.01"/>',
        'thermo'   => '<path d="M14 4v10.5a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
        'droplets' => '<path d="M7 16.3c2.2 0 4-1.8 4-4 0-1.2-.6-2.3-1.8-3.2S7.2 7 7 5.7c-.3 1.3-1 2.6-2.2 3.5S3 11.1 3 12.3c0 2.2 1.8 4 4 4Z"/><path d="M12.6 6.6A11 11 0 0 0 14 3c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.9 6.9 0 0 1-11.8 4.9"/>',
        'camera'   => '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3Z"/><circle cx="12" cy="13" r="3"/>',
        'hammer'   => '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6M20.9 11.7 13.3 4a3 3 0 0 0-4.3 0L7.7 5.4l1.4 1.4a3 3 0 0 1 0 4.3"/>',
        'user'     => '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        'chat'     => '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/>',
        'printer'  => '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
        'download' => '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
        'refresh'  => '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
        'external' => '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
        'plus'     => '<path d="M12 5v14M5 12h14"/>',
    ];
    $inner = $p[$name] ?? $p['check'];
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $inner . '</svg>';
}

/* ------------------------------------------------------------------ */
/* Shortcodes used inside content bodies                              */
/* ------------------------------------------------------------------ */

function render_shortcodes(string $html, array $page = []): string
{
    $map = [
        '[[phone]]'        => '<a href="' . e(tel_link()) . '">' . e(cfg('phone_display')) . '</a>',
        '[[email]]'        => '<a href="mailto:' . e(cfg('public_email')) . '">' . e(cfg('public_email')) . '</a>',
        '[[license]]'      => e(cfg('license')),
        '[[company]]'      => e(cfg('company')),
    ];
    $html = strtr($html, $map);
    $html = preg_replace_callback('/\[\[(cta|form|cta-storm|services-grid|tools-grid|author-box)(?::([^\]]*))?\]\]/', function ($m) use ($page) {
        $arg = $m[2] ?? '';
        ob_start();
        switch ($m[1]) {
            case 'cta':
                component('cta-band', ['heading' => $arg ?: null]);
                break;
            case 'cta-storm':
                component('cta-storm');
                break;
            case 'form':
                component('claim-form', ['context' => $page['title'] ?? '']);
                break;
            case 'services-grid':
                component('services-grid');
                break;
            case 'tools-grid':
                component('tools-grid');
                break;
            case 'author-box':
                component('author-box');
                break;
        }
        return ob_get_clean();
    }, $html);
    return $html;
}

/** Include a reusable component from templates/components/<name>.php with variables. */
function component(string $name, array $vars = []): void
{
    $file = MPA_ROOT . '/templates/components/' . $name . '.php';
    if (!is_file($file)) {
        return;
    }
    extract($vars, EXTR_SKIP);
    include $file;
}

/** Add id attributes to <h2> tags so the table of contents can link to them. */
function add_heading_ids(string $html, array &$toc = []): string
{
    $used = [];
    return preg_replace_callback('/<h2(\s[^>]*)?>(.*?)<\/h2>/is', function ($m) use (&$toc, &$used) {
        $attrs = $m[1] ?? '';
        $text = trim(strip_tags($m[2]));
        if (preg_match('/\sid="([^"]+)"/', $attrs, $idm)) {
            $id = $idm[1];
        } else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-');
            $id = substr($id, 0, 60) ?: 'section';
            $base = $id;
            $i = 2;
            while (isset($used[$id])) {
                $id = $base . '-' . $i++;
            }
            $attrs .= ' id="' . $id . '"';
        }
        $used[$id] = true;
        $toc[] = ['id' => $id, 'text' => html_entity_decode($text, ENT_QUOTES, 'UTF-8')];
        return '<h2' . $attrs . '>' . $m[2] . '</h2>';
    }, $html);
}

/** Wrap bare <table> elements so they scroll horizontally on phones. */
function wrap_tables(string $html): string
{
    return preg_replace('/<table(?![^>]*data-nowrap)(.*?)<\/table>/is', '<div class="table-wrap"><table$1</table></div>', $html);
}

/* ------------------------------------------------------------------ */
/* Navigation                                                         */
/* ------------------------------------------------------------------ */

function primary_nav(): array
{
    return [
        ['Home', '/'],
        ['About Us', '/about-us/'],
        ['Services', '/services/', [
            ['Hail Damage Claims', '/services/hail-damage-claims/'],
            ['Roof Damage Claims', '/services/roof-damage-insurance-claims/'],
            ['Wind Damage Claims', '/services/wind-damage-claims/'],
            ['Storm Damage Claims', '/services/storm-damage-claims/'],
            ['Hurricane Damage Claims', '/services/hurricane-damage-claims/'],
            ['Fire Damage Claims', '/services/fire-damage-claims/'],
            ['Smoke Damage Claims', '/services/smoke-damage-claims/'],
            ['Water Damage Claims', '/services/water-damage-claims/'],
            ['Residential Claims', '/services/residential-property-claims/'],
            ['Commercial Claims', '/services/commercial-property-claims/'],
            ['Denied Claims', '/services/denied-insurance-claims/'],
            ['Underpaid Claims', '/services/underpaid-insurance-claims/'],
            ['Delayed Claims', '/services/delayed-insurance-claims/'],
            ['Claim Supplements', '/services/insurance-claim-supplements/'],
            ['Insurance Appraisal', '/services/insurance-appraisal/'],
            ['Estimate Reviews', '/services/insurance-estimate-review/'],
        ]],
        ['Resources', '/claim-tools/', [
            ['Claim Tools', '/claim-tools/'],
            ['Settlement Calculator', '/claim-calculator/'],
            ['Documentation Checklist', '/claim-documentation-checklist/'],
            ['Storm Event Lookup', '/storm-lookup/'],
            ['Live McAllen Weather', '/weather/'],
            ['Storm History', '/storm-history/'],
            ['Weather Events', '/weather-events/'],
            ['Local Building Codes', '/local-building-codes/'],
            ['Areas We Serve', '/service-areas/'],
        ]],
        ['Blog', '/blog/'],
        ['Contact', '/contact/'],
    ];
}

function footer_nav(): array
{
    return [
        ['Home', '/'],
        ['About Us', '/about-us/'],
        ['Services', '/services/'],
        ['Blog', '/blog/'],
        ['Contact', '/contact/'],
        ['Free Claim Review', '/free-claim-review/'],
        ['Live Weather', '/weather/'],
        ['Storm History', '/storm-history/'],
        ['Weather Events', '/weather-events/'],
        ['Local Building Codes', '/local-building-codes/'],
        ['Claim Tools', '/claim-tools/'],
        ['Areas We Serve', '/service-areas/'],
        ['Joseph Dittman', '/author/joseph-dittman/'],
        ['Privacy Policy', '/privacy-policy/'],
        ['Terms of Use', '/terms-of-use/'],
    ];
}

function asset_version(string $rel): string
{
    $f = MPA_ROOT . '/assets/' . $rel;
    return is_file($f) ? (string) filemtime($f) : '1';
}

/** Service cards shown in grids (path => [label, icon, blurb]). */
function service_cards(): array
{
    return [
        ['/services/hail-damage-claims/', 'Hail Damage Claims', 'hail', 'Roof, siding, window, and HVAC damage from Rio Grande Valley hailstorms.'],
        ['/services/roof-damage-insurance-claims/', 'Roof Damage Claims', 'home', 'Shingle, tile, and metal roof claims, from inspection to repair scope.'],
        ['/services/wind-damage-claims/', 'Wind Damage Claims', 'wind', 'Lifted shingles, fallen trees, and damage from straight-line winds.'],
        ['/services/storm-damage-claims/', 'Storm Damage Claims', 'storm', 'Losses from severe thunderstorms, including wind, hail, and rain intrusion.'],
        ['/services/hurricane-damage-claims/', 'Hurricane Damage Claims', 'hurricane', 'Tropical storm and hurricane claims, deductibles, and policy questions.'],
        ['/services/fire-damage-claims/', 'Fire Damage Claims', 'fire', 'Structure, contents, and additional living expense after a fire.'],
        ['/services/smoke-damage-claims/', 'Smoke Damage Claims', 'smoke', 'Soot, odor, and smoke residue that insurers often under-scope.'],
        ['/services/water-damage-claims/', 'Water Damage Claims', 'water', 'Sudden leaks, burst pipes, and storm-related water intrusion.'],
        ['/services/residential-property-claims/', 'Residential Property Claims', 'home', 'Help for McAllen homeowners with dwelling and contents claims.'],
        ['/services/commercial-property-claims/', 'Commercial Property Claims', 'building', 'Retail, office, warehouse, multifamily, and business interruption.'],
        ['/services/denied-insurance-claims/', 'Denied Claims', 'x-doc', 'Reviewing denial letters, policy language, and the evidence behind them.'],
        ['/services/underpaid-insurance-claims/', 'Underpaid Claims', 'dollar', 'When the insurer\'s estimate does not cover the real cost of repairs.'],
        ['/services/delayed-insurance-claims/', 'Delayed Claims', 'clock', 'Texas claim-handling deadlines and how to move a stalled claim forward.'],
        ['/services/insurance-claim-supplements/', 'Claim Supplements', 'layers', 'Adding missed items, code upgrades, and hidden damage to the scope.'],
        ['/services/insurance-appraisal/', 'Insurance Appraisal', 'scale', 'How the appraisal clause works when you and the insurer disagree on amount.'],
        ['/services/insurance-estimate-review/', 'Estimate Reviews', 'search', 'Line-by-line review of the carrier\'s Xactimate or Symbility estimate.'],
    ];
}
