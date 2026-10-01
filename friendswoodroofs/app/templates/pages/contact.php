<?php partial('page-hero', [
    'eyebrow' => 'Contact us',
    'title'   => 'Contact Friendswood Roofers',
    'lead'    => 'Call us or send an estimate request. Tell us what is going on with your roof and we will follow up to talk it through.',
    'actions' => false,
]); ?>
<section class="section section--first">
  <div class="container estimate-layout">
    <div class="contact-aside">
      <a class="call-panel call-panel--large" href="<?= e(phone_href()) ?>">
        <?= icon('phone') ?>
        <span><span class="call-panel-label">Call Friendswood Roofers</span><span class="call-panel-number"><?= e(phone_display()) ?></span></span>
      </a>

      <div class="side-card">
        <h2 class="h3">How to describe your roofing concern</h2>
        <p>A few details help us understand the problem before we visit:</p>
        <ol class="tips-list">
          <li><strong>What you see.</strong> A stain, drip, missing shingles, debris, granules in gutters or something else.</li>
          <li><strong>Where.</strong> Which room or side of the house, and roughly how big the area is.</li>
          <li><strong>When.</strong> When you first noticed it, and whether it happens in every rain, only heavy rain or after wind.</li>
          <li><strong>Is water coming in now?</strong> Let us know if there is an active leak.</li>
          <li><strong>What you know about the roof.</strong> Approximate age and material, if known. "Not sure" is fine.</li>
        </ol>
        <p class="small">Please do not climb onto your roof to check. Observations from the ground or inside your home are enough. The <a href="/roofing-project-planner/">Roofing Project Planner</a> can help you put this together.</p>
      </div>

      <div class="side-card">
        <h2 class="h3">Service area</h2>
        <p>We serve homeowners in Friendswood, TX. Include your address or ZIP code and we will confirm your home is within our area. <a href="/service-area/">More about our service area</a>.</p>
      </div>
    </div>
    <?php partial('estimate-form', [
        'returnTo' => '/contact/',
        'heading'  => 'Request an Estimate',
        'intro'    => 'Only your name, phone number, property address or ZIP code and the service you need are required. Email is optional.',
    ]); ?>
  </div>
</section>
