<?php
declare(strict_types=1);

use RT\Auth;

if (Auth::user()) {
    redirect(admin_url('dashboard'));
}
$error = null;
if (is_post()) {
    Auth::checkCsrf();
    $error = Auth::attempt((string) ($_POST['email'] ?? ''), (string) ($_POST['password'] ?? ''));
    if ($error === null) {
        redirect(admin_url('dashboard'), 303);
    }
}
admin_header('Sign in');
?>
<form method="post" class="card narrow" action="<?= e(admin_url('login')) ?>">
  <?= Auth::csrfField() ?>
  <?php if ($error): ?><div class="alert alert--danger" role="alert"><?= e($error) ?></div><?php endif; ?>
  <?= f_text('email', 'E-mail', $_POST['email'] ?? '', ['type' => 'email', 'required' => true]) ?>
  <?= f_text('password', 'Password', '', ['type' => 'password', 'required' => true]) ?>
  <button class="btn btn--primary" type="submit">Sign in</button>
</form>
<?php
admin_footer();
