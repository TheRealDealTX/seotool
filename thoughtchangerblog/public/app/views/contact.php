<?php
$sent = ($_GET['sent'] ?? '') === 'contact';
$err = isset($_GET['error']) ? (string) $_GET['error'] : '';
view('head', ['meta' => [
    'title' => 'Contact Us - Thought Changer',
    'description' => 'We’d love to hear from you. Thought Changer is built on conversation, curiosity, and connection—use the form below to contact us.',
    'canonical' => '/contact-us/', 'bodyClass' => 'page contact',
    'robots' => ($sent || $err) ? 'noindex, follow' : null,
    'schema' => [['@type' => 'ContactPage', '@id' => SITE_URL . '/contact-us/#webpage', 'url' => SITE_URL . '/contact-us/', 'name' => 'Contact Us - Thought Changer', 'isPartOf' => ['@id' => SITE_URL . '/#website']]],
]]);
?>
<section class="page-hero">
  <div class="wrap-narrow">
    <h1 class="page-title reveal">Contact Us</h1>
    <p class="page-lede reveal">Have a thought you’d like to share, a question that’s been sitting with you, or a reflection sparked by something you read here? We’d love to hear from you. Thought Changer is built on conversation, curiosity, and connection—use the form below to reach out.</p>
  </div>
</section>
<section class="band band-tight">
  <div class="wrap contact-grid">
    <div class="contact-card reveal">
      <h2>Get in touch</h2>
      <p>Email us directly anytime:</p>
      <p><a class="contact-mail" href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p>
      <p>We read every message and usually reply within a few days.</p>
      <ul class="contact-list">
        <li>Reader questions &amp; reflections</li>
        <li>Topic suggestions</li>
        <li>Collaborations &amp; partnerships</li>
      </ul>
    </div>
    <form class="contact-form js-ajax reveal" id="contact" method="post" action="/contact-us/">
      <input type="hidden" name="form" value="contact">
      <input type="hidden" name="tk" value="<?= e(csrf_token()) ?>">
      <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div>
      <div class="field"><label for="c-subject">Subject <span class="opt">(optional)</span></label><input id="c-subject" name="subject"></div>
      <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>
      <button type="submit" class="btn btn-accent">Send</button>
      <p class="form-status<?= $err ? ' is-error' : '' ?>" role="status" aria-live="polite"><?= $sent ? 'Thank you — your message is on its way. We’ll reply soon.' : e($err) ?></p>
    </form>
  </div>
</section>
<?php view('foot'); ?>
