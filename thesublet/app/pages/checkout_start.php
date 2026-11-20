<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
if (!$l) not_found();
if ($g = form_guard()) { flash($g, 'err'); redirect('/'); }
if (!rate_limit('checkout', 10, 3600)) { flash('Too many attempts — please try again later.', 'err'); redirect('/'); }
$owner = current_owner();
session_boot();
$kind = post('kind') === 'new' ? 'new' : 'upgrade';
$allowed = ($owner && (int)$l['owner_id'] === (int)$owner['id'])
    || (($_SESSION['last_submit'] ?? 0) == $l['id'])
    || sign_ok('upgrade:' . $l['id'] . ':' . $l['contact_email'], post('t'));
if (!$allowed) { flash('That upgrade link is not valid.', 'err'); redirect('/'); }
if ($l['tier'] === 'paid') { flash('This listing is already verified.', 'ok'); redirect($owner ? '/account/' : listing_url($l)); }
if (!stripe_ready()) { flash('Card payments are not available yet. Please try again soon.', 'warn'); redirect('/'); }
try {
    redirect(stripe_checkout($l, $kind, $l['contact_email'], $l['contact_name']), 303);
} catch (Throwable $e) {
    error_log('[stripe] ' . $e->getMessage());
    flash('We couldn’t start the payment. Please try again in a moment.', 'err');
    redirect('/');
}
