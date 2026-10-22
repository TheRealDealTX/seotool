<?php
// Contact form handler. Messages are always appended to data/messages.php (which starts
// with an exit() line, so it cannot be read over the web even though .htaccess is ignored
// on this host) and also emailed when CONTACT_TO is set in inc/config.php.

function contact_handle(): ?string
{
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
        return isset($_GET['sent']) ? 'sent' : null;
    }
    $f = fn($k, $n) => trim(mb_substr(str_replace(["\r", "\0"], '', (string) ($_POST[$k] ?? '')), 0, $n));
    $name = $f('name', 100);
    $email = $f('email', 150);
    $topic = $f('topic', 60);
    $msg = $f('message', 5000);
    // Honeypot and a minimum fill time quietly drop most bots.
    if ($f('website', 100) !== '' || time() - (int) ($_POST['t'] ?? 0) < 3) {
        redirect('/contact/?sent=1', 303);
    }
    if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return 'error';
    }
    $line = json_encode(['at' => date('c'), 'ip' => $_SERVER['REMOTE_ADDR'] ?? '', 'name' => $name, 'email' => $email, 'topic' => $topic, 'message' => $msg], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $file = ROOT . '/data/messages.php';
    if (!is_file($file)) {
        @file_put_contents($file, "<?php exit; ?>\n");
    }
    @file_put_contents($file, $line . "\n", FILE_APPEND | LOCK_EX);
    if (CONTACT_TO !== '') {
        $name1 = preg_replace('/[^\p{L}\p{N} .\'-]/u', '', $name);
        @mail(CONTACT_TO, '[Under Desk Elliptical] ' . $topic . ' from ' . $name1, $msg . "\n\n-- \n$name1 <$email>",
            "From: " . SITE_NAME . " <noreply@" . SITE_HOST . ">\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8");
    }
    redirect('/contact/?sent=1', 303);
}
