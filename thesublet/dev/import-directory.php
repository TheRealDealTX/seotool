<?php
// CLI: php dev/import-directory.php [path/to/directory.json]  — uses app/config.php DB
define('APP', true);
$_SERVER['HTTP_HOST'] = 'cli';
require __DIR__ . '/../app/bootstrap.php';
$file = $argv[1] ?? __DIR__ . '/directory/directory.json';
$rows = json_decode(file_get_contents($file), true) ?: [];
print_r(import_directory($rows));
