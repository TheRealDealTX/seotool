<?php
/**
 * Check official and ticket links of upcoming events (optional cron, e.g. daily).
 *   php app/bin/check-links.php [--limit=100]
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap.php';

if (PHP_SAPI !== 'cli') {
    exit("CLI only\n");
}
$opts = getopt('', ['limit::']);
$r = RT\LinkChecker::run((int) ($opts['limit'] ?? 100));
echo "Checked {$r['checked']} link(s); {$r['broken']} broken.\n";
