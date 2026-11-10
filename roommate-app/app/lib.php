<?php
// Shared helpers.

function e($s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function base_url(): string
{
    global $CONFIG;
    return rtrim($CONFIG['base_url'] ?? '', '/');
}

function url(string $path = '/'): string
{
    return $path;
}

function redirect(string $path): void
{
    header('Location: ' . $path);
    exit;
}

function back(string $fallback = '/home'): void
{
    $ref = $_SERVER['HTTP_REFERER'] ?? '';
    $host = $_SERVER['HTTP_HOST'] ?? '';
    if ($ref && parse_url($ref, PHP_URL_HOST) === $host) {
        redirect($ref);
    }
    redirect($fallback);
}

function is_post(): bool
{
    return ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
}

function input(string $key, $default = '')
{
    $v = $_POST[$key] ?? $_GET[$key] ?? $default;
    return is_string($v) ? trim($v) : $v;
}

function is_ajax(): bool
{
    return ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'fetch'
        || str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
}

function json_out($data, int $code = 200): void
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data);
    exit;
}

// ---------- CSRF ----------
function csrf_token(): string
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">';
}

function verify_csrf(): void
{
    $t = $_POST['_csrf'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!is_string($t) || !hash_equals(csrf_token(), $t)) {
        if (is_ajax()) {
            json_out(['error' => 'Your session expired. Refresh the page and try again.'], 419);
        }
        flash('error', 'Your session expired. Please try again.');
        back();
    }
}

// ---------- Flash ----------
function flash(string $type, string $msg): void
{
    $_SESSION['flash'][] = [$type, $msg];
}

function take_flashes(): array
{
    $f = $_SESSION['flash'] ?? [];
    unset($_SESSION['flash']);
    return $f;
}

function old(string $key, $default = '')
{
    return $_SESSION['old'][$key] ?? $default;
}

// ---------- Auth ----------
function current_user(): ?array
{
    static $user = false;
    if ($user === false) {
        $user = null;
        if (!empty($_SESSION['uid'])) {
            $user = one('SELECT * FROM users WHERE id = ?', [$_SESSION['uid']]);
            if (!$user || $user['status'] !== 'active') {
                $user = null;
                unset($_SESSION['uid']);
            } elseif (empty($user['last_seen']) || strtotime($user['last_seen']) < time() - 60) {
                q('UPDATE users SET last_seen = NOW() WHERE id = ?', [$user['id']]);
            }
        }
    }
    return $user;
}

function uid(): int
{
    return (int)(current_user()['id'] ?? 0);
}

function is_admin(): bool
{
    return (current_user()['role'] ?? '') === 'admin';
}

function require_login(): array
{
    $u = current_user();
    if (!$u) {
        if (is_ajax()) {
            json_out(['error' => 'Please log in.'], 401);
        }
        $_SESSION['after_login'] = $_SERVER['REQUEST_URI'] ?? '/home';
        redirect('/login');
    }
    return $u;
}

function require_admin(): array
{
    $u = require_login();
    if ($u['role'] !== 'admin') {
        http_response_code(403);
        render('error', ['title' => 'Not allowed', 'message' => 'This area is for administrators only.']);
        exit;
    }
    return $u;
}

function login_user(array $user): void
{
    session_regenerate_id(true);
    $_SESSION['uid'] = (int)$user['id'];
}

