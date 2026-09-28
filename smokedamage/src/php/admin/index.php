<?php
// SmokeDamage.com admin: leads, blog + keyword queue, event scans, locations,
// SEO metadata, redirects, settings and automation status.
//
// Content itself is authored in the git repository (content/*.md) and built to
// static HTML; the admin manages runtime data and queues requests that the weekly
// automation applies on its next run.
require_once __DIR__ . '/../api/lib.php';

header('X-Robots-Tag: noindex, nofollow');
header('X-Frame-Options: DENY');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'");

sd_session_start();
$priv = sd_private_dir();
$S = $_GET['s'] ?? 'dashboard';
$msg = '';
$err = '';

// ------------------------------------------------------------------ auth
$auth = sd_read_json('admin.json', []);
if (isset($_GET['logout'])) { $_SESSION = []; session_destroy(); header('Location: /admin/'); exit; }
if (($_POST['action'] ?? '') === 'login') {
    if (!sd_rate_limit('admin-login', 8, 900)) { $err = 'Too many attempts. Wait 15 minutes.'; }
    elseif (!empty($auth['password_hash']) && hash_equals((string)($auth['username'] ?? 'admin'), (string)($_POST['username'] ?? ''))
        && password_verify((string)($_POST['password'] ?? ''), $auth['password_hash'])) {
        session_regenerate_id(true);
        $_SESSION['admin'] = $auth['username'] ?? 'admin';
        $_SESSION['admin_until'] = time() + 8 * 3600;
        header('Location: /admin/'); exit;
    } else { $err = 'Incorrect username or password.'; }
}

