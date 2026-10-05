<?php
// Form handling for /contact-us/ and /submit-property/. Messages are emailed to
// the site address and also appended to app/storage/submissions.log as a backup.

function form_handle($kind, array $fields) {
    csrf_token(); // start the session before any output
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') return null;
    $errors = [];
    if (!hash_equals($_SESSION['csrf'] ?? '', (string)($_POST['csrf'] ?? ''))) $errors[] = 'Your session expired. Please try again.';
    if (!empty($_POST['website_url'])) return ['ok' => true, 'values' => []]; // honeypot: pretend success
    if (time() - (int)($_POST['t'] ?? 0) < 3) $errors[] = 'Please take a moment to fill out the form.';
    $last = $_SESSION['last_submit'] ?? 0;
    if (time() - $last < 30) $errors[] = 'Please wait a few seconds before sending another message.';

    $v = [];
    foreach ($fields as $name => [$label, $required, $type]) {
        $val = trim((string)($_POST[$name] ?? ''));
        $val = mb_substr(str_replace(["\r\n", "\r"], "\n", $val), 0, $type === 'textarea' ? 5000 : 300);
        if ($type !== 'textarea') $val = str_replace("\n", ' ', $val);
        if ($required && $val === '') $errors[] = "$label is required.";
        if ($val !== '' && $type === 'email' && !filter_var($val, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
        if ($val !== '' && $type === 'url' && !filter_var($val, FILTER_VALIDATE_URL)) $errors[] = "$label must be a full link starting with https://";
        $v[$name] = $val;
    }
    if ($errors) return ['ok' => false, 'errors' => $errors, 'values' => $v];

    $subject = $kind === 'contact' ? 'Website message from ' . $v['name'] : 'New property submission: ' . $v['pname'];
    $body = '';
    foreach ($fields as $name => [$label]) $body .= "$label: " . ($v[$name] !== '' ? $v[$name] : '-') . "\n";
    $body .= "\nSent " . date('c') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? '?') . "\n";

    $dir = APP . '/storage';
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    @file_put_contents("$dir/submissions.log", json_encode(['kind' => $kind, 'at' => date('c'), 'ip' => $_SERVER['REMOTE_ADDR'] ?? null] + $v, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

    $to = cfg('email');
    $headers = 'From: ' . cfg('name') . ' <' . $to . ">\r\n" .
               'Reply-To: ' . preg_replace('/[\r\n]+/', '', $v['email']) . "\r\n" .
               "Content-Type: text/plain; charset=UTF-8\r\n";
    @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $to);
    $_SESSION['last_submit'] = time();
    return ['ok' => true, 'values' => []];
}

function form_field($name, $label, $type, $required, $value, $extra = '') {
    $id = 'f-' . $name;
    $req = $required ? ' required' : '';
    $star = $required ? ' <span class="req" aria-hidden="true">*</span>' : '';
    if ($type === 'textarea') $input = "<textarea id=\"$id\" name=\"$name\" rows=\"5\"$req $extra>" . e($value) . '</textarea>';
    else $input = "<input id=\"$id\" type=\"$type\" name=\"$name\" value=\"" . e($value) . "\"$req $extra>";
    return "<label class=\"field\" for=\"$id\"><span>" . e($label) . "$star</span>$input</label>";
}

function form_hidden() {
    return '<input type="hidden" name="csrf" value="' . e(csrf_token()) . '">' .
           '<input type="hidden" name="t" value="' . time() . '">' .
           '<label class="hp" aria-hidden="true">Leave this empty <input type="text" name="website_url" tabindex="-1" autocomplete="off"></label>';
}

function form_notice($res, $ok_msg) {
    if (!$res) return '';
    if ($res['ok']) return '<div class="notice notice-ok" role="status">' . icon('check') . ' ' . e($ok_msg) . '</div>';
    return '<div class="notice notice-err" role="alert"><strong>Please fix the following:</strong><ul>' . implode('', array_map(fn($x) => '<li>' . e($x) . '</li>', $res['errors'])) . '</ul></div>';
}
