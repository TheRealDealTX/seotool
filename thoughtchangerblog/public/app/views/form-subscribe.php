<?php $sent = ($_GET['sent'] ?? '') === 'subscribe'; $err = (!str_starts_with(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH), '/contact-us') && isset($_GET['error'])) ? (string) $_GET['error'] : ''; ?>
<form class="subscribe-form js-ajax" method="post" action="/subscribe/" id="subscribe-form">
  <input type="hidden" name="form" value="subscribe">
  <input type="hidden" name="tk" value="<?= e(csrf_token()) ?>">
  <input type="hidden" name="page" value="<?= e(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH)) ?>">
  <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <label class="sr-only" for="nl-email">Email address</label>
  <input id="nl-email" type="email" name="email" required placeholder="Your email address" autocomplete="email">
  <button type="submit" class="btn btn-accent">Subscribe</button>
  <p class="form-status<?= $err ? ' is-error' : '' ?>" role="status" aria-live="polite"><?= $sent ? 'You’re in! Watch your inbox for the next thought.' : e($err) ?></p>
</form>
