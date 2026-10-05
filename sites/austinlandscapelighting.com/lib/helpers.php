<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

/** HTML-escape for text and attribute contexts. */
function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Absolute URL for a site path. */
function url(string $path = '/'): string
{
    return SITE_ORIGIN . $path;
}

/** Path to an image in assets/img (full size or thumbnail). */
function img(string $name, bool $thumb = false): string
{
    return $thumb ? "/assets/img/thumbs/{$name}.webp" : "/assets/img/{$name}.webp";
}

/** <img> tag with both sizes via srcset, lazy by default. */
function picture(string $name, string $alt, array $opts = []): string
{
    $w = $opts['width'] ?? 1600;
    $h = $opts['height'] ?? 900;
    $lazy = ($opts['eager'] ?? false) ? 'eager' : 'lazy';
    $fetch = ($opts['eager'] ?? false) ? ' fetchpriority="high"' : '';
    $class = isset($opts['class']) ? ' class="' . e($opts['class']) . '"' : '';
    $sizes = $opts['sizes'] ?? '(max-width: 760px) 100vw, 50vw';
    return sprintf(
        '<img src="%s" srcset="%s 720w, %s 1600w" sizes="%s" alt="%s" width="%d" height="%d" loading="%s" decoding="async"%s%s>',
        img($name), img($name, true), img($name), e($sizes), e($alt), $w, $h, $lazy, $fetch, $class
    );
}

/** Plain-text word count for an HTML fragment. */
function word_count(string $html): int
{
    return str_word_count(strip_tags($html));
}

/** Reading time in minutes. */
function reading_time(string $html): int
{
    return max(1, (int) ceil(word_count($html) / 220));
}

/** Format an ISO date as "July 19, 2026". */
function nice_date(string $iso): string
{
    $t = strtotime($iso);
    return $t ? date('F j, Y', $t) : $iso;
}

/** Add id attributes to <h2> headings and return [html, toc]. */
function with_heading_ids(string $html): array
{
    $toc = [];
    $html = preg_replace_callback('/<h2([^>]*)>(.*?)<\/h2>/s', function ($m) use (&$toc) {
        $text = trim(strip_tags($m[2]));
        $id = slugify($text);
        $n = 1;
        $base = $id;
        $ids = array_column($toc, 'id');
        while (in_array($id, $ids, true)) {
            $id = $base . '-' . (++$n);
        }
        $toc[] = ['id' => $id, 'text' => $text];
        return '<h2 id="' . e($id) . '"' . $m[1] . '>' . $m[2] . '</h2>';
    }, $html);
    return [$html, $toc];
}

function slugify(string $s): string
{
    $s = strtolower(trim($s));
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    return trim($s, '-') ?: 'section';
}

/** Current year for the footer. */
function year(): string
{
    return date('Y');
}

/** Redirect helper. */
function redirect(string $to, int $code = 301): never
{
    header('Location: ' . $to, true, $code);
    exit;
}

/** Shuffle-free deterministic pick of N items from a list, offset by a seed string. */
function pick(array $items, int $n, string $seed = ''): array
{
    if (!$items) {
        return [];
    }
    $offset = $seed === '' ? 0 : (crc32($seed) % count($items));
    $out = [];
    for ($i = 0; $i < min($n, count($items)); $i++) {
        $out[] = $items[($offset + $i) % count($items)];
    }
    return $out;
}
