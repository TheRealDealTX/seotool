<?php
// Claim review form handler for enforceinterest.com.
// Sends the submission (with any attachments) to info@enforceinterest.com through the
// Hostinger mailbox over authenticated SMTP, keeps a copy in a log outside the web root,
// and replies with JSON. SMTP credentials live in a config file that is never in git:
//   ../ei-mail-config.php  (preferred, outside public_html), or
//   ./_private/mail-config.php (fallback; a PHP file, so it can't be downloaded)
// Each returns: ['host'=>'smtp.hostinger.com','port'=>465,'user'=>'info@…','pass'=>'…','to'=>'info@…']
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');
header('Cache-Control: no-store');

const MAX_FILES = 5;
const MAX_BYTES = 10485760; // 10 MB total
const SITE_EMAIL = 'info@enforceinterest.com';

function reply($ok, $msg, $code = 200) {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'message' => $msg]);
    exit;
}
function clean($v, $max = 200) {
    $v = trim(strip_tags((string)$v));
    $v = preg_replace('/[\r\n\t]+/', ' ', $v);
    return mb_substr($v, 0, $max);
}
function config() {
    foreach ([dirname(__DIR__) . '/ei-mail-config.php', __DIR__ . '/_private/mail-config.php'] as $f) {
        if (is_file($f)) { $c = include $f; if (is_array($c)) return $c; }
    }
    return null;
}
function store_dir() {
    $out = dirname(__DIR__);
    if (is_writable($out)) return $out;
    $p = __DIR__ . '/_private';
    if (!is_dir($p)) @mkdir($p, 0750);
    return $p;
}
function log_line($text) {
    $dir = store_dir();
    $file = $dir === dirname(__DIR__) ? $dir . '/ei-contact-messages.log' : $dir . '/messages.log.php';
    if (!is_file($file) && substr($file, -4) === '.php') @file_put_contents($file, "<?php http_response_code(404); exit; ?>\n");
    @file_put_contents($file, '[' . gmdate('c') . '] ' . $text . "\n----\n", FILE_APPEND | LOCK_EX);
}

// ---- minimal SMTP client (implicit TLS on 465, AUTH LOGIN) ----
function smtp_send($cfg, $from, $to, $replyTo, $subject, $text, $files = []) {
    $host = $cfg['host'] ?? 'smtp.hostinger.com';
    $port = (int)($cfg['port'] ?? 465);
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port, $errno, $errstr, 20);
    if (!$fp) return "connect: $errstr";
    stream_set_timeout($fp, 20);
    $read = function () use ($fp) { $data = ''; while (($line = fgets($fp, 515)) !== false) { $data .= $line; if (isset($line[3]) && $line[3] === ' ') break; } return $data; };
    $cmd = function ($c, $expect) use ($fp, $read) { if ($c !== null) fwrite($fp, $c . "\r\n"); $r = $read(); return (strpos($r, (string)$expect) === 0) ? true : trim($r); };
    $host_name = $_SERVER['SERVER_NAME'] ?? 'enforceinterest.com';
    foreach ([[null, 220], ['EHLO ' . $host_name, 250]] as $s) { if (($r = $cmd($s[0], $s[1])) !== true) { fclose($fp); return $r; } }
    if ($port !== 465) {
        if (($r = $cmd('STARTTLS', 220)) !== true) { fclose($fp); return $r; }
        stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
        $cmd('EHLO ' . $host_name, 250);
    }
    $steps = [['AUTH LOGIN', 334], [base64_encode($cfg['user']), 334], [base64_encode($cfg['pass']), 235],
              ['MAIL FROM:<' . $from . '>', 250], ['RCPT TO:<' . $to . '>', 250], ['DATA', 354]];
    foreach ($steps as $s) { if (($r = $cmd($s[0], $s[1])) !== true) { fclose($fp); return $r; } }
    $b = 'b' . bin2hex(random_bytes(12));
    $h  = 'Date: ' . date('r') . "\r\n";
    $h .= 'From: "Enforce Interest Website" <' . $from . ">\r\n";
    $h .= 'To: <' . $to . ">\r\n";
    if ($replyTo) $h .= 'Reply-To: ' . $replyTo . "\r\n";
    $h .= 'Subject: =?UTF-8?B?' . base64_encode($subject) . "?=\r\n";
    $h .= 'Message-ID: <' . bin2hex(random_bytes(10)) . '@enforceinterest.com>' . "\r\n";
    $h .= "MIME-Version: 1.0\r\n";
    $body = '';
    if ($files) {
        $h .= "Content-Type: multipart/mixed; boundary=\"$b\"\r\n";
        $body .= "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text)) . "\r\n";
        foreach ($files as $f) {
            $n = preg_replace('/[^A-Za-z0-9._ -]/', '_', $f['name']);
            $body .= "--$b\r\nContent-Type: {$f['type']}; name=\"$n\"\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"$n\"\r\n\r\n" . chunk_split(base64_encode($f['data'])) . "\r\n";
        }
        $body .= "--$b--\r\n";
    } else {
        $h .= "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n";
        $body = chunk_split(base64_encode($text));
    }
    $msg = preg_replace('/^\./m', '..', $h . "\r\n" . $body);
    fwrite($fp, $msg . "\r\n.\r\n");
    $r = $read();
    $cmd('QUIT', 221);
    fclose($fp);
    return strpos($r, '250') === 0 ? true : trim($r);
}

