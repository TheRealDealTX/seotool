<?php
require __DIR__ . '/lib.php';
cd_post_only();
if (!cd_rate_limit('contact', 5, 3600)) cd_json(['ok' => false, 'error' => 'Too many messages — please try again later.'], 429);
$name = trim(substr($_POST['name'] ?? '', 0, 100));
$email = trim(substr($_POST['email'] ?? '', 0, 150));
$topic = trim(substr($_POST['topic'] ?? '', 0, 60));
$msg = trim(substr($_POST['message'] ?? '', 0, 5000));
if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    cd_json(['ok' => false, 'error' => 'Please fill in your name, a valid email and a message.'], 422);
}
$rec = ['time' => date('c'), 'name' => $name, 'email' => $email, 'topic' => $topic, 'message' => $msg];
cd_append_private('contact-messages', json_encode($rec, JSON_UNESCAPED_UNICODE) . "\n");
$cfg = cd_config();
if (!empty($cfg['notify_email'])) {
    $safe = fn($s) => str_replace(["\r", "\n"], ' ', $s);
    @mail($cfg['notify_email'], '[cebudavao.com] ' . $safe($topic) . ' from ' . $safe($name),
          "From: $name <$email>\nTopic: $topic\n\n$msg", 'Reply-To: ' . $safe($email));
}
cd_json(['ok' => true, 'message' => 'Salamat! Your message has been sent.']);
