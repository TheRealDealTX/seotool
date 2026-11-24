<?php defined('APP') || exit;

cache_private();
$owner = current_owner();
$d = ['furnished' => 1, 'pets' => 'no', 'min_stay' => 1, 'beds' => '1', 'baths' => '1',
    'city' => get('city'), 'state' => strtoupper(get('state')), 'available_from' => date('Y-m-d')];
if ($owner) { $d['contact_name'] = $owner['name']; $d['contact_email'] = $owner['email']; }
$tier = get('tier') === 'free' ? 'free' : (get('tier') === 'paid' ? 'paid' : 'paid');
$err = [];

if (is_post()) {
    $tier = post('tier') === 'free' ? 'free' : 'paid';
    if ($g = form_guard()) {
        $err['form'] = $g;
    } elseif (!rate_limit('submit', 6, 3600)) {
        $err['form'] = 'Too many submissions from your connection. Please try again in an hour.';
    } else {
        [$data, $err] = listing_from_input($_POST);
        if (empty($_POST['agree'])) $err['agree'] = 'Please confirm you have the right to rent this place.';
        $d = array_merge($d, $_POST);
        if (!$err) {
            $data['slug'] = slugify($data['title'], 60);
            $data['tier'] = 'free';
            $data['status'] = $tier === 'paid' ? 'pending_payment' : 'pending';
            $data['owner_id'] = $owner['id'] ?? null;
            $data['ip'] = client_ip();
            $data['created_at'] = $data['updated_at'] = now();
            $data['lat'] = $data['lng'] = null;
            $lat = $data['_lat']; $lng = $data['_lng']; unset($data['_lat'], $data['_lng']);
            $id = insert('listings', $data);
            $tmp = ['_lat' => $lat, '_lng' => $lng, 'state' => $data['state'], 'city_slug' => $data['city_slug']];
            resolve_coords($tmp, $id);
            update('listings', ['lat' => $tmp['lat'], 'lng' => $tmp['lng']], 'id = ?', [$id]);
            [, $photoErr] = photos_save_uploads($id);
            $l = listing_get($id);

            if ($tier === 'paid' && stripe_ready()) {
                try {
                    $url = stripe_checkout($l, 'new', $l['contact_email'], $l['contact_name']);
                    redirect($url, 303);
                } catch (Throwable $e) {
                    error_log('[stripe] ' . $e->getMessage());
                    update('listings', ['status' => 'pending'], 'id = ?', [$id]);
                    flash('We couldn’t start the payment, so your listing was saved as a free listing for review. You can upgrade later from the email we send you.', 'warn');
                    $tier = 'free';
                }
            } elseif ($tier === 'paid') {
                update('listings', ['status' => 'pending'], 'id = ?', [$id]);
                flash('Card payments aren’t switched on yet, so your listing was saved as a free listing for review. We’ll email you an upgrade link once payments are available.', 'warn');
                $tier = 'free';
            }
            $l = listing_get($id);
            send_mail($l['contact_email'], 'We received your listing: ' . $l['title'], view('emails/received', ['l' => $l]));
            notify_admin('New listing to review: #' . $id, '<p><strong>' . e($l['title']) . '</strong> — ' . e($l['city'] . ', ' . $l['state']) . ' — ' . money($l['rent']) . '/mo</p><p>' . e(excerpt($l['description'], 300)) . '</p><p><a href="' . e(base_url('/admin/listing/' . $id . '/')) . '">Review in admin</a></p>');
            if ($photoErr) flash('Some photos couldn’t be added: ' . implode(' ', $photoErr), 'warn');
            session_boot();
            $_SESSION['last_submit'] = $id;
            redirect('/post-a-sublet/thanks/', 303);
        }
    }
}

$tierHtml = '<fieldset class="tier-pick"><legend>Choose a listing type</legend><div class="tiers tiers-pick">'
    . '<label class="tier tier-hi"><input type="radio" name="tier" value="paid"' . ($tier === 'paid' ? ' checked' : '') . '><span class="tier-body"><strong>Verified listing — ' . e(price_label()) . ' one-time</strong>'
    . '<span>Published instantly · contact details shown · “Verified host” badge · dashboard to edit, renew &amp; add photos. Promo codes accepted at checkout.</span></span></label>'
    . '<label class="tier"><input type="radio" name="tier" value="free"' . ($tier === 'free' ? ' checked' : '') . '><span class="tier-body"><strong>Free listing</strong>'
    . '<span>Reviewed by our team before it goes live (usually within 1–2 days) · contact details hidden; renters message you via our relay · upgrade any time.</span></span></label>'
    . '</div>' . (stripe_ready() ? '' : '<p class="small muted">Note: card payments are being set up — verified listings will be saved for review until then.</p>') . '</fieldset>';

$crumbs = [['The Sublet', '/'], ['List your place', '/post-a-sublet/']];
ob_start(); ?>
<div class="wrap narrow-lg">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head">
    <h1>List your sublet or short-term rental</h1>
    <p class="lead">Reach renters looking for furnished rooms and apartments for one to twelve months — interns, travel nurses, students and people relocating. It takes about five minutes.</p>
  </header>
  <?= flashes() ?>
  <?php if (isset($err['form'])): ?><div class="flash flash-err"><?= e($err['form']) ?></div><?php unset($err['form']); endif; ?>
  <?= view('listing_form', ['d' => $d, 'err' => $err, 'mode' => 'submit', 'action' => '/post-a-sublet/', 'tierHtml' => $tierHtml, 'submitLabel' => 'Continue']) ?>
  <aside class="note mt"><strong>Before you list:</strong> make sure your lease or landlord allows subletting, and check your city’s short-term-rental rules — many places regulate stays under 30 days. See <a href="/blog/how-to-sublet-your-apartment-legally/">how to sublet legally</a>.</aside>
</div>
<?php
page([
    'title' => 'List Your Sublet — Free or Verified | The Sublet',
    'description' => 'Post your furnished room, apartment or house for 1–12 month stays on The Sublet. Free reviewed listings or ' . price_label() . ' verified ones that go live now.',
    'canonical' => '/post-a-sublet/',
    'body' => ob_get_clean(),
    'h_extra' => leaflet_head(),
    'schema' => [schema_breadcrumbs($crumbs)],
]);
