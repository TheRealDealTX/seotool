<?php
// Kentucky Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$kia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$kia_real  = 'kentuckyinsuranceappraiser.com';
$kia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$kia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// /dir/index.php (or /index.php) duplicates /dir/: drop the file name, keeping any query string.
$kia_path  = (string) strtok($kia_uri, '?');
$kia_query = strpos($kia_uri, '?') !== false ? substr($kia_uri, strpos($kia_uri, '?')) : '';
$kia_clean = preg_replace('#(^|/)index\.php$#', '$1', $kia_path);
$kia_wrong = ($kia_host === 'www.' . $kia_real || ($kia_host === $kia_real && $kia_proto === 'http'));
// One 301 to https://kentuckyinsuranceappraiser.com for www. / plain http (real domain only) and for index.php URLs.
if ($kia_wrong) {
    header('Location: https://' . $kia_real . $kia_clean . $kia_query, true, 301);
    exit;
}
if ($kia_clean !== $kia_path) {
    header('Location: ' . $kia_clean . $kia_query, true, 301);
    exit;
}
// Keep preview/temporary hosts out of search results.
if ($kia_host !== $kia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
