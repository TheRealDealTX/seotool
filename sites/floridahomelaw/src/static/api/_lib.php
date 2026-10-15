<?php
// Helpers for the Florida Home Law form endpoint.

function fhl_json(array $data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Robots-Tag: noindex');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function fhl_tmp(): string
{
    $dir = sys_get_temp_dir() . '/floridahomelaw-rl';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return $dir;
}

/** Simple per-IP limiter: at most $max hits per $window seconds. */
function fhl_throttle(string $bucket, int $max, int $window): void
{
    $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'x')[0]);
    $file = fhl_tmp() . '/' . $bucket . '-' . sha1($ip);
    $now = time();
    $hits = is_file($file) ? array_filter(explode("\n", (string) file_get_contents($file))) : [];
    $hits = array_values(array_filter($hits, fn($t) => ($now - (int) $t) < $window));
    if (count($hits) >= $max) {
        fhl_json(['ok' => false, 'error' => 'Too many requests. Please wait a few minutes or call (407) 433-4131.'], 429);
    }
    $hits[] = $now;
    @file_put_contents($file, implode("\n", $hits), LOCK_EX);
}
