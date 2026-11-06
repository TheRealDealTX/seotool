<?php
// Georgia Insurance Appraiser — lead form handler.
// Receives the site's claim forms (POST) and emails them to the inbox below.
// Returns JSON: {"ok":true} or {"ok":false,"error":"..."}.
declare(strict_types=1);

const TO_EMAIL   = 'info@georgiainsuranceappraiser.com';
const FROM_EMAIL = 'info@georgiainsuranceappraiser.com';
const SITE_NAME  = 'Georgia Insurance Appraiser';

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method']);
    exit;
}

// Honeypot: real visitors never fill this hidden field.
if (!empty($_POST['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

// Basic per-IP throttle (5 submissions per 10 minutes).
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '0');
$ip = trim(explode(',', $ip)[0]);
$bucket = sys_get_temp_dir() . '/gia_' . md5($ip);
$hits = array_filter(
    is_file($bucket) ? (array) json_decode((string) file_get_contents($bucket), true) : [],
    fn($t) => is_int($t) && $t > time() - 600
);
if (count($hits) >= 5) {
    http_response_code(429);
    echo json_encode(['ok' => false, 'error' => 'rate']);
    exit;
}
$hits[] = time();
@file_put_contents($bucket, json_encode(array_values($hits)));

$clean = function (string $k, int $max = 300): string {
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
};

$name    = $clean('name', 120);
$email   = $clean('email', 160);
$phone   = $clean('phone', 40);
$role    = $clean('role', 60);
$loss    = $clean('loss', 60);
$city    = $clean('city', 80);
$carrier = $clean('carrier', 120);
$amount  = $clean('amount', 60);
$details = $clean('details', 4000);
$page    = $clean('page', 200);
$consent = !empty($_POST['consent']);

if ($name === '' || (!filter_var($email, FILTER_VALIDATE_EMAIL) && $phone === '') || !$consent) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'invalid']);
    exit;
}

$lines = [
    'Name'          => $name,
    'Email'         => $email,
    'Phone'         => $phone,
    'Role'          => $role,
    'Type of loss'  => $loss,
    'Location'      => $city,
    'Insurer'       => $carrier,
    'Amount in dispute' => $amount,
    'Submitted from'    => $page,
    'IP'            => $ip,
    'Time'          => gmdate('Y-m-d H:i:s') . ' UTC',
];
$body = "New claim inquiry from " . SITE_NAME . "\n\n";
foreach ($lines as $k => $v) {
    if ($v !== '') $body .= str_pad($k . ':', 20) . $v . "\n";
}
$body .= "\nClaim details:\n" . ($details !== '' ? $details : '(none)') . "\n";

$subject = '=?UTF-8?B?' . base64_encode('New claim inquiry: ' . $name . ($loss ? " ($loss)" : '')) . '?=';
$headers = [
    'From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
];
if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $headers[] = 'Reply-To: ' . $email;
}

$sent = @mail(TO_EMAIL, $subject, $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

// Keep a private backup copy outside the web root in case mail delivery fails.
$log = dirname(__DIR__, 2) . '/gia-leads.log';
@file_put_contents($log, json_encode(['t' => time()] + $lines + ['details' => $details, 'mailed' => $sent]) . "\n", FILE_APPEND | LOCK_EX);

echo json_encode(['ok' => true]);
