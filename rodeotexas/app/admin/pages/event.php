<?php
declare(strict_types=1);

use RT\Db;
use RT\EventAdmin;

$idParam = (string) ($_GET['id'] ?? 'new');
$id = ctype_digit($idParam) ? (int) $idParam : null;
$ev = $id ? Db::one('SELECT * FROM events WHERE id = ?', [$id]) : null;
if ($id && !$ev) {
    flash('Event not found.', 'danger');
    redirect(admin_url('events'));
}
$errors = [];
$input = null;
if (is_post()) {
    [$savedId, $errors] = EventAdmin::save($id, $_POST, (int) $admin['id']);
    if (!$errors) {
        if (!empty($_POST['from_review']) && ctype_digit((string) $_POST['from_review'])) {
            Db::update('review_items', ['status' => 'approved', 'event_id' => $savedId, 'resolved_at' => now_utc(), 'resolved_by' => (int) $admin['id'],
                'resolution_note' => 'Event created from submission'], 'id = :id AND kind = :k', ['id' => (int) $_POST['from_review'], 'k' => 'submission']);
        }
        flash('Event saved.');
        redirect(admin_url('event', ['id' => $savedId]), 303);
    }
    $input = $_POST;
}
// Prefill (from a submission) or current values
$pre = [];
if (!$ev && isset($_GET['from_review'])) {
    $ri = Db::one("SELECT payload FROM review_items WHERE id = ? AND kind = 'submission'", [(int) $_GET['from_review']]);
    $pl = $ri ? (json_decode((string) $ri['payload'], true) ?: []) : [];
    $pre = [
        'title' => $pl['title'] ?? '', 'start_date' => $pl['start_date'] ?? '', 'end_date' => $pl['end_date'] ?? '',
        'official_url' => $pl['official_url'] ?? '', 'ticket_url' => $pl['ticket_url'] ?? '', 'price_text' => $pl['price'] ?? '',
        'description' => $pl['description'] ?? '', 'level' => $pl['level'] ?? '', 'venue_name' => $pl['venue_name'] ?? '',
        'venue_address' => $pl['address'] ?? '', 'venue_city' => $pl['city'] ?? '', 'venue_zip' => $pl['postal_code'] ?? '',
        'org_name' => $pl['organizer_name'] ?? '', 'source_label' => 'Submitted by the organizer; reviewed by Rodeo Texas',
        'performances_hint' => $pl['times'] ?? '',
    ];
}
$org = $ev && $ev['organizer_id'] ? Db::one('SELECT * FROM organizers WHERE id = ?', [$ev['organizer_id']]) : null;
$val = static function (string $k, $fallback = '') use ($input, $ev, $pre, $org) {
    if ($input !== null) {
        return $input[$k] ?? '';
    }
    if ($ev && array_key_exists($k, $ev)) {
        return $ev[$k];
    }
    if ($org && str_starts_with($k, 'org_')) {
        return $org[substr($k, 4)] ?? '';
    }
    return $pre[$k] ?? $fallback;
};
$locked = $ev ? (json_decode((string) $ev['locked_fields'], true) ?: []) : [];
$venues = options_from("SELECT id, CONCAT(COALESCE(name, '(venue not listed)'), ' — ', COALESCE(city, '?')) AS label FROM venues ORDER BY city, name");
$types = options_from('SELECT id, name AS label FROM event_types ORDER BY sort');
$assocs = options_from("SELECT id, CONCAT(abbr, ' — ', name) AS label FROM associations ORDER BY sort");
$history = $ev ? Db::all('SELECT * FROM event_history WHERE event_id = ? ORDER BY id DESC LIMIT 40', [$ev['id']]) : [];
$sources = $ev ? Db::all('SELECT sr.source_uid, sr.state, sr.last_seen_at, s.name FROM source_records sr JOIN sources s ON s.id = sr.source_id WHERE sr.event_id = ?', [$ev['id']]) : [];
$related = $ev && $ev['group_id'] ? Db::all('SELECT id, title, start_date FROM events WHERE group_id = ? AND id <> ?', [$ev['group_id'], $ev['id']]) : [];
$perfText = $input !== null ? (string) ($input['performances'] ?? '') : ($ev ? EventAdmin::perfsToText((int) $ev['id']) : '');
$err = static fn(string $k): string => isset($errors[$k]) ? '<p class="field-error">' . e($errors[$k]) . '</p>' : '';

