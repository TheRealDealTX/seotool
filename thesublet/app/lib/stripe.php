<?php defined('APP') || exit;

function stripe_secret(): string
{
    return (string)setting('stripe_secret', cfg('stripe_secret', ''));
}

function stripe_webhook_secret(): string
{
    return (string)setting('stripe_webhook_secret', cfg('stripe_webhook_secret', ''));
}

function listing_price_cents(): int
{
    return max(50, (int)round(((float)setting('price_usd', '10')) * 100));
}

function price_label(): string
{
    $c = listing_price_cents();
    return '$' . ($c % 100 ? number_format($c / 100, 2) : number_format($c / 100));
}

function stripe_ready(): bool
{
    return stripe_secret() !== '';
}

function stripe_api(string $method, string $path, array $params = []): array
{
    $ch = curl_init('https://api.stripe.com/v1/' . ltrim($path, '/') . ($method === 'GET' && $params ? '?' . http_build_query($params) : ''));
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD => stripe_secret() . ':',
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => ['Stripe-Version: 2024-06-20'],
    ]);
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    }
    $res = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    if ($res === false) throw new RuntimeException('Stripe request failed: ' . $err);
    $data = json_decode($res, true) ?: [];
    if ($code >= 400) throw new RuntimeException('Stripe: ' . ($data['error']['message'] ?? "HTTP $code"));
    return $data;
}

/** Create a Checkout Session for a listing. $kind: new|upgrade */
function stripe_checkout(array $listing, string $kind, string $email, string $name, array $meta = []): string
{
    $title = $kind === 'upgrade' ? 'Verified listing upgrade' : ($kind === 'claim' ? 'Verified property claim' : 'Verified sublet listing');
    $session = stripe_api('POST', 'checkout/sessions', [
        'mode' => 'payment',
        'customer_email' => $email,
        'client_reference_id' => (string)$listing['id'],
        'allow_promotion_codes' => 'true',
        'line_items' => [[
            'quantity' => 1,
            'price_data' => [
                'currency' => 'usd',
                'unit_amount' => listing_price_cents(),
                'product_data' => [
                    'name' => $title . ' — The Sublet',
                    'description' => mb_substr('Auto-published listing with contact details shown, Verified host badge and owner dashboard: ' . $listing['title'], 0, 300),
                ],
            ],
        ]],
        'metadata' => ['listing_id' => (string)$listing['id'], 'kind' => $kind, 'name' => mb_substr($name, 0, 120)] + $meta,
        'success_url' => base_url('/checkout/success/?session_id={CHECKOUT_SESSION_ID}'),
        'cancel_url' => base_url('/checkout/cancel/?listing=' . $listing['id']),
    ]);
    insert('payments', [
        'listing_id' => (int)$listing['id'],
        'stripe_session_id' => $session['id'],
        'kind' => $kind,
        'amount_cents' => listing_price_cents(),
        'currency' => 'usd',
        'status' => 'open',
        'email' => $email,
        'created_at' => now(),
    ]);
    return $session['url'];
}

/** Verify Stripe-Signature header. */
function stripe_verify_signature(string $payload, string $header, string $secret, int $tolerance = 300): bool
{
    if ($secret === '' || $header === '') return false;
    $t = null; $sigs = [];
    foreach (explode(',', $header) as $part) {
        [$k, $v] = array_pad(explode('=', trim($part), 2), 2, '');
        if ($k === 't') $t = (int)$v;
        if ($k === 'v1') $sigs[] = $v;
    }
    if (!$t || !$sigs || abs(time() - $t) > $tolerance) return false;
    $expected = hash_hmac('sha256', $t . '.' . $payload, $secret);
    foreach ($sigs as $s) if (hash_equals($expected, $s)) return true;
    return false;
}

/**
 * Idempotently fulfil a completed Checkout Session (from webhook or success page).
 * Treats payment_status 'paid' and 'no_payment_required' (100%-off promo) as paid.
 */