function client_ip(): string
{
    return substr($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0', 0, 45);
}

function too_many_attempts(): bool
{
    q('DELETE FROM login_attempts WHERE created_at < (NOW() - INTERVAL 1 DAY)');
    return (int)val('SELECT COUNT(*) FROM login_attempts WHERE ip = ? AND created_at > (NOW() - INTERVAL 15 MINUTE)', [client_ip()]) >= 10;
}

function record_attempt(string $email): void
{
    q('INSERT INTO login_attempts (ip, email) VALUES (?, ?)', [client_ip(), $email]);
}

// ---------- Rendering ----------
function render(string $view, array $data = []): void
{
    extract($data, EXTR_SKIP);
    $viewFile = APP_DIR . '/views/' . $view . '.php';
    ob_start();
    require $viewFile;
    $content = ob_get_clean();
    $layout = $data['layout'] ?? (str_starts_with($view, 'admin/') ? 'admin_layout' : 'layout');
    require APP_DIR . '/views/' . $layout . '.php';
    unset($_SESSION['old']);
}

function partial(string $view, array $data = []): void
{
    extract($data, EXTR_SKIP);
    require APP_DIR . '/views/' . $view . '.php';
}

function not_found(): void
{
    http_response_code(404);
    render('error', ['title' => 'Page not found', 'message' => "We couldn't find that page."]);
    exit;
}

// ---------- Formatting ----------
function avatar_url(?array $u): string
{
    if (!empty($u['avatar'])) {
        return '/uploads/avatars/' . rawurlencode($u['avatar']);
    }
    return '';
}

function avatar(?array $u, string $size = 'md'): string
{
    $name = $u['name'] ?? '?';
    $src = avatar_url($u);
    if ($src) {
        return '<img class="avatar avatar-' . e($size) . '" src="' . e($src) . '" alt="' . e($name) . '" loading="lazy">';
    }
    $initials = '';
    foreach (preg_split('/\s+/', trim($name)) as $p) {
        if ($p !== '' && mb_strlen($initials) < 2) {
            $initials .= mb_strtoupper(mb_substr($p, 0, 1));
        }
    }
    $hue = crc32($name) % 360;
    return '<span class="avatar avatar-' . e($size) . ' avatar-initials" style="--h:' . $hue . '" aria-label="' . e($name) . '">' . e($initials ?: '?') . '</span>';
}

function time_ago(?string $dt): string
{
    if (!$dt) return '';
    $d = time() - strtotime($dt);
    if ($d < 60) return 'just now';
    if ($d < 3600) return floor($d / 60) . 'm';
    if ($d < 86400) return floor($d / 3600) . 'h';
    if ($d < 604800) return floor($d / 86400) . 'd';
    return date('M j', strtotime($dt)) . (date('Y', strtotime($dt)) !== date('Y') ? ', ' . date('Y', strtotime($dt)) : '');
}

function money($n): string
{
    return $n === null || $n === '' ? '' : '$' . number_format((int)$n);
}

function budget_label(array $u): string
{
    if ($u['budget_min'] && $u['budget_max']) return money($u['budget_min']) . '–' . money($u['budget_max']);
    if ($u['budget_max']) return 'Up to ' . money($u['budget_max']);
    if ($u['budget_min']) return 'From ' . money($u['budget_min']);
    return '';
}

function age_of(array $u): ?int
{
    return $u['birth_year'] ? (int)date('Y') - (int)$u['birth_year'] : null;
}

function is_online(array $u): bool
{
    return !empty($u['last_seen']) && strtotime($u['last_seen']) > time() - 300;
}

function linkify(string $text): string
{
    $t = nl2br(e($text));
    return preg_replace('~(https?://[^\s<]+)~', '<a href="$1" target="_blank" rel="noopener nofollow">$1</a>', $t);
}

function slugify(string $s): string
{
    $s = strtolower(trim(preg_replace('/[^A-Za-z0-9]+/', '-', $s), '-'));
    return $s ?: 'property';
}

function unique_slug(string $name, int $ignoreId = 0): string
{
    $base = slugify($name);
    $slug = $base;
    $i = 2;
    while (val('SELECT id FROM properties WHERE slug = ? AND id <> ?', [$slug, $ignoreId])) {
        $slug = $base . '-' . $i++;
    }
    return $slug;
}

const LABELS = [
    'looking_for' => ['need_place' => 'Needs a place', 'have_place' => 'Has a place', 'either' => 'Open to either'],
    'sleep_schedule' => ['early' => 'Early bird', 'normal' => 'Regular hours', 'night' => 'Night owl'],
    'smoking' => ['no' => 'Non-smoker', 'outside' => 'Smokes outside', 'yes' => 'Smoker'],
    'pets' => ['none' => 'No pets', 'have' => 'Has pets', 'ok' => 'Pet friendly', 'no_pets' => 'No pets please'],
    'guests' => ['rarely' => 'Guests rarely', 'sometimes' => 'Guests sometimes', 'often' => 'Guests often'],
    'gender' => ['' => 'Prefer not to say', 'male' => 'Male', 'female' => 'Female', 'nonbinary' => 'Non-binary', 'other' => 'Other'],
    'gender_pref' => ['any' => 'Any gender', 'male' => 'Male roommates', 'female' => 'Female roommates', 'nonbinary' => 'Non-binary roommates'],
    'cleanliness' => [1 => 'Relaxed', 2 => 'Easygoing', 3 => 'Tidy', 4 => 'Very tidy', 5 => 'Spotless'],
];

function label(string $field, $value): string
{
    return LABELS[$field][$value] ?? (string)$value;
}

function options(string $field, $selected): string
{
    $html = '';
    foreach (LABELS[$field] as $k => $v) {
        $html .= '<option value="' . e($k) . '"' . ((string)$k === (string)$selected ? ' selected' : '') . '>' . e($v) . '</option>';
    }
    return $html;
}

// ---------- Images ----------
/**
 * Validate an uploaded image, re-encode it (strips metadata and any payload), save it.
 * Returns the stored filename or null when nothing was uploaded. Throws on bad input.
 */
function save_upload(string $field, string $dir, int $maxW, int $maxH, bool $square = false): ?string
{
    if (empty($_FILES[$field]) || ($_FILES[$field]['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) {
        return null;
    }
    $f = $_FILES[$field];
    if ($f['error'] !== UPLOAD_ERR_OK) {
        throw new RuntimeException('Upload failed. Try a smaller image (max 8 MB).');
    }
    if ($f['size'] > 8 * 1024 * 1024) {
        throw new RuntimeException('Image is too large (max 8 MB).');
    }
    $info = @getimagesize($f['tmp_name']);
    if (!$info || !in_array($info[2], [IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_GIF, IMAGETYPE_WEBP], true)) {
        throw new RuntimeException('Please upload a JPG, PNG, GIF or WebP image.');
    }
    $src = match ($info[2]) {
        IMAGETYPE_JPEG => @imagecreatefromjpeg($f['tmp_name']),
        IMAGETYPE_PNG => @imagecreatefrompng($f['tmp_name']),
        IMAGETYPE_GIF => @imagecreatefromgif($f['tmp_name']),
        IMAGETYPE_WEBP => @imagecreatefromwebp($f['tmp_name']),
    };
    if (!$src) {
        throw new RuntimeException('That image could not be read.');
    }
    if ($info[2] === IMAGETYPE_JPEG && function_exists('exif_read_data')) {
        $exif = @exif_read_data($f['tmp_name']);
        $o = $exif['Orientation'] ?? 1;
        if ($o == 3) $src = imagerotate($src, 180, 0);
        if ($o == 6) $src = imagerotate($src, -90, 0);
        if ($o == 8) $src = imagerotate($src, 90, 0);
    }
    $w = imagesx($src);
    $h = imagesy($src);
    $sx = 0; $sy = 0; $sw = $w; $sh = $h;
    if ($square) {
        $side = min($w, $h);
        $sx = (int)(($w - $side) / 2);
        $sy = (int)(($h - $side) / 2);
        $sw = $sh = $side;
        $nw = $nh = min($maxW, $side);
    } else {
        $ratio = min(1, $maxW / $w, $maxH / $h);
        $nw = max(1, (int)round($w * $ratio));
        $nh = max(1, (int)round($h * $ratio));
    }
    $dst = imagecreatetruecolor($nw, $nh);
    imagefill($dst, 0, 0, imagecolorallocate($dst, 255, 255, 255));
    imagecopyresampled($dst, $src, 0, 0, $sx, $sy, $nw, $nh, $sw, $sh);
    $name = bin2hex(random_bytes(12)) . '.jpg';
    $path = APP_ROOT . '/uploads/' . $dir;
    if (!is_dir($path)) {
        mkdir($path, 0755, true);
    }
    imagejpeg($dst, $path . '/' . $name, 85);
    imagedestroy($src);
    imagedestroy($dst);
    return $name;
}

function delete_upload(string $dir, ?string $name): void
{
    if ($name && preg_match('/^[a-f0-9]{24}\.jpg$/', $name)) {
        @unlink(APP_ROOT . '/uploads/' . $dir . '/' . $name);
    }
}

// ---------- Social graph ----------
function friend_status(int $me, int $other): string
{
    // none | friends | sent | received
    $r = one('SELECT * FROM friendships WHERE (requester_id = ? AND addressee_id = ?) OR (requester_id = ? AND addressee_id = ?)', [$me, $other, $other, $me]);
    if (!$r) return 'none';
    if ($r['status'] === 'accepted') return 'friends';
    return (int)$r['requester_id'] === $me ? 'sent' : 'received';
}

function is_blocked_between(int $a, int $b): bool
{
    return (bool)val('SELECT 1 FROM blocks WHERE (blocker_id = ? AND blocked_id = ?) OR (blocker_id = ? AND blocked_id = ?)', [$a, $b, $b, $a]);
}

function blocked_ids(int $me): array
{
    return array_map('intval', array_column(all('SELECT blocked_id AS id FROM blocks WHERE blocker_id = ? UNION SELECT blocker_id FROM blocks WHERE blocked_id = ?', [$me, $me]), 'id'));
}

function friend_ids(int $me): array
{
    return array_map('intval', array_column(all("SELECT IF(requester_id = ?, addressee_id, requester_id) AS id FROM friendships WHERE status = 'accepted' AND (requester_id = ? OR addressee_id = ?)", [$me, $me, $me]), 'id'));
}

function can_message(int $me, int $other): bool
{
    if ($me === $other || is_blocked_between($me, $other)) return false;
    $target = one("SELECT status FROM users WHERE id = ?", [$other]);
    if (!$target || $target['status'] !== 'active') return false;
    if (setting('messaging_friends_only') === '1' && !is_admin()) {
        return friend_status($me, $other) === 'friends';
    }
    return true;
}

function notify(int $userId, string $type, ?int $actorId = null, ?int $entityId = null): void
{
    if ($userId === $actorId) return;
    q('INSERT INTO notifications (user_id, actor_id, type, entity_id) VALUES (?, ?, ?, ?)', [$userId, $actorId, $type, $entityId]);
    $actor = $actorId ? one('SELECT name, username FROM users WHERE id = ?', [$actorId]) : null;
    $who = $actor['name'] ?? 'Someone';
    $b = base_url();
    $mail = match ($type) {
        'friend_request' => ["$who sent you a friend request", "$who wants to connect on " . setting('site_name') . ".\n\nSee their profile and respond: $b/friends?tab=requests"],
        'friend_accept' => ["$who accepted your friend request", "You and $who are now friends.\n\nSay hi: $b/messages/" . ($actor['username'] ?? '')],
        'message' => ["New message from $who", "$who sent you a message.\n\nRead and reply: $b/messages/" . ($actor['username'] ?? '')],
        'comment' => ["$who commented on your post", "Read it: $b/post/" . (int)$entityId],
        'match' => ["You matched with $who!", "You and $who liked each other on Roommate Match, so you're now friends.\n\nSay hi: $b/messages/" . ($actor['username'] ?? '')],
        'agreement' => ["$who updated your roommate agreement", "Review it and sign when you're ready: $b/agreement/" . ($actor['username'] ?? '')],
        'agreement_signed' => ["$who signed your roommate agreement", "See it here: $b/agreement/" . ($actor['username'] ?? '')],
        'property_approved' => ['Your property was approved', "A property you submitted is now live. Renters can pick it and find you.\n\n$b/properties"],
        default => null,
    };
    if ($mail) {
        try { email_member($userId, $mail[0], $mail[1]); } catch (Throwable $e) { /* email must never break the app */ }
    }
}

function unread_counts(int $me): array
{
    $msgs = (int)val('SELECT COUNT(*) FROM messages m JOIN conversations c ON c.id = m.conversation_id
        WHERE (c.user_a = ? OR c.user_b = ?) AND m.sender_id <> ? AND m.read_at IS NULL', [$me, $me, $me]);
    $notifs = (int)val('SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0', [$me]);
    $reqs = (int)val("SELECT COUNT(*) FROM friendships WHERE addressee_id = ? AND status = 'pending'", [$me]);
    return ['messages' => $msgs, 'notifications' => $notifs, 'requests' => $reqs];
}

function audit(string $action, string $details = ''): void
{
    q('INSERT INTO audit_log (admin_id, action, details) VALUES (?, ?, ?)', [uid() ?: null, $action, mb_substr($details, 0, 1000)]);
}

function send_mail(string $to, string $subject, string $body, ?string &$error = null): bool
{
    global $CONFIG;
    $from = $CONFIG['mail_from'] ?? ('no-reply@' . ($_SERVER['HTTP_HOST'] ?? 'localhost'));
    $fromName = setting('site_name', 'Rise Roommates');
    $footer = "\n\n—\n" . $fromName . ' · ' . base_url() . "\nManage email notifications: " . base_url() . '/settings';
    $body .= $footer;
    if (!empty($CONFIG['smtp_host'])) {
        return smtp_send($to, $subject, $body, $from, $fromName, $error);
    }
    $headers = 'From: ' . $fromName . ' <' . $from . ">\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    return @mail($to, $subject, $body, $headers);
}

/** Minimal SMTP client (implicit TLS on 465 or STARTTLS on 587) with AUTH LOGIN. */
function smtp_send(string $to, string $subject, string $body, string $from, string $fromName, ?string &$error = null): bool
{
    global $CONFIG;
    $host = $CONFIG['smtp_host'];
    $port = (int)($CONFIG['smtp_port'] ?? 465);
    $remote = ($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $fp = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT,
        stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host]]));
    if (!$fp) { $error = "connect: $errstr"; return false; }
    stream_set_timeout($fp, 20);
    $read = function () use ($fp) {
        $data = '';
        while (($line = fgets($fp, 1024)) !== false) { $data .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $data;
    };
    $cmd = function (string $c, array $ok) use ($fp, $read, &$error) {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int)substr($r, 0, 3), $ok, true)) { $error = trim(preg_replace('/AUTH.*/', 'AUTH ...', $c)) . ' -> ' . trim($r); return false; }
        return true;
    };
    $ehlo = 'EHLO ' . (parse_url(base_url(), PHP_URL_HOST) ?: 'localhost');
    $ok = $cmd('', [220]) && $cmd($ehlo, [250]);
    if ($ok && $port !== 465) {
        $ok = $cmd('STARTTLS', [220]) && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) && $cmd($ehlo, [250]);
    }
    $enc = fn($s) => '=?UTF-8?B?' . base64_encode($s) . '?=';
    $msg = 'Date: ' . date('r') . "\r\n"
        . 'From: ' . $enc($fromName) . " <$from>\r\n"
        . "To: <$to>\r\n"
        . 'Subject: ' . $enc($subject) . "\r\n"
        . 'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . (explode('@', $from)[1] ?? 'localhost') . ">\r\n"
        . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($body)) . "\r\n.";
    $ok = $ok
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($CONFIG['smtp_user']), [334])
        && $cmd(base64_encode($CONFIG['smtp_pass']), [235])
        && $cmd("MAIL FROM:<$from>", [250])
        && $cmd("RCPT TO:<$to>", [250, 251])
        && $cmd('DATA', [354])
        && $cmd($msg, [250]);
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}

