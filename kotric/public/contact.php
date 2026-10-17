<?php
// Contact form handler: emails info@kotric.com and keeps a copy outside the web root.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function reply($ok, $msg, $code = 200) {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'message' => $msg]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    reply(false, 'Please use the form on the contact page.', 405);
}
if (!empty($_POST['website'])) {               // honeypot
    reply(true, 'Thanks! Your message has been sent.');
}

$name    = trim(strip_tags($_POST['name'] ?? ''));
$email   = trim($_POST['email'] ?? '');
$topic   = trim(strip_tags($_POST['topic'] ?? 'General'));
$message = trim(strip_tags($_POST['message'] ?? ''));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    reply(false, 'Please fill in your name, a valid email address and a message.', 422);
}
if (mb_strlen($message) > 5000 || mb_strlen($name) > 120) {
    reply(false, 'That message is a little long — please shorten it or email us directly.', 422);
}
$name  = preg_replace('/[\r\n]+/', ' ', $name);
$topic = preg_replace('/[\r\n]+/', ' ', $topic);

$to      = 'info@kotric.com';
$subject = 'Kotric contact: ' . mb_substr($topic, 0, 60);
$body    = "Name: $name\nEmail: $email\nTopic: $topic\n\n$message\n";
$headers = "From: Kotric Website <info@kotric.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";

$sent = @mail($to, $subject, $body, $headers);
@file_put_contents(dirname(__DIR__) . '/kotric-contact-messages.log',
    '[' . date('c') . "] $body----\n", FILE_APPEND | LOCK_EX);

if ($sent) {
    reply(true, 'Thanks! Your message has been sent — we usually reply within two working days.');
}
reply(true, 'Thanks! We received your message. If it is urgent, email info@kotric.com directly.');