function fulfil_checkout(array $s): ?int
{
    $paid = in_array($s['payment_status'] ?? '', ['paid', 'no_payment_required'], true);
    if (!$paid || ($s['status'] ?? 'complete') === 'expired') return null;
    $listingId = (int)($s['metadata']['listing_id'] ?? $s['client_reference_id'] ?? 0);
    $kind = $s['metadata']['kind'] ?? 'new';
    $l = listing_get($listingId);
    if (!$l) return null;

    $pay = row('SELECT * FROM payments WHERE stripe_session_id = ?', [$s['id']]);
    if ($pay && $pay['status'] === 'complete') return (int)$pay['owner_id'];

    $email = strtolower($s['customer_details']['email'] ?? $s['customer_email'] ?? $l['contact_email']);
    $name = $s['metadata']['name'] ?? $s['customer_details']['name'] ?? $l['contact_name'];
    $owner = row('SELECT * FROM owners WHERE email = ?', [$email]);
    $ownerId = $owner ? (int)$owner['id'] : insert('owners', ['email' => $email, 'name' => mb_substr((string)$name, 0, 120), 'created_at' => now()]);

    $promo = '';
    if (!empty($s['total_details']['amount_discount'])) $promo = 'discount ' . number_format($s['total_details']['amount_discount'] / 100, 2);
    $data = [
        'owner_id' => $ownerId, 'status' => 'complete', 'completed_at' => now(), 'email' => $email,
        'amount_cents' => (int)($s['amount_total'] ?? 0), 'promo' => $promo, 'listing_id' => $listingId,
    ];
    if ($pay) update('payments', $data, 'id = ?', [(int)$pay['id']]);
    else insert('payments', $data + ['stripe_session_id' => $s['id'], 'kind' => $kind, 'currency' => 'usd', 'created_at' => now()]);

    update('listings', ['tier' => 'paid', 'owner_id' => $ownerId, 'updated_at' => now()], 'id = ?', [$listingId]);
    if ($kind === 'claim') {
        $claim = row('SELECT * FROM claims WHERE id = ?', [(int)($s['metadata']['claim_id'] ?? 0)]);
        if ($claim) approve_claim($claim, true, $ownerId);
    }
    if (in_array($l['status'], ['pending', 'pending_payment', 'expired', 'rejected'], true) || $l['status'] === 'active') {
        publish_listing($listingId);
    }
    $l = listing_get($listingId);
    $o = row('SELECT * FROM owners WHERE id = ?', [$ownerId]);
    $link = magic_link_create($ownerId);
    send_mail($email, $o['email_verified_at'] ? 'Your verified listing is live on The Sublet' : 'Verify your email to manage your listing on The Sublet',
        view('emails/paid', ['l' => $l, 'o' => $o, 'link' => $link]));
    notify_admin('Paid listing #' . $listingId . ' (' . $kind . ')', '<p>' . e($l['title']) . ' — ' . e($email) . '</p><p><a href="' . e(base_url(listing_url($l))) . '">View listing</a></p>');
    return $ownerId;
}

/** Give a claimant control of a directory listing. $paid: verified via Stripe. */
function approve_claim(array $c, bool $paid, ?int $ownerId = null): void
{
    $l = listing_get((int)$c['listing_id']);
    if (!$l) return;
    if (!$ownerId) {
        $o = row('SELECT * FROM owners WHERE email = ?', [$c['email']]);
        $ownerId = $o ? (int)$o['id'] : insert('owners', ['email' => $c['email'], 'name' => $c['name'], 'phone' => $c['phone'], 'created_at' => now()]);
    }
    $upd = [
        'owner_id' => $ownerId, 'contact_name' => $c['name'], 'contact_email' => $c['email'], 'contact_phone' => $c['phone'],
        'claimed_at' => now(), 'status' => 'active', 'updated_at' => now(), 'published_at' => $l['published_at'] ?: now(),
    ];
    if (trim((string)$l['description']) === '' ) {
        $upd['description'] = $l['title'] . ' offers ' . strtolower(property_types()[$l['property_type']] ?? 'furnished housing') . ' in ' . $l['city'] . ', ' . $l['state'] . '. Contact us for current rates, minimum stays and availability.';
    }
    update('listings', $upd, 'id = ?', [(int)$l['id']]);
    update('claims', ['status' => 'approved', 'decided_at' => now()], 'id = ?', [(int)$c['id']]);
    // any other open claims on the same listing are closed
    q("UPDATE claims SET status = 'superseded', decided_at = ? WHERE listing_id = ? AND id <> ? AND status IN ('pending','pending_payment')", [now(), (int)$l['id'], (int)$c['id']]);
    if (!$paid) {
        $l = listing_get((int)$l['id']);
        send_mail($c['email'], 'Your claim for ' . $l['title'] . ' is approved',
            '<p>Hi ' . e($c['name']) . ',</p><p>You now manage <strong>' . e($l['title']) . '</strong> on The Sublet. Sign in to add photos, monthly rates, availability and house rules:</p>'
            . email_button(magic_link_create($ownerId), 'Open my dashboard')
            . '<p>Want a Verified host badge, top placement and your contact details shown? <a href="' . e(upgrade_link($l)) . '">Upgrade for ' . e(price_label()) . '</a>.</p>');
    }
}
