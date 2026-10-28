<?php
declare(strict_types=1);
// Shared helpers for the website checkers. Direct requests are denied by .htaccess.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === basename(__FILE__)) { http_response_code(404); exit; }

class CheckError extends RuntimeException {}

function validate_url(string $url): array {
    if (strlen($url) > 2048 || preg_match('/[\x00-\x20\x7f\\\\]/', $url)) throw new CheckError('The URL contains unsupported characters.', 400);
    $parts = parse_url($url);
    if (!$parts || !isset($parts['scheme'], $parts['host']) || !in_array(strtolower($parts['scheme']), ['https', 'http'], true)) throw new CheckError('Only HTTP and HTTPS URLs are supported.', 400);
    if (isset($parts['user']) || isset($parts['pass'])) throw new CheckError('URLs with credentials are not supported.', 400);
    $scheme = strtolower($parts['scheme']);
    $port = $parts['port'] ?? ($scheme === 'https' ? 443 : 80);
    if ($port !== ($scheme === 'https' ? 443 : 80)) throw new CheckError('Only standard HTTP and HTTPS ports are supported.', 400);
    $host = strtolower($parts['host']);
    if (strlen($host) > 253 || !preg_match('/^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/', $host)) throw new CheckError('Use a public domain name or a public IPv4 address. International domains must use punycode.', 400);
    foreach (['.localhost', '.local', '.internal', '.test', '.invalid', '.example', '.onion', '.lan', '.home.arpa'] as $suffix) {
        if (str_ends_with($host, $suffix)) throw new CheckError('Only public websites can be checked.', 400);
    }
    return ['host' => $host, 'port' => $port, 'scheme' => $scheme] + $parts;
}

function public_ipv4(string $ip): bool {
    if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) return false;
    $number = ip2long($ip);
    foreach ([['0.0.0.0',8], ['100.64.0.0',10], ['127.0.0.0',8], ['169.254.0.0',16], ['192.0.0.0',24], ['192.0.2.0',24], ['192.88.99.0',24], ['198.18.0.0',15], ['198.51.100.0',24], ['203.0.113.0',24], ['224.0.0.0',4], ['240.0.0.0',4]] as [$network, $bits]) {
        $mask = -1 << (32 - $bits);
        if (($number & $mask) === (ip2long($network) & $mask)) return false;
    }
    return true;
}

function public_address(string $host): string {
    $addresses = filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) ? [$host] : gethostbynamel($host);
    if (!$addresses) throw new CheckError('The hostname could not be resolved to a public IPv4 address.', 422);
    foreach ($addresses as $address) if (!public_ipv4($address)) throw new CheckError('This URL resolves to a private or reserved network address and cannot be checked.', 400);
    return $addresses[0];
}

function resolve_url(string $base, string $relative): string {
    $relative = trim($relative);
    if (preg_match('~^[a-z][a-z0-9+.-]*:~i', $relative)) return $relative;
    $p = parse_url($base);
    $origin = $p['scheme'] . '://' . $p['host'] . (isset($p['port']) ? ':' . $p['port'] : '');
    if (str_starts_with($relative, '//')) return $p['scheme'] . ':' . $relative;
    if ($relative === '') return preg_replace('/#.*$/', '', $base);
    if ($relative[0] === '#') return preg_replace('/#.*$/', '', $base) . $relative;
    if ($relative[0] === '?') return $origin . ($p['path'] ?? '/') . $relative;
    $suffix = ''; $path = $relative;
    if (preg_match('/[?#]/', $relative, $m, PREG_OFFSET_CAPTURE)) { $offset = $m[0][1]; $path = substr($relative, 0, $offset); $suffix = substr($relative, $offset); }
    if (!str_starts_with($path, '/')) $path = preg_replace('~/[^/]*$~', '/', $p['path'] ?? '/') . $path;
    $segments = [];
    foreach (explode('/', $path) as $segment) {
        if ($segment === '..') array_pop($segments);
        elseif ($segment !== '.') $segments[] = $segment;
    }
    $normalized = implode('/', $segments);
    if (!str_starts_with($normalized, '/')) $normalized = '/' . $normalized;
    return $origin . $normalized . $suffix;
}

