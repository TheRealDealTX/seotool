<?php
// Storm-alert sign-ups. Stored outside the web root when possible; otherwise
// in a .php file whose first line exits, so it can never be downloaded.
require __DIR__ . '/_lib.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    ph_json(['ok' => false, 'error' => 'POST only'], 405);
}
ph_rate_limit('subscribe', 5, 600);
if (!empty($_POST['website'])) {            // honeypot
    ph_json(['ok' => true, 'email' => '']);
}
$email = strtolower(trim((string) ($_POST['email'] ?? '')));
$phone = preg_replace('/\D+/', '', (string) ($_POST['phone'] ?? ''));
$smsConsent = !empty($_POST['sms_consent']);
$area = substr(preg_replace('/[^\w\s,.\-]/u', '', (string) ($_POST['area'] ?? '')), 0, 60);
$topics = array_slice(array_map(fn($t) => preg_replace('/[^a-z_]/', '', (string) $t), (array) ($_POST['topics'] ?? [])), 0, 8);
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 160) {
    ph_json(['ok' => false, 'error' => 'Please enter a valid email address.'], 400);
}
if ($phone !== '' && (strlen($phone) < 10 || strlen($phone) > 11)) {
    ph_json(['ok' => false, 'error' => 'Please enter a 10-digit U.S. mobile number, or leave it blank.'], 400);
}
if ($phone !== '' && !$smsConsent) {
    ph_json(['ok' => false, 'error' => 'Please check the SMS consent box to receive text alerts, or remove the phone number.'], 400);
}
$row = [gmdate('c'), $email, $smsConsent ? $phone : '', $area, implode('|', $topics)];
$line = implode(',', array_map(fn($v) => '"' . str_replace('"', '""', $v) . '"', $row)) . "\n";

$private = dirname(__DIR__, 2) . '/ph-private';
if (!is_dir($private)) {
    @mkdir($private, 0700, true);
}
if (is_dir($private) && is_writable($private)) {
    $file = $private . '/subscribers.csv';
    $header = "\"created_utc\",\"email\",\"sms_phone\",\"area\",\"topics\"\n";
} else {
    $file = __DIR__ . '/../data/subscribers.php';
    @mkdir(dirname($file), 0700, true);
    $header = "<?php http_response_code(404); exit; ?>\n\"created_utc\",\"email\",\"sms_phone\",\"area\",\"topics\"\n";
}
$new = !is_file($file);
if (@file_put_contents($file, ($new ? $header : '') . $line, FILE_APPEND | LOCK_EX) === false) {
    ph_json(['ok' => false, 'error' => 'Sign-ups are temporarily unavailable.'], 500);
}
ph_json(['ok' => true, 'email' => $email]);
