<?php
/**
 * Create an administrator or reset an existing administrator's password.
 *
 *   php app/bin/create-admin.php --email=you@example.com --name="Your Name"
 *       (prompts for the password; or add --password=… ; or --generate to print a random one)
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap.php';

use RT\Auth;

if (PHP_SAPI !== 'cli') {
    exit("CLI only\n");
}
$opts = getopt('', ['email:', 'name::', 'password::', 'generate']);
$email = $opts['email'] ?? '';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fwrite(STDERR, "Usage: php app/bin/create-admin.php --email=you@example.com [--name=\"Name\"] [--password=… | --generate]\n");
    exit(1);
}
$name = $opts['name'] ?? 'Administrator';
if (isset($opts['generate'])) {
    $password = rtrim(strtr(base64_encode(random_bytes(18)), '+/', 'Kx'), '=');
    echo "Generated password: {$password}\n";
} elseif (isset($opts['password'])) {
    $password = (string) $opts['password'];
} else {
    echo 'Password (min 12 chars): ';
    $password = trim((string) fgets(STDIN));
}
try {
    $id = Auth::createAdmin($email, $name, $password);
    echo "Administrator #{$id} ({$email}) saved.\n";
} catch (\InvalidArgumentException $e) {
    fwrite(STDERR, $e->getMessage() . "\n");
    exit(1);
}
