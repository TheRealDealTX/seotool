<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
$l = listing_get((int)$params[0]);
if (!$l) not_found();
$err = [];
$d = $l;
if (is_post()) {
    admin_guard_post();
    $do = post('do');
    if ($do === 'save') {
        [$data, $err] = listing_from_input($_POST, !is_directory($l), is_directory($l));
        $d = array_merge($d, $_POST);
        if (!$err) {
            $data['slug'] = slugify($data['title'], 60);
            if ($data['_lat'] !== null) resolve_coords($data, (int)$l['id']); else { unset($data['_lat'], $data['_lng']); $data['lat'] = null; $data['lng'] = null; }
            $data['admin_note'] = mb_substr(post('admin_note'), 0, 2000);
            $tier = post('tier') === 'paid' ? 'paid' : 'free';
            $data['tier'] = $tier;
            $data['updated_at'] = now();
            update('listings', $data, 'id = ?', [(int)$l['id']]);
            foreach ((array)($_POST['delete_photos'] ?? []) as $pid) q('DELETE FROM photos WHERE id = ? AND listing_id = ?', [(int)$pid, (int)$l['id']]);
            [$n, $pe] = photos_save_uploads((int)$l['id']);
            flash('Saved.' . ($n ? " $n photo(s) added." : ''));
            if ($pe) flash(implode(' ', $pe), 'warn');
            redirect('/admin/listing/' . $l['id'] . '/');
        }
    } else {
        admin_listing_action((int)$l['id'], $do, post('reason'));
        flash('Done: ' . $do);
        redirect($do === 'delete' ? '/admin/listings/' : '/admin/listing/' . $l['id'] . '/');
    }
}
$owner = $l['owner_id'] ? row('SELECT * FROM owners WHERE id = ?', [(int)$l['owner_id']]) : null;
$reports = rows('SELECT * FROM reports WHERE listing_id = ? ORDER BY id DESC', [(int)$l['id']]);
$msgs = (int)val('SELECT COUNT(*) FROM messages WHERE listing_id = ?', [(int)$l['id']]);
ob_start(); ?>
<p><a href="/admin/listings/">← All listings</a> · <a href="<?= e(listing_url($l)) ?>" target="_blank">Open public page</a></p>
<div class="admin-meta">
  <p>Status: <span class="status status-<?= e($l['status']) ?>"><?= e(listing_status_label($l['status'])) ?></span> · Tier: <strong><?= e($l['tier']) ?></strong> · Views: <?= (int)$l['views'] ?> · Messages: <?= $msgs ?> · IP: <?= e($l['ip']) ?> · Created <?= e($l['created_at']) ?><?= $l['expires_at'] ? ' · Expires ' . e($l['expires_at']) : '' ?></p>
  <p>Owner: <?= $owner ? e($owner['name'] . ' <' . $owner['email'] . '>') . ($owner['email_verified_at'] ? ' ✔ verified' : ' (email not verified)') : '— (free lister, no account)' ?></p>
  <?php if ($reports): ?><p class="warn-text">⚠ <?= count($reports) ?> report(s): <?= e(implode(', ', array_column($reports, 'reason'))) ?> — <a href="/admin/reports/">view</a></p><?php endif; ?>
  <form method="post" class="admin-actions"><?= csrf_field() ?>
    <button class="btn btn-sm" name="do" value="approve">Approve &amp; publish</button>
    <input type="text" name="reason" placeholder="Reason (emailed on reject)" maxlength="500">
    <button class="btn btn-sm btn-ghost" name="do" value="reject">Reject</button>
    <button class="btn btn-sm btn-ghost" name="do" value="expire">Expire</button>
    <button class="btn btn-sm btn-ghost" name="do" value="rented">Mark rented</button>
    <button class="btn btn-sm btn-danger" name="do" value="delete" data-confirm="Delete this listing and its photos permanently?">Delete</button>
  </form>
</div>
<h2>Edit</h2>
<?php
$extra = '<fieldset><legend>Admin</legend><div class="row3"><label>Tier<select name="tier"><option value="free"' . ($l['tier'] === 'free' ? ' selected' : '') . '>Free</option><option value="paid"' . ($l['tier'] === 'paid' ? ' selected' : '') . '>Paid / verified</option></select></label></div>'
    . '<label>Internal note<textarea name="admin_note" rows="2">' . e($l['admin_note'] ?? '') . '</textarea></label><input type="hidden" name="do" value="save"></fieldset>';
echo str_replace('<div class="form-actions">', $extra . '<div class="form-actions">',
    view('listing_form', ['d' => $d, 'err' => $err, 'mode' => 'admin', 'action' => '/admin/listing/' . $l['id'] . '/', 'photos' => listing_photos((int)$l['id']), 'submitLabel' => 'Save listing']));
admin_page('Listing #' . $l['id'], ob_get_clean());
