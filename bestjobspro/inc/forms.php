<?php
// Contact and job-application forms: validation, spam traps and email delivery.

const FORM_MIN_SECONDS = 4;     // humans take longer than this to fill a form
const RESUME_TYPES = [
    'pdf'  => ['application/pdf'],
    'doc'  => ['application/msword', 'application/octet-stream'],
    'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip', 'application/octet-stream'],
    'rtf'  => ['application/rtf', 'text/rtf', 'text/plain'],
    'txt'  => ['text/plain'],
];

function form_secret(): string
{
    // Optional inc/secret.php (not in git) can define FORM_SECRET; otherwise derive one per install.
    if (is_file(__DIR__ . '/secret.php')) {
        require_once __DIR__ . '/secret.php';
    }
    return defined('FORM_SECRET') ? FORM_SECRET : hash('sha256', __DIR__ . php_uname('n'));
}

/** Hidden fields: a honeypot and a signed timestamp. */
function form_guard_fields(): string
{
    $t = (string)time();
    $sig = hash_hmac('sha256', $t, form_secret());
    return '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
        . '<input type="hidden" name="_t" value="' . $t . '"><input type="hidden" name="_s" value="' . $sig . '">';
}

function form_is_spam(): bool
{
    if (!empty($_POST['website'])) {
        return true;
    }
    $t = (string)($_POST['_t'] ?? '');
    $s = (string)($_POST['_s'] ?? '');
    if (!ctype_digit($t) || !hash_equals(hash_hmac('sha256', $t, form_secret()), $s)) {
        return true;
    }
    $age = time() - (int)$t;
    return $age < FORM_MIN_SECONDS || $age > 86400;
}

function clean_line(string $key, int $max = 120): string
{
    $v = trim((string)($_POST[$key] ?? ''));
    $v = preg_replace('/[\r\n\t]+/', ' ', $v);
    return mb_substr($v, 0, $max);
}

function clean_text(string $key, int $max = 4000): string
{
    return mb_substr(trim(str_replace("\r", '', (string)($_POST[$key] ?? ''))), 0, $max);
}

function old(array $vals, string $key): string
{
    return e($vals[$key] ?? '');
}

/**
 * Send a plain-text email, optionally with one attachment.
 * $attach = ['name' => …, 'type' => …, 'data' => raw bytes]
 */
function send_mail(string $subject, string $text, string $replyTo, ?array $attach = null): bool
{
    $headers = [
        'From: ' . SITE_NAME . ' Website <' . FORM_FROM . '>',
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'X-Mailer: BestJobsPro-Site',
    ];
    if ($attach) {
        $b = 'bjp_' . bin2hex(random_bytes(12));
        $headers[] = 'Content-Type: multipart/mixed; boundary="' . $b . '"';
        $body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n" . $text . "\r\n"
            . "--$b\r\nContent-Type: " . $attach['type'] . '; name="' . $attach['name'] . "\"\r\n"
            . "Content-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"" . $attach['name'] . "\"\r\n\r\n"
            . chunk_split(base64_encode($attach['data'])) . "--$b--\r\n";
    } else {
        $headers[] = 'Content-Type: text/plain; charset=UTF-8';
        $body = $text;
    }
    $subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    return @mail(FORM_TO, $subject, $body, implode("\r\n", $headers), '-f' . FORM_FROM);
}

/** Returns [errors, values]. Redirects on success. */
function handle_contact_form(): array
{
    $v = [
        'first' => clean_line('first'), 'last' => clean_line('last'),
        'phone' => clean_line('phone', 40), 'email' => clean_line('email', 160),
        'role'  => clean_line('role', 20), 'message' => clean_text('message'),
    ];
    if (form_is_spam()) {
        redirect('/contact-us/?sent=1#contact-form', 303);
    }
    $err = [];
    if ($v['first'] === '') $err['first'] = 'Please enter your first name.';
    if ($v['last'] === '') $err['last'] = 'Please enter your last name.';
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $err['email'] = 'Please enter a valid email address.';
    if (!in_array($v['role'], ['Job seeker', 'Employer'], true)) $err['role'] = 'Tell us whether you are a job seeker or an employer.';
    if (mb_strlen($v['message']) < 10) $err['message'] = 'Please add a short message so we know how to help.';
    if ($err) {
        return [$err, $v];
    }
    $text = "New contact form message from bestjobspro.com\n\n"
        . "Name:  {$v['first']} {$v['last']}\nEmail: {$v['email']}\nPhone: {$v['phone']}\nI am a: {$v['role']}\n\n"
        . "Message:\n{$v['message']}\n\n--\nSent " . date('Y-m-d H:i T') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? '?');
    if (!send_mail("Website contact: {$v['first']} {$v['last']} ({$v['role']})", $text, $v['email'])) {
        return [['form' => 'Sorry, your message could not be sent. Please call us at ' . SITE_PHONE . ' or email ' . SITE_EMAIL . '.'], $v];
    }
    redirect('/contact-us/?sent=1#contact-form', 303);
}

