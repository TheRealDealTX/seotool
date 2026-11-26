<?php
// Stripe Checkout over the REST API (no SDK). Fulfilment is idempotent and runs
// from both the success-page redirect and the checkout.session.completed webhook.

function mhr_stripe_configured() { return mhr_secret_setting('stripe_secret') !== ''; }

function mhr_stripe($method, $path, array $params = [], &$error = null) {
    $key = mhr_secret_setting('stripe_secret');
    if ($key === '') { $error = 'Stripe is not configured yet.'; return null; }
    $url = rtrim(mhr_cfg('stripe_api_base') ?: 'https://api.stripe.com', '/') . $path;
    $ch = curl_init();
    $opts = [
        CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 30, CURLOPT_CONNECTTIMEOUT => 10,
        CURLOPT_USERPWD => $key . ':', CURLOPT_HTTPHEADER => ['Stripe-Version: 2024-06-20'],
    ];
    if ($method === 'GET') $opts[CURLOPT_URL] = $url . ($params ? '?' . http_build_query($params) : '');
    else { $opts[CURLOPT_URL] = $url; $opts[CURLOPT_POST] = true; $opts[CURLOPT_POSTFIELDS] = http_build_query($params); }
    curl_setopt_array($ch, $opts);
    $body = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $cerr = curl_error($ch);
    curl_close($ch);
    if ($body === false) { $error = 'Could not reach Stripe: ' . $cerr; error_log('mhr stripe: ' . $error); return null; }
    $json = json_decode($body, true);
    if ($code >= 400 || !is_array($json)) {
        $error = $json['error']['message'] ?? "Stripe returned HTTP $code";
        error_log('mhr stripe: ' . $error);
        return null;
    }
    return $json;
}

