<?php
/** Public event submission form (held for administrator review). */
defined('RT_APP') || exit;

use RT\EventRepo;
use RT\PublicForm;
use RT\Submissions;

$errors = [];
$v = [];
$sent = isset($_GET['sent']);
$fields = ['title', 'start_date', 'end_date', 'times', 'venue_name', 'address', 'city', 'postal_code', 'official_url', 'ticket_url',
    'organizer_name', 'organizer_contact', 'association', 'event_type', 'level', 'price', 'description', 'name', 'email', 'relationship', 'notes'];

if (is_post()) {
    header('Cache-Control: no-store');
    foreach ($fields as $k) {
        $v[$k] = is_string($_POST[$k] ?? null) ? $_POST[$k] : '';
    }
    $check = PublicForm::check('submit', $_POST, 6);
    if ($check === 'spam') {
        redirect('/submit-event/?sent=1', 303);   // pretend success; store nothing
    } elseif ($check !== null) {
        $errors['form'] = $check;
    }
    $data = [
        'title' => clean_str($v['title'], 200),
        'start_date' => valid_date($v['start_date']),
        'end_date' => valid_date($v['end_date']),
        'times' => clean_str($v['times'], 300),
        'venue_name' => clean_str($v['venue_name'], 200),
        'address' => clean_str($v['address'], 200),
        'city' => clean_str($v['city'], 100),
        'postal_code' => clean_str($v['postal_code'], 10),
        'official_url' => valid_url($v['official_url']),
        'ticket_url' => valid_url($v['ticket_url']),
        'organizer_name' => clean_str($v['organizer_name'], 200),
        'organizer_contact' => clean_str($v['organizer_contact'], 200),
        'association' => clean_str($v['association'], 60),
        'event_type' => clean_str($v['event_type'], 60),
        'level' => in_array($v['level'], levels(), true) ? $v['level'] : null,
        'price' => clean_str($v['price'], 200),
        'description' => clean_text($v['description'], 3000),
        'relationship' => in_array($v['relationship'], ['organizer', 'contestant', 'fan', 'other'], true) ? $v['relationship'] : null,
        'notes' => clean_text($v['notes'], 1000),
    ];
    $name = clean_str($v['name'], 120);
    $email = valid_email($v['email']);
    if (!$data['title']) { $errors['title'] = 'Enter the event name.'; }
    if (!$data['start_date']) { $errors['start_date'] = 'Enter the first day of the event.'; }
    if ($data['start_date'] && $data['start_date'] < date('Y-m-d', strtotime('-1 day'))) { $errors['start_date'] = 'Please submit upcoming events only.'; }
    if ($v['end_date'] !== '' && !$data['end_date']) { $errors['end_date'] = 'Enter a valid date.'; }
    if ($data['end_date'] && $data['start_date'] && $data['end_date'] < $data['start_date']) { $errors['end_date'] = 'The last day cannot be before the first day.'; }
    if (!$data['city']) { $errors['city'] = 'Enter the Texas city or town where it takes place.'; }
    if ($data['postal_code'] && !RT\Geo::isTexasZip($data['postal_code'])) { $errors['postal_code'] = 'That is not a Texas ZIP code. We only list events held in Texas.'; }
    if ($v['official_url'] !== '' && !$data['official_url']) { $errors['official_url'] = 'Enter a full web address starting with https://'; }
    if ($v['ticket_url'] !== '' && !$data['ticket_url']) { $errors['ticket_url'] = 'Enter a full web address starting with https://'; }
    if (!$email) { $errors['email'] = 'Enter your e-mail so we can ask questions about the listing.'; }
    if (empty($_POST['confirm_texas'])) { $errors['confirm_texas'] = 'Please confirm the event takes place in Texas.'; }

    if (!$errors) {
        Submissions::store('submission', $data['title'] . ' — ' . $data['start_date'] . ' — ' . $data['city'], $data, $name, $email);
        redirect('/submit-event/?sent=1', 303);
    }
}

