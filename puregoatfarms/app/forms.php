<?php
// Contact and newsletter form handlers. Submissions are emailed to SITE_EMAIL
// and appended to a private log (outside the web root when the host allows).
defined('PGF') || exit;

function storage_dir(): string
{
    $outside = dirname(DOCROOT) . '/pgf-storage';
    if (is_dir($outside) || @mkdir($outside, 0750, true)) {
        if (is_writable($outside)) return $outside;
    }
    return DOCROOT . '/storage';
}

// Each log is a .php file that exits immediately, so it is never readable over HTTP.
function store_line(string $file, array $row): void
{
    $path = storage_dir() . "/$file.php";
    if (!is_file($path)) {
        @file_put_contents($path, "<?php exit; ?>\n", LOCK_EX);
    }
    @file_put_contents($path, json_encode($row, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}

function client_ip(): string
{
    return $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
}

// Simple per-IP throttle: at most $max submissions per hour.
function throttled(string $bucket, int $max = 5): bool
{
    // Stored as .php with an exit guard so it is never readable over HTTP.
    $path = storage_dir() . '/throttle-' . $bucket . '.php';
    $guard = "<?php exit; ?>\n";
    $now = time();
    $data = is_file($path) ? (json_decode(substr((string) @file_get_contents($path), strlen($guard)), true) ?: []) : [];
    $key = hash('sha256', strtok(client_ip(), ','));
    $hits = array_values(array_filter($data[$key] ?? [], fn($t) => $t > $now - 3600));
    if (count($hits) >= $max) return true;
    $hits[] = $now;
    $data[$key] = $hits;
    foreach ($data as $k => $v) {
        if (!array_filter($v, fn($t) => $t > $now - 3600)) unset($data[$k]);
    }
    @file_put_contents($path, $guard . json_encode($data), LOCK_EX);
    return false;
}

function looks_like_bot(): bool
{
    // Honeypot filled in, or form submitted faster than a human could type.
    $ts = (int) ($_POST['ts'] ?? 0);
    return !empty($_POST['website']) || ($ts && time() - $ts < 3);
}

function clean(string $key, int $max): string
{
    return trim(mb_substr(str_replace(["\r", "\0"], '', (string) ($_POST[$key] ?? '')), 0, $max));
}

function send_mail(string $subject, string $body, string $replyTo = ''): bool
{
    $headers = [
        'From: Pure Goat Farms <no-reply@' . SITE_HOST . '>',
        'Content-Type: text/plain; charset=UTF-8',
    ];
    if ($replyTo && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    return @mail(SITE_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
}

const CONTACT_TOPICS = ['Goat Breeds', 'Health & Care', 'Milking & Dairy', 'Kidding Season', 'Farm Life', 'Something else'];

function handle_contact(): void
{
    $name = clean('name', 100);
    $email = clean('email', 200);
    $topic = clean('topic', 40);
    $message = clean('message', 5000);

    if (looks_like_bot()) redirect('/contact/?sent=1', 303);

    $errors = [];
    if ($name === '') $errors[] = 'Please add your name.';
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
    if (!in_array($topic, CONTACT_TOPICS, true)) $topic = 'Something else';
    if (mb_strlen($message) < 10) $errors[] = 'Please write a little more in your message.';
    if (!$errors && throttled('contact')) $errors[] = 'Too many messages from your connection. Please try again later or email us directly.';

    if ($errors) {
        http_response_code(422);
        echo page_file('contact', ['errors' => $errors, 'old' => compact('name', 'email', 'topic', 'message')]);
        return;
    }

    store_line('contact', ['at' => date('c'), 'name' => $name, 'email' => $email, 'topic' => $topic, 'message' => $message]);
    send_mail("[Pure Goat Farms] $topic — $name", "Name: $name\nEmail: $email\nTopic: $topic\n\n$message\n", $email);
    redirect('/contact/?sent=1', 303);
}

function handle_subscribe(): void
{
    $email = clean('email', 200);
    $back = parse_url($_SERVER['HTTP_REFERER'] ?? '/', PHP_URL_PATH) ?: '/';
    if (!str_starts_with($back, '/') || str_starts_with($back, '//')) $back = '/';

    if (!looks_like_bot() && filter_var($email, FILTER_VALIDATE_EMAIL) && !throttled('subscribe', 3)) {
        store_line('subscribers', ['at' => date('c'), 'email' => $email]);
        send_mail('[Pure Goat Farms] New newsletter subscriber', "New subscriber: $email\n");
        redirect($back . '?subscribed=1#newsletter', 303);
    }
    redirect($back . '?subscribed=0#newsletter', 303);
}
