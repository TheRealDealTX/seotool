<?php
// Contact + newsletter handler. Sends to the site inbox and keeps a CSV copy outside public_html.
$to = 'info@findsforfitness.com';
$back = $_SERVER['HTTP_REFERER'] ?? '/contact/';
if (parse_url($back, PHP_URL_HOST) && parse_url($back, PHP_URL_HOST) !== ($_SERVER['HTTP_HOST'] ?? '')) { $back = '/contact/'; }
$back = strtok($back, '?#');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
if (!empty($_POST['website'])) { header('Location: ' . $back . '?sent=1', true, 303); exit; }   // honeypot

$clean = fn($v, $n) => trim(substr(str_replace(["\r", "\n"], ' ', (string)($v ?? '')), 0, $n));
$type = $_POST['type'] === 'newsletter' ? 'newsletter' : 'contact';
$email = filter_var($clean($_POST['email'] ?? '', 200), FILTER_VALIDATE_EMAIL);
if (!$email) { header('Location: ' . $back . '?error=email', true, 303); exit; }
$name = $clean($_POST['name'] ?? '', 120);
$topic = $clean($_POST['topic'] ?? '', 80);
$message = trim(substr((string)($_POST['message'] ?? ''), 0, 5000));

$subject = $type === 'newsletter' ? 'New newsletter subscriber' : 'Contact form: ' . ($topic ?: 'Message') . ' from ' . ($name ?: $email);
$body = "Type: $type\nName: $name\nEmail: $email\nTopic: $topic\n\n$message\n\n--\nSent from findsforfitness.com";
$headers = "From: Finds For Fitness <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";
@mail($to, $subject, $body, $headers);

$log = dirname(__DIR__) . '/form-submissions.csv';
if ($fh = @fopen($log, 'a')) { fputcsv($fh, [date('c'), $type, $name, $email, $topic, $message]); fclose($fh); }

header('Location: ' . $back . '?sent=1' . ($type === 'newsletter' ? '#nl-h' : ''), true, 303);
