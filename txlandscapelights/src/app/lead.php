<?php
// Texas Landscape Lights - quote / popup form handler.
// Emails every submission to info@txlandscapelights.com and appends a copy to
// leads.csv one level above public_html (not web-reachable), so no lead is lost
// while the mailbox is being set up. Answers JSON for fetch() and redirects to
// /thank-you/ for plain form posts.

const TO = 'info@txlandscapelights.com';
const FROM = 'noreply@txlandscapelights.com';
const SITE = 'Texas Landscape Lights';

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function done(bool $ok, string $error = ''): void {
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        if (!$ok) http_response_code(400);
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/quote/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /quote/', true, 303);
    exit;
}

$f = static fn(string $k, int $max = 200): string =>
    trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max));

// Spam traps: hidden honeypot field, and posts sent faster than a human could type.
if ($f('website') !== '') done(true);
$t = (int)$f('t', 20);
if ($t > 0 && (microtime(true) * 1000 - $t) < 2500) done(true);

$lead = [
    'name'    => $f('name', 120),
    'phone'   => $f('phone', 40),
    'email'   => $f('email', 160),
    'city'    => $f('city', 120),
    'project' => $f('project', 120),
    'time'    => $f('time', 40),
    'message' => $f('message', 4000),
    'form'    => $f('form', 40),
    'page'    => $f('source', 300),
];

if ($lead['name'] === '' || $lead['phone'] === '' || $lead['email'] === '') {
    done(false, 'Please add your name, phone and email.');
}
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    done(false, 'Please check your email address.');
}
if (preg_match_all('#https?://#i', $lead['message']) > 2) done(true);

$when = (new DateTime('now', new DateTimeZone('America/Chicago')))->format('Y-m-d H:i:s T');
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);

// Backup copy outside the web root.
$saved = false;
$dir = dirname(__DIR__, 2) . '/leads';
if (!is_dir($dir)) @mkdir($dir, 0700, true);
if (is_dir($dir) && ($fh = @fopen($dir . '/leads.csv', 'a'))) {
    if (flock($fh, LOCK_EX)) {
        if (fstat($fh)['size'] === 0) fputcsv($fh, array_merge(['received'], array_keys($lead), ['ip']), ',', '"', '\\');
        $saved = fputcsv($fh, array_merge([$when], array_values($lead), [$ip]), ',', '"', '\\') !== false;
        flock($fh, LOCK_UN);
    }
    fclose($fh);
}

$labels = [
    'name' => 'Name', 'phone' => 'Phone', 'email' => 'Email', 'city' => 'City / area',
    'project' => 'Project type', 'time' => 'Best time to call', 'message' => 'Project details',
    'form' => 'Form', 'page' => 'Sent from page',
];
$lines = ["New lighting request from txlandscapelights.com", str_repeat('-', 46)];
foreach ($labels as $k => $label) {
    if ($lead[$k] !== '') $lines[] = $label . ': ' . $lead[$k];
}
$lines[] = 'Received: ' . $when;
$lines[] = 'IP: ' . $ip;

$clean = static fn(string $s): string => preg_replace('/[\r\n]+/', ' ', $s);
$subject = 'New lighting request: ' . $clean($lead['name']) . ($lead['city'] !== '' ? ' (' . $clean($lead['city']) . ')' : '');
$headers = implode("\r\n", [
    'From: ' . SITE . ' <' . FROM . '>',
    'Reply-To: ' . $clean($lead['name']) . ' <' . $clean($lead['email']) . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP',
]);

$sent = @mail(TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', implode("\n", $lines), $headers, '-f' . FROM);

// Either copy is enough: a mail hiccup still counts as received when the CSV holds the lead.
if (!$sent && !$saved) done(false, 'We could not send your request just now.');
done(true);