// ---- request checks ----
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') reply(false, 'Please use the form on the contact page.', 405);
if (!empty($_POST['website'])) reply(true, 'Thanks! Your claim details were sent.');           // honeypot
if ((int)($_POST['t'] ?? 0) < 4) reply(true, 'Thanks! Your claim details were sent.');          // filled too fast to be human

// simple per-IP rate limit: 5 per hour
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0';
$ip = trim(explode(',', $ip)[0]);
$rl = sys_get_temp_dir() . '/ei-rl-' . md5($ip);
$hits = array_filter(explode(',', (string)@file_get_contents($rl)), function ($t) { return $t && $t > time() - 3600; });
if (count($hits) >= 5) reply(false, 'Too many submissions from this connection. Please email ' . SITE_EMAIL . ' directly.', 429);
$hits[] = time();
@file_put_contents($rl, implode(',', $hits));

$f = [
    'Name' => clean($_POST['name'] ?? '', 120),
    'Email' => trim($_POST['email'] ?? ''),
    'Phone' => clean($_POST['phone'] ?? '', 40),
    'Insurance company' => clean($_POST['insurer'] ?? ''),
    'Type of claim' => clean($_POST['claim_type'] ?? ''),
    'Date of loss' => clean($_POST['date_of_loss'] ?? '', 20),
    'Claim number' => clean($_POST['claim_number'] ?? '', 60),
    'Supplements filed' => clean($_POST['supplements'] ?? '', 10),
    'Went to appraisal' => clean($_POST['appraisal'] ?? '', 10),
    'Denied then paid' => clean($_POST['denied_then_paid'] ?? '', 10),
    'Believes underpaid' => clean($_POST['underpaid'] ?? '', 10),
    'Approx. amount paid' => clean($_POST['amount_paid'] ?? '', 20),
    'Location' => clean($_POST['location'] ?? ''),
];
$message = trim(strip_tags((string)($_POST['message'] ?? '')));
if ($f['Name'] === '' || $message === '' || !filter_var($f['Email'], FILTER_VALIDATE_EMAIL) || ($_POST['consent'] ?? '') !== 'yes') {
    reply(false, 'Please fill in your name, a valid email address, a short description and the consent box.', 422);
}
if (mb_strlen($message) > 8000) reply(false, 'That description is a little long — please shorten it or email us directly.', 422);
$spam = preg_match_all('#https?://#i', $message) > 2 || preg_match('/\b(seo|backlinks?|guest post|crypto|casino|web design services|rank your website)\b/i', $message);

