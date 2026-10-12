<?php
// Contact form handler: emails the repair request to the business inbox.
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
function field($k, $max = 2000) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\n"], ' ', mb_substr($v, 0, $max));
    return $v;
}
if (field('website') !== '') { header('Location: /contact/?sent=1', true, 303); exit; }  // honeypot
$name = field('name', 120);
$email = filter_var(field('email', 200), FILTER_VALIDATE_EMAIL);
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 5000));
if (!$name || !$email || $message === '') { header('Location: /contact/?sent=0', true, 303); exit; }
$to = 'info@rjbledlcdtvservicecentre.com';
$subject = 'TV repair request: ' . field('brand', 60) . ' - ' . field('fault', 80);
$body = "Name: $name\nEmail: $email\nPhone: " . field('phone', 40) . "\nArea: " . field('area', 120)
      . "\nBrand: " . field('brand', 60) . "\nSymptom: " . field('fault', 80) . "\n\n" . $message . "\n";
$headers = "From: RJB Website <info@rjbledlcdtvservicecentre.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8";
$ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
