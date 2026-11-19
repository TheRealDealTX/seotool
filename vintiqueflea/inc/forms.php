<?php
defined('INC') || exit;
/** Form handling: contact, vendor applications, newsletter. Submissions are emailed and logged to /data. */

function clean_field(string $k, int $max = 2000): string
{
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    return mb_substr(strip_tags($v), 0, $max);
}

function log_submission(string $file, array $row): void
{
    $row = ['time' => date('c'), 'ip_hash' => substr(hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . app_secret()), 0, 16)] + $row;
    // Stored as *.php with an exit header so the log can't be downloaded even without .htaccess support.
    $path = DATA_DIR . '/' . $file . '.php';
    if (!is_file($path)) {
        @file_put_contents($path, "<?php exit; ?>\n", LOCK_EX);
    }
    @file_put_contents($path, json_encode($row, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);
}

function send_form_mail(string $subject, array $fields, string $replyTo): bool
{
    require_once INC . '/mailer.php';
    $body = '';
    foreach ($fields as $k => $v) {
        $body .= ucfirst(str_replace('_', ' ', $k)) . ":\n" . $v . "\n\n";
    }
    $headers = [
        'From: ' . SITE_NAME . ' Website <' . CONTACT_FROM . '>',
        'Content-Type: text/plain; charset=UTF-8',
    ];
    if (filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    $subject = '=?UTF-8?B?' . base64_encode('[' . SITE_NAME . '] ' . preg_replace('/[\r\n]+/', ' ', $subject)) . '?=';
    if ($smtp = smtp_config()) {
        return smtp_send($smtp, CONTACT_TO, $subject, $body, $replyTo);
    }
    return @mail(CONTACT_TO, $subject, $body, implode("\r\n", $headers));
}

/**
 * Validate + process a form. Returns ['ok' => bool, 'errors' => [], 'values' => []].
 * $spec: field => [label, required(bool), maxlen, type('text'|'email')]
 */
function process_form(string $kind, array $spec): array
{
    $values = [];
    $errors = [];
    foreach ($spec as $k => [$label, $req, $max, $type]) {
        $values[$k] = clean_field($k, $max);
        if ($req && $values[$k] === '') {
            $errors[$k] = "Please enter your $label.";
        } elseif ($type === 'email' && $values[$k] !== '' && !filter_var($values[$k], FILTER_VALIDATE_EMAIL)) {
            $errors[$k] = 'Please enter a valid email address.';
        }
    }
    if (!empty($_POST['website'])) {               // honeypot
        return ['ok' => true, 'errors' => [], 'values' => []];
    }
    if (!csrf_valid($_POST['csrf'] ?? null)) {
        $errors['_form'] = 'Your session expired. Please submit the form again.';
    }
    $joined = implode(' ', $values);
    if (preg_match_all('~https?://~i', $joined) > 2) {
        $errors['_form'] = 'Please remove some links from your message.';
    }
    if ($errors) {
        return ['ok' => false, 'errors' => $errors, 'values' => $values];
    }
    $mailed = send_form_mail(ucfirst($kind) . ' from ' . ($values['name'] ?? 'website'), $values, $values['email'] ?? '');
    log_submission($kind . '.jsonl', $values + ['_mailed' => $mailed]);
    return ['ok' => true, 'errors' => [], 'values' => []];
}

function form_field(string $name, string $label, array $state, string $type = 'text', array $opts = []): string
{
    $val = e($state['values'][$name] ?? '');
    $err = $state['errors'][$name] ?? '';
    $req = !empty($opts['required']);
    $id = 'f-' . $name;
    $h = '<div class="field' . ($err ? ' field--error' : '') . '"><label for="' . $id . '">' . e($label) . ($req ? ' <span aria-hidden="true">*</span>' : '') . '</label>';
    $aria = $err ? ' aria-invalid="true" aria-describedby="' . $id . '-err"' : '';
    $common = ' id="' . $id . '" name="' . $name . '"' . ($req ? ' required' : '') . $aria . (isset($opts['autocomplete']) ? ' autocomplete="' . $opts['autocomplete'] . '"' : '');
    if ($type === 'textarea') {
        $h .= '<textarea' . $common . ' rows="' . ($opts['rows'] ?? 6) . '">' . $val . '</textarea>';
    } elseif ($type === 'select') {
        $h .= '<select' . $common . '>';
        foreach ($opts['options'] as $o) {
            $h .= '<option' . ($val === e($o) ? ' selected' : '') . '>' . e($o) . '</option>';
        }
        $h .= '</select>';
    } else {
        $h .= '<input type="' . $type . '"' . $common . ' value="' . $val . '">';
    }
    if ($err) {
        $h .= '<p class="field__err" id="' . $id . '-err">' . e($err) . '</p>';
    }
    return $h . '</div>';
}

function form_hidden(): string
{
    return '<input type="hidden" name="csrf" value="' . e(csrf_token()) . '">'
        . '<div class="hp" aria-hidden="true"><label>Leave blank<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>';
}

function handle_subscribe(): never
{
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        redirect('/events/');
    }
    $email = trim((string) ($_POST['email'] ?? ''));
    $ok = empty($_POST['website']) && csrf_valid($_POST['csrf'] ?? null) && filter_var($email, FILTER_VALIDATE_EMAIL);
    if ($ok) {
        log_submission('subscribers.jsonl', ['email' => mb_substr($email, 0, 200), 'source' => mb_substr((string) ($_POST['source'] ?? ''), 0, 60)]);
    }
    render('subscribed', ['ok' => (bool) $ok]);
}
