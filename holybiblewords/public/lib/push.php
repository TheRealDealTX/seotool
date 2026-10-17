<?php
// Web Push (RFC 8030/8291/8292) for the verse-of-the-day streak reminder.
// No libraries: VAPID JWT (ES256) + aes128gcm payload encryption with ext-openssl.
// Keys and subscriptions live in lib/private/ (created on first use, never served:
// lib/ is denied by .htaccess, and none of it is in the repository).

const PUSH_DIR = __DIR__ . '/private';
const PUSH_SUBJECT = 'mailto:info@holybiblewords.com';
const REMINDER_HOUR = 21;   // local time; "when the day is ending"
// Only real browser push services may be stored as endpoints.
const PUSH_HOSTS = '/(^|\.)(fcm\.googleapis\.com|android\.googleapis\.com|push\.services\.mozilla\.com|web\.push\.apple\.com|notify\.windows\.com|push\.apple\.com)$/';

function b64u(string $s): string { return rtrim(strtr(base64_encode($s), '+/', '-_'), '='); }
function b64u_dec(string $s): string { return base64_decode(strtr($s, '-_', '+/') . str_repeat('=', (4 - strlen($s) % 4) % 4)); }

function push_dir(string $sub = ''): string {
    $d = PUSH_DIR . ($sub ? "/$sub" : '');
    if (!is_dir($d)) mkdir($d, 0700, true);
    return $d;
}

/** Raw 65-byte uncompressed P-256 public key of an OpenSSL key. */
function ec_raw_public($key): string {
    $d = openssl_pkey_get_details($key)['ec'];
    return "\x04" . str_pad($d['x'], 32, "\0", STR_PAD_LEFT) . str_pad($d['y'], 32, "\0", STR_PAD_LEFT);
}

/** PEM for a raw 65-byte P-256 public key. */
function ec_public_pem(string $raw): string {
    $der = hex2bin('3059301306072a8648ce3d020106082a8648ce3d030107034200') . $raw;
    return "-----BEGIN PUBLIC KEY-----\n" . chunk_split(base64_encode($der), 64, "\n") . "-----END PUBLIC KEY-----\n";
}

/** VAPID key pair, generated once and kept in lib/private/vapid.json. */
function vapid_keys(): array {
    $f = push_dir() . '/vapid.json';
    if (is_file($f)) return json_decode(file_get_contents($f), true);
    $k = openssl_pkey_new(['curve_name' => 'prime256v1', 'private_key_type' => OPENSSL_KEYTYPE_EC]);
    openssl_pkey_export($k, $pem);
    $keys = ['private' => $pem, 'public' => b64u(ec_raw_public($k))];
    file_put_contents($f, json_encode($keys), LOCK_EX);
    chmod($f, 0600);
    return $keys;
}

/** ES256 signature: DER from OpenSSL -> 64-byte r||s. */
function der_to_jose(string $der): string {
    $o = 3;                                     // 0x30 len 0x02
    $rl = ord($der[$o]); $r = substr($der, $o + 1, $rl); $o += 1 + $rl + 1;
    $sl = ord($der[$o]); $s = substr($der, $o + 1, $sl);
    $fix = fn($x) => str_pad(ltrim($x, "\0"), 32, "\0", STR_PAD_LEFT);
    return $fix($r) . $fix($s);
}

function vapid_header(string $endpoint): string {
    $keys = vapid_keys();
    $p = parse_url($endpoint);
    $jwt = b64u(json_encode(['typ' => 'JWT', 'alg' => 'ES256'])) . '.' .
           b64u(json_encode(['aud' => $p['scheme'] . '://' . $p['host'], 'exp' => time() + 12 * 3600, 'sub' => PUSH_SUBJECT]));
    openssl_sign($jwt, $sig, $keys['private'], OPENSSL_ALGO_SHA256);
    return 'vapid t=' . $jwt . '.' . b64u(der_to_jose($sig)) . ', k=' . $keys['public'];
}

