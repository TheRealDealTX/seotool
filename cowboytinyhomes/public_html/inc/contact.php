<?php
// Contact-form handling: validate, spam-check, email the lead and keep a copy.
//
// Every lead is appended to inc/data/leads.csv (inc/ is denied to the web by
// .htaccess) before the email is attempted, so nothing is lost if mail fails.

const LEAD_FIELDS = [
    'form', 'first_name', 'middle_name', 'last_name', 'phone', 'email', 'city', 'city_other',
    'project_type', 'remodel_area', 'remodel_other', 'address', 'own_property', 'contact_pref', 'message',
];

function contact_clean(string $v, int $max = 2000): string
{
    $v = trim(str_replace(["\r\n", "\r"], "\n", $v));
    $v = preg_replace('/[^\P{C}\n\t]/u', '', $v) ?? '';   // drop control chars except newline/tab
    return mb_substr($v, 0, $max);
}

/** @return array{ok: bool, errors: string[], values: array<string,string>} */
function handle_contact(array $post): array
{
    $v = [];
    foreach (LEAD_FIELDS as $f) {
        $v[$f] = contact_clean((string)($post[$f] ?? ''), $f === 'message' ? 5000 : 200);
    }
    $errors = [];

    // Spam traps: hidden honeypot field and a minimum time on the page.
    $ts = (int)($post['ts'] ?? 0);
    if (($post['website'] ?? '') !== '' || ($ts > 0 && time() - $ts < 3)) {
        return ['ok' => true, 'errors' => [], 'values' => []];   // pretend success; drop silently
    }

    if ($v['first_name'] === '') $errors[] = 'Please enter your name.';
    if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
    if (strlen(preg_replace('/\D/', '', $v['phone'])) < 10) $errors[] = 'Please enter a phone number with area code.';
    if (preg_match_all('#https?://#i', $v['message']) > 2) $errors[] = 'Please remove the links from your message.';
    if ($errors) return ['ok' => false, 'errors' => $errors, 'values' => $v];

    $labels = [
        'form' => 'Form', 'first_name' => 'First name', 'middle_name' => 'Middle name', 'last_name' => 'Last name',
        'phone' => 'Phone', 'email' => 'Email', 'city' => 'City', 'city_other' => 'Other city',
        'project_type' => 'Project type', 'remodel_area' => 'Area to remodel', 'remodel_other' => 'Other area',
        'address' => 'Project address', 'own_property' => 'Owns the property', 'contact_pref' => 'Preferred contact',
        'message' => 'Goals / message',
    ];
    $body = "New website lead from cowboytinyhomes.com\n\n";
    foreach ($labels as $k => $label) {
        if ($v[$k] !== '') $body .= str_pad($label . ':', 20) . ($k === 'message' ? "\n" : '') . $v[$k] . "\n";
    }
    $body .= "\nSubmitted: " . date('Y-m-d H:i:s T') . "\nPage: " . ($_SERVER['HTTP_REFERER'] ?? '/contact-us/') . "\n";

    // 1) Keep a copy.
    $dir = __DIR__ . '/data';
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    if (!is_file($dir . '/.htaccess')) @file_put_contents($dir . '/.htaccess', "Require all denied\n");
    $fh = @fopen($dir . '/leads.csv', 'ab');
    if ($fh) {
        if (flock($fh, LOCK_EX)) {
            if (ftell($fh) === 0 || filesize($dir . '/leads.csv') === 0) fputcsv($fh, array_merge(['submitted'], LEAD_FIELDS));
            fputcsv($fh, array_merge([date('c')], array_map(fn($f) => $v[$f], LEAD_FIELDS)));
            flock($fh, LOCK_UN);
        }
        fclose($fh);
    }

    // 2) Email it.
    $name = trim($v['first_name'] . ' ' . $v['last_name']);
    $what = $v['project_type'] ?: ($v['form'] === 'remodel' ? 'Remodel' : 'Design & Build');
    $subject = 'New lead: ' . $what . ' — ' . $name . ($v['city'] ? ' (' . $v['city'] . ')' : '');
    $safeName = preg_replace('/[^\p{L}\p{N} .\'-]/u', '', $name);
    $headers = implode("\r\n", [
        'From: ' . SITE_NAME . ' Website <' . MAIL_FROM . '>',
        'Reply-To: ' . ($safeName ? '"' . $safeName . '" ' : '') . '<' . $v['email'] . '>',
        'Content-Type: text/plain; charset=UTF-8',
        'X-Mailer: PHP',
    ]);
    @mail(LEAD_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . MAIL_FROM);

    return ['ok' => true, 'errors' => [], 'values' => $v];
}
