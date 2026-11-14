<?php
// Pennsylvania Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$pia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$pia_real  = 'pennsylvaniainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$pia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://pennsylvaniainsuranceappraiser.com - only on the real domain.
if ($pia_host === 'www.' . $pia_real || ($pia_host === $pia_real && $pia_proto === 'http')) {
    header('Location: https://' . $pia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$pia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($pia_uri, '?'), $pia_m)) {
    $pia_q = strpos($pia_uri, '?') !== false ? substr($pia_uri, strpos($pia_uri, '?')) : '';
    header('Location: ' . $pia_m[1] . $pia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($pia_host !== $pia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
