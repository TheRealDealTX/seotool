<?php
/** POST /contact/send — validates, filters spam, emails info@ and redirects back. */
defined('SCC') || (http_response_code(404) && exit);
require ROOT . '/inc/mailer.php';

function back(bool $ok): void
{
    header('Location: ' . SITE_ORIGIN . '/contact/?sent=' . ($ok ? '1' : '0'), true, 303);
    exit;
}

$p = fn($k) => trim((string) ($_POST[$k] ?? ''));
$name = mb_substr(preg_replace('/[\r\n]+/', ' ', $p('name')), 0, 80);
$email = $p('email');
$topic = mb_substr(preg_replace('/[\r\n]+/', ' ', $p('topic')), 0, 80);
$msg = mb_substr($p('message'), 0, 5000);
$t = (int) $p('t');
$sigOk = hash_equals(hash_hmac('sha256', (string) $t, config('form_secret', 'scc-form-' . SITE_ORIGIN)), $p('sig'));
$age = time() - $t;

// Validation
if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($msg) < 20) back(false);

// Spam heuristics: silently "succeed" so bots learn nothing.
$spam = $p('website') !== ''                    // honeypot filled
    || !$sigOk || $age < 4 || $age > 172800       // forged token, too fast, or stale
    || $p('js') !== '1'                           // no human interaction with the form
    || preg_match_all('#https?://#i', $msg) > 2
    || preg_match('/\b(seo|backlinks?|guest post|crypto|casino|viagra|loan|dormant|retrieve your (funds|balance)|GoogleSearchIndex|intimate photos|tinyurl)\b/i', $msg . ' ' . $name)
    || preg_match('/[\x{0400}-\x{04FF}]{5,}/u', $msg);

// Simple per-IP rate limit (5 per hour)
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0';
$ip = trim(explode(',', $ip)[0]);
$rl = sys_get_temp_dir() . '/scc-rl-' . md5($ip);
$hits = array_filter(array_map('intval', @file($rl) ?: []), fn($x) => $x > time() - 3600);
if (count($hits) >= 5) $spam = true;
@file_put_contents($rl, implode("\n", array_merge($hits, [time()])));

if ($spam) back(true);

$body = "New message from the solarcctvcamera.com contact form\n\n"
    . "Name:  $name\nEmail: $email\nTopic: $topic\n\n$msg\n\n--\nIP: $ip\nSent: " . date('c') . "\n";
$ok = smtp_send(SITE_EMAIL, "[Solar CCTV Camera] $topic — $name", $body, $email);
back($ok);
