<?php
// Contact form handler: emails the message to the site inbox.
$to = 'info@live-style.co.uk';
$json = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function done($ok, $msg, $json) {
    if ($json) {
        header('Content-Type: application/json');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'message' => $msg]);
    } else {
        header('Location: /contact/?' . ($ok ? 'sent=1' : 'error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: /contact/', true, 303); exit; }
if (!empty($_POST['website'])) done(true, 'Thanks, your message has been sent.', $json);   // honeypot

$name  = trim(substr(str_replace(["\r", "\n"], ' ', $_POST['name'] ?? ''), 0, 100));
$email = trim($_POST['email'] ?? '');
$msg   = trim(substr($_POST['message'] ?? '', 0, 5000));
if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    done(false, 'Please fill in your name, a valid email address and a message.', $json);
}

$headers = "From: Live-Style website <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";
$ok = mail($to, "Live-Style contact form: $name", "Name: $name\nEmail: $email\n\n$msg\n", $headers);
done($ok, $ok ? 'Thanks, your message has been sent. We will be in touch soon.'
              : 'Sorry, something went wrong. Please email ' . $to . ' directly.', $json);
