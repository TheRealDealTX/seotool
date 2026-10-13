<?php
// Keyword internal links, run by compile.php after the body-link check.
//
// Every page gets anchor phrases: the keywords it ranked for in the Semrush
// organic-positions export (old URLs follow the redirect table) plus its own
// `keyword` field. Body copy on other pages is then scanned for those phrases
// and the best-scoring matches become links: highest search volume first, one
// link per target and per anchor on a page, never a link to the page itself.
// Each target takes a limited number of these links site-wide, so a phrase
// repeated in boilerplate (the ANSI Z133 safety note) doesn't link from every
// page; same-department pages get first claim on them.
//
// Only body copy is touched (product body and Q&A, category buying guides and
// FAQ, guide sections and FAQ, brand "About"). Summaries, intros and headings
// stay plain because they also feed meta tags, JSON-LD and cards.
//
// Writes seo-data/internal-links.csv listing every link it added.
//
// It also builds $popular, the "Popular searches" link blocks: per department,
// the pages that earned the most search traffic, each labeled with its biggest
// keyword (one whose words all appear in the page's own name, which rules out
// misspellings and odd queries). compile.php stores it in the catalog.
//
// Expects from compile.php: $products, $categories, $brands, $guides,
// $redirects, $root, $warn.

const AUTOLINK_MAX = ['products' => 4, 'categories' => 6, 'guides' => 8, 'brands' => 4]; // new links per page
const AUTOLINK_PER_PARA = 2;
const AUTOLINK_INBOUND = ['products' => 30, 'guides' => 30, 'categories' => 60, 'brands' => 60]; // added links per target
// Queries that are about the old store itself, or too generic to be a useful anchor.
const AUTOLINK_SKIP = '/\b(gap arborist|arborist supply|near me|stores?|shop|online|for sale|cheap|best)\b/';
const AUTOLINK_GENERIC = ['rope', 'ropes', 'saddle', 'saddles', 'helmet', 'helmets', 'chainsaw', 'chainsaws', 'gloves', 'boots',
    'pulley', 'pulleys', 'lanyard', 'lanyards', 'sling', 'slings', 'spurs', 'gear', 'harness', 'saw', 'saws', 'file', 'files',
    'chain', 'bar', 'oil', 'fuel', 'blades', 'blade', 'wedge', 'wedges', 'tools', 'hardware', 'climbing', 'rigging', 'arborist',
    // Brand or product names that are also everyday words in the copy.
    'edge', 'edges', 'land', 'notch', 'atlas', 'boss', 'oregon', 'groundie', 'phoenix', 'stein', 'marvin', 'kong', 'corona', 'klein'];

