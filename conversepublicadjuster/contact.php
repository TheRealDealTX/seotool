<?php
// Contact form handler for conversepublicadjuster.com.
// Delivery: PHP mail() first (works on ordinary Apache/LiteSpeed hosts). On Hostinger's Agency (H5G) platform
// sendmail is disabled, so the lead is relayed over HTTPS to FormSubmit.co, which emails CONTACT_TO
// (the inbox owner activates the relay once by clicking FormSubmit's confirmation email).
const CONTACT_TO   = 'josephdittmanappraiser@gmail.com';
const CONTACT_FROM = 'website@conversepublicadjuster.com';
const SUBJECT      = 'San Antonio claim review request';
const RELAY_URL    = 'https://formsubmit.co/ajax/' . CONTACT_TO;

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'POST only']);
    exit;
}
if (!empty($_POST['website'])) { // honeypot
    echo json_encode(['ok' => true]);
    exit;
}

$clean = function ($k, $max = 500) {
    $v = isset($_POST[$k]) ? trim((string)$_POST[$k]) : '';
    $v = preg_replace('/[\r\n]+/', ' ', $v);
    return mb_substr(strip_tags($v), 0, $max);
};

$name    = $clean('name', 120);
$phone   = $clean('phone', 40);
$email   = $clean('email', 120);
$address = $clean('address', 200);
$zip     = $clean('zip', 10);
$damage  = $clean('damage', 60);
$status  = $clean('status', 60);
$message = isset($_POST['message']) ? mb_substr(strip_tags(trim((string)$_POST['message'])), 0, 3000) : '';

if ($name === '' || $phone === '') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Name and phone are required']);
    exit;
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $email = '';
}

$body = "New claim review request from conversepublicadjuster.com\n\n"
      . "Name:     $name\n"
      . "Phone:    $phone\n"
      . "Email:    " . ($email ?: '-') . "\n"
      . "Address:  " . ($address ?: '-') . "\n"
      . "ZIP:      " . ($zip ?: '-') . "\n"
      . "Damage:   " . ($damage ?: '-') . "\n"
      . "Claim:    " . ($status ?: '-') . "\n\n"
      . "Message:\n" . ($message ?: '-') . "\n\n"
      . "Sent " . date('Y-m-d H:i T') . " from " . ($_SERVER['REMOTE_ADDR'] ?? '?') . "\n";

$headers = "From: San Antonio Public Adjuster <" . CONTACT_FROM . ">\r\n"
         . ($email ? "Reply-To: $name <$email>\r\n" : '')
         . "X-Mailer: PHP/" . phpversion();

$sent = @mail(CONTACT_TO, SUBJECT . ' - ' . $name, $body, $headers);

if (!$sent && function_exists('curl_init')) {
    // Relay through FormSubmit.co (JSON in, JSON out).
    $payload = [
        '_subject'  => SUBJECT . ' - ' . $name,
        '_template' => 'table',
        '_captcha'  => 'false',
        'Name'      => $name,
        'Phone'     => $phone,
        'Email'     => $email ?: '-',
        'Address'   => $address ?: '-',
        'ZIP'       => $zip ?: '-',
        'Damage'    => $damage ?: '-',
        'Claim'     => $status ?: '-',
        'Message'   => $message ?: '-',
        'Sent'      => date('Y-m-d H:i T') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? '?'),
    ];
    if ($email !== '') {
        $payload['_replyto'] = $email;
    }
    $ch = curl_init(RELAY_URL);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($payload),
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json', 'Accept: application/json',
                                   'Origin: https://conversepublicadjuster.com',
                                   'Referer: https://conversepublicadjuster.com/contact'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 15,
    ]);
    $resp = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    $json = is_string($resp) ? json_decode($resp, true) : null;
    $sent = $code >= 200 && $code < 300 && is_array($json)
         && (($json['success'] ?? '') === 'true' || ($json['success'] ?? false) === true);
    if (!$sent) {
        http_response_code(502);
        echo json_encode(['ok' => false, 'error' => 'relay failed', 'status' => $code,
                          'detail' => is_array($json) ? ($json['message'] ?? '') : '']);
        exit;
    }
}

if (!$sent) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'mail() failed']);
    exit;
}
echo json_encode(['ok' => true]);
