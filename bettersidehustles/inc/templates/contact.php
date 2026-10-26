<?php
// Contact page with a small mail() handler: honeypot, time trap, per-IP rate limit.
$status = null;
$old = ['first' => '', 'last' => '', 'email' => '', 'topic' => '', 'message' => ''];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    foreach ($old as $k => $_) {
        $old[$k] = trim((string) ($_POST[$k] ?? ''));
    }
    $tooFast = (time() - (int) ($_POST['t'] ?? 0)) < 3;
    $rateFile = sys_get_temp_dir() . '/bsh-contact-' . md5($_SERVER['REMOTE_ADDR'] ?? '');
    $limited = is_file($rateFile) && filemtime($rateFile) > time() - 60;
    if (!empty($_POST['website']) || $tooFast) {
        $status = 'ok'; // silently drop bots
    } elseif ($limited) {
        $status = 'Please wait a minute before sending another message.';
    } elseif ($old['first'] === '' || !filter_var($old['email'], FILTER_VALIDATE_EMAIL) || mb_strlen($old['message']) < 10) {
        $status = 'Please add your name, a valid email and a short message.';
    } else {
        $clean = fn($s) => str_replace(["\r", "\n"], ' ', $s);
        $body = "Name: {$old['first']} {$old['last']}\nEmail: {$old['email']}\nInterested in: {$old['topic']}\n\n{$old['message']}\n";
        $headers = 'From: ' . SITE_NAME . ' <' . CONTACT_FROM . ">\r\nReply-To: " . $clean($old['email']) . "\r\nContent-Type: text/plain; charset=utf-8";
        $sent = @mail(CONTACT_TO, '=?UTF-8?B?' . base64_encode('Contact form: ' . $clean($old['first'] . ' ' . $old['last'])) . '?=', $body, $headers);
        @touch($rateFile);
        $status = $sent ? 'ok' : 'Sorry — the message could not be sent. Please try again later.';
        if ($sent) {
            $old = array_map(fn() => '', $old);
        }
    }
}
$meta = [
    'title' => 'Contact Better Side Hustles',
    'description' => 'Contact the Better Side Hustles team with questions about side hustles, guide suggestions or partnership enquiries. We read every message.',
    'url' => '/contact/',
    'schema' => [
        ['@type' => 'ContactPage', 'name' => 'Contact ' . SITE_NAME, 'url' => SITE_URL . '/contact/'],
        schema_breadcrumbs([['Home', '/'], ['Contact', '/contact/']]),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.3" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Contact</nav>
    <span class="pill">Start the grind with us</span>
    <h1>Contact Better Side Hustles</h1>
    <p class="dek">Questions about a side hustle, a guide you'd like us to write or a partnership idea? Send us a message.</p>
  </div>
</section>
<div class="wrap contact-grid">
  <div class="article-body">
    <h2 id="how-we-help">How we can help</h2>
    <p>Better Side Hustles exists to help you earn more on your own terms, whether that means an extra $300 a month, paying off debt faster or building toward financial independence and early retirement.</p>
    <ul class="checks">
      <li><?= icon('check') ?><span><strong>Guide requests:</strong> don't see your city or platform? Tell us and we'll add it to the list.</span></li>
      <li><?= icon('check') ?><span><strong>Corrections:</strong> spotted an outdated fee or pay rate? We update guides quickly.</span></li>
      <li><?= icon('check') ?><span><strong>Partnerships:</strong> brands and platforms that genuinely help side hustlers.</span></li>
    </ul>
    <div class="callout"><strong>While you wait:</strong> try the <a href="/tools/side-hustle-quiz/">side hustle quiz</a>. It answers the most common question we get: "which side hustle should I start?"</div>
  </div>
  <form class="form" method="post" action="/contact/">
    <?php if ($status === 'ok'): ?><p class="notice notice-ok">Thanks! Your message is on its way. We usually reply within two business days.</p>
    <?php elseif ($status): ?><p class="notice notice-err"><?= e($status) ?></p><?php endif; ?>
    <div class="row2">
      <label>First name<input name="first" required autocomplete="given-name" value="<?= e($old['first']) ?>"></label>
      <label>Last name<input name="last" autocomplete="family-name" value="<?= e($old['last']) ?>"></label>
    </div>
    <label>Email<input type="email" name="email" required autocomplete="email" value="<?= e($old['email']) ?>"></label>
    <label>What would you like to do?
      <select name="topic">
        <?php foreach (['Freelancing', 'Transportation', 'Courses', 'Selling Products', 'Other'] as $t): ?>
        <option<?= $old['topic'] === $t ? ' selected' : '' ?>><?= e($t) ?></option>
        <?php endforeach; ?>
      </select>
    </label>
    <label>Message<textarea name="message" rows="6" required minlength="10"><?= e($old['message']) ?></textarea></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <input type="hidden" name="t" value="<?= time() ?>">
    <button class="btn btn-lg" type="submit"><?= icon('mail') ?>Send message</button>
  </form>
</div>
<?php require __DIR__ . '/footer.php'; ?>
