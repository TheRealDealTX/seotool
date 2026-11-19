<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Small, safe Markdown subset for user posts and comments.
 *
 * Everything is HTML-escaped first, so no raw HTML from users ever reaches the
 * page. Supported: paragraphs, line breaks, ## and ### headings, > quotes,
 * - / * / 1. lists, ``` code blocks, `code`, **bold**, *italic*, ~~strike~~,
 * [text](https://link), bare https:// links, and --- rules.
 * Links are rel="nofollow ugc noopener" (user-generated content).
 */
function md(string $src, bool $allowHeadings = true): string
{
    $src = str_replace(["\r\n", "\r"], "\n", $src);
    $src = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $src) ?? '';
    $lines = explode("\n", $src);
    $out = [];
    $para = [];
    $list = null;       // ['ul'|'ol', items[]]
    $quote = [];
    $code = null;

    $flushPara = function () use (&$para, &$out) {
        if ($para) {
            $out[] = '<p>' . implode("<br>\n", array_map('md_inline', $para)) . '</p>';
            $para = [];
        }
    };
    $flushList = function () use (&$list, &$out) {
        if ($list) {
            $out[] = '<' . $list[0] . '>' . implode('', array_map(fn($i) => '<li>' . md_inline($i) . '</li>', $list[1])) . '</' . $list[0] . '>';
            $list = null;
        }
    };
    $flushQuote = function () use (&$quote, &$out, $allowHeadings) {
        if ($quote) {
            $out[] = '<blockquote>' . md(implode("\n", $quote), $allowHeadings) . '</blockquote>';
            $quote = [];
        }
    };

    foreach ($lines as $line) {
        if ($code !== null) {
            if (preg_match('/^\s*```\s*$/', $line)) {
                $out[] = '<pre><code>' . e(implode("\n", $code)) . '</code></pre>';
                $code = null;
            } else {
                $code[] = $line;
            }
            continue;
        }
        if (preg_match('/^\s*```/', $line)) {
            $flushPara(); $flushList(); $flushQuote();
            $code = [];
            continue;
        }
        if (preg_match('/^\s*>\s?(.*)$/', $line, $m)) {
            $flushPara(); $flushList();
            $quote[] = $m[1];
            continue;
        }
        $flushQuote();
        if (trim($line) === '') {
            $flushPara(); $flushList();
            continue;
        }
        if (preg_match('/^\s*(?:-{3,}|\*{3,})\s*$/', $line)) {
            $flushPara(); $flushList();
            $out[] = '<hr>';
            continue;
        }
        if ($allowHeadings && preg_match('/^(#{1,3})\s+(.+)$/', $line, $m)) {
            $flushPara(); $flushList();
            $lvl = max(2, strlen($m[1]) + 1);   // # -> h2 (the page owns h1)
            $lvl = min($lvl, 4);
            $out[] = "<h$lvl>" . md_inline(rtrim($m[2], ' #')) . "</h$lvl>";
            continue;
        }
        if (preg_match('/^\s*[-*+]\s+(.+)$/', $line, $m)) {
            $flushPara();
            if (!$list || $list[0] !== 'ul') { $flushList(); $list = ['ul', []]; }
            $list[1][] = $m[1];
            continue;
        }
        if (preg_match('/^\s*\d{1,3}[.)]\s+(.+)$/', $line, $m)) {
            $flushPara();
            if (!$list || $list[0] !== 'ol') { $flushList(); $list = ['ol', []]; }
            $list[1][] = $m[1];
            continue;
        }
        if ($list && preg_match('/^\s{2,}(.+)$/', $line, $m)) {   // list item continuation
            $list[1][count($list[1]) - 1] .= ' ' . $m[1];
            continue;
        }
        $flushList();
        $para[] = $line;
    }
    if ($code !== null) {
        $out[] = '<pre><code>' . e(implode("\n", $code)) . '</code></pre>';
    }
    $flushPara(); $flushList(); $flushQuote();
    return implode("\n", $out);
}

function md_inline(string $s): string
{
    $s = e($s);
    $tokens = [];
    $stash = function (string $html) use (&$tokens): string {
        $tokens[] = $html;
        return "\x01" . (count($tokens) - 1) . "\x02";
    };
    // inline code first: nothing inside is formatted
    $s = preg_replace_callback('/`([^`]+)`/', fn($m) => $stash('<code>' . $m[1] . '</code>'), $s);
    // [text](url)
    $s = preg_replace_callback('/\[([^\]]{1,200})\]\((https?:\/\/[^\s)]{1,500}|\/(?!\/)[^\s)]{0,500})\)/i', function ($m) use ($stash) {
        $url = html_entity_decode($m[2], ENT_QUOTES);
        if ($url[0] === '/') {   // site-relative link
            return $stash('<a href="' . e($url) . '">' . $m[1] . '</a>');
        }
        return $stash(md_link($url, $m[1]));
    }, $s);
    // bare links
    $s = preg_replace_callback('/(?<![\w\/])(https?:\/\/[^\s<]{2,500})/i', function ($m) use ($stash) {
        $url = $m[1];
        $trail = '';
        while ($url !== '' && str_contains('.,;:!?)', substr($url, -1))) {
            $trail = substr($url, -1) . $trail;
            $url = substr($url, 0, -1);
        }
        $raw = html_entity_decode($url, ENT_QUOTES);
        $label = e(mb_strimwidth(preg_replace('#^https?://(www\.)?#', '', $raw), 0, 60, '…'));
        return $stash(md_link($raw, $label)) . $trail;
    }, $s);
    $s = preg_replace('/\*\*(?=\S)(.+?)(?<=\S)\*\*/', '<strong>$1</strong>', $s);
    $s = preg_replace('/__(?=\S)(.+?)(?<=\S)__/', '<strong>$1</strong>', $s);
    $s = preg_replace('/(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])/', '<em>$1</em>', $s);
    $s = preg_replace('/(?<![\w_])_(?=\S)(.+?)(?<=\S)_(?![\w_])/', '<em>$1</em>', $s);
    $s = preg_replace('/~~(?=\S)(.+?)(?<=\S)~~/', '<del>$1</del>', $s);
    return preg_replace_callback("/\x01(\d+)\x02/", fn($m) => $tokens[(int)$m[1]], $s);
}

function md_link(string $url, string $labelHtml): string
{
    $parts = parse_url($url);
    if (!$parts || !in_array(strtolower($parts['scheme'] ?? ''), ['http', 'https'], true) || empty($parts['host'])) {
        return $labelHtml;
    }
    $own = parse_url(cfg('base_url'), PHP_URL_HOST);
    $host = strtolower($parts['host']);
    if ($host === $own || $host === 'www.' . $own) {
        return '<a href="' . e($url) . '">' . $labelHtml . '</a>';
    }
    return '<a href="' . e($url) . '" rel="nofollow ugc noopener" target="_blank">' . $labelHtml . '</a>';
}

/** Count external links in raw markdown (used by the spam filter). */
function md_link_count(string $src): int
{
    return preg_match_all('#https?://#i', $src);
}

function md_plain(string $src): string
{
    $html = preg_replace('#<(?:/p|/li|br|/h\d|/blockquote|/pre)[^>]*>#i', '$0 ', md($src));
    return trim(preg_replace('/\s+/u', ' ', html_entity_decode(strip_tags($html), ENT_QUOTES)));
}