$page = [
    'title' => 'Submit a Texas Rodeo',
    'description' => 'Organizers and fans can submit Texas rodeos and related competitions. Every listing is reviewed before it is published.',
    'canonical' => '/submit-event/',
    'body_class' => 'page-form',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
$err = static fn(string $k): string => isset($errors[$k]) ? '<p class="field-error" id="err-' . $k . '">' . e($errors[$k]) . '</p>' : '';
$inv = static fn(string $k): string => isset($errors[$k]) ? ' aria-invalid="true" aria-describedby="err-' . $k . '"' : '';
?>
<div class="wrap narrow">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> Submit an event</nav>
  <h1>Submit a Texas rodeo</h1>
  <?php if ($sent): ?>
    <div class="alert alert--success" role="status"><strong>Thank you!</strong> Your event was received. A person reviews every submission before it appears on the site — usually within a few days.</div>
    <p><a class="btn" href="/rodeos/">Browse rodeos</a> <a class="btn btn--ghost" href="/submit-event/">Submit another event</a></p>
  <?php else: ?>
    <p>Know of a rodeo, ranch rodeo, youth or high school rodeo, bull riding or roping held in Texas? Tell us about it. We verify details with the official source before publishing.</p>
    <?php if ($errors): ?><div class="alert alert--danger" role="alert"><strong>Please fix the highlighted fields.</strong> <?= e($errors['form'] ?? '') ?></div><?php endif; ?>
    <form class="form" method="post" action="/submit-event/" novalidate>
      <?= PublicForm::fields('submit') ?>
      <fieldset><legend>Event</legend>
        <div class="field"><label for="s-title">Event name <span class="req">*</span></label><input id="s-title" name="title" required maxlength="200" value="<?= e($v['title'] ?? '') ?>"<?= $inv('title') ?>><?= $err('title') ?></div>
        <div class="field-row">
          <div class="field"><label for="s-start">First day <span class="req">*</span></label><input id="s-start" type="date" name="start_date" required value="<?= e($v['start_date'] ?? '') ?>"<?= $inv('start_date') ?>><?= $err('start_date') ?></div>
          <div class="field"><label for="s-end">Last day</label><input id="s-end" type="date" name="end_date" value="<?= e($v['end_date'] ?? '') ?>"<?= $inv('end_date') ?>><?= $err('end_date') ?></div>
        </div>
        <div class="field"><label for="s-times">Performance times</label><input id="s-times" name="times" maxlength="300" placeholder="e.g. Fri & Sat 7:30 PM, Sun 2 PM" value="<?= e($v['times'] ?? '') ?>"></div>
        <div class="field-row">
          <div class="field"><label for="s-assoc">Association / sanction</label><input id="s-assoc" name="association" maxlength="60" list="assoc-list" placeholder="PRCA, UPRA, THSRA…" value="<?= e($v['association'] ?? '') ?>">
            <datalist id="assoc-list"><?php foreach (EventRepo::associations() as $a): ?><option value="<?= e($a['abbr']) ?>"><?= e($a['name']) ?></option><?php endforeach; ?></datalist></div>
          <div class="field"><label for="s-type">Event type</label><select id="s-type" name="event_type"><option value="">Choose…</option><?php foreach (EventRepo::types() as $t): ?><option<?= ($v['event_type'] ?? '') === $t['name'] ? ' selected' : '' ?>><?= e($t['name']) ?></option><?php endforeach; ?></select></div>
          <div class="field"><label for="s-level">Level</label><select id="s-level" name="level"><option value="">Choose…</option><?php foreach (levels() as $l): ?><option value="<?= e($l) ?>"<?= ($v['level'] ?? '') === $l ? ' selected' : '' ?>><?= e(level_label($l)) ?></option><?php endforeach; ?></select></div>
        </div>
        <div class="field"><label for="s-desc">Description</label><textarea id="s-desc" name="description" rows="4" maxlength="3000"><?= e($v['description'] ?? '') ?></textarea></div>
      </fieldset>
      <fieldset><legend>Location (Texas only)</legend>
        <div class="field"><label for="s-venue">Venue / arena</label><input id="s-venue" name="venue_name" maxlength="200" value="<?= e($v['venue_name'] ?? '') ?>"></div>
        <div class="field"><label for="s-addr">Street address</label><input id="s-addr" name="address" maxlength="200" autocomplete="street-address" value="<?= e($v['address'] ?? '') ?>"></div>
        <div class="field-row">
          <div class="field"><label for="s-city">City or town <span class="req">*</span></label><input id="s-city" name="city" required maxlength="100" value="<?= e($v['city'] ?? '') ?>"<?= $inv('city') ?>><?= $err('city') ?></div>
          <div class="field"><label for="s-zip">ZIP code</label><input id="s-zip" name="postal_code" inputmode="numeric" maxlength="10" value="<?= e($v['postal_code'] ?? '') ?>"<?= $inv('postal_code') ?>><?= $err('postal_code') ?></div>
        </div>
        <div class="check"><input id="s-tx" type="checkbox" name="confirm_texas" value="1"<?= !empty($_POST['confirm_texas']) ? ' checked' : '' ?><?= $inv('confirm_texas') ?>><label for="s-tx">This event takes place in Texas <span class="req">*</span></label><?= $err('confirm_texas') ?></div>
      </fieldset>
      <fieldset><legend>Links &amp; tickets</legend>
        <div class="field"><label for="s-web">Official website or event page</label><input id="s-web" type="url" name="official_url" maxlength="500" placeholder="https://" value="<?= e($v['official_url'] ?? '') ?>"<?= $inv('official_url') ?>><?= $err('official_url') ?></div>
        <div class="field"><label for="s-tix">Official ticket link</label><input id="s-tix" type="url" name="ticket_url" maxlength="500" placeholder="https://" value="<?= e($v['ticket_url'] ?? '') ?>"<?= $inv('ticket_url') ?>><?= $err('ticket_url') ?></div>
        <div class="field"><label for="s-price">Admission prices</label><input id="s-price" name="price" maxlength="200" placeholder="e.g. Adults $15, kids 6–12 $5" value="<?= e($v['price'] ?? '') ?>"></div>
        <div class="field-row">
          <div class="field"><label for="s-org">Organizer</label><input id="s-org" name="organizer_name" maxlength="200" value="<?= e($v['organizer_name'] ?? '') ?>"></div>
          <div class="field"><label for="s-orgc">Organizer public phone or e-mail</label><input id="s-orgc" name="organizer_contact" maxlength="200" value="<?= e($v['organizer_contact'] ?? '') ?>"></div>
        </div>
      </fieldset>
      <fieldset><legend>About you</legend>
        <div class="field-row">
          <div class="field"><label for="s-name">Your name</label><input id="s-name" name="name" maxlength="120" autocomplete="name" value="<?= e($v['name'] ?? '') ?>"></div>
          <div class="field"><label for="s-email">Your e-mail <span class="req">*</span></label><input id="s-email" type="email" name="email" required maxlength="255" autocomplete="email" value="<?= e($v['email'] ?? '') ?>"<?= $inv('email') ?>><?= $err('email') ?></div>
        </div>
        <div class="field"><label for="s-rel">You are…</label><select id="s-rel" name="relationship"><option value="">Choose…</option><?php foreach (['organizer' => 'The organizer', 'contestant' => 'A contestant', 'fan' => 'A fan', 'other' => 'Other'] as $k => $l): ?><option value="<?= e($k) ?>"<?= ($v['relationship'] ?? '') === $k ? ' selected' : '' ?>><?= e($l) ?></option><?php endforeach; ?></select></div>
        <div class="field"><label for="s-notes">Notes for our editors</label><textarea id="s-notes" name="notes" rows="3" maxlength="1000"><?= e($v['notes'] ?? '') ?></textarea></div>
        <p class="fineprint">Your e-mail is used only to ask about this listing. It is never published. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </fieldset>
      <button class="btn btn--primary btn--lg" type="submit">Send for review</button>
    </form>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
