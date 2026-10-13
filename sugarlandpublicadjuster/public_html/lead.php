<?php
/**
 * Lead form handler. Every form on the site posts here.
 * Emails the lead to SITE['lead_to'] and keeps a CSV copy outside the web root
 * so no lead is lost if mail delivery fails.
 */
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/mailer.php';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $error = ''): void
{
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        if (!$ok) {
            http_response_code(422);
        }
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/contact/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact/', true, 303);
    exit;
}

function field(string $k, int $max = 200): string
{
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v);
    return mb_substr($v, 0, $max);
}

// Spam checks: honeypot filled, or submitted faster than a human could.
$ts = (int) ($_POST['ts'] ?? 0);
if (field('website') !== '' || ($ts && time() - $ts < 3)) {
    respond(true); // pretend success so bots learn nothing
}

$lead = [
    'name'    => field('name', 100),
    'phone'   => field('phone', 40),
    'email'   => field('email', 150),
    'damage'  => field('damage', 60),
    'address' => field('address', 200),
    'status'  => field('status', 80),
    'message' => field('message', 3000),
    'source'  => field('source', 40),
    'page'    => field('page', 200),
];

if ($lead['name'] === '' || strlen(preg_replace('/\D/', '', $lead['phone'])) < 10) {
    respond(false, 'Please enter your name and a valid phone number.');
}
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please enter a valid email address (or leave it blank).');
}
if (preg_match_all('#https?://#i', $lead['message']) > 2) {
    respond(false, 'Please remove links from your message, or call (832) 503-5866.');
}

$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);
$when = (new DateTime('now', new DateTimeZone('America/Chicago')))->format('Y-m-d g:i A T');

// Keep a private copy (outside public_html).
$dir = dirname(__DIR__) . '/slpa-leads';
if (!is_dir($dir)) {
    @mkdir($dir, 0700, true);
}
$csv = $dir . '/leads.csv';
$new = !is_file($csv);
if ($fh = @fopen($csv, 'a')) {
    if ($new) {
        fputcsv($fh, array_merge(['received'], array_keys($lead), ['ip']));
    }
    fputcsv($fh, array_merge([$when], array_values($lead), [$ip]));
    fclose($fh);
}

$subject = 'New claim review request: ' . $lead['name'] . ($lead['damage'] ? ' (' . $lead['damage'] . ')' : '');
$lines = [
    'New lead from sugarlandpublicadjuster.com',
    '',
    'Name:          ' . $lead['name'],
    'Phone:         ' . $lead['phone'],
    'Email:         ' . ($lead['email'] ?: '—'),
    'Damage type:   ' . ($lead['damage'] ?: '—'),
    'Address/ZIP:   ' . ($lead['address'] ?: '—'),
    'Claim status:  ' . ($lead['status'] ?: '—'),
    '',
    'What happened:',
    $lead['message'] ?: '—',
    '',
    '---',
    'Form:      ' . $lead['source'],
    'Page:      ' . SITE['origin'] . $lead['page'],
    'Received:  ' . $when,
    'IP:        ' . $ip,
];
$bodyText = implode("\r\n", $lines);

[$sent, $method, $mailErr] = send_mail(SITE['lead_to'], $subject, $bodyText, $lead['email'], $lead['name']);

if ($fh = @fopen($dir . '/mail.log', 'a')) {
    fwrite($fh, $when . ' ' . ($sent ? 'sent' : 'FAILED') . ' via ' . $method . ($mailErr ? ' (smtp error: ' . $mailErr . ')' : '') . ' ' . $lead['name'] . ' ' . $lead['phone'] . "\n");
    fclose($fh);
}

// The lead is saved either way; tell the visitor it went through.
respond(true);