function layout_head(string $title): void { ?>
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title><?= h($title) ?> · SmokeDamage.com Admin</title>
<style>
:root{--o:#FF6D1F;--c:#222;--cr:#FAF3E1;--s:#F5E7C6;--m:#6C665E;--l:rgba(34,34,34,.12)}
*{box-sizing:border-box}body{margin:0;font:15px/1.55 system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:var(--cr);color:var(--c)}
a{color:#9E3B09}header{background:var(--c);color:#fff;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
header a{color:#fff;text-decoration:none}header strong{font-size:16px}
.wrap{display:grid;grid-template-columns:220px 1fr;min-height:calc(100vh - 50px)}@media(max-width:800px){.wrap{grid-template-columns:1fr}}
nav{background:#fff;border-right:1px solid var(--l);padding:14px}nav a{display:block;padding:8px 12px;border-radius:8px;text-decoration:none;color:var(--c);font-weight:600}
nav a.on,nav a:hover{background:var(--s)}main{padding:24px;min-width:0}h1{margin:0 0 16px;font-size:24px}h2{font-size:18px;margin:26px 0 10px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}.card{background:#fff;border:1px solid var(--l);border-radius:12px;padding:16px}
.card small{display:block;color:var(--m);font-weight:700;text-transform:uppercase;font-size:11px;letter-spacing:.06em}.card b{font-size:20px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--l);border-radius:10px;overflow:hidden;font-size:14px}
th,td{padding:8px 10px;border-bottom:1px solid var(--l);text-align:left;vertical-align:top}th{background:var(--s);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.tw{overflow-x:auto}.ok{color:#1E6B2F;font-weight:700}.bad{color:#B3261E;font-weight:700}.warn{color:#9E3B09;font-weight:700}
input,select,textarea{font:inherit;padding:8px 10px;border:1px solid #bbb;border-radius:8px;background:#fff;max-width:100%}
button,.btn{font:inherit;font-weight:700;padding:8px 14px;border-radius:999px;border:0;background:var(--o);color:#1b1b1b;cursor:pointer;text-decoration:none;display:inline-block}
.btn2{background:#fff;border:1px solid #bbb}.msg{padding:10px 14px;border-radius:8px;background:#EAF6EC;margin-bottom:14px}.err{background:#FDECEA}
form.inline{display:inline}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}label{font-weight:600}
.pill{display:inline-block;padding:2px 8px;border-radius:999px;background:var(--s);font-size:12px;font-weight:700}
.login{max-width:360px;margin:12vh auto;background:#fff;padding:28px;border-radius:16px;border:1px solid var(--l)}
.login input{width:100%;margin:6px 0 12px}pre{white-space:pre-wrap;background:#fff;border:1px solid var(--l);padding:12px;border-radius:8px}
dl.kv{display:grid;grid-template-columns:180px 1fr;gap:6px 12px;background:#fff;border:1px solid var(--l);border-radius:10px;padding:14px}dl.kv dt{font-weight:700;color:var(--m)}dl.kv dd{margin:0}
</style></head><body>
<?php }

if (!$priv) {
    layout_head('Setup required');
    echo '<div class="login"><h1>Setup required</h1><p>The private data directory (sd-private next to public_html) is missing or not writable. Leads cannot be stored until it exists.</p></div></body></html>';
    exit;
}
if (!sd_admin_logged_in()) {
    layout_head('Sign in'); ?>
<form class="login" method="post" autocomplete="on"><h1>Admin sign in</h1>
<?php if ($err) echo '<p class="msg err">' . h($err) . '</p>'; ?>
<?php if (empty($auth['password_hash'])) echo '<p class="msg err">No admin credentials are configured yet (sd-private/admin.json).</p>'; ?>
<label for="u">Username</label><input id="u" name="username" autocomplete="username" required>
<label for="p">Password</label><input id="p" name="password" type="password" autocomplete="current-password" required>
<input type="hidden" name="action" value="login"><button type="submit">Sign in</button></form></body></html>
<?php exit; }

$_SESSION['admin_until'] = time() + 8 * 3600;
$csrf = sd_csrf();
$manifest = sd_read_json('site-manifest.json', []);
$settings = sd_settings();

// ------------------------------------------------------------------ helpers
function leads_all(): array {
    $dir = sd_path('leads');
    $out = [];
    foreach (glob($dir . '/*.json') ?: [] as $f) {
        $l = json_decode((string)file_get_contents($f), true);
        if (is_array($l) && !empty($l['id'])) $out[] = $l;
    }
    usort($out, fn($a, $b) => strcmp($b['id'], $a['id']));
    return $out;
}
function safe_id(string $id): bool { return (bool)preg_match('/^\d{8}-\d{6}-[0-9a-f]{8}$/', $id); }
function queue_request(string $type, array $data): bool {
    $q = sd_read_json('requests.json', []);
    $q[] = ['id' => bin2hex(random_bytes(5)), 'type' => $type, 'data' => $data, 'requested_at' => date('c'), 'by' => $_SESSION['admin'] ?? 'admin', 'status' => 'pending'];
    return sd_write_json('requests.json', $q);
}
function csv_cell($v): string { $v = (string)$v; if (preg_match('/^[=+\-@]/', $v)) $v = "'" . $v; return '"' . str_replace('"', '""', $v) . '"'; }
function csrf_field(): string { return '<input type="hidden" name="csrf" value="' . h($_SESSION['csrf']) . '">'; }
function when(?string $iso): string { if (!$iso) return '—'; $t = strtotime($iso); return $t ? date('M j, Y g:ia', $t) : h($iso); }

// ------------------------------------------------------------------ actions (POST)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && ($_POST['action'] ?? '') !== 'login') {
    if (!sd_check_csrf()) { $err = 'Your session expired. Please try again.'; }
    else {
        $a = $_POST['action'] ?? '';
        if ($a === 'lead_status' && safe_id($_POST['id'] ?? '')) {
            $l = sd_read_json('leads/' . $_POST['id'] . '.json', null);
            if ($l) { $l['status'] = in_array($_POST['status'], ['new', 'contacted', 'qualified', 'signed', 'not a fit', 'spam'], true) ? $_POST['status'] : 'new';
                $l['notes'] = sd_clean($_POST['notes'] ?? ($l['notes'] ?? ''), 4000); sd_write_json('leads/' . $l['id'] . '.json', $l); $msg = 'Lead updated.'; }
        } elseif ($a === 'settings') {
            $new = sd_read_json('settings.json', []);
            $rec = trim((string)($_POST['lead_recipient'] ?? ''));
            if (!filter_var($rec, FILTER_VALIDATE_EMAIL)) $err = 'Lead recipient must be a valid email address.';
            else {
                $new['lead_recipient'] = $rec;
                $new['popup_enabled'] = !empty($_POST['popup_enabled']);
                $new['popup_delay_seconds'] = max(0, min(120, (int)($_POST['popup_delay_seconds'] ?? 5)));
                $mf = trim((string)($_POST['mail_from'] ?? ''));
                if ($mf !== '' && filter_var($mf, FILTER_VALIDATE_EMAIL)) $new['mail_from'] = $mf;
                sd_write_json('settings.json', $new); $msg = 'Settings saved. They apply immediately.';
            }
        } elseif ($a === 'site_change') {
            $fields = ['phone_display', 'email', 'licensed_address', 'blog_author', 'ga4_id', 'gsc_verification', 'bing_verification', 'social'];
            $data = [];
            foreach ($fields as $f) if (isset($_POST[$f]) && trim($_POST[$f]) !== '') $data[$f] = sd_clean($_POST[$f], 300);
            if ($data) { queue_request('site_settings', $data); $msg = 'Change request queued. The next automation run applies it and rebuilds the site.'; }
        } elseif ($a === 'password') {
            $p1 = (string)($_POST['p1'] ?? '');
            if (strlen($p1) < 14) $err = 'Use at least 14 characters.';
            elseif ($p1 !== ($_POST['p2'] ?? '')) $err = 'Passwords do not match.';
            elseif (!password_verify((string)($_POST['current'] ?? ''), $auth['password_hash'] ?? '')) $err = 'Current password is incorrect.';
            else { $auth['password_hash'] = password_hash($p1, PASSWORD_DEFAULT); $auth['changed_at'] = date('c'); sd_write_json('admin.json', $auth); $msg = 'Password changed.'; }
        } elseif ($a === 'redirect_add') {
            $from = '/' . ltrim(trim((string)$_POST['from']), '/');
            $to = trim((string)$_POST['to']);
            $code = in_array((int)$_POST['code'], [301, 302, 307, 308], true) ? (int)$_POST['code'] : 301;
            if (!preg_match('#^/[A-Za-z0-9/_\-.%]*$#', $from) || $from === '/') $err = 'The "from" path must be a site path like /old-page/.';
            elseif (!preg_match('#^(/|https://)#', $to)) $err = 'The destination must start with / or https://';
            else { $r = sd_read_json('redirects.json', []); $r = array_values(array_filter($r, fn($x) => ($x['from'] ?? '') !== $from));
                $r[] = ['from' => $from, 'to' => $to, 'code' => $code, 'added' => date('c')]; sd_write_json('redirects.json', $r); $msg = 'Redirect saved.'; }
        } elseif ($a === 'redirect_del') {
            $r = sd_read_json('redirects.json', []); $from = (string)$_POST['from'];
            sd_write_json('redirects.json', array_values(array_filter($r, fn($x) => ($x['from'] ?? '') !== $from))); $msg = 'Redirect removed.';
        } elseif ($a === 'keyword_import' && !empty($_FILES['csv']['tmp_name']) && is_uploaded_file($_FILES['csv']['tmp_name'])) {
            $fh = fopen($_FILES['csv']['tmp_name'], 'r');
            $head = array_map(fn($x) => strtolower(trim(preg_replace('/^\xEF\xBB\xBF/', '', (string)$x))), fgetcsv($fh, null, ',', '"', '') ?: []);
            $ki = array_search('keyword', $head, true);
            $vi = array_search('volume', $head, true); $di = array_search('keyword difficulty', $head, true); if ($di === false) $di = array_search('kd', $head, true);
            $ci = array_search('cpc (usd)', $head, true); if ($ci === false) $ci = array_search('cpc', $head, true);
            $ii = array_search('intent', $head, true);
            if ($ki === false) $err = 'The CSV needs a "Keyword" column (SEMrush exports work as-is).';
            else {
                $q = sd_read_json('keyword-imports.json', []); $seen = array_flip(array_map(fn($x) => strtolower($x['keyword']), $q)); $n = 0;
                while (($row = fgetcsv($fh, null, ',', '"', '')) !== false && $n < 5000) {
                    $kw = strtolower(trim((string)($row[$ki] ?? ''))); if ($kw === '' || isset($seen[$kw])) continue;
                    // Volumes/KD/CPC are copied from the uploaded file only - never estimated.
                    $q[] = ['keyword' => $kw, 'volume' => $vi !== false ? ($row[$vi] ?? '') : '', 'kd' => $di !== false ? ($row[$di] ?? '') : '',
                        'cpc' => $ci !== false ? ($row[$ci] ?? '') : '', 'intent' => $ii !== false ? ($row[$ii] ?? '') : '', 'status' => 'imported', 'imported_at' => date('c')];
                    $seen[$kw] = 1; $n++;
                }
                sd_write_json('keyword-imports.json', $q); $msg = "$n keywords imported into the queue.";
            }
        } elseif ($a === 'keyword_status') {
            $q = sd_read_json('keyword-imports.json', []);
            foreach ($q as &$k) if ($k['keyword'] === ($_POST['keyword'] ?? '')) $k['status'] = in_array($_POST['status'], ['imported', 'priority', 'skip'], true) ? $_POST['status'] : 'imported';
            unset($k); sd_write_json('keyword-imports.json', $q); $msg = 'Keyword updated.';
        } elseif ($a === 'seo_change') {
            $path = (string)($_POST['path'] ?? '');
            $data = ['path' => $path];
            if (trim($_POST['title'] ?? '') !== '') $data['title'] = sd_clean($_POST['title'], 120);
            if (trim($_POST['description'] ?? '') !== '') $data['description'] = sd_clean($_POST['description'], 300);
            if (count($data) > 1) { queue_request('seo_metadata', $data); $msg = 'SEO change queued for ' . $path . '. It will be applied and published on the next automation run.'; }
        } elseif ($a === 'approve') {
            $kind = in_array($_POST['kind'] ?? '', ['event', 'blog'], true) ? $_POST['kind'] : '';
            if ($kind) { queue_request('publish_' . $kind, ['source' => (string)$_POST['source'], 'decision' => $_POST['decision'] === 'reject' ? 'reject' : 'publish']); $msg = 'Decision queued for the next automation run.'; }
        } elseif ($a === 'request_cancel') {
            $q = sd_read_json('requests.json', []);
            foreach ($q as &$r) if ($r['id'] === ($_POST['id'] ?? '') && $r['status'] === 'pending') $r['status'] = 'cancelled';
            unset($r); sd_write_json('requests.json', $q); $msg = 'Request cancelled.';
        }
    }
}

// ------------------------------------------------------------------ file download / CSV export (GET)
if ($S === 'file' && safe_id($_GET['id'] ?? '')) {
    $l = sd_read_json('leads/' . $_GET['id'] . '.json', null);
    foreach (($l['files'] ?? []) as $f) {
        if ($f['stored'] === ($_GET['f'] ?? '')) {
            $p = sd_path('uploads/' . $l['id'] . '/' . $f['stored']);
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename="' . preg_replace('/[^A-Za-z0-9._ -]/', '_', $f['name']) . '"');
            header('Content-Length: ' . filesize($p));
            readfile($p); exit;
        }
    }
    http_response_code(404); exit('Not found');
}
if ($S === 'leads_csv') {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="smokedamage-leads-' . date('Y-m-d') . '.csv"');
    $cols = ['id', 'received_at', 'status', 'full_name', 'phone', 'email', 'property_type', 'city', 'zip', 'date_of_loss', 'insurance_company', 'claim_status', 'damage', 'source', 'message', 'notes'];
    echo implode(',', $cols) . "\r\n";
    foreach (leads_all() as $l) { echo implode(',', array_map(fn($c) => csv_cell(is_array($l[$c] ?? '') ? implode('; ', $l[$c]) : ($l[$c] ?? '')), $cols)) . "\r\n"; }
    exit;
}

// ------------------------------------------------------------------ page
$nav = ['dashboard' => 'Dashboard', 'leads' => 'Leads', 'blog' => 'Blog queue', 'keywords' => 'SEMrush keyword queue', 'events' => 'Event scans & events',
    'locations' => 'Location pages', 'seo' => 'SEO metadata', 'redirects' => 'Redirects', 'requests' => 'Automation requests', 'settings' => 'Site settings'];
layout_head($nav[$S] ?? 'Admin');
$auto = $manifest['automation'] ?? [];
$scan = $manifest['event_scan'] ?? [];
?>
<header><strong><a href="/admin/">SmokeDamage.com Admin</a></strong><span><a href="/" target="_blank" rel="noopener">View site</a> · <a href="/admin/?logout=1">Sign out</a></span></header>
<div class="wrap"><nav aria-label="Admin"><?php foreach ($nav as $k => $v) echo '<a href="/admin/?s=' . $k . '"' . ($S === $k || ($S === 'lead' && $k === 'leads') ? ' class="on"' : '') . '>' . h($v) . '</a>'; ?></nav>
<main>
<?php if ($msg) echo '<p class="msg">' . h($msg) . '</p>'; if ($err) echo '<p class="msg err">' . h($err) . '</p>';

if ($S === 'dashboard'):
    $leads = leads_all(); $new = count(array_filter($leads, fn($l) => ($l['status'] ?? '') === 'new'));
    $pend = count(array_filter(sd_read_json('requests.json', []), fn($r) => $r['status'] === 'pending'));
    $semrush = !empty($auto['semrush_connected']); ?>
<h1>Dashboard</h1>
<div class="cards">
<div class="card"><small>New leads</small><b><?= $new ?></b> <span class="pill"><?= count($leads) ?> total</span></div>
<div class="card"><small>Last event scan</small><b><?= h($auto['last_event_scan'] ?? ($scan['last_scan'] ?? '—')) ?></b></div>
<div class="card"><small>Next event scan</small><b><?= h($auto['next_event_scan'] ?? '—') ?></b></div>
<div class="card"><small>Last blog generated</small><b><?= h($auto['last_blog_generated'] ?? '—') ?></b></div>
<div class="card"><small>Next blog generation</small><b><?= h($auto['next_blog_generation'] ?? '—') ?></b></div>
<div class="card"><small>SEMrush</small><b class="<?= $semrush ? 'ok' : 'bad' ?>"><?= $semrush ? 'Connected' : 'Not connected' ?></b></div>
<div class="card"><small>Pending automation requests</small><b><?= $pend ?></b></div>
<div class="card"><small>Site last built</small><b style="font-size:15px"><?= when($manifest['built_at'] ?? null) ?></b></div>
</div>
<?php if (!empty($auto['notes'])) echo '<h2>Automation notes</h2><pre>' . h(is_array($auto['notes']) ? implode("\n", $auto['notes']) : $auto['notes']) . '</pre>'; ?>
<h2>Recent leads</h2>
<div class="tw"><table><tr><th>Received</th><th>Name</th><th>City</th><th>Claim status</th><th>Status</th></tr>
<?php foreach (array_slice($leads, 0, 8) as $l) echo '<tr><td>' . when($l['received_at']) . '</td><td><a href="/admin/?s=lead&id=' . h($l['id']) . '">' . h($l['full_name']) . '</a></td><td>' . h($l['city']) . '</td><td>' . h($l['claim_status']) . '</td><td><span class="pill">' . h($l['status']) . '</span></td></tr>'; ?>
</table></div>

<?php elseif ($S === 'leads'): $leads = leads_all(); ?>
<h1>Leads</h1><p><a class="btn btn2" href="/admin/?s=leads_csv">Export CSV</a> Lead notifications go to <b><?= h($settings['lead_recipient']) ?></b>.</p>
<div class="tw"><table><tr><th>Received</th><th>Name</th><th>Phone</th><th>Email</th><th>City</th><th>Property</th><th>Claim status</th><th>Damage</th><th>Files</th><th>Emailed</th><th>Status</th></tr>
<?php foreach ($leads as $l) echo '<tr><td>' . when($l['received_at']) . '</td><td><a href="/admin/?s=lead&id=' . h($l['id']) . '">' . h($l['full_name']) . '</a></td><td><a href="tel:' . h(preg_replace('/[^\d+]/', '', $l['phone'])) . '">' . h($l['phone']) . '</a></td><td><a href="mailto:' . h($l['email']) . '">' . h($l['email']) . '</a></td><td>' . h($l['city']) . '</td><td>' . h($l['property_type']) . '</td><td>' . h($l['claim_status']) . '</td><td>' . h(implode(', ', $l['damage'] ?? [])) . '</td><td>' . count($l['files'] ?? []) . '</td><td>' . (!empty($l['email_sent']) ? '<span class="ok">yes</span>' : '<span class="bad">no</span>') . '</td><td><span class="pill">' . h($l['status']) . '</span></td></tr>';
if (!$leads) echo '<tr><td colspan="11">No leads yet.</td></tr>'; ?>
</table></div>

<?php elseif ($S === 'lead' && safe_id($_GET['id'] ?? '')): $l = sd_read_json('leads/' . $_GET['id'] . '.json', null); if (!$l) { echo '<p>Not found.</p>'; } else { ?>
<h1><?= h($l['full_name']) ?></h1>
<dl class="kv"><?php foreach (['received_at' => 'Received', 'phone' => 'Phone', 'email' => 'Email', 'property_type' => 'Property type', 'city' => 'Texas city', 'zip' => 'ZIP', 'date_of_loss' => 'Date of loss', 'insurance_company' => 'Insurance company', 'claim_status' => 'Claim status', 'source' => 'Source', 'referrer' => 'Referrer'] as $k => $lab) echo '<dt>' . h($lab) . '</dt><dd>' . h($k === 'received_at' ? when($l[$k]) : ($l[$k] ?? '')) . '</dd>'; ?>
<dt>Damage types</dt><dd><?= h(implode(', ', $l['damage'] ?? [])) ?></dd><dt>Email notification</dt><dd><?= !empty($l['email_sent']) ? 'Sent' : '<span class="bad">Not sent — follow up from here</span>' ?></dd></dl>
<h2>What happened</h2><pre><?= h($l['message'] ?: '—') ?></pre>
<h2>Documents</h2><?php if (empty($l['files'])) echo '<p>None uploaded.</p>'; else { echo '<ul>'; foreach ($l['files'] as $f) echo '<li><a href="/admin/?s=file&id=' . h($l['id']) . '&f=' . h($f['stored']) . '">' . h($f['name']) . '</a> (' . round($f['size'] / 1024) . ' KB)</li>'; echo '</ul>'; } ?>
<h2>Follow-up</h2><form method="post"><?= csrf_field() ?><input type="hidden" name="action" value="lead_status"><input type="hidden" name="id" value="<?= h($l['id']) ?>">
<div class="row"><label for="st">Status</label><select id="st" name="status"><?php foreach (['new', 'contacted', 'qualified', 'signed', 'not a fit', 'spam'] as $o) echo '<option' . ($o === $l['status'] ? ' selected' : '') . '>' . $o . '</option>'; ?></select></div>
<label for="nt">Internal notes</label><br><textarea id="nt" name="notes" rows="5" style="width:100%"><?= h($l['notes'] ?? '') ?></textarea><div class="row"><button>Save</button></div></form>
<?php } ?>

<?php elseif ($S === 'blog'): $blog = $manifest['blog'] ?? []; ?>
<h1>Blog queue</h1>
<p>One article is researched, written and checked each week by the automation (SEMrush-informed when connected). Posts that fail the pre-publish check are saved as drafts and listed here for review.</p>
<div class="tw"><table><tr><th>Status</th><th>Title</th><th>Focus keyword</th><th>Published</th><th>Check notes</th><th></th></tr>
<?php foreach ($blog as $p) { $st = $p['status'] ?? 'published';
echo '<tr><td><span class="pill">' . h($st) . '</span></td><td>' . ($st === 'published' ? '<a href="' . h($p['path']) . '" target="_blank">' . h($p['title']) . '</a>' : h($p['title'])) . '</td><td>' . h($p['keyword']) . '</td><td>' . h($p['published']) . '</td><td>' . h($p['check'] ?? '') . '</td><td>';
if ($st !== 'published') echo '<form class="inline" method="post">' . csrf_field() . '<input type="hidden" name="action" value="approve"><input type="hidden" name="kind" value="blog"><input type="hidden" name="source" value="' . h($p['source']) . '"><button name="decision" value="publish">Approve</button> <button class="btn2" name="decision" value="reject">Reject</button></form>';
echo '</td></tr>'; } if (!$blog) echo '<tr><td colspan="6">No posts yet.</td></tr>'; ?></table></div>
<p><a href="/admin/?s=keywords">Keyword queue →</a></p>

<?php elseif ($S === 'keywords'): $kq = $manifest['keyword_queue'] ?? []; $imp = sd_read_json('keyword-imports.json', []); ?>
<h1>SEMrush keyword queue</h1>
<p>SEMrush API: <b class="<?= !empty($auto['semrush_connected']) ? 'ok' : 'bad' ?>"><?= !empty($auto['semrush_connected']) ? 'Connected (weekly pull by the automation)' : 'Not connected — import a SEMrush CSV below' ?></b>. Volumes, difficulty and CPC shown here come only from SEMrush data; nothing is estimated.</p>
<h2>Import a keyword CSV</h2>
<form method="post" enctype="multipart/form-data"><?= csrf_field() ?><input type="hidden" name="action" value="keyword_import"><div class="row"><input type="file" name="csv" accept=".csv,text/csv" required><button>Import</button></div></form>
<?php if ($imp) { ?><h2>Imported keywords (<?= count($imp) ?>)</h2><div class="tw"><table><tr><th>Keyword</th><th>Volume</th><th>KD</th><th>CPC</th><th>Intent</th><th>Status</th></tr>
<?php foreach (array_slice($imp, 0, 300) as $k) echo '<tr><td>' . h($k['keyword']) . '</td><td>' . h($k['volume']) . '</td><td>' . h($k['kd']) . '</td><td>' . h($k['cpc']) . '</td><td>' . h($k['intent']) . '</td><td><form class="inline" method="post">' . csrf_field() . '<input type="hidden" name="action" value="keyword_status"><input type="hidden" name="keyword" value="' . h($k['keyword']) . '"><select name="status" onchange="this.form.submit()">' . implode('', array_map(fn($o) => '<option' . ($o === $k['status'] ? ' selected' : '') . '>' . $o . '</option>', ['imported', 'priority', 'skip'])) . '</select></form></td></tr>'; ?>
</table></div><?php } ?>
<h2>Editorial queue (from the repository)</h2>
<div class="tw"><table><tr><th>Keyword</th><th>Volume</th><th>KD</th><th>Cluster</th><th>Proposed title</th><th>Status</th><th>Conflict</th></tr>
<?php foreach ($kq as $k) echo '<tr><td>' . h($k['keyword'] ?? '') . '</td><td>' . h($k['volume'] ?? '') . '</td><td>' . h($k['kd'] ?? '') . '</td><td>' . h($k['cluster'] ?? '') . '</td><td>' . h($k['proposed_title'] ?? '') . '</td><td><span class="pill">' . h($k['status'] ?? '') . '</span></td><td>' . h($k['target_page_conflict'] ?? '') . '</td></tr>'; ?>
</table></div>

<?php elseif ($S === 'events'): $ev = $manifest['events'] ?? []; ?>
<h1>Event scans &amp; events</h1>
<dl class="kv"><dt>Last scan</dt><dd><?= h($scan['last_scan'] ?? '—') ?></dd><dt>Window</dt><dd><?= h(implode(' → ', $scan['window'] ?? [])) ?></dd><dt>Next scan</dt><dd><?= h($auto['next_event_scan'] ?? '—') ?></dd><dt>Created last scan</dt><dd><?= h(implode(', ', $scan['created'] ?? []) ?: 'None') ?></dd></dl>
<h2>Published events</h2><div class="tw"><table><tr><th>Date</th><th>Event</th><th>County</th></tr>
<?php foreach ($ev as $e) if (($e['status'] ?? 'published') === 'published') echo '<tr><td>' . h($e['event_date']) . '</td><td><a href="' . h($e['path']) . '" target="_blank">' . h($e['title']) . '</a></td><td>' . h($e['county']) . '</td></tr>'; ?></table></div>
<h2>Draft events (need review)</h2><div class="tw"><table><tr><th>Date</th><th>Event</th><th>County</th><th></th></tr>
<?php $d = 0; foreach ($ev as $e) if (($e['status'] ?? '') !== 'published') { $d++; echo '<tr><td>' . h($e['event_date']) . '</td><td>' . h($e['title']) . '</td><td>' . h($e['county']) . '</td><td><form class="inline" method="post">' . csrf_field() . '<input type="hidden" name="action" value="approve"><input type="hidden" name="kind" value="event"><input type="hidden" name="source" value="' . h($e['source']) . '"><button name="decision" value="publish">Approve</button> <button class="btn2" name="decision" value="reject">Reject</button></form></td></tr>'; }
if (!$d) echo '<tr><td colspan="4">No drafts.</td></tr>'; ?></table></div>
<h2>Rejected candidates (last scan)</h2><div class="tw"><table><tr><th>Candidate</th><th>Reason</th></tr>
<?php foreach (($scan['rejected'] ?? []) as $r) echo '<tr><td>' . h($r['name'] ?? '') . '</td><td>' . h($r['reason'] ?? '') . '</td></tr>'; ?></table></div>

<?php elseif ($S === 'locations'): ?>
<h1>Location pages</h1><div class="tw"><table><tr><th>City</th><th>County</th><th>Words</th><th>URL</th></tr>
<?php foreach (($manifest['locations'] ?? []) as $l) echo '<tr><td>' . h($l['city']) . '</td><td>' . h($l['county']) . '</td><td>' . h($l['words']) . '</td><td><a href="' . h($l['path']) . '" target="_blank">' . h($l['path']) . '</a></td></tr>'; ?></table></div>

<?php elseif ($S === 'seo'): ?>
<h1>SEO metadata</h1><p>Titles aim for ~50–60 characters and descriptions for ≤150. Submit a change and the next automation run applies it to the page source, validates and republishes.</p>
<div class="tw"><table><tr><th>Page</th><th>Title</th><th>Description</th><th>Change</th></tr>
<?php foreach (($manifest['pages'] ?? []) as $p) { if (!empty($p['noindex'])) continue; $tl = mb_strlen($p['title']); $dl = mb_strlen($p['description']);
echo '<tr><td><a href="' . h($p['path']) . '" target="_blank">' . h($p['path']) . '</a><br><small>' . h($p['kind']) . '</small></td><td>' . h($p['title']) . '<br><small class="' . ($tl > 65 || $tl < 30 ? 'warn' : 'ok') . '">' . $tl . ' chars</small></td><td>' . h($p['description']) . '<br><small class="' . ($dl > 150 ? 'bad' : 'ok') . '">' . $dl . ' chars</small></td>'
 . '<td><details><summary>Edit</summary><form method="post">' . csrf_field() . '<input type="hidden" name="action" value="seo_change"><input type="hidden" name="path" value="' . h($p['path']) . '"><input name="title" placeholder="New title" style="width:260px"><br><textarea name="description" placeholder="New description (≤150)" maxlength="300" style="width:260px"></textarea><br><button>Queue change</button></form></details></td></tr>'; } ?>
</table></div>

<?php elseif ($S === 'redirects'): $r = sd_read_json('redirects.json', []); ?>
<h1>Redirects</h1><p>Redirects apply to paths that don't exist as pages. (Old WordPress paths like /wp-admin/ and /feed/ are already handled.)</p>
<form method="post" class="row"><?= csrf_field() ?><input type="hidden" name="action" value="redirect_add"><input name="from" placeholder="/old-path/" required><input name="to" placeholder="/new-path/" required><select name="code"><option>301</option><option>302</option><option>307</option><option>308</option></select><button>Add redirect</button></form>
<div class="tw"><table><tr><th>From</th><th>To</th><th>Code</th><th></th></tr>
<?php foreach ($r as $x) echo '<tr><td>' . h($x['from']) . '</td><td>' . h($x['to']) . '</td><td>' . h($x['code']) . '</td><td><form class="inline" method="post">' . csrf_field() . '<input type="hidden" name="action" value="redirect_del"><input type="hidden" name="from" value="' . h($x['from']) . '"><button class="btn2">Remove</button></form></td></tr>';
if (!$r) echo '<tr><td colspan="4">No custom redirects.</td></tr>'; ?></table></div>

<?php elseif ($S === 'requests'): $q = sd_read_json('requests.json', []); ?>
<h1>Automation requests</h1><p>Requests queued from this admin (SEO edits, site-setting changes, draft approvals). The weekly automation applies pending requests, rebuilds, validates and publishes.</p>
<div class="tw"><table><tr><th>Requested</th><th>Type</th><th>Details</th><th>Status</th><th></th></tr>
<?php foreach (array_reverse($q) as $x) echo '<tr><td>' . when($x['requested_at']) . '</td><td>' . h($x['type']) . '</td><td><code>' . h(json_encode($x['data'], JSON_UNESCAPED_SLASHES)) . '</code></td><td><span class="pill">' . h($x['status']) . '</span>' . (!empty($x['result']) ? '<br><small>' . h($x['result']) . '</small>' : '') . '</td><td>' . ($x['status'] === 'pending' ? '<form class="inline" method="post">' . csrf_field() . '<input type="hidden" name="action" value="request_cancel"><input type="hidden" name="id" value="' . h($x['id']) . '"><button class="btn2">Cancel</button></form>' : '') . '</td></tr>';
if (!$q) echo '<tr><td colspan="5">No requests.</td></tr>'; ?></table></div>

<?php elseif ($S === 'settings'): $site = $manifest['site'] ?? []; ?>
<h1>Site settings</h1>
<h2>Runtime settings (apply immediately)</h2>
<form method="post"><?= csrf_field() ?><input type="hidden" name="action" value="settings">
<div class="row"><label for="lr">Lead recipient email</label><input id="lr" name="lead_recipient" type="email" value="<?= h($settings['lead_recipient']) ?>" required style="width:280px"></div>
<div class="row"><label for="mf">Send notifications from</label><input id="mf" name="mail_from" type="email" value="<?= h($settings['mail_from']) ?>" style="width:280px"></div>
<div class="row"><label><input type="checkbox" name="popup_enabled" value="1" <?= !empty($settings['popup_enabled']) ? 'checked' : '' ?>> Show the claim-review popup to first-time visitors</label></div>
<div class="row"><label for="pd">Popup delay (seconds)</label><input id="pd" name="popup_delay_seconds" type="number" min="0" max="120" value="<?= (int)$settings['popup_delay_seconds'] ?>" style="width:90px"></div>
<button>Save settings</button></form>
<h2>Published site details (change requests)</h2>
<p>These values are compiled into every page. Enter only what should change; the automation applies it and republishes.</p>
<dl class="kv"><?php foreach (['brand' => 'Brand', 'company' => 'Company', 'license_number' => 'TDI license #', 'licensed_address' => 'Licensed address (from TDI record)', 'phone_display' => 'Phone', 'email' => 'Email', 'blog_author' => 'Blog author', 'ga4_id' => 'GA4 measurement ID'] as $k => $lab) echo '<dt>' . h($lab) . '</dt><dd>' . h($site[$k] ?? '') . '</dd>'; ?></dl>
<form method="post" style="margin-top:12px"><?= csrf_field() ?><input type="hidden" name="action" value="site_change">
<?php foreach (['phone_display' => 'Phone', 'email' => 'Email', 'licensed_address' => 'Licensed address', 'blog_author' => 'Blog author', 'ga4_id' => 'GA4 ID (G-XXXX)', 'gsc_verification' => 'Search Console verification token', 'bing_verification' => 'Bing verification token', 'social' => 'Social profile URLs (comma separated)'] as $k => $lab) echo '<div class="row"><label style="width:240px" for="c-' . $k . '">' . h($lab) . '</label><input id="c-' . $k . '" name="' . $k . '" style="width:340px"></div>'; ?>
<button>Queue change request</button></form>
<h2>Change admin password</h2>
<form method="post"><?= csrf_field() ?><input type="hidden" name="action" value="password">
<div class="row"><input type="password" name="current" placeholder="Current password" autocomplete="current-password" required><input type="password" name="p1" placeholder="New password (14+ chars)" autocomplete="new-password" required><input type="password" name="p2" placeholder="Repeat new password" autocomplete="new-password" required><button>Change password</button></div></form>
<?php else: echo '<p>Not found.</p>'; endif; ?>
</main></div></body></html>
