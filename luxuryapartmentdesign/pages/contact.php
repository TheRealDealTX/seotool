<?php
$path = '/contact/';
$sent = null;
$errors = [];
$vals = ['name' => '', 'email' => '', 'topic' => 'General question', 'message' => ''];
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    foreach ($vals as $k => $_) {
        $vals[$k] = trim((string) ($_POST[$k] ?? ''));
    }
    if ($vals['name'] === '') $errors[] = 'Please tell us your name.';
    if (!filter_var($vals['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
    if (mb_strlen($vals['message']) < 10) $errors[] = 'Please write a short message (10+ characters).';
    $bot = !empty($_POST['website']) || (time() - (int) ($_POST['ts'] ?? 0)) < 3;
    if (!$errors && !$bot) {
        $fh = fopen(data_dir() . '/messages.csv', 'a');
        if ($fh) {
            fputcsv($fh, [date('c'), $vals['name'], $vals['email'], $vals['topic'], $vals['message']]);
            fclose($fh);
        }
        if (CONTACT_EMAIL !== '') {
            require_once dirname(__DIR__) . '/inc/mailer.php';
            $subject = '[' . SITE_NAME . '] ' . $vals['topic'] . ' from ' . $vals['name'];
            $text = $vals['message'] . "\n\n---\nName: " . $vals['name'] . "\nEmail: " . $vals['email'] . "\nTopic: " . $vals['topic'] . "\nSent: " . date('r') . "\n\nReply to this email to answer " . $vals['name'] . '.';
            if (!smtp_send(CONTACT_EMAIL, $subject, $text, $vals['email'])) {
                @mail(CONTACT_EMAIL, $subject, $text, 'From: ' . CONTACT_EMAIL . "\r\nReply-To: " . $vals['email']);
            }
        }
        $sent = true;
    } elseif ($bot && !$errors) {
        $sent = true; // quietly accept bots
    }
}
$crumbs = [['Home', '/'], ['Contact', $path]];
page_head([
    'title' => 'Contact Luxury Apartment Design',
    'description' => 'Contact the Luxury Apartment Design editorial team with a question, a topic suggestion, a correction or a partnership enquiry. We read every message.',
    'path' => $path,
    'schema' => [['@type' => 'ContactPage', '@id' => url($path), 'name' => 'Contact ' . SITE_NAME], schema_breadcrumbs($crumbs)],
]);
?>
<section class="page-hero">
  <div class="container container--narrow">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Contact <?= e(SITE_NAME) ?></h1>
    <p class="page-hero__lead">Have a design question, a topic you would like us to cover, or spotted something we should correct? Send us a note. We read every message and reply to as many as we can.</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <?php if ($sent): ?>
      <div class="notice notice--ok"><p><strong>Thank you, your message is on its way.</strong> We usually reply within a few business days.</p></div>
    <?php else: ?>
      <?php if ($errors): ?><div class="notice notice--err"><ul><?php foreach ($errors as $er) echo '<li>' . e($er) . '</li>'; ?></ul></div><?php endif; ?>
      <form class="form" method="post" action="/contact/">
        <div class="form__row">
          <label>Your name<input type="text" name="name" required value="<?= e($vals['name']) ?>" autocomplete="name"></label>
          <label>Email<input type="email" name="email" required value="<?= e($vals['email']) ?>" autocomplete="email"></label>
        </div>
        <label>Topic
          <select name="topic">
            <?php foreach (['General question', 'Article suggestion', 'Correction', 'Tool feedback', 'Partnership'] as $t): ?>
            <option<?= $vals['topic'] === $t ? ' selected' : '' ?>><?= e($t) ?></option>
            <?php endforeach; ?>
          </select>
        </label>
        <label>Message<textarea name="message" rows="7" required><?= e($vals['message']) ?></textarea></label>
        <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="ts" value="<?= time() ?>">
        <button class="btn btn--gold" type="submit">Send message</button>
      </form>
    <?php endif; ?>
    <div class="prose contact-extra">
      <h2>Before you write</h2>
      <p>Looking for a quick answer? Many common questions are covered by our free tools: the <a href="/tools/rug-size-calculator/">Rug Size Calculator</a>, <a href="/tools/art-hanging-calculator/">Art Hanging Calculator</a> and <a href="/tools/paint-calculator/">Paint Calculator</a> solve the measurements people ask us about most.</p>
      <p>We do not offer paid design consultations, and we never accept payment for editorial coverage. Read our <a href="/editorial-policy/">editorial policy</a> for details.</p>
    </div>
  </div>
</section>
<?php page_foot(); ?>
