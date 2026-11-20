<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)get('listing'));
session_boot();
$mine = $l && (($_SESSION['last_submit'] ?? 0) == $l['id'] || (current_owner() && (int)$l['owner_id'] === (int)current_owner()['id']));
if ($mine && is_post() && !form_guard()) {
    update('listings', ['status' => 'pending', 'updated_at' => now()], "id = ? AND status = 'pending_payment'", [(int)$l['id']]);
    notify_admin('New listing to review: #' . $l['id'], '<p>' . e($l['title']) . ' (checkout cancelled, saved as free)</p><p><a href="' . e(base_url('/admin/listing/' . $l['id'] . '/')) . '">Review</a></p>');
    redirect('/post-a-sublet/thanks/', 303);
}
ob_start(); ?>
<div class="wrap narrow section center">
  <h1>Payment cancelled</h1>
  <p>No charge was made.</p>
  <?php if ($mine && $l['status'] === 'pending_payment'): ?>
    <p>Your listing “<?= e($l['title']) ?>” is saved. You can try paying again, or submit it as a free listing for review instead.</p>
    <form method="post" action="/checkout/start/<?= (int)$l['id'] ?>/" class="inline"><?= csrf_field() ?><input type="hidden" name="kind" value="new"><button class="btn" type="submit">Try payment again</button></form>
    <form method="post" action="/checkout/cancel/?listing=<?= (int)$l['id'] ?>" class="inline"><?= csrf_field() ?><button class="btn btn-ghost" type="submit">Submit as a free listing</button></form>
  <?php else: ?>
    <p><a class="btn" href="/">Back to The Sublet</a></p>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Payment cancelled | The Sublet', 'robots' => 'noindex', 'body' => ob_get_clean()]);
