<?php
// JSON API used by app.js (and the offline cache).

function json_out($data, int $status = 200, int $maxAge = 86400): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: public, max-age=' . $maxAge);
    header('Access-Control-Allow-Origin: *');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}

function api(string $path): void {
    $vers = versions();
    $seg = explode('/', trim(substr($path, 5), '/'));   // after "/api/"
    $route = $seg[0] ?? '';

    if ($route === 'chapter' && count($seg) === 4 && isset($vers[$seg[1]], books()[$seg[2]]) && ctype_digit($seg[3])) {
        [$_, $ver, $slug, $c] = $seg;
        $c = (int)$c;
        $book = books()[$slug];
        if ($c < 1 || $c > count($book['verses'])) { json_out(['error' => 'not found'], 404); return; }
        json_out([
            'ver' => $ver, 'book' => $slug, 'name' => book_name($book, $ver), 'ch' => $c,
            'verses' => chapter_text($ver, $slug, $c),
            // what the reader shows: [first verse, last verse, version, text]
            'rows' => array_map(fn($r) => [$r['n'], $r['to'], $r['src'], $r['text']], resolve_chapter($ver, $slug, $c)),
        ]);
        return;
    }

    if ($route === 'commentary' && count($seg) === 4 && isset(books()[$seg[1]]) && ctype_digit($seg[2]) && ctype_digit($seg[3])) {
        [$_, $slug, $c, $v] = $seg;
        $c = (int)$c; $v = (int)$v;
        $book = books()[$slug];
        if ($c < 1 || $c > count($book['verses']) || $v < 1 || $v > $book['verses'][$c - 1]) { json_out(['error' => 'not found'], 404); return; }
        $items = [];
        foreach (COMMENTARIES as $id => $meta) {
            $f = DATA_DIR . "/commentary/$id/$slug.json";
            if (!is_file($f)) continue;
            $d = json_decode(file_get_contents($f), true);
            $row = $d['m'][$c - 1];
            // a verse without its own note belongs to the passage note before it
            $from = $v;
            while ($from > 1 && $row[$from - 1] === -1) $from--;
            $i = $row[$from - 1];
            if ($i === -1) continue;
            // the whole passage this note covers within the chapter
            $from = array_search($i, $row, true) + 1;
            $to = max(array_keys($row, $i, true)) + 1;
            while ($to < count($row) && $row[$to] === -1) $to++;
            $items[] = ['id' => $id, 'name' => $meta['name'], 'short' => $meta['short'], 'from' => $from, 'to' => $to, 'html' => $d['e'][$i]];
        }
        json_out(['book' => $slug, 'ch' => $c, 'v' => $v, 'items' => $items, 'license' => 'Public domain'], 200, 604800);
        return;
    }

    if ($route === 'push') {
        require_once __DIR__ . '/push.php';
        $act = $seg[1] ?? '';
        if ($act === 'key') { json_out(['key' => vapid_keys()['public'], 'hour' => REMINDER_HOUR], 200, 86400); return; }
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') { json_out(['error' => 'POST only'], 405, 0); return; }
        $in = json_decode(file_get_contents('php://input', false, null, 0, 8192), true) ?: [];
        if ($act === 'subscribe') {
            $sub = $in['subscription'] ?? [];
            $sub['tz'] = $in['tz'] ?? 'UTC';
            $sub['hour'] = $in['hour'] ?? REMINDER_HOUR;
            $ok = sub_save($sub);
            if ($ok && !empty($in['read'])) sub_mark_read((string)$sub['endpoint'], (string)$in['read']);
            json_out(['ok' => $ok], $ok ? 200 : 400, 0); return;
        }
        if ($act === 'read') { sub_mark_read((string)($in['endpoint'] ?? ''), (string)($in['date'] ?? '')); json_out(['ok' => true], 200, 0); return; }
        if ($act === 'unsubscribe') { sub_delete((string)($in['endpoint'] ?? '')); json_out(['ok' => true], 200, 0); return; }
        json_out(['error' => 'not found'], 404, 0); return;
    }

    if ($route === 'votd') {
        $date = preg_match('/^\d{4}-\d{2}-\d{2}$/', $_GET['date'] ?? '') ? $_GET['date'] : site_today();
        [$slug, $c, $v] = votd_for($date);
        $out = ['date' => $date, 'book' => $slug, 'ch' => $c, 'v' => $v, 'text' => []];
        foreach ($vers as $k => $_) {
            $row = verse_display($k, $slug, $c, $v);
            $out['text'][$k] = $row['text'];
            $out['src'][$k] = $row['src'];
            $out['ref'][$k] = book_name(books()[$slug], $row['src']) . " $c:" . range_label($row);
        }
        json_out($out, 200, 3600);
        return;
    }

    if ($route === 'search') {
        $ver = isset($vers[$_GET['v'] ?? '']) ? $_GET['v'] : 'ta';
        $q = mb_substr(trim($_GET['q'] ?? ''), 0, 200);
        $ref = parse_ref($q);
        $t = in_array($_GET['t'] ?? '', ['ot', 'nt'], true) ? $_GET['t'] : '';
        $res = $q === '' ? ['total' => 0, 'results' => []] : search($ver, $q, $t, max(0, (int)($_GET['offset'] ?? 0)), 30);
        $rows = array_map(function ($r) use ($ver) {
            $b = book_by_index($r[0]);
            return ['book' => $b['slug'], 'ch' => $r[1], 'v' => $r[2], 'ref' => ref_label($b, $ver, $r[1], $r[2]), 'text' => $r[3]];
        }, $res['results']);
        json_out(['q' => $q, 'ver' => $ver, 'total' => $res['total'], 'results' => $rows,
            'ref' => $ref ? ['book' => $ref[0], 'ch' => $ref[1], 'v' => $ref[2], 'url' => url_for($ver, $ref[0], $ref[1], $ref[2])] : null], 200, 3600);
        return;
    }

    if ($route === 'ref') {
        $ref = parse_ref($_GET['q'] ?? '');
        $ver = isset($vers[$_GET['v'] ?? '']) ? $_GET['v'] : 'ta';
        json_out($ref ? ['book' => $ref[0], 'ch' => $ref[1], 'v' => $ref[2], 'url' => url_for($ver, $ref[0], $ref[1], $ref[2])] : null);
        return;
    }

    json_out(['error' => 'not found'], 404);
}