$autolink = (function () use ($products, $categories, $brands, $guides, $redirects, $root) {
    $sets = compact('products', 'categories', 'brands', 'guides');
    $type = [];
    foreach ($sets as $set => $items) foreach ($items as $path => $_) $type[$path] = $set;
    $resolve = function (string $path) use ($type, $redirects): ?string {
        for ($i = 0; $i < 4 && !isset($type[$path]); $i++) {
            if (!isset($redirects[$path])) return null;
            $path = $redirects[$path];
        }
        return isset($type[$path]) ? $path : null;
    };
    $brandNames = [];
    foreach ($brands as $b) $brandNames[strtolower($b['name'])] = $b['name'];
    $norm = fn(string $k) => trim(preg_replace('/\s+/', ' ', strtolower($k)));
    $usable = function (string $k) use ($brandNames): bool {
        if (strlen($k) < 4 || preg_match(AUTOLINK_SKIP, $k)) return false;
        // A phrase cut off mid-thought ("carburetor for") makes a poor anchor.
        if (preg_match('/^(a|an|the|for|of|to|in|on|with|and|or|vs)\b|\b(a|an|the|for|of|to|in|on|with|and|or|vs|by)$/', $k)) return false;
        if (str_contains($k, ' ')) return true;
        return !in_array($k, AUTOLINK_GENERIC, true) && (isset($brandNames[$k]) || preg_match('/\d/', $k) || strlen($k) >= 6);
    };

    // anchor => [target, score]. Semrush rankings first: the URL Google ranked for a
    // keyword is the page that keyword should point at. Best position wins a tie.
    $best = [];
    $traffic = [];
    $f = fopen("$root/seo-data/organic-positions-2026-06.csv", 'r');
    $head = fgetcsv($f, null, ',', '"', '');
    while (($r = fgetcsv($f, null, ',', '"', '')) !== false) {
        $r = array_combine($head, $r);
        $k = $norm($r['Keyword']);
        $to = $resolve((string)parse_url($r['URL'], PHP_URL_PATH));
        if (!$to || !$usable($k)) continue;
        $vol = (int)$r['Search Volume'];
        $pos = (int)$r['Position'];
        if (!isset($best[$k]) || $pos < $best[$k][2]) $best[$k] = [$to, $vol, $pos];
        $traffic[$to] = ($traffic[$to] ?? 0) + (int)$r['Traffic'];
    }
    fclose($f);
    $anchors = [];
    // A phrase is "specific" when it names a brand or a model number. A generic phrase
    // ("replacement pads") may only point at a product from inside that product's category.
    $specific = function (string $k) use ($brandNames): bool {
        foreach (explode(' ', $k) as $w) if (isset($brandNames[$w]) || preg_match('/\d/', $w)) return true;
        return false;
    };
    foreach ($best as $k => [$to, $vol]) $anchors[$k] = [$to, max($vol, 10), $specific($k)];

    // Each page's own keyword. When several pages share one, a category beats a
    // product, and a product shared by variants is left out as ambiguous.
    $own = [];
    foreach ($sets as $set => $items) foreach ($items as $path => $x) {
        $k = $norm($x['keyword'] ?? '');
        if ($k !== '' && $usable($k)) $own[$k][$set === 'categories' ? 0 : 1][] = $path;
    }
    foreach ($own as $k => $by) {
        if (isset($anchors[$k])) continue;
        $pick = isset($by[0]) ? (count($by[0]) === 1 ? $by[0][0] : null) : (count($by[1]) === 1 ? $by[1][0] : null);
        if ($pick) $anchors[$k] = [$pick, 20, $specific($k)];
    }
    // Short product names ("Silky Sugoi", "Petzl GriGri"), the way the copy refers
    // to them: two to four leading words of the name that carry a brand or model
    // number plus a model word. A
    // name shared by several products goes to the one with the most search volume.
    $volOf = [];
    foreach ($best as [$to, $vol]) $volOf[$to] = max($volOf[$to] ?? 0, $vol);
    $short = [];
    foreach ($products as $path => $x) {
        $words = preg_split('/\s+/', $norm(preg_replace('/[^\w\s\-\'.]/u', ' ', $x['name'])));
        $brand = $norm($x['brand_name'] ?? '');
        for ($n = 2; $n <= min(4, count($words) - 1); $n++) {
            $k = implode(' ', array_slice($words, 0, $n));
            $model = array_filter(array_slice($words, 0, $n), fn($w) => strlen($w) >= 3 && $w !== $brand
                && !in_array(rtrim($w, 's'), AUTOLINK_GENERIC, true) && !isset($brandNames[$w]));
            if (!$model || !$specific($k) || !$usable($k) || isset($anchors[$k])) continue;
            $short[$k][] = [$path, $volOf[$path] ?? 0];
        }
    }
    foreach ($short as $k => $list) {
        usort($list, fn($a, $b) => $b[1] <=> $a[1]);
        if (count($list) > 1 && $list[0][1] === $list[1][1]) continue; // a tie is ambiguous
        $anchors[$k] = [$list[0][0], max(20, $list[0][1]), true];
    }
    // Brand names link to their brand page.
    foreach ($brands as $path => $b) {
        $k = $norm($b['name']);
        if (!isset($anchors[$k]) && $usable($k) && !in_array($k, AUTOLINK_GENERIC, true)) $anchors[$k] = [$path, 15, true];
    }

    // Longest phrase first, so "husqvarna 450 rancher" is tried before "husqvarna 450".
    uksort($anchors, fn($a, $b) => strlen($b) <=> strlen($a) ?: strcmp($a, $b));
    // Brand names match only in their own casing ("Weaver", "CAMP", "At Height").
    $rx = [];
    foreach ($anchors as $k => $_) {
        $word = isset($brandNames[$k]) ? $brandNames[$k] : $k;
        $rx[$k] = '/(?<![\w\-])' . str_replace('\ ', '[\s\-]+', preg_quote($word, '/')) . 's?(?![\w\-])/' . (isset($brandNames[$k]) ? '' : 'i');
    }
    // Index anchors by their first word, so a page only tries phrases that could match.
    $byWord = [];
    foreach ($anchors as $k => $_) $byWord[preg_split('/[\s\-]+/', $k)[0]][] = $k;
    return ['anchors' => $anchors, 'rx' => $rx, 'type' => $type, 'byWord' => $byWord, 'best' => $best, 'traffic' => $traffic];
})();

