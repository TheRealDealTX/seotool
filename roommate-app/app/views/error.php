<div class="empty-state card narrow">
  <h1><?= e($title ?? 'Something went wrong') ?></h1>
  <p class="muted"><?= e($message ?? '') ?></p>
  <a class="btn btn-primary" href="<?= current_user() ? '/home' : '/' ?>">Go home</a>
</div>
