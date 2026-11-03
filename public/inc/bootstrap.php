<?php
/**
 * Shared constants and helpers. Every include file starts with
 * `defined('SCC') || exit;` so nothing under inc/, content/ or pages/
 * can be executed by requesting it directly.
 */
defined('SCC') || exit;

const SITE_NAME   = 'Solar CCTV Camera';
const SITE_ORIGIN = 'https://solarcctvcamera.com';
const SITE_EMAIL  = 'info@solarcctvcamera.com';
const SITE_TAGLINE = 'Independent solar security camera guides, tools and buying advice';
const GA_ID = 'GT-K54JDCWX';
const AMAZON_TAG = 'josephrayditt-20';
const BUILD_DATE = '2026-11-03';

define('ROOT', dirname(__DIR__));

/** Private settings (SMTP password) live outside the repo. */
function config(string $key, $default = null)
{
    static $cfg = null;
    if ($cfg === null) {
        $cfg = [];
        foreach ([dirname(ROOT) . '/scc-config.php', ROOT . '/inc/config.local.php'] as $f) {
            if (@is_file($f)) { $cfg = (array) (include $f); break; }
        }
    }
    return $cfg[$key] ?? $default;
}

function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return SITE_ORIGIN . $path;
}

function asset(string $path): string
{
    $f = ROOT . '/assets/' . $path;
    $v = @filemtime($f) ?: 1;
    return '/assets/' . $path . '?v=' . $v;
}

/** Responsive <img> for images processed into assets/img (name.webp + name-640.webp). */
function img(string $name, string $alt, array $o = []): string
{
    $name = preg_replace('/\.webp$/', '', $name);
    $file = ROOT . "/assets/img/$name.webp";
    [$w, $h] = @getimagesize($file) ?: [1200, 800];
    $src = "/assets/img/$name.webp";
    $srcset = is_file(ROOT . "/assets/img/$name-640.webp") ? " srcset=\"/assets/img/$name-640.webp 640w, $src {$w}w\"" : '';
    $sizes = e($o['sizes'] ?? '(max-width: 760px) 100vw, 760px');
    $lazy = !empty($o['eager']) ? 'fetchpriority="high"' : 'loading="lazy" decoding="async"';
    $cls = isset($o['class']) ? ' class="' . e($o['class']) . '"' : '';
    return "<img src=\"$src\"$srcset sizes=\"$sizes\" width=\"$w\" height=\"$h\" alt=\"" . e($alt) . "\" $lazy$cls>";
}

function img_url(string $name): string
{
    return abs_url('/assets/img/' . preg_replace('/\.webp$/', '', $name) . '.webp');
}

function amazon(string $short): string
{
    return 'https://amzn.to/' . $short;
}

function fmt_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

function slugify(string $s): string
{
    $s = strtolower(html_entity_decode(strip_tags($s), ENT_QUOTES, 'UTF-8'));
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    return trim($s, '-');
}

function json_ld(array $data): string
{
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . "</script>\n";
}

/** Inline SVG icon set (stroke icons, 24x24). */
function icon(string $name, int $size = 20): string
{
    static $p = [
        'sun' => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'moon' => '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
        'battery' => '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2"/><path d="M6 10v4M10 10v4"/>',
        'camera' => '<path d="M3 7h11l3 3v4l-3 3H3z"/><circle cx="9" cy="12" r="2.5"/><path d="M17 10l4-2v8l-4-2"/>',
        'wifi' => '<path d="M5 12.6a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="19.5" r="1"/>',
        'signal' => '<path d="M4 20v-3M9 20v-7M14 20V9M19 20V4"/>',
        'panel' => '<path d="M3 4h18l-2 11H5z"/><path d="M4 9.5h16M9 4l-1 11M15 4l1 11M12 15v5M8 20h8"/>',
        'angle' => '<path d="M4 20h16"/><path d="M4 20 16 6"/><path d="M10 20a6 6 0 0 0-1.8-4.3"/>',
        'calc' => '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/>',
        'shield' => '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="m9 12 2 2 4-4"/>',
        'eye' => '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        'map' => '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
        'home' => '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/>',
        'tool' => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
        'book' => '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
        'arrow' => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'check' => '<path d="m5 12 5 5 9-10"/>',
        'x' => '<path d="M6 6l12 12M18 6 6 18"/>',
        'alert' => '<path d="M12 3 2 21h20z"/><path d="M12 10v5M12 18v.5"/>',
        'cloud' => '<path d="M7 18a4 4 0 0 1-.6-8 6 6 0 0 1 11.4 1.5A3.5 3.5 0 0 1 17.5 18z"/>',
        'snow' => '<path d="M12 2v20M4.9 7l14.2 10M4.9 17 19.1 7"/>',
        'rv' => '<path d="M2 16V7a2 2 0 0 1 2-2h12l4 5v6z"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M6 9h4v3H6z"/>',
        'barn' => '<path d="M3 21V10l9-6 9 6v11z"/><path d="M9 21v-6h6v6M9 15l6 6M15 15l-6 6"/>',
        'tree' => '<path d="M12 2 6 11h3l-4 6h14l-4-6h3z"/><path d="M12 17v5"/>',
        'gate' => '<path d="M3 21V5M21 21V5M3 9h18M3 17h18M7 9v8M11 9v8M15 9v8M19 9v8"/>',
        'car' => '<path d="M3 13l2-6h14l2 6v5H3z"/><circle cx="7" cy="15.5" r="1.5"/><circle cx="17" cy="15.5" r="1.5"/>',
        'tent' => '<path d="M3 20 12 4l9 16z"/><path d="M12 4v16M9 20l3-6 3 6"/>',
        'building' => '<path d="M4 21V3h10v18M14 9h6v12"/><path d="M7 7h2M7 11h2M7 15h2M17 13h0M17 17h0"/>',
        'light' => '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
        'key' => '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
        'mail' => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'sd' => '<path d="M7 2h8l4 4v16H7z"/><path d="M10 6v3M13 6v3M16 6v3"/>',
        'dollar' => '<path d="M12 2v20M17 6.5C17 4.6 14.8 4 12 4S7 4.9 7 7c0 4.6 10 2.4 10 7 0 2-2.2 3-5 3s-5-.7-5-2.8"/>',
        'refresh' => '<path d="M20 11a8 8 0 0 0-14-5L3 9M4 13a8 8 0 0 0 14 5l3-3"/><path d="M3 4v5h5M21 20v-5h-5"/>',
        'plug' => '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0z"/><path d="M12 18v4"/>',
        'drill' => '<path d="M3 8h11v6H3z"/><path d="M14 10h7M8 14v6h3"/>',
        'menu' => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'star' => '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
        'compass' => '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
        'zap' => '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    ];
    $d = $p[$name] ?? $p['sun'];
    return "<svg class=\"ic\" width=\"$size\" height=\"$size\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\">$d</svg>";
}
