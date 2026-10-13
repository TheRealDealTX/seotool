<?php
/** Core helpers: request info, content loading, routing. */

function h($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function request_host(): string
{
    $host = strtolower($_SERVER['HTTP_HOST'] ?? PRODUCTION_HOST);
    return preg_replace('/:\d+$/', '', $host);
}

function is_production(): bool
{
    $host = request_host();
    return $host === PRODUCTION_HOST || $host === 'www.' . PRODUCTION_HOST;
}

function canonical(string $path): string
{
    return CANONICAL_ORIGIN . $path;
}

function asset(string $path): string
{
    $file = SITE_ROOT . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return $path . '?v=' . $v;
}

function tel_link(): string
{
    return 'tel:' . BIZ['phone_e164'];
}

function sms_link(): string
{
    return 'sms:' . BIZ['phone_e164'];
}

/** Load a content file (returns its array) or null. Slugs are validated. */
function load_content(string $type, string $slug): ?array
{
    if (!preg_match('/^[a-z0-9-]+$/', $slug) || !preg_match('/^[a-z]+$/', $type)) {
        return null;
    }
    $file = SITE_ROOT . "/content/$type/$slug.php";
    if (!is_file($file)) {
        return null;
    }
    $data = require $file;
    if (!is_array($data)) {
        return null;
    }
    $data['_type'] = $type;
    $data['_slug'] = $slug;
    $data['_file'] = $file;
    return $data;
}

/** All content items of a type, keyed by slug (skips index.php). */
function load_all(string $type): array
{
    static $cache = [];
    if (isset($cache[$type])) {
        return $cache[$type];
    }
    $items = [];
    foreach (glob(SITE_ROOT . "/content/$type/*.php") as $file) {
        $slug = basename($file, '.php');
        if ($slug === 'index') {
            continue;
        }
        $item = load_content($type, $slug);
        if ($item) {
            $items[$slug] = $item;
        }
    }
    return $cache[$type] = $items;
}

function url_for(string $type, string $slug): string
{
    switch ($type) {
        case 'posts':      return "/post/$slug/";
        case 'services':   return "/services/$slug/";
        case 'commercial': return "/commercial-claims/$slug/";
        case 'areas':      return "/areas/$slug/";
        case 'tools':      return "/tools/$slug/";
        default:           return "/$slug/";
    }
}

function posts_sorted(): array
{
    $posts = load_all('posts');
    uasort($posts, fn($a, $b) => strcmp($b['published'] ?? '', $a['published'] ?? ''));
    return $posts;
}

/** Look up title/description for any internal URL (used for "related" cards). */
function page_for_url(string $url): ?array
{
    $map = [
        '#^/post/([a-z0-9-]+)/$#'              => 'posts',
        '#^/services/([a-z0-9-]+)/$#'          => 'services',
        '#^/commercial-claims/([a-z0-9-]+)/$#' => 'commercial',
        '#^/areas/([a-z0-9-]+)/$#'             => 'areas',
        '#^/tools/([a-z0-9-]+)/$#'             => 'tools',
    ];
    foreach ($map as $re => $type) {
        if (preg_match($re, $url, $m)) {
            $p = load_content($type, $m[1]);
            return $p ? $p + ['_url' => $url] : null;
        }
    }
    $hubs = ['/services/' => 'services', '/commercial-claims/' => 'commercial'];
    if (isset($hubs[$url])) {
        $p = load_content($hubs[$url], 'index');
        return $p ? $p + ['_url' => $url] : null;
    }
    return null;
}

function word_count(string $html): int
{
    return str_word_count(strip_tags($html));
}

function read_minutes(string $html): int
{
    return max(1, (int) round(word_count($html) / 230));
}

function fmt_date(?string $ymd): string
{
    if (!$ymd) {
        return '';
    }
    $t = strtotime($ymd);
    return $t ? date('F j, Y', $t) : $ymd;
}

/** Add ids to <h2> tags and return [html, toc]. */
function add_heading_ids(string $html): array
{
    $toc = [];
    $used = [];
    $html = preg_replace_callback('#<h2([^>]*)>(.*?)</h2>#s', function ($m) use (&$toc, &$used) {
        $text = trim(html_entity_decode(strip_tags($m[2]), ENT_QUOTES, 'UTF-8'));
        if (preg_match('/\bid="([^"]+)"/', $m[1], $idm)) {
            $id = $idm[1];
        } else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-') ?: 'section';
            $base = $id;
            $i = 2;
            while (isset($used[$id])) {
                $id = $base . '-' . $i++;
            }
        }
        $used[$id] = true;
        $toc[] = [$id, $text];
        $attrs = strpos($m[1], 'id=') === false ? $m[1] . ' id="' . $id . '"' : $m[1];
        return "<h2$attrs>{$m[2]}</h2>";
    }, $html);
    return [$html, $toc];
}

function send_status(int $code): void
{
    http_response_code($code);
}

function redirect(string $to, int $code = 301): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

/**
 * Private storage. Hostinger's plain-PHP hosting ignores .htaccess, so files
 * inside the web root can be downloaded. Prefer a folder next to public_html;
 * fall back to storage/ inside the site with unguessable file names.
 */
function private_dir(): string
{
    static $dir = null;
    if ($dir !== null) {
        return $dir;
    }
    $outside = dirname(SITE_ROOT) . '/txpa-private';
    if ((is_dir($outside) || @mkdir($outside, 0700, true)) && is_writable($outside)) {
        return $dir = $outside;
    }
    return $dir = SITE_ROOT . '/storage';
}

/** Secret used to sign form tokens; kept in a .php file so a direct request prints nothing. */
function site_secret(): string
{
    static $secret = null;
    if ($secret) {
        return $secret;
    }
    $file = private_dir() . '/secret.php';
    if (!is_file($file)) {
        @file_put_contents($file, "<?php return '" . bin2hex(random_bytes(32)) . "';\n");
        @chmod($file, 0600);
    }
    $s = is_file($file) ? (include $file) : '';
    return $secret = (is_string($s) && $s !== '') ? $s : hash('sha256', __FILE__ . PRODUCTION_HOST);
}

/** Lead log path; the name includes part of the secret so it can't be guessed. */
function leads_file(): string
{
    return private_dir() . '/leads-' . substr(hash('sha256', site_secret()), 0, 20) . '.csv';
}

function form_token(): string
{
    $t = (string) time();
    return $t . '.' . hash_hmac('sha256', $t, site_secret());
}

function form_token_valid(string $token): bool
{
    [$t, $sig] = array_pad(explode('.', $token, 2), 2, '');
    if (!ctype_digit($t) || !hash_equals(hash_hmac('sha256', $t, site_secret()), $sig)) {
        return false;
    }
    $age = time() - (int) $t;
    return $age >= 3 && $age <= 86400; // humans take a few seconds; tokens expire in a day
}
