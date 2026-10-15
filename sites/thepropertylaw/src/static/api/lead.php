<?php
// Free case review requests from thepropertylaw.com for The Lawgical Firm, P.A.
// Each request is appended to ../data/leads.php (its first line exits, and
// .htaccess 404s /data/, so it is never served; download it from hPanel File
// Manager). If ../data/lead-config.php exists it is also emailed. Create that
// file on the server only (never commit it):
//   <?php if (!defined('TPL_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@thepropertylaw.com'];
require __DIR__ . '/_lib.php';
define('TPL_LEAD', true);
const TPL_PHONE = '(407) 433-4131';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    tpl_json(['ok' => false, 'error' => 'POST only'], 405);
}
tpl_throttle('lead', 6, 600);

$field = fn(string $k, int $max) => trim(mb_substr(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string) ($_POST[$k] ?? '')), 0, $max));
if ($field('company_url', 100) !== '') {          // honeypot
    tpl_json(['ok' => true, 'name' => 'there']);
}
$lead = [
    'received_utc' => gmdate('c'),
    'name'         => $field('name', 100),
    'phone'        => $field('phone', 30),
    'email'        => strtolower($field('email', 160)),
    'location'     => $field('location', 100),
    'claim_type'   => $field('claim_type', 80),
    'property'     => $field('property', 40),
    'description'  => trim(mb_substr((string) ($_POST['description'] ?? ''), 0, 3000)),
    'consent'      => !empty($_POST['consent']) ? 'yes' : 'no',
    'page'         => $field('page', 200),
    'ip'           => trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]),
];
$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    tpl_json(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 400);
}
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    tpl_json(['ok' => false, 'error' => 'Please check the email address.'], 400);
}
if ($lead['location'] === '') {
    tpl_json(['ok' => false, 'error' => 'Please enter the property city or ZIP code.'], 400);
}
if ($lead['consent'] !== 'yes') {
    tpl_json(['ok' => false, 'error' => 'Please check the acknowledgment box before sending.'], 400);
}

$dir = __DIR__ . '/../data';
@mkdir($dir, 0700, true);
$file = $dir . '/leads.php';
$row = fn(array $r) => implode(',', array_map(fn($v) => '"' . str_replace('"', '""', (string) $v) . '"', $r)) . "\n";
$first = !is_file($file);
$saved = @file_put_contents($file, ($first ? "<?php http_response_code(404); exit; ?>\n" . $row(array_keys($lead)) : '') . $row(array_values($lead)), FILE_APPEND | LOCK_EX);

$mailed = false;
$cfgFile = $dir . '/lead-config.php';
if (is_file($cfgFile)) {
    $cfg = include $cfgFile;
    $to = array_filter((array) ($cfg['to'] ?? []), fn($e) => filter_var($e, FILTER_VALIDATE_EMAIL));
    if ($to) {
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@thepropertylaw.com';
        $text = "Free case review request from thepropertylaw.com\n\n";
        foreach ($lead as $k => $v) {
            $text .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 15) . ($k === 'description' ? "\n" : ' ') . $v . "\n";
        }
        $headers = "From: The Property Law <$from>\r\nContent-Type: text/plain; charset=UTF-8";
        if ($lead['email'] !== '') {
            $headers .= "\r\nReply-To: " . $lead['email'];
        }
        $subject = '=?UTF-8?B?' . base64_encode('Property claim lead: ' . $lead['name'] . ' (' . $lead['claim_type'] . ')') . '?=';
        $mailed = @mail(implode(',', $to), $subject, $text, $headers);
    }
}
if ($saved === false && !$mailed) {
    tpl_json(['ok' => false, 'error' => 'We could not save your request. Please call ' . TPL_PHONE . '.'], 500);
}
tpl_json(['ok' => true, 'name' => explode(' ', $lead['name'])[0]]);
