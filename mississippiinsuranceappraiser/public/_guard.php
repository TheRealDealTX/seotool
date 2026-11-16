<?php
// Mississippi Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'mississippiinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$mia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
$mia_path  = strtok($mia_uri, '?');
$mia_qs    = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
// /dir/index.php (and /index.php) are duplicate URLs of /dir/.
$mia_clean = preg_match('#^(.*/)index\.php$#', $mia_path, $mia_m) ? $mia_m[1] : null;
// 301 www. and plain http to https://mississippiinsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . ($mia_clean ?? $mia_path) . $mia_qs, true, 301);
    exit;
}
if ($mia_clean !== null) {
    header('Location: ' . $mia_clean . $mia_qs, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
