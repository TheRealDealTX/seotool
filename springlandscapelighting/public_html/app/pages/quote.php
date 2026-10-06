<?php defined('SLT') || exit;
page_hero(['title' => 'Request a Free Lighting Quote', 'eyebrow' => 'Complimentary consultation', 'sub' => 'Ready to improve how your home looks and feels after sunset? Tell us a little about your property, the areas you want to light and the result you have in mind.', 'crumbs' => [['Home', '/'], ['Request a Quote', null]]]);
$err = isset($_GET['error']);
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap split" style="align-items:start">
    <div class="prose">
      <p class="lead">Spring Landscape Lighting provides custom outdoor lighting design, installation, repair and system upgrades for homes in Spring, Texas and nearby communities.</p>
      <p>Whether you want to highlight your home's architecture, improve pathway visibility, illuminate mature trees or create a more inviting patio or pool area, we will help you plan a system that fits your property, your routines and your budget.</p>
      <p>Complete the form to request a complimentary consultation. Once we receive your details, we will contact you to discuss your goals, answer questions and explain the next steps.</p>
      <h2>What happens next</h2>
      <ol class="steps">
        <li><strong>We call or email you.</strong> A short conversation about your property, priorities and timing.</li>
        <li><strong>We walk the property.</strong> We look at architecture, trees, beds, power, viewing angles and how you use the space.</li>
        <li><strong>You get a clear plan and proposal.</strong> Techniques, fixture locations, zones and controls, explained in plain language.</li>
        <li><strong>We install and fine-tune at night.</strong> Clean installation, then a night-time adjustment so everything looks balanced.</li>
      </ol>
      <div class="callout"><strong>No obligation.</strong> You do not need to know how many fixtures you need. A brief description of your property and what you would like to see is enough to start the conversation.</div>
      <p>Prefer to plan first? Try the <a href="/tools/fixture-estimator/">fixture estimator</a> or the <a href="/tools/lighting-visualizer/">lighting visualizer</a>, then mention your results in the form.</p>
    </div>
    <div class="formcard" data-reveal="right" style="position:sticky;top:96px">
      <h3>Tell us about your project</h3>
      <?php if ($err): ?><div class="qform__status err" style="margin-bottom:14px">Something was missing. Please add your name and a phone number or email and try again.</div><?php endif; ?>
      <?php quote_form('quote'); ?>
    </div>
  </div>
</section>
<section class="sec sec--forest"><div class="wrap"><?php section_head('Our process', 'Simple from start to finish'); process_strip(); ?></div></section>
