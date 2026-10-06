<?php
// Renter News contact form handler. Mails the newsroom; answers JSON for the
// fetch() in site.js and redirects back for no-JS submissions.
$to = 'info@renternews.net';
$json = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
function done($ok, $msg, $json) {
    if ($json) { header('Content-Type: application/json'); echo json_encode(['ok' => $ok, 'error' => $ok ? null : $msg]); }
    else { header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303); }
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
if (!empty($_POST['website'])) done(true, '', $json);                     // honeypot: pretend success
$name  = trim(substr(strip_tags($_POST['name'] ?? ''), 0, 100));
$email = trim(substr($_POST['email'] ?? '', 0, 200));
$topic = trim(substr(strip_tags($_POST['topic'] ?? 'Other'), 0, 40));
$msg   = trim(substr(strip_tags($_POST['message'] ?? ''), 0, 5000));
if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) done(false, 'Please fill in your name, a valid email and a message.', $json);
$name = str_replace(["\r", "\n"], ' ', $name);
$body = "Name: $name\nEmail: $email\nTopic: $topic\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n\n$msg\n";
$headers = "From: Renter News <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8";
$ok = mail($to, "[Renter News] $topic from $name", $body, $headers);
done($ok, 'Sorry, the message could not be sent. Please email info@renternews.net.', $json);
