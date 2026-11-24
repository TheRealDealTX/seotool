<?php
// /submit-property/ handling: free listings wait for review; paid listings go to
// Stripe and are published the moment payment completes. A cancelled checkout
// leaves the submission as a free, pending listing.

function mhr_free_received_email($name, $title) {
    return "Hi " . ($name ?: 'there') . ",\n\nThanks for submitting \"$title\" to " . cfg('name') . ". Our team will review it, usually within 1–2 business days.\n\n"
        . "Once it's approved, the listing is published with your contact details hidden. We'll email you a link to verify it for " . mhr_price_label()
        . ", which shows your phone, email and website and adds a Verified owner badge.\n\n— " . cfg('name');
}

function mhr_submit_values() {
    $keys = ['name', 'email', 'phone', 'plan', 'pname', 'address', 'base', 'operator', 'price', 'rent_note', 'proximity', 'beds', 'bath', 'area',
        'pets', 'utilities', 'eligibility', 'amenities', 'listing_phone', 'listing_email', 'website', 'description', 'photos', 'bah'];
    $v = [];
    foreach ($keys as $k) $v[$k] = in_array($k, ['description', 'amenities'], true) ? mhr_post($k, 5000) : mhr_line($k, 300);
    $v['plan'] = $v['plan'] === 'paid' ? 'paid' : 'free';
    $v['email'] = mb_strtolower($v['email']);
    return $v;
}

