<?php
require __DIR__ . '/lib.php';
cd_post_only();
if (!cd_rate_limit('subscribe', 5, 3600)) cd_json(['ok' => false, 'error' => 'Too many attempts — please try again later.'], 429);
$email = strtolower(trim(substr($_POST['email'] ?? '', 0, 150)));
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) cd_json(['ok' => false, 'error' => 'Please enter a valid email address.'], 422);
$f = cd_data_dir() . '/subscribers.php';
$existing = is_file($f) ? file_get_contents($f) : '';
if (strpos($existing, ',' . $email . "\n") === false) {
    cd_append_private('subscribers', date('c') . ',' . $email . "\n");
}
cd_json(['ok' => true, 'message' => 'You\'re subscribed — daghang salamat!']);
