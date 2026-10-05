<?php
// beltonbanners.com - quote / contact form handler.
// Receives POSTs from every .quote-form on the site, validates them, emails
// the request to the studio and answers with JSON (AJAX) or a redirect to
// /thank-you/ (plain form post). No database, no sessions, no third parties.

declare(strict_types=1);

const TO_EMAIL   = 'dittmanbanners@gmail.com';
const FROM_EMAIL = 'noreply@beltonbanners.com';
const SITE       = 'https://beltonbanners.com';
const LOG_DIR    = __DIR__ . '/../inquiries';   // outside the document root; optional

$ajax = (isset($_POST['ajax']) && $_POST['ajax'] === '1')
    || (stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false);

function respond(bool $ok, string $message, int $status = 200): void
{
    global $ajax;
    if ($ajax) {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode(['ok' => $ok, 'message' => $message], JSON_UNESCAPED_UNICODE);
        exit;
    }
    if ($ok) {
        header('Location: ' . SITE . '/thank-you/', true, 303);
        exit;
    }
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><meta charset="utf-8"><title>Could not send</title>'
        . '<body style="font-family:sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem">'
        . '<h1>Could not send your request</h1><p>' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8') . '</p>'
        . '<p><a href="javascript:history.back()">Go back</a> or call / text <a href="tel:+18177292961">+1 817-729-2961</a>.</p></body>';
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Location: ' . SITE . '/contact-us/', true, 302);
    exit;
}

$field = static function (string $key, int $max = 2000): string {
    $v = $_POST[$key] ?? '';
    if (!is_string($v)) {
        return '';
    }
    $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/', '', $v) ?? '');
    return mb_substr($v, 0, $max);
};

// Honeypot: real visitors never see this field.
if ($field('website') !== '') {
    respond(true, 'Sent! Christina will be in touch soon.');
}

$name      = $field('name', 120);
$email     = $field('email', 200);
$phone     = $field('phone', 60);
$occasion  = $field('occasion', 80);
$size      = $field('size', 40);
$eventDate = $field('event_date', 40);
$wording   = $field('wording', 300);
$message   = $field('message', 4000);
$product   = $field('product', 300);
$source    = $field('source', 80);

if ($name === '' || mb_strlen($name) < 2) {
    respond(false, 'Please enter your name.', 422);
}
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please enter a valid email address so we can reply.', 422);
}
if ($message === '' && $wording === '' && $product === '') {
    respond(false, 'Tell us a little about the banner you have in mind.', 422);
}
// Header-injection guard: no line breaks in anything that touches a header.
foreach ([$name, $email, $phone] as $hv) {
    if (preg_match('/[\r\n]/', $hv)) {
        respond(false, 'Invalid input.', 422);
    }
}
// Crude link-spam filter.
if (preg_match_all('#https?://#i', $message) > 3) {
    respond(false, 'Your message looks like spam. Please call or text instead.', 422);
}

$lines = [
    'New banner request from beltonbanners.com',
    str_repeat('-', 42),
    'Name:        ' . $name,
    'Email:       ' . $email,
    'Phone:       ' . ($phone ?: '-'),
    'Occasion:    ' . ($occasion ?: '-'),
    'Size:        ' . ($size ?: '-'),
    'Event date:  ' . ($eventDate ?: '-'),
    'Wording:     ' . ($wording ?: '-'),
    'Product:     ' . ($product ?: '-'),
    'Sent from:   ' . ($source ?: '-'),
    'Time:        ' . date('Y-m-d H:i:s T'),
    'IP:          ' . ($_SERVER['REMOTE_ADDR'] ?? '-'),
    str_repeat('-', 42),
    'Message:',
    $message !== '' ? $message : '(none)',
];
$body = implode("\n", $lines) . "\n";

$subjectBits = array_filter([$occasion ?: null, $size ?: null, $name]);
$subject = 'Banner request: ' . implode(' / ', $subjectBits);
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$headers = [
    'From: Belton Banners Website <' . FROM_EMAIL . '>',
    'Reply-To: ' . str_replace(['"', '<', '>'], '', $name) . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: PHP/' . PHP_VERSION,
];

$sent = @mail(TO_EMAIL, $subject, $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

// Keep a private copy as a safety net in case mail delivery is delayed.
$logged = false;
if (!is_dir(LOG_DIR)) {
    @mkdir(LOG_DIR, 0700, true);
}
if (is_dir(LOG_DIR) && is_writable(LOG_DIR)) {
    $logged = (bool) @file_put_contents(
        LOG_DIR . '/inquiries-' . date('Y-m') . '.txt',
        $body . "\n\n",
        FILE_APPEND | LOCK_EX
    );
}

if ($sent || $logged) {
    respond(true, 'Sent! Christina will be in touch soon - usually within a day.');
}
respond(false, 'The message could not be sent right now. Please call or text +1 817-729-2961 or email dittmanbanners@gmail.com.', 500);
