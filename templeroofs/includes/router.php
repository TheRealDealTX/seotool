<?php
/** URL routing. */
defined('TR_ROOT') || exit;

function render_page(string $name, array $params): void
{
    extract($params, EXTR_SKIP);
    require TR_INC . '/pages/' . $name . '.php';
    exit;
}

function not_found(): void
{
    render_page('404', []);
}

function route_request(string $uri): void
{
    $path = rawurldecode((string) parse_url($uri, PHP_URL_PATH));
    $query = (string) parse_url($uri, PHP_URL_QUERY);

    // Legacy/odd paths: /index.php -> /
    if ($path === '/index.php') {
        header('Location: /' . ($query !== '' ? '?' . $query : ''), true, 301);
        exit;
    }
    // Add a trailing slash to extension-less paths (one canonical form).
    if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('~\.[a-z0-9]{2,5}$~i', $path)) {
        header('Location: ' . $path . '/' . ($query !== '' ? '?' . $query : ''), true, 301);
        exit;
    }
    if (preg_match('~//|[^a-z0-9/._-]~i', $path)) {
        not_found();
    }
    $seg = array_values(array_filter(explode('/', trim($path, '/')), 'strlen'));
    $n = count($seg);
    $first = $seg[0] ?? '';

    $static = [
        ''                     => 'home',
        'about'                => 'about',
        'services'             => 'services',
        'free-roof-inspection' => 'free-roof-inspection',
        'service-areas'        => 'areas',
        'tools'                => 'tools',
        'weather'              => 'weather',
        'blog'                 => 'blog',
        'contact'              => 'contact',
        'privacy-policy'       => 'privacy-policy',
        'terms-of-use'         => 'terms-of-use',
        'sitemap'              => 'html-sitemap',
        'thank-you'            => 'thank-you',
    ];

    if ($n <= 1 && isset($static[$first]) && $path === ($first === '' ? '/' : '/' . $first . '/')) {
        render_page($static[$first], []);
    }
    if ($path === '/sitemap.xml') {
        render_page('sitemap-xml', []);
    }
    if ($path === '/api/lead/') {
        handle_lead_post();
        exit;
    }
    if ($path === '/api/weather/') {
        require_once TR_INC . '/weather.php';
        json_out(weather_payload());
    }
    if ($n === 2 && $first === 'services' && ($s = service($seg[1]))) {
        render_page('service', ['service' => $s]);
    }
    if ($n === 2 && $first === 'service-areas' && ($a = area($seg[1]))) {
        render_page('area', ['area' => $a]);
    }
    if ($n === 2 && $first === 'tools' && isset(catalog('tools')[$seg[1]])) {
        render_page('tool-' . $seg[1], ['tool' => catalog('tools')[$seg[1]], 'toolSlug' => $seg[1]]);
    }
    if ($n === 2 && $first === 'blog' && $seg[1] === 'feed') {
        render_page('feed', []);
    }
    if ($n === 2 && $first === 'blog' && ($p = post($seg[1]))) {
        render_page('post', ['post' => $p]);
    }
    if ($n === 3 && $first === 'blog' && $seg[1] === 'category' && isset(catalog('blog_categories')[$seg[2]])) {
        render_page('blog', ['category' => $seg[2]]);
    }
    not_found();
}
