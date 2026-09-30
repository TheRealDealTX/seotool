<?php
/**
 * Authenticated endpoint for the external weekly import routine.
 * See app/lib/RemoteImport.php and docs/SOURCES.md ("External weekly routine").
 */
defined('RT_APP') || exit;

use RT\PublicForm;
use RT\RemoteImport;

header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

if (!is_https() && !cfg('debug')) {
    json_out(['error' => 'HTTPS required'], 403);
}
// Token guessing: after 20 failed attempts in an hour, the IP is refused before any check.
$fails = RT\Db::one("SELECT hits, window_start FROM rate_limits WHERE bucket = 'api-import-fail' AND ip_hash = ?", [ip_hash()]);
if ($fails && (int) $fails['hits'] >= 20 && strtotime($fails['window_start'] . ' UTC') > time() - 3600) {
    json_out(['error' => 'Too many failed attempts; try again later'], 429);
}
if (!RemoteImport::authorized()) {
    PublicForm::rateLimit('api-import-fail', 1000);
    usleep(300000);
    json_out(['error' => 'Invalid or missing token'], 401);
}
@set_time_limit(300);
ignore_user_abort(true);

if (($what ?? '') === 'sources') {
    json_out(RemoteImport::sourcesForRoutine());
}
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Allow: POST');
    json_out(['error' => 'Use POST'], 405);
}
[$code, $resp] = RemoteImport::handle((string) file_get_contents('php://input', false, null, 0, RemoteImport::MAX_BODY + 1));
json_out($resp, $code);
