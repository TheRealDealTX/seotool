<?php
// Form handling: contact + newsletter. Every submission is emailed to the site mailbox via SMTP.
declare(strict_types=1);
require_once APP . '/mailer.php';

function handle_form(string $path): void {
    $form = (string) ($_POST['form'] ?? '');
    $wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
    $back = $form === 'contact' ? '/contact-us/' : (parse_url($_SERVER['HTTP_REFERER'] ?? '', PHP_URL_PATH) ?: '/');
    if (!in_array($form, ['contact', 'subscribe'], true)) { http_response_code(405); exit; }

    $result = process_form($form);
    if ($wantsJson) {
        header('Content-Type: application/json');
        http_response_code($result['ok'] ? 200 : 422);
        echo json_encode($result);
        return;
    }
    $sep = str_contains($back, '?') ? '&' : '?';
    header('Location: ' . SITE_URL . $back . $sep . ($result['ok'] ? 'sent=' . $form : 'error=' . urlencode($result['message'])) . '#' . $form, true, 303);
}

function process_form(string $form): array {
    $name  = trim(mb_substr((string) ($_POST['name'] ?? ''), 0, 120));
    $email = trim(mb_substr((string) ($_POST['email'] ?? ''), 0, 200));
    $msg   = trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 5000));
    $subj  = trim(mb_substr((string) ($_POST['subject'] ?? ''), 0, 150));

    // Spam traps: hidden honeypot field + signed timestamp (rejects instant/replayed posts).
    if (($_POST['website'] ?? '') !== '' || !csrf_ok((string) ($_POST['tk'] ?? ''))) {
        return ['ok' => true, 'message' => 'Thank you!']; // silently drop bots
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) return ['ok' => false, 'message' => 'Please enter a valid email address.'];
    if ($form === 'contact' && ($name === '' || mb_strlen($msg) < 5)) return ['ok' => false, 'message' => 'Please add your name and a message.'];
    if (preg_match_all('#https?://#i', $msg) > 3) return ['ok' => false, 'message' => 'Please limit links in your message.'];
    if (!rate_ok()) return ['ok' => false, 'message' => 'Too many submissions. Please try again later.'];

    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
    $page = (string) ($_POST['page'] ?? '');
    if ($form === 'contact') {
        $subject = 'Contact form: ' . ($subj !== '' ? $subj : 'Message from ' . $name);
        $body = "New message from the Thought Changer contact form\n\n"
              . "Name:    $name\nEmail:   $email\n" . ($subj !== '' ? "Subject: $subj\n" : '')
              . "\n$msg\n\n---\nSent " . date('Y-m-d H:i T') . " from " . SITE_URL . "/contact-us/ (IP $ip)\n";
    } else {
        $subject = 'Newsletter signup: ' . $email;
        $body = "New newsletter signup on Thought Changer\n\nEmail: $email\n" . ($name !== '' ? "Name:  $name\n" : '')
              . "Page:  $page\n\n---\nSent " . date('Y-m-d H:i T') . " (IP $ip)\n";
    }
    $cfg = config();
    $ok = (new Mailer($cfg))->send($cfg['mail_to'], $subject, $body, $email, $name ?: null);
    if (!$ok) {
        // Never lose a submission: keep a private copy outside the web root.
        @file_put_contents(private_dir() . '/tc-submissions.log', json_encode(['t' => date('c'), 'form' => $form, 'name' => $name, 'email' => $email, 'subject' => $subj, 'message' => $msg, 'page' => $page]) . "\n", FILE_APPEND | LOCK_EX);
        return ['ok' => false, 'message' => 'Sorry, something went wrong sending your message. Please email ' . SITE_EMAIL . ' directly.'];
    }
    return ['ok' => true, 'message' => $form === 'contact' ? 'Thank you — your message is on its way. We’ll reply soon.' : 'You’re in! Watch your inbox for the next thought.'];
}

function rate_ok(): bool {
    $dir = sys_get_temp_dir() . '/tc-rate';
    @mkdir($dir, 0700, true);
    $f = $dir . '/' . hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . 'tc');
    $hits = array_filter(array_map('intval', is_file($f) ? file($f, FILE_IGNORE_NEW_LINES) : []), fn($t) => $t > time() - 3600);
    if (count($hits) >= 6) return false;
    $hits[] = time();
    @file_put_contents($f, implode("\n", $hits));
    return true;
}
