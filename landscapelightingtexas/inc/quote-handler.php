<?php
// Handles POST /quote/. Emails the request and keeps a server-side copy in
// storage/ (each file starts with an exit guard so it can't be read over HTTP).
defined('LLT') or die(http_response_code(404));

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
function quote_reply(bool $ok, string $msg, bool $json): void {
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 422);
        echo json_encode(['ok' => $ok, 'message' => $msg]);
    } else {
        header('Location: ' . SITE_ORIGIN . '/quote/?' . ($ok ? 'sent=1' : 'error=1'), true, 303);
    }
    exit;
}

$f = fn($k, $max = 200) => trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max));
$d = [
    'first_name' => $f('first_name', 80), 'last_name' => $f('last_name', 80), 'email' => $f('email', 160),
    'phone' => $f('phone', 40), 'city' => $f('city', 80), 'service' => $f('service', 80),
    'message' => $f('message', 4000), 'source' => $f('source', 60),
];

// Spam checks: honeypot filled, or submitted faster than a human could.
$t = (int)($_POST['t'] ?? 0);
if ($f('website') !== '' || ($t && time() - $t < 3)) quote_reply(true, 'Thanks! Your request has been received.', $wantsJson);

if ($d['first_name'] === '' || !filter_var($d['email'], FILTER_VALIDATE_EMAIL) || strlen(preg_replace('/\D/', '', $d['phone'])) < 10) {
    quote_reply(false, 'Please add your first name, a valid email address and a 10-digit phone number.', $wantsJson);
}

$d['received'] = date('c');
$d['ip'] = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$dir = dirname(__DIR__) . '/storage';
if (!is_dir($dir)) @mkdir($dir, 0750, true);
$saved = @file_put_contents($dir . '/quote-' . date('Ymd-His') . '-' . bin2hex(random_bytes(3)) . '.php',
    "<?php exit; ?>\n" . json_encode($d, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)) !== false;

$body = "New quote request from landscapelightingtexas.com\n\n";
foreach (['first_name' => 'First name', 'last_name' => 'Last name', 'email' => 'Email', 'phone' => 'Phone', 'city' => 'City', 'service' => 'Service', 'source' => 'Form', 'received' => 'Received'] as $k => $label) {
    $body .= str_pad($label . ':', 12) . $d[$k] . "\n";
}
$body .= "\nProject details:\n" . $d['message'] . "\n";
$headers = "From: Landscape Lighting Texas <no-reply@" . SITE_HOST . ">\r\n"
         . "Reply-To: " . preg_replace('/[\r\n]/', '', $d['email']) . "\r\nContent-Type: text/plain; charset=utf-8\r\n";
$subject = 'Quote request: ' . $d['first_name'] . ' ' . $d['last_name'] . ($d['city'] ? ' (' . $d['city'] . ')' : '');
$mailed = function_exists('mail') && @mail(QUOTE_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);

if ($mailed || $saved) {
    quote_reply(true, 'Thank you, ' . $d['first_name'] . '! Your request is in. A Landscape Lighting Texas designer will contact you within one business day.', $wantsJson);
}
quote_reply(false, 'Sorry, we could not send your request. Please call ' . PHONE . ' or email ' . EMAIL . '.', $wantsJson);
