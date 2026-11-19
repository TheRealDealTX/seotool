<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Thin PDO wrapper. Production runs on MySQL; local tests run on SQLite,
 * so queries stick to SQL both understand.
 */
function db(): PDO
{
    static $pdo = null;
    if ($pdo) {
        return $pdo;
    }
    $c = cfg('db');
    $pdo = new PDO($c['dsn'], $c['user'] ?? null, $c['pass'] ?? null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ]);
    if (db_is_sqlite($pdo)) {
        $pdo->exec('PRAGMA foreign_keys = ON');
        $pdo->exec('PRAGMA journal_mode = WAL');
        $pdo->sqliteCreateFunction('LOG10', fn($x) => log10((float)$x), 1);
        $pdo->sqliteCreateFunction('GREATEST', fn(...$a) => max($a), -1);
    } else {
        $pdo->exec("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci, time_zone = '+00:00'");
    }
    return $pdo;
}

function db_is_sqlite(?PDO $pdo = null): bool
{
    return ($pdo ?? db())->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite';
}

function q(string $sql, array $params = []): PDOStatement
{
    $st = db()->prepare($sql);
    foreach ($params as $k => $v) {
        $key = is_int($k) ? $k + 1 : (str_starts_with($k, ':') ? $k : ':' . $k);
        $type = is_int($v) ? PDO::PARAM_INT : (is_null($v) ? PDO::PARAM_NULL : (is_bool($v) ? PDO::PARAM_INT : PDO::PARAM_STR));
        $st->bindValue($key, is_bool($v) ? (int)$v : $v, $type);
    }
    $st->execute();
    return $st;
}

function one(string $sql, array $params = []): ?array
{
    $r = q($sql, $params)->fetch();
    return $r === false ? null : $r;
}

function all(string $sql, array $params = []): array
{
    return q($sql, $params)->fetchAll();
}

function val(string $sql, array $params = [])
{
    $r = q($sql, $params)->fetchColumn();
    return $r === false ? null : $r;
}

function insert(string $table, array $row): int
{
    $cols = array_keys($row);
    $sql = 'INSERT INTO ' . $table . ' (' . implode(',', $cols) . ') VALUES (:' . implode(',:', $cols) . ')';
    q($sql, $row);
    return (int)db()->lastInsertId();
}

function update(string $table, array $row, string $where, array $params = []): int
{
    $set = implode(',', array_map(fn($c) => "$c = :set_$c", array_keys($row)));
    $p = [];
    foreach ($row as $k => $v) {
        $p["set_$k"] = $v;
    }
    return q("UPDATE $table SET $set WHERE $where", $p + $params)->rowCount();
}

function now(): string
{
    return gmdate('Y-m-d H:i:s');
}
