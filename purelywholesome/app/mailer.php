<?php
// Contact form and newsletter handling. Submissions are emailed to SITE_EMAIL and
// also appended to app/storage/*.php, which start with an exit guard so the
// files can't be read over HTTP even on hosts that ignore .htaccess.

function store_line(string $file, array $row): void
{
    $path = ROOT . '/app/storage/' . $file;
    if (!is_file($path)) {
        file_put_contents($path, "<?php exit; ?>\n");
    }
    file_put_contents($path, json_encode($row, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}

function too_fast(): bool
{
    $t = (int)($_POST['t'] ?? 0);
    return $t > 0 && time() - $t < 3;   // bots submit instantly
}

function handle_contact(array $f): array
{
    $errors = [];
    if (!empty($_POST['website']) || too_fast()) {
        return []; // honeypot: pretend success
    }
    if ($f['name'] === '' || mb_strlen($f['name']) > 80) $errors['name'] = 'Please tell us your name.';
    if (!filter_var($f['email'], FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Please enter a valid email address.';
    if (mb_strlen($f['message']) < 10) $errors['message'] = 'Please write a little more so we can help.';
    if (mb_strlen($f['message']) > 5000) $errors['message'] = 'Please keep your message under 5,000 characters.';
    if ($errors) return $errors;
    $topic = in_array($f['topic'], ['question', 'recipe', 'livestock', 'correction', 'other'], true) ? $f['topic'] : 'other';
    store_line('messages.php', ['at' => date('c'), 'name' => $f['name'], 'email' => $f['email'], 'topic' => $topic, 'message' => $f['message'], 'ip' => $_SERVER['REMOTE_ADDR'] ?? '']);
    $name = str_replace(["\r", "\n"], ' ', $f['name']);
    @mail(SITE_EMAIL, '[Purely Wholesome Farm] ' . ucfirst($topic) . ' from ' . $name, $f['message'] . "\n\n-- \n" . $name . ' <' . $f['email'] . '>',
        "From: Purely Wholesome Farm <no-reply@purelywholesome.com>\r\nReply-To: " . $f['email'] . "\r\nContent-Type: text/plain; charset=utf-8");
    return [];
}

function handle_subscribe(string $email, string $honeypot): bool
{
    if ($honeypot !== '') return true;
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) return false;
    store_line('subscribers.php', ['at' => date('c'), 'email' => $email]);
    return true;
}
