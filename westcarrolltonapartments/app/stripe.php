<?php defined('WCA') || exit;

function stripe_ready(): bool
{
    return (string)setting('stripe_secret_key', '') !== '';
}

function listing_price_cents(): int
{
    return (int)setting('listing_price_cents', 1000);
}

function stripe_request(string $method, string $path, array $params = []): array
{
    $ch = curl_init('https://api.stripe.com/v1/' . ltrim($path, '/') . ($method === 'GET' && $params ? '?' . http_build_query($params) : ''));
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD => setting('stripe_secret_key') . ':',
        CURLOPT_TIMEOUT => 30,
        CURLOPT_CUSTOMREQUEST => $method,
    ]);
    if ($method !== 'GET') curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    $res = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    $data = json_decode((string)$res, true) ?: [];
    if ($code >= 400 || !$data) {
        throw new RuntimeException('Stripe error: ' . ($data['error']['message'] ?? "HTTP $code"));
    }
    return $data;
}

/**
 * Create a pending payment row + Stripe Checkout session and return the redirect URL.
 * purpose: 'claim' (existing listing) or 'submit' (new paid listing)
 */
function start_checkout(string $purpose, int $listingId, string $name, string $email, string $listingName): string
{
    $pdo = db();
    $pdo->prepare('INSERT INTO payments (purpose, listing_id, name, email, amount, status, created_at) VALUES (?,?,?,?,?,?,?)')
        ->execute([$purpose, $listingId, $name, $email, listing_price_cents(), 'pending', now()]);
    $paymentId = (int)$pdo->lastInsertId();

    $label = $purpose === 'claim' ? 'Claim & manage listing: ' : 'Featured owner listing: ';
    $session = stripe_request('POST', 'checkout/sessions', [
        'mode' => 'payment',
        'allow_promotion_codes' => 'true',
        'customer_email' => $email,
        'client_reference_id' => (string)$paymentId,
        'line_items' => [[
            'quantity' => 1,
            'price_data' => [
                'currency' => 'usd',
                'unit_amount' => listing_price_cents(),
                'product_data' => [
                    'name' => mb_substr($label . $listingName, 0, 250),
                    'description' => 'One-time fee. Shows your contact details and gives you an owner account to edit the listing on West Carrollton Apartments.',
                ],
            ],
        ]],
        'metadata' => ['payment_id' => $paymentId, 'purpose' => $purpose, 'listing_id' => $listingId],
        'success_url' => url('/checkout/success/?session_id={CHECKOUT_SESSION_ID}'),
        'cancel_url' => url('/checkout/cancel/?p=' . $paymentId),
    ]);
    $pdo->prepare('UPDATE payments SET session_id = ? WHERE id = ?')->execute([$session['id'], $paymentId]);
    return $session['url'];
}

/** Idempotently fulfil a paid Checkout session. Returns the payment row or null. */
function fulfill_session(array $session): ?array
{
    // 'no_payment_required' happens when a 100%-off promotion code is used
    if (!in_array($session['payment_status'] ?? '', ['paid', 'no_payment_required'], true)) return null;
    $pdo = db();
    $st = $pdo->prepare('SELECT * FROM payments WHERE session_id = ?');
    $st->execute([$session['id']]);
    $p = $st->fetch();
    if (!$p) return null;
    if ($p['status'] === 'paid') return $p;

    // Mark paid first (guards against double fulfilment from webhook + redirect)
    $paidCents = isset($session['amount_total']) ? (int)$session['amount_total'] : (int)$p['amount'];
    $upd = $pdo->prepare("UPDATE payments SET status = 'paid', completed_at = ?, amount = ? WHERE id = ? AND status <> 'paid'");
    $upd->execute([now(), $paidCents, $p['id']]);
    $p['amount'] = $paidCents;
    if ($upd->rowCount() === 0) return $p;

    $user = user_find_or_create($p['name'], $p['email']);
    $pdo->prepare('UPDATE payments SET user_id = ? WHERE id = ?')->execute([$user['id'], $p['id']]);

    $listing = listing_by_id((int)$p['listing_id']);
    if ($listing) {
        $pdo->prepare("UPDATE listings SET owner_id = ?, contact_visible = 1, status = 'published', updated_at = ? WHERE id = ?")
            ->execute([$user['id'], now(), $listing['id']]);
    }

    $lname = $listing['name'] ?? 'your listing';
    if (!$user['verified_at']) {
        $link = url('/account/verify/?token=' . $user['verify_token']);
        send_mail($user['email'], 'Verify your email to manage ' . $lname,
            '<p>Hi ' . e($user['name']) . ',</p><p>Thanks for your payment. Your listing <strong>' . e($lname) . '</strong> is now live with your contact details shown.</p>'
            . '<p>Please verify your email address to activate your owner account and start editing your listing:</p>'
            . email_button($link, 'Verify my email'));
    } else {
        $link = url('/account/login/');
        send_mail($user['email'], 'You now manage ' . $lname,
            '<p>Hi ' . e($user['name']) . ',</p><p>Thanks for your payment. <strong>' . e($lname) . '</strong> has been added to your owner account and your contact details are now visible.</p>'
            . email_button($link, 'Go to my account'));
    }
    notify_admin(($p['purpose'] === 'claim' ? 'Listing claimed: ' : 'Paid listing published: ') . $lname,
        '<p><strong>' . e($p['name']) . '</strong> (' . e($p['email']) . ') paid ' . money($p['amount'] / 100) . ' to '
        . ($p['purpose'] === 'claim' ? 'claim' : 'publish') . ' <a href="' . e(url('/apartments/' . ($listing['slug'] ?? '') . '/')) . '">' . e($lname) . '</a>.</p>'
        . '<p>Review it in the <a href="' . e(url('/admin/listings/edit/?id=' . (int)$p['listing_id'])) . '">admin panel</a>.</p>');
    return $p;
}

function stripe_verify_webhook(string $payload, string $sigHeader, string $secret): bool
{
    $parts = [];
    foreach (explode(',', $sigHeader) as $kv) {
        [$k, $v] = array_pad(explode('=', trim($kv), 2), 2, '');
        $parts[$k][] = $v;
    }
    $ts = (int)($parts['t'][0] ?? 0);
    if (!$ts || abs(time() - $ts) > 600) return false;
    $expected = hash_hmac('sha256', $ts . '.' . $payload, $secret);
    foreach ($parts['v1'] ?? [] as $sig) {
        if (hash_equals($expected, $sig)) return true;
    }
    return false;
}

/* ---------- Users ---------- */

function user_by_email(string $email): ?array
{
    $st = db()->prepare('SELECT * FROM users WHERE email = ?');
    $st->execute([strtolower($email)]);
    return $st->fetch() ?: null;
}

function user_find_or_create(string $name, string $email): array
{
    $email = strtolower(trim($email));
    $u = user_by_email($email);
    if ($u) return $u;
    db()->prepare('INSERT INTO users (name, email, verify_token, created_at) VALUES (?,?,?,?)')
        ->execute([$name, $email, random_token(), now()]);
    return user_by_email($email);
}
