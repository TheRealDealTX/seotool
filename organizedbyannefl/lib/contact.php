<?php
// Handles the contact and tips-signup forms (POST /contact-submit, routed by index.php).
// Emails the submission to the business inbox and appends it to a log outside the web
// root so no lead is lost if mail delivery fails.
const OBA_TO = 'info@organizedbyannefl.com';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
function respond($ok, $error = '') {
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json');
        if (!$ok) http_response_code(400);
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } else {
        header('Location: /contact?' . ($ok ? 'sent=1' : 'error=1'), true, 303);
    }
    exit;
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Allow: POST', true, 405); exit; }

function field($k, $max = 200) {
    $v = $_POST[$k] ?? '';
    if (is_array($v)) $v = implode(', ', array_map('strval', $v));
    return trim(mb_substr(str_replace(["\r", "\0"], '', (string)$v), 0, $max));
}

// Bots: filled honeypot or submitted faster than a human could. Pretend success.
$ts = (int)($_POST['ts'] ?? 0);
if (field('website') !== '' || ($ts > 0 && (microtime(true) * 1000 - $ts) < 2500)) respond(true);

$type  = field('type', 20) === 'tips' ? 'tips' : 'contact';
$email = field('email', 254);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) respond(false, 'Please enter a valid email address.');
$data = ['Type' => $type === 'tips' ? 'Tips newsletter signup' : 'Consultation request', 'Email' => $email];
if ($type === 'contact') {
    $data['Name'] = str_replace("\n", ' ', field('name', 120));
    $data['Phone'] = str_replace("\n", ' ', field('phone', 40));
    $data['Neighborhood'] = str_replace("\n", ' ', field('city', 120));
    $data['Spaces'] = field('spaces', 400);
    $data['Consultation'] = field('consult', 60);
    $data['Message'] = field('message', 5000);
    if ($data['Name'] === '' || $data['Message'] === '') respond(false, 'Please add your name and a short message.');
}
$data['Submitted'] = date('c');
$data['IP'] = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '');

$body = '';
foreach ($data as $k => $v) $body .= $k . ': ' . $v . "\n";

$saved = false;
$dir = dirname(__DIR__, 2) . '/oba-submissions';
if (is_dir($dir) || @mkdir($dir, 0700, true)) {
    $saved = @file_put_contents($dir . '/submissions.log', $body . "----\n", FILE_APPEND | LOCK_EX) !== false;
}
$subject = $type === 'tips' ? 'New tips signup: ' . $email : 'New consultation request from ' . $data['Name'];
$headers = "From: Organized by Anne Website <" . OBA_TO . ">\r\nReply-To: " . $email . "\r\nContent-Type: text/plain; charset=utf-8";
$mailed = @mail(OBA_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);

if ($saved || $mailed) respond(true);
respond(false, 'We could not send your message. Please email ' . OBA_TO . ' directly.');
