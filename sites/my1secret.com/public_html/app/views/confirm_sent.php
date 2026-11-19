<?php defined('M1S') || exit; ?>
<div class="narrow center error-page">
  <p class="error-code">✉</p>
  <h1>Check your email to publish</h1>
  <p class="lede">We sent a confirmation link to <strong><?= e($email) ?></strong>. Click it and your post goes live right away.</p>
  <p class="muted">You only do this once: after confirming, your next posts and comments from this browser publish instantly. The email comes from support@my1secret.com. If you don't see it in a few minutes, check your spam folder.</p>
  <p><a class="btn btn-accent" href="<?= e($back) ?>">Back to the conversation</a> <a class="btn btn-ghost" href="/register/" rel="nofollow">Create an account instead</a></p>
</div>