/** File-based limiter with 64 fixed buckets so storage stays bounded. */
function rate_limit(string $name = 'check', int $max = 12, int $window = 120): void {
    $dir = sys_get_temp_dir() . '/jm-toolbox-' . substr(hash('sha256', __DIR__), 0, 16);
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) throw new CheckError('The server cannot create temporary rate-limit storage.', 503);
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $bucket = hexdec(substr(hash('sha256', $name . $ip), 0, 4)) % 64;
    $file = @fopen($dir . '/' . $name . '-' . $bucket, 'c+');
    if (!$file || !flock($file, LOCK_EX)) throw new CheckError('The request limiter is unavailable. Try again shortly.', 503);
    try {
        $data = json_decode(stream_get_contents($file), true) ?: [];
        $now = time(); $key = hash('sha256', $ip . ':' . intdiv($now, $window));
        $data = array_filter($data, static fn($entry) => is_array($entry) && ($entry['until'] ?? 0) > $now);
        if (count($data) >= 256 || ($data[$key]['count'] ?? 0) >= $max) {
            header('Retry-After: ' . $window);
            throw new CheckError('Too many requests. Please wait ' . ($window >= 120 ? intdiv($window, 60) . ' minutes' : $window . ' seconds') . ' and try again.', 429);
        }
        $data[$key] = ['count' => ($data[$key]['count'] ?? 0) + 1, 'until' => $now + $window];
        ftruncate($file, 0); rewind($file); fwrite($file, json_encode($data)); fflush($file);
    } finally { flock($file, LOCK_UN); fclose($file); }
}

class PublicFetcher {
    private int $count = 0;
    private float $deadline;
    public function __construct(private int $maxRequests = 14, int $seconds = 40) { $this->deadline = microtime(true) + $seconds; }
    public function get(string $url, int $maxBytes = 3145728): array {
        $chain = []; $started = microtime(true);
        for ($redirect = 0; $redirect <= 5; $redirect++) {
            if (++$this->count > $this->maxRequests || microtime(true) >= $this->deadline) throw new CheckError('The check reached its request or time limit.', 422);
            $url = preg_replace('/#.*$/', '', $url);
            $parts = validate_url($url); $address = public_address($parts['host']);
            $body = ''; $headers = []; $oversized = false;
            $ch = curl_init($url);
            curl_setopt_array($ch, [
                CURLOPT_RETURNTRANSFER => false,
                CURLOPT_FOLLOWLOCATION => false,
                CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
                CURLOPT_CONNECTTIMEOUT => 5,
                CURLOPT_TIMEOUT => max(1, min(12, (int)ceil($this->deadline - microtime(true)))),
                CURLOPT_SSL_VERIFYPEER => true,
                CURLOPT_SSL_VERIFYHOST => 2,
                CURLOPT_PROXY => '',
                CURLOPT_RESOLVE => [$parts['host'] . ':' . $parts['port'] . ':' . $address],
                CURLOPT_IPRESOLVE => CURL_IPRESOLVE_V4,
                CURLOPT_USERAGENT => 'Mozilla/5.0 (compatible; JMAutidaToolbox/2.0; +https://jmautida.com/tools)',
                CURLOPT_HTTPHEADER => ['Accept: text/html,application/xhtml+xml,application/json,image/*;q=0.8,*/*;q=0.5', 'Accept-Language: en-US,en;q=0.8'],
                CURLOPT_ENCODING => '',
                CURLOPT_WRITEFUNCTION => static function ($handle, string $chunk) use (&$body, &$oversized, $maxBytes): int {
                    if (strlen($body) + strlen($chunk) > $maxBytes) { $oversized = true; return 0; }
                    $body .= $chunk; return strlen($chunk);
                },
                CURLOPT_HEADERFUNCTION => static function ($handle, string $line) use (&$headers): int {
                    if (str_starts_with($line, 'HTTP/')) $headers = [];
                    elseif (str_contains($line, ':')) { [$k, $v] = explode(':', $line, 2); $headers[strtolower(trim($k))][] = trim($v); }
                    return strlen($line);
                },
            ]);
            $success = curl_exec($ch);
            $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
            $type = (string)curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
            curl_close($ch);
            if ($oversized) throw new CheckError('A resource exceeded the ' . round($maxBytes / 1048576, 1) . ' MB limit.', 422);
            if ($success === false) throw new CheckError('A resource could not be fetched securely within the time limit.', 422);
            $location = $headers['location'][0] ?? '';
            if (in_array($status, [301, 302, 303, 307, 308], true) && $location !== '') {
                if ($redirect === 5) throw new CheckError('The website redirected too many times.', 422);
                $chain[] = ['url' => $url, 'status' => $status];
                $url = resolve_url($url, $location); continue;
            }
            return ['url' => $url, 'status' => $status, 'type' => $type, 'body' => $body, 'headers' => $headers, 'redirects' => $chain, 'ms' => (int)round((microtime(true) - $started) * 1000)];
        }
        throw new CheckError('The website could not be checked.', 422);
    }
}

