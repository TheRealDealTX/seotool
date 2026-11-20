<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
if (!$l) json_out(['ok' => false, 'error' => 'Listing not found.'], 404);
if ($err = form_guard()) json_out(['ok' => false, 'error' => $err], 400);
if (!rate_limit('report', 5, 3600)) json_out(['ok' => false, 'error' => 'Too many reports. Please try again later.'], 429);
$reasons = ['scam', 'wrong', 'unavailable', 'discrimination', 'illegal', 'other'];
$reason = in_array(post('reason'), $reasons, true) ? post('reason') : 'other';
$email = strtolower(post('email'));
insert('reports', ['listing_id' => (int)$l['id'], 'reason' => $reason, 'details' => mb_substr(post('details'), 0, 2000),
    'reporter_email' => valid_email($email) ? $email : '', 'ip' => client_ip(), 'created_at' => now()]);
notify_admin('Listing reported (' . $reason . '): #' . $l['id'],
    '<p><strong>' . e($l['title']) . '</strong></p><p>Reason: ' . e($reason) . '</p><p>' . nl2br(e(post('details'))) . '</p><p><a href="' . e(base_url('/admin/reports/')) . '">Review reports</a></p>');
json_out(['ok' => true, 'message' => 'Thanks — our team will review this listing.']);
