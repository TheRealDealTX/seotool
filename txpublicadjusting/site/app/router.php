<?php
/** Request routing: redirects, special files, then pages. */

function route(): void
{
    $uri = $_SERVER['REQUEST_URI'] ?? '/';
    $path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
    $query = parse_url($uri, PHP_URL_QUERY);
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

    if (!is_production()) {
        header('X-Robots-Tag: noindex, nofollow');
    }
    // Force HTTPS (TLS ends upstream, so check the forwarded scheme) and the bare domain.
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure && $method === 'GET') {
        redirect('https://' . request_host() . $path . ($query ? "?$query" : ''));
    }
    if (request_host() === 'www.' . PRODUCTION_HOST) {
        redirect(CANONICAL_ORIGIN . $path . ($query ? "?$query" : ''));
    }

    if ($path === '/robots.txt') {
        header('Content-Type: text/plain; charset=utf-8');
        echo is_production()
            ? "User-agent: *\nDisallow: /storage/\nDisallow: /app/\nDisallow: /content/\n\nSitemap: " . CANONICAL_ORIGIN . "/sitemap.xml\n"
            : "User-agent: *\nDisallow: /\n";
        return;
    }
    if ($path === '/site.webmanifest') {
        header('Content-Type: application/manifest+json; charset=utf-8');
        header('Cache-Control: public, max-age=86400');
        readfile(SITE_ROOT . '/app/site.webmanifest.json');
        return;
    }
    if ($path === '/sitemap.xml') {
        render_sitemap();
        return;
    }
    if ($path === '/contact-submit/' || $path === '/contact-submit') {
        handle_contact($method);
        return;
    }

    $lower = strtolower($path);
    $key = rtrim($lower, '/') . '/';

    // WordPress leftovers: gone for good.
    if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|xmlrpc\.php|wp-login\.php|wp-cron\.php)#', $lower)) {
        render_gone();
        return;
    }
    if (preg_match('#^/(category|tag)/#', $lower) || $key === '/feed/' || preg_match('#/feed/$#', $key)) {
        redirect('/blog/');
    }
    if (preg_match('#^/author/#', $lower)) {
        redirect('/about-us/');
    }
    // ?p=123 / ?page_id= style WordPress links.
    if ($path === '/' && $query && preg_match('/(^|&)(p|page_id|cat)=\d+/', $query)) {
        redirect('/');
    }

    $map = require SITE_ROOT . '/app/redirects.php';
    if (isset($map['redirects'][$key])) {
        redirect($map['redirects'][$key]);
    }
    if (in_array($key, $map['gone'], true)) {
        render_gone();
        return;
    }

    // Canonical form: lowercase with a trailing slash.
    if ($path !== '/' && ($path !== $key)) {
        if (dispatch($key, true)) {
            redirect($key . ($query ? "?$query" : ''));
        }
        render_404();
        return;
    }
    if (!dispatch($path, false)) {
        render_404();
    }
}

/**
 * Render the page for a normalized path. With $probe = true only reports
 * whether a page exists (used to decide on the trailing-slash redirect).
 */
function dispatch(string $path, bool $probe): bool
{
    $simple = [
        '/'                => 'render_home',
        '/about-us/'       => 'render_about',
        '/contact-us/'     => 'render_contact',
        '/blog/'           => 'render_blog',
        '/areas/'          => 'render_areas_hub',
        '/tools/'          => 'render_tools_hub',
        '/services/'       => fn() => render_hub('services', 'Services'),
        '/commercial-claims/' => fn() => render_hub('commercial', 'Commercial claims'),
        '/privacy-policy/' => fn() => render_simple_page('privacy-policy', 'Privacy policy'),
        '/terms-of-use/'   => fn() => render_simple_page('terms-of-use', 'Terms of use'),
    ];
    if (isset($simple[$path])) {
        if (!$probe) {
            $simple[$path]();
        }
        return true;
    }

    $patterns = [
        '#^/post/([a-z0-9-]+)/$#'              => ['posts', [['Guides', '/blog/']]],
        '#^/services/([a-z0-9-]+)/$#'          => ['services', [['Services', '/services/']]],
        '#^/commercial-claims/([a-z0-9-]+)/$#' => ['commercial', [['Commercial claims', '/commercial-claims/']]],
        '#^/areas/([a-z0-9-]+)/$#'             => ['areas', [['Service areas', '/areas/']]],
        '#^/tools/([a-z0-9-]+)/$#'             => ['tools', [['Free tools', '/tools/']]],
    ];
    foreach ($patterns as $re => [$type, $trail]) {
        if (!preg_match($re, $path, $m) || $m[1] === 'index') {
            continue;
        }
        $p = load_content($type, $m[1]);
        if (!$p) {
            return false;
        }
        if ($probe) {
            return true;
        }
        $crumbs = array_merge([['Home', '/']], $trail, [[$p['crumb'] ?? ($p['city'] ?? $p['h1'] ?? $p['title']), $path]]);
        if ($type === 'areas') {
            render_area($p, $path, $crumbs);
        } elseif ($type === 'tools') {
            render_tool($p, $path, $crumbs);
        } else {
            render_article($p, $path, $crumbs);
        }
        return true;
    }
    return false;
}

function render_404(): void
{
    send_status(404);
    render_page([
        'title'       => 'Page not found',
        'description' => 'That page has moved or no longer exists.',
        'path'        => '/404/',
        'noindex'     => true,
    ], function () {
        ?>
<section class="hero hero--page hero--center">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <p class="eyebrow">Error 404</p>
      <h1>We couldn't find that page</h1>
      <p class="hero__lead">The page may have moved when we reorganized the site. These are the most useful places to start.</p>
      <div class="hero__btns">
        <a class="btn btn--primary" href="/">Home</a>
        <a class="btn btn--light" href="/blog/">Claim guides</a>
        <a class="btn btn--light" href="/tools/">Free tools</a>
      </div>
    </div>
  </div>
</section>
<?php
    });
}

function render_gone(): void
{
    send_status(410);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Gone</title><p>This page has been permanently removed. <a href="/">Go to the homepage</a>.</p>';
}

function render_sitemap(): void
{
    header('Content-Type: application/xml; charset=utf-8');
    $urls = [['/', date('Y-m-d')]];
    foreach (['/about-us/', '/contact-us/', '/services/', '/commercial-claims/', '/areas/', '/blog/', '/tools/', '/privacy-policy/', '/terms-of-use/'] as $u) {
        $urls[] = [$u, null];
    }
    foreach (['services', 'commercial', 'areas', 'tools', 'posts'] as $type) {
        foreach (load_all($type) as $slug => $p) {
            $urls[] = [url_for($type, $slug), $p['updated'] ?? null];
        }
    }
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($urls as [$u, $mod]) {
        echo '  <url><loc>' . h(canonical($u)) . '</loc>' . ($mod ? '<lastmod>' . h($mod) . '</lastmod>' : '') . "</url>\n";
    }
    echo '</urlset>' . "\n";
}
