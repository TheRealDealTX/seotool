<form class="subscribe" action="/subscribe/" method="post" data-subscribe>
  <label class="sr-only" for="sub-email-<?= $subId = bin2hex(random_bytes(3)) ?>">Email address</label>
  <input id="sub-email-<?= $subId ?>" type="email" name="email" required placeholder="you@example.com" autocomplete="email">
  <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
  <button class="btn btn--peach" type="submit">Subscribe</button>
  <p class="subscribe__msg" role="status" aria-live="polite"></p>
</form>
