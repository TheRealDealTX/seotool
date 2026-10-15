<?php
// Free case review submissions (hurricaneflood.com) for The Lawgical Firm, P.A.
// Each lead is appended to ../data/leads.php (its first line exits, so the file
// returns 404 on the web; download it from hPanel File Manager). If
// ../data/lead-config.php exists on the server (never committed), each lead is
// also emailed. That file must start with the guard line:
//   <?php if (!defined('HF_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@hurricaneflood.com'];
require __DIR__ . '/_lib.php';
define('HF_LEAD', true);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    hf_json(['ok' => false, 'error' => 'POST only'], 405);
}
hf_rate_limit('lead', 6, 600);

$clean = fn(string $k, int $max) => trim(mb_substr(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string) ($_POST[$k] ?? '')), 0, $max));
if ($clean('website', 100) !== '') {           // honeypot: pretend success
    hf_json(['ok' => true, 'name' => 'there']);
}
$lead = [
    'received_utc' => gmdate('c'),
    'name'        => $clean('name', 100),
    'phone'       => $clean('phone', 30),
    'email'       => strtolower($clean('email', 160)),
    'location'    => $clean('location', 100),
    'claim_type'  => $clean('claim_type', 100),
    'message'     => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000)),
    'consent'     => !empty($_POST['consent']) ? 'yes' : 'no',
    'page'        => $clean('page', 200),
    'ip'          => trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]),
];
$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    hf_json(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 400);
}
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    hf_json(['ok' => false, 'error' => 'Please enter a valid email address.'], 400);
}
if ($lead['location'] === '') {
    hf_json(['ok' => false, 'error' => 'Please enter the property city or ZIP code.'], 400);
}
if ($lead['consent'] !== 'yes') {
    hf_json(['ok' => false, 'error' => 'Please check the acknowledgment box.'], 400);
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
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@hurricaneflood.com';
        $body = "New free case review request from hurricaneflood.com\n\n";
        foreach ($lead as $k => $v) {
            $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 15) . ($k === 'message' ? "\n" : ' ') . $v . "\n";
        }
        $headers = "From: HurricaneFlood.com <$from>\r\nContent-Type: text/plain; charset=UTF-8\r\nReply-To: " . $lead['email'];
        $subject = '=?UTF-8?B?' . base64_encode('Hurricane flood lead: ' . $lead['name'] . ' (' . $lead['claim_type'] . ')') . '?=';
        $mailed = @mail(implode(',', $to), $subject, $body, $headers);
    }
}
if ($saved === false && !$mailed) {
    hf_json(['ok' => false, 'error' => 'We could not save your request. Please call (407) 433-4131.'], 500);
}
hf_json(['ok' => true, 'name' => explode(' ', $lead['name'])[0]]);
