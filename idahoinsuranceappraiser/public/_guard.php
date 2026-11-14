<?php
// Idaho Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$iia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$iia_real  = 'idahoinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$iia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://idahoinsuranceappraiser.com - only on the real domain.
if ($iia_host === 'www.' . $iia_real || ($iia_host === $iia_real && $iia_proto === 'http')) {
    header('Location: https://' . $iia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$iia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($iia_uri, '?'), $iia_m)) {
    $iia_q = strpos($iia_uri, '?') !== false ? substr($iia_uri, strpos($iia_uri, '?')) : '';
    header('Location: ' . $iia_m[1] . $iia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($iia_host !== $iia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
