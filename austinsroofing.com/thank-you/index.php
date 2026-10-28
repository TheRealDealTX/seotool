<?php
require dirname(__DIR__) . '/includes/layout.php';
page_start([
    'title' => 'Thank You | Austin Roofing',
    'description' => 'Thanks for contacting Austin Roofing. We have your request and will be in touch shortly.',
    'path' => '/thank-you/', 'noindex' => true,
]);
page_hero('Thank You — We Got Your Request', [
    'eyebrow' => 'Austin Roofing',
    'lead' => 'A member of the Austin Roofing team will reach out shortly to schedule your free inspection. If water is coming in right now, call us — we answer 24/7.',
]);
?>
<section class="section section--tight">
  <div class="container">
    <h2 class="section-title">While You Wait, Try Our Free Roofing Tools</h2>
    <?php tool_cards(); ?>
  </div>
</section>
<script>if(window.gtag)gtag('event','generate_lead');</script>
<?php page_end();
