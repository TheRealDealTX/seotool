<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Guest contributions: anyone can post or comment with a name and a valid email.
 *
 * - The email must be well-formed and its domain must accept mail (MX/A record).
 * - A guest's first contribution is held until they click a confirmation link
 *   emailed from the support mailbox. That proves the address is real and keeps
 *   bots out. Confirming marks the email verified and sets a signed cookie, so
 *   later contributions from that browser publish instantly.
 * - Guests cannot vote or report (those need an account) and are rate limited.
 */
const M1S_GUEST_COOKIE = 'm1s_guest';

function guest_sign(string $email): string
{
    return hash_hmac('sha256', 'guest|' . strtolower($email), cfg('secret'));
}

/** ['name' => ..., 'email' => ..., 'trusted' => bool] from the guest cookie. */
function guest_cookie(): array
{
    $raw = $_COOKIE[M1S_GUEST_COOKIE] ?? '';
    $data = json_decode(base64_decode(strtr((string)$raw, '-_', '+/'), true) ?: '', true);
    if (!is_array($data) || !isset($data['n'], $data['e'])) {
        return ['name' => '', 'email' => '', 'trusted' => false];
    }
    $trusted = isset($data['s']) && hash_equals(guest_sign($data['e']), (string)$data['s']);
    return ['name' => (string)$data['n'], 'email' => (string)$data['e'], 'trusted' => $trusted];
}

function guest_cookie_set(string $name, string $email, bool $trusted): void
{
    $data = ['n' => $name, 'e' => $email];
    if ($trusted) {
        $data['s'] = guest_sign($email);
    }
    $val = rtrim(strtr(base64_encode(json_encode($data)), '+/', '-_'), '=');
    setcookie(M1S_GUEST_COOKIE, $val, [
        'expires' => time() + 86400 * 365, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax',
        'secure' => ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https' || ($_SERVER['HTTPS'] ?? '') === 'on',
    ]);
    $_COOKIE[M1S_GUEST_COOKIE] = $val;
}

/** Validate a guest name + email. Returns an error message or null. */
function guest_validate(string $name, string $email): ?string
{
    if (!preg_match("/^[\\p{L}\\p{N} .'_-]{2,40}$/u", $name) || !preg_match('/\p{L}/u', $name)) {
        return 'Enter your name (2 to 40 letters; it is shown with your post).';
    }
    $lname = mb_strtolower(trim($name));
    if (in_array($lname, reserved_usernames(), true) || in_array($lname, ['my 1 secret', 'my1secret team', 'moderator', 'admin team'], true)) {
        return 'Please use your own name.';
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 190) {
        return 'Enter a valid email address. It is never shown publicly.';
    }
    $domain = strtolower(substr(strrchr($email, '@'), 1));
    if (in_array($domain, disposable_domains(), true)) {
        return 'Please use a permanent email address.';
    }
    if (!cfg('skip_mx_check') && !checkdnsrr($domain, 'MX') && !checkdnsrr($domain, 'A')) {
        return 'That email domain does not accept mail. Check the address.';
    }
    if (one('SELECT email FROM guests WHERE email = ? AND banned = 1', [$email])) {
        return 'This email address cannot post here.';
    }
    return null;
}

function disposable_domains(): array
{
    return ['mailinator.com', 'guerrillamail.com', '10minutemail.com', 'tempmail.com', 'temp-mail.org', 'yopmail.com',
        'trashmail.com', 'sharklasers.com', 'getnada.com', 'dispostable.com', 'maildrop.cc', 'throwawaymail.com', 'fakeinbox.com'];
}

/** Has this browser confirmed this email before? */
function guest_is_trusted(string $email): bool
{
    $c = guest_cookie();
    if (!$c['trusted'] || strcasecmp($c['email'], $email) !== 0) {
        return false;
    }
    return (bool)one('SELECT email FROM guests WHERE email = ? AND verified_at IS NOT NULL AND banned = 0', [strtolower($email)]);
}