/** Email a member about activity if they opted in and aren't active on the site right now. */
function email_member(int $userId, string $subject, string $body): void
{
    $u = one("SELECT name, email, email_notifications, last_seen, is_demo FROM users WHERE id = ? AND status = 'active'", [$userId]);
    if (!$u || !$u['email_notifications'] || $u['is_demo']) return;
    if ($u['last_seen'] && strtotime($u['last_seen']) > time() - 300) return; // online — they'll see it in the app
    send_mail($u['email'], $subject, "Hi " . explode(' ', $u['name'])[0] . ",\n\n" . $body);
}

/** Email the site's admin inbox (admin_email setting, falls back to admin accounts). */
function email_admins(string $subject, string $body): void
{
    $to = setting('admin_email', '');
    $list = $to ? [$to] : array_column(all("SELECT email FROM users WHERE role = 'admin' AND status = 'active'"), 'email');
    foreach (array_unique($list) as $addr) send_mail($addr, '[Admin] ' . $subject, $body);
}

function profile_completeness(array $u): int
{
    $fields = ['avatar', 'bio', 'birth_year', 'occupation', 'city', 'budget_max', 'move_in_date', 'interests'];
    $n = 0;
    foreach ($fields as $f) {
        if (!empty($u[$f])) $n++;
    }
    $hasProp = (bool)val('SELECT 1 FROM user_properties WHERE user_id = ? LIMIT 1', [$u['id']]);
    return (int)round(($n + ($hasProp ? 1 : 0)) / (count($fields) + 1) * 100);
}

