<?php
// Estimate-request handler for every lead form on stonecoatedroofs.com.
// Each request is appended to a JSON-lines file OUTSIDE the web root and emailed
// to the address(es) in ../scr-config.php (also outside the web root), e.g.:
//   <?php return ['to' => 'leads@example.com', 'from' => 'no-reply@stonecoatedroofs.com'];
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

function out($code, $data) { http_response_code($code); echo json_encode($data); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(405, ['ok' => false, 'error' => 'POST only.']);
if (!empty($_POST['website'])) out(200, ['ok' => true]);           // honeypot: pretend success

$f = function ($k, $max = 200) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = preg_replace('/[\r\n\t]+/', ' ', $v);
    return mb_substr(strip_tags($v), 0, $max);
};
$lead = [
    'time'   => gmdate('c'),
    'name'   => $f('name', 120),
    'phone'  => $f('phone', 40),
    'email'  => $f('email', 160),
    'city'   => $f('city', 120),
    'type'   => $f('type', 80),
    'reason' => $f('reason', 80),
    'page'   => $f('page', 300),
    'ip'     => $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? ''),
    'ua'     => mb_substr((string)($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 250),
];
$digits = preg_replace('/\D/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || $lead['city'] === '') {
    out(422, ['ok' => false, 'error' => 'Please add your name, a 10-digit phone number and your city.']);
}
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    out(422, ['ok' => false, 'error' => 'That email address looks incomplete.']);
}

$private = dirname(__DIR__);                                           // the folder above public_html
$dir = $private . '/scr-leads';
if (!is_dir($dir)) @mkdir($dir, 0700, true);

// light rate limit: 5 requests per IP per 10 minutes
$rl = $dir . '/rate-' . md5($lead['ip']) . '.txt';
$hits = array_filter(array_map('intval', @file($rl, FILE_IGNORE_NEW_LINES) ?: []), function ($t) { return $t > time() - 600; });
if (count($hits) >= 5) out(429, ['ok' => false, 'error' => 'Too many requests — please call us instead.']);
$hits[] = time();
@file_put_contents($rl, implode("\n", $hits));

$saved = @file_put_contents($dir . '/quote-requests.jsonl', json_encode($lead, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX) !== false;

$cfg = @include $private . '/scr-config.php';
$sent = false;
if (is_array($cfg) && !empty($cfg['to'])) {
    $from = $cfg['from'] ?? 'no-reply@stonecoatedroofs.com';
    $subject = 'New estimate request: ' . $lead['name'] . ' (' . $lead['city'] . ')';
    $body = "New stone coated roofing estimate request\n\n";
    foreach (['name', 'phone', 'email', 'city', 'type', 'reason', 'page', 'time'] as $k) $body .= str_pad(ucfirst($k) . ':', 9) . $lead[$k] . "\n";
    $headers = "From: Stone Coated Roofs <$from>\r\nContent-Type: text/plain; charset=utf-8";
    if ($lead['email'] !== '') $headers .= "\r\nReply-To: " . $lead['email'];
    $sent = @mail($cfg['to'], $subject, $body, $headers);
}

if (!$saved && !$sent) out(500, ['ok' => false, 'error' => 'We could not save your request.']);
out(200, ['ok' => true]);
