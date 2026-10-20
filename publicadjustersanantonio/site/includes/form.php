<?php
/**
 * Free Claim Review form: tokens, rate limiting, validation, and delivery.
 */

declare(strict_types=1);

require_once __DIR__ . '/functions.php';

/** Per-installation secret used to sign form tokens (auto-created, never public). */
function app_secret(): string
{
    static $secret = null;
    if ($secret !== null) {
        return $secret;
    }
    $file = data_path('.secret');
    if (is_file($file)) {
        $secret = trim((string) file_get_contents($file));
    }
    if (!$secret) {
        $secret = bin2hex(random_bytes(32));
        @file_put_contents($file, $secret, LOCK_EX);
        @chmod($file, 0600);
    }
    return $secret;
}

/**
 * Stateless signed CSRF token: "<timestamp>.<nonce>.<hmac>".
 * Works with page caching because the JavaScript also fetches a fresh token.
 */
function form_token(): string
{
    $ts = (string) time();
    $nonce = bin2hex(random_bytes(8));
    $sig = hash_hmac('sha256', $ts . '.' . $nonce, app_secret());
    return $ts . '.' . $nonce . '.' . $sig;
}

/** Returns '' when valid, otherwise an error code. */
function verify_form_token(string $token): string
{
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return 'token_invalid';
    }
    [$ts, $nonce, $sig] = $parts;
    if (!ctype_digit($ts) || !ctype_xdigit($nonce)) {
        return 'token_invalid';
    }
    $expected = hash_hmac('sha256', $ts . '.' . $nonce, app_secret());
    if (!hash_equals($expected, $sig)) {
        return 'token_invalid';
    }
    $age = time() - (int) $ts;
    if ($age < (int) cfg('min_fill_seconds', 3)) {
        return 'too_fast';
    }
    if ($age > 86400 * 2) {
        return 'token_expired';
    }
    // One-time use: remember nonces for 2 days.
    $dir = data_path('ratelimit');
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    $nfile = $dir . '/nonce-' . $nonce;
    if (is_file($nfile)) {
        return 'token_reused';
    }
    @touch($nfile);
    return '';
}

function client_ip(): string
{
    // Hostinger's CDN passes the visitor address in these headers.
    foreach (['HTTP_CF_CONNECTING_IP', 'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'] as $h) {
        if (!empty($_SERVER[$h])) {
            $ip = trim(explode(',', (string) $_SERVER[$h])[0]);
            if (filter_var($ip, FILTER_VALIDATE_IP)) {
                return $ip;
            }
        }
    }
    return '0.0.0.0';
}

/** File-based sliding-window rate limit. Returns true when the request is allowed. */
function rate_limit_ok(string $bucket, int $max, int $window): bool
{
    $dir = data_path('ratelimit');
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    $file = $dir . '/' . $bucket . '-' . hash('sha256', client_ip() . app_secret()) . '.json';
    $fp = @fopen($file, 'c+');
    if (!$fp) {
        return true; // fail open rather than block real visitors
    }
    flock($fp, LOCK_EX);
    $raw = stream_get_contents($fp);
    $hits = $raw ? (json_decode($raw, true) ?: []) : [];
    $now = time();
    $hits = array_values(array_filter($hits, fn($t) => $t > $now - $window));
    $ok = count($hits) < $max;
    if ($ok) {
        $hits[] = $now;
    }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($hits));
    flock($fp, LOCK_UN);
    fclose($fp);
    return $ok;
}

/** Remove stale nonce and rate-limit files (called from cron). */
function cleanup_ratelimit_dir(): int
{
    $n = 0;
    foreach (glob(data_path('ratelimit') . '/*') ?: [] as $f) {
        if (is_file($f) && filemtime($f) < time() - 86400 * 3) {
            @unlink($f);
            $n++;
        }
    }
    return $n;
}

function clean_text(string $s, int $max): string
{
    $s = str_replace("\0", '', $s);
    $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $s) ?? '';
    $s = trim($s);
    return mb_substr($s, 0, $max);
}

function clean_line(string $s, int $max): string
{
    // Single-line fields: strip CR/LF so nothing can be injected into mail headers.
    return clean_text(str_replace(["\r", "\n"], ' ', $s), $max);
}

/**
 * Validate the submitted form. Returns [array $data, array $errors].
 */
