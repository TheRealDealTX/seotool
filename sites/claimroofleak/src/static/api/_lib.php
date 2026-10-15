<?php
// Helpers for the claimroofleak.com form endpoint.

function crl_reply(array $data, int $code = 200): void
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Robots-Tag: noindex');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function crl_client_ip(): string
{
    $raw = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
    return trim(explode(',', $raw)[0]);
}

/** Per-IP throttle: at most $max posts per $window seconds. */
function crl_throttle(string $name, int $max, int $window): void
{
    $dir = sys_get_temp_dir() . '/claimroofleak-rl';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    $file = $dir . '/' . $name . '-' . sha1(crl_client_ip());
    $now = time();
    $hits = is_file($file) ? array_filter(array_map('intval', explode(',', (string) file_get_contents($file)))) : [];
    $hits = array_values(array_filter($hits, fn($t) => $now - $t < $window));
    if (count($hits) >= $max) {
        crl_reply(['ok' => false, 'error' => 'Too many requests. Please wait a few minutes or call (407) 433-4131.'], 429);
    }
    $hits[] = $now;
    @file_put_contents($file, implode(',', $hits), LOCK_EX);
}

/** Single-line, length-limited POST field. */
function crl_field(string $key, int $max): string
{
    $v = (string) ($_POST[$key] ?? '');
    $v = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v);
    return trim(mb_substr($v, 0, $max));
}