function paginate(int $total, int $perPage): array
{
    $page = max(1, (int)($_GET['page'] ?? 1));
    $pages = max(1, (int)ceil($total / $perPage));
    $page = min($page, $pages);
    return [$page, $pages, ($page - 1) * $perPage];
}

function page_link(int $p): string
{
    $qs = $_GET;
    $qs['page'] = $p;
    return '?' . http_build_query($qs);
}

function icon(string $name): string
{
    static $paths = [
        'home' => '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20h5v-6h4v6h5V9.5"/>',
        'search' => '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        'building' => '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
        'users' => '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.5-3.5 3.2-5.5 6.5-5.5s6 2 6.5 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14.5c2.5 0 4.2 1.6 4.5 4.5"/>',
        'chat' => '<path d="M4 5h16v11H9l-5 4z"/>',
        'bell' => '<path d="M6 16V11a6 6 0 1 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
        'user' => '<circle cx="12" cy="8" r="4"/><path d="M4 21c.6-4 3.8-6.5 8-6.5s7.4 2.5 8 6.5"/>',
        'edit' => '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
        'gear' => '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
        'shield' => '<path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6z"/>',
        'info' => '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
        'logout' => '<path d="M15 4h4v16h-4"/><path d="M10 8l-4 4 4 4M6 12h10"/>',
        'heart' => '<path d="M12 20s-7.5-4.6-9-9.5C2 7 4.5 4.5 7.5 4.5c2 0 3.5 1.2 4.5 2.7 1-1.5 2.5-2.7 4.5-2.7 3 0 5.5 2.5 4.5 6-1.5 4.9-9 9.5-9 9.5z"/>',
        'comment' => '<path d="M4 5h16v11H9l-5 4z"/>',
        'pin' => '<path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
        'calendar' => '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
        'dollar' => '<path d="M12 3v18M16.5 7.5c-.5-1.5-2.3-2.5-4.5-2.5-2.5 0-4.5 1.3-4.5 3.3 0 4.7 9 2.4 9 7.2 0 2-2 3.5-4.5 3.5-2.4 0-4.2-1-4.8-2.8"/>',
        'briefcase' => '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 12h18"/>',
        'image' => '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
        'send' => '<path d="M21 3 10 14M21 3l-7 18-4-7-7-4z"/>',
        'plus' => '<path d="M12 5v14M5 12h14"/>',
        'check' => '<path d="m5 12 5 5 9-10"/>',
        'x' => '<path d="M6 6l12 12M18 6 6 18"/>',
        'flag' => '<path d="M5 21V4h11l-1.5 4L16 12H5"/>',
        'star' => '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
        'more' => '<circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/>',
        'sparkle' => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
        'back' => '<path d="M15 5l-7 7 7 7"/>',
        'link' => '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
        'trash' => '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
        'ban' => '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
        'moon' => '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
        'chart' => '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    ];
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . ($paths[$name] ?? '') . '</svg>';
}

function property_image(array $p): string
{
    if (!empty($p['image'])) return '/uploads/properties/' . rawurlencode($p['image']);
    if (!empty($p['image_url'])) return $p['image_url'];
    return '';
}

/**
 * Import one page of apartment listings from the Rise Apartments WordPress API.
 * Returns ['page' => n, 'total_pages' => n, 'added' => n, 'updated' => n].
 */
function sync_rise_page(int $page): array
{
    $base = rtrim(setting('sync_source', 'https://riseapartments.com'), '/');
    $url = $base . '/wp-json/wp/v2/apartment?per_page=100&page=' . $page . '&orderby=id&order=asc'
        . '&_embed=wp:featuredmedia&_fields=id,title,link,city,content,status,_links,_embedded';
    $headers = [];
    $body = null;
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 60, CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_USERAGENT => 'RiseRoommatesSync/1.0',
            CURLOPT_HEADERFUNCTION => function ($c, $h) use (&$headers) { $p = explode(':', $h, 2); if (count($p) === 2) $headers[strtolower(trim($p[0]))] = trim($p[1]); return strlen($h); }]);
        $body = curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($code === 400) return ['page' => $page, 'total_pages' => $page - 1, 'added' => 0, 'updated' => 0]; // past the end
        if ($code !== 200) throw new RuntimeException("Source returned HTTP $code");
    } else {
        $body = @file_get_contents($url, false, stream_context_create(['http' => ['timeout' => 60, 'user_agent' => 'RiseRoommatesSync/1.0']]));
        foreach ($http_response_header ?? [] as $h) { $p = explode(':', $h, 2); if (count($p) === 2) $headers[strtolower(trim($p[0]))] = trim($p[1]); }
    }
    $items = json_decode((string)$body, true);
    if (!is_array($items)) throw new RuntimeException('Unexpected response from source');
    static $cityTerms = null;
    if ($cityTerms === null) {
        $cityTerms = [];
        $t = json_decode((string)@file_get_contents($base . '/wp-json/wp/v2/city?per_page=100&_fields=id,name'), true);
        foreach ((array)$t as $c) $cityTerms[$c['id']] = trim(preg_replace('/\s*(TX\s*)?Apartments$/i', '', $c['name']));
    }
    $added = $updated = 0;
    foreach ($items as $a) {
        $name = trim(html_entity_decode(strip_tags($a['title']['rendered'] ?? ''), ENT_QUOTES | ENT_HTML5, 'UTF-8'));
        $name = trim(preg_replace('/[\x{00A0}\s]+/u', ' ', $name));
        if ($name === '') continue;
        $text = html_entity_decode(strip_tags($a['content']['rendered'] ?? ''), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $text = trim(preg_replace('/[\x{00A0}\s]+/u', ' ', $text));
        $address = $city = $state = $zip = null;
        if (preg_match('/^(.{3,120}?),\s*([A-Za-z .\'-]{2,40}),\s*([A-Z]{2})\s*(\d{5})?/', $text, $m)) {
            [$address, $city, $state, $zip] = [trim($m[1]), trim($m[2]), $m[3], $m[4] ?? null];
        } else {
            $termId = $a['city'][0] ?? null;
            $city = $termId && isset($cityTerms[$termId]) && $cityTerms[$termId] !== 'USA' ? $cityTerms[$termId] : null;
            if ($city === 'Dallas/Fort Worth') $city = 'Dallas';
            $state = $city ? 'TX' : null;
        }
        $media = $a['_embedded']['wp:featuredmedia'][0] ?? [];
        $sizes = $media['media_details']['sizes'] ?? [];
        $img = $sizes['medium_large']['source_url'] ?? $sizes['large']['source_url'] ?? $media['source_url'] ?? null;
        $ext = (int)$a['id'];
        $existing = one('SELECT id FROM properties WHERE external_id = ?', [$ext]);
        if ($existing) {
            q('UPDATE properties SET name = ?, address = COALESCE(?, address), city = COALESCE(?, city), state = COALESCE(?, state), zip = COALESCE(?, zip), external_url = ?, image_url = ? WHERE id = ?',
                [$name, $address, $city, $state, $zip, $a['link'] ?? null, $img, $existing['id']]);
            $updated++;
        } else {
            q("INSERT INTO properties (name, slug, address, city, state, zip, external_id, external_url, image_url, status) VALUES (?,?,?,?,?,?,?,?,?, 'approved')",
                [$name, unique_slug($name), $address, $city, $state, $zip, $ext, $a['link'] ?? null, $img]);
            $added++;
        }
    }
    $totalPages = (int)($headers['x-wp-totalpages'] ?? ($items ? $page + 1 : $page));
    return ['page' => $page, 'total_pages' => $totalPages, 'added' => $added, 'updated' => $updated];
}

