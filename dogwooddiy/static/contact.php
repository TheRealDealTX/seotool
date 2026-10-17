<?php
// Contact form handler: emails the message to info@dogwooddiy.com.
$to = 'info@dogwooddiy.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /contact/', true, 303);
    exit;
}
$clean = function ($v, $max) {
    $v = trim((string)($v ?? ''));
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr($v, 0, $max);
};
// Honeypot: bots fill the hidden "website" field.
if (!empty($_POST['website'])) {
    header('Location: /contact/?sent=1', true, 303);
    exit;
}
$name = $clean($_POST['name'] ?? '', 100);
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$topic = $clean($_POST['topic'] ?? 'Message', 60);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);
if ($name === '' || !$email || $message === '') {
    header('Location: /contact/?sent=0', true, 303);
    exit;
}
$subject = '=?UTF-8?B?' . base64_encode("[Dogwood DIY] $topic from $name") . '?=';
$body = "Name: $name\nEmail: $email\nTopic: $topic\n\n$message\n";
$headers = "From: Dogwood DIY <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$ok = mail($to, $subject, $body, $headers);
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
