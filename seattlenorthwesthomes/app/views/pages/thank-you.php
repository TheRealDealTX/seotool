<?php defined('SNW') || (http_response_code(404) && exit);
$f = $_GET['f'] ?? '';
$msg = [
    'newsletter' => 'You\'re subscribed! Watch your inbox for new listings and Seattle market notes.',
    'sell' => 'Thanks! We\'ll review recent sales near your home and get back to you with next steps, usually within one business day.',
    'buy' => 'Thanks! We\'re putting together homes that match your wish list and will be in touch soon.',
    'showing' => 'Thanks! We\'ll contact you shortly to confirm a time.',
][$f] ?? 'Thanks for reaching out — we\'ll get back to you within one business day.'; ?>
<section class="section center">
  <div class="wrap narrow">
    <p class="eyebrow">Message received</p>
    <h1>Thank You</h1>
    <p class="lead"><?= e($msg) ?></p>
    <p class="cta-actions center"><a class="btn btn-primary" href="/homes-for-sale/">Browse Homes for Sale</a> <a class="btn btn-ghost-dark" href="/blog/">Read the Blog</a></p>
  </div>
</section>
