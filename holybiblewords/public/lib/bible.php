<?php
// Data access and Bible helpers. No output.

const SITE_URL  = 'https://holybiblewords.com';
const SITE_NAME = 'Holy Bible Words';
const DATA_DIR  = __DIR__ . '/../data';
const ASSET_VER = '5';

function versions(): array {
    static $v;
    return $v ??= json_decode(file_get_contents(DATA_DIR . '/versions.json'), true);
}

function books(): array {
    static $b;
    if ($b === null) {
        $b = [];
        foreach (json_decode(file_get_contents(DATA_DIR . '/books.json'), true) as $i => $row) {
            $row['i'] = $i;
            $b[$row['slug']] = $row;
        }
    }
    return $b;
}

function book_by_index(int $i): ?array {
    return array_values(books())[$i] ?? null;
}

function book_name(array $book, string $ver): string {
    return $book['names'][versions()[$ver]['nameKey']];
}

/** Versions consulted, in order, when $ver lacks a verse (e.g. ml -> ceb -> ta). */
function version_chain(string $ver): array {
    return array_merge([$ver], versions()[$ver]['fallback'] ?? []);
}

/** Chapters of a book: list of lists of verse text (null = not available). */
function book_text(string $ver, string $slug): array {
    static $cache = [];
    $key = "$ver/$slug";
    if (!isset($cache[$key])) {
        $f = DATA_DIR . "/$ver/$slug.json";
        $cache[$key] = is_file($f) ? json_decode(file_get_contents($f), true)['c'] : [];
    }
    return $cache[$key];
}

function chapter_text(string $ver, string $slug, int $ch): array {
    return book_text($ver, $slug)[$ch - 1] ?? [];
}

function verse_text(string $ver, string $slug, int $ch, int $v): ?string {
    return chapter_text($ver, $slug, $ch)[$v - 1] ?? null;
}

function chapter_available(string $ver, string $slug, int $ch): int {
    return count(array_filter(chapter_text($ver, $slug, $ch), fn($x) => $x !== null));
}