function html_document(string $html): DOMDocument {
    $doc = new DOMDocument();
    $previous = libxml_use_internal_errors(true);
    $doc->loadHTML('<?xml encoding="UTF-8">' . $html, LIBXML_NONET | LIBXML_NOERROR | LIBXML_NOWARNING | LIBXML_COMPACT);
    libxml_clear_errors(); libxml_use_internal_errors($previous);
    return $doc;
}
function clean_text(?string $value, int $max = 400): string {
    $value = trim(preg_replace('/\s+/u', ' ', (string)$value) ?? '');
    if (!function_exists('mb_strlen')) return strlen($value) > $max ? substr($value, 0, $max) . '…' : $value;
    return mb_strlen($value) > $max ? mb_substr($value, 0, $max) . '…' : $value;
}
function result_check(string $label, string $state, string $detail): array { return compact('label', 'state', 'detail'); }
function meta_values(DOMDocument $doc): array {
    $values = [];
    foreach ($doc->getElementsByTagName('meta') as $tag) {
        $name = strtolower(trim($tag->getAttribute('name') ?: $tag->getAttribute('property')));
        if ($name !== '') $values[$name][] = clean_text($tag->getAttribute('content'), 600);
        $equiv = strtolower(trim($tag->getAttribute('http-equiv')));
        if ($equiv !== '') $values['http-equiv:' . $equiv][] = clean_text($tag->getAttribute('content'), 300);
    }
    return $values;
}
function links_with_rel(DOMDocument $doc, string $rel): array {
    $items = [];
    foreach ($doc->getElementsByTagName('link') as $link) {
        $rels = preg_split('/\s+/', strtolower(trim($link->getAttribute('rel'))));
        if (in_array($rel, $rels, true) && trim($link->getAttribute('href')) !== '') $items[] = $link;
    }
    return $items;
}
function document_base(DOMDocument $doc, string $url): string {
    $base = $doc->getElementsByTagName('base')->item(0);
    return $base && $base->hasAttribute('href') ? resolve_url($url, $base->getAttribute('href')) : $url;
}
function first_values(array $values, array $keys): array {
    $out = [];
    foreach ($keys as $k) $out[$k] = $values[$k][0] ?? '';
    return $out;
}

/** Collect @type values from decoded JSON-LD, including nested @graph entries. */
function schema_types($node, array &$types, int $depth = 0): void {
    if ($depth > 6 || !is_array($node)) return;
    if (isset($node['@type'])) foreach ((array)$node['@type'] as $t) if (is_string($t)) $types[$t] = ($types[$t] ?? 0) + 1;
    foreach ($node as $key => $child) if (is_array($child) && ($key === '@graph' || is_int($key) || $depth < 2)) schema_types($child, $types, $depth + 1);
}

