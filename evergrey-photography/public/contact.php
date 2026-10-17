<?php
// Inquiry form handler: validates the POST from /contact and emails it to the studio.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

const TO = 'info@evergrey-photography.com';

function out($ok, $error = '') {
    echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    out(false, 'Please use the form on the contact page.');
}

$f = function ($k, $max = 200) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
};

// Spam traps: hidden field must be empty; form must take more than 3 seconds.
if ($f('website') !== '') out(true);
$ts = (int)$f('ts', 20);
if ($ts > 0 && (microtime(true) * 1000 - $ts) < 3000) out(true);

$name = $f('name', 120);
$email = $f('email', 160);
$message = $f('message', 5000);
if ($name === '' || $message === '') out(false, 'Please add your name and a short message.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(false, 'That email address doesn’t look right.');

$rows = [
    'Name' => $name, 'Partner' => $f('partner', 120), 'Email' => $email, 'Phone' => $f('phone', 40),
    'Planning' => $f('type', 40), 'Date' => $f('date', 60), 'Location' => $f('location', 200), 'Found us via' => $f('heard', 200),
];
$body = '';
foreach ($rows as $k => $v) if ($v !== '') $body .= str_pad($k . ':', 14) . $v . "\n";
$body .= "\n" . str_replace("\n", "\r\n", $message) . "\n\n--\nSent from the inquiry form at " . ($_SERVER['HTTP_HOST'] ?? '') . "\n";

$safeName = preg_replace('/[^\p{L}\p{N} .\'-]/u', '', $name);
$subject = 'New inquiry: ' . $safeName . ($rows['Date'] ? ' — ' . preg_replace('/[^\p{L}\p{N} ,.\/-]/u', '', $rows['Date']) : '');
$headers = [
    'From: Evergrey Photography <' . TO . '>',
    'Reply-To: ' . $safeName . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
];

$sent = @mail(TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
if (!$sent) out(false, 'Our mail server didn’t accept the message.');
out(true);
