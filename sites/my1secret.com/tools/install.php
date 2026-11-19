<?php
// CLI installer for local development:  M1S_CONFIG=... php tools/install.php
declare(strict_types=1);
define('M1S', true);
define('M1S_ROOT', dirname(__DIR__) . '/public_html');
define('M1S_APP', M1S_ROOT . '/app');
require M1S_APP . '/bootstrap.php';
require M1S_APP . '/schema.php';
$r = run_install();
echo implode("\n", $r['log']), "\n";
if ($r['admin_password']) {
    echo "admin password: {$r['admin_password']}\n";
}
