<?php
// Contact form handler: emails the message to the site inbox.
$to = 'info@hatetolovethesplit.com';
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: /contact/', true, 303); exit; }
$clean = fn($v) => trim(str_replace(["\r", "\n"], ' ', (string)($v ?? '')));
$name  = mb_substr($clean($_POST['name'] ?? ''), 0, 120);
$email = filter_var($clean($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$msg   = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);
if (!empty($_POST['website'])) { header('Location: /contact/?sent=1', true, 303); exit; } // honeypot
if ($name === '' || !$email || $msg === '') { header('Location: /contact/?error=1', true, 303); exit; }
$headers = "From: Hate to Love the Split <{$to}>\r\nReply-To: {$email}\r\nContent-Type: text/plain; charset=utf-8";
$ok = @mail($to, "Website message from {$name}", "Name: {$name}\nEmail: {$email}\n\n{$msg}\n", $headers);
header('Location: /contact/?' . ($ok ? 'sent=1' : 'error=1'), true, 303);
