<?php
// zibetti.co - inquiry form handler. Sends the form to info@zibetti.co.
$to = 'info@zibetti.co';

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Location: /contact-us/', true, 303);
    exit;
}
// Honeypot: bots fill the hidden "website" field. Pretend success.
if (!empty($_POST['website'])) {
    header('Location: /contact-us/?sent=1', true, 303);
    exit;
}

function field($k, $max = 200) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr($v, 0, $max);
}

$name = field('name');
$email = field('email');
$date = field('date');
$location = field('location');
$type = field('type');
$services = isset($_POST['services']) && is_array($_POST['services']) ? implode(', ', array_map('strval', array_slice($_POST['services'], 0, 5))) : '';
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: /contact-us/?sent=0', true, 303);
    exit;
}

$body = "New inquiry from zibetti.co\n\n"
    . "Names: $name\nEmail: $email\nDate: $date\nLocation: $location\nPlanning: $type\nInterested in: $services\n\n"
    . "Message:\n$message\n";
$headers = [
    'From: Zibetti Website <' . $to . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
];
$ok = @mail($to, 'New inquiry: ' . $name . ($date ? " ($date)" : ''), $body, implode("\r\n", $headers));
header('Location: /contact-us/?sent=' . ($ok ? '1' : '0'), true, 303);
