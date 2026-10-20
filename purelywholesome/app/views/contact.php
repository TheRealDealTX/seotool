<?php /** @var array $crumbs @var ?bool $sent @var array $errors @var array $old */
$heroTitle = 'Contact Purely Wholesome Farm'; $heroEyebrow = 'We’d love to hear from you';
$heroLede = 'Questions about a recipe, a goat that’s off her feed, a correction, or a success story to share? Send it over. We read every message and do our best to reply promptly.';
include __DIR__ . '/partials/page-hero.php'; ?>
<section class="section section--tight">
  <div class="wrap contact">
    <form class="contact__form" method="post" action="/contact-us/" novalidate>
      <?php if ($sent): ?><p class="alert alert--ok"><?= icon('check') ?> Thank you! Your message is on its way to the farm.</p><?php endif ?>
      <?php if ($errors): ?><p class="alert alert--err">Please fix the highlighted fields.</p><?php endif ?>
      <div class="field <?= isset($errors['name']) ? 'has-error' : '' ?>"><label for="c-name">Name</label><input id="c-name" name="name" required maxlength="80" value="<?= e($old['name']) ?>" autocomplete="name"><?php if (isset($errors['name'])): ?><small><?= e($errors['name']) ?></small><?php endif ?></div>
      <div class="field <?= isset($errors['email']) ? 'has-error' : '' ?>"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required value="<?= e($old['email']) ?>" autocomplete="email"><?php if (isset($errors['email'])): ?><small><?= e($errors['email']) ?></small><?php endif ?></div>
      <div class="field"><label for="c-topic">What’s it about?</label>
        <select id="c-topic" name="topic">
          <?php foreach (['question' => 'A general question', 'recipe' => 'A recipe', 'livestock' => 'Goats or chickens', 'correction' => 'A correction', 'other' => 'Something else'] as $v => $l): ?><option value="<?= $v ?>" <?= $old['topic'] === $v ? 'selected' : '' ?>><?= $l ?></option><?php endforeach ?>
        </select></div>
      <div class="field <?= isset($errors['message']) ? 'has-error' : '' ?>"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required maxlength="5000"><?= e($old['message']) ?></textarea><?php if (isset($errors['message'])): ?><small><?= e($errors['message']) ?></small><?php endif ?></div>
      <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
      <input type="hidden" name="t" value="<?= time() ?>">
      <button class="btn btn--primary btn--lg" type="submit"><?= icon('mail') ?> Send message</button>
    </form>
    <aside class="contact__aside">
      <div class="about__card">
        <h2>Before you write</h2>
        <p>Many questions are answered in the FAQs at the end of each guide. Try a quick search:</p>
        <form class="hero__search hero__search--page" action="/" method="get" role="search"><?= icon('search') ?><input type="search" name="s" placeholder="e.g. brine time" aria-label="Search"></form>
        <p><strong>Email:</strong> <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p>
        <p class="small">Sick animal? Please call your veterinarian first: we can’t diagnose animals over email.</p>
      </div>
    </aside>
  </div>
</section>