// Phase 1: every page's candidate links. $fields is a list of references to its
// body strings in reading order; $ancestors are pages it already links to by
// breadcrumb, sidebar or brand line, which are worth less as body links.
$autolinkPages = [];
$autolinkCollect = function (string $self, string $set, string $dept, array $fields, array $ancestors, string $cat) use ($autolink, &$autolinkPages, $products): void {
    ['anchors' => $anchors, 'rx' => $rx, 'byWord' => $byWord] = $autolink;
    // Text with existing links blanked out, so a phrase is never matched inside one.
    $plains = [];
    $linked = [$self => true];
    foreach ($fields as $fi => $t) {
        $plains[$fi] = preg_replace_callback('#<a [^>]*>.*?</a>#', fn($m) => str_repeat("\0", strlen($m[0])), $t);
        preg_match_all('#<a href="([^"]*)">#', $t, $m);
        foreach ($m[1] as $h) $linked[$h] = true;
    }
    $try = [];
    foreach (array_unique(preg_split('/[^a-z0-9\']+/', strtolower(implode(' ', $plains)), -1, PREG_SPLIT_NO_EMPTY)) as $w) {
        foreach ($byWord[$w] ?? [] as $k) $try[$k] = true;
    }
    $cands = [];
    foreach ($try as $k => $_) {
        [$to, $score, $spec] = $anchors[$k];
        if (isset($linked[$to])) continue;
        if (!$spec && isset($products[$to]) && !str_starts_with($cat, $products[$to]['category'])
            && !str_starts_with($products[$to]['category'], $cat ?: "\0")) continue;
        foreach ($plains as $fi => $plain) {
            if (preg_match($rx[$k], $plain)) {
                $score *= in_array($to, $ancestors, true) ? 0.25 : 1;
                $cands[] = [$score, $k, $to, $fi];
                break;
            }
        }
    }
    $autolinkPages[$self] = ['set' => $set, 'dept' => $dept, 'fields' => $fields, 'linked' => $linked, 'cands' => $cands];
};

$sectionRefs = function (array &$sections): array {
    $refs = [];
    foreach ($sections as &$s) foreach (['p', 'list'] as $k) if (isset($s[$k])) foreach ($s[$k] as &$t) $refs[] = &$t;
    return $refs;
};
$faqRefs = function (array &$faq): array {
    $refs = [];
    foreach ($faq as &$f) $refs[] = &$f['a'];
    return $refs;
};
$trailOf = function (?string $cat) use (&$categories): array {
    $out = [];
    for ($q = $cat; $q !== null && isset($categories[$q]); $q = $categories[$q]['parent']) $out[] = $q;
    return $out;
};
$deptOf = fn(string $path) => explode('/', trim($path, '/'))[0];

foreach ($products as $path => &$p) {
    $p['body'] ??= []; $p['faq'] ??= [];
    $anc = $trailOf($p['category']);
    if ($p['brand_path']) $anc[] = $p['brand_path'];
    $autolinkCollect($path, 'products', $deptOf($p['category']), array_merge($sectionRefs($p['body']), $faqRefs($p['faq'])), $anc, $p['category']);
}
unset($p);
foreach ($categories as $path => &$c) {
    $c['guide'] ??= []; $c['faq'] ??= [];
    $autolinkCollect($path, 'categories', $deptOf($path), array_merge($sectionRefs($c['guide']), $faqRefs($c['faq'])), $trailOf($c['parent']), $path);
}
unset($c);
foreach ($guides as $path => &$g) {
    $g['sections'] ??= []; $g['faq'] ??= [];
    $autolinkCollect($path, 'guides', '', array_merge($sectionRefs($g['sections']), $faqRefs($g['faq'])), [], '');
}
unset($g);
foreach ($brands as $path => &$b) {
    $refs = [];
    foreach ($b['about'] ?? [] as $i => $_) $refs[] = &$b['about'][$i];
    $autolinkCollect($path, 'brands', '', $refs, [], '');
    unset($refs);
}
unset($b);

// Phase 2: hand out links, best first. A candidate from the target's own
// department ranks ahead of the same score from elsewhere.
$targetDept = function (string $to) use ($autolink, $products, $deptOf): string {
    return match ($autolink['type'][$to]) {
        'products' => $deptOf($products[$to]['category']),
        'categories' => $deptOf($to),
        default => '',
    };
};
$queue = [];
foreach ($autolinkPages as $self => $pg) {
    foreach ($pg['cands'] as [$score, $k, $to, $fi]) {
        $same = $pg['dept'] !== '' && $pg['dept'] === $targetDept($to);
        $queue[] = [$score * ($same ? 1 : 0.5), $self, $k, $to, $fi];
    }
}
usort($queue, fn($a, $b) => $b[0] <=> $a[0] ?: strcmp($a[1], $b[1]) ?: strcmp($a[2], $b[2]));

