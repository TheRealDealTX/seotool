<?php
// Arkansas Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$aia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$aia_real  = 'arkansasinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$aia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$aia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://arkansasinsuranceappraiser.com - only on the real domain.
if ($aia_host === 'www.' . $aia_real || ($aia_host === $aia_real && $aia_proto === 'http')) {
    $aia_uri = preg_replace('#^((?:[^?]*/)?)index\.php(?=$|\?)#', '$1', $aia_uri);
    header('Location: https://' . $aia_real . $aia_uri, true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($aia_uri, '?'), $aia_m)) {
    $aia_q = strpos($aia_uri, '?') !== false ? substr($aia_uri, strpos($aia_uri, '?')) : '';
    header('Location: ' . $aia_m[1] . $aia_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($aia_host !== $aia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
