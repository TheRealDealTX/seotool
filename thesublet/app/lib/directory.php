<?php defined('APP') || exit;

const PER_PAGE = 24;

/** Read filter params from the query string. */
function filters_from_query(): array
{
    $f = [];
    foreach (['min', 'max'] as $k) if (($v = (int)get($k)) > 0) $f[$k] = $v;
    foreach (['from', 'to'] as $k) if (preg_match('/^\d{4}-\d{2}-\d{2}$/', get($k))) $f[$k] = get($k);
    if (isset(property_types()[get('type')])) $f['type'] = get('type');
    foreach (['furnished', 'pets', 'verified', 'summer'] as $k) if (get($k) === '1') $f[$k] = 1;
    if (in_array(get('sort'), ['price_asc', 'price_desc', 'available'], true)) $f['sort'] = get('sort');
    if (get('q') !== '') $f['q'] = mb_substr(get('q'), 0, 60);
    return $f;
}

function directory_section(array $locked, string $basePath, ?array $center, array $preset = [], ?string $emptyHtml = null, bool $showQ = false): array
{
    $f = filters_from_query() + $preset;
    $page = max(1, (int)get('page', '1'));
    $all = $f + $locked;
    $total = listing_search($all, 1, 0)['total'];
    $pg = paginate($total, PER_PAGE, $page);
    $res = listing_search($all, PER_PAGE, $pg['offset']);
    $cards = listing_card_data($res['items']);
    $jsLocked = $locked + $preset;
    $html = view('directory', ['f' => $f, 'locked' => $jsLocked, 'res' => $res, 'cards' => $cards, 'pg' => $pg, 'basePath' => $basePath, 'center' => $center, 'emptyHtml' => $emptyHtml, 'showQ' => $showQ]);
    return ['html' => $html, 'cards' => $cards, 'total' => $res['total'], 'filtered' => (bool)array_diff_key(filters_from_query(), ['sort' => 1])];
}

function directory_scripts(): array
{
    return [];
}

function leaflet_head(): string
{
    return '<link rel="preconnect" href="https://unpkg.com" crossorigin>';
}