// attachments
$files = [];
if (!empty($_FILES['files']) && is_array($_FILES['files']['name'])) {
    $total = 0;
    $allowed = ['application/pdf' => 'pdf', 'image/jpeg' => 'jpg', 'image/png' => 'png'];
    $finfo = function_exists('finfo_open') ? finfo_open(FILEINFO_MIME_TYPE) : null;
    foreach ($_FILES['files']['name'] as $i => $name) {
        if (($_FILES['files']['error'][$i] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) continue;
        if ($_FILES['files']['error'][$i] !== UPLOAD_ERR_OK) reply(false, 'One of the files could not be uploaded. Please try again or email it to ' . SITE_EMAIL . '.', 422);
        $tmp = $_FILES['files']['tmp_name'][$i];
        $type = $finfo ? finfo_file($finfo, $tmp) : ($_FILES['files']['type'][$i] ?? '');
        if (!isset($allowed[$type])) reply(false, 'Please attach PDF, JPG or PNG files only.', 422);
        $total += filesize($tmp);
        if (count($files) >= MAX_FILES || $total > MAX_BYTES) reply(false, 'Please attach up to 5 files, 10 MB total — or email larger files to ' . SITE_EMAIL . '.', 422);
        $files[] = ['name' => basename($name), 'type' => $type, 'data' => file_get_contents($tmp)];
    }
}

$lines = [];
foreach ($f as $k => $v) if ($v !== '') $lines[] = str_pad($k . ':', 22) . $v;
$text = "New claim review request from enforceinterest.com\n\n" . implode("\n", $lines) . "\n\nWhat happened:\n" . $message .
        "\n\n" . (count($files) ? count($files) . " attachment(s) included.\n" : '') . "IP: $ip\nSent: " . gmdate('Y-m-d H:i') . " UTC\n";
log_line(($spam ? '[SPAM?] ' : '') . $text);
if ($spam) reply(true, 'Thanks! Your claim details were sent. We usually reply within one business day.');

$cfg = config();
$sent = false;
$subject = 'Claim review: ' . $f['Name'] . ($f['Type of claim'] ? ' — ' . $f['Type of claim'] : '');
$replyTo = '"' . str_replace('"', '', $f['Name']) . '" <' . $f['Email'] . '>';
if ($cfg && !empty($cfg['user']) && !empty($cfg['pass'])) {
    $to = $cfg['to'] ?? SITE_EMAIL;
    $r = smtp_send($cfg, $cfg['user'], $to, $replyTo, $subject, $text, $files);
    $sent = ($r === true);
    if (!$sent) log_line('SMTP error: ' . $r);
    if ($sent) {
        $ack = "Hi " . $f['Name'] . ",\n\nThanks for contacting Enforce Interest. We received your claim review request and will reply within one business day.\n\n" .
               "If you have claim letters, payment stubs, estimates or an appraisal award you haven't sent yet, just reply to this email and attach them.\n\n" .
               "Enforce Interest — a Rise Public Adjusting service\nTexas public adjuster license #3356839\nhttps://enforceinterest.com\n\n" .
               "We are not a law firm and do not provide legal advice.";
        smtp_send($cfg, $cfg['user'], $f['Email'], 'Enforce Interest <' . SITE_EMAIL . '>', 'We received your claim review request', $ack);
    }
}
if (!$sent) {
    $headers = "From: Enforce Interest Website <" . SITE_EMAIL . ">\r\nReply-To: " . $replyTo . "\r\nContent-Type: text/plain; charset=utf-8";
    $sent = @mail(SITE_EMAIL, $subject, $text . (count($files) ? "\n(Attachments could not be sent by fallback mail; see the log.)" : ''), $headers);
}
if ($sent) reply(true, 'Thanks! Your claim details were sent. We usually reply within one business day.');
reply(true, 'Thanks — we received your request. If it is urgent, email ' . SITE_EMAIL . ' directly.');
