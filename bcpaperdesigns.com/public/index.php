<?php
// bcpaperdesigns.com front controller. The host serves existing files directly and
// sends "/" and unknown paths here (see README, "Hosting").
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$home = 'https://bcpaperdesigns.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Relative so redirects also work on the preview domain before DNS moves
function go($to) { header('Location: ' . $to, true, 301); exit; }

// Canonical host and scheme, only once the real domain points here
if ($host === 'www.bcpaperdesigns.com' || ($host === 'bcpaperdesigns.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$aliases = ['fire-truck-birthday-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards' => 'fire-truck-birthday-party-decorations', 'monster-birthday-banner-party-decoration-supplies-happy-birthday-handmade-in-usa' => 'monster-birthday-party-decorations', 'reptile-birthday-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards' => 'reptile-birthday-party-decorations', 'reptile-birthday-banner-party-decoration-supplies-happy-birthday-handmade-in-usa' => 'reptile-birthday-party-decorations', 'woodland-animal-themed-baby-shower-decorations-printable-instant-download-banner-centerpiece-cupcakes-thank-you-games' => 'woodland-baby-shower-decorations', 'pink-girl-book-themed-baby-shower-games-printable-instant-download' => 'book-themed-baby-shower-games-printable-instant-download', 'pink-girl-turtle-party-banners-instant-download-pdf-printable-file' => 'pink-girl-turtle-party-banners'];
$themes  = ['pink-elephant-baby-shower-decorations', 'blue-elephant-baby-shower-decorations', 'yellow-elephant-baby-shower-decorations-yellow-and-grey', 'yellow-elephant-baby-shower-banner-for-gender-neutral-party', 'pdf-elephant-baby-shower-or-birthday-decorations-banner-invitations-cake-topper-centerpiece-cupcakes-diy-printable', 'construction-truck-birthday-decorations', 'fire-truck-birthday-party-decorations', 'blue-boy-lion-king-baby-shower-decorations', 'monster-birthday-party-decorations', 'reptile-birthday-party-decorations', 'b-whale-baby-shower-navy-teal-b-br-or-birthday-party-decorations', 'coral-owl-baby-shower-or-birthday-party-decorations', 'ladybug-birthday-party-or-baby-shower-decorations', 'pink-gold-giraffe-baby-shower-or-birthday-party-decorations', 'woodland-baby-shower-decorations', 'dinosaur-birthday-party-or-baby-shower-decorations', 'baby-shark-birthday-party-or-baby-shower-decorations', 'jungle-safari-baby-shower-decorations', 'jungle-safari-baby-shower-decorations-1', 'duck-baby-shower-decorations-blue-yellow', 'pink-girl-rubber-duck-baby-shower-or-birthday-party-decorations', 'pink-hot-air-balloon-baby-shower-decorations', 'book-themed-baby-shower-decorations-printable-instant-download-banner-centerpiece-cupcakes-thank-you-games', 'book-themed-baby-shower-games-printable-instant-download', 'bowling-birthday-cake-topper-bowling-party-decorations-diy-printable-decorations-made-to-match-banner-invitation-signs-cupcake-toppers-favor-tags', 'football-birthday-cake-topper-football-party-decorations-personalized-diy-printable-editable-made-to-match-banner-invitation-signs-cupcake-toppers-favor-tags', 'kids-halloween-birthday-party-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards', 'pink-girl-turtle-party-banners', 'pink-turtle-baby-shower-or-birthday-party-decorations', 'my-little-pony-horse-birthday-party-or-baby-shower-decorations', 'emoji-banner'];
$collections = ['baby-shower-decorations', 'birthday-party-decorations', 'banners'];

// Old Shopify product URLs, including /collections/<c>/products/<slug>
if (preg_match('#^(?:/collections/[^/]+)?/products/([^/.]+)#', $path, $m)) {
    $slug = strtolower($m[1]);
    if (isset($aliases[$slug])) $slug = $aliases[$slug];
    if (in_array($slug, $themes, true)) go('/products/' . $slug . '/');
    go('/collections/');
}
if (preg_match('#^/collections/([^/]+)/?$#', $path, $m)) {
    go(in_array($m[1], $collections, true) ? '/collections/' . $m[1] . '/' : '/collections/');
}
if (preg_match('#^/(collections|products)/?$#', $path)) go('/collections/');
if (preg_match('#^/pages/(about[^/]*)/?$#', $path)) go('/about/');
if (preg_match('#^/pages/(contact[^/]*)/?$#', $path)) go('/contact/');
if (preg_match('#^/blogs?(/.*)?$#', $path) && !is_dir(__DIR__ . $path)) go('/blog/');
if (preg_match('#^/(cart|account|search|checkout|index\.php/.*|my-account|wp-admin|wp-login\.php|feed)(/.*)?$#', $path)) go('/');
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) go($path . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
