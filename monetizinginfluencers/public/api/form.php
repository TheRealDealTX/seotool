<?php
/**
 * Single handler for every form on the site (newsletter, contact, get-started,
 * write-for-us pitch, web-design quote).
 *
 * Emails the submission to SITE_EMAIL (SMTP via inc/smtp.php, mail() fallback) and appends a copy to a log file that
 * sits OUTSIDE public_html (../../mi-form-submissions.log relative to this file).
 * Answers JSON for fetch() requests (ajax=1) and redirects for plain POSTs.
 */
require __DIR__ . '/../inc/config.php';
require __DIR__ . '/../inc/smtp.php';

const FORMS = [
    'newsletter'   => ['Newsletter signup', ['email']],
    'contact'      => ['Contact message', ['name', 'email', 'message']],
    'get-started'  => ['Get Started request', ['name', 'email']],
    'write-for-us' => ['Write For Us pitch', ['name', 'email', 'topic']],
    'web-design'   => ['Web design quote request', ['name', 'email']],
];

$ajax = !empty($_POST['ajax']);

function finish(bool $ok, string $msg, string $form, string $return, bool $ajax): void
{
    if ($ajax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $msg]);
        exit;
    }
    $path = (is_string($return) && preg_match('#^/[A-Za-z0-9/_\-]*$#', $return)) ? $return : '/';
    header('Location: ' . $path . '?form=' . rawurlencode($form) . '&sent=' . ($ok ? 'ok' : 'err') . '#' . rawurlencode($form), true, 303);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /', true, 302);
    exit;
}

$form   = (string) ($_POST['form'] ?? '');
$return = (string) ($_POST['return'] ?? '/');
if (!isset(FORMS[$form])) {
    finish(false, 'Unknown form.', 'contact', '/contact/', $ajax);
}
[$label, $required] = FORMS[$form];

// Spam guards: honeypot must be empty and the form must have been open for 3+ seconds.
$ts = (int) ($_POST['ts'] ?? 0);
if (!empty($_POST['website_url']) || $ts === 0 || time() - $ts < 3) {
    finish(true, 'Thanks! You are on the list.', $form, $return, $ajax); // silently drop bots
}

// Collect and clean fields.
$skip = ['form', 'return', 'ts', 'website_url', 'ajax'];
$data = [];
foreach ($_POST as $k => $v) {
    if (in_array($k, $skip, true) || !preg_match('/^[a-z_]{1,40}$/', $k)) {
        continue;
    }
    $v = is_array($v) ? implode(', ', array_map('strval', $v)) : (string) $v;
    $data[$k] = trim(mb_substr(str_replace("\0", '', $v), 0, 8000));
}
foreach ($required as $r) {
    if (($data[$r] ?? '') === '') {
        finish(false, 'Please fill in all required fields.', $form, $return, $ajax);
    }
}
$email = $data['email'] ?? '';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    finish(false, 'Please enter a valid email address.', $form, $return, $ajax);
}

// Very small per-IP rate limit (5 submissions / 10 minutes) using the temp dir.
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$rl = sys_get_temp_dir() . '/mi_rl_' . md5($ip);
$hits = array_filter(array_map('intval', @file($rl) ?: []), fn($t) => $t > time() - 600);
if (count($hits) >= 5) {
    finish(false, 'Too many submissions. Please try again in a few minutes.', $form, $return, $ajax);
}
$hits[] = time();
@file_put_contents($rl, implode("\n", $hits));

// Build the message.
$lines = [];
foreach ($data as $k => $v) {
    $lines[] = ucwords(str_replace('_', ' ', $k)) . ': ' . $v;
}
$body = $label . " from monetizinginfluencers.com\n\n" . implode("\n", $lines)
    . "\n\nPage: " . $return . "\nIP: " . $ip . "\nTime: " . gmdate('Y-m-d H:i:s') . " UTC\n";

$log = dirname(__DIR__, 2) . '/mi-form-submissions.log';
$logged = @file_put_contents($log, str_repeat('-', 60) . "\n" . $body, FILE_APPEND | LOCK_EX) !== false;

$safeName = preg_replace('/[\r\n<>"]+/', ' ', $data['name'] ?? '');
$replyTo = ($safeName !== '' ? '"' . $safeName . '" ' : '') . '<' . $email . '>';
$subject = '[' . SITE_NAME . '] ' . $label . ($safeName !== '' ? ' - ' . $safeName : '');

// Send through the info@ mailbox over authenticated SMTP; fall back to PHP mail() if that fails.
$sent = smtp_send(SITE_EMAIL, $subject, $body, $replyTo, $smtpErr);
if (!$sent) {
    @file_put_contents($log, 'SMTP failed: ' . $smtpErr . "\n", FILE_APPEND | LOCK_EX);
    $headers = [
        'From: ' . SITE_NAME . ' <' . SITE_EMAIL . '>',
        'Reply-To: ' . $replyTo,
        'Content-Type: text/plain; charset=UTF-8',
    ];
    $sent = @mail(SITE_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
}

$messages = [
    'newsletter'   => 'You are in! Watch your inbox for the next creator money memo.',
    'contact'      => 'Thanks! Your message is in. We reply within 1-2 business days.',
    'get-started'  => 'Request received! We will email you a monetization plan outline within 2 business days.',
    'write-for-us' => 'Pitch received! We review every pitch within 5-7 business days.',
    'web-design'   => 'Quote request received! We will email you within 1-2 business days.',
];
// Either the email or the log copy is enough to keep the lead.
if (!$sent && !$logged) {
    finish(false, 'We could not send that right now. Please email ' . SITE_EMAIL . ' directly.', $form, $return, $ajax);
}
finish(true, $messages[$form], $form, $return, $ajax);
