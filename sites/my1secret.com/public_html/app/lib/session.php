<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Sessions live in the database (the shared server /tmp is not private), and
 * are started lazily: anonymous visitors who never post get no cookie at all.
 */
final class M1sDbSession implements SessionHandlerInterface
{
    public function open(string $path, string $name): bool { return true; }
    public function close(): bool { return true; }

    public function read(string $id): string|false
    {
        $r = one('SELECT data FROM sessions WHERE id = ?', [hash('sha256', $id)]);
        return $r ? (string)$r['data'] : '';
    }

    public function write(string $id, string $data): bool
    {
        $h = hash('sha256', $id);
        $uid = $_SESSION['uid'] ?? null;
        if (q('UPDATE sessions SET data = ?, user_id = ?, updated_at = ? WHERE id = ?', [$data, $uid, now(), $h])->rowCount() === 0) {
            if (!one('SELECT id FROM sessions WHERE id = ?', [$h])) {
                insert('sessions', ['id' => $h, 'data' => $data, 'user_id' => $uid, 'updated_at' => now()]);
            }
        }
        return true;
    }

    public function destroy(string $id): bool
    {
        q('DELETE FROM sessions WHERE id = ?', [hash('sha256', $id)]);
        return true;
    }

    public function gc(int $max_lifetime): int|false
    {
        return q('DELETE FROM sessions WHERE updated_at < ?', [gmdate('Y-m-d H:i:s', time() - $max_lifetime)])->rowCount();
    }
}

const M1S_SESSION_NAME = 'm1s_sid';
const M1S_SESSION_LIFETIME = 60 * 60 * 24 * 30;   // 30 days

function session_start_once(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    $secure = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
    session_set_save_handler(new M1sDbSession(), true);
    session_name(M1S_SESSION_NAME);
    ini_set('session.gc_maxlifetime', (string)M1S_SESSION_LIFETIME);
    ini_set('session.gc_probability', '1');
    ini_set('session.gc_divisor', '200');
    ini_set('session.use_strict_mode', '1');
    session_set_cookie_params([
        'lifetime' => M1S_SESSION_LIFETIME,
        'path'     => '/',
        'secure'   => $secure,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_cache_limiter('');
    session_start();
}

function session_active_or_cookie(): bool
{
    return session_status() === PHP_SESSION_ACTIVE || isset($_COOKIE[M1S_SESSION_NAME]);
}
