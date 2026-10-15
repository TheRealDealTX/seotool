<?php
// Shared helpers for the Pensacola Hurricane JSON endpoints.

function ph_json($data, int $status = 200, int $maxAge = 0): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Robots-Tag: noindex');
    header($maxAge > 0 ? "Cache-Control: public, max-age=$maxAge" : 'Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function ph_cache_dir(): string
{
    $dir = sys_get_temp_dir() . '/pensacolahurricane-cache';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return $dir;
}

/** GET a URL with a short timeout; returns the body or null. */
function ph_fetch(string $url, int $timeout = 12): ?string
{
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_CONNECTTIMEOUT => 6,
        CURLOPT_TIMEOUT => $timeout,
        CURLOPT_USERAGENT => 'PensacolaHurricane.com (storm information site)',
        CURLOPT_HTTPHEADER => ['Accept: application/json, application/xml;q=0.9, */*;q=0.5'],
    ]);
    $body = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return ($body !== false && $code >= 200 && $code < 300) ? $body : null;
}

/** Fetch through a file cache. Serves a stale copy if the upstream is down. */
function ph_cached_fetch(string $url, int $ttl): ?string
{
    $file = ph_cache_dir() . '/' . sha1($url);
    if (is_file($file) && (time() - filemtime($file)) < $ttl) {
        return file_get_contents($file);
    }
    $body = ph_fetch($url);
    if ($body !== null) {
        @file_put_contents($file, $body, LOCK_EX);
        return $body;
    }
    return is_file($file) ? file_get_contents($file) : null;
}

/** Very small per-IP rate limiter (requests per window). */
function ph_rate_limit(string $bucket, int $max, int $window): void
{
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $ip = trim(explode(',', $ip)[0]);
    $file = ph_cache_dir() . '/rl-' . $bucket . '-' . sha1($ip);
    $hits = is_file($file) ? array_filter(explode("\n", (string) file_get_contents($file))) : [];
    $now = time();
    $hits = array_values(array_filter($hits, fn($t) => ($now - (int) $t) < $window));
    if (count($hits) >= $max) {
        ph_json(['error' => 'Too many requests. Please wait a minute and try again.'], 429);
    }
    $hits[] = $now;
    @file_put_contents($file, implode("\n", $hits), LOCK_EX);
}
