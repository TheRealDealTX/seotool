<?php
// Contact form handler: emails the message to info@comeicavoliamerenda.com.
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
function field($k, $max) { return trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max)); }
$name = field('name', 100); $email = field('email', 200); $topic = field('topic', 60);
$message = field('message', 5000); $trap = field('website', 200);
if ($trap !== '') { header('Location: /contact/?sent=1', true, 303); exit; }   // bot
$ok = $name !== '' && $message !== '' && filter_var($email, FILTER_VALIDATE_EMAIL);
if ($ok) {
    $clean = function ($s) { return str_replace(["\r", "\n"], ' ', $s); };
    $to = 'info@comeicavoliamerenda.com';
    $subject = 'Website message: ' . $clean($topic ?: 'Contact');
    $body = "Name: {$clean($name)}\nEmail: {$clean($email)}\nTopic: {$clean($topic)}\n\n{$message}\n";
    $headers = "From: Come i Cavoli a Merenda <info@comeicavoliamerenda.com>\r\n"
             . 'Reply-To: ' . $clean($email) . "\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    $ok = @mail($to, $subject, $body, $headers);
}
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