const QUIZ_TYPES = [
    'planner' => ['name' => 'The Neat Planner', 'emoji' => '🗂️', 'desc' => 'Organized, tidy and reliable. You like a calm, clean home, shared chore charts and bills paid on time.', 'best' => ['planner', 'pro', 'homebody']],
    'social' => ['name' => 'The Social Host', 'emoji' => '🎉', 'desc' => 'Your place is where friends gather. You love game nights, cooking for people and a lively home.', 'best' => ['social', 'adventurer']],
    'owl' => ['name' => 'The Night Owl', 'emoji' => '🦉', 'desc' => 'You come alive after dark — late shifts, creative projects or gaming. You keep it quiet, just late.', 'best' => ['owl', 'homebody']],
    'homebody' => ['name' => 'The Chill Homebody', 'emoji' => '🛋️', 'desc' => 'Cozy nights in, low drama, easygoing. You want a peaceful home and a roommate who respects downtime.', 'best' => ['homebody', 'planner', 'owl']],
    'pro' => ['name' => 'The Busy Professional', 'emoji' => '💼', 'desc' => 'Work, gym, sleep, repeat. You\'re rarely home, value quiet mornings and want a roommate who\'s low-maintenance.', 'best' => ['pro', 'planner', 'adventurer']],
    'adventurer' => ['name' => 'The Adventurer', 'emoji' => '🧭', 'desc' => 'Always out exploring — trips, concerts, hikes. Flexible, spontaneous and easy to live with.', 'best' => ['adventurer', 'social', 'pro']],
];

function quiz_badge(?string $type): string
{
    if (!$type || !isset(QUIZ_TYPES[$type])) return '';
    $t = QUIZ_TYPES[$type];
    return '<span class="type-badge" title="' . e($t['desc']) . '">' . $t['emoji'] . ' ' . e($t['name']) . '</span>';
}
