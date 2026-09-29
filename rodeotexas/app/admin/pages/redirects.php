<?php
declare(strict_types=1);

use RT\Db;

$error = null;
if (is_post()) {
    if (($_POST['action'] ?? '') === 'delete' && post_int('id')) {
        Db::q('DELETE FROM redirects WHERE id = ?', [post_int('id')]);
        flash('Redirect deleted.');
    } else {
        $from = post_str('from_path', 190);
        $to = post_str('to_path', 500);
        if (!$from || !str_starts_with($from, '/') || !$to || (!str_starts_with($to, '/') && !valid_url($to))) {
            flash('From must start with "/"; To must be a site path or full URL.', 'danger');
        } else {
            Db::q('INSERT INTO redirects (from_path, to_path, code, created_at) VALUES (?, ?, 301, ?) ON DUPLICATE KEY UPDATE to_path = VALUES(to_path)', [$from, $to, now_utc()]);
            flash('Redirect saved.');
        }
    }
    redirect(admin_url('redirects'), 303);
}
$rows = Db::all('SELECT * FROM redirects ORDER BY hits DESC, from_path LIMIT 1000');
admin_header('301 redirects');
?>
<p class="small">Redirects apply only to URLs that no longer exist on the new site (old WordPress URLs, renamed articles and events).</p>
<form method="post" class="card row3">
  <?= RT\Auth::csrfField() ?>
  <?= f_text('from_path', 'From (old path)', '', ['placeholder' => '/old-page/']) ?>
  <?= f_text('to_path', 'To', '', ['placeholder' => '/rodeos/']) ?>
  <div><button class="btn btn--primary" type="submit">Add redirect</button></div>
</form>
<table class="table small"><thead><tr><th>From</th><th>To</th><th>Hits</th><th></th></tr></thead><tbody>
<?php foreach ($rows as $r): ?><tr><td><code><?= e($r['from_path']) ?></code></td><td><code><?= e($r['to_path']) ?></code></td><td><?= (int) $r['hits'] ?></td>
  <td><form method="post" data-confirm="Delete this redirect?"><?= RT\Auth::csrfField() ?><input type="hidden" name="action" value="delete"><input type="hidden" name="id" value="<?= (int) $r['id'] ?>"><button class="linkbtn">Delete</button></form></td></tr><?php endforeach; ?>
</tbody></table>
<?php
admin_footer();
