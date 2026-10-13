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
        $partial = $b['available'][$ver] === 0 ? ' class="na" title="Not yet available in this version"' : '';
        $h .= '<li><a href="' . url_for($ver, $slug) . '"' . $partial . ' data-book="' . $slug . '">'
            . e(book_name($b, $ver)) . '<small>' . count($b['verses']) . '</small></a></li>';
    }
    return $h . '</ul>';
}

function votd_card(string $ver, string $ymd, bool $h1 = false): string {
    [$slug, $c, $v] = votd_for($ymd);
    $book = books()[$slug];
    $text = verse_text($ver, $slug, $c, $v);
    $shownVer = $ver;
    if ($text === null) { $shownVer = 'ta'; $text = verse_text('ta', $slug, $c, $v); }
    $date = DateTimeImmutable::createFromFormat('!Y-m-d', $ymd)->format('l, F j, Y');
    $tag = $h1 ? 'h1' : 'h2';
    $note = $shownVer !== $ver ? '<p class="note">Not yet available in ' . e(versions()[$ver]['label']) . ' — showing KJV.</p>' : '';
    return '<section class="votd" data-votd data-date="' . $ymd . '" data-ver="' . $ver . '" data-ref="' . "$slug.$c.$v" . '">'
        . '<div class="votd-head"><' . $tag . '>' . icon('sun') . ' Verse of the Day</' . $tag . '><time datetime="' . $ymd . '">' . $date . '</time></div>'
        . '<blockquote class="votd-text" lang="' . e(versions()[$shownVer]['lang']) . '">' . verse_html($text) . '</blockquote>'
        . '<p class="votd-ref"><a href="' . url_for($ver, $slug, $c, $v) . '">' . e(ref_label($book, $shownVer, $c, $v)) . ' <span class="badge">' . e(versions()[$shownVer]['short']) . '</span></a></p>'
        . $note
        . '<div class="votd-actions">'
        . '<a class="btn" href="' . url_for($ver, $slug, $c) . '#v' . $v . '">' . icon('book') . ' Read chapter</a>'
        . '<button class="btn ghost" type="button" data-action="share-votd">' . icon('share') . ' Share</button>'
        . '<button class="btn ghost" type="button" data-action="image-votd">' . icon('image') . ' Image</button>'
        . '</div></section>';
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
            . '<span>' . ($k === 'ta' ? 'English · complete Old and New Testament' : 'Cebuano · ' . ($pct < 100 ? "$pct% available, more coming" : 'complete')) . '</span>'
            . icon('right') . '</a>';
    }
    $body = '<section class="hero"><div class="wrap">'
        . '<h1>Read the Holy Bible Online</h1>'
        . '<p class="lead">The King James Version and Ang Biblia, 2011 in one place. Jump to any chapter or verse, switch versions without losing your place, and get a new verse every day.</p>'
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
        'description' => 'Explore the Holy Bible online with Holy Bible Words – the complete King James Version and Ang Biblia, 2011, easy chapter and verse navigation, and an inspiring verse of the day.',
        'canonical' => '/', 'body' => $body, 'type' => 'home', 'ver' => $ver,
        'switch' => ['ta' => '/ta/', 'ml' => '/ml/'],
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

