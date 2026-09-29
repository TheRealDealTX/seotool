<?php
declare(strict_types=1);

namespace RT;

use PDO;
use PDOStatement;

/**
 * Thin PDO wrapper. Every query uses prepared statements with bound values.
 * Table and column names passed to insert()/update() are always literals
 * from our own code, never user input.
 */
final class Db
{
    private static ?PDO $pdo = null;

    public static function pdo(): PDO
    {
        if (self::$pdo === null) {
            $c = cfg('db');
            $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s',
                $c['host'], (int) ($c['port'] ?? 3306), $c['name'], $c['charset'] ?? 'utf8mb4');
            self::$pdo = new PDO($dsn, $c['user'], $c['pass'], [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
                PDO::ATTR_STRINGIFY_FETCHES  => false,
            ]);
            self::$pdo->exec("SET time_zone = '+00:00'");
        }
        return self::$pdo;
    }

    /** For tests: inject a connection. */
    public static function setPdo(?PDO $pdo): void
    {
        self::$pdo = $pdo;
    }

    public static function q(string $sql, array $params = []): PDOStatement
    {
        $st = self::pdo()->prepare($sql);
        foreach ($params as $k => $v) {
            $key = is_int($k) ? $k + 1 : (str_starts_with((string) $k, ':') ? $k : ':' . $k);
            $type = is_int($v) ? PDO::PARAM_INT : ($v === null ? PDO::PARAM_NULL : (is_bool($v) ? PDO::PARAM_BOOL : PDO::PARAM_STR));
            $st->bindValue($key, $v, $type);
        }
        $st->execute();
        return $st;
    }

    public static function one(string $sql, array $params = []): ?array
    {
        $r = self::q($sql, $params)->fetch();
        return $r === false ? null : $r;
    }

    public static function all(string $sql, array $params = []): array
    {
        return self::q($sql, $params)->fetchAll();
    }

    public static function val(string $sql, array $params = [])
    {
        $r = self::q($sql, $params)->fetchColumn();
        return $r === false ? null : $r;
    }

    public static function insert(string $table, array $data): int
    {
        $cols = array_keys($data);
        $sql = 'INSERT INTO `' . $table . '` (`' . implode('`,`', $cols) . '`) VALUES (:' . implode(',:', $cols) . ')';
        self::q($sql, $data);
        return (int) self::pdo()->lastInsertId();
    }

    public static function update(string $table, array $data, string $where, array $whereParams = []): int
    {
        if (!$data) {
            return 0;
        }
        $set = [];
        $params = [];
        foreach ($data as $col => $v) {
            $set[] = '`' . $col . '` = :set_' . $col;
            $params['set_' . $col] = $v;
        }
        $sql = 'UPDATE `' . $table . '` SET ' . implode(', ', $set) . ' WHERE ' . $where;
        return self::q($sql, array_merge($params, $whereParams))->rowCount();
    }

    /** Run $fn inside a transaction; rolls back and rethrows on any error. */
    public static function tx(callable $fn)
    {
        $pdo = self::pdo();
        if ($pdo->inTransaction()) {
            return $fn();
        }
        $pdo->beginTransaction();
        try {
            $r = $fn();
            $pdo->commit();
            return $r;
        } catch (\Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
    }

    /** Build "IN (:p0,:p1…)" with params. */
    public static function in(string $prefix, array $values, array &$params): string
    {
        if (!$values) {
            return '(NULL)';
        }
        $keys = [];
        foreach (array_values($values) as $i => $v) {
            $k = $prefix . $i;
            $keys[] = ':' . $k;
            $params[$k] = $v;
        }
        return '(' . implode(',', $keys) . ')';
    }
}
