<?php
// Contact form handler: mails submissions to the journal inbox.
$to = 'info@heathergreenstudios.com';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }

function field($k, $max) {
    $v = trim((string)($_POST[$k] ?? ''));
    return mb_substr(str_replace("\0", '', $v), 0, $max);
}
$name = field('name', 120);
$email = field('email', 200);
$topic = field('topic', 60);
$msg = field('message', 5000);

// Honeypot: bots fill the hidden "website" field. Pretend success.
if (field('website', 200) !== '') { header('Location: /contact/?sent=1', true, 303); exit; }

$ok = $name !== '' && $msg !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)
      && !preg_match('/[\r\n]/', $name . $email . $topic);

if ($ok) {
    $subject = '[heathergreenstudios.com] ' . ($topic ?: 'Message') . ' from ' . $name;
    $body = "Name: $name\nEmail: $email\nTopic: $topic\n\n$msg\n";
    $headers = "From: HGS Studio Journal <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8";
    $ok = mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $to);
}
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
