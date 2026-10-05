<?php
/**
 * Estimate form handler. POST /contact/send
 * Validates, filters bots (honeypot + timing), emails the business and logs
 * the lead to a file outside the document root. Redirects to /thank-you/.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    redirect(SITE_ORIGIN . '/contact/');
}

$f = fn(string $k, int $max = 200): string => mb_substr(trim((string) ($_POST[$k] ?? '')), 0, $max);
$first = $f('first_name', 60);
$last = $f('last_name', 60);
$email = $f('email', 120);
$phone = $f('phone', 30);
$service = $f('service', 80);
$city = $f('city', 60);
$message = $f('message', 2000);
$honey = $f('website', 200);
$ts = (int) ($_POST['ts'] ?? 0);
$fromPage = $f('page', 200);

// Bots: honeypot filled, or submitted faster than a human could type.
if ($honey !== '' || ($ts && time() - $ts < 3)) {
    redirect(SITE_ORIGIN . '/thank-you/', 303);
}

$errors = [];
if ($first === '' || $last === '') $errors[] = 'name';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'email';
if (strlen(preg_replace('/\D/', '', $phone)) < 10) $errors[] = 'phone';
if ($errors) {
    redirect(SITE_ORIGIN . '/contact/?sent=0&fields=' . implode(',', $errors) . '#contact', 303);
}

$lines = [
    "New estimate request from austinlandscapelighting.com",
    "",
    "Name:    {$first} {$last}",
    "Email:   {$email}",
    "Phone:   {$phone}",
    "Service: " . ($service ?: '(not specified)'),
    "City:    " . ($city ?: '(not specified)'),
    "Page:    " . ($fromPage ?: '/contact/'),
    "",
    "Message:",
    $message ?: '(none)',
    "",
    "Sent " . date('c') . " from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
];
$bodyText = implode("\n", $lines);

$to = BIZ['email'];
$subject = "Estimate request: {$first} {$last}" . ($city ? " ({$city})" : '');
$safeName = preg_replace('/[\r\n"]+/', ' ', "{$first} {$last}");
$headers = [
    'From: Austin Landscape Lighting Website <no-reply@austinlandscapelighting.com>',
    'Reply-To: ' . $safeName . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
];
$sent = @mail($to, $subject, $bodyText, implode("\r\n", $headers));

// Lead log outside public_html (best effort).
$logDir = dirname(SITE_ROOT) . '/leads';
if (!is_dir($logDir)) {
    @mkdir($logDir, 0750, true);
}
if (is_dir($logDir) && is_writable($logDir)) {
    @file_put_contents($logDir . '/leads.log', $bodyText . "\n" . str_repeat('-', 60) . "\n", FILE_APPEND | LOCK_EX);
}

redirect(SITE_ORIGIN . '/thank-you/' . ($sent ? '' : '?mail=0'), 303);
