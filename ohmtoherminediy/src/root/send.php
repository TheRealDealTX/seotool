<?php
// Contact + newsletter form handler. Emails submissions to the site inbox.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');
$to = 'info@ohmtoherminediy.com';

function out($ok, $msg, $code = 200) { http_response_code($code); echo json_encode(['ok' => $ok, 'message' => $msg]); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(false, 'Method not allowed.', 405);
if (!empty($_POST['website'])) out(true, 'Thank you!');               // honeypot: pretend success

$type  = ($_POST['type'] ?? '') === 'newsletter' ? 'newsletter' : 'contact';
$email = trim($_POST['email'] ?? '');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(false, 'Please enter a valid email address.', 422);

$clean = function ($s, $max) { return mb_substr(trim(str_replace(["\r", "\0"], '', (string)$s)), 0, $max); };
$name  = $clean($_POST['name'] ?? '', 120);
$topic = $clean($_POST['topic'] ?? '', 120);
$msg   = $clean($_POST['message'] ?? '', 5000);
if ($type === 'contact' && ($name === '' || $msg === '')) out(false, 'Please fill in your name and message.', 422);

// Very small rate limit: one submission per IP per 30 seconds.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? 'x');
$lock = sys_get_temp_dir() . '/omm_' . md5($ip);
if (is_file($lock) && time() - filemtime($lock) < 30) out(false, 'Please wait a few seconds before sending again.', 429);
@touch($lock);

$subject = $type === 'newsletter' ? 'New newsletter signup' : 'Contact form: ' . ($topic ?: 'Message') . ' from ' . str_replace("\n", ' ', $name);
$body = $type === 'newsletter'
    ? "Newsletter signup\n\nEmail: $email\nDate: " . date('c') . "\n"
    : "Name: $name\nEmail: $email\nTopic: $topic\n\n$msg\n\n--\nSent " . date('c') . " from the ohmtoherminediy.com contact form\n";
$headers = "From: Oh, Mother Mine DIY <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8\r\nX-Mailer: PHP";

$sent = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $to);
if (!$sent) out(false, "We couldn't send that right now. Please email info@ohmtoherminediy.com directly.", 500);
out(true, $type === 'newsletter' ? "You're in! Watch your inbox for our next project. 💌" : "Thank you! We'll reply within two business days.");
