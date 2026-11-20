<?php defined('APP') || exit;

/** Passwordless login for owners. Returns the absolute URL to email. */
function magic_link_create(int $ownerId, int $ttlMin = 60): string
{
    $token = bin2hex(random_bytes(24));
    insert('login_tokens', [
        'owner_id' => $ownerId,
        'token_hash' => hash('sha256', $token),
        'expires_at' => gmdate('Y-m-d H:i:s', time() + $ttlMin * 60),
        'created_at' => now(),
    ]);
    return base_url('/auth/' . $token . '/');
}

/** Consume a token (single use). Returns owner row or null. */
function magic_link_consume(string $token): ?array
{
    if (!preg_match('/^[a-f0-9]{48}$/', $token)) return null;
    $t = row('SELECT * FROM login_tokens WHERE token_hash = ?', [hash('sha256', $token)]);
    if (!$t || $t['used_at'] || $t['expires_at'] < now()) return null;
    update('login_tokens', ['used_at' => now()], 'id = ?', [(int)$t['id']]);
    $o = row("SELECT * FROM owners WHERE id = ? AND status = 'active'", [(int)$t['owner_id']]);
    if (!$o) return null;
    $upd = ['last_login_at' => now()];
    if (!$o['email_verified_at']) $upd['email_verified_at'] = now();
    update('owners', $upd, 'id = ?', [(int)$o['id']]);
    return row('SELECT * FROM owners WHERE id = ?', [(int)$o['id']]);
}

function magic_token_valid(string $token): bool
{
    if (!preg_match('/^[a-f0-9]{48}$/', $token)) return false;
    $t = row('SELECT used_at, expires_at FROM login_tokens WHERE token_hash = ?', [hash('sha256', $token)]);
    return $t && !$t['used_at'] && $t['expires_at'] >= now();
}

function owner_login(array $o): void
{
    session_boot();
    session_regenerate_id(true);
    $_SESSION['owner_id'] = (int)$o['id'];
}

function current_owner(): ?array
{
    if (!isset($_COOKIE['ts_sess'])) return null;
    session_boot();
    if (empty($_SESSION['owner_id'])) return null;
    static $o = false;
    if ($o === false) $o = row("SELECT * FROM owners WHERE id = ? AND status = 'active'", [(int)$_SESSION['owner_id']]);
    return $o ?: null;
}

function require_owner(): array
{
    $o = current_owner();
    if (!$o) redirect('/login/?next=' . rawurlencode($_SERVER['REQUEST_URI'] ?? '/account/'));
    return $o;
}

/* ---------- admin ---------- */

function admin_pass_hash(): string
{
    return (string)setting('admin_pass_hash', cfg('admin_pass_hash', ''));
}

function is_admin(): bool
{
    if (!isset($_COOKIE['ts_sess'])) return false;
    session_boot();
    return !empty($_SESSION['admin']) && ($_SESSION['admin_ip'] ?? '') === client_ip();
}

function require_admin(): void
{
    cache_private();
    header('X-Robots-Tag: noindex, nofollow');
    if (!is_admin()) redirect('/admin/login/');
}
