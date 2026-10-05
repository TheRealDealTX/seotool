<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$svcs = services();
$areasAll = areas();
$postsAll = array_slice(array_values(posts()), 0, 3);
$faqs = array_slice(site_faqs(), 0, 6);

$page = [
    'title' => 'Austin Landscape Lighting | Outdoor Lighting Design & Installation in Austin, TX',
    'title_raw' => true,
    'description' => 'Austin Landscape Lighting designs and installs low-voltage LED outdoor lighting for Austin homes and businesses. Free dusk consultations and a 2-year warranty.',
    'path' => '/',
    'active' => '/',
    'body_class' => 'is-home',
    'tools_js' => true,
    'schema' => [
        schema_webpage(['title' => 'Austin Landscape Lighting', 'description' => 'Austin Landscape Lighting: outdoor lighting design and installation in Austin, TX.', 'path' => '/']),
        schema_faq($faqs),
    ],
];

$techniques = [
    ['uplight', 'Architectural uplighting', 'Grazing light up limestone and columns', 'uplight window porch', 'Fixtures at the base of the wall rake light upward so every ledge and mortar line casts a shadow. This is the technique that makes an Austin stone facade look carved after dark.'],
    ['path', 'Path & step lighting', 'Pools of light every 6 to 8 feet', 'path steps window porch', 'Shielded path lights throw light down, never out. Staggered along the walk, they guide guests to the door without a runway look. Step lights hide in risers and walls.'],
    ['moon', 'Moonlighting', 'Downlights hidden in the canopy', 'moon treeup window', 'A fixture mounted 20 to 30 feet up in a live oak casts dappled shadows across the lawn exactly like a full moon. Our most requested technique in Rollingwood and Westlake.'],
    ['tree', 'Tree uplighting', 'Narrow beams up the trunk', 'treeup window porch', 'Two fixtures per large tree, aimed up the trunk into the canopy, turn an oak into a sculpture. We cross-light so no single side goes flat.'],
    ['sparkle', 'The full composition', 'All layers, balanced at night', 'uplight path moon treeup steps window porch stars', 'Each layer is aimed and dimmed after dark so the facade, trees, paths and interior glow read as one scene. Shielded 2700K fixtures keep the Hill Country sky dark.'],
];

ob_start(); ?>
<section class="hero spotlight" data-spotlight>
  <div class="hero__bg">
    <?= picture('austin-landscape-lighting-1', 'Austin home illuminated at night by Austin Landscape Lighting', ['eager' => true, 'class' => 'hero__photo', 'sizes' => '100vw']) ?>
    <canvas data-hero-canvas aria-hidden="true"></canvas>
  </div>
  <div class="container hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Austin, Texas · Est. 2020 · 4.9★ on Google</p>
      <h1 class="display">Austin Landscape Lighting that makes your home <em>glow after dark</em>.</h1>
      <p class="lede">Austin Landscape Lighting designs, installs and maintains low-voltage LED outdoor lighting for homes and businesses across Austin and the Hill Country. Brass fixtures, night-aimed designs, one-day installs and a two-year workmanship warranty.</p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="/contact/">Get a Free Design Consultation <?= icon('arrow') ?></a>
        <a class="btn btn--ghost btn--lg" href="<?= BIZ['phone_href'] ?>"><?= icon('phone') ?> <?= e(BIZ['phone_display']) ?></a>
      </div>
      <ul class="hero__trust">
        <li><?= icon('shield') ?> Licensed &amp; insured</li>
        <li><?= icon('warranty') ?> 2-year workmanship warranty</li>
        <li><?= icon('bulb') ?> LED, 2700K warm white</li>
        <li><?= icon('clock') ?> Most installs in one day</li>
      </ul>
    </div>
    <div class="hero__scene" data-reveal="scale">
      <?= str_replace('<svg class="scene"', '<svg class="scene" data-hero-scene', visualizer_scene('hero')) ?>
      <button class="hero__switch" type="button" data-hero-switch><?= icon('switch') ?><span>Flip the switch</span></button>
    </div>
  </div>
  <div class="hero__scroll">Scroll</div>
</section>

<section class="section--tight stats-band">
  <div class="container"><?= stats_row() ?></div>
</section>

<?= area_marquee() ?>

