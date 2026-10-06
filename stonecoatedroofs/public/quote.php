<?php
// Estimate-request handler for every lead form on stonecoatedroofs.com.
// Each request is appended to scr-leads/quote-requests.php: a PHP file whose first
// line exits, so requesting it over the web returns an empty page — the JSON lines
// after it are only readable through the file manager. (The host does not let PHP
// write outside public_html; a folder above it is used instead when writable.)
// If scr-config.php exists (here or one level up) the request is also emailed:
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

$dir = null;
foreach ([dirname(__DIR__) . '/scr-leads', __DIR__ . '/scr-leads'] as $cand) {
    if ((is_dir($cand) || @mkdir($cand, 0700, true)) && is_writable($cand)) { $dir = $cand; break; }
}
if ($dir === null) $dir = sys_get_temp_dir();
$guard = "<?php http_response_code(404); exit; ?>\n";

// light rate limit: 5 requests per IP per 10 minutes
$rl = $dir . '/rate-' . md5($lead['ip']) . '.php';
$hits = array_filter(array_map('intval', array_slice(@file($rl, FILE_IGNORE_NEW_LINES) ?: [], 1)), function ($t) { return $t > time() - 600; });
if (count($hits) >= 5) out(429, ['ok' => false, 'error' => 'Too many requests — please call us instead.']);
$hits[] = time();
@file_put_contents($rl, $guard . implode("\n", $hits));

$store = $dir . '/quote-requests.php';
if (!is_file($store)) @file_put_contents($store, $guard);
$saved = @file_put_contents($store, json_encode($lead, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX) !== false;

$cfg = null;
foreach ([dirname(__DIR__) . '/scr-config.php', __DIR__ . '/scr-config.php'] as $c) {
    if (is_file($c)) { $cfg = @include $c; break; }
}
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
