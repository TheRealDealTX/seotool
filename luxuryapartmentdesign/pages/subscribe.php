<?php
// Newsletter sign-up: appends to a CSV in the private data folder.
$ajax = ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'fetch';
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    redirect('/');
}
$email = trim((string) ($_POST['email'] ?? ''));
$ok = filter_var($email, FILTER_VALIDATE_EMAIL) && empty($_POST['website']);
if ($ok) {
    $line = [date('c'), $email, substr((string) ($_SERVER['HTTP_REFERER'] ?? ''), 0, 200)];
    $fh = fopen(data_dir() . '/subscribers.csv', 'a');
    if ($fh) {
        fputcsv($fh, $line);
        fclose($fh);
    }
}
$msg = $ok ? 'Thank you! You are on the list.' : 'Please enter a valid email address.';
if ($ajax) {
    header('Content-Type: application/json');
    echo json_encode(['ok' => (bool) $ok, 'message' => $msg]);
    exit;
}
page_head(['title' => 'Subscribe', 'description' => $msg, 'path' => '/subscribe/', 'robots' => 'noindex, follow']);
?>
<section class="page-hero"><div class="container container--narrow">
  <h1><?= $ok ? 'You are subscribed' : 'Something went wrong' ?></h1>
  <p class="page-hero__lead"><?= e($msg) ?></p>
  <p><a class="btn btn--gold" href="/">Back to the homepage</a></p>
</div></section>
<?php page_foot(); ?>
