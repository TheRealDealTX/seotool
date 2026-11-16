<?php
// Virginia Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$via_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$via_real  = 'virginiainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$via_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://virginiainsuranceappraiser.com - only on the real domain.
if ($via_host === 'www.' . $via_real || ($via_host === $via_real && $via_proto === 'http')) {
    header('Location: https://' . $via_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $via_m)) {
    $via_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $via_m[1] . $via_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($via_host !== $via_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
