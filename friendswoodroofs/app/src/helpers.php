<?php
declare(strict_types=1);

/** Escape for HTML text and attribute context. */
function e(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');
}

/** Read a site setting with dot notation, e.g. config('weather.zoom'). */
function config(string $key, mixed $default = null): mixed
{
    $value = $GLOBALS['FR_CONFIG'] ?? [];
    foreach (explode('.', $key) as $part) {
        if (!is_array($value) || !array_key_exists($part, $value)) {
            return $default;
        }
        $value = $value[$part];
    }
    return $value;
}

/** Absolute production URL for a site path ("/services/" -> "https://…/services/"). */
function abs_url(string $path = '/'): string
{
    return rtrim((string) config('base_url'), '/') . '/' . ltrim($path, '/');
}

/** Root-relative asset URL with a cache-busting version from the file's mtime. */
function asset(string $path): string
{
    $path = ltrim($path, '/');
    $file = FR_PUBLIC . '/' . $path;
    $v = is_file($file) ? (string) filemtime($file) : '1';
    return '/' . $path . '?v=' . $v;
}

function phone_display(): string
{
    return (string) config('phone_display');
}

function phone_href(): string
{
    return 'tel:' . (string) config('phone_tel');
}

/** Render a partial template with local variables. */
function partial(string $name, array $vars = []): void
{
    extract($vars, EXTR_SKIP);
    require FR_APP . '/templates/partials/' . $name . '.php';
}

/** Return a partial's output as a string. */
function partial_html(string $name, array $vars = []): string
{
    ob_start();
    partial($name, $vars);
    return (string) ob_get_clean();
}

/** Inline SVG icon from the small built-in set (decorative, aria-hidden). */
function icon(string $name, string $class = 'icon'): string
{
    static $paths = [
        'phone'    => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
        'clipboard'=> '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M9 12h6M9 16h6"/>',
        'arrow'    => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'check'    => '<path d="M20 6 9 17l-5-5"/>',
        'wrench'   => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
        'home'     => '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'search'   => '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
        'storm'    => '<path d="M17.5 17H7a5 5 0 1 1 1.6-9.7A6 6 0 0 1 20 9.5 3.8 3.8 0 0 1 17.5 17z"/><path d="m13 13-2 4h3l-2 4"/>',
        'layers'   => '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
        'shield'   => '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>',
        'calendar' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        'droplet'  => '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
        'map'      => '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
        'menu'     => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'close'    => '<path d="M6 6l12 12M18 6 6 18"/>',
        'chevron'  => '<path d="m6 9 6 6 6-6"/>',
        'copy'     => '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
        'alert'    => '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
        'info'     => '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
        'sun'      => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'leaf'     => '<path d="M5 19c10 0 14-6 14-15C10 4 5 9 5 15v4z"/><path d="M5 19 14 10"/>',
        'external' => '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    ];
    $body = $paths[$name] ?? '';
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $body . '</svg>';
}

/** Format a Y-m-d date for display, e.g. "October 1, 2026". */
function display_date(string $ymd): string
{
    $d = DateTimeImmutable::createFromFormat('!Y-m-d', $ymd, new DateTimeZone((string) config('timezone', 'UTC')));
    return $d ? $d->format('F j, Y') : $ymd;
}

/** Responsive <img> for a photo in /assets/img/ (generated at 480/960/1600 widths). */
function photo(string $key, string $sizes = '100vw', bool $eager = false, string $class = ''): string
{
    $img = image_info($key);
    if (!$img) {
        return '';
    }
    $srcset = [];
    foreach ($img['widths'] as $w) {
        $srcset[] = '/assets/img/' . $key . '-' . $w . '.webp ' . $w . 'w';
    }
    $default = '/assets/img/' . $key . '-' . $img['widths'][1] . '.webp';
    $attrs = [
        'src'      => $default,
        'srcset'   => implode(', ', $srcset),
        'sizes'    => $sizes,
        'width'    => (string) $img['w'],
        'height'   => (string) $img['h'],
        'alt'      => $img['alt'],
        'decoding' => 'async',
    ];
    if ($eager) {
        $attrs['fetchpriority'] = 'high';
    } else {
        $attrs['loading'] = 'lazy';
    }
    if ($class !== '') {
        $attrs['class'] = $class;
    }
    $html = '<img';
    foreach ($attrs as $k => $v) {
        $html .= ' ' . $k . '="' . e($v) . '"';
    }
    return $html . '>';
}

function image_info(string $key): ?array
{
    static $images = null;
    $images ??= require FR_APP . '/content/images.php';
    return $images[$key] ?? null;
}

/** Short credit line for a photo ("Photo: Name, CC BY 4.0"). */
function photo_credit(string $key): string
{
    $img = image_info($key);
    if (!$img) {
        return '';
    }
    return 'Illustrative photo: ' . e($img['author']) . ', '
        . ($img['license_url'] ? '<a href="' . e($img['license_url']) . '" rel="noopener license">' . e($img['license']) . '</a>' : e($img['license']))
        . ' &middot; <a href="/image-credits/">Image credits</a>';
}

/** Current request path (no query string), always starting with "/". */
function request_path(): string
{
    // Not parse_url(): it would read a leading "//" as a host name.
    $path = rawurldecode(strtok((string) ($_SERVER['REQUEST_URI'] ?? '/'), '?#') ?: '/');
    return str_starts_with($path, '/') ? $path : '/' . $path;
}

function client_ip(): string
{
    // Hostinger terminates TLS at a proxy; REMOTE_ADDR is still the visitor or
    // the proxy. Only used (hashed) for rate limiting, never stored in clear.
    return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
}
