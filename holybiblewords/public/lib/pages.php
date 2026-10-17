<?php
// Page builders. Each returns the array render_page() takes.

function version_alternates(callable $path): array {
    $alt = [];
    foreach (versions() as $k => $_) $alt[$k] = $path($k);
    return $alt;
}

function books_grid(string $ver, string $testament): string {
    $h = '<ul class="book-grid">';
    foreach (books() as $slug => $b) {
        if ($b['t'] !== $testament) continue;
        $partial = $b['available'][$ver] === 0 ? ' class="na" title="Not yet available in ' . e(versions()[$ver]['label']) . '"' : '';
        $h .= '<li><a href="' . url_for($ver, $slug) . '"' . $partial . ' data-book="' . $slug . '">'
            . e(book_name($b, $ver)) . '<small>' . count($b['verses']) . '</small></a></li>';
    }
    return $h . '</ul>';
}

function votd_card(string $ver, string $ymd, bool $h1 = false): string {
    [$slug, $c, $v] = votd_for($ymd);
    $book = books()[$slug];
    $row = verse_display($ver, $slug, $c, $v);
    $text = $row['text'];
    $shownVer = $row['src'];
    $date = DateTimeImmutable::createFromFormat('!Y-m-d', $ymd)->format('l, F j, Y');
    $tag = $h1 ? 'h1' : 'h2';
    $note = fill_note($ver, $shownVer);
    return '<section class="votd" data-votd data-date="' . $ymd . '" data-ver="' . $ver . '" data-ref="' . "$slug.$c.$v" . '">'
        . '<div class="votd-head"><' . $tag . '>' . icon('sun') . ' Verse of the Day</' . $tag . '><time datetime="' . $ymd . '">' . $date . '</time></div>'
        . '<blockquote class="votd-text" lang="' . e(versions()[$shownVer]['lang']) . '">' . verse_html($text, $shownVer) . '</blockquote>'
        . '<p class="votd-ref"><a href="' . url_for($ver, $slug, $c, $v) . '">' . e(book_name($book, $shownVer) . " $c:" . range_label($row)) . ' <span class="badge">' . e(versions()[$shownVer]['short']) . '</span></a></p>'
        . $note
        . '<div class="votd-actions">'
        . '<button class="btn" type="button" data-action="votd-done">' . icon('check') . ' Mark as read</button>'
        . '<a class="btn ghost" href="' . url_for($ver, $slug, $c) . '#v' . $v . '">' . icon('book') . ' Read chapter</a>'
        . '<button class="btn ghost" type="button" data-action="explain-votd">' . icon('bulb') . ' Explain</button>'
        . '<button class="btn ghost" type="button" data-action="share-votd">' . icon('share') . ' Share</button>'
        . '<button class="btn ghost" type="button" data-action="image-votd">' . icon('image') . ' Image</button>'
        . '</div>'
        . '<div class="streak" data-streak hidden></div></section>';
}

/** "Not yet available in X — showing Y." when a fill-in version is used. */
function fill_note(string $ver, string $src): string {
    if ($src === $ver) return '';
    return '<p class="note">Not yet available in ' . e(versions()[$ver]['label']) . ' — showing ' . e(versions()[$src]['label']) . '.</p>';
}

/** Credit lines for every version whose text appears on a page. */
function credits(array $vers): string {
    $h = '';
    foreach (array_unique($vers) as $k) {
        $v = versions()[$k];
        $title = $v['fullTitle'] ?? $v['label'];
        $h .= '<p class="ver-credit">' . (str_starts_with($v['copyright'], $title) ? '' : e($title) . ' — ') . e($v['copyright'])
            . (isset($v['notice']) ? ' ' . e($v['notice']) : '')
            . (isset($v['license']) ? ' <a href="' . e($v['license']) . '" rel="license noopener" target="_blank">License</a>' : '') . '</p>';
    }
    return $h;
}

function jump_box(string $ver, string $value = '', bool $autofocus = false): string {
    return '<form class="jump" action="/search/" method="get" role="search">'
        . '<input type="hidden" name="v" value="' . e($ver) . '">'
        . '<label class="sr-only" for="q">Search the Bible or go to a verse</label>'
        . '<input id="q" name="q" type="search" value="' . e($value) . '" placeholder="Search, or type a verse: John 3:16" autocomplete="off" enterkeyhint="search"' . ($autofocus ? ' autofocus' : '') . '>'
        . '<button type="submit" aria-label="Search">' . icon('search') . '</button></form>';
}

