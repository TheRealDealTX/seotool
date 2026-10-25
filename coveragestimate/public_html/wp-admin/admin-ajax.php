<?php
// Drop-in replacement for WordPress admin-ajax.php that handles Elementor Pro
// form submissions (action=elementor_pro_forms_send_form) and returns the same
// JSON shape Elementor's frontend script expects, so the forms behave as before.

$private = dirname(__DIR__) . '/ce-private';
header('Content-Type: application/json; charset=UTF-8');
header('X-Robots-Tag: noindex');

function ce_respond(bool $ok, string $message, array $errors = [], array $extra = []): void
{
    $data = ['message' => $message, 'data' => (object) $extra];
    if (!$ok) {
        $data['errors'] = (object) $errors;
    }
    echo json_encode(['success' => $ok, 'data' => $data]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || ($_POST['action'] ?? '') !== 'elementor_pro_forms_send_form') {
    http_response_code(400);
    header('Content-Type: text/plain; charset=UTF-8');
    echo '0';
    exit;
}

$forms = json_decode(file_get_contents($private . '/forms.json'), true);
$formId = (string) ($_POST['form_id'] ?? '');
if (!isset($forms[$formId])) {
    ce_respond(false, 'There’s something wrong. This form does not exist.');
}
$form = $forms[$formId];
$input = is_array($_POST['form_fields'] ?? null) ? $_POST['form_fields'] : [];

// Basic abuse protection: a per-IP rate limit (8 submissions per hour).
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);
$rateFile = sys_get_temp_dir() . '/ce_rate_' . md5($ip);
$hits = array_filter(array_map('intval', @file($rateFile, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600);
if (count($hits) >= 8) {
    ce_respond(false, $form['error_message']);
}
$hits[] = time();
@file_put_contents($rateFile, implode("\n", $hits));

// Validate like Elementor: required fields and email format.
$errors = [];
$values = [];
foreach ($form['fields'] as $field) {
    $raw = $input[$field['id']] ?? '';
    $value = is_array($raw) ? implode(', ', array_map('strval', $raw)) : trim((string) $raw);
    $value = mb_substr($value, 0, $field['type'] === 'textarea' ? 5000 : 300);
    if ($field['required'] && $value === '') {
        $errors[$field['id']] = $form['required_message'];
    } elseif ($field['type'] === 'email' && $value !== '' && !filter_var($value, FILTER_VALIDATE_EMAIL)) {
        $errors[$field['id']] = 'Invalid email address.';
    } elseif ($field['type'] === 'tel' && $value !== '' && !preg_match('/^[0-9()#&+*\-=. ]+$/', $value)) {
        $errors[$field['id']] = 'The field accepts only numbers and phone characters (#, -, *, etc).';
    }
    $values[] = ['id' => $field['id'], 'title' => $field['label'], 'value' => $value];
}
if ($errors) {
    ce_respond(false, $form['invalid_message'], $errors);
}

// Build the email body the way Elementor's [all-fields] + metadata does.
$tz = new DateTimeZone('-05:00'); // matches the WordPress site's UTC-5 setting
$now = new DateTime('now', $tz);
$esc = fn($s) => nl2br(htmlspecialchars($s, ENT_QUOTES, 'UTF-8'));
$lines = [];
foreach ($values as $v) {
    $lines[] = $esc($v['title']) . ': ' . $esc($v['value']);
}
$meta = [];
$pageUrl = (string) ($_POST['referrer'] ?? ($_SERVER['HTTP_REFERER'] ?? ''));
foreach ($form['metadata'] as $m) {
    if ($m === 'date') { $meta[] = 'Date: ' . $now->format('F j, Y'); }
    if ($m === 'time') { $meta[] = 'Time: ' . $now->format('g:i A'); }
    if ($m === 'page_url') { $meta[] = 'Page URL: ' . $esc($pageUrl); }
    if ($m === 'user_agent') { $meta[] = 'User Agent: ' . $esc($_SERVER['HTTP_USER_AGENT'] ?? ''); }
    if ($m === 'remote_ip') { $meta[] = 'Remote IP: ' . $esc($ip); }
}
$html = implode('<br>', $lines);
if ($meta) {
    $html .= '<br><br>---<br><br>' . implode('<br>', $meta);
}

$replyTo = null;
foreach ($values as $v) {
    if ($v['id'] === $form['email_reply_to'] && filter_var($v['value'], FILTER_VALIDATE_EMAIL)) {
        $replyTo = $v['value'];
    }
}

// Save a copy of every submission (replaces Elementor's Submissions screen).
$record = ['time' => $now->format(DATE_ATOM), 'form' => $form['name'], 'page' => $pageUrl, 'ip' => $ip, 'fields' => array_column($values, 'value', 'title')];
@file_put_contents($private . '/submissions.log', json_encode($record, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);

if (in_array('email', $form['actions'], true)) {
    $cfgFile = $private . '/mail-config.php';
    if (!is_file($cfgFile)) {
        ce_respond(false, $form['server_message']);
    }
    $cfg = require $cfgFile;
    require $private . '/smtp.php';
    $to = array_values(array_filter(array_map('trim', explode(',', $form['email_to']))));
    if (($cfg['host'] ?? '') === 'dryrun') {
        // Local testing only: record the message instead of sending it.
        @file_put_contents($private . '/dryrun-mail.log', json_encode(['to' => $to, 'subject' => $form['email_subject'], 'reply_to' => $replyTo, 'html' => $html]) . "\n", FILE_APPEND);
        $sent = true;
        $detail = 'dryrun';
    } else [$sent, $detail] = ce_smtp_send($cfg, $cfg['from'] ?? $form['email_from'], $form['email_from_name'], $to, $form['email_subject'], $html, $replyTo);
    if (!$sent) {
        @file_put_contents($private . '/mail-errors.log', $now->format(DATE_ATOM) . ' ' . str_replace("\n", ' | ', $detail) . "\n", FILE_APPEND | LOCK_EX);
        ce_respond(false, $form['server_message']);
    }
}

$extra = [];
if (!empty($form['popup_action'])) {
    $extra['popup'] = ['action' => $form['popup_action'], 'id' => ''];
}
ce_respond(true, $form['success_message'], [], $extra);
