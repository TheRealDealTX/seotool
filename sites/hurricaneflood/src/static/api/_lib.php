<?php
// Shared helpers for hurricaneflood.com API endpoints.

function hf_json(array $data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Robots-Tag: noindex');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function hf_tmp_dir(): string
{
    $dir = sys_get_temp_dir() . '/hurricaneflood-tmp';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return $dir;
}

/** Small per-IP limiter: at most $max requests per $window seconds. */
function hf_rate_limit(string $bucket, int $max, int $window): void
{
    $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'unknown')[0]);
    $file = hf_tmp_dir() . '/rl-' . $bucket . '-' . sha1($ip);
    $now = time();
    $hits = is_file($file) ? array_filter(explode("\n", (string) file_get_contents($file))) : [];
    $hits = array_values(array_filter($hits, fn($t) => ($now - (int) $t) < $window));
    if (count($hits) >= $max) {
        hf_json(['ok' => false, 'error' => 'Too many requests. Please wait a few minutes or call us.'], 429);
    }
    $hits[] = $now;
    @file_put_contents($file, implode("\n", $hits), LOCK_EX);
}
