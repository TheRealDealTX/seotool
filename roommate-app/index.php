<?php
// Rise Roommates — front controller.
require __DIR__ . '/app/bootstrap.php';

$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
$path = '/' . trim($path, '/');

// [method(s), pattern, handler file, function]
$routes = [
    ['GET', '/', 'pages', 'page_landing'],
    ['GET', '/terms', 'pages', 'page_terms'],
    ['GET', '/privacy', 'pages', 'page_privacy'],
    ['GET', '/safety', 'pages', 'page_safety'],

    ['GET|POST', '/login', 'auth', 'auth_login'],
    ['GET|POST', '/register', 'auth', 'auth_register'],
    ['POST', '/logout', 'auth', 'auth_logout'],
    ['GET|POST', '/forgot', 'auth', 'auth_forgot'],
    ['GET|POST', '/reset', 'auth', 'auth_reset'],

    ['GET', '/home', 'feed', 'feed_home'],
    ['POST', '/post', 'feed', 'feed_create'],
    ['GET', '/post/(\d+)', 'feed', 'feed_show'],
    ['POST', '/post/(\d+)/like', 'feed', 'feed_like'],
    ['POST', '/post/(\d+)/comment', 'feed', 'feed_comment'],
    ['POST', '/post/(\d+)/delete', 'feed', 'feed_delete'],
    ['POST', '/comment/(\d+)/delete', 'feed', 'feed_comment_delete'],
    ['POST', '/report', 'feed', 'feed_report'],

    ['GET', '/discover', 'discover', 'discover_index'],

    ['GET', '/u/([A-Za-z0-9_]+)', 'profile', 'profile_show'],
    ['GET|POST', '/profile/edit', 'profile', 'profile_edit'],
    ['GET|POST', '/settings', 'profile', 'profile_settings'],

    ['GET', '/friends', 'friends', 'friends_index'],
    ['POST', '/friend/(\d+)/(add|accept|decline|cancel|remove)', 'friends', 'friends_action'],
    ['POST', '/block/(\d+)', 'friends', 'friends_block'],
    ['POST', '/unblock/(\d+)', 'friends', 'friends_unblock'],

    ['GET', '/messages', 'messages', 'messages_index'],
    ['GET', '/messages/([A-Za-z0-9_]+)', 'messages', 'messages_thread'],
    ['GET|POST', '/api/conversation/(\d+)', 'messages', 'messages_api'],
    ['GET', '/api/counts', 'messages', 'messages_counts'],

    ['GET', '/properties', 'properties', 'properties_index'],
    ['GET|POST', '/properties/new', 'properties', 'properties_new'],
    ['GET', '/properties/([a-z0-9-]+)', 'properties', 'properties_show'],
    ['POST', '/property/(\d+)/toggle', 'properties', 'properties_toggle'],

    ['GET', '/notifications', 'notifications', 'notifications_index'],

    ['GET', '/match', 'match', 'match_index'],
    ['POST', '/api/swipe', 'match', 'match_swipe'],
    ['GET', '/matches', 'match', 'match_list'],
    ['GET|POST', '/quiz', 'quiz', 'quiz_index'],
    ['GET', '/tools', 'tools', 'tools_index'],
    ['GET', '/tools/rent-split', 'tools', 'tools_rent'],
    ['GET', '/agreements', 'agreement', 'agreement_list'],
    ['GET|POST', '/agreement/([A-Za-z0-9_]+)', 'agreement', 'agreement_show'],
    ['GET|POST', '/api/lounge/(\d+)', 'properties', 'properties_lounge'],
    ['POST', '/api/typing/(\d+)', 'messages', 'messages_typing'],
    ['POST', '/api/message/(\d+)', 'messages', 'messages_action'],
    ['GET', '/api/gifs', 'feed', 'feed_gifs'],
    ['POST', '/api/theme', 'profile', 'profile_theme'],

    ['GET', '/admin', 'admin', 'admin_dashboard'],
    ['GET|POST', '/admin/users', 'admin', 'admin_users'],
    ['GET|POST', '/admin/users/(\d+)', 'admin', 'admin_user'],
    ['GET|POST', '/admin/properties', 'admin', 'admin_properties'],
    ['GET|POST', '/admin/properties/(new|\d+)', 'admin', 'admin_property'],
    ['GET|POST', '/admin/reports', 'admin', 'admin_reports'],
    ['GET|POST', '/admin/posts', 'admin', 'admin_posts'],
    ['GET|POST', '/admin/settings', 'admin', 'admin_settings'],
    ['GET', '/admin/audit', 'admin', 'admin_audit'],
    ['GET|POST', '/admin/sync', 'admin', 'admin_sync'],
    ['GET', '/api/properties', 'properties', 'properties_search'],
];

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
foreach ($routes as [$methods, $pattern, $file, $fn]) {
    if (!preg_match('#^' . $pattern . '$#', $path, $m)) continue;
    if (!in_array($method, explode('|', $methods), true)) {
        http_response_code(405);
        exit('Method not allowed');
    }
    if ($method === 'POST') {
        verify_csrf();
    }
    require APP_DIR . '/pages/' . $file . '.php';
    array_shift($m);
    $fn(...$m);
    exit;
}
not_found();