function e(?string $s): string {
    return htmlspecialchars($s ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Verse text -> HTML. In the KJV, [brackets] mark translator-supplied words (italics). */
function verse_html(string $text, string $ver = 'ta'): string {
    return empty(versions()[$ver]['italics']) ? e($text) : preg_replace('/\[([^\]]*)\]/', '<i>$1</i>', e($text));
}

function verse_plain(string $text, string $ver = 'ta'): string {
    return empty(versions()[$ver]['italics']) ? $text : str_replace(['[', ']'], '', $text);
}

/**
 * A chapter as displayed in $ver: one row per rendered verse, each
 * ['n' => first verse, 'to' => last verse (ranges), 'text', 'src' => version the text came from].
 * Missing verses are filled from the version's fallback chain; verses a
 * translation joined with the previous one ("") extend that row's range.
 */
function resolve_chapter(string $ver, string $slug, int $c): array {
    static $cache = [];
    $key = "$ver/$slug/$c";
    if (isset($cache[$key])) return $cache[$key];
    $rows = [];
    $count = books()[$slug]['verses'][$c - 1] ?? 0;
    for ($n = 1; $n <= $count; $n++) {
        foreach (version_chain($ver) as $src) {
            $t = verse_text($src, $slug, $c, $n);
            if ($t === null) continue;
            if ($t === '') {
                $last = count($rows) - 1;
                if ($last >= 0 && $rows[$last]['src'] === $src && $rows[$last]['to'] === $n - 1) { $rows[$last]['to'] = $n; continue 2; }
                continue;   // joined verse whose start came from another version: keep looking
            }
            $rows[] = ['n' => $n, 'to' => $n, 'text' => $t, 'src' => $src];
            continue 2;
        }
    }
    return $cache[$key] = $rows;
}

/** The displayed row that contains verse $v, or null. */
function verse_display(string $ver, string $slug, int $c, int $v): ?array {
    foreach (resolve_chapter($ver, $slug, $c) as $row) if ($v >= $row['n'] && $v <= $row['to']) return $row;
    return null;
}

function range_label(array $row): string {
    return $row['n'] === $row['to'] ? (string)$row['n'] : $row['n'] . '–' . $row['to'];
}

function url_for(string $ver, ?string $book = null, ?int $ch = null, ?int $v = null): string {
    $u = "/$ver/";
    if ($book) $u .= "$book/";
    if ($ch) $u .= "$ch/";
    if ($v) $u .= "$v/";
    return $u;
}

function ref_label(array $book, string $ver, int $ch, ?int $v = null): string {
    return book_name($book, $ver) . " $ch" . ($v ? ":$v" : '');
}

// ---- reference parsing ("jn 3:16", "1 Cor 13", "Juan 3 16") ----

function norm_key(string $s): string {
    $num = ['i' => '1', 'ii' => '2', 'iii' => '3', 'first' => '1', 'second' => '2', 'third' => '3',
            '1st' => '1', '2nd' => '2', '3rd' => '3'];
    $s = preg_replace_callback('/^(iii|ii|i|first|second|third|1st|2nd|3rd)\s+/u',
        fn($m) => $num[$m[1]], mb_strtolower(trim($s)));
    return preg_replace('/[^a-z0-9]/u', '', $s);
}

function book_lookup(): array {
    static $map;
    if ($map === null) {
        $map = [];
        foreach (books() as $slug => $b) {
            $keys = array_merge([$slug, $b['names']['en'], $b['names']['ceb']], $b['abbr']);
            // Cebuano names without the "Mga" / "Mga Taga-" prefix
            $keys[] = preg_replace('/^(\d )?Mga (Taga-)?/u', '$1', $b['names']['ceb']);
            foreach ($keys as $k) {
                $k = norm_key($k);
                if ($k !== '' && !isset($map[$k])) $map[$k] = $slug;
            }
        }
    }
    return $map;
}

function find_book(string $name): ?string {
    $k = norm_key($name);
    if ($k === '') return null;
    $map = book_lookup();
    if (isset($map[$k])) return $map[$k];
    // unique prefix match ("revel", "phili" is ambiguous -> first in canon order)
    foreach (books() as $slug => $b) {
        foreach ([$slug, norm_key($b['names']['en']), norm_key($b['names']['ceb'])] as $cand) {
            if (strlen($k) >= 3 && str_starts_with($cand, $k)) return $slug;
        }
    }
    return null;
}

/** Returns [book, chapter|null, verse|null] or null. */
function parse_ref(string $q): ?array {
    $q = trim($q);
    if (!preg_match('/^((?:[1-3]|i{1,3})?\s*[\p{L}][\p{L}\s.\-]*?)\s*(\d+)?(?:\s*[:.\s]\s*(\d+))?\s*$/iu', $q, $m)) return null;
    $slug = find_book($m[1]);
    if (!$slug) return null;
    $book = books()[$slug];
    $ch = isset($m[2]) && $m[2] !== '' ? (int)$m[2] : null;
    $v = isset($m[3]) && $m[3] !== '' ? (int)$m[3] : null;
    if ($ch !== null && ($ch < 1 || $ch > count($book['verses']))) return null;
    if ($v !== null && ($v < 1 || $v > $book['verses'][$ch - 1])) return null;
    // single-chapter books: "jude 5" means verse 5
    if ($ch !== null && $v === null && count($book['verses']) === 1 && $ch > 1 && $ch <= $book['verses'][0]) {
        return [$slug, 1, $ch];
    }
    return [$slug, $ch, $v];
}

// ---- verse of the day ----

function votd_list(): array {
    static $l;
    return $l ??= json_decode(file_get_contents(DATA_DIR . '/votd.json'), true);
}

/** Same formula as app.js: whole days since 2024-01-01 modulo list length. */
function votd_for(string $ymd): array {
    $d = DateTimeImmutable::createFromFormat('!Y-m-d', $ymd, new DateTimeZone('UTC'));
    $epoch = new DateTimeImmutable('2024-01-01', new DateTimeZone('UTC'));
    $days = intdiv($d->getTimestamp() - $epoch->getTimestamp(), 86400);
    $list = votd_list();
    $n = count($list);
    return $list[(($days * 37) % $n + $n) % $n];
}

function site_today(): string {
    return (new DateTimeImmutable('now', new DateTimeZone('Asia/Manila')))->format('Y-m-d');
}

// ---- search ----

function search_fold(string $s): string {
    $s = mb_strtolower(str_replace(['[', ']'], '', $s));
    return strtr($s, ['á' => 'a', 'à' => 'a', 'é' => 'e', 'è' => 'e', 'í' => 'i', 'ó' => 'o', 'ú' => 'u', 'ñ' => 'n', '’' => "'", '‘' => "'"]);
}

/**
 * Full-text search. All words must match; "quoted phrases" match exactly.
 * Returns ['total' => int, 'results' => [[bookIndex, ch, v, text], ...]].
 */
function search(string $ver, string $q, string $testament = '', int $offset = 0, int $limit = 30): array {
    $terms = [];
    preg_match_all('/"([^"]+)"|(\S+)/u', search_fold($q), $mm, PREG_SET_ORDER);
    foreach ($mm as $m) {
        $t = trim($m[1] !== '' ? $m[1] : preg_replace('/[^\p{L}\p{N}\'-]/u', '', $m[2]));
        if ($t !== '') $terms[] = $t;
    }
    if (!$terms) return ['total' => 0, 'results' => [], 'terms' => []];
    $fh = fopen(DATA_DIR . "/$ver/search.tsv", 'r');
    $total = 0; $out = [];
    while (($line = fgets($fh)) !== false) {
        [$bi, $c, $v, $text] = explode("\t", rtrim($line, "\n"), 4);
        if ($testament === 'ot' && $bi >= 39) break;
        if ($testament === 'nt' && $bi < 39) continue;
        $f = search_fold($text);
        foreach ($terms as $t) if (!str_contains($f, $t)) continue 2;
        // whole-word check for single words so "love" doesn't match "glove"
        foreach ($terms as $t) {
            if (!preg_match('/(?<![\p{L}])' . preg_quote($t, '/') . '/u', $f)) continue 2;
        }
        if ($total >= $offset && count($out) < $limit) $out[] = [(int)$bi, (int)$c, (int)$v, $text];
        $total++;
    }
    fclose($fh);
    return ['total' => $total, 'results' => $out, 'terms' => $terms];
}

function highlight_terms(string $html, array $terms): string {
    foreach ($terms as $t) {
        $html = preg_replace('/(?<![\p{L}])(' . preg_quote(e($t), '/') . ')/iu', '<mark>$1</mark>', $html);
    }
    return $html;
}
