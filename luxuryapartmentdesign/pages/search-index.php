<?php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=3600');
$out = [];
foreach (articles() as $a) {
    $out[] = ['t' => $a['h1'], 'u' => '/' . $a['slug'] . '/', 'c' => CATEGORIES[$a['category']]['name'] ?? '', 'k' => $a['keyword'] . ' ' . implode(' ', $a['secondary_keywords'] ?? [])];
}
foreach (TOOLS as $s => $t) {
    $out[] = ['t' => $t['name'], 'u' => '/tools/' . $s . '/', 'c' => 'Free tool', 'k' => $t['short'] . ' calculator tool'];
}
echo json_encode($out, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
