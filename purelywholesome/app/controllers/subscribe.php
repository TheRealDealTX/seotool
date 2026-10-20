<?php
// Newsletter sign-up: stores the address and thanks the reader.
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    redirect('/');
}
require ROOT . '/app/mailer.php';
$ok = handle_subscribe(trim((string)($_POST['email'] ?? '')), (string)($_POST['website'] ?? ''));
if (($_SERVER['HTTP_ACCEPT'] ?? '') === 'application/json') {
    header('Content-Type: application/json');
    echo json_encode(['ok' => $ok]);
    exit;
}
render('subscribed', ['ok' => $ok], ['title' => 'Thanks for subscribing | ' . SITE_NAME, 'desc' => '', 'path' => '/subscribe/', 'robots' => 'noindex, follow']);