function handle_application_form(): array
{
    $v = [
        'first' => clean_line('first'), 'middle' => clean_line('middle'), 'last' => clean_line('last'),
        'phone' => clean_line('phone', 40), 'email' => clean_line('email', 160),
        'job'   => clean_line('job', 80), 'other' => clean_line('other', 120),
        'source'=> clean_line('source', 60), 'message' => clean_text('message'),
    ];
    if (form_is_spam()) {
        redirect('/applications/?sent=1#apply-form', 303);
    }
    $jobs = array_merge(array_column(JOBS, 0), ['Other']);
    $err = [];
    if ($v['first'] === '') $err['first'] = 'Please enter your first name.';
    if ($v['last'] === '') $err['last'] = 'Please enter your last name.';
    if (!preg_match('/\d{3}.*\d{3}.*\d{4}/', $v['phone'])) $err['phone'] = 'Please enter a phone number we can reach you on.';
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $err['email'] = 'Please enter a valid email address.';
    if (!in_array($v['job'], $jobs, true)) $err['job'] = 'Please choose the job you are applying for.';
    if ($v['job'] === 'Other' && $v['other'] === '') $err['other'] = 'Tell us which job you are looking for.';

    $attach = null;
    $f = $_FILES['resume'] ?? null;
    if ($f && $f['error'] !== UPLOAD_ERR_NO_FILE) {
        $ext = strtolower(pathinfo($f['name'], PATHINFO_EXTENSION));
        if ($f['error'] === UPLOAD_ERR_INI_SIZE || $f['error'] === UPLOAD_ERR_FORM_SIZE || $f['size'] > RESUME_MAX_BYTES) {
            $err['resume'] = 'Your résumé is larger than 10 MB. Please upload a smaller file.';
        } elseif ($f['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($f['tmp_name'])) {
            $err['resume'] = 'The upload did not finish. Please try again.';
        } elseif (!isset(RESUME_TYPES[$ext])) {
            $err['resume'] = 'Please upload a PDF, Word (.doc/.docx), RTF or TXT file.';
        } else {
            $mime = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']) ?: 'application/octet-stream';
            if (!in_array($mime, RESUME_TYPES[$ext], true)) {
                $err['resume'] = 'That file does not look like a ' . strtoupper($ext) . ' document.';
            } else {
                $safe = preg_replace('/[^A-Za-z0-9._-]+/', '-', $v['first'] . '-' . $v['last']) . '-resume.' . $ext;
                $attach = ['name' => $safe, 'type' => $mime, 'data' => file_get_contents($f['tmp_name'])];
            }
        }
    }
    if ($err) {
        return [$err, $v];
    }
    $job = $v['job'] === 'Other' ? 'Other: ' . $v['other'] : $v['job'];
    $text = "New job application from bestjobspro.com\n\n"
        . "Name:   {$v['first']} {$v['middle']} {$v['last']}\nPhone:  {$v['phone']}\nEmail:  {$v['email']}\n"
        . "Job:    $job\nFound us via: {$v['source']}\nRésumé: " . ($attach ? 'attached' : 'not provided') . "\n\n"
        . "Skills / message:\n{$v['message']}\n\n--\nSent " . date('Y-m-d H:i T') . ' from ' . ($_SERVER['REMOTE_ADDR'] ?? '?');
    if (!send_mail("Job application: $job - {$v['first']} {$v['last']}", $text, $v['email'], $attach)) {
        return [['form' => 'Sorry, your application could not be sent. Please email it to ' . SITE_EMAIL . ' or call ' . SITE_PHONE . '.'], $v];
    }
    redirect('/applications/?sent=1#apply-form', 303);
}

function field_error(array $err, string $key): string
{
    return isset($err[$key]) ? '<p class="field__err" id="err-' . e($key) . '">' . e($err[$key]) . '</p>' : '';
}

function aria_err(array $err, string $key): string
{
    return isset($err[$key]) ? ' aria-invalid="true" aria-describedby="err-' . e($key) . '"' : '';
}
