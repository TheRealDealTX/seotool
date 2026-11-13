<?php
// Wisconsin Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$wia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$wia_real  = 'wisconsininsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$wia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://wisconsininsuranceappraiser.com - only on the real domain.
if ($wia_host === 'www.' . $wia_real || ($wia_host === $wia_real && $wia_proto === 'http')) {
    header('Location: https://' . $wia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$wia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($wia_uri, '?'), $wia_m)) {
    $wia_q = strpos($wia_uri, '?') !== false ? substr($wia_uri, strpos($wia_uri, '?')) : '';
    header('Location: ' . $wia_m[1] . $wia_q, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($wia_host !== $wia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
