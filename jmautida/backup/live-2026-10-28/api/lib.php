<?php
declare(strict_types=1);
// Direct requests reveal no source or diagnostics.
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
    foreach (['.localhost', '.local', '.internal', '.test', '.invalid', '.example', '.onion'] as $suffix) {
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
function rate_limit(): void {
    $dir = sys_get_temp_dir() . '/jm-toolbox-' . substr(hash('sha256', __DIR__), 0, 16);
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) throw new CheckError('The server cannot create temporary rate-limit storage.', 503);
    // Fixed 64 buckets bound storage, even under many different IP addresses.
    $bucket = hexdec(substr(hash('sha256', $_SERVER['REMOTE_ADDR'] ?? 'unknown'), 0, 4)) % 64;
    $file = @fopen($dir . '/' . $bucket, 'c+');
    if (!$file || !flock($file, LOCK_EX)) throw new CheckError('The request limiter is unavailable. Try again shortly.', 503);
    try {
        $data = json_decode(stream_get_contents($file), true) ?: [];
        $now = time(); $key = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . ':' . intdiv($now, 120));
        $data = array_filter($data, static fn($entry) => is_array($entry) && ($entry['until'] ?? 0) > $now);
        if (count($data) >= 128 || ($data[$key]['count'] ?? 0) >= 12) { header('Retry-After: 120'); throw new CheckError('Too many checks. Please wait two minutes and try again.', 429); }
        $data[$key] = ['count' => ($data[$key]['count'] ?? 0) + 1, 'until' => $now + 120];
        ftruncate($file, 0); rewind($file); fwrite($file, json_encode($data)); fflush($file);
    } finally { flock($file, LOCK_UN); fclose($file); }
}
class PublicFetcher {
    private int $count = 0;
    private float $deadline;
    public function __construct() { $this->deadline = microtime(true) + 40; }
    public function get(string $url): array {
        for ($redirect = 0; $redirect <= 3; $redirect++) {
            if (++$this->count > 12 || microtime(true) >= $this->deadline) throw new CheckError('The check reached its request or time limit.', 422);
            $url = preg_replace('/#.*$/', '', $url);
            $parts = validate_url($url); $address = public_address($parts['host']);
            $body = ''; $location = ''; $oversized = false;
            $ch = curl_init($url);
            curl_setopt_array($ch, [
                CURLOPT_RETURNTRANSFER => false,
                CURLOPT_FOLLOWLOCATION => false,
                CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
                CURLOPT_CONNECTTIMEOUT => 4,
                CURLOPT_TIMEOUT => max(1, min(8, (int)ceil($this->deadline - microtime(true)))),
                CURLOPT_SSL_VERIFYPEER => true,
                CURLOPT_SSL_VERIFYHOST => 2,
                CURLOPT_PROXY => '',
                CURLOPT_RESOLVE => [$parts['host'] . ':' . $parts['port'] . ':' . $address],
                CURLOPT_IPRESOLVE => CURL_IPRESOLVE_V4,
                CURLOPT_USERAGENT => 'JMAutida-Toolbox/1.0 (public website metadata check)',
                CURLOPT_HTTPHEADER => ['Accept: text/html,application/xhtml+xml,application/json,image/*;q=0.8,*/*;q=0.5'],
                CURLOPT_ENCODING => '',
                CURLOPT_WRITEFUNCTION => static function ($handle, string $chunk) use (&$body, &$oversized): int {
                    if (strlen($body) + strlen($chunk) > 1048576) { $oversized = true; return 0; }
                    $body .= $chunk; return strlen($chunk);
                },
                CURLOPT_HEADERFUNCTION => static function ($handle, string $line) use (&$location): int {
                    if (stripos($line, 'Location:') === 0) $location = trim(substr($line, 9));
                    return strlen($line);
                },
            ]);
            $success = curl_exec($ch);
            $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
            $type = (string)curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
            curl_close($ch);
            if ($oversized) throw new CheckError('A resource exceeded the 1 MB limit.', 422);
            if ($success === false) throw new CheckError('A resource could not be fetched securely within the time limit.', 422);
            if (in_array($status, [301,302,303,307,308], true) && $location !== '') {
                if ($redirect === 3) throw new CheckError('The website redirected too many times.', 422);
                $url = resolve_url($url, $location); continue;
            }
            return ['url' => $url, 'status' => $status, 'type' => $type, 'body' => $body];
        }
        throw new CheckError('The website could not be checked.', 422);
    }
}
function html_document(string $html): DOMDocument {
    $doc = new DOMDocument();
    $previous = libxml_use_internal_errors(true);
    $doc->loadHTML('<?xml encoding="UTF-8">' . $html, LIBXML_NONET | LIBXML_NOERROR | LIBXML_NOWARNING);
    libxml_clear_errors(); libxml_use_internal_errors($previous);
    return $doc;
}
function text_length(string $value): int { return preg_match_all('/./us', $value) ?: strlen($value); }
function result_check(string $label, string $state, string $detail): array { return compact('label', 'state', 'detail'); }
function meta_values(DOMDocument $doc): array {
    $values = [];
    foreach ($doc->getElementsByTagName('meta') as $tag) {
        $name = strtolower(trim($tag->getAttribute('name') ?: $tag->getAttribute('property')));
        if ($name !== '') $values[$name][] = trim($tag->getAttribute('content'));
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
function inspect_meta(DOMDocument $doc, string $url): array {
    $values = meta_values($doc); $checks = [];
    $title = trim($doc->getElementsByTagName('title')->item(0)?->textContent ?? '');
    $description = $values['description'][0] ?? '';
    foreach ([['Page title', $title, 30, 60], ['Meta description', $description, 70, 160]] as [$label,$value,$min,$max]) {
        $len = text_length($value);
        $checks[] = result_check($label, !$len ? 'MISSING' : (($len < $min || $len > $max) ? 'NOTE' : 'PASS'), $len ? "$len characters. $value" . (($len < $min || $len > $max) ? " — Suggested range: $min–$max characters; this is a guideline." : '') : 'No non-empty value found.');
    }
    $titleCount = $doc->getElementsByTagName('title')->length;
    if ($titleCount > 1) $checks[] = result_check('Duplicate titles', 'NOTE', "$titleCount title elements found. Keep one descriptive page title.");
    foreach ($values as $name => $entries) if (count($entries) > 1 && in_array($name, ['description','robots','og:title','og:description','og:image','twitter:card'], true)) $checks[] = result_check('Duplicate ' . $name, 'NOTE', count($entries) . ' declarations found. Conflicting values can cause inconsistent results.');
    $canonical = links_with_rel($doc, 'canonical');
    if ($canonical) {
        $resolved = resolve_url(document_base($doc, $url), $canonical[0]->getAttribute('href'));
        try { validate_url($resolved); $state = count($canonical) > 1 ? 'NOTE' : 'PASS'; } catch (CheckError $error) { $state = 'NOTE'; }
        $checks[] = result_check('Canonical URL', $state, $resolved . (count($canonical) > 1 ? ' — Multiple canonicals found.' : ' — Declaration only; target not fetched.'));
    } else $checks[] = result_check('Canonical URL', 'MISSING', 'No canonical link declared.');
    foreach (['viewport'=>'Viewport', 'og:title'=>'Open Graph title', 'og:description'=>'Open Graph description', 'og:image'=>'Open Graph image', 'og:url'=>'Open Graph URL', 'og:type'=>'Open Graph type', 'twitter:card'=>'Twitter card'] as $key=>$label) {
        $value = $values[$key][0] ?? '';
        $state = $value === '' ? 'MISSING' : 'PASS';
        if ($key === 'twitter:card' && $value !== '' && !in_array($value,['summary','summary_large_image','app','player'],true)) $state = 'NOTE';
        if (in_array($key,['og:image','og:url'],true) && $value !== '') {
            try { validate_url($value); } catch (CheckError $error) { $state='NOTE'; $value .= ' — Use an absolute HTTP(S) URL.'; }
        }
        $checks[] = result_check($label, $state, $value ?: 'Not declared in the server-rendered HTML.');
    }
    $robots = implode(', ', $values['robots'] ?? []);
    $checks[] = result_check('Robots directive', preg_match('/\b(noindex|none)\b/i',$robots) ? 'NOTE' : 'PASS', $robots ?: 'No HTML robots restriction declared. HTTP headers and robots.txt are not checked.');
    return ['title'=>$title, 'description'=>$description, 'checks'=>$checks];
}
function inspect_icons(DOMDocument $doc, string $url, PublicFetcher $fetcher): array {
    $checks = []; $base = document_base($doc, $url);
    $icons = links_with_rel($doc, 'icon');
    $apple = array_merge(links_with_rel($doc, 'apple-touch-icon'), links_with_rel($doc, 'apple-touch-icon-precomposed'));
    $probe = static function (string $label, string $resource) use ($fetcher): array {
        try {
            $response = $fetcher->get($resource);
            $ok = $response['status'] >= 200 && $response['status'] < 300;
            $image = preg_match('~^image/~i', $response['type']);
            return result_check($label, $ok && $image ? 'PASS' : 'NOTE', $response['url'] . ' — HTTP ' . $response['status'] . ', ' . ($response['type'] ?: 'unknown content type') . ($ok && !$image ? '. Expected an image content type.' : ''));
        } catch (CheckError $error) { return result_check($label, 'NOTE', $resource . ' — ' . $error->getMessage()); }
    };
    if (!$icons) $checks[] = result_check('Declared favicon', 'MISSING', 'No link with rel="icon" found.');
    foreach (array_slice($icons, 0, 3) as $i=>$icon) $checks[] = $probe('Favicon ' . ($i+1) . ($icon->getAttribute('sizes') ? ' · ' . $icon->getAttribute('sizes') : ''), resolve_url($base, $icon->getAttribute('href')));
    if (count($icons)>3) $checks[] = result_check('Additional favicons', 'NOTE', (count($icons)-3) . ' additional declarations were not fetched.');
    $checks[] = $probe('Conventional /favicon.ico', resolve_url($url, '/favicon.ico'));
    if ($apple) $checks[] = $probe('Apple touch icon', resolve_url($base, $apple[0]->getAttribute('href')));
    else $checks[] = result_check('Apple touch icon', 'MISSING', 'Add a rel="apple-touch-icon" declaration for iOS home-screen use.');
    $manifests = links_with_rel($doc, 'manifest');
    if (!$manifests) $checks[] = result_check('Web app manifest', 'MISSING', 'No rel="manifest" declaration. Optional for a standard website.');
    else {
        try {
            $response = $fetcher->get(resolve_url($base, $manifests[0]->getAttribute('href')));
            $manifest = json_decode($response['body'], true);
            if ($response['status'] < 200 || $response['status'] >= 300 || !is_array($manifest) || !str_starts_with(ltrim($response['body']),'{')) throw new CheckError('The manifest did not return a successful JSON object.', 422);
            $checks[] = result_check('Web app manifest', 'PASS', $response['url'] . ' — Valid JSON object.');
            $manifestIcons = is_array($manifest['icons'] ?? null) ? $manifest['icons'] : [];
            if (!$manifestIcons) $checks[] = result_check('Manifest icons', 'MISSING', 'No icons array with entries found.');
            $sizes = [];
            foreach (array_slice($manifestIcons,0,3) as $i=>$icon) {
                if (!is_array($icon) || !is_string($icon['src'] ?? null) || !$icon['src']) { $checks[] = result_check('Manifest icon '.($i+1), 'NOTE', 'Missing or invalid src value.'); continue; }
                if (is_string($icon['sizes'] ?? null)) $sizes = array_merge($sizes, preg_split('/\s+/', $icon['sizes']));
                $checks[] = $probe('Manifest icon '.($i+1), resolve_url($response['url'],$icon['src']));
            }
            $checks[] = result_check('Installable icon declarations', in_array('192x192',$sizes,true) && in_array('512x512',$sizes,true) ? 'PASS' : 'NOTE', 'Recommended declarations: 192x192 and 512x512. Inspected the first three manifest icons; dimensions are not decoded.');
        } catch (CheckError $error) { $checks[] = result_check('Web app manifest', 'NOTE', $error->getMessage()); }
    }
    return ['checks'=>$checks];
}
