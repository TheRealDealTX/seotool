<?php defined('SNW') || (http_response_code(404) && exit);
/* /blog/, /blog/page/N/, /blog/category/<cat>/ (+ /page/N/) */
$cats = categories();
if ($category !== null && !isset($cats[$category])) { not_found(); return; }
$all = $category ? array_filter(posts(), fn($p) => $p['category'] === $category) : posts();
$per = 12;
$pages = max(1, (int) ceil(count($all) / $per));
if ($page < 1 || $page > $pages) { not_found(); return; }
if ($page === 1 && str_contains($path, '/page/')) redirect($category ? '/blog/category/' . $category . '/' : '/blog/');
$base = $category ? '/blog/category/' . $category . '/' : '/blog/';
$canonical = $page > 1 ? $base . 'page/' . $page . '/' : $base;
$items = array_slice($all, ($page - 1) * $per, $per);
$heading = $category ? $cats[$category]['name'] : 'Seattle Real Estate Blog';
$crumbs = [['Blog', '/blog/']];
if ($category) $crumbs[] = [$cats[$category]['name'], $base];
render('blog', compact('items', 'page', 'pages', 'base', 'category', 'heading'), [
    'title'       => ($category ? $cats[$category]['name'] . ' | Seattle Real Estate Blog' : 'Seattle Real Estate Blog: Buying, Selling & Living') . ($page > 1 ? ' — Page ' . $page : ''),
    'description' => ($category ? $cats[$category]['description'] : 'Local advice on buying and selling homes in Seattle, neighborhood guides, home improvement ideas and market insights.') . ($page > 1 ? ' Page ' . $page . ' of ' . $pages . '.' : ''),
    'canonical'   => $canonical,
    'prev'        => $page > 1 ? ($page === 2 ? $base : $base . 'page/' . ($page - 1) . '/') : null,
    'next'        => $page < $pages ? $base . 'page/' . ($page + 1) . '/' : null,
    'schema'      => [schema_breadcrumbs($crumbs), schema_item_list(array_map(fn($p) => '/blog/' . $p['slug'] . '/', $items))],
]);
