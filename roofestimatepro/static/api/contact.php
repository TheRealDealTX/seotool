<?php
// Roof Estimate Pro — form handler for /get-estimate/, /claim/, /get-a-scope/
// and the contact forms. Emails the submission (with attachments) to the
// office inbox and answers the page's fetch() with JSON.
//
// Configuration lives in the constants below. To collect the claim-review or
// scope fee online, paste a Stripe Payment Link into the matching constant;
// the visitor is sent there after a successful submission.

const TO_EMAIL      = 'contact@roofestimatepro.com';
const FROM_EMAIL    = 'no-reply@roofestimatepro.com';
const STRIPE_CLAIM  = '';   // e.g. https://buy.stripe.com/xxxx  ($50 claim estimate review)
const STRIPE_SCOPE  = '';   // e.g. https://buy.stripe.com/yyyy  ($200 scope of damages)
const MAX_BYTES     = 20 * 1024 * 1024;
const ALLOWED_EXT   = ['jpg', 'jpeg', 'png', 'webp', 'heic', 'gif', 'pdf', 'esx', 'xlsx', 'xls', 'csv', 'doc', 'docx', 'zip', 'txt'];

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function reply($ok, $extra = []) {
    http_response_code($ok ? 200 : 400);
    echo json_encode(array_merge(['ok' => $ok], $extra));
    exit;
}
function clean($v, $max = 5000) {
    $v = is_string($v) ? trim($v) : '';
    $v = str_replace("\0", '', $v);
    return mb_substr($v, 0, $max);
}
function header_safe($v) { return preg_replace('/[\r\n]+/', ' ', $v); }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') reply(false, ['error' => 'POST only.']);

// Spam checks: honeypot field, minimum fill time, simple per-IP rate limit.
if (clean($_POST['website'] ?? '') !== '') reply(true, ['message' => 'Thanks!']);
$ts = (int) ($_POST['ts'] ?? 0);
if ($ts > 0 && (microtime(true) * 1000 - $ts) < 2500) reply(false, ['error' => 'That was quick — please try again.']);

$private = dirname($_SERVER['DOCUMENT_ROOT'] ?? __DIR__) . '/rep-private';
if (!is_dir($private)) @mkdir($private, 0700, true);
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$ip = trim(explode(',', $ip)[0]);
if (is_dir($private) && is_writable($private)) {
    $rl = $private . '/rl-' . md5($ip) . '.json';
    $hits = is_file($rl) ? (json_decode((string) @file_get_contents($rl), true) ?: []) : [];
    $hits = array_values(array_filter($hits, function ($t) { return $t > time() - 3600; }));
    if (count($hits) >= 8) reply(false, ['error' => 'Too many requests from this connection.']);
    $hits[] = time();
    @file_put_contents($rl, json_encode($hits));
}

$type  = clean($_POST['form_type'] ?? 'estimate', 30);
$name  = clean($_POST['name'] ?? '', 120);
$email = clean($_POST['email'] ?? '', 200);
$phone = clean($_POST['phone'] ?? '', 40);
if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) reply(false, ['error' => 'Please enter your name and a valid email.']);

$labels = [
    'estimate' => 'Estimate request',
    'claim'    => 'Claim estimate review',
    'scope'    => 'Scope of damages order',
    'contact'  => 'Contact message',
];
$subjectType = $labels[$type] ?? 'Website request';

// Every posted field goes into the email, in form order.
$skip = ['website', 'ts', 'form_type'];
$lines = [];
foreach ($_POST as $k => $v) {
    if (in_array($k, $skip, true)) continue;
    if (is_array($v)) $v = implode(', ', array_map('clean', $v));
    $v = clean($v);
    if ($v === '') continue;
    $lines[] = ucwords(str_replace('_', ' ', $k)) . ': ' . $v;
}
$lines[] = '';
$lines[] = 'Page: ' . clean($_SERVER['HTTP_REFERER'] ?? '', 300);
$lines[] = 'IP: ' . $ip;
$lines[] = 'Time: ' . gmdate('Y-m-d H:i:s') . ' UTC';
$body = implode("\n", $lines);

// Attachments
$files = [];
$bytes = 0;
foreach ($_FILES as $field) {
    $names = is_array($field['name']) ? $field['name'] : [$field['name']];
    $tmps  = is_array($field['tmp_name']) ? $field['tmp_name'] : [$field['tmp_name']];
    $errs  = is_array($field['error']) ? $field['error'] : [$field['error']];
    $sizes = is_array($field['size']) ? $field['size'] : [$field['size']];
    foreach ($names as $i => $fn) {
        if ($errs[$i] === UPLOAD_ERR_NO_FILE || $fn === '') continue;
        if ($errs[$i] !== UPLOAD_ERR_OK) reply(false, ['error' => 'An attachment failed to upload.']);
        $ext = strtolower(pathinfo($fn, PATHINFO_EXTENSION));
        if (!in_array($ext, ALLOWED_EXT, true)) reply(false, ['error' => "Files of type .$ext can't be attached."]);
        $bytes += (int) $sizes[$i];
        if ($bytes > MAX_BYTES) reply(false, ['error' => 'Attachments are over 20 MB in total.']);
        $files[] = ['name' => preg_replace('/[^A-Za-z0-9._ -]/', '_', $fn), 'path' => $tmps[$i]];
    }
}

$subject = header_safe("[Roof Estimate Pro] $subjectType — $name");
$boundary = 'rep_' . bin2hex(random_bytes(12));
$headers = [
    'From: Roof Estimate Pro <' . FROM_EMAIL . '>',
    'Reply-To: ' . header_safe("$name <$email>"),
    'MIME-Version: 1.0',
    "Content-Type: multipart/mixed; boundary=\"$boundary\"",
];
$msg  = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n$body\r\n";
foreach ($files as $f) {
    $data = chunk_split(base64_encode((string) file_get_contents($f['path'])));
    $msg .= "--$boundary\r\nContent-Type: application/octet-stream; name=\"{$f['name']}\"\r\n"
          . "Content-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$f['name']}\"\r\n\r\n$data\r\n";
}
$msg .= "--$boundary--";

$sent = @mail(TO_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $msg, implode("\r\n", $headers), '-f' . FROM_EMAIL);

// Keep a copy of the text so nothing is lost if mail delivery fails.
if (is_dir($private) && is_writable($private)) {
    @file_put_contents($private . '/submissions.log', "==== $subject\n$body\nFiles: " . implode(', ', array_column($files, 'name')) . "\nMail sent: " . ($sent ? 'yes' : 'NO') . "\n\n", FILE_APPEND | LOCK_EX);
}
if (!$sent) reply(false, ['error' => 'Our mail server did not accept the message.']);

$redirect = '';
if ($type === 'claim' && STRIPE_CLAIM !== '') $redirect = STRIPE_CLAIM . '?prefilled_email=' . rawurlencode($email);
if ($type === 'scope' && STRIPE_SCOPE !== '') $redirect = STRIPE_SCOPE . '?prefilled_email=' . rawurlencode($email);

$message = [
    'claim' => 'Got it — your claim details are in. We will confirm the review and send a secure payment link shortly.',
    'scope' => 'Got it — your scope order is in. We will confirm the details and send a secure payment link shortly.',
][$type] ?? 'Thanks — your request is in. An estimator will be in touch shortly by email or phone.';
if ($redirect !== '') $message = 'Thanks — taking you to secure checkout…';

reply(true, ['message' => $message, 'redirect' => $redirect]);
