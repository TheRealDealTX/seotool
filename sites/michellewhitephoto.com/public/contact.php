<?php
// Contact form handler: emails inquiries to the studio address.
$to = 'info@michellewhitephoto.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }

function field($k, $max = 200) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr($v, 0, $max);
}
// Honeypot: bots fill the hidden "website" field.
if (!empty($_POST['website'])) { header('Location: /contact/?sent=1', true, 303); exit; }

$name = field('name', 120);
$email = filter_var(field('email', 200), FILTER_VALIDATE_EMAIL);
$type = field('type', 60);
$date = field('date', 80);
$loc = field('location', 200);
$msg = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);

if ($name === '' || !$email || $msg === '') { header('Location: /contact/?sent=0', true, 303); exit; }

$host = preg_replace('/[^a-z0-9.-]/i', '', $_SERVER['HTTP_HOST'] ?? 'michellewhitephoto.com');
$subject = "New inquiry: $type - $name";
$body = "Name: $name\nEmail: $email\nInquiry: $type\nDate: $date\nLocation: $loc\n\n$msg\n\n-- Sent from $host";
$headers = "From: Michelle White Photo <no-reply@michellewhitephoto.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";
$ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
