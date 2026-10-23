<?php
// Contact form handler for /contact-us/.
// Messages are appended to a CSV outside the web root (never inside it: the host ignores .htaccess). If a config file
// exists there returning ['to' => 'you@example.com'], each message is also emailed.
//   <home>/dogearcleaner-private/config.php   (create it on the server; never commit it)
//   <home>/dogearcleaner-private/messages.csv (created automatically)
$back = '/contact-us/';
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: ' . $back, true, 303); exit; }

function field($k, $max) { return trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max)); }
$first = field('first_name', 80); $last = field('last_name', 80); $email = field('email', 160);
$topic = field('topic', 60); $msg = field('message', 5000);

if (field('website', 200) !== '') { header('Location: ' . $back . '?sent=1', true, 303); exit; } // honeypot
if ($first === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: ' . $back . '?error=invalid', true, 303); exit;
}

$dir = dirname(__DIR__) . '/dogearcleaner-private';
if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
if (!is_dir($dir) || !is_writable($dir)) { $dir = null; }   // never fall back to a folder inside the web root

// Basic flood control: max 5 messages per IP per hour.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '');
$ip = trim(explode(',', $ip)[0]);
if ($dir) {
    $rl = $dir . '/rate-' . md5($ip) . '.txt';
    $hits = array_filter(array_map('intval', @file($rl, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600);
    if (count($hits) >= 5) { header('Location: ' . $back . '?error=rate', true, 303); exit; }
    $hits[] = time(); @file_put_contents($rl, implode("\n", $hits));
}

$row = [date('c'), $first, $last, $email, $topic, $msg, $ip];
$ok = false;
if ($dir && ($fh = @fopen($dir . '/messages.csv', 'a'))) { $ok = fputcsv($fh, $row) !== false; fclose($fh); }

$cfg = is_file(dirname(__DIR__) . '/dogearcleaner-private/config.php') ? include dirname(__DIR__) . '/dogearcleaner-private/config.php' : [];
if (!empty($cfg['to'])) {
    $subject = '[Dog Ear Cleaner] ' . ($topic ?: 'Contact form') . ' - ' . $first;
    $body = "From: $first $last <$email>\nTopic: $topic\n\n$msg\n";
    $sent = @mail($cfg['to'], $subject, $body, "From: Dog Ear Cleaner <no-reply@dogearcleaner.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8");
    $ok = $ok || $sent;
}
header('Location: ' . $back . ($ok ? '?sent=1' : '?error=save'), true, 303);
