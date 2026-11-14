<?php
// New Hampshire Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nhia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nhia_real  = 'newhampshireinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nhia_proto = strtolower(trim(explode(',', $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'))[0]));
$nhia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
$nhia_path  = strtok($nhia_uri, '?');
$nhia_q     = strpos($nhia_uri, '?') !== false ? substr($nhia_uri, strpos($nhia_uri, '?')) : '';
// /dir/index.php and /index.php are duplicate URLs of /dir/ and /.
if (preg_match('#^(.*/)index\.php$#', $nhia_path, $nhia_m)) {
    $nhia_path = $nhia_m[1];
    $nhia_idx = true;
}
// 301 www. and plain http to https://newhampshireinsuranceappraiser.com - only on the real domain.
if ($nhia_host === 'www.' . $nhia_real || ($nhia_host === $nhia_real && $nhia_proto === 'http')) {
    header('Location: https://' . $nhia_real . $nhia_path . $nhia_q, true, 301);
    exit;
}
if (!empty($nhia_idx)) {
    header('Location: ' . $nhia_path . $nhia_q, true, 301);
    exit;
}
// Keep preview / temporary domains out of search results.
if ($nhia_host !== $nhia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
