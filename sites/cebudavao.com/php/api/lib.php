<?php
// Shared helpers for the small JSON endpoints. The host does not let PHP write
// outside public_html, so private data lives in api/_data/ as .php files that
// start with an exit guard: requesting them runs PHP and returns nothing.
const CD_GUARD = "<?php http_response_code(404); exit; ?>\n";
function cd_data_dir() {
    $d = __DIR__ . '/_data';
    if (!is_dir($d)) @mkdir($d, 0700, true);
    if (!is_file($d . '/index.php')) @file_put_contents($d . '/index.php', CD_GUARD);
    return is_writable($d) ? $d : sys_get_temp_dir();
}
function cd_append_private($name, $line) {
    $f = cd_data_dir() . '/' . $name . '.php';
    if (!is_file($f)) @file_put_contents($f, CD_GUARD);
    return @file_put_contents($f, $line, FILE_APPEND | LOCK_EX);
}
function cd_config() {
    // Optional server-side config, never committed: api/_data/config.php containing
    //   <?php return ['notify_email' => 'you@example.com'];
    // (requested directly it just returns nothing).
    $f = __DIR__ . '/_data/config.php';
    return is_file($f) ? (include $f) : [];
}
function cd_json($data, $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function cd_rate_limit($bucket, $max, $window) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0';
    $ip = trim(explode(',', $ip)[0]);
    $f = cd_data_dir() . '/rl-' . $bucket . '-' . md5($ip) . '.txt';
    $now = time();
    $hits = is_file($f) ? array_filter(array_map('intval', file($f)), fn($t) => $t > $now - $window) : [];
    if (count($hits) >= $max) return false;
    $hits[] = $now;
    @file_put_contents($f, implode("\n", $hits));
    return true;
}
function cd_post_only() {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') cd_json(['ok' => false, 'error' => 'POST only'], 405);
    if (!empty($_POST['website'])) cd_json(['ok' => true, 'message' => 'Thanks!']);   // honeypot
}
