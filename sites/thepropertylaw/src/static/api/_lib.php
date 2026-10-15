<?php
// Helpers for the thepropertylaw.com lead endpoint.

function tpl_json(array $data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Robots-Tag: noindex');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function tpl_tmp(): string
{
    $dir = sys_get_temp_dir() . '/thepropertylaw-tmp';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    return $dir;
}

/** Per-IP sliding-window limiter: at most $max hits per $window seconds. */
function tpl_throttle(string $bucket, int $max, int $window): void
{
    $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'unknown')[0]);
    $file = tpl_tmp() . '/rl-' . $bucket . '-' . sha1($ip);
    $now = time();
    $hits = is_file($file) ? array_filter(explode("\n", (string) file_get_contents($file))) : [];
    $hits = array_values(array_filter($hits, fn($t) => ($now - (int) $t) < $window));
    if (count($hits) >= $max) {
        tpl_json(['ok' => false, 'error' => 'Too many requests. Please wait a few minutes or call us.'], 429);
    }
    $hits[] = $now;
    @file_put_contents($file, implode("\n", $hits), LOCK_EX);
}