function page_home(): array {
    $ver = 'ta';
    $today = site_today();
    $popular = [['john', 3], ['psalms', 23], ['genesis', 1], ['romans', 8], ['1corinthians', 13], ['matthew', 5], ['proverbs', 3], ['isaiah', 40]];
    $pop = '';
    foreach ($popular as [$s, $c]) {
        $pop .= '<a class="chip" href="' . url_for($ver, $s, $c) . '" data-keep-ver>' . e(ref_label(books()[$s], $ver, $c)) . '</a>';
    }
    $vcards = '';
    foreach (versions() as $k => $v) {
        $n = array_sum(array_map(fn($b) => $b['available'][$k], books()));
        $pct = round($n / 31102 * 100);
        $vcards .= '<a class="ver-card" href="/' . $k . '/" data-ver="' . $k . '"><strong>' . e($v['label']) . '</strong>'
            . '<span>' . e($v['desc']) . ($pct < 100 ? " · $pct% available, more coming" : '') . '</span>'
            . icon('right') . '</a>';
    }
    $body = '<section class="hero"><div class="wrap">'
        . '<h1>Read the Holy Bible Online</h1>'
        . '<p class="lead">The King James Version and Ang Pulong sa Dios (Cebuano) in one place. Jump to any chapter or verse, switch versions without losing your place, and get a new verse every day.</p>'
        . jump_box($ver)
        . '<div class="chips">' . $pop . '</div>'
        . '</div></section>'
        . '<div class="wrap home-grid">'
        . votd_card($ver, $today)
        . '<section class="continue" data-continue hidden><h2>Continue reading</h2><a class="continue-link" href="#"></a></section>'
        . '<section><h2>Choose a version</h2><div class="ver-cards">' . $vcards . '</div></section>'
        . '</div>'
        . '<div class="wrap"><section class="books-section"><h2>Old Testament</h2>' . books_grid($ver, 'ot') . '</section>'
        . '<section class="books-section"><h2>New Testament</h2>' . books_grid($ver, 'nt') . '</section>'
        . features_strip()
        . blog_teasers()
        . recommended_bibles()
        . '</div>';
    return [
        'title' => 'Holy Bible Words | Read The Bible Online',
        'description' => 'Explore the Holy Bible online with Holy Bible Words – the complete King James Version and Ang Pulong sa Dios, easy chapter and verse navigation, and an inspiring verse of the day.',
        'canonical' => '/', 'body' => $body, 'type' => 'home', 'ver' => $ver,
        'switch' => version_alternates(fn($k) => "/$k/"),
        'jsonld' => [
            ['@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL, 'name' => SITE_NAME, 'alternateName' => 'The Bible',
             'potentialAction' => ['@type' => 'SearchAction', 'target' => SITE_URL . '/search/?q={search_term_string}', 'query-input' => 'required name=search_term_string']],
            ['@type' => 'Organization', '@id' => SITE_URL . '/#organization', 'name' => SITE_NAME, 'url' => SITE_URL, 'email' => 'info@holybiblewords.com',
             'logo' => SITE_URL . '/assets/img/icon-512.png'],
        ],
    ];
}

function features_strip(): string {
    $f = [
        ['compare', 'Switch versions instantly', 'Tap KJV or AB at the top. You stay on the same chapter and verse.'],
        ['columns', 'Side-by-side view', 'Read both versions in parallel, verse by verse.'],
        ['highlight', 'Highlights & notes', 'Mark verses in four colors, bookmark, and add notes.'],
        ['play', 'Listen', 'Have any chapter read aloud.'],
        ['calendar', 'Bible in a year', 'A daily reading plan that tracks your progress.'],
        ['download', 'Works offline', 'Install the app and read without a connection.'],
    ];
    $h = '<section class="features"><h2>Made for reading</h2><ul>';
    foreach ($f as [$i, $t, $d]) $h .= '<li>' . icon($i) . '<strong>' . e($t) . '</strong><span>' . e($d) . '</span></li>';
    return $h . '</ul></section>';
}

function blog_posts(): array {
    static $posts;
    if ($posts === null) {
        $posts = [];
        foreach (json_decode(file_get_contents(__DIR__ . '/content/posts.json'), true) as $p) $posts[$p['slug']] = $p;
    }
    return $posts;
}

function blog_teasers(): string {
    $h = '<section class="articles"><h2>Articles you might like</h2><div class="article-cards">';
    foreach (blog_posts() as $p) {
        $h .= '<a class="article-card" href="/blog/' . e($p['slug']) . '/"><img src="' . e($p['image']) . '" alt="" loading="lazy" width="400" height="225">'
            . '<strong>' . e($p['title']) . '</strong><span>' . e($p['excerpt']) . '</span></a>';
    }
    return $h . '</div></section>';
}

