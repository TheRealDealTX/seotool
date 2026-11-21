<?php defined('APP') || exit;

cache_private();
$l = listing_get((int)$params[0]);
if (!$l || $l['status'] !== 'active' || is_unclaimed($l) || !valid_email((string)$l['contact_email'])) json_out(['ok' => false, 'error' => 'This listing is no longer accepting messages.'], 404);
if ($err = form_guard()) json_out(['ok' => false, 'error' => $err], 400);
if (!rate_limit('contact', 6, 3600) || !rate_limit('contact-day', 20, 86400)) {
    json_out(['ok' => false, 'error' => 'You’ve sent a lot of messages. Please try again later.'], 429);
}
$name = mb_substr(post('name'), 0, 120);
$email = strtolower(mb_substr(post('email'), 0, 190));
$msg = mb_substr(post('message'), 0, 3000);
if (mb_strlen($name) < 2 || !valid_email($email) || mb_strlen($msg) < 20) {
    json_out(['ok' => false, 'error' => 'Please add your name, a valid email and a message of at least 20 characters.'], 422);
}
if (preg_match_all('#https?://#i', $msg) > 2) json_out(['ok' => false, 'error' => 'Please remove links from your message.'], 422);

$mid = insert('messages', ['listing_id' => (int)$l['id'], 'kind' => 'listing', 'sender_name' => $name, 'sender_email' => $email,
    'body' => $msg, 'ip' => client_ip(), 'created_at' => now()]);
$html = view('emails/relay', ['l' => $l, 'name' => $name, 'email' => $email, 'msg' => $msg]);
$ok = send_mail($l['contact_email'], 'New message about your sublet: ' . $l['title'], $html, $email);
if ($ok) update('messages', ['relayed' => 1], 'id = ?', [$mid]);
json_out(['ok' => true, 'message' => 'Message sent! The host will reply to you by email. Remember: never pay before touring.']);
