<?php
// fraserandmorris.com - contact form handler. Emails enquiries to the studio.
$to = 'info@fraserandmorris.com';
$back = '/contact.html';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: ' . $back, true, 303);
    exit;
}
function field($k, $max) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}
// Honeypot: bots fill the hidden "website" field.
if (field('website', 200) !== '') {
    header('Location: ' . $back . '?sent=1#form', true, 303);
    exit;
}
$name = str_replace("\n", ' ', field('name', 120));
$email = field('email', 160);
$phone = str_replace("\n", ' ', field('phone', 40));
$location = str_replace("\n", ' ', field('location', 120));
$type = str_replace("\n", ' ', field('type', 80));
$message = field('message', 5000);

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: ' . $back . '?error=1#form', true, 303);
    exit;
}
$body = "New garden enquiry from fraserandmorris.com\n\n"
      . "Name: $name\nEmail: $email\nPhone: $phone\nLocation: $location\nGarden type: $type\n\n"
      . "Message:\n$message\n";
$headers = [
    'From: Fraser & Morris Website <' . $to . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=utf-8',
];
$ok = @mail($to, 'Garden enquiry: ' . $name, $body, implode("\r\n", $headers));
header('Location: ' . $back . ($ok ? '?sent=1' : '?error=1') . '#form', true, 303);
