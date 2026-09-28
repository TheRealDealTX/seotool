<?php
// Claim-review form handler: validates, stores the lead privately, emails the
// configured recipient. Spam protection: honeypot, minimum fill time, per-IP
// rate limit. Claim documents are stored in sd-private/uploads/, never emailed
// or exposed publicly, and never sent to analytics.
require __DIR__ . '/lib.php';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') sd_json(['ok' => false, 'error' => 'Method not allowed.'], 405);

$fail = fn(string $msg, int $code = 400) => sd_json(['ok' => false, 'error' => $msg], $code);
$phoneMsg = ' Please call +1 (844) 537-1427 or email info@smokedamage.com.';

// Honeypot: bots fill every field. Pretend success so they learn nothing.
if (!empty($_POST['website'])) sd_json(['ok' => true]);
// Minimum fill time (3 s) - a human can't complete the form faster.
$started = (int)($_POST['started_at'] ?? 0);
if ($started > 0 && (microtime(true) * 1000 - $started) < 3000) sd_json(['ok' => true]);

if (!sd_private_dir()) $fail('The form is temporarily unavailable.' . $phoneMsg, 503);
if (!sd_rate_limit('lead', 5, 3600)) $fail('Too many requests from this connection. Please try again later, or call us.' . $phoneMsg, 429);

$statuses = ['Not Yet Filed', 'Claim Filed', 'Already Inspected', 'Partially Paid', 'Denied', 'Delayed', 'Underpaid', 'Closed Claim', 'Not Sure'];
$damages = ['Smoke', 'Soot', 'Fire', 'Odor', 'Contents', 'HVAC', 'Water From Fire Suppression', 'Commercial Loss', 'Other'];

$lead = [
    'full_name' => sd_clean($_POST['full_name'] ?? '', 120),
    'phone' => sd_clean($_POST['phone'] ?? '', 30),
    'email' => sd_clean($_POST['email'] ?? '', 160),
    'property_type' => sd_clean($_POST['property_type'] ?? '', 60),
    'city' => sd_clean($_POST['city'] ?? '', 80),
    'zip' => sd_clean($_POST['zip'] ?? '', 5),
    'date_of_loss' => sd_clean($_POST['date_of_loss'] ?? '', 10),
    'insurance_company' => sd_clean($_POST['insurance_company'] ?? '', 120),
    'claim_status' => in_array($_POST['claim_status'] ?? '', $statuses, true) ? $_POST['claim_status'] : '',
    'damage' => array_values(array_intersect($damages, array_map('strval', (array)($_POST['damage'] ?? [])))),
    'message' => sd_clean($_POST['message'] ?? '', 5000),
    'source' => preg_replace('/[^a-z0-9-]/i', '', substr((string)($_POST['source'] ?? ''), 0, 40)),
];

if ($lead['full_name'] === '') $fail('Please enter your name.');
if (strlen(preg_replace('/\D/', '', $lead['phone'])) < 10) $fail('Please enter a 10-digit phone number.');
if (!filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) $fail('Please enter a valid email address.');
if ($lead['city'] === '') $fail('Please enter the Texas city where the property is located.');
if ($lead['zip'] !== '' && !preg_match('/^\d{5}$/', $lead['zip'])) $fail('ZIP code should be 5 digits.');
if ($lead['date_of_loss'] !== '' && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $lead['date_of_loss'])) $lead['date_of_loss'] = '';
// Link-stuffed messages are spam.
if (preg_match_all('#https?://#i', $lead['message']) > 3) sd_json(['ok' => true]);

$id = date('Ymd-His') . '-' . bin2hex(random_bytes(4));
$lead['id'] = $id;
$lead['received_at'] = date('c');
$lead['status'] = 'new';
$lead['ip_hash'] = hash('sha256', sd_client_ip() . date('Y-m'));
$lead['user_agent'] = sd_clean($_SERVER['HTTP_USER_AGENT'] ?? '', 200);
$lead['referrer'] = sd_clean($_SERVER['HTTP_REFERER'] ?? '', 200);

