<?php
require dirname(__DIR__) . '/inc/config.php';

$page = [
    'title' => 'About Insurance Adjuster Salary',
    'description' => 'Insurance Adjuster Salary publishes independent pay research, calculators and career guides for staff, independent, CAT and public insurance adjusters.',
    'path' => '/about/',
    'image' => 'handshake.webp',
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('About us', 'Clear pay data for people who settle claims', 'We help career changers and working adjusters understand what the job really pays &mdash; and how to earn more of it.', 'handshake.webp', ['About' => null]);
?>
<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Our mission</span>
      <h2>Why this site exists</h2>
      <p>Ask ten adjusters what the job pays and you will hear ten answers. Staff adjusters quote salaries, independents talk about fee bills, CAT adjusters remember their best storm, and public adjusters talk percentages. None of it is wrong &mdash; it just isn't comparable.</p>
      <p>Insurance Adjuster Salary pulls that information into one place. We anchor our numbers to the Bureau of Labor Statistics, translate fee schedules and contingency fees into annual income, and explain the trade-offs behind each path in plain English.</p>
      <p>We also believe getting started should be fast and affordable. That is why we point new adjusters toward online pre-licensing courses that can have them licensed in about a week.</p>
    </div>
    <div class="photo-frame reveal reveal-delay-1"><img src="/assets/img/handshake.webp" alt="Two professionals shaking hands after settling a claim" width="1200" height="800" loading="lazy"></div>
  </div>
</section>
<section class="section section-dark">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">How we work</span><h2>Our editorial standards</h2></div>
    <div class="grid-3">
      <div class="card card-dark reveal"><div class="icon-wrap"><?= icon('book', 24) ?></div><h3>Sourced</h3><p>National pay figures come from the BLS Occupational Outlook Handbook. Role and state ranges are clearly labeled as estimates.</p></div>
      <div class="card card-dark reveal reveal-delay-1"><div class="icon-wrap"><?= icon('shield', 24) ?></div><h3>Independent</h3><p>We are not an insurance carrier or adjusting firm. We may earn a commission from course links, which never changes our pay data.</p></div>
      <div class="card card-dark reveal reveal-delay-2"><div class="icon-wrap"><?= icon('trend', 24) ?></div><h3>Updated</h3><p>We review guides as new wage data, fee schedules and licensing rules are published, and date every update.</p></div>
    </div>
  </div>
</section>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
