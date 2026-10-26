<?php
// Command line tasks (also what the Hostinger cron job runs).
//   php app/cli.php migrate
//   php app/cli.php import camden-heights 1810-main ...
//   php app/cli.php sync [limit]
//   php app/cli.php parse page.html "Property Name"   (debug the parser)
PHP_SAPI === 'cli' || exit;
require __DIR__ . '/bootstrap.php';
require __DIR__ . '/lib/Rise.php';

$cmd = $argv[1] ?? '';
switch ($cmd) {
    case 'migrate':
        db_migrate();
        echo "ok\n";
        break;
    case 'import':
        db_migrate();
        echo (new RiseImporter())->importSlugs(array_slice($argv, 2)), " imported\n";
        break;
    case 'sync':
        db_migrate();
        echo json_encode((new RiseImporter())->sync((int) ($argv[2] ?? 0))), "\n";
        break;
    case 'parse':
        echo json_encode(RiseParser::parse(file_get_contents($argv[2]), $argv[3] ?? ''), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE), "\n";
        break;
    default:
        fwrite(STDERR, "usage: php app/cli.php migrate|import <slug...>|sync [limit]|parse <file> <name>\n");
        exit(1);
}
