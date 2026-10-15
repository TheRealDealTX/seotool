<?php
// Free case review requests for The Lawgical Firm, P.A. from deniedtheclaim.com.
// Each lead is appended to ../data/leads.php (its first line exits, so the file
// 404s on the web; download it from hPanel File Manager). If
// ../data/lead-config.php exists on the server (never commit it), each lead is
// also emailed:
//   <?php if (!defined('DTC_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@deniedtheclaim.com'];
require __DIR__ . '/_lib.php';
define('DTC_LEAD', true);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    dtc_json(['ok' => false, 'error' => 'POST only'], 405);
}
dtc_rate_limit('lead', 6, 600);

$clean = fn($k, $max) => trim(mb_substr(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string) ($_POST[$k] ?? '')), 0, $max));
if ($clean('website', 100) !== '') {          // honeypot filled: pretend success
    dtc_json(['ok' => true, 'name' => 'there']);
}
$lead = [
    'received_utc' => gmdate('c'),
    'name' => $clean('name', 100),
    'phone' => $clean('phone', 30),
    'email' => strtolower($clean('email', 160)),
    'location' => $clean('location', 100),
    'claim_type' => $clean('claim_type', 80),
    'status' => $clean('status', 80),
    'message' => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000)),
    'consent' => !empty($_POST['consent']) ? 'yes' : 'no',
    'page' => $clean('page', 200),
    'ip' => trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]),
];
$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    dtc_json(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 400);
}
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    dtc_json(['ok' => false, 'error' => 'Please check your email address.'], 400);
}
if ($lead['location'] === '') {
    dtc_json(['ok' => false, 'error' => 'Please enter the property city or ZIP code.'], 400);
}
if ($lead['consent'] !== 'yes') {
    dtc_json(['ok' => false, 'error' => 'Please check the acknowledgment box before sending.'], 400);
}

$dir = __DIR__ . '/../data';
@mkdir($dir, 0700, true);
$file = $dir . '/leads.php';
$csv = fn(array $row) => implode(',', array_map(fn($v) => '"' . str_replace('"', '""', (string) $v) . '"', $row)) . "\n";
$new = !is_file($file);
$saved = @file_put_contents($file, ($new ? "<?php http_response_code(404); exit; ?>\n" . $csv(array_keys($lead)) : '') . $csv(array_values($lead)), FILE_APPEND | LOCK_EX);

$mailed = false;
$cfgFile = $dir . '/lead-config.php';
if (is_file($cfgFile)) {
    $cfg = include $cfgFile;
    $to = array_filter((array) ($cfg['to'] ?? []), fn($e) => filter_var($e, FILTER_VALIDATE_EMAIL));
    if ($to) {
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@deniedtheclaim.com';
        $body = "New free case review request from deniedtheclaim.com\n\n";
        foreach ($lead as $k => $v) {
            $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 16) . ($k === 'message' ? "\n" : ' ') . $v . "\n";
        }
        $headers = "From: Denied the Claim <$from>\r\nContent-Type: text/plain; charset=UTF-8\r\nReply-To: " . $lead['email'];
        $subject = '=?UTF-8?B?' . base64_encode('Denied claim lead: ' . $lead['name'] . ' (' . $lead['claim_type'] . ')') . '?=';
        $mailed = @mail(implode(',', $to), $subject, $body, $headers);
    }
}
if ($saved === false && !$mailed) {
    dtc_json(['ok' => false, 'error' => 'We could not save your request. Please call (407) 433-4131.'], 500);
}
dtc_json(['ok' => true, 'name' => explode(' ', $lead['name'])[0]]);