function recommended_bibles(): string {
    if (in_native_app()) return '';
    $items = [
        ['https://amzn.to/4dFhe1d', '/wp-content/uploads/2025/02/ESV-Mens-Study-Bible.jpg', "ESV Men's Study Bible", 413],
        ['https://amzn.to/4yY7WG7', '/wp-content/uploads/2025/02/NIV-The-Womans-Study-Bible.jpg', "NIV The Woman's Study Bible", 348],
        ['https://amzn.to/4h5YpoZ', '/wp-content/uploads/2025/02/ESV-Holy-Bible-for-Kids.jpg', 'ESV Holy Bible for Kids', 427],
    ];
    $h = '<section class="shop"><h2>Recommended Bibles</h2><p class="muted">As an Amazon Associate we earn from qualifying purchases.</p><div class="shop-items">';
    foreach ($items as [$href, $img, $name, $w]) {
        $h .= '<a href="' . $href . '" rel="sponsored noopener" target="_blank"><img src="' . $img . '" alt="' . e($name) . '" width="' . $w . '" height="522" loading="lazy"><span>' . e($name) . '</span></a>';
    }
    return $h . '</div></section>';
}

function fill_names(string $ver): string {
    $names = array_map(fn($k) => versions()[$k]['label'], versions()[$ver]['fallback'] ?? []);
    return implode(', then ', $names);
}

function page_version(string $ver): array {
    $v = versions()[$ver];
    $n = array_sum(array_map(fn($b) => $b['available'][$ver], books()));
    $notice = $n < 31102 ? '<p class="notice">' . number_format($n) . ' of 31,102 verses are available in ' . e($v['label'])
        . ' so far. Books not yet available are dimmed; their verses are shown from ' . e(fill_names($ver)) . ', clearly marked.</p>' : '';
    $body = '<div class="wrap">' . breadcrumbs([['Home', '/'], [$v['label'], null]])
        . '<header class="page-head"><h1>' . e($v['fullTitle'] ?? $v['label']) . '</h1><p class="muted">' . e($v['desc']) . '</p></header>'
        . jump_box($ver) . $notice
        . '<section class="books-section"><h2>Old Testament</h2>' . books_grid($ver, 'ot') . '</section>'
        . '<section class="books-section"><h2>New Testament</h2>' . books_grid($ver, 'nt') . '</section>'
        . '<section class="copyright-page"><h2>Copyright</h2>' . credits([$ver]) . '</section></div>';
    return [
        'title' => ($ver === 'ta' ? 'KJV' : $v['name']) . ' | ' . SITE_NAME,
        'description' => 'Read the ' . $v['label'] . ' Bible online. Choose a book of the Old or New Testament.',
        'canonical' => "/$ver/", 'body' => $body, 'ver' => $ver, 'type' => 'version',
        'switch' => version_alternates(fn($k) => "/$k/"), 'alternates' => version_alternates(fn($k) => "/$k/"),
        'jsonld' => [breadcrumb_ld([['Home', '/'], [$v['label'], "/$ver/"]])],
    ];
}

