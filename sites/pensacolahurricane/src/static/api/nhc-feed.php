<?php
// Latest National Hurricane Center Atlantic products (RSS), cached 10 minutes.
require __DIR__ . '/_lib.php';
$body = ph_cached_fetch('https://www.nhc.noaa.gov/index-at.xml', 600);
if ($body === null) {
    ph_json(['error' => 'NHC feed unavailable', 'items' => []], 502);
}
libxml_use_internal_errors(true);
$xml = simplexml_load_string($body, 'SimpleXMLElement', LIBXML_NOCDATA | LIBXML_NONET);
$items = [];
if ($xml && isset($xml->channel->item)) {
    foreach ($xml->channel->item as $it) {
        $items[] = [
            'title' => trim((string) $it->title),
            'link' => trim((string) $it->link),
            'pubDate' => trim((string) $it->pubDate),
        ];
    }
}
ph_json(['items' => $items], 200, 300);
