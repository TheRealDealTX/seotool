<?php
// Tiny Homes Blueprint - store: Stripe Checkout, order records, download links and delivery email.
//
// Private data lives in PRIVATE_DIR (one level above public_html, never web-readable):
//   thb-secrets.php        stripe_secret (sk_live_... / sk_test_...), stripe_webhook_secret (whsec_...),
//                          download_secret (any long random string), plus the SMTP keys used by mailer.php
//   thb-plan-files/        <plan-slug>.zip - the paid downloads built by generator/build.py
//   thb-data/orders/       one JSON file per order, keyed by the Stripe Checkout Session id
//   thb-data/orders.csv    append-only sales log
//
// The flow: the plan page posts to /order/checkout/, which creates a Checkout Session and
// redirects to Stripe. Stripe sends the buyer back to /order/complete/ and also calls
// /order/webhook/; whichever arrives first records the order (fulfillment is idempotent)
// and emails the download link. /order/download/ streams the zip after checking the
// order's token, expiry and download count.

require_once __DIR__ . '/mailer.php';

const DOWNLOAD_DAYS = 365;     // link lifetime
const DOWNLOAD_MAX  = 25;      // downloads per order
const STRIPE_API    = 'https://api.stripe.com/v1';

function store_dir(string $sub = ''): string {
    $d = PRIVATE_DIR . '/thb-data' . ($sub !== '' ? "/$sub" : '');
    if (!is_dir($d)) @mkdir($d, 0750, true);
    return $d;
}

function plan_file(string $slug): string {
    return PRIVATE_DIR . '/thb-plan-files/' . basename($slug) . '.zip';
}

/** Online checkout is live once a Stripe key is configured and the plan's files are uploaded. */
function store_ready(?string $slug = null): bool {
    $s = thb_secrets();
    if (empty($s['stripe_secret'])) return false;
    return $slug === null || is_file(plan_file($slug));
}

/** Call the Stripe REST API. Returns the decoded response; throws on network or API errors. */
function stripe_api(string $method, string $path, array $params = []): array {
    $s = thb_secrets();
    $url = rtrim($s['stripe_api_base'] ?? STRIPE_API, '/') . $path;
    $ch = curl_init();
    $body = http_build_query($params);
    if ($method === 'GET' && $params) $url .= '?' . $body;
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD => $s['stripe_secret'] . ':',
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => ['Stripe-Version: 2024-06-20'],
    ]);
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }
    $raw = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    if ($raw === false) throw new RuntimeException("Stripe request failed: $err");
    $data = json_decode($raw, true) ?: [];
    if ($code >= 400) throw new RuntimeException('Stripe error: ' . ($data['error']['message'] ?? "HTTP $code"));
    return $data;
}

/** Create a Checkout Session for one plan and return its hosted payment URL. */
function create_checkout(string $slug, array $p, string $email = ''): string {
    $params = [
        'mode' => 'payment',
        'line_items' => [[
            'quantity' => 1,
            'price_data' => [
                'currency' => 'usd',
                'unit_amount' => (int)round($p['price'] * 100),
                'product_data' => [
                    'name' => $p['name'] . ' - Complete Plan Set',
                    'description' => mb_strimwidth($p['title'] . '. Construction drawings (PDF), CAD (DXF), electrical and plumbing plans, materials list, cost estimate and 3D model. Instant download; license to build one home.', 0, 480, '...'),
                    'metadata' => ['plan' => $slug],
                ],
            ],
        ]],
        'metadata' => ['plan' => $slug],
        'client_reference_id' => $slug,
        'payment_intent_data' => ['description' => SITE_NAME . ' ' . $p['name'], 'metadata' => ['plan' => $slug]],
        'allow_promotion_codes' => 'true',
        'billing_address_collection' => 'auto',
        'success_url' => SITE_URL . '/order/complete/?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => SITE_URL . "/plans/$slug/?checkout=canceled#order",
    ];
    if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)) $params['customer_email'] = $email;
    $session = stripe_api('POST', '/checkout/sessions', $params);
    if (empty($session['url'])) throw new RuntimeException('Stripe did not return a checkout URL');
    return $session['url'];
}

function order_path(string $sessionId): string {
    return store_dir('orders') . '/' . preg_replace('/[^A-Za-z0-9_]/', '', $sessionId) . '.json';
}

function load_order(string $sessionId): ?array {
    $f = order_path($sessionId);
    return is_file($f) ? json_decode((string)file_get_contents($f), true) : null;
}

function save_order(array $o): void {
    $f = order_path($o['session']);
    file_put_contents($f . '.tmp', json_encode($o, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);
    rename($f . '.tmp', $f);
}

/** Find an order by its public id (THB-XXXXXX). */
function find_order(string $orderId): ?array {
    if (!preg_match('/^THB-[A-Z0-9]{8}$/', $orderId)) return null;
    $idx = store_dir() . '/index.json';
    $map = is_file($idx) ? (json_decode((string)file_get_contents($idx), true) ?: []) : [];
    return isset($map[$orderId]) ? load_order($map[$orderId]) : null;
}

function index_order(array $o): void {
    $idx = store_dir() . '/index.json';
    $fp = fopen($idx, 'c+');
    flock($fp, LOCK_EX);
    $map = json_decode((string)stream_get_contents($fp), true) ?: [];
    $map[$o['id']] = $o['session'];
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($map));
    flock($fp, LOCK_UN);
    fclose($fp);
}

/**
 * Record a paid Checkout Session as an order and email the buyer. Safe to call more than
 * once for the same session (success page + webhook): the first call wins.
 */
