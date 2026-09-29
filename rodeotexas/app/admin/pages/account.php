<?php
declare(strict_types=1);

use RT\Auth;
use RT\Db;

if (is_post()) {
    $action = (string) ($_POST['action'] ?? '');
    if ($action === 'password') {
        $row = Db::one('SELECT password_hash FROM admins WHERE id = ?', [$admin['id']]);
        $new = (string) ($_POST['new_password'] ?? '');
        if (!password_verify((string) ($_POST['current_password'] ?? ''), $row['password_hash'])) {
            flash('Current password is incorrect.', 'danger');
        } elseif (strlen($new) < 12 || $new !== (string) ($_POST['new_password2'] ?? '')) {
            flash('New passwords must match and be at least 12 characters.', 'danger');
        } else {
            Db::update('admins', ['password_hash' => password_hash($new, PASSWORD_DEFAULT)], 'id = :id', ['id' => $admin['id']]);
            session_regenerate_id(true);
            flash('Password changed.');
        }
    } elseif ($action === 'add_admin') {
        $email = valid_email($_POST['email'] ?? null);
        $pw = (string) ($_POST['password'] ?? '');
        if (!$email || strlen($pw) < 12) {
            flash('Enter a valid e-mail and a password of at least 12 characters.', 'danger');
        } elseif (Db::val('SELECT id FROM admins WHERE email = ?', [strtolower($email)])) {
            flash('That e-mail already has an account.', 'danger');
        } else {
            Auth::createAdmin($email, post_str('name', 120) ?? 'Administrator', $pw);
            flash('Administrator added. Share the password with them securely.');
        }
    }
    redirect(admin_url('account'), 303);
}
$admins = Db::all('SELECT email, name, created_at, last_login_at FROM admins ORDER BY id');
admin_header('Account');
?>
<div class="grid2">
  <form method="post" class="card">
    <?= Auth::csrfField() ?><input type="hidden" name="action" value="password">
    <h2>Change your password</h2>
    <?= f_text('current_password', 'Current password', '', ['type' => 'password', 'required' => true]) ?>
    <?= f_text('new_password', 'New password (12+ characters)', '', ['type' => 'password', 'required' => true]) ?>
    <?= f_text('new_password2', 'Repeat new password', '', ['type' => 'password', 'required' => true]) ?>
    <button class="btn btn--primary" type="submit">Change password</button>
  </form>
  <form method="post" class="card">
    <?= Auth::csrfField() ?><input type="hidden" name="action" value="add_admin">
    <h2>Add an administrator</h2>
    <?= f_text('name', 'Name', '') ?>
    <?= f_text('email', 'E-mail', '', ['type' => 'email', 'required' => true]) ?>
    <?= f_text('password', 'Temporary password (12+ characters)', '', ['type' => 'password', 'required' => true]) ?>
    <button class="btn" type="submit">Add administrator</button>
  </form>
</div>
<section class="card"><h2>Administrators</h2><table class="table"><thead><tr><th>E-mail</th><th>Name</th><th>Created</th><th>Last login</th></tr></thead><tbody>
<?php foreach ($admins as $a): ?><tr><td><?= e($a['email']) ?></td><td><?= e($a['name']) ?></td><td><?= e(fmt_dt($a['created_at'], 'M j, Y')) ?></td><td><?= e(fmt_dt($a['last_login_at'])) ?></td></tr><?php endforeach; ?>
</tbody></table></section>
<?php
admin_footer();
