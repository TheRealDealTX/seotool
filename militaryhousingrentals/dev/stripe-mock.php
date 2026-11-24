<?php
// Tiny Stripe stand-in for local tests: Checkout Sessions API, a hosted
// "checkout page" with a promo-code field, and signed webhooks.
// php -S 127.0.0.1:8099 stripe-mock.php   (env: MOCK_WEBHOOK_URL, MOCK_WHSEC, MOCK_STATE)
$state = getenv('MOCK_STATE') ?: sys_get_temp_dir() . '/stripe-mock.json';
$db = is_file($state) ? json_decode(file_get_contents($state), true) : [];
$save = function () use (&$db, $state) { file_put_contents($state, json_encode($db)); };
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$m = $_SERVER['REQUEST_METHOD'];
header('Content-Type: application/json');
$auth = $_SERVER['PHP_AUTH_USER'] ?? '';
if (str_starts_with($path, '/v1/') && !preg_match('/^sk_test_/', $auth)) { http_response_code(401); echo json_encode(['error' => ['message' => 'Invalid API Key provided']]); return; }
if ($path === '/v1/balance') { echo json_encode(['object' => 'balance', 'livemode' => false]); return; }
if ($path === '/v1/checkout/sessions' && $m === 'POST') {
    $id = 'cs_test_' . bin2hex(random_bytes(12));
    $p = $_POST;
    $db[$id] = ['id' => $id, 'object' => 'checkout.session', 'status' => 'open', 'payment_status' => 'unpaid', 'amount_total' => (int)$p['line_items'][0]['price_data']['unit_amount'],
        'currency' => $p['line_items'][0]['price_data']['currency'], 'client_reference_id' => $p['client_reference_id'], 'metadata' => $p['metadata'],
        'customer_email' => $p['customer_email'], 'allow_promotion_codes' => $p['allow_promotion_codes'] ?? null, 'name' => $p['line_items'][0]['price_data']['product_data']['name'],
        'success_url' => str_replace('{CHECKOUT_SESSION_ID}', $id, $p['success_url']), 'cancel_url' => $p['cancel_url'],
        'url' => 'http://127.0.0.1:8099/pay/' . $id];
    $save(); echo json_encode($db[$id]); return;
}
if (preg_match('#^/v1/checkout/sessions/(cs_test_\w+)$#', $path, $mm)) {
    if (!isset($db[$mm[1]])) { http_response_code(404); echo json_encode(['error' => ['message' => 'No such checkout.session']]); return; }
    echo json_encode($db[$mm[1]]); return;
}
if (preg_match('#^/pay/(cs_test_\w+)$#', $path, $mm) && isset($db[$mm[1]])) {
    $s = &$db[$mm[1]];
    header('Content-Type: text/html; charset=utf-8');
    if ($m === 'POST') {
        $free = strtoupper(trim($_POST['promo'] ?? '')) === 'FREE100';
        $s['status'] = 'complete'; $s['payment_status'] = $free ? 'no_payment_required' : 'paid';
        if ($free) $s['amount_total'] = 0;
        $save();
        if (empty($_POST['skip_webhook']) && ($url = getenv('MOCK_WEBHOOK_URL'))) {
            $payload = json_encode(['id' => 'evt_' . bin2hex(random_bytes(6)), 'type' => 'checkout.session.completed', 'data' => ['object' => $s]]);
            $t = time(); $sig = hash_hmac('sha256', "$t.$payload", getenv('MOCK_WHSEC'));
            $ch = curl_init($url); curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $payload, CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HTTPHEADER => ['Content-Type: application/json', "Stripe-Signature: t=$t,v1=$sig"]]);
            $resp = curl_exec($ch); file_put_contents(dirname($state) . '/webhook.log', curl_getinfo($ch, CURLINFO_HTTP_CODE) . " $resp\n", FILE_APPEND);
        }
        header('Location: ' . $s['success_url'], true, 303); return;
    }
    $amt = '$' . number_format($s['amount_total'] / 100, 2);
    echo "<!doctype html><title>Mock Stripe Checkout</title><h1>Mock Stripe Checkout</h1><p data-product>" . htmlspecialchars($s['name']) . "</p><p>Total due: <strong data-amount>$amt</strong></p>"
        . "<form method=post>" . ($s['allow_promotion_codes'] === 'true' ? "<label>Add promotion code <input name=promo data-promo></label>" : '')
        . "<label><input type=checkbox name=skip_webhook value=1> skip webhook</label><button>Pay</button></form><a data-cancel href='" . htmlspecialchars($s['cancel_url']) . "'>Cancel</a>";
    return;
}
http_response_code(404); echo '{}';
