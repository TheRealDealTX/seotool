<?php
// Free case review requests from floridahomelaw.com for The Lawgical Firm, P.A.
// Each request is appended to ../data/leads.php (its first line exits, and
// .htaccess 404s /data/, so it is never served; download it from hPanel File
// Manager). If ../data/lead-config.php exists on the server, each request is
// also emailed. Create that file on the server only, never commit it:
//   <?php if (!defined('FHL_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@floridahomelaw.com'];
require __DIR__ . '/_lib.php';
define('FHL_LEAD', true);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fhl_json(['ok' => false, 'error' => 'POST only'], 405);
}
fhl_throttle('lead', 5, 600);

$f = fn(string $k, int $max) => trim(mb_substr(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string) ($_POST[$k] ?? '')), 0, $max));
if ($f('website', 100) !== '') {           // honeypot filled in: act normal, store nothing
    fhl_json(['ok' => true, 'name' => 'there']);
}
$lead = [
    'received_utc' => gmdate('c'),
    'name'       => $f('name', 100),
    'phone'      => $f('phone', 30),
    'email'      => strtolower($f('email', 160)),
    'location'   => $f('location', 100),
    'claim_type' => $f('claim_type', 80),
    'status'     => $f('status', 80),
    'message'    => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000)),
    'consent'    => !empty($_POST['consent']) ? 'yes' : 'no',
    'page'       => $f('page', 200),
    'ip'         => trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]),
];
$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    fhl_json(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 400);
}
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    fhl_json(['ok' => false, 'error' => 'Please enter a valid email address.'], 400);
}
if ($lead['location'] === '' || $lead['claim_type'] === '') {
    fhl_json(['ok' => false, 'error' => 'Please add the property city or ZIP and the type of claim.'], 400);
}
if ($lead['consent'] !== 'yes') {
    fhl_json(['ok' => false, 'error' => 'Please tick the acknowledgment box before sending.'], 400);
}

$dir = __DIR__ . '/../data';
@mkdir($dir, 0700, true);
$file = $dir . '/leads.php';
$csv = fn(array $row) => implode(',', array_map(fn($v) => '"' . str_replace('"', '""', (string) $v) . '"', $row)) . "\n";
$first = !is_file($file);
$saved = @file_put_contents($file, ($first ? "<?php http_response_code(404); exit; ?>\n" . $csv(array_keys($lead)) : '') . $csv(array_values($lead)), FILE_APPEND | LOCK_EX);

$mailed = false;
$cfgFile = $dir . '/lead-config.php';
if (is_file($cfgFile)) {
    $cfg = include $cfgFile;
    $to = array_filter((array) ($cfg['to'] ?? []), fn($e) => filter_var($e, FILTER_VALIDATE_EMAIL));
    if ($to) {
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@floridahomelaw.com';
        $body = "New free case review request from floridahomelaw.com\n\n";
        foreach ($lead as $k => $v) {
            $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 15) . ($k === 'message' ? "\n" : ' ') . $v . "\n";
        }
        $headers = "From: Florida Home Law <$from>\r\nReply-To: {$lead['email']}\r\nContent-Type: text/plain; charset=UTF-8";
        $subject = '=?UTF-8?B?' . base64_encode('Florida Home Law lead: ' . $lead['name'] . ' (' . $lead['claim_type'] . ')') . '?=';
        $mailed = @mail(implode(',', $to), $subject, $body, $headers);
    }
}
if ($saved === false && !$mailed) {
    fhl_json(['ok' => false, 'error' => 'We could not save your request. Please call (407) 433-4131.'], 500);
}
fhl_json(['ok' => true, 'name' => explode(' ', $lead['name'])[0]]);
