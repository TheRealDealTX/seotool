<?php
// michellewhitephoto.com - static site front controller.
// The host serves existing files directly and sends "/" and unknown paths here
// (see README, "Hosting note").
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$prod = 'michellewhitephoto.com';
$isProd = ($host === $prod || $host === 'www.' . $prod);
$scheme = 'https://';

// Canonical host/scheme once the real domain is attached.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($isProd && ($insecure || $host === 'www.' . $prod)) {
    header('Location: ' . $scheme . $prod . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

function serve($file, $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile($file);
    exit;
}

if ($path === '/' || $path === '/index.php' || $path === '/home') {
    serve(__DIR__ . '/home.html');
}

// robots.txt: block indexing on the temporary hostingersite.com domain.
if ($path === '/robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    if ($isProd) {
        echo "User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: https://$prod/sitemap.xml\n";
    } else {
        header('X-Robots-Tag: noindex, nofollow');
        echo "User-agent: *\nDisallow: /\n";
    }
    exit;
}

// Legacy URLs from the old site.
$legacy = [
    '/about' => '/about/',
    '/blog' => '/blog/',
    '/journal' => '/blog/',
    '/contact' => '/contact/',
    '/weddings' => '/weddings/',
    '/interiors' => '/interiors/',
    '/portfolio' => '/weddings/',
    '/wedding' => '/weddings/',
    '/info' => '/about/',
    '/investment' => '/weddings/',
];
$p = rtrim($path, '/');
if (isset($legacy[$p]) && $path !== $legacy[$p]) {
    header('Location: ' . $legacy[$p], true, 301);
    exit;
}

// Squarespace-era feeds and paginated/tag URLs.
if (preg_match('#^/blog/(tag|category)/#', $path) || isset($_GET['format'])) {
    header('Location: /blog/', true, 301);
    exit;
}

// Directory without trailing slash.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}

serve(__DIR__ . '/404.html', 404);
