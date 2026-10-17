<?php
// Contact + newsletter form handler. Emails submissions to info@shopvipgifts.com.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

$to = 'info@shopvipgifts.com';

function done($ok, $err = null, $code = 200) {
    http_response_code($code);
    echo json_encode($err ? ['ok' => $ok, 'error' => $err] : ['ok' => $ok]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    done(false, 'method', 405);
}
// Honeypot: bots fill the hidden "website" field. Pretend success.
if (!empty($_POST['website'])) {
    done(true);
}

$clean = function ($v, $max) {
    $v = trim((string)$v);
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);
    return mb_substr($v, 0, $max);
};
$form    = $_POST['form'] ?? 'contact';
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$name    = $clean($_POST['name'] ?? '', 100);
$topic   = $clean($_POST['topic'] ?? '', 100);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);

if (!$email) {
    done(false, 'email', 422);
}
if ($form === 'contact' && ($name === '' || $message === '')) {
    done(false, 'fields', 422);
}

$subject = $form === 'newsletter'
    ? 'New VIP list signup: ' . $email
    : 'Website enquiry' . ($topic ? " ($topic)" : '') . ' from ' . $name;
$body = $form === 'newsletter'
    ? "New newsletter signup\n\nEmail: $email\n"
    : "Name: $name\nEmail: $email\nTopic: $topic\n\n$message\n";
$body .= "\n--\nSent from shopvipgifts.com on " . gmdate('Y-m-d H:i') . " UTC\n";

$headers = [
    'From: Shop VIP Gifts <' . $to . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=utf-8',
];
$sent = @mail($to, $subject, $body, implode("\r\n", $headers));
done((bool)$sent, $sent ? null : 'send', $sent ? 200 : 500);
