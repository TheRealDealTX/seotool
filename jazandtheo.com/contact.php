<?php
// jazandtheo.com - contact form handler.
// Validates the /contact/ form, emails it to info@jazandtheo.com and answers
// with JSON (AJAX) or a redirect to /contact/thanks/ (plain form post).

declare(strict_types=1);

const TO_EMAIL   = 'info@jazandtheo.com';
const FROM_EMAIL = 'info@jazandtheo.com';
const LOG_DIR    = __DIR__ . '/../inquiries';   // outside the document root; optional

$ajax = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $message, int $status = 200): void
{
    global $ajax;
    if ($ajax) {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $message], JSON_UNESCAPED_UNICODE);
        exit;
    }
    if ($ok) {
        header('Location: /contact/thanks/', true, 303);
        exit;
    }
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Could not send</title>'
        . '<body style="font-family:sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem">'
        . '<h1>Your note could not be sent</h1><p>' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8') . '</p>'
        . '<p><a href="/contact/">Go back</a> or email <a href="mailto:' . TO_EMAIL . '">' . TO_EMAIL . '</a>.</p></body>';
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Location: /contact/', true, 302);
    exit;
}

$field = static function (string $key, int $max = 2000): string {
    $v = $_POST[$key] ?? '';
    if (!is_string($v)) {
        return '';
    }
    $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/', '', $v) ?? '');
    return mb_substr($v, 0, $max);
};

// Honeypot: real visitors never see this field.
if ($field('website') !== '') {
    respond(true, 'ok');
}

$name    = $field('name', 120);
$email   = $field('email', 200);
$topic   = $field('topic', 80);
$message = $field('message', 5000);

if (mb_strlen($name) < 2) {
    respond(false, 'Please enter your name.', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please enter a valid email address so we can reply.', 422);
}
if (mb_strlen($message) < 10) {
    respond(false, 'Please write a little more in your message.', 422);
}
foreach ([$name, $email, $topic] as $hv) {
    if (preg_match('/[\r\n]/', $hv)) {
        respond(false, 'Invalid input.', 400);
    }
}

$host    = preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'jazandtheo.com');
$subject = 'Jaz & Theo website: ' . ($topic !== '' ? $topic : 'New message') . ' from ' . $name;
$body    = "Name: $name\nEmail: $email\nTopic: " . ($topic ?: '-') . "\nSent from: $host\nTime: " . gmdate('Y-m-d H:i') . " UTC\n\n$message\n";
$headers = [
    'From: Jaz & Theo <' . FROM_EMAIL . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'Content-Type: text/plain; charset=utf-8',
    'X-Mailer: jazandtheo.com',
];

$sent = @mail(TO_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

if (is_dir(LOG_DIR) || @mkdir(LOG_DIR, 0700, true)) {
    @file_put_contents(LOG_DIR . '/' . gmdate('Y-m') . '.log', str_repeat('-', 60) . "\n" . $body . 'mail(): ' . ($sent ? 'ok' : 'failed') . "\n", FILE_APPEND | LOCK_EX);
}

if (!$sent) {
    respond(false, 'The mail server did not accept the message. Please email ' . TO_EMAIL . ' directly.', 502);
}
respond(true, 'ok');
