<?php defined('APP') || exit;

cache_private();
$payload = (string)file_get_contents('php://input');
$sig = $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '';
if (!stripe_verify_signature($payload, $sig, stripe_webhook_secret())) {
    http_response_code(400);
    echo 'Invalid signature';
    exit;
}
$event = json_decode($payload, true);
$type = $event['type'] ?? '';
try {
    if (in_array($type, ['checkout.session.completed', 'checkout.session.async_payment_succeeded'], true)) {
        fulfil_checkout($event['data']['object']);
    } elseif ($type === 'checkout.session.expired') {
        update('payments', ['status' => 'expired'], "stripe_session_id = ? AND status = 'open'", [$event['data']['object']['id'] ?? '']);
    }
} catch (Throwable $e) {
    error_log('[webhook] ' . $e->getMessage());
    http_response_code(500);
    echo 'error';
    exit;
}
http_response_code(200);
header('Content-Type: application/json');
echo '{"received":true}';
