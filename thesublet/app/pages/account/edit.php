<?php defined('APP') || exit;

cache_private();
$o = require_owner();
$l = listing_get((int)$params[0]);
if (!$l || (int)$l['owner_id'] !== (int)$o['id']) not_found();
$err = [];
$d = $l;
$d['lat'] = $l['lat']; $d['lng'] = $l['lng'];
if (is_post()) {
    if ($g = form_guard()) $err['form'] = $g;
    else {
        $in = $_POST + ['contact_email' => $o['email']];
        $in['contact_email'] = $o['email'];
        [$data, $err] = listing_from_input($in, false, is_directory($l));
        $d = array_merge($d, $_POST);
        if (!$err) {
            $data['slug'] = slugify($data['title'], 60);
            $data['contact_email'] = $o['email'];
            if ($data['_lat'] !== null && (abs($data['_lat'] - (float)$l['lat']) > 0.006 || abs($data['_lng'] - (float)$l['lng']) > 0.007)) {
                resolve_coords($data, (int)$l['id']);
            } else {
                unset($data['_lat'], $data['_lng']);
                if ($l['city_slug'] !== $data['city_slug'] || $l['state'] !== $data['state']) { $data['_lat'] = null; $data['_lng'] = null; resolve_coords($data, (int)$l['id']); }
            }
            $data['updated_at'] = now();
            if ($l['status'] === 'active' && !is_directory($l)) $data['expires_at'] = compute_expiry($data['available_to'], $l['published_at']);
            update('listings', $data, 'id = ?', [(int)$l['id']]);
            foreach ((array)($_POST['delete_photos'] ?? []) as $pid) q('DELETE FROM photos WHERE id = ? AND listing_id = ?', [(int)$pid, (int)$l['id']]);
            [$n, $pe] = photos_save_uploads((int)$l['id']);
            flash('Saved.' . ($n ? " Added $n photo" . ($n > 1 ? 's' : '') . '.' : ''));
            if ($pe) flash(implode(' ', $pe), 'warn');
            redirect('/account/listing/' . $l['id'] . '/');
        }
    }
}
ob_start(); ?>
<div class="wrap narrow-lg section">
  <p><a href="/account/">← Your listings</a></p>
  <h1>Edit listing</h1>
  <p class="muted">Status: <?= e(listing_status_label($l['status'])) ?> · <a href="<?= e(listing_url($l)) ?>">View</a></p>
  <?= flashes() ?>
  <?php if (isset($err['form'])): ?><div class="flash flash-err"><?= e($err['form']) ?></div><?php unset($err['form']); endif; ?>
  <div id="photos"></div>
  <?= view('listing_form', ['d' => $d, 'err' => $err, 'mode' => 'owner', 'action' => '/account/listing/' . $l['id'] . '/', 'photos' => listing_photos((int)$l['id']), 'submitLabel' => 'Save changes']) ?>
</div>
<?php
page(['title' => 'Edit listing | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean(), 'h_extra' => leaflet_head()]);
