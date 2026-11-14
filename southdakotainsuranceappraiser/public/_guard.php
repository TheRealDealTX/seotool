<?php
// South Dakota Insurance Appraiser - canonical host guard.
// Required by index.php and by the first line of every dir/index.php page.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$sdia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$sdia_real  = 'southdakotainsuranceappraiser.com';
$sdia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$sdia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://southdakotainsuranceappraiser.com - only on the real domain.
if ($sdia_host === 'www.' . $sdia_real || ($sdia_host === $sdia_real && $sdia_proto === 'http')) {
    header('Location: https://' . $sdia_real . $sdia_uri, true, 301);
    exit;
}
// /dir/index.php (and /index.php) duplicate the directory URL: 301 to /dir/.
if (preg_match('#^(.*/)index\.php$#', strtok($sdia_uri, '?'), $sdia_m)) {
    $sdia_q = strpos($sdia_uri, '?') !== false ? substr($sdia_uri, strpos($sdia_uri, '?')) : '';
    header('Location: ' . $sdia_m[1] . $sdia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($sdia_host !== $sdia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
