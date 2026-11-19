<?php
/** @var bool $ok */
page_start(['title' => 'Thanks for subscribing | Vintique Flea', 'description' => 'Newsletter signup.', 'path' => '/subscribe/', 'robots' => 'noindex, follow']);
?>
<div class="wrap narrow">
  <header class="page-head">
<?php if ($ok): ?>
    <h1>You're on the list! 🎉</h1>
    <p class="lede">We'll email you when the next Vintique Flea dates are announced. While you wait, why not <a href="/play/">play a game</a> or <a href="/shop/">browse curated finds</a>?</p>
<?php else: ?>
    <h1>Hmm, that didn't work</h1>
    <p class="lede">Please go back and check your email address, then try again.</p>
    <?= newsletter_form('retry') ?>
<?php endif; ?>
  </header>
</div>
<?php page_end();
