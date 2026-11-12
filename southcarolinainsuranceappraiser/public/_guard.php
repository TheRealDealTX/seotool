<?php
// South Carolina Insurance Appraiser - canonical host guard. Required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$scia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$scia_real  = 'southcarolinainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$scia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://southcarolinainsuranceappraiser.com - only on the real domain.
if ($scia_host === 'www.' . $scia_real || ($scia_host === $scia_real && $scia_proto === 'http')) {
    header('Location: https://' . $scia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory URL.
$scia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($scia_uri, '?'), $scia_m)) {
    $scia_q = strpos($scia_uri, '?') !== false ? substr($scia_uri, strpos($scia_uri, '?')) : '';
    header('Location: ' . $scia_m[1] . $scia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($scia_host !== $scia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
