<?php defined('APP') || exit;

cache_private();
$o = require_owner();
$l = listing_get((int)$params[0]);
if (!$l || (int)$l['owner_id'] !== (int)$o['id']) not_found();
if ($g = form_guard()) { flash($g, 'err'); redirect('/account/'); }
$do = post('do');
switch ($do) {
    case 'rented':
    case 'unavailable':
        if ($l['status'] === 'active') update('listings', ['status' => $do, 'updated_at' => now()], 'id = ?', [(int)$l['id']]);
        flash('Marked as ' . $do . '.');
        break;
    case 'renew':
    case 'activate':
        if ($l['tier'] !== 'paid') { flash('Only verified listings can be re-activated from the dashboard.', 'err'); break; }
        if ($l['available_to'] && $l['available_to'] < date('Y-m-d', time() + 86400)) {
            flash('Update the “available until” date first, then renew.', 'warn');
            redirect('/account/listing/' . $l['id'] . '/');
        }
        update('listings', ['status' => 'active', 'expires_at' => compute_expiry($l['available_to']), 'reminder_sent_at' => null,
            'published_at' => $l['published_at'] ?: now(), 'updated_at' => now()], 'id = ?', [(int)$l['id']]);
        flash('Listing is live until ' . fmt_date(compute_expiry($l['available_to'])) . '.');
        break;
    case 'delete':
        q('DELETE FROM photos WHERE listing_id = ?', [(int)$l['id']]);
        q('DELETE FROM listings WHERE id = ?', [(int)$l['id']]);
        flash('Listing deleted.');
        break;
}
redirect('/account/');