admin_header($ev ? 'Edit event' : 'New event');
?>
<?php if ($ev): ?>
  <p><a href="/rodeos/<?= e($ev['slug']) ?>/" target="_blank" rel="noopener">View public page ↗</a> · ID <?= (int) $ev['id'] ?> · <?= status_pill($ev['publish_state']) ?><?= $ev['is_legacy'] ? ' <span class="pill">legacy (archived from old site)</span>' : '' ?></p>
<?php endif; ?>
<?php if ($errors): ?><div class="alert alert--danger" role="alert">Please fix the errors below. <?= e($errors['form'] ?? '') ?></div><?php endif; ?>
<?php if (!empty($pre['performances_hint'])): ?><div class="alert alert--info">Submitted performance times: “<?= e($pre['performances_hint']) ?>” — enter them below in the standard format after checking them.</div><?php endif; ?>

<form method="post" class="form-grid">
  <?= RT\Auth::csrfField() ?>
  <?php if (!$ev && isset($_GET['from_review'])): ?><input type="hidden" name="from_review" value="<?= (int) $_GET['from_review'] ?>"><?php endif; ?>
  <section class="card">
    <h2>Event</h2>
    <?= f_text('title', 'Title', $val('title'), ['required' => true, 'maxlength' => 255]) ?><?= $err('title') ?>
    <?= f_text('slug', 'URL slug', $val('slug'), ['help' => $ev ? 'Changing it adds a 301 redirect from the old URL.' : 'Leave blank to generate from the title and year.']) ?><?= $err('slug') ?>
    <div class="row3">
      <?= f_text('start_date', 'Start date', $val('start_date'), ['type' => 'date', 'required' => true]) ?>
      <?= f_text('end_date', 'End date', $val('end_date'), ['type' => 'date']) ?>
      <?= f_select('publish_state', 'Publishing', $val('publish_state', 'draft'), ['draft' => 'Draft (hidden)', 'published' => 'Published', 'archived' => 'Archived (page kept, noindex)'], false) ?>
    </div>
    <?= $err('start_date') . $err('end_date') ?>
    <?= f_area('performances', 'Performances / show times (venue local time)', $perfText, ['rows' => 4, 'mono' => true, 'help' => 'One per line: 2026-10-03 19:30  or  2026-10-03 7:30pm-9:30pm | Slack. Leave empty if not published.']) ?><?= $err('performances') ?>
    <div class="row3">
      <?= f_select('status', 'Status', $val('status', 'scheduled'), ['scheduled' => 'Scheduled', 'postponed' => 'Postponed', 'canceled' => 'Canceled'], false) ?>
      <?= f_text('status_note', 'Status note (shown publicly)', $val('status_note')) ?>
      <?= f_check('featured', 'Feature on the homepage', (bool) $val('featured', 0)) ?>
    </div>
    <div class="row3">
      <?= f_select('event_type_id', 'Event type', $val('event_type_id'), $types) ?>
      <?= f_select('association_id', 'Association', $val('association_id'), $assocs) ?>
      <?= f_select('level', 'Level', $val('level'), array_combine(levels(), array_map('level_label', levels()))) ?>
    </div>
    <?= f_area('description', 'Description (plain text)', $val('description'), ['rows' => 5]) ?>
  </section>

  <section class="card">
    <h2>Venue</h2>
    <?= f_select('venue_id', 'Existing venue', $val('venue_id'), $venues) ?>
    <p class="small">Or create a new Texas venue (used when no existing venue is selected):</p>
    <div class="row2"><?= f_text('venue_name', 'Venue name', $input['venue_name'] ?? ($pre['venue_name'] ?? '')) ?><?= f_text('venue_address', 'Street address', $input['venue_address'] ?? ($pre['venue_address'] ?? '')) ?></div>
    <div class="row2"><?= f_text('venue_city', 'City', $input['venue_city'] ?? ($pre['venue_city'] ?? '')) ?><?= f_text('venue_zip', 'ZIP', $input['venue_zip'] ?? ($pre['venue_zip'] ?? '')) ?></div>
    <?= $err('venue_city') . $err('venue_zip') ?>
    <?= f_area('parking_info', 'Parking (this event; venue default is used if empty)', $val('parking_info'), ['rows' => 2]) ?>
    <?= f_area('accessibility_info', 'Accessibility (this event)', $val('accessibility_info'), ['rows' => 2]) ?>
  </section>

  <section class="card">
    <h2>Links, tickets &amp; organizer</h2>
    <?= f_text('official_url', 'Official website', $val('official_url'), ['type' => 'url']) ?><?= $err('official_url') ?>
    <?= f_text('ticket_url', 'Ticket link', $val('ticket_url'), ['type' => 'url']) ?><?= $err('ticket_url') ?>
    <?= f_check('ticket_url_verified', 'I checked this ticket link goes to the official seller (only verified links are shown publicly)', (bool) $val('ticket_url_verified', 0)) ?>
    <?= f_text('price_text', 'Prices', $val('price_text'), ['placeholder' => 'e.g. Adults $20, children 3–12 $10']) ?>
    <?= f_text('image_url', 'Image URL (optional)', $val('image_url'), ['type' => 'url']) ?><?= $err('image_url') ?>
    <div class="row2"><?= f_text('org_name', 'Organizer name', $val('org_name')) ?><?= f_text('org_website', 'Organizer website', $val('org_website'), ['type' => 'url']) ?></div>
    <div class="row2"><?= f_text('org_email', 'Organizer public e-mail', $val('org_email'), ['type' => 'email']) ?><?= f_text('org_phone', 'Organizer public phone', $val('org_phone')) ?></div>
  </section>

  <section class="card">
    <h2>Source &amp; grouping</h2>
    <?= f_text('source_label', 'Information source (shown publicly)', $val('source_label'), ['placeholder' => 'e.g. Organizer website']) ?>
    <?= f_text('source_url', 'Source URL', $val('source_url'), ['type' => 'url']) ?><?= $err('source_url') ?>
    <?= f_check('mark_verified', 'I verified these details against the official source today (updates “Last verified”)', false) ?>
    <?= f_text('group_with', 'Group with related event (enter its ID)', '', ['help' => 'Use for separate competitions of the same rodeo, e.g. the breakaway or Xtreme Bulls night.']) ?>
    <?php if ($related): ?><p class="small">Grouped with: <?php foreach ($related as $r): ?><a href="<?= e(admin_url('event', ['id' => $r['id']])) ?>">#<?= (int) $r['id'] ?> <?= e($r['title']) ?> (<?= e($r['start_date']) ?>)</a> <?php endforeach; ?></p><?= f_check('ungroup', 'Remove this event from its group', false) ?><?php endif; ?>
  </section>

  <?php if ($ev): ?>
  <section class="card">
    <h2>Import protection</h2>
    <p class="small">Fields you edit are locked so the weekly import cannot overwrite them; differing imported values appear in the review queue instead. Tick a field to let imports update it again.</p>
    <?php if ($locked): ?>
      <div class="checks"><?php foreach ($locked as $l): ?><label class="check"><input type="checkbox" name="unlock[]" value="<?= e($l) ?>"> unlock <code><?= e($l) ?></code></label><?php endforeach; ?></div>
    <?php else: ?><p class="small">No fields are locked.</p><?php endif; ?>
    <?php if ($sources): ?><p class="small">Linked source records: <?php foreach ($sources as $s): ?><br><?= e($s['name']) ?> · <code><?= e($s['source_uid']) ?></code> · last seen <?= e(fmt_dt($s['last_seen_at'], 'M j, Y')) ?><?php endforeach; ?></p><?php endif; ?>
  </section>
  <?php endif; ?>

  <div class="actions sticky"><button class="btn btn--primary" type="submit">Save event</button> <a class="btn" href="<?= e(admin_url('events')) ?>">Cancel</a></div>
</form>

<?php if ($history): ?>
<section class="card">
  <h2>Change history</h2>
  <table class="table small"><thead><tr><th>When</th><th>Who</th><th>Field</th><th>Old</th><th>New</th></tr></thead><tbody>
  <?php foreach ($history as $h): ?><tr><td class="nowrap"><?= e(fmt_dt($h['created_at'])) ?></td><td><?= e($h['actor']) ?></td><td><?= e($h['field']) ?></td><td><?= e(excerpt($h['old_value'], 80)) ?></td><td><?= e(excerpt($h['new_value'], 80)) ?></td></tr><?php endforeach; ?>
  </tbody></table>
</section>
<?php endif; ?>
<?php
admin_footer();
