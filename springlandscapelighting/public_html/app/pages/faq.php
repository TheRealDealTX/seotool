<?php defined('SLT') || exit;
page_hero(['title' => 'Landscape Lighting FAQ', 'eyebrow' => 'Helpful answers', 'sub' => 'Straight answers to the questions homeowners ask Spring Landscape Lighting most often: cost, design, installation, energy, repairs and maintenance.', 'crumbs' => [['Home', '/'], ['FAQ', null]]]);
$groups = [
 'Cost & planning' => [
  ['How much does landscape lighting cost in Spring, TX?', 'It depends on property size, the number of fixtures and zones, fixture quality, wire runs, controls and installation complexity. Spring Landscape Lighting provides a custom plan and a clear proposal after reviewing your property.'],
  ['Do I need to know how many lights I want?', 'No. Tell us what you want to see and how you use your outdoor spaces. We design the layout and fixture count around that.'],
  ['Can I install landscape lighting in phases?', 'Yes. We plan the whole property, then size the transformer and wiring so you can start with the front elevation and add trees, paths or the backyard later.'],
  ['Do you offer free consultations?', 'Yes. Consultations are complimentary and there is no obligation.'],
 ],
 'Design' => [
  ['What color temperature do you recommend?', 'Most homes look best between 2700K and 3000K: warm enough to flatter brick, stone and wood without looking yellow. Cooler light is used selectively, for example for moonlighting.'],
  ['Will my house look overlit?', 'Not if it is designed well. We use restraint, contrast and careful aiming, and we leave some areas dark so lit features stand out naturally.'],
  ['Can you light large live oaks and tall pines?', 'Yes. Large trees often need several fixtures for uplighting and cross-lighting, and sometimes tree-mounted downlights for a moonlight effect.'],
  ['Will the lights shine into my neighbors\' windows?', 'We aim and shield fixtures to control glare and light trespass, and we review it during the nighttime adjustment.'],
 ],
 'Installation & equipment' => [
  ['Do you use LED low-voltage lighting?', 'Yes. Professional low-voltage LED systems are efficient, long-lasting and offer precise control over brightness, beam spread and color.'],
  ['Will installation damage my landscaping?', 'We use careful methods to minimize disruption: wire is buried and concealed, beds are protected, roots are avoided and the site is left clean.'],
  ['Do I need an electrician?', 'Low-voltage systems typically plug into a dedicated outdoor GFCI outlet. If a new outlet or circuit is needed, that line-voltage work should be done by a licensed electrician.'],
  ['Does my HOA need to approve landscape lighting?', 'Many communities in the Spring and Woodlands area have deed restrictions or architectural review for exterior changes. Check your HOA guidelines; we can provide plan details to support an application.'],
 ],
 'Energy & controls' => [
  ['How much electricity does landscape lighting use?', 'Usually very little. A 20-fixture LED system at 5 watts running six hours a night uses about 18 kWh a month, roughly $3 at $0.16 per kWh. Try our energy cost calculator for your own numbers.'],
  ['Can the lights turn on and off automatically?', 'Yes. Astronomical timers follow sunset all year, photocells respond to darkness, and smart controls add zones, dimming and app control.'],
  ['Can different areas run on different schedules?', 'Yes. Zoning lets architectural lights turn off at midnight while path lights stay on longer, or patio lights run only when you are outside.'],
 ],
 'Repairs & maintenance' => [
  ['Can you repair an existing lighting system?', 'Yes. We troubleshoot dim fixtures, damaged wire, failed transformers, poor placement, outdated lamps and control problems, including systems installed by others.'],
  ['Should I convert my halogen lights to LED?', 'Usually yes. LEDs use roughly 70 to 80 percent less energy and need far fewer lamp changes. We check fixtures, wiring and the transformer to make sure the conversion performs well.'],
  ['How much maintenance does landscape lighting need?', 'Light seasonal care: clean lenses, trim plants, re-aim fixtures that get bumped, check connections and reset timers after outages. See our maintenance checklist for details.'],
  ['Why are some of my lights dimmer than others?', 'Common causes include voltage drop on long runs, loose or corroded connections, failing lamps and dirty lenses. A voltage check usually pinpoints it.'],
 ],
];
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap article">
    <div class="prose"><?php ob_start(); foreach ($groups as $g => $items) faq_block($items, $g); echo with_toc(ob_get_clean())[0]; ?></div>
    <aside class="aside">
      <nav class="toc"><h4>Topics</h4><ol><?php foreach ($groups as $g => $x) echo '<li><a href="#' . trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($g)), '-') . '">' . e($g) . '</a></li>'; ?></ol></nav>
      <div class="side-cta"><span class="eyebrow eyebrow--glow">Still have questions?</span><h4>Ask us directly</h4><p>We are happy to talk through your property.</p><a class="btn btn--glow" href="/contact/">Contact us</a><a class="btn btn--ghost" href="tel:<?= PHONE_TEL ?>"><?= PHONE ?></a></div>
    </aside>
  </div>
</section>
<?php cta_band(); ?>
