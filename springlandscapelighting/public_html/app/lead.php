<?php
defined('SLT') || exit;
// Handles quote / contact form posts. Responds with JSON for fetch() callers and
// redirects to /thank-you/ for plain form posts.

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
$fail = function (string $msg, int $code = 422) use ($wantsJson) {
    if ($wantsJson) { http_response_code($code); header('Content-Type: application/json'); echo json_encode(['ok' => false, 'error' => $msg]); exit; }
    redirect('/quote/?error=1', 303);
};
$clean = fn($k, $n = 200) => trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $n));

$ts  = (int)($_POST['ts'] ?? 0);
$sig = (string)($_POST['sig'] ?? '');
$bot = $clean('website') !== '' || !hash_equals(hash_hmac('sha256', (string)$ts, form_secret()), $sig) || time() - $ts < 3 || time() - $ts > 86400 * 2;

$name = $clean('name', 120); $phone = $clean('phone', 40); $email = $clean('email', 160);
$project = $clean('project', 80); $area = $clean('area', 120); $time = $clean('time', 30);
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 4000));
$source = $clean('source', 200);

if ($name === '' || ($phone === '' && $email === '')) $fail('Please add your name and a phone number or email.');
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) $fail('Please check your email address.');
if ($bot) { // Pretend success so bots learn nothing.
    if ($wantsJson) { header('Content-Type: application/json'); echo json_encode(['ok' => true]); exit; }
    redirect('/thank-you/', 303);
}

$row = ['time' => date('c'), 'name' => $name, 'phone' => $phone, 'email' => $email, 'project' => $project, 'area' => $area,
        'best_time' => $time, 'message' => $message, 'source' => $source, 'ip' => $_SERVER['REMOTE_ADDR'] ?? ''];

// Keep a copy on the server (PHP-guarded so the file can't be downloaded).
$log = APP . '/data/leads.php';
if (!is_file($log)) @file_put_contents($log, "<?php exit; ?>\n");
@file_put_contents($log, json_encode($row, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

$body = "New lighting consultation request\n\n";
foreach ($row as $k => $v) $body .= str_pad(ucfirst(str_replace('_', ' ', $k)) . ':', 12) . " $v\n";
$headers = "From: Spring Landscape Lighting <no-reply@springlandscapelighting.com>\r\n"
         . ($email ? "Reply-To: " . str_replace(["\n", "\r"], '', $email) . "\r\n" : '')
         . "Content-Type: text/plain; charset=UTF-8\r\n";
@mail(LEAD_TO, 'New quote request: ' . $name . ($project ? " ($project)" : ''), $body, $headers);

if ($wantsJson) { header('Content-Type: application/json'); echo json_encode(['ok' => true]); exit; }
redirect('/thank-you/', 303);
