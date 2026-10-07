<?php
// Live headline wire: Google News RSS search per topic, cached 20 minutes on disk.
require __DIR__ . '/lib.php';
$topics = [
    'cebu'   => 'Cebu when:2d',
    'davao'  => 'Davao when:2d',
    'other'  => 'Philippines travel when:7d',
    'ph'     => 'Philippines when:1d',
    'sports' => 'Philippines sports OR PBA OR Gilas when:2d',
];
$t = $_GET['topic'] ?? 'cebu';
if (!isset($topics[$t])) $t = 'cebu';
$cache = cd_data_dir() . '/news-' . $t . '.json';
header('Cache-Control: public, max-age=600');
if (is_file($cache) && filemtime($cache) > time() - 1200) {
    header('Content-Type: application/json; charset=utf-8');
    readfile($cache);
    exit;
}
$url = 'https://news.google.com/rss/search?q=' . rawurlencode($topics[$t]) . '&hl=en-PH&gl=PH&ceid=PH:en';
$ctx = stream_context_create(['http' => ['timeout' => 8, 'user_agent' => 'Mozilla/5.0 (compatible; CebuDavaoNewsWire/1.0; +https://cebudavao.com/news/)']]);
$xml = @file_get_contents($url, false, $ctx);
$items = [];
if ($xml && ($rss = @simplexml_load_string($xml))) {
    foreach ($rss->channel->item as $it) {
        $title = (string)$it->title;
        $source = (string)$it->source;
        if ($source && str_ends_with($title, ' - ' . $source)) $title = substr($title, 0, -strlen(' - ' . $source));
        $items[] = ['title' => $title, 'link' => (string)$it->link, 'source' => $source,
                    'date' => date('c', strtotime((string)$it->pubDate))];
        if (count($items) >= 12) break;
    }
}
if (!$items && is_file($cache)) {           // serve stale on failure
    header('Content-Type: application/json; charset=utf-8');
    readfile($cache);
    exit;
}
$out = json_encode(['topic' => $t, 'updated' => date('c'), 'items' => $items], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
if ($items) @file_put_contents($cache, $out);
header('Content-Type: application/json; charset=utf-8');
echo $out;
