<?php
// Estimate / contact form handler. Emails the lead to FORM_TO (SMTP via
// includes/.smtp.php when present, else mail()) and keeps a
// backup copy in includes/leads.log (web access to includes/ is denied).
require __DIR__ . '/includes/layout.php';
require __DIR__ . '/includes/mailer.php';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact-us/', true, 303);
    exit;
}

$back = '/contact-us/';
$clean = fn($k, $max = 200) => trim(mb_substr(str_replace(["\r", "\n"], ' ', (string) ($_POST[$k] ?? '')), 0, $max));

$name    = $clean('name', 120);
$phone   = $clean('phone', 40);
$email   = $clean('email', 160);
$address = $clean('address', 200);
$service = $clean('service', 80);
$source  = $clean('source', 200);
$message = trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 4000));
$ts      = (int) ($_POST['ts'] ?? 0);
$sig     = (string) ($_POST['sig'] ?? '');

// Spam checks: honeypot, signed timestamp, minimum fill time, link spam.
$age = time() - $ts;
$spam = ($_POST['website'] ?? '') !== ''
    || !hash_equals(hash_hmac('sha256', (string) $ts, form_secret()), $sig)
    || $age < 3 || $age > 86400
    || preg_match_all('#https?://#i', $message) > 2;

if ($spam) {
    header('Location: /thank-you/', true, 303); // don't tell bots they failed
    exit;
}
if ($name === '' || ($phone === '' && $email === '') || ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL))) {
    header('Location: ' . $back . '?error=1#quote', true, 303);
    exit;
}

$lines = [
    'New roofing estimate request from austinsroofing.com',
    '',
    'Name:     ' . $name,
    'Phone:    ' . $phone,
    'Email:    ' . $email,
    'Address:  ' . $address,
    'Service:  ' . $service,
    'Page:     ' . $source,
    'Time:     ' . date('Y-m-d H:i:s T'),
    '',
    'Message:',
    $message,
];
$body = implode("\n", $lines);
$subject = 'Roofing estimate request: ' . ($service ?: 'General') . ' — ' . $name;
$replyTo = $email !== '' ? $name . ' <' . $email . '>' : '';
$error = null;
$cfg = smtp_config();
if ($cfg) {
    // Preferred: authenticated SMTP through the info@ mailbox.
    $sent = smtp_send($cfg, FORM_TO, $subject, $body, $replyTo, $error);
} else {
    $headers = ['From: Austin Roofing Website <noreply@austinsroofing.com>', 'Content-Type: text/plain; charset=UTF-8'];
    if ($replyTo !== '') {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    $sent = @mail(FORM_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), '-fnoreply@austinsroofing.com');
}

@file_put_contents(__DIR__ . '/includes/leads.log', json_encode([
    'time' => date('c'), 'sent' => $sent, 'error' => $error, 'name' => $name, 'phone' => $phone, 'email' => $email,
    'address' => $address, 'service' => $service, 'source' => $source, 'message' => $message,
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);

header('Location: /thank-you/', true, 303);
