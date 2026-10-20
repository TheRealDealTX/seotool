<section class="notfound">
  <div class="wrap wrap--narrow">
    <?php if ($ok): ?>
      <p class="notfound__code" aria-hidden="true"><span><?= icon('mail') ?></span></p>
      <h1>You’re on the list!</h1>
      <p>Thanks for joining the Purely Wholesome Farm letter. Look out for the next one at the start of the month.</p>
    <?php else: ?>
      <h1>That email didn’t look right</h1>
      <p>Please go back and try again with a valid email address.</p>
    <?php endif ?>
    <p class="notfound__links"><a class="btn btn--primary" href="/">Back to the farm</a></p>
  </div>
</section>