<section class="section" id="services">
  <div class="container">
    <?= section_head('What we do', 'Outdoor lighting for every corner of your property', 'From a subtle path to a dramatic facade, Austin Landscape Lighting designs each system around your architecture and landscape. Twelve services, one cohesive glow.') ?>
    <div class="grid grid--4">
      <?php foreach (array_values($svcs) as $i => $s) echo service_card($s, $i); ?>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <?= section_head('See the difference', 'Same house. Flip the switch.', 'Drag the handle to see what a professionally designed system from Austin Landscape Lighting does for curb appeal, safety and the way a home feels at night.') ?>
    <div data-reveal="scale"><?= switch_compare('landscape-lighting-austin-2', 'Austin limestone home before and after landscape lighting', 'Drag to flip the switch') ?></div>
  </div>
</section>

<section class="section" id="techniques">
  <div class="container">
    <?= section_head('How light shapes a home', 'Five techniques, layered by a designer', 'Hover or tap a technique to see it on the house. Austin Landscape Lighting combines them so the final scene feels natural, never floodlit.', 'left') ?>
    <div class="tech" data-tech>
      <div class="tech__list" data-reveal="left">
        <?php foreach ($techniques as $t): ?>
        <button class="tech__item" type="button" data-layers="<?= e($t[3]) ?>" data-title="<?= e($t[1]) ?>" data-desc="<?= e($t[4]) ?>">
          <?= icon($t[0]) ?><span><strong><?= e($t[1]) ?></strong><small><?= e($t[2]) ?></small></span><?= icon('arrow', 'ico ico--sm') ?>
        </button>
        <?php endforeach; ?>
      </div>
      <div class="tech__media" data-reveal="right">
        <?= visualizer_scene('tech') ?>
        <div class="tech__caption" data-tech-caption></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="why">
  <div class="container feature-split">
    <div class="feature-split__media" data-reveal="left" data-parallax="0.08">
      <?= picture('landscape-lighting-designer-austin-tx-1', 'Austin Landscape Lighting designer aiming a brass uplight at dusk', ['width' => 1600, 'height' => 1200]) ?>
      <div class="float-card" data-reveal style="--delay:200ms"><strong>127</strong><small>five-star Google reviews from Austin homeowners and businesses</small></div>
    </div>
    <div data-reveal="right">
      <p class="eyebrow">Why Austin Landscape Lighting</p>
      <h2 class="display">Lighting that looks like it belongs there</h2>
      <p class="lede">We are not electricians with a box of fixtures. Austin Landscape Lighting is a design-first studio that has spent six years learning how light behaves on limestone, live oaks and Hill Country slopes.</p>
      <ul class="checks">
        <li><?= icon('pencil') ?><div><strong>Custom design, never cookie-cutter</strong><span>Every system is drawn fixture by fixture around your home's architecture, trees and how you use the yard.</span></div></li>
        <li><?= icon('shield') ?><div><strong>Licensed, insured professionals</strong><span>Background-checked technicians carrying full liability coverage, on every Austin Landscape Lighting crew.</span></div></li>
        <li><?= icon('dollar') ?><div><strong>No-surprise pricing</strong><span>A written, itemized estimate before any work begins. The price we quote is the price you pay.</span></div></li>
        <li><?= icon('warranty') ?><div><strong>Two-year workmanship warranty</strong><span>Plus manufacturer warranties on solid brass fixtures that range from ten years to lifetime.</span></div></li>
        <li><?= icon('leaf') ?><div><strong>Locally owned, dark-sky minded</strong><span>We live here too. Shielded 2700K fixtures keep the glow on your home and the stars over the Hill Country.</span></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="container">
    <?= section_head('How it works', 'From first call to final glow, Austin Landscape Lighting makes it easy', 'Four steps, no guesswork. Most homes go from consultation to lit in under two weeks.') ?>
    <?= process_steps() ?>
  </div>
</section>

<section class="parallax-band">
  <?= picture('austin-landscape-tree-lighting-1', 'Live oak moonlighting in an Austin backyard', ['sizes' => '100vw']) ?>
  <div class="container" data-reveal>
    <blockquote>"Our oak trees look incredible now. They used a moon-lighting technique that creates the most natural, beautiful dappled light. Every neighbor has asked who did it."<cite>Sandra W. · Rollingwood · Austin Landscape Lighting client</cite></blockquote>
  </div>
</section>

