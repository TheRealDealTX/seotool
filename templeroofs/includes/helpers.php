<?php
/** Small shared helpers. */
defined('TR_ROOT') || exit;

/** Escape for HTML text and attribute context. */
function e($value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');
}

function cfg(string $key, $default = null)
{
    return $GLOBALS['TR_CONFIG'][$key] ?? $default;
}

function catalog(string $key): array
{
    return $GLOBALS['TR_CATALOG'][$key] ?? [];
}

/** Absolute URL for a root-relative path ("/about/" -> "https://templeroofs.com/about/"). */
function abs_url(string $path = '/'): string
{
    return rtrim(cfg('base_url'), '/') . '/' . ltrim($path, '/');
}

/** Cache-busted asset URL. */
function asset(string $path): string
{
    $file = TR_ROOT . '/assets/' . ltrim($path, '/');
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : TR_VERSION;
    return '/assets/' . ltrim($path, '/') . '?v=' . $v;
}

/**
 * "Now" in America/Chicago. On the command line only, TR_NOW (e.g.
 * TR_NOW=2026-10-20) can be set to preview scheduled content during QA.
 */
function tr_now(): DateTimeImmutable
{
    $tz = new DateTimeZone(cfg('timezone'));
    if (PHP_SAPI === 'cli' && getenv('TR_NOW')) {
        return new DateTimeImmutable(getenv('TR_NOW'), $tz);
    }
    return new DateTimeImmutable('now', $tz);
}

function tel_href(): string
{
    return 'tel:' . cfg('phone_e164');
}

function format_date(DateTimeInterface $d): string
{
    return $d->format('F j, Y');
}

/** Words in an HTML fragment. */
function word_count(string $html): int
{
    $text = trim(preg_replace('/\s+/u', ' ', strip_tags(str_replace('<', ' <', $html))));
    return $text === '' ? 0 : count(explode(' ', $text));
}

function reading_minutes(string $html): int
{
    return max(1, (int) round(word_count($html) / 225));
}

/** Image manifest (dimensions, alt text, credits) produced with the images. */
function image_manifest(): array
{
    static $m = null;
    if ($m === null) {
        $file = TR_ROOT . '/assets/images/manifest.json';
        $m = is_file($file) ? (json_decode((string) file_get_contents($file), true) ?: []) : [];
    }
    return $m;
}

/**
 * Responsive <img> for an image key. Files: /assets/images/{key}-{480|800|1600}.webp
 * Options: sizes, class, eager (bool), priority (bool), alt (string).
 */
function img(string $key, string $alt = '', array $o = []): string
{
    $m = image_manifest()[$key] ?? [];
    $w = (int) ($m['w'] ?? 1600);
    $h = (int) ($m['h'] ?? 1067);
    // The manifest alt text was written while viewing each photo, so it is
    // preferred over page-supplied text whenever it exists.
    if (!empty($m['alt']) && empty($o['decorative'])) {
        $alt = $m['alt'];
    }
    $base = '/assets/images/' . $key;
    $srcset = [];
    foreach ([480, 800, 1600] as $size) {
        if (is_file(TR_ROOT . $base . '-' . $size . '.webp')) {
            $srcset[] = $base . '-' . $size . '.webp ' . $size . 'w';
        }
    }
    $src = $base . '-800.webp';
    $attrs = [
        'src'      => $src,
        'srcset'   => implode(', ', $srcset),
        'sizes'    => $o['sizes'] ?? '(max-width: 768px) 100vw, 50vw',
        'width'    => $w,
        'height'   => $h,
        'alt'      => $alt,
        'decoding' => 'async',
    ];
    if (!empty($o['class'])) {
        $attrs['class'] = $o['class'];
    }
    if (!empty($o['priority'])) {
        $attrs['fetchpriority'] = 'high';
    } elseif (empty($o['eager'])) {
        $attrs['loading'] = 'lazy';
    }
    $out = '<img';
    foreach ($attrs as $k => $v) {
        $out .= ' ' . $k . '="' . e($v) . '"';
    }
    return $out . '>';
}

/** Inline SVG icon from the sprite in the footer. */
function icon(string $name, string $class = ''): string
{
    return '<svg class="icon ' . e($class) . '" aria-hidden="true" focusable="false"><use href="#i-' . e($name) . '"></use></svg>';
}

/** Send a JSON response and stop. */
function json_out(array $data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

/** Atomically write a file inside storage. */
function storage_write(string $file, string $data): bool
{
    $dir = dirname($file);
    if (!is_dir($dir) && !@mkdir($dir, 0755, true)) {
        return false;
    }
    $tmp = $file . '.' . bin2hex(random_bytes(4)) . '.tmp';
    if (@file_put_contents($tmp, $data, LOCK_EX) === false) {
        return false;
    }
    return @rename($tmp, $file);
}

/** Visitor IP (only used hashed, for rate limiting). */
function client_ip(): string
{
    return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
}
