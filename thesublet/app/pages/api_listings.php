<?php defined('APP') || exit;

$f = filters_from_query();
if (preg_match('/^[a-z]{2}$/', get('state'))) $f['state'] = get('state');
if (preg_match('/^[a-z0-9-]+$/', get('city'))) $f['city'] = get('city');
if (get('ids') !== '') {
    $f = ['ids' => array_slice(array_filter(array_map('intval', explode(',', get('ids')))), 0, 60)];
    if (!$f['ids']) json_out(['total' => 0, 'items' => []]);
}
$page = max(1, (int)get('page', '1'));
$per = min(200, max(1, (int)get('per', (string)PER_PAGE)));
$res = listing_search($f, $per, ($page - 1) * $per);
$cards = listing_card_data($res['items']);
if (get('full') === '1') {
    // for the compare page
    $byId = array_column($res['items'], null, 'id');
    $am = amenity_options();
    foreach ($cards as &$c) {
        $l = $byId[$c['id']];
        $c['deposit'] = (int)$l['deposit'];
        $c['amenities'] = array_values(array_map(fn($a) => $am[$a] ?? $a, array_filter(explode(',', (string)$l['amenities']))));
        $c['pets_h'] = pet_options()[$l['pets']] ?? '';
    }
    unset($c);
}
foreach ($cards as &$c) $c['html'] = listing_card_html($c);
unset($c);
header('Cache-Control: public, max-age=60');
json_out(['total' => $res['total'], 'page' => $page, 'pages' => (int)ceil($res['total'] / $per), 'items' => $cards]);