// ------------------------------------------------------------------ uploads
$allowed = ['pdf' => ['application/pdf'], 'jpg' => ['image/jpeg'], 'jpeg' => ['image/jpeg'], 'png' => ['image/png'],
    'webp' => ['image/webp'], 'heic' => ['image/heic', 'image/heif', 'application/octet-stream'], 'heif' => ['image/heif', 'image/heic', 'application/octet-stream'],
    'doc' => ['application/msword', 'application/octet-stream', 'application/x-ole-storage', 'application/CDFV2'],
    'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip', 'application/octet-stream'],
    'xls' => ['application/vnd.ms-excel', 'application/octet-stream', 'application/x-ole-storage', 'application/CDFV2'],
    'xlsx' => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'application/octet-stream'],
    'txt' => ['text/plain']];
$lead['files'] = [];
if (!empty($_FILES['files']) && is_array($_FILES['files']['name'])) {
    $n = count($_FILES['files']['name']);
    $total = 0;
    if ($n > 8) $fail('Please attach up to 8 files.');
    $finfo = function_exists('finfo_open') ? finfo_open(FILEINFO_MIME_TYPE) : null;
    for ($i = 0; $i < $n; $i++) {
        $err = $_FILES['files']['error'][$i];
        if ($err === UPLOAD_ERR_NO_FILE) continue;
        if ($err !== UPLOAD_ERR_OK) $fail('One of the files could not be uploaded. Try smaller files, or email them to info@smokedamage.com.');
        $tmp = $_FILES['files']['tmp_name'][$i];
        $size = (int)$_FILES['files']['size'][$i];
        $total += $size;
        if ($total > 20 * 1024 * 1024) $fail('Attachments must total 20 MB or less.');
        $orig = sd_clean(basename((string)$_FILES['files']['name'][$i]), 150);
        $ext = strtolower(pathinfo($orig, PATHINFO_EXTENSION));
        if (!isset($allowed[$ext])) $fail('Unsupported file type: ' . h($orig) . '. Please use PDF, images, Word or Excel files.');
        $mime = $finfo ? finfo_file($finfo, $tmp) : 'application/octet-stream';
        if (!in_array($mime, $allowed[$ext], true)) $fail('The file ' . h($orig) . ' does not look like a valid ' . strtoupper($ext) . ' file.');
        $stored = bin2hex(random_bytes(12)) . '.' . $ext;
        $dest = sd_path("uploads/$id");
        if (!is_dir($dest)) @mkdir($dest, 0750, true);
        if (!move_uploaded_file($tmp, "$dest/$stored")) $fail('A file could not be saved.' . $phoneMsg, 500);
        $lead['files'][] = ['name' => $orig, 'stored' => $stored, 'size' => $size, 'mime' => $mime];
    }
}

if (!sd_write_json("leads/$id.json", $lead)) $fail('We could not save your request.' . $phoneMsg, 500);

// ------------------------------------------------------------------ email
$s = sd_settings();
$to = filter_var($s['lead_recipient'] ?? '', FILTER_VALIDATE_EMAIL) ? $s['lead_recipient'] : 'info@smokedamage.com';
$line = fn($k, $v) => str_pad($k . ':', 20) . ($v === '' ? '—' : $v) . "\n";
$body = "New claim review request from SmokeDamage.com\n\n"
    . $line('Name', $lead['full_name']) . $line('Phone', $lead['phone']) . $line('Email', $lead['email'])
    . $line('Property type', $lead['property_type']) . $line('Texas city', $lead['city']) . $line('ZIP', $lead['zip'])
    . $line('Date of loss', $lead['date_of_loss']) . $line('Insurance company', $lead['insurance_company'])
    . $line('Claim status', $lead['claim_status']) . $line('Damage types', implode(', ', $lead['damage']))
    . $line('Source', $lead['source']) . $line('Attachments', (string)count($lead['files']))
    . "\nWhat happened:\n" . ($lead['message'] ?: '—') . "\n\n"
    . "Lead ID: $id\nView in admin (attachments are stored privately there): https://smokedamage.com/admin/?s=lead&id=" . rawurlencode($id) . "\n";
$subject = 'Claim review request: ' . preg_replace('/[\r\n]+/', ' ', $lead['full_name'] . ' — ' . $lead['city'] . ($lead['claim_status'] ? ' (' . $lead['claim_status'] . ')' : ''));
[$sent, $info] = sd_send_mail($to, $subject, $body, $lead['email']);
$lead['email_sent'] = $sent;
$lead['email_info'] = $info;
sd_write_json("leads/$id.json", $lead);

sd_json(['ok' => true, 'id' => $id]);
