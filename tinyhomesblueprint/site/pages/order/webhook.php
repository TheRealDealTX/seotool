<?php
// POST /order/webhook/ - Stripe webhook endpoint. Configure it in the Stripe dashboard for
// checkout.session.completed, checkout.session.async_payment_succeeded and charge.refunded.
require_once __DIR__ . '/../../inc/store.php';
header('Content-Type: application/json');
$payload = (string)file_get_contents('php://input');
$secret = thb_secrets()['stripe_webhook_secret'] ?? '';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || $secret === '' || !stripe_signature_ok($payload, $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '', $secret)) {
    http_response_code(400);
    echo '{"error":"invalid signature"}';
    exit;
}
$event = json_decode($payload, true) ?: [];
$obj = $event['data']['object'] ?? [];
try {
    switch ($event['type'] ?? '') {
        case 'checkout.session.completed':
        case 'checkout.session.async_payment_succeeded':
            fulfill_session($obj);
            break;
        case 'charge.refunded':
            // A full refund disables the download link.
            if (($obj['amount_refunded'] ?? 0) >= ($obj['amount'] ?? PHP_INT_MAX)) {
                foreach (glob(store_dir('orders') . '/*.json') ?: [] as $f) {
                    $o = json_decode((string)file_get_contents($f), true);
                    if ($o && $o['payment_intent'] !== '' && $o['payment_intent'] === ($obj['payment_intent'] ?? null)) {
                        $o['revoked'] = true;
                        save_order($o);
                    }
                }
            }
            break;
    }
} catch (Throwable $e) {
    error_log('webhook: ' . $e->getMessage());
    http_response_code(500);
    echo '{"error":"processing failed"}';
    exit;
}
echo '{"received":true}';