function fulfill_session(array $session): ?array {
    global $PLANS;
    if (($session['payment_status'] ?? '') !== 'paid') return null;
    $slug = $session['metadata']['plan'] ?? $session['client_reference_id'] ?? '';
    if (!isset($PLANS[$slug])) {
        error_log('fulfill: unknown plan for session ' . ($session['id'] ?? '?'));
        return null;
    }
    $lock = fopen(store_dir() . '/fulfill.lock', 'c');
    flock($lock, LOCK_EX);
    try {
        if ($existing = load_order($session['id'])) return $existing;
        $p = $PLANS[$slug];
        $o = [
            'id' => 'THB-' . strtoupper(substr(bin2hex(random_bytes(6)), 0, 8)),
            'session' => $session['id'],
            'payment_intent' => is_array($session['payment_intent'] ?? null) ? $session['payment_intent']['id'] : ($session['payment_intent'] ?? ''),
            'plan' => $slug,
            'plan_name' => $p['name'] . ' - ' . $p['title'],
            'amount' => ($session['amount_total'] ?? 0) / 100,
            'currency' => strtoupper($session['currency'] ?? 'usd'),
            'email' => strtolower(trim($session['customer_details']['email'] ?? $session['customer_email'] ?? '')),
            'name' => $session['customer_details']['name'] ?? '',
            'token' => bin2hex(random_bytes(20)),
            'created' => time(),
            'expires' => time() + DOWNLOAD_DAYS * 86400,
            'downloads' => 0,
            'revoked' => false,
        ];
        save_order($o);
        index_order($o);
        $log = store_dir() . '/orders.csv';
        $new = !is_file($log);
        $fp = fopen($log, 'a');
        if ($new) fputcsv($fp, ['date', 'order', 'plan', 'amount', 'email', 'name', 'stripe_session']);
        fputcsv($fp, [date('c', $o['created']), $o['id'], $o['plan'], $o['amount'], $o['email'], $o['name'], $o['session']]);
        fclose($fp);
    } finally {
        flock($lock, LOCK_UN);
        fclose($lock);
    }
    if ($o['email']) send_mail($o['email'], "Your plan files: {$p['name']} (order {$o['id']})", order_email($o), SITE_EMAIL, SITE_NAME);
    send_mail(SITE_EMAIL, "New plan sale: {$p['name']} - \${$o['amount']} ({$o['id']})",
        "Order {$o['id']}\nPlan: {$o['plan_name']}\nAmount: \${$o['amount']} {$o['currency']}\nBuyer: {$o['name']} <{$o['email']}>\nStripe session: {$o['session']}\n\nThe buyer was emailed their download link automatically.\n",
        $o['email'], $o['name']);
    return $o;
}

function download_url(array $o): string {
    return SITE_URL . '/order/download/?o=' . rawurlencode($o['id']) . '&t=' . $o['token'];
}

function order_email(array $o): string {
    $first = trim(explode(' ', $o['name'])[0] ?? '');
    return ($first !== '' ? "Hi $first,\n\n" : "Hi,\n\n")
        . "Thank you for buying {$o['plan_name']} from " . SITE_NAME . ".\n\n"
        . "Download your complete plan set here:\n" . download_url($o) . "\n\n"
        . "The download is a zip file with the construction drawing set (PDF, 24 x 36 in.), CAD drawings (DXF), "
        . "electrical and plumbing plans, the materials list and cost estimate (CSV), a 3D model (OBJ) and images.\n\n"
        . "The link works for " . DOWNLOAD_DAYS . " days and up to " . DOWNLOAD_MAX . " downloads. Lost it? Get it again any time at "
        . SITE_URL . "/order/lookup/ with this email address.\n\n"
        . "Order number: {$o['id']}\nAmount paid: \$" . number_format($o['amount'], 2) . "\n\n"
        . "Your purchase includes a license to build one home from this plan. Want changes, such as a flipped layout or a different "
        . "foundation? Just reply to this email or call " . SITE_PHONE . " for a modification quote.\n\n"
        . "Happy building,\n" . SITE_NAME . "\n" . SITE_URL . "\n";
}

/** Verify a Stripe webhook signature header (t=...,v1=...) against the raw request body. */
function stripe_signature_ok(string $payload, string $header, string $secret, int $tolerance = 300): bool {
    $t = null;
    $sigs = [];
    foreach (explode(',', $header) as $part) {
        [$k, $v] = array_pad(explode('=', trim($part), 2), 2, '');
        if ($k === 't') $t = (int)$v;
        if ($k === 'v1') $sigs[] = $v;
    }
    if (!$t || !$sigs || abs(time() - $t) > $tolerance) return false;
    $expected = hash_hmac('sha256', $t . '.' . $payload, $secret);
    foreach ($sigs as $sig) if (hash_equals($expected, $sig)) return true;
    return false;
}

/** Simple per-IP rate limit backed by a small JSON file. */
function rate_limited(string $bucket, int $max, int $window): bool {
    $f = store_dir('ratelimit') . '/' . $bucket . '-' . hash('sha256', $_SERVER['REMOTE_ADDR'] ?? 'cli') . '.json';
    $hits = is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : [];
    $now = time();
    $hits = array_values(array_filter($hits, fn($t) => $t > $now - $window));
    if (count($hits) >= $max) return true;
    $hits[] = $now;
    file_put_contents($f, json_encode($hits), LOCK_EX);
    return false;
}

/** Orders placed with an email address (used by the lookup page). */
function orders_for_email(string $email): array {
    $email = strtolower(trim($email));
    $out = [];
    foreach (glob(store_dir('orders') . '/*.json') ?: [] as $f) {
        $o = json_decode((string)file_get_contents($f), true);
        if ($o && $o['email'] === $email && empty($o['revoked'])) $out[] = $o;
    }
    return $out;
}