// Returns ['state' => null|'free'|'error', 'errors' => [], 'values' => []]. Redirects to Stripe for paid listings.
function mhr_submit_handle() {
    mhr_session_start();
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') return ['state' => null, 'errors' => [], 'values' => ['plan' => ($_GET['plan'] ?? '') === 'paid' ? 'paid' : 'free']];
    $g = mhr_guard_check();
    if ($g === 'honeypot') return ['state' => 'free', 'errors' => [], 'values' => []];
    $v = mhr_submit_values();
    $err = $g ? [$g] : [];
    if (time() - ($_SESSION['last_submit'] ?? 0) < 30) $err[] = 'Please wait a few seconds before sending another submission.';
    foreach (['name' => 'Your name', 'email' => 'Your email', 'phone' => 'Your phone', 'pname' => 'Property name', 'address' => 'Address', 'description' => 'Property description'] as $k => $label)
        if ($v[$k] === '') $err[] = "$label is required.";
    if ($v['email'] !== '' && !filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $err[] = 'Please enter a valid email address.';
    if ($v['listing_email'] !== '' && !filter_var($v['listing_email'], FILTER_VALIDATE_EMAIL)) $err[] = 'Please enter a valid public contact email.';
    $base = null;
    foreach (bases() as $b) if ($b['slug'] === $v['base'] || $b['name'] === $v['base']) $base = $b;
    if (!$base) $err[] = 'Please choose the nearest installation.';
    $website = $v['website'];
    if ($website !== '' && !preg_match('#^https?://#i', $website)) $website = 'https://' . $website;
    if ($website !== '' && !filter_var($website, FILTER_VALIDATE_URL)) $err[] = 'Please enter a valid website address.';
    if ($v['photos'] !== '' && !filter_var($v['photos'], FILTER_VALIDATE_URL)) $err[] = 'The photo link must be a full link starting with https://';
    if ($v['plan'] === 'paid' && empty($_POST['authorized'])) $err[] = 'Please confirm you are the owner, manager or an authorized representative.';
    if ($err) return ['state' => 'error', 'errors' => $err, 'values' => $v];

    try { mhr_db(); } catch (MhrDbUnavailable $e) {
        return ['state' => 'error', 'errors' => ['Submissions are temporarily unavailable. Please try again shortly or contact us.'], 'values' => $v];
    }
    $slug = mhr_unique_slug($v['pname']);
    [$images, $img_err] = mhr_handle_uploads('photo_files', $v['pname'], MHR_MAX_PHOTOS);
    [$lat, $lng] = mhr_base_center($base['slug']);
    $highlights = [];
    if ($v['bah'] !== '') $highlights[] = 'BAH-friendly rent';
    $data = mhr_normalize([
        'slug' => $slug, 'title' => $v['pname'], 'base' => $base['slug'], 'featured' => false, 'date' => gmdate('Y-m-d'),
        'address' => $v['address'], 'lat' => $lat, 'lng' => $lng,
        'price' => (int)preg_replace('/[^0-9]/', '', explode('.', $v['price'])[0]),
        'rent_note' => $v['rent_note'] !== '' ? $v['rent_note'] : null,
        'beds' => round((float)$v['beds'], 1), 'baths' => round((float)$v['bath'], 1), 'sqft' => (int)$v['area'],
        'website' => $website, 'amenities' => mhr_list_from_text($v['amenities']), 'images' => $images,
        'description' => mhr_text_to_html($v['description']), 'operator' => $v['operator'],
        'phone' => $v['listing_phone'] !== '' ? $v['listing_phone'] : $v['phone'], 'email' => $v['listing_email'],
        'eligibility' => $v['eligibility'], 'pets' => $v['pets'], 'utilities' => $v['utilities'],
        'nearby' => $v['proximity'] !== '' ? [$v['proximity'] . ' to ' . $base['name']] : [],
        'highlights' => $highlights, 'photo_note' => $images ? 'Photos provided by the owner.' : '',
    ]);
    if (!$data['rent_note']) unset($data['rent_note']);
    mhr_q("INSERT INTO mhr_listings (slug, origin, data, status, plan, submitter_name, submitter_email, submitter_phone, admin_note, created_at, updated_at)
           VALUES (?, 'db', ?, 'pending', ?, ?, ?, ?, ?, ?, ?)", [$slug, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), $v['plan'],
        $v['name'], $v['email'], $v['phone'], $v['photos'] !== '' ? 'Photo link from submitter: ' . $v['photos'] : null, mhr_now(), mhr_now()]);
    $_SESSION['last_submit'] = time();

    $summary = $v + ['slug' => $slug, 'photos_uploaded' => count($images)];
    mhr_log_message('submit', $v['name'], $v['email'], $v['phone'], 'Property: ' . $v['pname'], array_diff_key($summary, array_flip(['name', 'email', 'phone'])));
    @file_put_contents(APP . '/storage/submissions.log', json_encode(['kind' => 'submit', 'at' => date('c'), 'ip' => mhr_client_ip()] + $summary, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
    mhr_mail(mhr_notify_email(), 'New ' . $v['plan'] . ' property submission: ' . $v['pname'],
        "Plan: {$v['plan']}\nProperty: {$v['pname']}\nAddress: {$v['address']}\nBase: {$base['name']}\nSubmitted by: {$v['name']} <{$v['email']}> {$v['phone']}\nPhotos uploaded: " . count($images)
        . ($v['plan'] === 'paid' ? "\n\nThe listing goes live automatically once payment completes; if checkout is cancelled it stays pending as a free listing." : '')
        . "\n\nReview: " . abs_url(mhr_admin_path() . 'listings/' . $slug . '/'), $v['email']);

    if ($v['plan'] === 'paid') {
        $owner = mhr_owner_find_or_create($v['name'], $v['email']);
        $url = mhr_stripe_configured() && $owner['status'] === 'active' ? mhr_checkout_start('submit', $slug, $v['pname'], $owner, $e) : null;
        if ($url) mhr_redirect($url);
        mhr_set_cols($slug, ['plan' => 'free']);
        mhr_mail($v['email'], 'We received your property: ' . $v['pname'], mhr_free_received_email($v['name'], $v['pname']));
        return ['state' => 'free', 'errors' => array_merge(['Online payment is not available right now, so we saved your property as a free listing for review.'], $img_err), 'values' => []];
    }
    mhr_mail($v['email'], 'We received your property: ' . $v['pname'], mhr_free_received_email($v['name'], $v['pname']));
    return ['state' => 'free', 'errors' => $img_err, 'values' => []];
}
