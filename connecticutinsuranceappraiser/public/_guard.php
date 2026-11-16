<?php
// Connecticut Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$cia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$cia_real  = 'connecticutinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$cia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://connecticutinsuranceappraiser.com - only on the real domain.
if ($cia_host === 'www.' . $cia_real || ($cia_host === $cia_real && $cia_proto === 'http')) {
    header('Location: https://' . $cia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$cia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($cia_uri, '?'), $cia_m)) {
    $cia_q = strpos($cia_uri, '?') !== false ? substr($cia_uri, strpos($cia_uri, '?')) : '';
    header('Location: ' . $cia_m[1] . $cia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($cia_host !== $cia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
