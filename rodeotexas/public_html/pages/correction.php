<?php
/** Report a correction for an event: /rodeos/<slug>/report/ */
defined('RT_APP') || exit;

use RT\Dates;
use RT\EventRepo;
use RT\PublicForm;
use RT\Submissions;

$e = EventRepo::bySlug($slug);
if (!$e) {
    rt_not_found();
}
$fieldsList = [
    'dates' => 'Dates', 'times' => 'Show times', 'venue' => 'Venue or address', 'status' => 'Canceled / postponed',
    'official_url' => 'Official website', 'tickets' => 'Tickets or prices', 'organizer' => 'Organizer', 'other' => 'Something else',
];
$errors = [];
$v = ['field' => '', 'details' => '', 'evidence_url' => '', 'name' => '', 'email' => ''];
$sent = isset($_GET['sent']);
if (is_post()) {
    header('Cache-Control: no-store');
    foreach ($v as $k => $_) {
        $v[$k] = is_string($_POST[$k] ?? null) ? $_POST[$k] : '';
    }
    $check = PublicForm::check('correction', $_POST, 8);
    if ($check === 'spam') {
        redirect('/rodeos/' . $e['slug'] . '/report/?sent=1', 303);
    } elseif ($check !== null) {
        $errors['form'] = $check;
    }
    $field = array_key_exists($v['field'], $fieldsList) ? $v['field'] : null;
    $details = clean_text($v['details'], 2000);
    $evidence = valid_url($v['evidence_url']);
    $email = $v['email'] !== '' ? valid_email($v['email']) : null;
    if (!$field) { $errors['field'] = 'Choose what needs correcting.'; }
    if (!$details || mb_strlen($details) < 5) { $errors['details'] = 'Tell us the correct information.'; }
    if ($v['evidence_url'] !== '' && !$evidence) { $errors['evidence_url'] = 'Enter a full web address starting with https://'; }
    if ($v['email'] !== '' && !$email) { $errors['email'] = 'Enter a valid e-mail or leave it blank.'; }
    if (!$errors) {
        Submissions::store('correction', $e['title'] . ' — ' . $fieldsList[$field], [
            'event' => $e['title'], 'event_url' => abs_url('/rodeos/' . $e['slug'] . '/'), 'field' => $fieldsList[$field],
            'details' => $details, 'evidence_url' => $evidence,
        ], clean_str($v['name'], 120), $email, (int) $e['id']);
        redirect('/rodeos/' . $e['slug'] . '/report/?sent=1', 303);
    }
}
$page = [
    'title' => 'Report a correction — ' . $e['title'],
    'description' => 'Tell us about a change or mistake in the listing for ' . $e['title'] . '.',
    'canonical' => '/rodeos/' . $e['slug'] . '/report/',
    'robots' => 'noindex,follow',
    'body_class' => 'page-form',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
$err = static fn(string $k): string => isset($errors[$k]) ? '<p class="field-error" id="err-' . $k . '">' . e($errors[$k]) . '</p>' : '';
$inv = static fn(string $k): string => isset($errors[$k]) ? ' aria-invalid="true" aria-describedby="err-' . $k . '"' : '';
?>
<div class="wrap narrow">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> <a href="/rodeos/<?= e($e['slug']) ?>/"><?= e($e['title']) ?></a> <span aria-hidden="true">›</span> Report a correction</nav>
  <h1>Report a correction</h1>
  <p class="lead"><strong><?= e($e['title']) ?></strong> · <?= e(Dates::range($e['start_date'], $e['end_date'])) ?> · <?= e(RT\View::place($e)) ?></p>
  <?php if ($sent): ?>
    <div class="alert alert--success" role="status"><strong>Thank you.</strong> An editor will check your report against the official source and update the listing.</div>
    <p><a class="btn" href="/rodeos/<?= e($e['slug']) ?>/">Back to the event</a></p>
  <?php else: ?>
    <?php if ($errors): ?><div class="alert alert--danger" role="alert"><strong>Please fix the highlighted fields.</strong> <?= e($errors['form'] ?? '') ?></div><?php endif; ?>
    <form class="form" method="post" novalidate>
      <?= PublicForm::fields('correction') ?>
      <div class="field"><label for="c-field">What is wrong or missing? <span class="req">*</span></label>
        <select id="c-field" name="field" required<?= $inv('field') ?>><option value="">Choose…</option>
          <?php foreach ($fieldsList as $k => $l): ?><option value="<?= e($k) ?>"<?= $v['field'] === $k ? ' selected' : '' ?>><?= e($l) ?></option><?php endforeach; ?>
        </select><?= $err('field') ?></div>
      <div class="field"><label for="c-details">Correct information <span class="req">*</span></label><textarea id="c-details" name="details" rows="5" required maxlength="2000"<?= $inv('details') ?>><?= e($v['details']) ?></textarea><?= $err('details') ?></div>
      <div class="field"><label for="c-ev">Where can we confirm this? (link)</label><input id="c-ev" type="url" name="evidence_url" maxlength="500" placeholder="https://" value="<?= e($v['evidence_url']) ?>"<?= $inv('evidence_url') ?>><?= $err('evidence_url') ?></div>
      <div class="field-row">
        <div class="field"><label for="c-name">Your name (optional)</label><input id="c-name" name="name" maxlength="120" autocomplete="name" value="<?= e($v['name']) ?>"></div>
        <div class="field"><label for="c-email">Your e-mail (optional)</label><input id="c-email" type="email" name="email" maxlength="255" autocomplete="email" value="<?= e($v['email']) ?>"<?= $inv('email') ?>><?= $err('email') ?></div>
      </div>
      <button class="btn btn--primary" type="submit">Send report</button>
    </form>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
