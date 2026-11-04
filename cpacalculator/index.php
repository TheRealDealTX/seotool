<?php
/* CPA Calculator — front controller.
 * The Hostinger H5G platform serves existing files directly, ignores .htaccess and sends "/"
 * plus every unknown path here, so all page routing, redirects and 404s happen in this file. */
define('CPA', 1);
require __DIR__ . '/app/bootstrap.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$qs   = parse_url($uri, PHP_URL_QUERY);

function redirect(string $to, int $code = 301): void { header('Location: ' . SITE_ORIGIN . $to, true, $code); exit; }

/* Canonical scheme + host (TLS terminates upstream; X-Forwarded-Proto carries the original scheme). */
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.cpacalculator.com') redirect($uri);

/* Old WordPress ?p= / ?page_id= shortlinks. */
if ($path === '/' && $qs) {
  parse_str($qs, $q);
  $ids = [24 => '/', 27 => '/about-us/', 29 => '/our-methodology/', 31 => '/contact/', 33 => '/blog/', 3 => '/privacy-policy/', 60 => '/terms-of-use/',
          62 => '/disclaimer/', 76 => '/calculators/', 118 => '/calculators/federal-income-tax/', 142 => '/calculators/1099-tax-calculator/',
          84 => '/blog/got-a-1099-exactly-what-to-do-next/', 196 => '/blog/understanding-your-w-2/', 199 => '/blog/quarterly-taxes-101-guide/'];
  $id = (int) ($q['p'] ?? $q['page_id'] ?? 0);
  if ($id && isset($ids[$id])) redirect($ids[$id]);
  if (isset($q['s'])) redirect('/calculators/');
}

/* Legacy WordPress endpoints. */
if (preg_match('#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes)(/|$)#', $path)) redirect('/');
if (preg_match('#^/((post|page|category|author)-sitemap\d*\.xml|sitemap_index\.xml|wp-sitemap.*\.xml)$#', $path)) redirect('/sitemap.xml');
if (preg_match('#^/(feed|comments/feed|blog/feed)/?$#', $path)) redirect('/blog/');
if (preg_match('#^/(author|category|tag)/#', $path)) redirect('/blog/');
if (preg_match('#^/blog/([a-z0-9-]+)/feed/?$#', $path, $m)) redirect('/blog/' . $m[1] . '/');
if (preg_match('#^/topic/guides/(page/\d+/?)?$#', $path) && $path !== '/topic/guides/') redirect('/topic/guides/');
if ($path === '/home.php' || $path === '/index.php') redirect('/');

if ($path === '/sitemap.xml') { require __DIR__ . '/app/sitemap.php'; exit; }

/* Trailing slash for page-style paths. */
if ($path !== '/' && substr($path, -1) !== '/' && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) redirect($path . '/' . ($qs ? '?' . $qs : ''));

$pages = __DIR__ . '/app/pages';
$file = null;
$P = ['path' => $path, 'schema' => [], 'scripts' => []];

$static = [
  '/' => 'home', '/calculators/' => 'calculators/index', '/blog/' => 'blog/index', '/topic/guides/' => 'blog/index',
  '/about-us/' => 'about-us', '/contact/' => 'contact', '/our-methodology/' => 'our-methodology',
  '/disclaimer/' => 'disclaimer', '/privacy-policy/' => 'privacy-policy', '/terms-of-use/' => 'terms-of-use',
];
if (isset($static[$path])) {
  $file = $pages . '/' . $static[$path] . '.php';
} elseif (preg_match('#^/calculators/federal-income-tax/(\d{4,7})/$#', $path, $m)) {
  $AMOUNT = (int) $m[1];
  if (in_array($AMOUNT, SALARY_PAGES, true)) $file = $pages . '/calculators/salary.php';
} elseif (preg_match('#^/calculators/state-income-tax/([a-z-]+)/$#', $path, $m) && ($STATE = state_by_slug($m[1]))) {
  $file = $pages . '/calculators/state.php';
} elseif (preg_match('#^/calculators/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
  $file = $pages . '/calculators/' . $m[1] . '.php';
} elseif (preg_match('#^/blog/([a-z0-9-]+)/$#', $path, $m) && post_is_live($m[1])) {
  $SLUG = $m[1];
  $file = $pages . '/blog/' . $m[1] . '.php';
}

if (!$file || !is_file($file)) {
  http_response_code(404);
  $file = $pages . '/404.php';
}

ob_start();
include $file;
$body = ob_get_clean();
render_page($P, $body);
