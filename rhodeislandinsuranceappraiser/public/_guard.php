<?php
// Rhode Island Insurance Appraiser - canonical host guard. Required by index.php and by the first line of every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$ria_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$ria_real  = 'rhodeislandinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$ria_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$ria_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://rhodeislandinsuranceappraiser.com - only on the real domain.
if ($ria_host === 'www.' . $ria_real || ($ria_host === $ria_real && $ria_proto === 'http')) {
    header('Location: https://' . $ria_real . preg_replace('#^(.*/)index\.php(\?|$)#', '$1$2', $ria_uri), true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory URL.
if (preg_match('#^(.*/)index\.php$#', strtok($ria_uri, '?'), $ria_m)) {
    $ria_q = strpos($ria_uri, '?') !== false ? substr($ria_uri, strpos($ria_uri, '?')) : '';
    header('Location: ' . $ria_m[1] . $ria_q, true, 301);
    exit;
}
// Keep the temporary preview domain (and any other host) out of search results.
if ($ria_host !== $ria_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
