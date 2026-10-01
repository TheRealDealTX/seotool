<?php
declare(strict_types=1);

defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)

use PHPMailer\PHPMailer\Exception as MailException;
use PHPMailer\PHPMailer\PHPMailer;

/**
 * Load SMTP settings. Looks in this order:
 *   1. the file named by the FR_MAIL_CONFIG environment variable
 *   2. app/config/mail.php
 * Returns null when no usable configuration exists.
 */
function mail_config(): ?array
{
    $candidates = array_filter([
        getenv('FR_MAIL_CONFIG') ?: null,
        FR_APP . '/config/mail.php',
    ]);
    foreach ($candidates as $file) {
        if (is_file($file)) {
            $cfg = require $file;
            if (is_array($cfg)) {
                // Estimate requests go here unless mail.php overrides it.
                $cfg['recipient'] = ($cfg['recipient'] ?? '') ?: 'teamwriteforus.today@gmail.com';
                return $cfg;
            }
        }
    }
    return null;
}

function mail_is_configured(?array $cfg = null): bool
{
    $cfg ??= mail_config();
    if (!$cfg) {
        return false;
    }
    foreach (['recipient', 'host', 'port', 'username', 'password', 'from_email'] as $k) {
        if (empty($cfg[$k])) {
            return false;
        }
    }
    return $cfg['password'] !== 'CHANGE-ME'
        && filter_var($cfg['recipient'], FILTER_VALIDATE_EMAIL)
        && filter_var($cfg['from_email'], FILTER_VALIDATE_EMAIL);
}

/**
 * Send an estimate request via authenticated SMTP.
 * Returns true only when the SMTP server accepted the message.
 */
function send_estimate_email(array $data): bool
{
    $cfg = mail_config();
    if (!mail_is_configured($cfg)) {
        app_log('mail', 'Estimate email NOT sent: SMTP is not configured (see config/mail.example.php).');
        return false;
    }

    $mail = new PHPMailer(true);
    try {
        $mail->isSMTP();
        $mail->Host       = (string) $cfg['host'];
        $mail->Port       = (int) $cfg['port'];
        $mail->SMTPAuth   = true;
        $mail->Username   = (string) $cfg['username'];
        $mail->Password   = (string) $cfg['password'];
        $enc = strtolower((string) ($cfg['encryption'] ?? 'ssl'));
        $mail->SMTPSecure = $enc === 'tls' ? PHPMailer::ENCRYPTION_STARTTLS : ($enc === 'none' ? '' : PHPMailer::ENCRYPTION_SMTPS);
        if ($enc === 'none') {
            $mail->SMTPAutoTLS = false; // only for local testing against a dev SMTP sink
        }
        $mail->Timeout    = (int) ($cfg['timeout'] ?? 15);
        $mail->CharSet    = PHPMailer::CHARSET_UTF8;
        $mail->XMailer    = ' '; // don't advertise the library version

        // Sender is always the authenticated domain mailbox.
        $mail->setFrom((string) $cfg['from_email'], (string) ($cfg['from_name'] ?? config('name')), false);
        $mail->Sender = (string) $cfg['from_email'];
        $mail->addAddress((string) $cfg['recipient']);
        // The visitor's validated email is only used as Reply-To.
        if ($data['email'] !== '') {
            $mail->addReplyTo($data['email'], $data['name']);
        }

        $serviceLabel = service_options()[$data['service']] ?? 'Roofing';
        // clean_line() already removed CR/LF; PHPMailer also encodes headers.
        $mail->Subject = 'Estimate request: ' . $serviceLabel . ' - ' . $data['name'];

        $rows = [
            'Name'                   => $data['name'],
            'Phone'                  => $data['phone'],
            'Email'                  => $data['email'] !== '' ? $data['email'] : '(not provided)',
            'Property address / ZIP' => $data['location'],
            'Service needed'         => $serviceLabel,
            'Consent to contact'     => 'Yes',
            'Submitted'              => date('F j, Y g:i a T'),
            'Page'                   => $data['source'],
        ];
        $text = "New estimate request from friendswoodroofs.com\n\n";
        $html = '<h2 style="font-family:Arial,sans-serif;color:#0f2340">New estimate request</h2><table cellpadding="6" style="font-family:Arial,sans-serif;border-collapse:collapse">';
        foreach ($rows as $label => $value) {
            $text .= $label . ': ' . $value . "\n";
            $html .= '<tr><th align="left" style="border-bottom:1px solid #ddd">' . e($label) . '</th><td style="border-bottom:1px solid #ddd">' . e($value) . '</td></tr>';
        }
        $html .= '</table>';
        $message = $data['message'] !== '' ? $data['message'] : '(no message)';
        $text .= "\nMessage:\n" . $message . "\n";
        $html .= '<h3 style="font-family:Arial,sans-serif">Message</h3><p style="font-family:Arial,sans-serif;white-space:pre-wrap">' . nl2br(e($message)) . '</p>';
        if ($data['phone'] !== '') {
            $html .= '<p style="font-family:Arial,sans-serif"><a href="tel:' . e(preg_replace('/[^0-9+]/', '', $data['phone'])) . '">Call ' . e($data['name']) . '</a></p>';
        }

        $mail->isHTML(true);
        $mail->Body    = $html;
        $mail->AltBody = $text;

        $mail->send();
        return true;
    } catch (MailException $ex) {
        // Log the transport error only - never the submission or credentials.
        app_log('mail', 'Estimate email failed: ' . $mail->ErrorInfo);
        return false;
    }
}
