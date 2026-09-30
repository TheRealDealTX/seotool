<?php
declare(strict_types=1);

use RT\Auth;
use RT\Db;

$newToken = null;
if (is_post() && ($_POST['action'] ?? '') === 'gen_token') {
    $newToken = RT\RemoteImport::generateToken();   // shown once below, never stored in plain text
} elseif (is_post() && ($_POST['action'] ?? '') === 'revoke_token') {
    RT\RemoteImport::revokeToken();
    flash('Import token revoked. The external routine can no longer send events until you create a new one.');
    redirect(admin_url('account'), 303);
} elseif (is_post()) {
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
<section class="card">
  <h2>External weekly import routine</h2>
  <p class="small">The weekly routine runs outside this server, fetches the permitted event sources and researches official organizer
    sites, then sends the records to <code><?= e(abs_url('/api/import/')) ?></code>. It needs this token. Only a hash is stored here.</p>
  <?php if ($newToken): ?>
    <div class="alert alert--warning"><strong>Copy this token now — it will not be shown again.</strong><br>
      Put it in the Claude Code cloud environment settings as the environment variable <code>RODEOTEXAS_IMPORT_TOKEN</code>
      (environment menu → Edit → Environment variables). Do not e-mail it or paste it into chats.
      <pre class="mono"><?= e($newToken) ?></pre></div>
  <?php endif; ?>
  <p>Status: <?= RT\RemoteImport::tokenCreatedAt() ? 'token active since ' . e(fmt_dt(RT\RemoteImport::tokenCreatedAt())) : '<strong>no token</strong> (the routine cannot send events)' ?></p>
  <form method="post" class="inline" data-confirm="Create a new token? Any previous token stops working immediately."><?= Auth::csrfField() ?><input type="hidden" name="action" value="gen_token"><button class="btn btn--primary" type="submit"><?= RT\RemoteImport::tokenCreatedAt() ? 'Replace token' : 'Create token' ?></button></form>
  <?php if (RT\RemoteImport::tokenCreatedAt()): ?>
  <form method="post" class="inline" data-confirm="Revoke the token? The routine will stop importing."><?= Auth::csrfField() ?><input type="hidden" name="action" value="revoke_token"><button class="btn" type="submit">Revoke</button></form>
  <?php endif; ?>
</section>
<section class="card"><h2>Administrators</h2><table class="table"><thead><tr><th>E-mail</th><th>Name</th><th>Created</th><th>Last login</th></tr></thead><tbody>
<?php foreach ($admins as $a): ?><tr><td><?= e($a['email']) ?></td><td><?= e($a['name']) ?></td><td><?= e(fmt_dt($a['created_at'], 'M j, Y')) ?></td><td><?= e(fmt_dt($a['last_login_at'])) ?></td></tr><?php endforeach; ?>
</tbody></table></section>
<?php
admin_footer();
