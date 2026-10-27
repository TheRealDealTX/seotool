<?php
// Admin sessions, passwords, CSRF and login throttling.
defined('HA_ROOT') || exit;

final class Auth
{
    private const MAX_FAILS = 8;      // per IP …
    private const WINDOW = 900;       // … per 15 minutes

    public static function start(): void
    {
        if (session_status() === PHP_SESSION_ACTIVE) {
            return;
        }
        $https = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
        session_name('ha_admin');
        session_set_cookie_params(['lifetime' => 0, 'path' => '/admin', 'secure' => $https, 'httponly' => true, 'samesite' => 'Lax']);
        session_start();
    }

    public static function user(): ?array
    {
        self::start();
        if (empty($_SESSION['uid'])) {
            return null;
        }
        static $u;
        if ($u === null) {
            $st = db_alive()->prepare('SELECT id, email, name, role FROM users WHERE id = ?');
            $st->execute([$_SESSION['uid']]);
            $u = $st->fetch() ?: false;
        }
        return $u ?: null;
    }

    public static function ip(): string
    {
        return mb_substr(trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]), 0, 64);
    }

    public static function throttled(): bool
    {
        $st = db()->prepare('SELECT COUNT(*) FROM login_attempts WHERE ip = ? AND at > ?');
        $st->execute([self::ip(), time() - self::WINDOW]);
        return (int) $st->fetchColumn() >= self::MAX_FAILS;
    }

    public static function attempt(string $email, string $password): bool
    {
        $st = db()->prepare('SELECT * FROM users WHERE email = ?');
        $st->execute([strtolower(trim($email))]);
        $u = $st->fetch();
        if (!$u || !password_verify($password, $u['pass_hash'])) {
            db()->prepare('INSERT INTO login_attempts (ip, at) VALUES (?, ?)')->execute([self::ip(), time()]);
            usleep(400000);
            return false;
        }
        db()->prepare('DELETE FROM login_attempts WHERE ip = ?')->execute([self::ip()]);
        if (password_needs_rehash($u['pass_hash'], PASSWORD_DEFAULT)) {
            db()->prepare('UPDATE users SET pass_hash = ? WHERE id = ?')->execute([password_hash($password, PASSWORD_DEFAULT), $u['id']]);
        }
        db()->prepare('UPDATE users SET last_login = ? WHERE id = ?')->execute([gmdate('c'), $u['id']]);
        self::start();
        session_regenerate_id(true);
        $_SESSION['uid'] = (int) $u['id'];
        return true;
    }

    public static function logout(): void
    {
        self::start();
        $_SESSION = [];
        session_destroy();
    }

    public static function csrf(): string
    {
        self::start();
        return $_SESSION['csrf'] ??= bin2hex(random_bytes(16));
    }

    public static function checkCsrf(): void
    {
        if (!hash_equals(self::csrf(), (string) ($_POST['_csrf'] ?? $_SERVER['HTTP_X_CSRF'] ?? ''))) {
            http_response_code(400);
            exit('Your session expired. Go back, refresh the page and try again.');
        }
    }

    public static function createUser(string $email, string $name, string $password, string $role = 'editor'): void
    {
        db()->prepare('INSERT INTO users (email, name, pass_hash, role, created_at) VALUES (?, ?, ?, ?, ?)')
            ->execute([strtolower(trim($email)), trim($name), password_hash($password, PASSWORD_DEFAULT), $role === 'admin' ? 'admin' : 'editor', gmdate('c')]);
    }

    public static function flash(?string $msg = null, string $type = 'ok'): ?array
    {
        self::start();
        if ($msg !== null) {
            $_SESSION['flash'] = [$type, $msg];
            return null;
        }
        $f = $_SESSION['flash'] ?? null;
        unset($_SESSION['flash']);
        return $f;
    }
}
