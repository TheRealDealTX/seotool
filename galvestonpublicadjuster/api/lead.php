<?php
// Lead form handler: emails every submission to LEAD_EMAIL and keeps a private backup log.
// Responds with JSON to fetch() requests and redirects plain form posts to /thank-you/.
require dirname(__DIR__) . '/inc/config.php';

$ajax = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
function done($ok, $msg, $ajax) {
    if ($ajax) {
        header('Content-Type: application/json');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'message' => $msg]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/contact/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: /contact/', true, 303); exit; }

$f = fn($k, $max = 200) => trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max));
$lead = [
    'name'       => $f('name', 120),
    'phone'      => $f('phone', 40),
    'email'      => $f('email', 160),
    'address'    => $f('address', 200),
    'claim_type' => $f('claim_type', 60),
    'status'     => $f('status', 60),
    'message'    => $f('message', 3000),
    'source'     => $f('source', 40),
    'page'       => $f('page', 300),
];

// Honeypot: bots fill the hidden "website" field. Pretend success.
if ($f('website') !== '') done(true, 'Thanks!', $ajax);

if ($lead['name'] === '' || strlen(preg_replace('/\D/', '', $lead['phone'])) < 10) {
    done(false, 'Please enter your name and a 10-digit phone number.', $ajax);
}
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) $lead['email'] = '';

// Simple per-IP throttle: 5 submissions per 10 minutes.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);
$rl = sys_get_temp_dir() . '/gpa-rl-' . md5($ip);
$hits = array_filter(is_file($rl) ? (array)json_decode(file_get_contents($rl), true) : [], fn($t) => $t > time() - 600);
if (count($hits) >= 5) done(false, 'Too many requests — please call ' . PHONE . '.', $ajax);
$hits[] = time();
@file_put_contents($rl, json_encode(array_values($hits)));

$when = date('Y-m-d H:i:s T');
$subject = 'New claim lead: ' . $lead['name'] . ' — ' . $lead['claim_type'];
$body = "New lead from galvestonpublicadjuster.com\n\n"
    . "Name:        {$lead['name']}\n"
    . "Phone:       {$lead['phone']}\n"
    . "Email:       {$lead['email']}\n"
    . "Property:    {$lead['address']}\n"
    . "Claim type:  {$lead['claim_type']}\n"
    . "Status:      {$lead['status']}\n"
    . "Form:        {$lead['source']}\n"
    . "Page:        {$lead['page']}\n"
    . "Received:    $when\n"
    . "IP:          $ip\n\n"
    . "Message:\n{$lead['message']}\n";

$headers = [
    'From: ' . SITE_NAME . ' <' . MAIL_FROM . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: gpa-lead',
];
if ($lead['email'] !== '') $headers[] = 'Reply-To: ' . $lead['email'];
$sent = @mail(LEAD_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), '-f' . MAIL_FROM);

// Backup log (PHP file that exits immediately, so it can't be read over the web).
$log = PRIVATE_DIR . '/leads.php';
if (!is_dir(PRIVATE_DIR)) @mkdir(PRIVATE_DIR, 0750, true);
if (!is_file($log)) @file_put_contents($log, "<?php exit; ?>\n");
@file_put_contents($log, json_encode($lead + ['time' => $when, 'ip' => $ip, 'mailed' => $sent], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

done(true, 'Thank you! ' . AUTHOR . ' will call you shortly. Need help now? Call ' . PHONE . '.', $ajax);