function validate_claim_form(array $post): array
{
    $allowedTypes = ['Hail damage', 'Wind / storm damage', 'Hurricane / tropical storm', 'Roof damage', 'Fire damage', 'Smoke damage', 'Water damage', 'Flood-related', 'Commercial property', 'Other'];
    $allowedStatus = ['Not filed yet', 'Filed - waiting on insurer', 'Inspection completed', 'Claim denied', 'Claim underpaid / low offer', 'Claim delayed', 'Claim closed / settled', 'Other'];

    $d = [
        'full_name'    => clean_line((string) ($post['full_name'] ?? ''), 100),
        'email'        => clean_line((string) ($post['email'] ?? ''), 150),
        'phone'        => clean_line((string) ($post['phone'] ?? ''), 30),
        'location'     => clean_line((string) ($post['location'] ?? ''), 80),
        'claim_type'   => clean_line((string) ($post['claim_type'] ?? ''), 60),
        'insurer'      => clean_line((string) ($post['insurer'] ?? ''), 100),
        'claim_status' => clean_line((string) ($post['claim_status'] ?? ''), 60),
        'date_of_loss' => clean_line((string) ($post['date_of_loss'] ?? ''), 10),
        'message'      => clean_text((string) ($post['message'] ?? ''), 4000),
        'privacy_ack'  => !empty($post['privacy_ack']),
        'page_context' => clean_line((string) ($post['page_context'] ?? ''), 150),
    ];
    $err = [];
    if (mb_strlen($d['full_name']) < 2) {
        $err['full_name'] = 'Please enter your full name.';
    }
    if (!filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
        $err['email'] = 'Please enter a valid email address.';
    }
    $digits = preg_replace('/\D/', '', $d['phone']);
    if (strlen($digits) < 10 || strlen($digits) > 15) {
        $err['phone'] = 'Please enter a valid phone number, including area code.';
    }
    if (mb_strlen($d['location']) < 2) {
        $err['location'] = 'Please enter the property city or ZIP code.';
    }
    if (!in_array($d['claim_type'], $allowedTypes, true)) {
        $err['claim_type'] = 'Please choose a claim type.';
    }
    if (!in_array($d['claim_status'], $allowedStatus, true)) {
        $err['claim_status'] = 'Please choose the claim status.';
    }
    if ($d['date_of_loss'] !== '') {
        $dt = DateTime::createFromFormat('Y-m-d', $d['date_of_loss']);
        if (!$dt || $dt->format('Y-m-d') !== $d['date_of_loss'] || $dt > new DateTime('tomorrow')) {
            $err['date_of_loss'] = 'Please enter a valid date of loss (or leave it blank).';
        }
    }
    if (mb_strlen($d['message']) < 10) {
        $err['message'] = 'Please describe what happened (at least a sentence).';
    }
    if (!$d['privacy_ack']) {
        $err['privacy_ack'] = 'Please confirm the privacy acknowledgement.';
    }
    // Basic link-spam heuristic.
    if (preg_match_all('#https?://#i', $d['message']) > 3) {
        $err['message'] = 'Please remove the links from your message.';
    }
    return [$d, $err];
}

/**
 * Validate uploaded files. Returns [array $files, ?string $error].
 * Files are attached to the email straight from PHP's temp folder and never
 * stored in the website.
 */
function validate_uploads(): array
{
    if (!cfg('uploads_enabled') || empty($_FILES['attachments']) || !is_array($_FILES['attachments']['name'])) {
        return [[], null];
    }
    $allowed = [
        'image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp',
        'image/heic' => 'heic', 'image/heif' => 'heif', 'application/pdf' => 'pdf',
    ];
    $f = $_FILES['attachments'];
    $out = [];
    $total = 0;
    $finfo = function_exists('finfo_open') ? finfo_open(FILEINFO_MIME_TYPE) : null;
    foreach ($f['name'] as $i => $name) {
        $errCode = $f['error'][$i] ?? UPLOAD_ERR_NO_FILE;
        if ($errCode === UPLOAD_ERR_NO_FILE || $name === '') {
            continue;
        }
        if ($errCode !== UPLOAD_ERR_OK) {
            return [[], 'One of the files could not be uploaded. Please try a smaller file.'];
        }
        if (count($out) >= (int) cfg('upload_max_files')) {
            return [[], 'Please attach no more than ' . (int) cfg('upload_max_files') . ' files.'];
        }
        $tmp = $f['tmp_name'][$i];
        $size = (int) $f['size'][$i];
        if (!is_uploaded_file($tmp)) {
            return [[], 'Upload rejected.'];
        }
        if ($size <= 0 || $size > (int) cfg('upload_max_bytes')) {
            return [[], 'Each file must be smaller than ' . (int) (cfg('upload_max_bytes') / 1048576) . ' MB.'];
        }
        $total += $size;
        if ($total > (int) cfg('upload_total_bytes')) {
            return [[], 'The attached files are too large in total.'];
        }
        $mime = $finfo ? (string) finfo_file($finfo, $tmp) : '';
        // Some servers report HEIC as application/octet-stream; allow by extension + magic bytes.
        $ext = strtolower(pathinfo((string) $name, PATHINFO_EXTENSION));
        if (!isset($allowed[$mime])) {
            $head = (string) @file_get_contents($tmp, false, null, 4, 8);
            if (in_array($ext, ['heic', 'heif'], true) && strpos($head, 'ftyp') === 0) {
                $mime = 'image/heic';
            } else {
                return [[], 'Only JPG, PNG, WEBP, HEIC, or PDF files are accepted.'];
            }
        }
        $safe = preg_replace('/[^A-Za-z0-9._-]+/', '-', pathinfo((string) $name, PATHINFO_FILENAME));
        $safe = trim(substr((string) $safe, 0, 60), '-.') ?: 'attachment';
        $out[] = ['tmp' => $tmp, 'name' => $safe . '.' . $allowed[$mime], 'mime' => $mime, 'size' => $size];
    }
    return [$out, null];
}