/** RFC 8291 aes128gcm body for one record. */
function push_encrypt(string $payload, string $uaPublicB64, string $authB64): string {
    $uaPub = b64u_dec($uaPublicB64);
    $auth = b64u_dec($authB64);
    $eph = openssl_pkey_new(['curve_name' => 'prime256v1', 'private_key_type' => OPENSSL_KEYTYPE_EC]);
    $asPub = ec_raw_public($eph);
    $ecdh = openssl_pkey_derive(openssl_pkey_get_public(ec_public_pem($uaPub)), $eph, 32);
    $ikm = hash_hkdf('sha256', $ecdh, 32, "WebPush: info\0" . $uaPub . $asPub, $auth);
    $salt = random_bytes(16);
    $cek = hash_hkdf('sha256', $ikm, 16, "Content-Encoding: aes128gcm\0", $salt);
    $nonce = hash_hkdf('sha256', $ikm, 12, "Content-Encoding: nonce\0", $salt);
    $ct = openssl_encrypt($payload . "\x02", 'aes-128-gcm', $cek, OPENSSL_RAW_DATA, $nonce, $tag);
    return $salt . pack('N', 4096) . chr(strlen($asPub)) . $asPub . $ct . $tag;
}

/** Sends one notification. Returns the HTTP status (404/410 = subscription gone). */
function push_send(array $sub, array $message): int {
    $body = push_encrypt(json_encode($message, JSON_UNESCAPED_UNICODE), $sub['keys']['p256dh'], $sub['keys']['auth']);
    $ch = curl_init($sub['endpoint']);
    curl_setopt_array($ch, [
        CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/octet-stream', 'Content-Encoding: aes128gcm',
            'TTL: 10800', 'Urgency: normal', 'Topic: streak',
            'Authorization: ' . vapid_header($sub['endpoint']),
        ],
    ]);
    curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    return (int)$code;
}

// ---- subscription store: one small JSON file per subscription ----

function sub_file(string $endpoint): string { return push_dir('subs') . '/' . hash('sha256', $endpoint) . '.json'; }

function valid_endpoint(string $e): bool {
    $p = parse_url($e);
    return ($p['scheme'] ?? '') === 'https' && preg_match(PUSH_HOSTS, $p['host'] ?? '') && strlen($e) < 1000;
}

function sub_save(array $s): bool {
    $e = (string)($s['endpoint'] ?? '');
    if (!valid_endpoint($e) || empty($s['keys']['p256dh']) || empty($s['keys']['auth'])) return false;
    $tz = in_array($s['tz'] ?? '', DateTimeZone::listIdentifiers(), true) ? $s['tz'] : 'UTC';
    $old = is_file(sub_file($e)) ? json_decode(file_get_contents(sub_file($e)), true) : [];
    $rec = [
        'endpoint' => $e,
        'keys' => ['p256dh' => substr((string)$s['keys']['p256dh'], 0, 200), 'auth' => substr((string)$s['keys']['auth'], 0, 100)],
        'tz' => $tz,
        'hour' => max(0, min(23, (int)($s['hour'] ?? REMINDER_HOUR))),
        'read' => $old['read'] ?? '', 'sent' => $old['sent'] ?? '', 'created' => $old['created'] ?? date('c'),
    ];
    return (bool)file_put_contents(sub_file($e), json_encode($rec), LOCK_EX);
}

function sub_mark_read(string $endpoint, string $date): void {
    $f = sub_file($endpoint);
    if (!is_file($f) || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) return;
    $rec = json_decode(file_get_contents($f), true);
    if ($date > ($rec['read'] ?? '')) { $rec['read'] = $date; file_put_contents($f, json_encode($rec), LOCK_EX); }
}

function sub_delete(string $endpoint): void {
    $f = sub_file($endpoint);
    if (is_file($f)) unlink($f);
}

/** Called by cron: remind everyone whose local reminder hour has come and who hasn't read today. */
function send_due_reminders(): array {
    $sent = $gone = 0;
    foreach (glob(push_dir('subs') . '/*.json') as $f) {
        $rec = json_decode(file_get_contents($f), true);
        if (!$rec) continue;
        $now = new DateTimeImmutable('now', new DateTimeZone($rec['tz']));
        $today = $now->format('Y-m-d');
        if ((int)$now->format('G') < $rec['hour'] || ($rec['read'] ?? '') === $today || ($rec['sent'] ?? '') === $today) continue;
        $code = push_send($rec, [
            'title' => 'Keep your streak going 🔥',
            'body' => 'You haven’t read today’s Verse of the Day yet. It only takes a minute.',
            'url' => '/verse-of-the-day/',
            'tag' => 'streak-' . $today,
        ]);
        if ($code === 404 || $code === 410) { unlink($f); $gone++; continue; }
        if ($code >= 200 && $code < 300) { $rec['sent'] = $today; file_put_contents($f, json_encode($rec), LOCK_EX); $sent++; }
    }
    return ['sent' => $sent, 'removed' => $gone];
}
