<?php
declare(strict_types=1);

namespace RT;

/**
 * Admin sessions and login.
 *  - password_hash()/password_verify() with PASSWORD_DEFAULT (bcrypt/argon), rehash on login
 *  - secure, HttpOnly, SameSite=Strict session cookie scoped to /admin/, strict mode
 *  - session id regenerated on login; idle (2h) and absolute (12h) timeouts
 *  - login throttling per e-mail and per IP (hashed)
 *  - CSRF token per session, checked on every POST
 */
final class Auth
{
    public const IDLE = 7200;
    public const ABSOLUTE = 43200;
    public const MAX_FAILS_EMAIL = 5;
    public const MAX_FAILS_IP = 20;
    public const WINDOW_MIN = 15;

    public static function start(): void
    {
        if (session_status() === PHP_SESSION_ACTIVE) {
            return;
        }
        ini_set('session.use_strict_mode', '1');
        ini_set('session.use_only_cookies', '1');
        ini_set('session.cookie_httponly', '1');
        ini_set('session.gc_maxlifetime', (string) self::ABSOLUTE);
        $dir = RT_STORAGE . '/cache/sessions';
        if (!is_dir($dir)) {
            @mkdir($dir, 0700, true);
        }
        if (is_dir($dir) && is_writable($dir)) {
            session_save_path($dir);
        }
        session_name('rt_admin');
        session_set_cookie_params([
            'lifetime' => 0,
            'path'     => '/admin/',
            'secure'   => is_https(),
            'httponly' => true,
            'samesite' => 'Strict',
        ]);
        session_start();

        $now = time();
        if (isset($_SESSION['admin_id'])) {
            $idle = $now - (int) ($_SESSION['last_seen'] ?? 0);
            $age = $now - (int) ($_SESSION['login_at'] ?? 0);
            if ($idle > self::IDLE || $age > self::ABSOLUTE) {
                self::logout();
                session_start();
            }
        }
        $_SESSION['last_seen'] = $now;
        if (empty($_SESSION['csrf'])) {
            $_SESSION['csrf'] = bin2hex(random_bytes(32));
        }
    }

    public static function user(): ?array
    {
        if (empty($_SESSION['admin_id'])) {
            return null;
        }
        static $cache = null;
        if ($cache === null || (int) $cache['id'] !== (int) $_SESSION['admin_id']) {
            $cache = Db::one('SELECT id, email, name, last_login_at FROM admins WHERE id = ?', [(int) $_SESSION['admin_id']]);
        }
        return $cache;
    }

    public static function require(): array
    {
        $u = self::user();
        if (!$u) {
            redirect('/admin/?page=login');
        }
        return $u;
    }

    public static function isThrottled(string $email): bool
    {
        $since = gmdate('Y-m-d H:i:s', time() - self::WINDOW_MIN * 60);
        $byEmail = (int) Db::val('SELECT COUNT(*) FROM login_attempts WHERE email = ? AND success = 0 AND attempted_at > ?', [strtolower($email), $since]);
        $byIp = (int) Db::val('SELECT COUNT(*) FROM login_attempts WHERE ip_hash = ? AND success = 0 AND attempted_at > ?', [ip_hash(), $since]);
        return $byEmail >= self::MAX_FAILS_EMAIL || $byIp >= self::MAX_FAILS_IP;
    }

    /** @return string|null error message, or null on success */
    public static function attempt(string $email, string $password): ?string
    {
        $email = strtolower(trim($email));
        if (self::isThrottled($email)) {
            return 'Too many failed attempts. Please wait ' . self::WINDOW_MIN . ' minutes and try again.';
        }
        $row = Db::one('SELECT id, password_hash FROM admins WHERE email = ?', [$email]);
        // Verify against a dummy hash when the user does not exist (constant-ish timing).
        static $dummy = null;
        $dummy ??= password_hash(bin2hex(random_bytes(8)), PASSWORD_DEFAULT);
        $hash = $row['password_hash'] ?? $dummy;
        $ok = password_verify($password, $hash) && $row !== null;
        Db::insert('login_attempts', [
            'ip_hash' => ip_hash(), 'email' => $email, 'success' => $ok ? 1 : 0, 'attempted_at' => now_utc(),
        ]);
        if (!$ok) {
            usleep(random_int(200000, 500000));
            return 'Incorrect e-mail or password.';
        }
        if (password_needs_rehash($row['password_hash'], PASSWORD_DEFAULT)) {
            Db::update('admins', ['password_hash' => password_hash($password, PASSWORD_DEFAULT)], 'id = :id', ['id' => $row['id']]);
        }
        session_regenerate_id(true);
        $_SESSION['admin_id'] = (int) $row['id'];
        $_SESSION['login_at'] = time();
        $_SESSION['last_seen'] = time();
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
        Db::update('admins', ['last_login_at' => now_utc()], 'id = :id', ['id' => $row['id']]);
        // Housekeeping.
        Db::q('DELETE FROM login_attempts WHERE attempted_at < ?', [gmdate('Y-m-d H:i:s', time() - 86400 * 30)]);
        return null;
    }

    public static function logout(): void
    {
        $_SESSION = [];
        if (session_status() === PHP_SESSION_ACTIVE) {
            $p = session_get_cookie_params();
            setcookie(session_name(), '', ['expires' => time() - 3600, 'path' => $p['path'], 'secure' => $p['secure'], 'httponly' => true, 'samesite' => 'Strict']);
            session_destroy();
        }
    }

    public static function csrfToken(): string
    {
        return (string) ($_SESSION['csrf'] ?? '');
    }

    public static function csrfField(): string
    {
        return '<input type="hidden" name="_csrf" value="' . e(self::csrfToken()) . '">';
    }

    public static function checkCsrf(): void
    {
        $sent = (string) ($_POST['_csrf'] ?? '');
        if ($sent === '' || !hash_equals(self::csrfToken(), $sent)) {
            http_response_code(400);
            exit('Invalid or expired form token. Go back, reload the page and try again.');
        }
        // Same-origin check as a second layer.
        $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
        $oHost = (string) parse_url($origin, PHP_URL_HOST);
        $oPort = parse_url($origin, PHP_URL_PORT);
        $originHost = strtolower($oHost . ($oPort ? ':' . $oPort : ''));
        if ($origin !== '' && $origin !== 'null' && $originHost !== strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''))) {
            http_response_code(400);
            exit('Cross-origin request rejected.');
        }
    }

    public static function createAdmin(string $email, string $name, string $password): int
    {
        if (strlen($password) < 12) {
            throw new \InvalidArgumentException('Password must be at least 12 characters.');
        }
        $email = strtolower(trim($email));
        $existing = Db::val('SELECT id FROM admins WHERE email = ?', [$email]);
        $hash = password_hash($password, PASSWORD_DEFAULT);
        if ($existing) {
            Db::update('admins', ['password_hash' => $hash, 'name' => $name], 'id = :id', ['id' => $existing]);
            return (int) $existing;
        }
        return Db::insert('admins', ['email' => $email, 'name' => $name, 'password_hash' => $hash, 'created_at' => now_utc()]);
    }
}