/** Minimal robots.txt evaluation for the "*" group: longest matching rule wins. */
function robots_allows(string $robots, string $path): array {
    $groups = []; $current = null; $sitemaps = []; $lastWasAgent = false;
    foreach (preg_split('/\r?\n/', $robots) as $line) {
        $line = trim(preg_replace('/#.*$/', '', $line));
        if ($line === '' || !str_contains($line, ':')) continue;
        [$k, $v] = array_map('trim', explode(':', $line, 2)); $k = strtolower($k);
        if ($k === 'sitemap') { $sitemaps[] = $v; continue; }
        if ($k === 'user-agent') {
            if (!$lastWasAgent) { $groups[] = ['agents' => [], 'rules' => []]; $current = count($groups) - 1; }
            $groups[$current]['agents'][] = strtolower($v); $lastWasAgent = true; continue;
        }
        $lastWasAgent = false;
        if ($current !== null && in_array($k, ['allow', 'disallow'], true)) $groups[$current]['rules'][] = [$k, $v];
    }
    $rules = [];
    foreach ($groups as $g) if (in_array('googlebot', $g['agents'], true)) $rules = array_merge($rules, $g['rules']);
    if (!$rules) foreach ($groups as $g) if (in_array('*', $g['agents'], true)) $rules = array_merge($rules, $g['rules']);
    $best = null; $bestLen = -1;
    foreach ($rules as [$type, $pattern]) {
        if ($pattern === '') continue;
        $regex = '~^' . str_replace(['\*', '\$'], ['.*', '$'], preg_quote($pattern, '~')) . '~';
        if (preg_match($regex, $path) && strlen($pattern) > $bestLen) { $best = [$type, $pattern]; $bestLen = strlen($pattern); }
        elseif (preg_match($regex, $path) && strlen($pattern) === $bestLen && $type === 'allow') $best = [$type, $pattern];
    }
    return ['allowed' => !$best || $best[0] === 'allow', 'rule' => $best ? ucfirst($best[0]) . ': ' . $best[1] : '', 'sitemaps' => array_slice($sitemaps, 0, 5)];
}

