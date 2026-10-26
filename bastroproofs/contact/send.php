<?php
/**
 * Estimate form handler. Validates, rejects bots (honeypot + timing-free checks),
 * emails FORM_RECIPIENT and redirects back with ?sent=1|0.
 */
declare(strict_types=1);
require dirname(__DIR__) . '/includes/config.php';

$back = '/contact/';
$ref = $_SERVER['HTTP_REFERER'] ?? '';
if ($ref !== '' && parse_url($ref, PHP_URL_HOST) === SITE['domain']) {
    $back = parse_url($ref, PHP_URL_PATH) ?: '/contact/';
}

function done(string $back, bool $ok): never
{
    $anchor = $back === '/' ? '#estimate' : '';
    header('Location: ' . $back . '?sent=' . ($ok ? '1' : '0') . $anchor, true, 303);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact/', true, 302);
    exit;
}

// Honeypot: real people never fill this in. Pretend success.
if (!empty($_POST['website'])) {
    done($back, true);
}

$clean = fn(string $k, int $max = 200) => trim(mb_substr(str_replace(["\r", "\n"], ' ', (string) ($_POST[$k] ?? '')), 0, $max));
$name    = $clean('name', 100);
$phone   = $clean('phone', 40);
$email   = $clean('email', 150);
$address = $clean('address', 200);
$service = $clean('service', 100);
$context = $clean('context', 60);
$message = trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 3000));

if ($name === '' || !preg_match('/\d{7,}/', preg_replace('/\D/', '', $phone))) {
    done($back, false);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $email = '';
}

$body = "New roof estimate request from bastroproofs.com\n\n"
      . "Name:     $name\nPhone:    $phone\nEmail:    $email\nAddress:  $address\n"
      . "Service:  $service\nFrom:     $context\n\nMessage:\n$message\n";
$headers = [
    'From: Bastrop Roofing Website <no-reply@' . SITE['domain'] . '>',
    'Content-Type: text/plain; charset=UTF-8',
];
if ($email !== '') {
    $headers[] = 'Reply-To: ' . $email;
}

$ok = @mail(FORM_RECIPIENT, 'Roof estimate request: ' . $name, $body, implode("\r\n", $headers));
done($back, $ok);