$autolinkLog = [];
$inbound = [];
$added = [];
$perField = [];
foreach ($queue as [$score, $self, $k, $to, $fi]) {
    $pg = &$autolinkPages[$self];
    $set = $pg['set'];
    if (($added[$self] ?? 0) >= AUTOLINK_MAX[$set] || isset($pg['linked'][$to])
        || ($perField["$self#$fi"] ?? 0) >= AUTOLINK_PER_PARA
        || ($inbound[$to] ?? 0) >= AUTOLINK_INBOUND[$autolink['type'][$to]]) { unset($pg); continue; }
    $t = &$pg['fields'][$fi];
    // Match again on the current text: links added earlier move offsets and may cover the phrase.
    $plain = preg_replace_callback('#<a [^>]*>.*?</a>#', fn($m) => str_repeat("\0", strlen($m[0])), $t);
    if (preg_match($autolink['rx'][$k], $plain, $mm, PREG_OFFSET_CAPTURE)) {
        [$word, $at] = $mm[0];
        $t = substr($t, 0, $at) . '<a href="' . $to . '">' . $word . '</a>' . substr($t, $at + strlen($word));
        $pg['linked'][$to] = true;
        $perField["$self#$fi"] = ($perField["$self#$fi"] ?? 0) + 1;
        $added[$self] = ($added[$self] ?? 0) + 1;
        $inbound[$to] = ($inbound[$to] ?? 0) + 1;
        $autolinkLog[] = [$self, $word, $to];
    }
    unset($t, $pg);
}
unset($autolinkPages);

usort($autolinkLog, fn($a, $b) => strcmp($a[0], $b[0]) ?: strcmp($a[2], $b[2]));
$fh = fopen("$root/seo-data/internal-links.csv", 'w');
fputcsv($fh, ['page', 'anchor', 'target'], ',', '"', '');
foreach ($autolinkLog as $row) fputcsv($fh, $row, ',', '"', '');
fclose($fh);
printf("autolink: %d links added across %d pages, %d targets\n", count($autolinkLog),
    count(array_unique(array_column($autolinkLog, 0))), count(array_unique(array_column($autolinkLog, 2))));

// ---- Popular searches ---------------------------------------------------------------
const POPULAR_PER_DEPT = 16;
const POPULAR_UPPER = ['ansi', 'ngk', 'grcs', 'ehs', 'cmi', 'erb', 'mrs', 'srs', 'ppe', 'xp'];
$brandCase = [];
foreach ($brands as $b) if (!str_contains($b['name'], ' ')) $brandCase[strtolower($b['name'])] = $b['name'];
$label = [];
foreach ($autolink['best'] as $k => [$to, $vol]) {
    $x = $products[$to] ?? $categories[$to] ?? $brands[$to] ?? $guides[$to];
    $own = ' ' . strtolower(preg_replace('/[^\w]+/', ' ', ($x['name'] ?? $x['h1'] ?? '') . ' ' . ($x['h1'] ?? '') . ' ' . ($x['keyword'] ?? '') . ' ' . ($x['brand_name'] ?? ''))) . ' ';
    $ws = explode(' ', $k);
    // Not a usable label: a repeated word ("carabiner carabiner"), a split fraction ("1 2"), or too long.
    if (count($ws) > 5 || count(array_unique($ws)) < count($ws) || preg_match('/\b\d+ \d+\b/', $k)) continue;
    $fits = true;
    foreach (preg_split('/[^\w]+/', $k, -1, PREG_SPLIT_NO_EMPTY) as $w) {
        if (!str_contains($own, " $w ") && !str_contains($own, ' ' . rtrim($w, 's') . ' ') && !str_contains($own, " {$w}s ")) { $fits = false; break; }
    }
    if ($fits && $vol > ($label[$to][1] ?? -1)) $label[$to] = [$k, $vol];
}
$popular = [];
foreach ($autolink['traffic'] as $to => $tr) {
    if (!isset($label[$to])) continue;
    $kind = $autolink['type'][$to];
    $dept = match ($kind) { 'products' => $deptOf($products[$to]['category']), 'categories' => $deptOf($to), default => '' };
    // Title case; brand names keep their own casing ("NGK", "CAMP"), model codes go upper case ("372XP").
    $text = implode(' ', array_map(fn($w) => $brandCase[$w] ?? (preg_match('/\d/', $w) || in_array($w, POPULAR_UPPER, true) ? strtoupper($w) : ucfirst($w)), explode(' ', $label[$to][0])));
    $row = [$text, $to, $tr];
    if ($dept !== '') $popular[$dept][] = $row;
    $popular[''][] = $row;
}
foreach ($popular as &$rows) {
    usort($rows, fn($a, $b) => $b[2] <=> $a[2] ?: strcmp($a[1], $b[1]));
    $rows = array_map(fn($r) => [$r[0], $r[1]], array_slice($rows, 0, POPULAR_PER_DEPT));
}
unset($rows);
printf("popular: %d departments\n", count($popular) - 1);