function inspect_seo(DOMDocument $doc, array $page, PublicFetcher $fetcher): array {
    $url = $page['url']; $base = document_base($doc, $url); $host = strtolower(parse_url($url, PHP_URL_HOST) ?? '');
    $values = meta_values($doc);
    $titles = $doc->getElementsByTagName('title');
    $htmlEl = $doc->getElementsByTagName('html')->item(0);
    $canon = links_with_rel($doc, 'canonical');
    $canonical = $canon ? resolve_url($base, $canon[0]->getAttribute('href')) : '';
    $charset = '';
    foreach ($doc->getElementsByTagName('meta') as $m) if ($m->hasAttribute('charset')) { $charset = $m->getAttribute('charset'); break; }
    if ($charset === '' && preg_match('/charset=([\w-]+)/i', $values['http-equiv:content-type'][0] ?? $page['type'], $mm)) $charset = $mm[1];

    $hreflang = [];
    foreach (links_with_rel($doc, 'alternate') as $l) if ($l->getAttribute('hreflang') !== '' && count($hreflang) < 20) $hreflang[] = ['lang' => $l->getAttribute('hreflang'), 'href' => resolve_url($base, $l->getAttribute('href'))];

    $headings = ['h1' => 0, 'h2' => 0, 'h3' => 0, 'h4' => 0, 'h5' => 0, 'h6' => 0]; $outline = []; $h1 = [];
    $xpath = new DOMXPath($doc);
    foreach ($xpath->query('//h1|//h2|//h3|//h4|//h5|//h6') as $h) {
        $tag = strtolower($h->nodeName); $headings[$tag]++;
        $text = clean_text($h->textContent, 140);
        if ($tag === 'h1' && count($h1) < 5) $h1[] = $text;
        if (count($outline) < 60) $outline[] = [(int)$tag[1], $text];
    }

    $images = 0; $noAlt = 0; $emptyAlt = 0; $missingSamples = [];
    foreach ($doc->getElementsByTagName('img') as $img) {
        $images++;
        if (!$img->hasAttribute('alt')) { $noAlt++; if (count($missingSamples) < 8) $missingSamples[] = resolve_url($base, $img->getAttribute('src') ?: $img->getAttribute('data-src')); }
        elseif (trim($img->getAttribute('alt')) === '') $emptyAlt++;
    }

    $internal = 0; $external = 0; $nofollow = 0; $empty = 0;
    foreach ($doc->getElementsByTagName('a') as $a) {
        $href = trim($a->getAttribute('href'));
        if ($href === '' || $href[0] === '#' || preg_match('~^(javascript|mailto|tel):~i', $href)) { if ($href === '') $empty++; continue; }
        $linkHost = strtolower(parse_url(resolve_url($base, $href), PHP_URL_HOST) ?? '');
        if ($linkHost === '' || $linkHost === $host || preg_replace('/^www\./', '', $linkHost) === preg_replace('/^www\./', '', $host)) $internal++; else $external++;
        if (preg_match('/\bnofollow\b/i', $a->getAttribute('rel'))) $nofollow++;
    }

    $types = []; $ldErrors = 0; $ldBlocks = 0;
    foreach ($xpath->query('//script[@type="application/ld+json"]') as $s) {
        $ldBlocks++;
        $json = json_decode(trim($s->textContent), true);
        if ($json === null) { $ldErrors++; continue; }
        schema_types($json, $types);
    }
    $microdata = $xpath->query('//*[@itemtype]')->length;

    $words = 0; $bodyText = '';
    $body = $doc->getElementsByTagName('body')->item(0);
    if ($body) {
        $clone = $body->cloneNode(true);
        foreach (['script', 'style', 'noscript', 'template', 'svg', 'iframe'] as $tag) {
            $nodes = []; foreach ($clone->getElementsByTagName($tag) as $n) $nodes[] = $n;
            foreach ($nodes as $n) $n->parentNode?->removeChild($n);
        }
        $bodyText = preg_replace('/\s+/u', ' ', $clone->textContent) ?? '';
        $words = preg_match_all('/[\p{L}\p{N}]+(?:[\'’-][\p{L}\p{N}]+)*/u', $bodyText) ?: 0;
    }

    $robotsTxt = ['checked' => false];
    try {
        $origin = parse_url($url, PHP_URL_SCHEME) . '://' . parse_url($url, PHP_URL_HOST);
        $r = $fetcher->get($origin . '/robots.txt', 524288);
        $robotsTxt = ['checked' => true, 'status' => $r['status'], 'url' => $r['url']];
        if ($r['status'] >= 200 && $r['status'] < 300 && !preg_match('~text/html~i', $r['type'])) {
            $path = (parse_url($url, PHP_URL_PATH) ?: '/') . (($q = parse_url($url, PHP_URL_QUERY)) ? '?' . $q : '');
            $robotsTxt += robots_allows($r['body'], $path) + ['found' => true];
        } else $robotsTxt['found'] = false;
    } catch (CheckError $e) { $robotsTxt = ['checked' => true, 'found' => false, 'error' => $e->getMessage()]; }

    $icons = links_with_rel($doc, 'icon');
    return [
        'title' => clean_text($titles->item(0)?->textContent, 300), 'titleCount' => $titles->length,
        'description' => $values['description'][0] ?? '', 'descriptionCount' => count($values['description'] ?? []),
        'canonical' => $canonical, 'canonicalCount' => count($canon),
        'robots' => implode(', ', array_merge($values['robots'] ?? [], $values['googlebot'] ?? [])),
        'xRobots' => implode(', ', $page['headers']['x-robots-tag'] ?? []),
        'viewport' => $values['viewport'][0] ?? '', 'charset' => $charset, 'lang' => $htmlEl?->getAttribute('lang') ?? '',
        'keywords' => $values['keywords'][0] ?? '',
        'og' => first_values($values, ['og:title', 'og:description', 'og:image', 'og:image:alt', 'og:url', 'og:type', 'og:site_name', 'og:locale']),
        'twitter' => first_values($values, ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:site']),
        'themeColor' => $values['theme-color'][0] ?? '',
        'favicon' => $icons ? resolve_url($base, $icons[0]->getAttribute('href')) : '',
        'hreflang' => $hreflang,
        'headings' => $headings, 'h1' => $h1, 'outline' => $outline,
        'images' => ['total' => $images, 'missingAlt' => $noAlt, 'emptyAlt' => $emptyAlt, 'missingSamples' => $missingSamples],
        'links' => ['internal' => $internal, 'external' => $external, 'nofollow' => $nofollow, 'empty' => $empty],
        'schema' => ['types' => $types, 'blocks' => $ldBlocks, 'errors' => $ldErrors, 'microdata' => $microdata],
        'words' => $words, 'excerpt' => clean_text($bodyText, 300),
        'robotsTxt' => $robotsTxt,
        'https' => str_starts_with($url, 'https://'), 'bytes' => strlen($page['body']), 'ms' => $page['ms'],
        'redirects' => $page['redirects'], 'server' => clean_text($page['headers']['server'][0] ?? '', 60),
        'compressed' => isset($page['headers']['content-encoding']),
    ];
}

function image_info(array $response): array {
    $type = strtolower($response['type']);
    $body = $response['body'];
    if (str_contains($type, 'svg') || preg_match('/^\s*(<\?xml[^>]*>\s*)?<svg/i', substr($body, 0, 512))) return ['width' => null, 'height' => null, 'format' => 'SVG', 'vector' => true];
    $info = @getimagesizefromstring($body);
    if (!$info) return ['width' => null, 'height' => null, 'format' => '', 'vector' => false];
    $formats = [IMAGETYPE_PNG => 'PNG', IMAGETYPE_ICO => 'ICO', IMAGETYPE_JPEG => 'JPEG', IMAGETYPE_GIF => 'GIF', IMAGETYPE_WEBP => 'WebP', IMAGETYPE_BMP => 'BMP'];
    return ['width' => $info[0] ?: null, 'height' => $info[1] ?: null, 'format' => $formats[$info[2]] ?? image_type_to_extension($info[2], false), 'vector' => false];
}

function inspect_icons(DOMDocument $doc, string $url, PublicFetcher $fetcher): array {
    $checks = []; $found = []; $base = document_base($doc, $url);
    $probe = static function (string $label, string $resource, string $declared = '') use ($fetcher, &$found): array {
        try {
            $response = $fetcher->get($resource, 1048576);
            $ok = $response['status'] >= 200 && $response['status'] < 300;
            $isImage = preg_match('~^image/~i', $response['type']) || ($ok && image_info($response)['format'] !== '');
            $info = $ok ? image_info($response) : ['width' => null, 'height' => null, 'format' => '', 'vector' => false];
            $found[] = ['label' => $label, 'url' => $response['url'], 'status' => $response['status'], 'type' => $response['type'], 'declared' => $declared, 'ok' => $ok && $isImage] + $info;
            $dims = $info['vector'] ? 'scalable SVG' : ($info['width'] ? $info['width'] . '×' . $info['height'] . ' px ' . $info['format'] : 'unknown size');
            return result_check($label, $ok && $isImage ? 'PASS' : 'NOTE', $response['url'] . ' — HTTP ' . $response['status'] . ', ' . ($ok && $isImage ? $dims : ($response['type'] ?: 'unknown content type') . ($ok ? '. Expected an image.' : '')));
        } catch (CheckError $error) {
            $found[] = ['label' => $label, 'url' => $resource, 'status' => 0, 'type' => '', 'declared' => $declared, 'ok' => false, 'width' => null, 'height' => null, 'format' => '', 'vector' => false];
            return result_check($label, 'NOTE', $resource . ' — ' . $error->getMessage());
        }
    };
    $icons = links_with_rel($doc, 'icon');
    $apple = array_merge(links_with_rel($doc, 'apple-touch-icon'), links_with_rel($doc, 'apple-touch-icon-precomposed'));
    if (!$icons) $checks[] = result_check('Declared favicon', 'MISSING', 'No <link rel="icon"> found. Browsers will fall back to /favicon.ico.');
    foreach (array_slice($icons, 0, 4) as $i => $icon) $checks[] = $probe('Favicon ' . ($i + 1) . ($icon->getAttribute('sizes') ? ' · ' . $icon->getAttribute('sizes') : ''), resolve_url($base, $icon->getAttribute('href')), $icon->getAttribute('sizes'));
    if (count($icons) > 4) $checks[] = result_check('Additional favicons', 'NOTE', (count($icons) - 4) . ' more declarations were not fetched.');
    $checks[] = $probe('/favicon.ico fallback', resolve_url($url, '/favicon.ico'));
    if ($apple) $checks[] = $probe('Apple touch icon', resolve_url($base, $apple[0]->getAttribute('href')), $apple[0]->getAttribute('sizes'));
    else {
        $c = $probe('Apple touch icon (undeclared)', resolve_url($url, '/apple-touch-icon.png'));
        $checks[] = $c['state'] === 'PASS' ? result_check('Apple touch icon', 'NOTE', 'Found at /apple-touch-icon.png but not declared. Add <link rel="apple-touch-icon" href="/apple-touch-icon.png">.') : result_check('Apple touch icon', 'MISSING', 'Add a 180×180 PNG with <link rel="apple-touch-icon"> for iOS home screens.');
    }
    $manifestInfo = null;
    $manifests = links_with_rel($doc, 'manifest');
    if (!$manifests) $checks[] = result_check('Web app manifest', 'MISSING', 'No rel="manifest" link. Optional, but it provides Android home-screen icons.');
    else {
        try {
            $response = $fetcher->get(resolve_url($base, $manifests[0]->getAttribute('href')), 262144);
            $manifest = json_decode($response['body'], true);
            if ($response['status'] < 200 || $response['status'] >= 300 || !is_array($manifest)) throw new CheckError('The manifest did not return valid JSON.', 422);
            $checks[] = result_check('Web app manifest', 'PASS', $response['url'] . ' — valid JSON.');
            $manifestIcons = is_array($manifest['icons'] ?? null) ? $manifest['icons'] : [];
            $manifestInfo = ['url' => $response['url'], 'name' => clean_text((string)($manifest['name'] ?? ''), 80), 'short_name' => clean_text((string)($manifest['short_name'] ?? ''), 40), 'theme_color' => clean_text((string)($manifest['theme_color'] ?? ''), 20), 'background_color' => clean_text((string)($manifest['background_color'] ?? ''), 20), 'display' => clean_text((string)($manifest['display'] ?? ''), 20), 'icons' => count($manifestIcons)];
            if (!$manifestIcons) $checks[] = result_check('Manifest icons', 'MISSING', 'The manifest has no icons array.');
            $sizes = [];
            foreach ($manifestIcons as $icon) if (is_array($icon) && is_string($icon['sizes'] ?? null)) $sizes = array_merge($sizes, preg_split('/\s+/', strtolower($icon['sizes'])));
            foreach (array_slice($manifestIcons, 0, 3) as $i => $icon) {
                if (!is_array($icon) || !is_string($icon['src'] ?? null) || !$icon['src']) { $checks[] = result_check('Manifest icon ' . ($i + 1), 'NOTE', 'Missing or invalid src.'); continue; }
                $checks[] = $probe('Manifest icon ' . ($i + 1) . (is_string($icon['sizes'] ?? null) ? ' · ' . $icon['sizes'] : ''), resolve_url($response['url'], $icon['src']), (string)($icon['sizes'] ?? ''));
            }
            $checks[] = result_check('192 & 512 px icons', in_array('192x192', $sizes, true) && in_array('512x512', $sizes, true) ? 'PASS' : 'NOTE', 'Android and install prompts expect 192×192 and 512×512 icons. Declared: ' . ($sizes ? implode(', ', array_unique($sizes)) : 'none') . '.');
        } catch (CheckError $error) { $checks[] = result_check('Web app manifest', 'NOTE', $error->getMessage()); }
    }
    return ['checks' => $checks, 'icons' => $found, 'manifest' => $manifestInfo];
}
