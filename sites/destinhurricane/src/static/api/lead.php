<?php
// Free claim review requests for The Lawgical Firm, P.A. (destinhurricane.com).
// Each request is appended to ../data/leads.php (its first line exits, so the
// file 404s on the web; download it from hPanel File Manager). If
// ../data/lead-config.php exists on the server, the request is also emailed.
// That file is created on the server only, never committed, and starts with a
// guard so a direct request for it returns 404:
//   <?php if (!defined('DH_LEAD')) { http_response_code(404); exit; }
//   return ['to' => ['intake@example.com'], 'from' => 'leads@destinhurricane.com'];
require __DIR__ . '/_lib.php';
define('DH_LEAD', true);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    dh_json(['ok' => false, 'error' => 'POST only'], 405);
}
dh_rate_limit('lead', 6, 600);

$field = fn($k, $max) => trim(mb_substr(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', (string) ($_POST[$k] ?? '')), 0, $max));
if ($field('website', 100) !== '') {            // honeypot: act as if it worked
    dh_json(['ok' => true, 'name' => 'there']);
}
$lead = [
    'received_utc' => gmdate('c'),
    'name' => $field('name', 100),
    'phone' => $field('phone', 30),
    'email' => strtolower($field('email', 160)),
    'location' => $field('location', 100),
    'issue' => $field('issue', 80),
    'storm' => $field('storm', 80),
    'insurer' => $field('insurer', 100),
    'message' => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000)),
    'no_relationship_ack' => !empty($_POST['ack']) ? 'yes' : 'no',
    'sms_consent' => !empty($_POST['sms_consent']) ? 'yes' : 'no',
    'page' => $field('page', 200),
    'site' => 'destinhurricane.com',
    'ip' => trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]),
];
$digits = preg_replace('/\D+/', '', $lead['phone']);
if ($lead['name'] === '' || strlen($digits) < 10 || strlen($digits) > 11) {
    dh_json(['ok' => false, 'error' => 'Please enter your name and a 10-digit phone number.'], 400);
}
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) {
    dh_json(['ok' => false, 'error' => 'Please check the email address.'], 400);
}
if ($lead['location'] === '') {
    dh_json(['ok' => false, 'error' => 'Please enter the property city or ZIP code.'], 400);
}
if ($lead['no_relationship_ack'] !== 'yes') {
    dh_json(['ok' => false, 'error' => 'Please tick the box confirming that this form does not create an attorney-client relationship.'], 400);
}

$dir = __DIR__ . '/../data';
@mkdir($dir, 0700, true);
$file = $dir . '/leads.php';
$csv = fn(array $row) => implode(',', array_map(fn($v) => '"' . str_replace('"', '""', (string) $v) . '"', $row)) . "\n";
$fresh = !is_file($file);
$saved = @file_put_contents($file, ($fresh ? "<?php http_response_code(404); exit; ?>\n" . $csv(array_keys($lead)) : '') . $csv(array_values($lead)), FILE_APPEND | LOCK_EX);

$mailed = false;
$cfgFile = $dir . '/lead-config.php';
if (is_file($cfgFile)) {
    $cfg = include $cfgFile;
    $to = array_filter((array) ($cfg['to'] ?? []), fn($e) => filter_var($e, FILTER_VALIDATE_EMAIL));
    if ($to) {
        $from = filter_var($cfg['from'] ?? '', FILTER_VALIDATE_EMAIL) ?: 'leads@destinhurricane.com';
        $body = "New free claim review request from destinhurricane.com\n\n";
        foreach ($lead as $k => $v) {
            $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 22) . ($k === 'message' ? "\n" : ' ') . $v . "\n";
        }
        $headers = "From: Destin Hurricane <$from>\r\nContent-Type: text/plain; charset=UTF-8";
        if ($lead['email'] !== '') {
            $headers .= "\r\nReply-To: " . $lead['email'];
        }
        $subject = '=?UTF-8?B?' . base64_encode('Destin storm claim lead: ' . $lead['name'] . ' (' . $lead['issue'] . ')') . '?=';
        $mailed = @mail(implode(',', $to), $subject, $body, $headers);
    }
}
if ($saved === false && !$mailed) {
    dh_json(['ok' => false, 'error' => 'We could not save your request. Please call (850) 203-3385.'], 500);
}
dh_json(['ok' => true, 'name' => explode(' ', $lead['name'])[0], 'saved' => $saved !== false, 'mailed' => (bool) $mailed]);
