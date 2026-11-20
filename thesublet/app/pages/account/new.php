<?php defined('APP') || exit;

// Additional listing for a signed-in host: saved, then paid via Checkout to publish.
cache_private();
$o = require_owner();
$err = [];
$d = ['furnished' => 1, 'pets' => 'no', 'min_stay' => 1, 'beds' => '1', 'baths' => '1', 'available_from' => date('Y-m-d'), 'contact_name' => $o['name']];
if (is_post()) {
    if ($g = form_guard()) $err['form'] = $g;
    elseif (!rate_limit('submit', 6, 3600)) $err['form'] = 'Too many submissions. Try again later.';
    else {
        $in = $_POST; $in['contact_email'] = $o['email'];
        [$data, $err] = listing_from_input($in, false);
        if (empty($_POST['agree'])) $err['agree'] = 'Please confirm you have the right to rent this place.';
        $d = array_merge($d, $_POST);
        if (!$err) {
            $data['slug'] = slugify($data['title'], 60);
            $data['contact_email'] = $o['email'];
            $data += ['tier' => 'free', 'status' => 'pending_payment', 'owner_id' => (int)$o['id'], 'ip' => client_ip(), 'created_at' => now(), 'updated_at' => now()];
            $lat = $data['_lat']; $lng = $data['_lng']; unset($data['_lat'], $data['_lng']);
            $id = insert('listings', $data);
            $tmp = ['_lat' => $lat, '_lng' => $lng, 'state' => $data['state'], 'city_slug' => $data['city_slug']];
            resolve_coords($tmp, $id);
            update('listings', ['lat' => $tmp['lat'], 'lng' => $tmp['lng']], 'id = ?', [$id]);
            photos_save_uploads($id);
            if (stripe_ready()) {
                try { redirect(stripe_checkout(listing_get($id), 'new', $o['email'], $o['name']), 303); }
                catch (Throwable $e) { error_log('[stripe] ' . $e->getMessage()); }
            }
            flash('Listing saved. Use “Pay & publish” to put it live' . (stripe_ready() ? '.' : ' once card payments are switched on.'), 'warn');
            redirect('/account/');
        }
    }
}
ob_start(); ?>
<div class="wrap narrow-lg section">
  <p><a href="/account/">← Your listings</a></p>
  <h1>New verified listing</h1>
  <p class="muted">Each verified listing is a one-time <?= e(price_label()) ?> and goes live as soon as payment completes.</p>
  <?php if (isset($err['form'])): ?><div class="flash flash-err"><?= e($err['form']) ?></div><?php unset($err['form']); endif; ?>
  <?= view('listing_form', ['d' => $d, 'err' => $err, 'mode' => 'new', 'action' => '/account/new/', 'submitLabel' => 'Continue to payment']) ?>
</div>
<?php
page(['title' => 'New listing | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean(), 'h_extra' => leaflet_head()]);
