<?php
// Georgia Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$gia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$gia_real  = 'georgiainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$gia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://georgiainsuranceappraiser.com - only on the real domain.
if ($gia_host === 'www.' . $gia_real || ($gia_host === $gia_real && $gia_proto === 'http')) {
    header('Location: https://' . $gia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($gia_host !== $gia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