/** Build and send the notification. Returns true only when the mail server accepted it. */
function send_claim_email(array $d, array $files): bool
{
    require_once __DIR__ . '/lib/PHPMailer/Exception.php';
    require_once __DIR__ . '/lib/PHPMailer/PHPMailer.php';
    require_once __DIR__ . '/lib/PHPMailer/SMTP.php';

    $rows = [
        'Name'             => $d['full_name'],
        'Email'            => $d['email'],
        'Phone'            => $d['phone'],
        'Property city/ZIP'=> $d['location'],
        'Claim type'       => $d['claim_type'],
        'Claim status'     => $d['claim_status'],
        'Insurance company'=> $d['insurer'] ?: '—',
        'Date of loss'     => $d['date_of_loss'] ? format_date($d['date_of_loss']) : '—',
        'Submitted from'   => $d['page_context'] ?: '—',
        'Submitted at'     => date('F j, Y g:i A T'),
        'Attachments'      => $files ? count($files) . ' file(s)' : 'None',
    ];
    $html = '<h2 style="font-family:Arial,sans-serif;color:#10243A">New Free Claim Review request</h2><table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse">';
    $text = "New Free Claim Review request\n\n";
    foreach ($rows as $k => $v) {
        $html .= '<tr><td style="border-bottom:1px solid #eee"><strong>' . e($k) . '</strong></td><td style="border-bottom:1px solid #eee">' . e($v) . '</td></tr>';
        $text .= $k . ': ' . $v . "\n";
    }
    $html .= '</table><h3 style="font-family:Arial,sans-serif;color:#10243A">Message</h3><p style="font-family:Arial,sans-serif;font-size:14px;white-space:pre-wrap">' . nl2br(e($d['message'])) . '</p>';
    $text .= "\nMessage:\n" . $d['message'] . "\n";

    $mail = new PHPMailer\PHPMailer\PHPMailer(true);
    try {
        $mail->CharSet = 'UTF-8';
        $useSmtp = cfg('smtp_pass') !== '' && cfg('smtp_host') !== '';
        if ($useSmtp) {
            $mail->isSMTP();
            $mail->Host = cfg('smtp_host');
            $mail->Port = (int) cfg('smtp_port');
            $mail->SMTPAuth = cfg('smtp_user') !== '';
            $mail->Username = cfg('smtp_user');
            $mail->Password = cfg('smtp_pass');
            if (cfg('smtp_secure') === 'none') {
                // Only for local testing against a mail sink.
                $mail->SMTPSecure = '';
                $mail->SMTPAutoTLS = false;
            } else {
                $mail->SMTPSecure = cfg('smtp_secure') === 'tls' ? PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS : PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS;
            }
            $mail->SMTPDebug = (int) cfg('smtp_debug');
            $mail->Timeout = 20;
        } elseif (cfg('allow_mail_fallback')) {
            $mail->isMail();
        } else {
            log_line('mail', 'SMTP password not configured; message not sent.');
            return false;
        }
        $mail->setFrom(cfg('mail_from'), cfg('mail_from_name'));
        $mail->addAddress(cfg('mail_to'));
        $mail->addReplyTo($d['email'], $d['full_name']);
        $mail->Subject = 'Free Claim Review: ' . $d['claim_type'] . ' - ' . $d['full_name'] . ' (' . $d['location'] . ')';
        $mail->isHTML(true);
        $mail->Body = $html;
        $mail->AltBody = $text;
        foreach ($files as $file) {
            $mail->addAttachment($file['tmp'], $file['name'], PHPMailer\PHPMailer\PHPMailer::ENCODING_BASE64, $file['mime']);
        }
        $mail->send();
        log_line('mail', 'Claim review delivered (' . $d['claim_type'] . ', ' . count($files) . ' attachment(s)).');
        return true;
    } catch (Throwable $ex) {
        // Log the technical reason only; never log the visitor's message.
        log_line('mail', 'Delivery failed: ' . $mail->ErrorInfo . ' ' . $ex->getMessage());
        return false;
    }
}