<section class="section" id="tools">
  <div class="container">
    <?= section_head('Plan before you call', 'Free planning tools from Austin Landscape Lighting', 'Estimate fixture counts, build a budget, size a transformer or preview color temperatures. Then let us turn the plan into a design.') ?>
    <div class="grid grid--4">
      <?php foreach (array_values(tools()) as $i => $t) echo tool_card($t, $i); ?>
    </div>
    <div style="margin-top:40px" data-reveal="scale">
      <?= tool_markup('fixture-calculator', true) ?>
    </div>
  </div>
</section>

<section class="section section--alt" id="reviews">
  <div class="container">
    <?= section_head('Reviews', 'Austin homeowners love what they see', '<span class="rating-badge"><span class="stars">' . str_repeat(icon('star', 'ico ico--star'), 5) . '</span> 4.9 stars · 127 reviews on Google</span>') ?>
    <div class="reviews-grid">
      <?php foreach (REVIEWS as $i => $r) echo review_card($r, $i); ?>
    </div>
    <p style="text-align:center;margin-top:28px" data-reveal><a class="btn btn--ghost" href="/reviews/">Read more Austin Landscape Lighting reviews <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section" id="areas">
  <div class="container feature-split">
    <div data-reveal="left">
      <p class="eyebrow">Service areas</p>
      <h2 class="display">Serving greater Austin and the Hill Country</h2>
      <p class="lede">From Tarrytown and Westlake to Georgetown, Dripping Springs and Kyle, Austin Landscape Lighting brings professional outdoor lighting to homeowners and businesses across Central Texas. No yard too complex.</p>
      <div class="pill-list" style="margin:22px 0 26px"><?php foreach ($areasAll as $a) echo area_chip($a); ?></div>
      <a class="btn btn--ghost" href="/service-areas/">Explore every service area <?= icon('arrow') ?></a>
    </div>
    <div class="feature-split__media" data-reveal="right" data-parallax="0.08">
      <?= picture('residential-landscape-lighting-austin-1', 'Residential landscape lighting on a Round Rock home by Austin Landscape Lighting', ['width' => 1600, 'height' => 1200]) ?>
      <div class="float-card" data-reveal style="--delay:200ms"><strong>12</strong><small>cities served from one Austin-based team, usually within 30 minutes</small></div>
    </div>
  </div>
</section>

<section class="section section--alt" id="gallery">
  <div class="container">
    <?= section_head('Recent work', 'A glimpse of Austin after dark', 'A few favorites from the Austin Landscape Lighting project gallery. Tap any photo to enlarge.') ?>
    <div class="gallery-strip" data-lightbox data-reveal>
      <?php foreach (['landscape-lighting-austin-tx-1', 'landscape-lighting-ideas-for-pools-1', 'modern-landscape-lighting-austin-2', 'landscape-lighting-ideas-for-trees-1', 'commercial-landscape-lighting-austin-1', 'front-yard-landscape-lighting-ideas-1'] as $g): ?>
        <?= picture($g, ucfirst(str_replace('-', ' ', preg_replace('/-\d+$/', '', $g))) . ' by Austin Landscape Lighting', ['width' => 1600, 'height' => 1200, 'sizes' => '(max-width: 760px) 100vw, 33vw']) ?>
      <?php endforeach; ?>
    </div>
    <p style="text-align:center" data-reveal><a class="btn btn--ghost" href="/gallery/">Browse the full gallery <?= icon('camera') ?></a></p>
  </div>
</section>

<section class="section" id="blog">
  <div class="container">
    <?= section_head('Austin Landscape Lighting resources', 'Guides for planning your outdoor lighting', 'Fixture counts, cost ranges, design rules and ideas from the designers at Austin Landscape Lighting.') ?>
    <div class="blog-grid">
      <?php foreach ($postsAll as $p) echo post_card($p); ?>
    </div>
    <p style="text-align:center;margin-top:28px" data-reveal><a class="btn btn--ghost" href="/blog/">See more articles <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section section--alt" id="faq">
  <div class="container container--narrow">
    <?= section_head('Questions', 'Austin Landscape Lighting FAQ', 'Straight answers on cost, timelines, LEDs, warranties and color temperature.') ?>
    <?= faq_list($faqs, 'home-faq') ?>
    <p style="text-align:center;margin-top:24px" data-reveal><a href="/faq/">All frequently asked questions <?= icon('arrow', 'ico ico--sm') ?></a></p>
  </div>
</section>

<?= contact_section('Limited openings this month', 'Ready to see your property in a whole new light?') ?>
<?php
$content = ob_get_clean();
render_page($page, $content);
