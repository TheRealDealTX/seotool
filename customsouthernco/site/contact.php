<?php
// Minimal contact form handler: validates, drops spam, mails info@customsouthernco.com.
$to = 'info@customsouthernco.com';
$back = '/contact/';
$ajax = ($_SERVER['HTTP_ACCEPT'] ?? '') === 'application/json';
function done($ok, $msg, $ajax, $back) {
    if ($ajax) { header('Content-Type: application/json'); echo json_encode(['ok' => $ok, 'message' => $msg]); exit; }
    header('Location: ' . $back . '?sent=' . ($ok ? '1' : '0'), true, 303); exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ' . $back, true, 303); exit; }
if (!empty($_POST['website'])) { done(true, 'Thanks!', $ajax, $back); }
$name = trim(substr(strip_tags($_POST['name'] ?? ''), 0, 120));
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$subject = trim(substr(strip_tags($_POST['subject'] ?? 'General question'), 0, 80));
$message = trim(substr(strip_tags($_POST['message'] ?? ''), 0, 5000));
if (!$name || !$email || !$message) { done(false, 'Please fill in your name, a valid email and a message.', $ajax, $back); }
$name = str_replace(["\r", "\n"], ' ', $name);
$headers = "From: Custom Southern Co. <{$to}>\r\nReply-To: {$name} <{$email}>\r\nContent-Type: text/plain; charset=utf-8";
$ok = @mail($to, "[Contact] {$subject} - {$name}", "Name: {$name}\nEmail: {$email}\n\n{$message}", $headers);
done($ok, $ok ? "Thanks, {$name}! Your message is on its way." : 'Sorry, the message could not be sent. Please email ' . $to . ' directly.', $ajax, $back);
