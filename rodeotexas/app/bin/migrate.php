<?php
/**
 * Apply pending SQL migrations in app/migrations/ (in filename order).
 *   php app/bin/migrate.php
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap.php';

use RT\Db;

function rt_migrate(): array
{
    Db::pdo()->exec('CREATE TABLE IF NOT EXISTS schema_migrations (version VARCHAR(100) NOT NULL PRIMARY KEY, applied_at DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4');
    $done = array_column(Db::all('SELECT version FROM schema_migrations'), 'version');
    $applied = [];
    $files = glob(RT_APP . '/migrations/*.sql') ?: [];
    sort($files);
    foreach ($files as $f) {
        $v = basename($f);
        if (in_array($v, $done, true)) {
            continue;
        }
        $sql = (string) file_get_contents($f);
        $sql = preg_replace('/^\s*--.*$/m', '', $sql) ?? $sql;
        foreach (preg_split('/;\s*(\r?\n|$)/', $sql) as $stmt) {
            if (trim($stmt) !== '') {
                Db::pdo()->exec($stmt);
            }
        }
        Db::insert('schema_migrations', ['version' => $v, 'applied_at' => now_utc()]);
        $applied[] = $v;
    }
    return $applied;
}

if (PHP_SAPI === 'cli' && realpath($argv[0] ?? '') === __FILE__) {
    $a = rt_migrate();
    echo $a ? 'Applied: ' . implode(', ', $a) . "\n" : "Database is up to date.\n";
}