function page_version(string $ver): array {
    $v = versions()[$ver];
    $n = array_sum(array_map(fn($b) => $b['available'][$ver], books()));
    $notice = $n < 31102 ? '<p class="notice">' . number_format($n) . ' of 31,102 verses are available in ' . e($v['label'])
        . ' so far. Books not yet available are dimmed; their chapters open in KJV.</p>' : '';
    $body = '<div class="wrap">' . breadcrumbs([['Home', '/'], [$v['label'], null]])
        . '<header class="page-head"><h1>' . e($v['label']) . '</h1><p class="muted">' . e($v['copyright']) . '</p></header>'
        . jump_box($ver) . $notice
        . '<section class="books-section"><h2>Old Testament</h2>' . books_grid($ver, 'ot') . '</section>'
        . '<section class="books-section"><h2>New Testament</h2>' . books_grid($ver, 'nt') . '</section></div>';
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
    $first = verse_text($ver, $slug, 1, 1);
    $intro = $first ? '<blockquote class="book-open">' . verse_html($first) . ' <cite>' . e($name) . ' 1:1</cite></blockquote>' : '';
    $notice = $book['available'][$ver] === 0 ? '<p class="notice">' . e($name) . ' is not yet available in ' . e(versions()[$ver]['label']) . '. Chapters open with the KJV text.</p>' : '';
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
        . '<button type="button" class="icon-btn" data-action="parallel" aria-pressed="false" aria-label="Side-by-side with the other version" title="Side by side">' . icon('columns') . '</button>'
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

function render_verses(string $ver, string $slug, int $c, ?int $mark = null): string {
    $verses = chapter_text($ver, $slug, $c);
    $kjv = $ver === 'ta' ? $verses : chapter_text('ta', $slug, $c);
    $h = '';
    foreach ($kjv as $i => $fallback) {
        $n = $i + 1;
        $t = $verses[$i] ?? null;
        $cls = 'v' . ($mark === $n ? ' marked' : '');
        $extra = '';
        if ($t === null) { $t = $fallback; $cls .= ' fb'; $extra = ' <span class="fb-tag" title="Not yet available in ' . e(versions()[$ver]['label']) . '">KJV</span>'; }
        $h .= '<span class="' . $cls . '" id="v' . $n . '" data-v="' . $n . '"><a class="vn" href="' . url_for($ver, $slug, $c, $n) . '">' . $n . '</a> '
            . verse_html($t) . $extra . '</span> ';
    }
    return $h;
}

function page_chapter(string $ver, string $slug, int $c): array {
    $book = books()[$slug];
    $name = book_name($book, $ver);
    $avail = chapter_available($ver, $slug, $c);
    $total = $book['verses'][$c - 1];
    $notice = '';
    if ($avail < $total) {
        $notice = '<p class="notice">' . ($avail === 0 ? 'This chapter is' : ($total - $avail) . ' verse' . ($total - $avail > 1 ? 's' : '') . ' in this chapter are')
            . ' not yet available in ' . e(versions()[$ver]['label']) . ' and ' . ($avail === 0 ? 'is' : 'are') . ' shown from the KJV.</p>';
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
        . '</article>' . $foot . '<p class="ver-credit">' . e(versions()[$ver]['label']) . ' — ' . e(versions()[$ver]['copyright']) . '</p></div>';
    $first = verse_text($ver, $slug, $c, 1) ?? verse_text('ta', $slug, $c, 1);
    return [
        'title' => "$name $c | " . SITE_NAME,
        'description' => "Read $name chapter $c (" . versions()[$ver]['short'] . '): ' . mb_strimwidth(verse_plain($first), 0, 120, '…'),
        'canonical' => url_for($ver, $slug, $c), 'body' => $body, 'ver' => $ver, 'type' => 'chapter',
        'noindex' => $avail === 0,
        'switch' => version_alternates(fn($k) => url_for($k, $slug, $c)),
        'alternates' => version_alternates(fn($k) => url_for($k, $slug, $c)),
        'data' => ['ver' => $ver, 'book' => $slug, 'ch' => $c],
        'jsonld' => [breadcrumb_ld([['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["$name $c", url_for($ver, $slug, $c)]])],
    ];
}

function page_verse(string $ver, string $slug, int $c, int $v): array {
    $book = books()[$slug];
    $name = book_name($book, $ver);
    $text = verse_text($ver, $slug, $c, $v);
    $missing = $text === null;
    $shown = $missing ? verse_text('ta', $slug, $c, $v) : $text;
    $label = ref_label($book, $ver, $c, $v);
    $count = $book['verses'][$c - 1];

    $compare = '';
    foreach (versions() as $k => $vv) {
        if ($k === $ver) continue;
        $ot = verse_text($k, $slug, $c, $v);
        if ($ot === null) continue;
        $compare .= '<div class="compare-item" lang="' . e($vv['lang']) . '"><h2><a href="' . url_for($k, $slug, $c, $v) . '">' . e(ref_label($book, $k, $c, $v)) . ' · ' . e($vv['short']) . '</a></h2><p>' . verse_html($ot) . '</p></div>';
    }
    $nav = '<nav class="verse-nav" aria-label="Verse">'
        . ($v > 1 ? '<a class="btn ghost" rel="prev" href="' . url_for($ver, $slug, $c, $v - 1) . '">' . icon('left') . " $name $c:" . ($v - 1) . '</a>' : '<span></span>')
        . ($v < $count ? '<a class="btn ghost" rel="next" href="' . url_for($ver, $slug, $c, $v + 1) . '">' . "$name $c:" . ($v + 1) . ' ' . icon('right') . '</a>' : '<span></span>')
        . '</nav>';
    $grid = '<ul class="num-grid small">';
    for ($i = 1; $i <= $count; $i++) {
        $grid .= '<li><a href="' . url_for($ver, $slug, $c, $i) . '"' . ($i === $v ? ' aria-current="page"' : '') . '>' . $i . '</a></li>';
    }
    $grid .= '</ul>';
    $crumbs = [['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["Chapter $c", url_for($ver, $slug, $c)], ["Verse $v", null]];
    $body = reader_bar($ver, $slug, $c, $v)
        . '<div class="wrap reader-wrap">' . breadcrumbs($crumbs)
        . '<article class="verse-page" data-ver="' . $ver . '" data-book="' . $slug . '" data-ch="' . $c . '" data-v="' . $v . '">'
        . '<h1>' . e($label) . '</h1>'
        . ($missing ? '<p class="notice">This verse is not yet available in ' . e(versions()[$ver]['label']) . '. Showing the KJV.</p>' : '')
        . '<blockquote class="verse-card" lang="' . e(versions()[$missing ? 'ta' : $ver]['lang']) . '"><p>' . verse_html($shown) . '</p>'
        . '<footer>' . e($label) . ' · ' . e(versions()[$missing ? 'ta' : $ver]['short']) . '</footer></blockquote>'
        . '<div class="verse-actions" data-ref="' . "$slug.$c.$v" . '">'
        . '<button class="btn ghost" type="button" data-action="verse-copy">' . icon('copy') . ' Copy</button>'
        . '<button class="btn ghost" type="button" data-action="verse-share">' . icon('share') . ' Share</button>'
        . '<button class="btn ghost" type="button" data-action="verse-image">' . icon('image') . ' Image</button>'
        . '<button class="btn ghost" type="button" data-action="verse-save">' . icon('bookmark') . ' Save</button>'
        . '</div>'
        . '<a class="btn" href="' . url_for($ver, $slug, $c) . '#v' . $v . '">' . icon('book') . ' Read ' . e("$name $c") . ' in context</a>'
        . ($compare ? '<section class="compare">' . $compare . '</section>' : '')
        . $nav
        . '<h2 class="grid-title">More verses in ' . e("$name $c") . '</h2>' . $grid
        . '</article></div>';
    $plain = verse_plain($shown);
    return [
        'title' => "$label | " . SITE_NAME,
        'description' => mb_strimwidth($plain, 0, 155, '…'),
        'canonical' => url_for($ver, $slug, $c, $v), 'body' => $body, 'ver' => $ver, 'type' => 'verse',
        'noindex' => $missing,
        'switch' => version_alternates(fn($k) => url_for($k, $slug, $c, $v)),
        'alternates' => array_filter(version_alternates(fn($k) => verse_text($k, $slug, $c, $v) !== null ? url_for($k, $slug, $c, $v) : null)),
        'data' => ['ver' => $ver, 'book' => $slug, 'ch' => $c, 'v' => $v],
        'jsonld' => [
            breadcrumb_ld([['Home', '/'], [versions()[$ver]['label'], "/$ver/"], [$name, url_for($ver, $slug)], ["$name $c", url_for($ver, $slug, $c)], [$label, url_for($ver, $slug, $c, $v)]]),
            ['@type' => 'Quotation', 'text' => $plain, 'isPartOf' => ['@type' => 'Book', 'name' => versions()[$missing ? 'ta' : $ver]['label']], 'citation' => $label],
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
            . '<span>' . highlight_terms(verse_html($text), $res['terms']) . '</span></a></li>';
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
        $t = verse_text($ver, $s, $c, $v) ?? verse_text('ta', $s, $c, $v);
        $past .= '<li><a href="' . url_for($ver, $s, $c, $v) . '"><time datetime="' . $day . '">' . (new DateTimeImmutable($day))->format('D, M j') . '</time>'
            . '<strong>' . e(ref_label($b, $ver, $c, $v)) . '</strong><span>' . verse_html($t) . '</span></a></li>';
    }
    $body = '<div class="wrap narrow">' . votd_card($ver, $today, true)
        . '<p class="muted">A new verse is chosen automatically every day at midnight in your time zone. Install the app to keep it one tap away.</p>'
        . '<section><h2>Previous days</h2><ol class="results past-votd">' . $past . '</ol></section></div>';
    return [
        'title' => 'Verse of the Day | ' . SITE_NAME,
        'description' => 'Today’s Bible verse of the day from the King James Version and Ang Biblia, 2011. A new verse every day.',
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
