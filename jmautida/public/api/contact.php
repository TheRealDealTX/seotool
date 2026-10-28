<?php
declare(strict_types=1);
require_once __DIR__ . '/lib.php';
require_once __DIR__ . '/mailer.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function fail(string $message, int $code = 400): void {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $message]);
    exit;
}
function field(array $in, string $key, int $max): string {
    $value = is_string($in[$key] ?? null) ? trim($in[$key]) : '';
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    return function_exists('mb_substr') ? mb_substr($value, 0, $max) : substr($value, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Allow: POST'); fail('Use POST to send a message.', 405); }
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && !preg_match('~^https?://(www\.)?jmautida\.com$~i', $origin) && !preg_match('~^https?://(localhost|127\.0\.0\.1)(:\d+)?$~', $origin)) fail('Cross-site submissions are not accepted.', 403);
$type = strtolower(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0]);
$raw = file_get_contents('php://input', false, null, 0, 20001);
if ($raw === false || strlen($raw) > 20000) fail('Your message is too long.', 413);
$in = $type === 'application/json' ? json_decode($raw, true) : $_POST;
if (!is_array($in)) fail('The form could not be read. Please try again.');

$config = is_file(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : null;
if (!is_array($config) || empty($config['smtp']['pass'])) fail('The contact form is not configured yet. Please email autida@jmautida.com directly.', 503);

$name = field($in, 'name', 100);
$email = field($in, 'email', 200);
$site = field($in, 'site', 300);
$message = field($in, 'message', 5000);
$topics = ['project' => 'Website project', 'seo' => 'SEO & marketing', 'tool' => 'Tool idea or bug', 'other' => 'Something else'];
$topic = $topics[field($in, 'topic', 20)] ?? 'Something else';

// Spam traps: hidden honeypot field and a minimum time on page.
$elapsed = (int)(microtime(true) * 1000) - (int)field($in, 'ts', 20);
if (field($in, 'company', 200) !== '' || $elapsed < 2500) { echo json_encode(['ok' => true]); exit; }
if ($name === '' || $email === '' || $message === '') fail('Please fill in your name, email and message.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $email)) fail('Please enter a valid email address.');
if ((function_exists('mb_strlen') ? mb_strlen($message) : strlen($message)) < 10) fail('Please write a message of at least 10 characters.');
if ($site !== '' && !preg_match('~^https?://~i', $site)) $site = 'https://' . $site;
if (preg_match_all('~https?://~i', $message) > 5) fail('Please include fewer links in your message.');

try { rate_limit('contact', 5, 900); }
catch (CheckError $e) { fail('You have sent several messages recently. Please wait a few minutes, or email autida@jmautida.com directly.', 429); }

$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$when = gmdate('D, j M Y H:i') . ' UTC';
$text = "New message from the jmautida.com contact form\n\nTopic: $topic\nName: $name\nEmail: $email\n" . ($site ? "Website: $site\n" : '') . "\nMessage:\n$message\n\n— Sent $when · IP $ip";
$h = static fn(string $v): string => htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
$html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#111;max-width:620px">'
    . '<h2 style="margin:0 0 4px;font-size:20px">New message from jmautida.com</h2>'
    . '<p style="margin:0 0 18px;color:#666;font-size:13px">' . $h($topic) . ' · ' . $h($when) . '</p>'
    . '<table style="border-collapse:collapse;margin-bottom:18px">'
    . '<tr><td style="padding:4px 14px 4px 0;color:#666">Name</td><td><strong>' . $h($name) . '</strong></td></tr>'
    . '<tr><td style="padding:4px 14px 4px 0;color:#666">Email</td><td><a href="mailto:' . $h($email) . '">' . $h($email) . '</a></td></tr>'
    . ($site ? '<tr><td style="padding:4px 14px 4px 0;color:#666">Website</td><td>' . $h($site) . '</td></tr>' : '')
    . '</table><div style="white-space:pre-wrap;padding:16px;background:#f5f6f8;border-radius:8px">' . $h($message) . '</div>'
    . '<p style="color:#999;font-size:12px;margin-top:18px">Reply directly to this email to answer ' . $h($name) . '. IP ' . $h($ip) . '</p></div>';

try {
    $mailer = new SmtpMailer($config['smtp'] + ['from_name' => 'jmautida.com']);
    $mailer->send($config['to'] ?? $config['smtp']['user'], "[$topic] " . $name . ' via jmautida.com', $text, $html, $email, $name);
    echo json_encode(['ok' => true]);
} catch (Throwable $e) {
    error_log('Contact form mail failed: ' . $e->getMessage());
    fail('The message could not be sent right now. Please email autida@jmautida.com directly.', 502);
}
