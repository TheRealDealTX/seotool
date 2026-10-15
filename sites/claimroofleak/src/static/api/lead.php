<?php
// Free case review requests from claimroofleak.com for The Lawgical Firm, P.A.
//
// Each request is appended to ../data/leads.php (its first line exits, so the
// file returns 404 on the web; download it from hPanel File Manager). If the
// server has ../data/lead-config.php (never committed), each request is also
// emailed. That file must start with the guard line:
//   <?php if (!defined('CRL_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@claimroofleak.com'];
require __DIR__ . '/_lib.php';
define('CRL_LEAD', true);

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    crl_reply(['ok' => false, 'error' => 'Method not allowed'], 405);
}
crl_throttle('lead', 5, 900);

if (crl_field('website', 200) !== '') {          // honeypot filled: act normal, store nothing
    crl_reply(['ok' => true, 'first' => 'there']);
}

$lead = [
    'received_utc' => gmdate('c'),
    'name'         => crl_field('name', 100),
    'phone'        => crl_field('phone', 30),
    'email'        => strtolower(crl_field('email', 160)),
    'location'     => crl_field('location', 100),
    'claim_type'   => crl_field('claim_type', 80),
    'message'      => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000)),
    'consent'      => !empty($_POST['consent']) ? 'yes' : 'no',
    'page'         => crl_field('page', 200),
    'ip'           => crl_client_ip(),
];

$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    crl_reply(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 422);
}
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    crl_reply(['ok' => false, 'error' => 'Please enter a valid email address.'], 422);
}
if ($lead['location'] === '') {
    crl_reply(['ok' => false, 'error' => 'Please enter the property city or ZIP code.'], 422);
}
if ($lead['consent'] !== 'yes') {
    crl_reply(['ok' => false, 'error' => 'Please check the consent box so the firm can contact you.'], 422);
}

$dataDir = dirname(__DIR__) . '/data';
if (!is_dir($dataDir)) {
    @mkdir($dataDir, 0700, true);
}
$store = $dataDir . '/leads.php';
$row = fn(array $r) => implode(',', array_map(fn($v) => '"' . str_replace('"', '""', (string) $v) . '"', $r)) . "\n";
$prefix = is_file($store) ? '' : "<?php http_response_code(404); exit; ?>\n" . $row(array_keys($lead));
$saved = @file_put_contents($store, $prefix . $row(array_values($lead)), FILE_APPEND | LOCK_EX) !== false;

$mailed = false;
$cfgPath = $dataDir . '/lead-config.php';
if (is_file($cfgPath)) {
    $cfg = include $cfgPath;
    $to = array_filter((array) ($cfg['to'] ?? []), fn($a) => filter_var($a, FILTER_VALIDATE_EMAIL));
    if ($to) {
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@claimroofleak.com';
        $text = "New roof leak claim review request (claimroofleak.com)\n\n";
        foreach ($lead as $k => $v) {
            $text .= ucfirst(str_replace('_', ' ', $k)) . ': ' . ($k === 'message' ? "\n" . $v : $v) . "\n";
        }
        $headers = "From: Claim Roof Leak <$from>\r\nReply-To: {$lead['email']}\r\nContent-Type: text/plain; charset=UTF-8";
        $subject = '=?UTF-8?B?' . base64_encode('Roof claim lead: ' . $lead['name'] . ' - ' . $lead['claim_type']) . '?=';
        $mailed = @mail(implode(',', $to), $subject, $text, $headers);
    }
}

if (!$saved && !$mailed) {
    crl_reply(['ok' => false, 'error' => 'Something went wrong saving your request. Please call (407) 433-4131.'], 500);
}
crl_reply(['ok' => true, 'first' => explode(' ', $lead['name'])[0]]);
