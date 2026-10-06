<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Free quote · No obligation';
$P['lead'] = 'Tell us about your property and what you would like to see after dark. A Landscape Lighting Texas designer replies within one business day to schedule your free dusk consultation.';
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container grid-2" style="align-items:start">
    <div class="reveal"><?php if (isset($_GET['sent'])) echo callout('<p>Thank you — your request is in. A designer will contact you within one business day.</p>', 'note', 'Request received'); ?><?php quote_form('Request Your Free Quote', 'Quote page'); ?></div>
    <div>
      <?php section_head('What happens next', 'Simple, Transparent and Pressure-Free', '', 'left'); ?>
      <ol class="steps" style="grid-template-columns:1fr;text-align:left">
        <li><h3>We call you back</h3><p>Within one business day, a designer confirms your goals, timing and budget range and books a visit around sunset.</p></li>
        <li><h3>Dusk consultation</h3><p>We walk the property as it gets dark, test fixture positions and talk through ideas — architecture, trees, paths, patios and pools.</p></li>
        <li><h3>Your design &amp; itemized quote</h3><p>You receive a lighting plan with fixture types, quantities, zones, controls and pricing. No surprises, no obligation.</p></li>
      </ol>
      <div class="info-card glow-card reveal" style="margin-top:36px">
        <h3>Prefer to talk now?</h3>
        <p>Call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a> or email <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a>.<br><?= HOURS ?> · Serving all of Texas.</p>
      </div>
      <div class="tool-promo-wrap reveal"><?= tool_promo('/landscape-lighting-cost-calculator/') ?></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <?php stats([['1400', '+', 'Projects completed'], ['1', ' day', 'Typical install time'], ['4.9', '★', 'Average rating'], ['5', '-yr', 'Workmanship warranty']]); ?>
  </div>
</section>
<?php faqs([
    ['Is the consultation really free?', 'Yes. The dusk consultation and your written, itemized quote are free and carry no obligation.'],
    ['Why do you visit at dusk?', 'Light behaves completely differently at night. Seeing your home as it gets dark lets us judge distances, glare, reflections from stone and how far light should reach — things a daytime visit cannot show.'],
    ['How soon can you install?', 'Scheduling depends on the season and project size. Most residential installations take one day once the design is approved; we will give you a date when we send your quote.'],
    ['Do you work with my landscaper, builder or HOA?', 'Yes. We regularly coordinate with landscape designers, pool builders and homebuilders, and we can provide fixture specifications and plans for HOA architectural review.'],
], 'Before You Request a Quote'); ?>