/** Read + check the guest fields of a submitted form. Returns [name, email, error]. */
function guest_from_post(string $kind): array
{
    $name = trim(preg_replace('/\s+/u', ' ', input('guest_name')));
    $email = strtolower(input('guest_email'));
    if (!bot_check_passes(2)) {
        return [$name, $email, 'Something looked automated about that. Please try again.'];
    }
    if ($err = guest_validate($name, $email)) {
        return [$name, $email, $err];
    }
    $limits = $kind === 'post' ? [3, 3600] : [10, 3600];
    if (!throttle('guest-' . $kind, $limits[0], $limits[1]) || !throttle('guest-' . $kind . '-e', $limits[0], $limits[1], $email)) {
        return [$name, $email, 'You are posting very quickly. Take a short break and try again.'];
    }
    return [$name, $email, null];
}

/** Email a confirmation link for a pending guest thread/comment. */
function guest_send_confirmation(string $type, int $id, string $name, string $email, string $title): bool
{
    $token = bin2hex(random_bytes(20));
    $tid = insert('guest_tokens', ['email' => $email, 'token_hash' => hash('sha256', $token), 'target_type' => $type,
        'target_id' => $id, 'created_at' => now()]);
    $link = abs_url('/confirm/?id=' . $tid . '&t=' . $token);
    $what = $type === 'thread' ? 'your post' : 'your comment';
    return send_mail($email, 'Confirm ' . $what . ' on My 1 Secret',
        "Hi $name,\n\nThanks for contributing to My 1 Secret! Click this link to publish $what:\n\n$link\n\n"
        . "\"" . mb_strimwidth($title, 0, 120, '…') . "\"\n\n"
        . "You only need to do this once per browser: after you confirm, your next posts and comments publish right away.\n\n"
        . "If you did not write this, ignore this email and nothing will be published.\n\n- The My 1 Secret team\n" . abs_url('/'));
}

/** Delete guest contributions that were never confirmed (called occasionally). */
function guest_gc(): void
{
    if (random_int(1, 30) !== 1) {
        return;
    }
    $cut = gmdate('Y-m-d H:i:s', time() - 86400 * 7);
    q("DELETE FROM comments WHERE status = 'pending' AND created_at < ?", [$cut]);
    q("DELETE FROM threads WHERE status = 'pending' AND created_at < ?", [$cut]);
    q('DELETE FROM guest_tokens WHERE created_at < ?', [$cut]);
}

function guest_fields(bool $compact = false): string
{
    $g = guest_cookie();
    $h = '<div class="guest-fields' . ($compact ? ' compact' : '') . '">'
        . '<div><label for="gn-' . ($id = bin2hex(random_bytes(3))) . '">Your name</label>'
        . '<input id="gn-' . $id . '" name="guest_name" type="text" required maxlength="40" autocomplete="name" value="' . e(old('guest_name', $g['name'])) . '"></div>'
        . '<div><label for="ge-' . $id . '">Email <span class="muted">(never shown)</span></label>'
        . '<input id="ge-' . $id . '" name="guest_email" type="email" required maxlength="190" autocomplete="email" value="' . e(old('guest_email', $g['email'])) . '"></div>'
        . '</div>' . bot_check_fields();
    if (!$g['trusted']) {
        $h .= '<p class="hint">First time? We\'ll email you a link to publish. After that your posts appear instantly. Or <a href="/register/" rel="nofollow">create a free account</a> to vote and get a profile.</p>';
    }
    return $h;
}

/** Remember name/email for prefill; keep the trust signature if it already matches. */
function guest_remember(string $name, string $email): void
{
    $c = guest_cookie();
    guest_cookie_set($name, $email, $c['trusted'] && strcasecmp($c['email'], $email) === 0);
}

/** j***@gmail.com style mask for "we emailed you" messages. */
function guest_mask(string $email): string
{
    [$user, $domain] = explode('@', $email, 2) + ['', ''];
    return mb_substr($user, 0, 1) . str_repeat('*', max(2, min(6, mb_strlen($user) - 1))) . '@' . $domain;
}