function page_book(string $ver, string $slug): array {
    $book = books()[$slug];
    $name = book_name($book, $ver);
    $grid = '<ul class="num-grid">';
    foreach ($book['verses'] as $i => $n) {
        $c = $i + 1;
        $na = chapter_available($ver, $slug, $c) === 0 ? ' class="na"' : '';
        $grid .= '<li><a href="' . url_for($ver, $slug, $c) . '"' . $na . '>' . $c . '</a></li>';
    }
    $grid .= '</ul>';
    $first = verse_display($ver, $slug, 1, 1);
    $intro = $first ? '<blockquote class="book-open">' . verse_html($first['text'], $first['src']) . ' <cite>' . e(book_name($book, $first['src'])) . ' 1:' . range_label($first) . ' · ' . e(versions()[$first['src']]['short']) . '</cite></blockquote>' : '';
    $notice = $book['available'][$ver] === 0 ? '<p class="notice">' . e($name) . ' is not yet available in ' . e(versions()[$ver]['label']) . '. Chapters open with the ' . e(fill_names($ver)) . ' text.</p>' : '';
    $crumbs = [['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, null]];
    $body = '<div class="wrap">' . breadcrumbs($crumbs)
        . '<header class="page-head"><h1>' . e($name) . '</h1><p class="muted">' . count($book['verses']) . ' chapter' . (count($book['verses']) > 1 ? 's' : '') . ' · ' . e(versions()[$ver]['label']) . '</p></header>'
        . $notice . $intro . '<h2 class="grid-title">Chapters</h2>' . $grid . '</div>';
    return [
        'title' => "$name | " . SITE_NAME,
        'description' => "Read the book of $name (" . versions()[$ver]['short'] . ') online, chapter by chapter.',
        'canonical' => url_for($ver, $slug), 'body' => $body, 'ver' => $ver, 'type' => 'book',
        'noindex' => $book['available'][$ver] === 0,
        'switch' => version_alternates(fn($k) => url_for($k, $slug)),
        'alternates' => version_alternates(fn($k) => url_for($k, $slug)),
        'data' => ['ver' => $ver, 'book' => $slug],
        'jsonld' => [breadcrumb_ld([['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)]])],
    ];
}

/** Reader toolbar: prev / picker / next + tools. */
function reader_bar(string $ver, string $slug, int $c, ?int $v = null): string {
    $book = books()[$slug];
    [$prev, $next] = chapter_neighbors($slug, $c);
    $p = $prev ? '<a class="icon-btn" rel="prev" href="' . url_for($ver, $prev[0], $prev[1]) . '" aria-label="Previous chapter">' . icon('left') . '</a>' : '<span class="icon-btn" aria-hidden="true"></span>';
    $n = $next ? '<a class="icon-btn" rel="next" href="' . url_for($ver, $next[0], $next[1]) . '" aria-label="Next chapter">' . icon('right') . '</a>' : '<span class="icon-btn" aria-hidden="true"></span>';
    return '<div class="reader-bar">' . $p
        . '<button type="button" class="picker-btn" data-action="picker" data-book="' . $slug . '" data-ch="' . $c . '">'
        . '<span>' . e(book_name($book, $ver)) . ' ' . $c . ($v ? ":$v" : '') . '</span>' . icon('down') . '</button>'
        . $n
        . '<span class="reader-tools">'
        . '<button type="button" class="icon-btn" data-action="parallel" aria-pressed="false" aria-label="Side by side with another version" title="Side by side">' . icon('columns') . '</button>'
        . '<button type="button" class="icon-btn" data-action="listen" aria-label="Listen to this chapter" title="Listen">' . icon('play') . '</button>'
        . '</span></div>';
}

function chapter_neighbors(string $slug, int $c): array {
    $list = array_keys(books());
    $i = array_search($slug, $list, true);
    $count = count(books()[$slug]['verses']);
    $prev = $c > 1 ? [$slug, $c - 1] : ($i > 0 ? [$list[$i - 1], count(books()[$list[$i - 1]]['verses'])] : null);
    $next = $c < $count ? [$slug, $c + 1] : ($i < count($list) - 1 ? [$list[$i + 1], 1] : null);
    return [$prev, $next];
}

/**
 * The chapter's verses. A row covering a range ("14–16") carries empty anchors
 * for the joined verses so #v15 links still land on it. Rows filled from another
 * version get class "fb" and a badge naming that version.
 */
function render_verses(string $ver, string $slug, int $c, ?int $mark = null): string {
    $h = '';
    foreach (resolve_chapter($ver, $slug, $c) as $row) {
        $n = $row['n'];
        $cls = 'v' . ($mark !== null && $mark >= $n && $mark <= $row['to'] ? ' marked' : '');
        $extra = '';
        if ($row['src'] !== $ver) {
            $cls .= ' fb';
            $extra = ' <span class="fb-tag" data-src="' . $row['src'] . '" title="Not yet available in ' . e(versions()[$ver]['label']) . '; from ' . e(versions()[$row['src']]['label']) . '">' . e(versions()[$row['src']]['short']) . '</span>';
        }
        $anchors = '';
        for ($j = $n + 1; $j <= $row['to']; $j++) $anchors .= '<span class="v-anchor" id="v' . $j . '"></span>';
        $h .= '<span class="' . $cls . '" id="v' . $n . '" data-v="' . $n . '"' . ($row['to'] > $n ? ' data-to="' . $row['to'] . '"' : '') . '>' . $anchors
            . '<a class="vn" href="' . url_for($ver, $slug, $c, $n) . '">' . range_label($row) . '</a> '
            . verse_html($row['text'], $row['src']) . $extra . '</span> ';
    }
    return $h;
}

function page_chapter(string $ver, string $slug, int $c): array {
    $book = books()[$slug];
    $name = book_name($book, $ver);
    $rows = resolve_chapter($ver, $slug, $c);
    $srcs = array_values(array_unique(array_column($rows, 'src')));
    $filled = array_sum(array_map(fn($r) => $r['src'] !== $ver ? $r['to'] - $r['n'] + 1 : 0, $rows));
    $total = $book['verses'][$c - 1];
    $notice = '';
    if ($filled > 0) {
        $from = implode(' and ', array_map(fn($k) => versions()[$k]['label'], array_diff($srcs, [$ver])));
        $notice = '<p class="notice">' . ($filled >= $total ? 'This chapter is' : $filled . ' verse' . ($filled > 1 ? 's' : '') . ' in this chapter ' . ($filled > 1 ? 'are' : 'is'))
            . ' not yet available in ' . e(versions()[$ver]['label']) . ' and ' . ($filled >= $total || $filled === 1 ? 'is' : 'are') . ' shown from ' . e($from) . ', marked with a badge.</p>';
    }
    [$prev, $next] = chapter_neighbors($slug, $c);
    $foot = '<nav class="chapter-foot" aria-label="Chapter">'
        . ($prev ? '<a class="btn ghost" href="' . url_for($ver, $prev[0], $prev[1]) . '">' . icon('left') . ' ' . e(ref_label(books()[$prev[0]], $ver, $prev[1])) . '</a>' : '<span></span>')
        . ($next ? '<a class="btn" href="' . url_for($ver, $next[0], $next[1]) . '">' . e(ref_label(books()[$next[0]], $ver, $next[1])) . ' ' . icon('right') . '</a>' : '<span></span>')
        . '</nav>';
    $crumbs = [['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["Chapter $c", null]];
    $body = reader_bar($ver, $slug, $c)
        . '<div class="wrap reader-wrap">' . breadcrumbs($crumbs)
        . '<article class="chapter" lang="' . e(versions()[$ver]['lang']) . '" data-ver="' . $ver . '" data-book="' . $slug . '" data-ch="' . $c . '">'
        . '<h1><span class="book-title">' . e($name) . '</span> <span class="ch-num">' . $c . '</span></h1>'
        . $notice
        . '<div class="verses">' . render_verses($ver, $slug, $c) . '</div>'
        . '</article>' . $foot . credits($srcs) . '</div>';
    return [
        'title' => "$name $c | " . SITE_NAME,
        'description' => "Read $name chapter $c (" . versions()[$ver]['short'] . '): ' . mb_strimwidth(verse_plain($rows[0]['text'], $rows[0]['src']), 0, 120, '…'),
        'canonical' => url_for($ver, $slug, $c), 'body' => $body, 'ver' => $ver, 'type' => 'chapter',
        'noindex' => chapter_available($ver, $slug, $c) === 0,
        'switch' => version_alternates(fn($k) => url_for($k, $slug, $c)),
        'alternates' => version_alternates(fn($k) => url_for($k, $slug, $c)),
        'data' => ['ver' => $ver, 'book' => $slug, 'ch' => $c],
        'jsonld' => [breadcrumb_ld([['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["$name $c", url_for($ver, $slug, $c)]])],
    ];
}

function page_verse(string $ver, string $slug, int $c, int $v): array {
    $book = books()[$slug];
    $name = book_name($book, $ver);
    $row = verse_display($ver, $slug, $c, $v);
    $src = $row['src'];
    $missing = $src !== $ver;
    $label = book_name($book, $src) . " $c:" . range_label($row);
    $count = $book['verses'][$c - 1];

    $compare = '';
    foreach (versions() as $k => $vv) {
        if ($k === $ver) continue;
        $t = verse_text($k, $slug, $c, $v);
        if ($t === null) continue;
        $orow = verse_display($k, $slug, $c, $v);
        $compare .= '<div class="compare-item" lang="' . e($vv['lang']) . '"><h2><a href="' . url_for($k, $slug, $c, $orow['n']) . '">' . e(book_name($book, $k) . " $c:" . range_label($orow)) . ' · ' . e($vv['short']) . '</a></h2><p>' . verse_html($orow['text'], $k) . '</p></div>';
    }
    $prevV = $row['n'] - 1;
    $nextV = $row['to'] + 1;
    $nav = '<nav class="verse-nav" aria-label="Verse">'
        . ($prevV >= 1 ? '<a class="btn ghost" rel="prev" href="' . url_for($ver, $slug, $c, $prevV) . '">' . icon('left') . " $name $c:$prevV" . '</a>' : '<span></span>')
        . ($nextV <= $count ? '<a class="btn ghost" rel="next" href="' . url_for($ver, $slug, $c, $nextV) . '">' . "$name $c:$nextV" . ' ' . icon('right') . '</a>' : '<span></span>')
        . '</nav>';
    $grid = '<ul class="num-grid small">';
    for ($i = 1; $i <= $count; $i++) {
        $grid .= '<li><a href="' . url_for($ver, $slug, $c, $i) . '"' . ($i >= $row['n'] && $i <= $row['to'] ? ' aria-current="page"' : '') . '>' . $i . '</a></li>';
    }
    $grid .= '</ul>';
    $crumbs = [['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["Chapter $c", url_for($ver, $slug, $c)], ["Verse $v", null]];
    $body = reader_bar($ver, $slug, $c, $v)
        . '<div class="wrap reader-wrap">' . breadcrumbs($crumbs)
        . '<article class="verse-page" data-ver="' . $ver . '" data-book="' . $slug . '" data-ch="' . $c . '" data-v="' . $v . '">'
        . '<h1>' . e(ref_label($book, $ver, $c, $v)) . '</h1>'
        . ($missing ? '<p class="notice">This verse is not yet available in ' . e(versions()[$ver]['label']) . '. Showing ' . e(versions()[$src]['label']) . '.</p>' : '')
        . '<blockquote class="verse-card" lang="' . e(versions()[$src]['lang']) . '"><p>' . verse_html($row['text'], $src) . '</p>'
        . '<footer>' . e($label) . ' · ' . e(versions()[$src]['short']) . '</footer></blockquote>'
        . '<div class="verse-actions" data-ref="' . "$slug.$c.{$row['n']}" . '">'
        . '<button class="btn ghost" type="button" data-action="verse-copy">' . icon('copy') . ' Copy</button>'
        . '<button class="btn ghost" type="button" data-action="verse-share">' . icon('share') . ' Share</button>'
        . '<button class="btn ghost" type="button" data-action="verse-image">' . icon('image') . ' Image</button>'
        . '<button class="btn ghost" type="button" data-action="verse-save">' . icon('bookmark') . ' Save</button>'
        . '<button class="btn ghost" type="button" data-action="verse-explain">' . icon('bulb') . ' Explain</button>'
        . '</div><section class="commentary" data-commentary hidden></section>'
        . '<a class="btn" href="' . url_for($ver, $slug, $c) . '#v' . $v . '">' . icon('book') . ' Read ' . e("$name $c") . ' in context</a>'
        . ($compare ? '<section class="compare">' . $compare . '</section>' : '')
        . $nav
        . '<h2 class="grid-title">More verses in ' . e("$name $c") . '</h2>' . $grid
        . credits([$src])
        . '</article></div>';
    $plain = verse_plain($row['text'], $src);
    return [
        'title' => ref_label($book, $ver, $c, $v) . ' | ' . SITE_NAME,
        'description' => mb_strimwidth($plain, 0, 155, '…'),
        'canonical' => url_for($ver, $slug, $c, $v), 'body' => $body, 'ver' => $ver, 'type' => 'verse',
        'noindex' => $missing,
        'switch' => version_alternates(fn($k) => url_for($k, $slug, $c, $v)),
        'alternates' => array_filter(version_alternates(fn($k) => verse_text($k, $slug, $c, $v) ? url_for($k, $slug, $c, $v) : null)),
        'data' => ['ver' => $ver, 'book' => $slug, 'ch' => $c, 'v' => $v],
        'jsonld' => [
            breadcrumb_ld([['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["$name $c", url_for($ver, $slug, $c)], [ref_label($book, $ver, $c, $v), url_for($ver, $slug, $c, $v)]]),
            ['@type' => 'Quotation', 'text' => $plain, 'isPartOf' => ['@type' => 'Book', 'name' => versions()[$src]['fullTitle'] ?? versions()[$src]['label']], 'citation' => $label],
        ],
    ];
}

function page_search(string $q, string $ver, string $t, int $page): array {
    $per = 30;
    $res = $q !== '' ? search($ver, $q, $t, ($page - 1) * $per, $per) : ['total' => 0, 'results' => [], 'terms' => []];
    $list = '';
    foreach ($res['results'] as [$bi, $c, $v, $text]) {
        $b = book_by_index($bi);
        $list .= '<li><a href="' . url_for($ver, $b['slug'], $c, $v) . '"><strong>' . e(ref_label($b, $ver, $c, $v)) . '</strong>'
            . '<span>' . highlight_terms(verse_html($text, $ver), $res['terms']) . '</span></a></li>';
    }
    $filters = '';
    foreach (['' => 'All', 'ot' => 'Old Testament', 'nt' => 'New Testament'] as $k => $lbl) {
        $filters .= '<a class="chip' . ($k === $t ? ' on' : '') . '" href="/search/?' . e(http_build_query(['q' => $q, 'v' => $ver, 't' => $k])) . '">' . $lbl . '</a>';
    }
    $pages = '';
    $last = (int)ceil($res['total'] / $per);
    if ($last > 1) {
        $pages = '<nav class="pager">';
        if ($page > 1) $pages .= '<a class="btn ghost" href="/search/?' . e(http_build_query(['q' => $q, 'v' => $ver, 't' => $t, 'page' => $page - 1])) . '">' . icon('left') . ' Previous</a>';
        $pages .= '<span>Page ' . $page . ' of ' . $last . '</span>';
        if ($page < $last) $pages .= '<a class="btn ghost" href="/search/?' . e(http_build_query(['q' => $q, 'v' => $ver, 't' => $t, 'page' => $page + 1])) . '">Next ' . icon('right') . '</a>';
        $pages .= '</nav>';
    }
    $summary = $q === '' ? '<p class="muted">Search by word or phrase (use "quotes" for an exact phrase), or type a reference like <em>Psalm 23</em> or <em>Juan 3:16</em>.</p>'
        : '<p class="muted">' . number_format($res['total']) . ' result' . ($res['total'] === 1 ? '' : 's') . ' for <strong>' . e($q) . '</strong> in ' . e(versions()[$ver]['label']) . '</p>';
    $body = '<div class="wrap"><header class="page-head"><h1>Search the Bible</h1></header>'
        . jump_box($ver, $q, $q === '') . ($q !== '' ? '<div class="chips">' . $filters . '</div>' : '') . $summary
        . '<ol class="results">' . $list . '</ol>' . $pages . '</div>';
    return [
        'title' => ($q !== '' ? "“{$q}” — " : '') . 'Search | ' . SITE_NAME,
        'canonical' => '/search/', 'body' => $body, 'ver' => $ver, 'type' => 'search', 'noindex' => $q !== '',
        'switch' => version_alternates(fn($k) => '/search/?' . http_build_query(array_filter(['q' => $q, 'v' => $k, 't' => $t]))),
        'data' => ['ver' => $ver],
    ];
}

function page_votd(string $ver): array {
    $today = site_today();
    $past = '';
    $d = new DateTimeImmutable($today);
    for ($i = 1; $i <= 6; $i++) {
        $day = $d->modify("-$i day")->format('Y-m-d');
        [$s, $c, $v] = votd_for($day);
        $b = books()[$s];
        $row = verse_display($ver, $s, $c, $v);
        $past .= '<li><a href="' . url_for($ver, $s, $c, $v) . '"><time datetime="' . $day . '">' . (new DateTimeImmutable($day))->format('D, M j') . '</time>'
            . '<strong>' . e(book_name($b, $row['src']) . " $c:" . range_label($row)) . ($row['src'] !== $ver ? ' · ' . e(versions()[$row['src']]['short']) : '') . '</strong><span>' . verse_html($row['text'], $row['src']) . '</span></a></li>';
    }
    $body = '<div class="wrap narrow">' . votd_card($ver, $today, true)
        . '<p class="muted">A new verse is chosen automatically every day at midnight in your time zone. Install the app to keep it one tap away.</p>'
        . '<section><h2>Previous days</h2><ol class="results past-votd">' . $past . '</ol></section>' . credits(version_chain($ver)) . '</div>';
    return [
        'title' => 'Verse of the Day | ' . SITE_NAME,
        'description' => 'Today’s Bible verse of the day from the King James Version and Ang Pulong sa Dios. A new verse every day.',
        'canonical' => '/verse-of-the-day/', 'body' => $body, 'ver' => $ver, 'type' => 'votd',
        'switch' => version_alternates(fn($k) => '/verse-of-the-day/?v=' . $k), 'data' => ['ver' => $ver],
    ];
}

function page_plan(): array {
    $body = '<div class="wrap narrow"><header class="page-head"><h1>Bible in a Year</h1>'
        . '<p class="muted">Read the whole Bible in 365 days, about 3–4 chapters a day. Your progress is saved on this device.</p></header>'
        . '<div id="plan-app" class="plan"><noscript><p class="notice">The reading plan needs JavaScript.</p></noscript></div></div>';
    return ['title' => 'Bible in a Year Reading Plan | ' . SITE_NAME, 'description' => 'A free daily Bible reading plan: read the whole Bible in a year and track your progress.',
        'canonical' => '/plan/', 'body' => $body, 'type' => 'plan'];
}

function page_saved(): array {
    $body = '<div class="wrap narrow"><header class="page-head"><h1>Saved</h1><p class="muted">Bookmarks, highlights, notes and reading history are stored on this device.</p></header>'
        . '<div class="tabs" role="tablist"><button role="tab" data-tab="bookmarks" aria-selected="true">Bookmarks</button><button role="tab" data-tab="highlights">Highlights</button><button role="tab" data-tab="notes">Notes</button><button role="tab" data-tab="history">History</button></div>'
        . '<div id="saved-app"><noscript><p class="notice">Saved items need JavaScript.</p></noscript></div></div>';
    return ['title' => 'Saved Verses | ' . SITE_NAME, 'canonical' => '/saved/', 'body' => $body, 'type' => 'saved', 'noindex' => true];
}

function page_app(): array {
    $body = '<div class="wrap narrow"><header class="page-head"><h1>Get the Holy Bible Words app</h1>'
        . '<p class="lead">The same Bible, verse of the day, highlights and reading plan — on your home screen, and readable offline.</p></header>'
        . '<div class="install-box" data-install>'
        . '<button class="btn" type="button" data-action="install" hidden>' . icon('download') . ' Install the app</button>'
        . '<div class="install-help">'
        . '<h2>Android</h2><p>Open holybiblewords.com in Chrome, tap the ⋮ menu and choose <strong>Install app</strong> (or <strong>Add to Home screen</strong>).</p>'
        . '<h2>iPhone and iPad</h2><p>Open holybiblewords.com in Safari, tap the Share button and choose <strong>Add to Home Screen</strong>.</p>'
        . '<h2>Desktop</h2><p>In Chrome or Edge, click the install icon at the right of the address bar.</p>'
        . '</div></div>'
        . '<section class="offline-box"><h2>Read offline</h2><p>Download a whole version to this device so you can read without a connection.</p>'
        . '<ol class="steps"><li><strong>On iPhone and iPad, open the app from your Home Screen first</strong> and download from inside it. '
        . 'Safari and the Home Screen app keep separate storage, so a download made in Safari isn’t available in the app.</li>'
        . '<li>Tap a version below and wait until it says <strong>Downloaded</strong> (a few seconds on Wi-Fi).</li>'
        . '<li>That’s it. With no connection, open the app as usual: it shows your downloaded versions and you can read any book and chapter.</li></ol>'
        . '<div class="offline-actions">'
        . implode('', array_map(fn($k) => '<button class="btn ghost" type="button" data-action="offline" data-ver="' . $k . '">' . icon('download') . ' ' . e(versions()[$k]['label']) . '</button>', array_keys(versions())))
        . '</div><p class="muted" data-offline-status></p></section></div>';
    return ['title' => 'Get the App | ' . SITE_NAME, 'description' => 'Install Holy Bible Words on Android, iPhone or desktop and read the Bible offline.',
        'canonical' => '/app/', 'body' => $body, 'type' => 'app'];
}

function page_blog_index(): array {
    $body = '<div class="wrap">' . breadcrumbs([['Home', '/'], ['Blog', null]]) . '<header class="page-head"><h1>Blog</h1></header>' . blog_teasers() . '</div>';
    return ['title' => 'Blog | ' . SITE_NAME, 'canonical' => '/blog/', 'body' => $body, 'type' => 'blog',
        'description' => 'Articles on faith, the Bible and Christian living from Holy Bible Words.'];
}

function page_blog_post(array $p): array {
    $date = (new DateTimeImmutable($p['date']))->format('F j, Y');
    $body = '<div class="wrap narrow">' . breadcrumbs([['Home', '/'], ['Blog', '/blog/'], [$p['title'], null]])
        . '<article class="post"><h1>' . e($p['title']) . '</h1><p class="muted"><time datetime="' . e(substr($p['date'], 0, 10)) . '">' . $date . '</time></p>'
        . '<img class="post-hero" src="' . e($p['image']) . '" alt="" width="1200" height="675">'
        . '<div class="prose">' . $p['html'] . '</div></article>' . blog_teasers() . '</div>';
    return ['title' => $p['title'] . ' | ' . SITE_NAME, 'description' => $p['excerpt'], 'canonical' => '/blog/' . $p['slug'] . '/',
        'body' => $body, 'type' => 'post', 'article' => true, 'og_image' => $p['image'],
        'jsonld' => [['@type' => 'BlogPosting', 'headline' => $p['title'], 'datePublished' => $p['date'], 'dateModified' => $p['modified'],
            'image' => SITE_URL . $p['image'], 'mainEntityOfPage' => SITE_URL . '/blog/' . $p['slug'] . '/', 'publisher' => ['@id' => SITE_URL . '/#organization']]]];
}

function page_static(string $slug): array {
    $p = json_decode(file_get_contents(__DIR__ . "/content/$slug.json"), true);
    $body = '<div class="wrap narrow"><article class="post"><h1>' . e($p['title']) . '</h1><div class="prose">' . $p['html'] . '</div></article></div>';
    return ['title' => $p['title'] . ' | ' . SITE_NAME, 'canonical' => "/$slug/", 'body' => $body, 'type' => 'page'];
}

function page_offline(): array {
    $body = '<div class="wrap narrow offline-shell" data-offline-shell><h1>You’re offline</h1>'
        . '<p class="muted">This page isn’t saved on your device yet. Chapters you have opened before, and versions you downloaded on the <a href="/app/">app page</a>, still work.</p></div>';
    return ['title' => 'Offline | ' . SITE_NAME, 'canonical' => '/offline/', 'body' => $body, 'type' => 'offline', 'noindex' => true];
}

function page_404(): array {
    $body = '<div class="wrap narrow"><header class="page-head"><h1>Page not found</h1>'
        . '<p class="muted">That page doesn’t exist. Try searching, or pick a book below.</p></header>' . jump_box('ta')
        . '<section class="books-section"><h2>Old Testament</h2>' . books_grid('ta', 'ot') . '</section>'
        . '<section class="books-section"><h2>New Testament</h2>' . books_grid('ta', 'nt') . '</section></div>';
    return ['title' => 'Page Not Found | ' . SITE_NAME, 'canonical' => '/404', 'body' => $body, 'type' => '404', 'noindex' => true];
}