// Creates the payment row and a Checkout Session. Returns the Checkout URL or null.
function mhr_checkout_start($kind, $slug, $title, $owner, &$error = null) {
    mhr_q('INSERT INTO mhr_payments (kind, listing_slug, owner_id, name, email, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [$kind, $slug, $owner['id'], $owner['name'], $owner['email'], 'pending', mhr_now()]);
    $pid = (int)mhr_db()->lastInsertId();
    $label = $kind === 'submit' ? 'Verified listing' : 'Listing claim & verification';
    $session = mhr_stripe('POST', '/v1/checkout/sessions', [
        'mode' => 'payment',
        'line_items' => [[
            'quantity' => 1,
            'price_data' => [
                'currency' => mhr_setting('currency', 'usd'),
                'unit_amount' => mhr_price_cents(),
                'product_data' => ['name' => mb_substr("$label: $title", 0, 250), 'description' => 'Featured placement, your contact details shown and a Verified owner badge on ' . cfg('name') . '.'],
            ],
        ]],
        'allow_promotion_codes' => 'true',
        'customer_email' => $owner['email'],
        'client_reference_id' => (string)$pid,
        'metadata' => ['payment_id' => (string)$pid, 'kind' => $kind, 'slug' => $slug],
        'success_url' => abs_url('/checkout/success/') . '?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => abs_url('/checkout/cancel/') . '?p=' . $pid . '&s=' . substr(mhr_hmac('cancel|' . $pid), 0, 20),
    ], $error);
    if (!$session || empty($session['url'])) {
        mhr_q("UPDATE mhr_payments SET status = 'failed', note = ? WHERE id = ?", [mb_substr((string)$error, 0, 255), $pid]);
        return null;
    }
    mhr_q('UPDATE mhr_payments SET stripe_session_id = ? WHERE id = ?', [$session['id'], $pid]);
    mhr_session_start();
    $_SESSION['mhr_checkout'][] = $pid;
    return $session['url'];
}

function mhr_session_paid(array $s) {
    return in_array($s['payment_status'] ?? '', ['paid', 'no_payment_required'], true) && ($s['status'] ?? 'complete') === 'complete';
}

// Applies a completed Checkout Session exactly once. Returns the payment row (or null).
function mhr_fulfil(array $s) {
    if (!mhr_session_paid($s)) return null;
    $pid = (int)($s['metadata']['payment_id'] ?? $s['client_reference_id'] ?? 0);
    $db = mhr_db();
    $db->beginTransaction();
    try {
        $p = mhr_row('SELECT * FROM mhr_payments WHERE id = ? FOR UPDATE', [$pid]);
        if (!$p || ($p['stripe_session_id'] && $p['stripe_session_id'] !== $s['id'])) { $db->rollBack(); error_log('mhr fulfil: unknown session ' . ($s['id'] ?? '?')); return null; }
        if ($p['status'] === 'fulfilled') { $db->commit(); return $p; }

        $note = null;
        $slug = $p['listing_slug'];
        $row = mhr_ensure_row($slug);
        if (!$row) $note = 'Listing no longer exists';
        elseif ($row['owner_id'] && (int)$row['owner_id'] !== (int)$p['owner_id']) $note = 'Listing already had another owner: review';
        else {
            $cols = ['owner_id' => $p['owner_id'], 'contact_visible' => 1, 'verified' => 1, 'plan' => 'paid'];
            if ($p['kind'] === 'submit' || ($row['origin'] === 'db' && in_array($row['status'], ['pending', 'rejected'], true))) {
                $cols['status'] = 'published';
                $cols['published_at'] = mhr_now();
            }
            mhr_set_cols($slug, $cols);
            // Paid listings are Featured (badge, Featured section, first in search results).
            mhr_save_fields($slug, ['featured' => true] + ($p['kind'] === 'submit' && $row['origin'] === 'db' ? ['date' => gmdate('Y-m-d')] : []));
        }
        mhr_q("UPDATE mhr_payments SET status = 'fulfilled', stripe_session_id = ?, amount_total = ?, currency = ?, payment_status = ?, note = ?, fulfilled_at = ? WHERE id = ?",
            [$s['id'], $s['amount_total'] ?? null, $s['currency'] ?? null, $s['payment_status'], $note, mhr_now(), $pid]);
        $db->commit();
    } catch (Throwable $e) {
        if ($db->inTransaction()) $db->rollBack();
        throw $e;
    }
    $p = mhr_row('SELECT * FROM mhr_payments WHERE id = ?', [$pid]);
    mhr_after_fulfil($p, $s);
    return $p;
}

function mhr_after_fulfil(array $p, array $s) {
    $owner = mhr_owner($p['owner_id']);
    [$l] = mhr_listing_full($p['listing_slug']);
    $title = $l['title'] ?? $p['listing_slug'];
    $url = abs_url('/properties/' . $p['listing_slug'] . '/');
    $amount = $p['amount_total'] !== null ? '$' . number_format($p['amount_total'] / 100, 2) . ' ' . strtoupper((string)$p['currency']) : '—';
    if ($owner) {
        $body = "Hi " . ($owner['name'] ?: 'there') . ",\n\nThanks for your payment. Here is your receipt.\n\n"
            . "Item: " . ($p['kind'] === 'submit' ? 'Verified listing' : 'Listing claim & verification') . "\nListing: $title\nAmount: $amount\n"
            . "Date: " . gmdate('F j, Y') . "\nReference: MHR-" . $p['id'] . "\n\n"
            . ($p['note'] ? "We'll review this listing and be in touch shortly.\n\n" : "Your listing is now Featured and shows your contact details and a Verified owner badge:\n$url\n\n")
            . "Manage your listing at " . abs_url('/account/') . "\n\n— " . cfg('name');
        mhr_mail($owner['email'], 'Receipt: ' . $title, $body);
        if (!$owner['email_verified_at']) mhr_send_login_link($owner, 'verify');
    }
    mhr_mail(mhr_notify_email(), 'Payment received: ' . $title,
        "Kind: {$p['kind']}\nListing: $title\n$url\nOwner: " . ($owner ? "{$owner['name']} <{$owner['email']}>" : '?') . "\nAmount: $amount\nStripe status: {$p['payment_status']}\n"
        . ($p['note'] ? "NOTE: {$p['note']}\n" : '') . "\nAdmin: " . abs_url(mhr_admin_path() . 'payments/'));
}

// Verifies the Stripe-Signature header. Returns the decoded event or null.
function mhr_stripe_verify_event($payload, $header, $secret, $tolerance = 300) {
    if ($secret === '' || $header === '') return null;
    $t = null; $sigs = [];
    foreach (explode(',', $header) as $part) {
        [$k, $v] = array_pad(explode('=', trim($part), 2), 2, '');
        if ($k === 't') $t = (int)$v;
        if ($k === 'v1') $sigs[] = $v;
    }
    if (!$t || !$sigs || abs(time() - $t) > $tolerance) return null;
    $expected = hash_hmac('sha256', $t . '.' . $payload, $secret);
    foreach ($sigs as $sig) if (hash_equals($expected, $sig)) return json_decode($payload, true);
    return null;
}

function mhr_stripe_webhook() {
    $payload = file_get_contents('php://input');
    $event = mhr_stripe_verify_event($payload, $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '', mhr_secret_setting('stripe_webhook_secret'));
    header('Content-Type: application/json');
    header('Cache-Control: no-store');
    if (!$event) { http_response_code(400); echo '{"error":"invalid signature"}'; return; }
    try {
        if (in_array($event['type'] ?? '', ['checkout.session.completed', 'checkout.session.async_payment_succeeded'], true)) {
            $s = $event['data']['object'] ?? [];
            if (!empty($s['id']) && mhr_session_paid($s)) mhr_fulfil($s);
        }
    } catch (Throwable $e) {
        error_log('mhr webhook: ' . $e->getMessage());
        http_response_code(500); echo '{"error":"server"}'; return;
    }
    echo '{"received":true}';
}
