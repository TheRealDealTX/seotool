<?php
declare(strict_types=1);

use RT\Db;
use RT\Geo;

$id = (int) ($_GET['id'] ?? 0);
$v = Db::one('SELECT * FROM venues WHERE id = ?', [$id]);
if (!$v) {
    redirect(admin_url('venues'));
}
$errors = [];
if (is_post()) {
    $d = [
        'name' => post_str('name'), 'address' => post_str('address'), 'city' => post_str('city', 120),
        'county' => post_str('county', 120), 'postal_code' => post_str('postal_code', 10),
        'timezone' => in_array($_POST['timezone'] ?? '', ['America/Chicago', 'America/Denver'], true) ? $_POST['timezone'] : 'America/Chicago',
        'region_id' => post_int('region_id'),
        'parking_info' => clean_text($_POST['parking_info'] ?? null, 2000),
        'accessibility_info' => clean_text($_POST['accessibility_info'] ?? null, 2000),
    ];
    $lat = trim((string) ($_POST['lat'] ?? '')); $lng = trim((string) ($_POST['lng'] ?? ''));
    if ($lat !== '' || $lng !== '') {
        if (!is_numeric($lat) || !is_numeric($lng) || !Geo::inTexasBox((float) $lat, (float) $lng)) {
            $errors['lat'] = 'Coordinates must be inside Texas (e.g. 32.7410, -97.3685).';
        } else {
            $d['lat'] = round((float) $lat, 6); $d['lng'] = round((float) $lng, 6); $d['location_precision'] = 'address';
        }
    }
    if (!$d['city']) { $errors['city'] = 'City is required.'; }
    if ($d['postal_code'] && !Geo::isTexasZip($d['postal_code'])) { $errors['postal_code'] = 'Not a Texas ZIP code.'; }
    if (!empty($_POST['regeocode']) && !$errors) {
        Geo::$budget = 2;
        $g = Geo::geocode(implode(', ', array_filter([$d['name'], $d['address'], $d['city'], 'TX', $d['postal_code']])));
        if ($g && $g['state'] === 'TX') {
            $d += ['lat' => $g['lat'], 'lng' => $g['lng'], 'location_precision' => $g['precision']];
            $d['county'] = $d['county'] ?: $g['county'];
            flash('Location found by OpenStreetMap — check the map pin on the event page.');
        } else {
            flash('OpenStreetMap could not find that address. Enter coordinates by hand.', 'warning');
        }
    }
    if (!$errors) {
        $d['manually_edited'] = 1;
        $d['updated_at'] = now_utc();
        Db::tx(function () use ($d, $id) {
            Db::update('venues', $d, 'id = :id', ['id' => $id]);
            Db::q('UPDATE events SET timezone = ? WHERE venue_id = ?', [$d['timezone'], $id]);
        });
        flash('Venue saved. It is now protected from automatic updates.');
        redirect(admin_url('venue', ['id' => $id]), 303);
    }
    $v = array_merge($v, $_POST);
}
$regions = options_from('SELECT id, name AS label FROM regions ORDER BY sort');
admin_header('Venue');
?>
<form method="post" class="card">
  <?= RT\Auth::csrfField() ?>
  <div class="row2"><?= f_text('name', 'Name', $v['name']) ?><?= f_text('address', 'Street address', $v['address']) ?></div>
  <div class="row3"><?= f_text('city', 'City', $v['city'], ['required' => true]) ?><?= f_text('county', 'County', $v['county']) ?><?= f_text('postal_code', 'ZIP', $v['postal_code']) ?></div>
  <?= isset($errors['city']) ? '<p class="field-error">' . e($errors['city']) . '</p>' : '' ?><?= isset($errors['postal_code']) ? '<p class="field-error">' . e($errors['postal_code']) . '</p>' : '' ?>
  <div class="row3"><?= f_text('lat', 'Latitude', $v['lat']) ?><?= f_text('lng', 'Longitude', $v['lng']) ?><?= f_check('regeocode', 'Look up coordinates from the address (OpenStreetMap)', false) ?></div>
  <?= isset($errors['lat']) ? '<p class="field-error">' . e($errors['lat']) . '</p>' : '' ?>
  <p class="small">Map precision: <?= e($v['location_precision']) ?>.</p>
  <div class="row2"><?= f_select('timezone', 'Time zone', $v['timezone'], ['America/Chicago' => 'Central (most of Texas)', 'America/Denver' => 'Mountain (El Paso & Hudspeth counties)'], false) ?><?= f_select('region_id', 'Region', $v['region_id'], $regions) ?></div>
  <?= f_area('parking_info', 'Parking (default for events here)', $v['parking_info'], ['rows' => 3]) ?>
  <?= f_area('accessibility_info', 'Accessibility (default for events here)', $v['accessibility_info'], ['rows' => 3]) ?>
  <button class="btn btn--primary" type="submit">Save venue</button>
</form>
<?php
admin_footer();
