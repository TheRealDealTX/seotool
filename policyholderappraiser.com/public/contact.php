<?php
// policyholderappraiser.com - contact form handler.
// Receives the POST from the site forms, validates, emails the office, and
// answers JSON (fetch) or redirects to /thank-you/ (no-JS fallback).
//
// Recipient: set FORM_TO in ../form-config.php (outside public_html), e.g.
//   <?php const FORM_TO = 'someone@example.com';
// Without that file the message goes to the site's own info@ mailbox.
declare(strict_types=1);

$cfg = __DIR__ . '/../form-config.php';
if (is_file($cfg)) { require $cfg; }
if (!defined('FORM_TO')) { define('FORM_TO', 'info@policyholderappraiser.com'); }

const FROM     = 'forms@policyholderappraiser.com';
const SITE     = 'https://policyholderappraiser.com';
const MAX_LEN  = 4000;

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $message, int $code = 200): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message]);
        exit;
    }
    if ($ok) {
        header('Location: ' . SITE . '/thank-you/', true, 303);
        exit;
    }
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><meta charset="utf-8"><title>Form error</title><p>' . htmlspecialchars($message) .
         ' Please call or text (832) 503-5866, or <a href="' . SITE . '/contact/">go back</a>.</p>';
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: ' . SITE . '/contact/', true, 302);
    exit;
}

// Same-origin check (no cookies, so this is the CSRF guard).
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
if ($origin !== '' && stripos($origin, 'policyholderappraiser.com') === false) {
    respond(false, 'Request rejected.', 403);
}

// Honeypot: real visitors never see this field.
if (trim((string)($_POST['website'] ?? '')) !== '') {
    respond(true, 'Thanks.');
}

$clean = static function (string $key, int $max = 300): string {
    $v = trim((string)($_POST[$key] ?? ''));
    $v = preg_replace('/[\r\n\t]+/', ' ', $v) ?? '';
    return mb_substr($v, 0, $max);
};

$name    = $clean('name');
$phone   = $clean('phone', 40);
$email   = $clean('email');
$zip     = $clean('zip', 20);
$carrier = $clean('carrier', 120);
$stage   = $clean('stage', 120);
$type    = $clean('type', 120);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, MAX_LEN);
$page    = $clean('page', 200);

if ($name === '' || $phone === '') {
    respond(false, 'Please include your name and phone number.', 422);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'That email address does not look right.', 422);
}
if (preg_match_all('/https?:\/\//i', $message) > 2) {
    respond(false, 'Please remove the links from your message.', 422);
}
if (empty($_POST['consent'])) {
    respond(false, 'Please confirm that we may contact you about your claim.', 422);
}

$lines = [
    "New appraisal inquiry from policyholderappraiser.com",
    "",
    "Name:      $name",
    "Phone:     $phone",
    "Email:     " . ($email ?: '-'),
    "ZIP:       " . ($zip ?: '-'),
    "Carrier:   " . ($carrier ?: '-'),
    "Stage:     " . ($stage ?: '-'),
    "Loss type: " . ($type ?: '-'),
    "Page:      " . ($page ?: '-'),
    "",
    "Message:",
    $message !== '' ? $message : '-',
    "",
    "IP: " . ($_SERVER['REMOTE_ADDR'] ?? '-'),
    "Time: " . date('c'),
];
$body = implode("\n", $lines);

$headers = [
    'From: Policyholder Appraiser <' . FROM . '>',
    'Reply-To: ' . ($email !== '' ? "$name <$email>" : FROM),
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
];

$subject = 'Appraisal inquiry: ' . $name . ($zip ? " ($zip)" : '');
$sent = @mail(FORM_TO, $subject, $body, implode("\r\n", $headers), '-f' . FROM);

// Always keep a copy on the server (outside public_html) in case mail is delayed.
$logDir = __DIR__ . '/../form-log';
if (!is_dir($logDir)) { @mkdir($logDir, 0700, true); }
@file_put_contents($logDir . '/' . date('Y-m') . '.log', $body . "\n" . str_repeat('-', 60) . "\n", FILE_APPEND | LOCK_EX);

if (!$sent) {
    respond(false, 'We could not send your message right now.', 500);
}
respond(true, 'Thanks. We will be in touch shortly.');
