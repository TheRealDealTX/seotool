<?php defined('SLT') || exit;
page_hero(['title' => 'Contact Spring Landscape Lighting', 'eyebrow' => 'Get in touch', 'sub' => 'Questions about a new system, a repair or an LED upgrade? Call, email or send a message and we will get back to you.', 'crumbs' => [['Home', '/'], ['Contact', null]]]);
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 data-split>We'd love to hear about your property</h2>
      <p style="color:#cfdcd3" data-reveal>Spring Landscape Lighting serves homeowners in Spring, Klein, Champion Forest, Gleannloch Farms, Augusta Pines, The Woodlands and surrounding North Houston communities. The quickest way to reach us is by phone.</p>
      <div class="ccards" data-reveal style="margin:28px 0">
        <a class="ccard" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><span><small>Call</small><strong><?= PHONE ?></strong></span></a>
        <a class="ccard" href="mailto:<?= EMAIL ?>"><?= icon('mail') ?><span><small>Email</small><strong><?= EMAIL ?></strong></span></a>
        <a class="ccard" href="/service-areas/"><?= icon('map-pin') ?><span><small>Service area</small><strong>Spring, TX &amp; North Houston</strong></span></a>
        <a class="ccard" href="/quote/"><?= icon('calendar') ?><span><small>Consultations</small><strong>Request a free lighting plan</strong></span></a>
      </div>
      <div class="pills" data-reveal><?php foreach (AREAS as $k => $a): ?><a class="pill" href="/service-areas/<?= $k ?>/"><?= icon('map-pin') ?><?= e($a['short']) ?></a><?php endforeach; ?></div>
    </div>
    <div class="formcard" data-reveal="right"><h3>Send us a message</h3><?php quote_form('contact'); ?></div>
  </div>
</section>
<section class="sec sec--forest"><div class="wrap" style="max-width:900px"><?php section_head('Before you call', 'Quick answers'); faq_block([
  ['Do you offer free consultations?', 'Yes. Spring Landscape Lighting offers a complimentary consultation to discuss your property and goals before any proposal.'],
  ['Do you repair systems another company installed?', 'Yes. We troubleshoot and repair existing systems, including older halogen installations, and can recommend upgrades where they make sense.'],
  ['Which areas do you serve?', 'Spring, Klein, Champion Forest, Gleannloch Farms, Augusta Pines, The Woodlands and nearby North Houston communities. If you are close by, just ask.'],
], '', false); ?></div></section>
