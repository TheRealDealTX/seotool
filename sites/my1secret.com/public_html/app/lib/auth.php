<?php
declare(strict_types=1);
defined('M1S') || exit;

function current_user(): ?array
{
    static $loaded = false, $user = null;
    if ($loaded) {
        return $user;
    }
    $loaded = true;
    if (!session_active_or_cookie()) {
        return null;
    }
    session_start_once();
    $uid = $_SESSION['uid'] ?? null;
    if (!$uid) {
        return null;
    }
    $user = one('SELECT * FROM users WHERE id = ?', [(int)$uid]);
    if (!$user || (int)$user['banned'] === 1 || ($user['session_epoch'] ?? 0) != ($_SESSION['epoch'] ?? 0)) {
        unset($_SESSION['uid']);
        $user = null;
        return null;
    }
    if (strtotime($user['last_seen_at'] . ' UTC') < time() - 600) {
        q('UPDATE users SET last_seen_at = ? WHERE id = ?', [now(), $user['id']]);
    }
    return $user;
}

function uid(): ?int
{
    $u = current_user();
    return $u ? (int)$u['id'] : null;
}

function is_admin(?array $u = null): bool
{
    $u = $u ?? current_user();
    return $u && $u['role'] === 'admin';
}

function is_mod(?array $u = null): bool
{
    $u = $u ?? current_user();
    return $u && in_array($u['role'], ['admin', 'mod'], true);
}

function require_login(): array
{
    $u = current_user();
    if (!$u) {
        if (wants_json()) {
            json_out(['error' => 'login', 'login' => '/login/'], 401);
        }
        $next = $_SERVER['REQUEST_URI'] ?? '/';
        if (is_post()) {
            $next = parse_url($_SERVER['HTTP_REFERER'] ?? '/', PHP_URL_PATH) ?: '/';
        }
        redirect('/login/?next=' . rawurlencode($next));
    }
    return $u;
}

function require_mod(): array
{
    $u = require_login();
    if (!is_mod($u)) {
        forbidden();
    }
    return $u;
}

function require_admin(): array
{
    $u = require_login();
    if (!is_admin($u)) {
        forbidden();
    }
    return $u;
}

function login_user(array $user): void
{
    session_start_once();
    session_regenerate_id(true);
    $_SESSION['uid'] = (int)$user['id'];
    $_SESSION['epoch'] = (int)($user['session_epoch'] ?? 0);
    $_SESSION['csrf'] = bin2hex(random_bytes(32));
    q('UPDATE users SET last_seen_at = ? WHERE id = ?', [now(), $user['id']]);
}

function logout_user(): void
{
    session_start_once();
    $_SESSION = [];
    session_destroy();
    setcookie(M1S_SESSION_NAME, '', ['expires' => time() - 3600, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax',
        'secure' => ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https' || ($_SERVER['HTTPS'] ?? '') === 'on']);
}

/** Safe local redirect target from ?next= */
function safe_next(string $next, string $fallback = '/'): string
{
    if ($next === '' || $next[0] !== '/' || str_starts_with($next, '//') || str_contains($next, '\\')) {
        return $fallback;
    }
    return $next;
}

function valid_username(string $u): bool
{
    return (bool)preg_match('/^[A-Za-z0-9_-]{3,20}$/', $u)
        && !in_array(strtolower($u), reserved_usernames(), true);
}

function reserved_usernames(): array
{
    return ['admin', 'administrator', 'mod', 'moderator', 'root', 'system', 'support', 'staff', 'my1secret',
        'help', 'login', 'register', 'settings', 'null', 'undefined', 'deleted', 'anonymous', 'official'];
}

function user_url(array|string $u): string
{
    $name = is_array($u) ? $u['username'] : $u;
    return '/u/' . rawurlencode($name) . '/';
}

function user_label(array $row, string $prefix = ''): string
{
    $name = $row[$prefix . 'username'] ?? null;
    if (!$name) {
        if (!empty($row['guest_name'])) {
            return '<span class="user user-guest">' . e($row['guest_name']) . '</span> <span class="badge" title="Posted without an account">guest</span>';
        }
        return '<span class="muted">[deleted]</span>';
    }
    $role = $row[$prefix . 'role'] ?? 'member';
    $badge = $role === 'admin' ? ' <span class="badge badge-team" title="My 1 Secret team">team</span>'
        : ($role === 'mod' ? ' <span class="badge badge-mod" title="Moderator">mod</span>' : '');
    return '<a class="user" href="' . e(user_url($name)) . '">u/' . e($name) . '</a>' . $badge;
}
