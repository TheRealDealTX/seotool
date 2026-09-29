<?php
declare(strict_types=1);

use RT\Db;

if (is_post()) {
    $d = ['abbr' => post_str('abbr', 20), 'name' => post_str('name', 160),
        'level' => in_array($_POST['level'] ?? '', levels(), true) ? $_POST['level'] : 'amateur', 'website' => valid_url($_POST['website'] ?? null)];
    if (!$d['abbr'] || !$d['name']) {
        flash('Abbreviation and name are required.', 'danger');
    } elseif ($id = post_int('id')) {
        Db::update('associations', $d, 'id = :id', ['id' => $id]);
        flash('Association updated.');
    } else {
        $d['slug'] = slugify($d['abbr']);
        if (Db::val('SELECT id FROM associations WHERE slug = ?', [$d['slug']])) {
            flash('That abbreviation already exists.', 'danger');
        } else {
            $d['sort'] = 100;
            Db::insert('associations', $d);
            flash('Association added.');
        }
    }
    redirect(admin_url('associations'), 303);
}
$rows = Db::all('SELECT a.*, (SELECT COUNT(*) FROM events e WHERE e.association_id = a.id) n FROM associations a ORDER BY sort, abbr');
$levels = array_combine(levels(), array_map('level_label', levels()));
admin_header('Associations');
?>
<p class="small">Association labels are shown on events. Only assign an association when the organizer states the sanction.</p>
<?php foreach ($rows as $a): ?>
  <form method="post" class="card row5">
    <?= RT\Auth::csrfField() ?><input type="hidden" name="id" value="<?= (int) $a['id'] ?>">
    <?= f_text('abbr', 'Abbr.', $a['abbr']) ?><?= f_text('name', 'Name', $a['name']) ?><?= f_select('level', 'Level', $a['level'], $levels, false) ?><?= f_text('website', 'Website', $a['website']) ?>
    <div><span class="small"><?= (int) $a['n'] ?> events</span><br><button class="btn" type="submit">Save</button></div>
  </form>
<?php endforeach; ?>
<form method="post" class="card row5">
  <?= RT\Auth::csrfField() ?><?= f_text('abbr', 'Abbr.', '') ?><?= f_text('name', 'Name', '') ?><?= f_select('level', 'Level', 'amateur', $levels, false) ?><?= f_text('website', 'Website', '') ?>
  <div><button class="btn btn--primary" type="submit">Add association</button></div>
</form>
<?php
admin_footer();
