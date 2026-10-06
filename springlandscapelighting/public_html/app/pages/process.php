<?php defined('SLT') || exit;
add_schema(['@type' => 'HowTo', 'name' => 'How Spring Landscape Lighting designs and installs a landscape lighting system',
  'step' => array_map(fn($p, $i) => ['@type' => 'HowToStep', 'position' => $i + 1, 'name' => $p[0], 'text' => $p[2]], PROCESS, array_keys(PROCESS))]);
page_hero(['title' => 'Our Landscape Lighting Process', 'eyebrow' => 'Simple from start to finish', 'sub' => 'From the first conversation to the final nighttime adjustment, our process keeps the project clear, collaborative and focused on the finished effect.', 'cta' => true, 'crumbs' => [['Home', '/'], ['Our Process', null]]]);
$detail = [
  'We begin by talking through your property, priorities, concerns and budget, and the way you use your outdoor areas in the evening. Bring photos, Pinterest boards or simply a sense of how you want home to feel.',
  'We review architecture, trees, gardens, pathways, patios, driveways, pools, electrical access and important viewing angles: from the street, the front door, the back patio and inside the house. Drainage, irrigation and root zones get noted too.',
  'We choose lighting techniques, fixture locations, beam spreads, brightness levels and color temperature, then organize everything into zones with appropriate controls. Transformer sizing and wire routing are planned for today and for future additions.',
  'You receive a straightforward recommendation based on the planned scope, explained in plain language. Want to phase it? We will show you what to install first and how later layers connect.',
  'Your system is installed with professional low-voltage components and property-conscious methods: wire is buried and concealed, beds and lawns are protected, connections are sealed and the site is left clean.',
  'We return after dark to aim and refine every fixture. Brightness, glare, shadows and viewing angles are reviewed until the whole property feels balanced. Then we walk you through the controls.',
];
?>
<section class="sec">
  <div class="wrap">
    <div class="timeline">
      <div class="timeline__fill"></div>
      <?php foreach (PROCESS as $i => [$t, $ic, $d]): ?>
      <div class="timeline__item" data-reveal>
        <span class="timeline__dot"><?= $i + 1 ?></span>
        <span class="eyebrow">Step <?= $i + 1 ?></span>
        <h3><?= e($t) ?></h3>
        <p><?= e($detail[$i]) ?></p>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap" style="max-width:900px">
    <?php section_head('Process questions', 'What to expect'); faq_block([
      ['How long does a landscape lighting installation take?', 'Many residential projects are installed in one to a few days depending on size, trenching and the number of zones. The nighttime adjustment is scheduled after installation.'],
      ['Do I need to be home for the consultation?', 'It helps to walk the property together so we understand how you use it, but we can also start with a phone call and photos.'],
      ['Can I install the system in phases?', 'Yes. We design the full plan up front and size the transformer and wiring so later phases connect cleanly.'],
      ['Why do you adjust the lights at night?', 'Glare, hot spots, shadows and balance can only be judged in the dark. A few degrees of aim can make the difference between dramatic and distracting.'],
    ], '', false); ?>
  </div>
</section>
<?php cta_band(); ?>
