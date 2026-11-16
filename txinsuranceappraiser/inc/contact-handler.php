<?php
/**
 * POST /contact-submit/ — lead form handler.
 * Emails the lead to SITE['form_to'] and appends a backup row to data/leads.csv
 * (the data/ folder is blocked from the web by .htaccess).
 */
declare(strict_types=1);

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function respond(bool $ok, string $message, bool $json): never
{
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/contact-us/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact-us/', true, 302);
    exit;
}

$f = fn(string $k, int $max = 200) => trim(mb_substr(strip_tags((string) ($_POST[$k] ?? '')), 0, $max));

// Spam traps: honeypot field and a minimum fill time.
if ($f('website') !== '' || (time() - (int) ($_POST['ts'] ?? 0)) < 3) {
    respond(true, 'Thanks! We received your request.', $wantsJson);
}

$data = [
    'first_name' => $f('first_name', 80),
    'last_name'  => $f('last_name', 80),
    'phone'      => $f('phone', 40),
    'email'      => $f('email', 120),
    'city'       => $f('city', 80),
    'loss_type'  => $f('loss_type', 40),
    'message'    => $f('message', 3000),
    'sms_consent'=> ($_POST['sms_consent'] ?? '') === 'yes' ? 'yes' : 'no',
    'source'     => $f('source', 200),
];

if ($data['first_name'] === '' || $data['phone'] === '' || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please add your name, phone number and a valid email address.', $wantsJson);
}
foreach (['first_name', 'last_name', 'email', 'phone'] as $k) {
    if (preg_match('/[\r\n]/', $data[$k])) {
        respond(false, 'Invalid input.', $wantsJson);
    }
}

$when = date('Y-m-d H:i:s');
$ip   = $_SERVER['REMOTE_ADDR'] ?? '';

// Backup copy
$dir = ROOT . '/data';
if (is_writable($dir)) {
    $fh = fopen($dir . '/leads.csv', 'a');
    if ($fh) {
        fputcsv($fh, array_merge([$when, $ip], array_values($data)));
        fclose($fh);
    }
}

$body = "New claim review request from txinsuranceappraiser.com\n\n";
foreach ($data as $k => $v) {
    $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 14) . ' ' . $v . "\n";
}
$body .= "\nSubmitted: $when\nIP: $ip\n";

$headers = [
    'From: ' . SITE['name'] . ' <' . SITE['form_from'] . '>',
    'Reply-To: ' . $data['first_name'] . ' ' . $data['last_name'] . ' <' . $data['email'] . '>',
    'Content-Type: text/plain; charset=UTF-8',
];
$subject = 'Claim review request: ' . $data['first_name'] . ' ' . $data['last_name'] . ($data['city'] ? ' (' . $data['city'] . ')' : '');
@mail(SITE['form_to'], $subject, $body, implode("\r\n", $headers));

respond(true, 'Thank you! Joseph or a team member will contact you shortly — usually the same business day.', $wantsJson);
