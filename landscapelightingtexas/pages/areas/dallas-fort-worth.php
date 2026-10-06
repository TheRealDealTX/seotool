<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'North Texas · The Metroplex';
$P['lead'] = 'Dallas–Fort Worth landscape lighting for brick and stone estates, tree-lined streets and backyard retreats, designed to meet HOA rules and stand up to North Texas hail.';
$P['_cities'] = $AREAS['dallas-fort-worth'][2];
?>
<section class="section">
  <div class="container">
    <?php split('architectural-uplighting', 'Architectural uplighting on a stone and brick North Texas home at night', '
      <p class="eyebrow">Lighting the Metroplex</p>
      <h2 class="section-title">Dallas–Fort Worth Landscape Lighting With Curb Appeal</h2>
      <p class="lead-p">North Texas homes are built to make an impression: brick and stone facades, tall entries, stacked gables and long driveways. Well-designed Dallas–Fort Worth landscape lighting keeps that impression going after dark, with balanced light that shows off the architecture instead of flattening it.</p>
      <p>Landscape Lighting Texas designs and installs low-voltage LED systems across the Metroplex, from established Dallas and Fort Worth neighborhoods to newer communities in Frisco, McKinney and Southlake. We start every project with a dusk walk of your property, then design around your home’s materials, trees and the way you use the yard.</p>
      <p>Then we build it to last through the region’s hail, temperature swings and shifting clay soil.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light in Dallas–Fort Worth', 'Metroplex homeowners usually start with the front of the house, then add the backyard. These are our most-requested features.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Brick &amp; stone facades</h3><p>Grazing light brings out the texture of brick and stone, and wider washes balance broad facades without bright spots on windows. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Driveways &amp; entries</h3><p>Low path lights, bollards and well-lit front steps give long estate driveways a clear, welcoming route to the door. See <a href="/services/pathway-driveway-lighting/">pathway and driveway lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Oaks, elms &amp; crape myrtles</h3><p>Live oaks, cedar elms, red oaks and crape myrtles each get beams matched to their height and spread. See <a href="/services/garden-tree-lighting/">tree and garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('water') ?></span><h3>Pools &amp; outdoor living</h3><p>Pool surrounds, fire features and outdoor kitchens lit in layers for evenings outside. See <a href="/services/pool-water-feature-lighting/">pool lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('smart') ?></span><h3>Smart control</h3><p>App-based zones, dimming and astronomical timers that adjust to sunset through the year. See <a href="/services/smart-lighting-systems/">smart lighting systems</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Homes &amp; commercial sites</h3><p>Shielded security lighting for homes, plus exterior lighting for offices, retail and multifamily properties. See <a href="/services/security-lighting/">security and floodlighting</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Landscape Lighting for North Texas', '', 'left'); ?>
        <p>North Texas weather is tough on outdoor equipment. Spring hailstorms can crack plastic lenses and dent thin housings, summer heat bakes everything in direct sun, and the occasional winter freeze tests every seal. Much of the Metroplex also sits on expansive clay that swells when wet and shrinks in drought, which can shift fixtures and stress buried connections.</p>
        <p>Many neighborhoods in Southlake, Plano, Frisco and other suburbs also have HOA guidelines about exterior lighting. We design with those rules in mind and can provide fixture details and a plan for architectural review when your association asks for one.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Solid brass and copper fixtures with glass lenses that stand up to hail better than plastic',
            'Sturdy stakes and fixture mounts set to stay put as clay soil moves',
            'Direct-burial cable with slack at each fixture so movement does not pull connections apart',
            'Shielded, low-glare fixtures and warm 2700K–3000K color that suit HOA guidelines',
            'Fixture specifications and a lighting plan for HOA architectural review',
            'Multi-tap transformers and 12- or 10-gauge cable for long runs on larger lots',
            'Seasonal timer settings so lights follow early winter dusk and late summer sunsets',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'Dallas–Fort Worth Communities We Serve', 'We work across both sides of the Metroplex. Do not see yours? <a href="/quote/">Ask us</a>; nearby areas are usually within reach.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['Dallas', 'Highland Park', 'University Park', 'Preston Hollow', 'Lakewood', 'Fort Worth', 'Westover Hills', 'Plano', 'Frisco', 'McKinney', 'Allen', 'Prosper', 'Southlake', 'Colleyville', 'Keller', 'Grapevine', 'Flower Mound', 'Coppell', 'Arlington', 'Irving', 'Garland', 'Rockwall', 'Denton'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'A North Texas Facade, Lit With Balance', 'Drag the slider to compare. Grazing light on stone and brick, soft washes on the wider walls and lit entry columns give the home presence from the street.'); ?>
    <?php before_after('architectural-uplighting', 'Architectural uplighting on a Texas home, installed by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How a Dallas–Fort Worth Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer meets you at sunset to walk the property, look at the facade and trees as the light drops and talk through HOA requirements.</p></li>
      <li><h3>Custom design</h3><p>You get a lighting plan and itemized quote: fixtures, beam angles, color temperature, transformer size and zones. Typical residential projects fall in a planning range of $2,500–$12,000.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs cable, fixtures and the transformer, working around irrigation, roots and hardscape, and cleans up as we go.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We return after dark to aim and balance each fixture, set the timer and show you the controls. Work is covered by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/lighting-design-simulator/') ?></div>
  </div>
</section>

<?php faqs([
    ['Will my HOA approve landscape lighting?', 'Many HOAs readily allow tasteful landscape lighting, especially warm, shielded, low-glare designs. Rules vary by community, so we review your guidelines during the consultation and can provide fixture specifications and a plan for your architectural review submission.'],
    ['How does landscape lighting hold up to North Texas hail?', 'Solid brass and copper fixtures with tempered glass lenses handle hail far better than plastic or thin aluminum. Most low-profile fixtures also sit sheltered among plants. If a storm does damage something, our <a href="/services/landscape-lighting-maintenance/">repair service</a> can replace lenses or fixtures quickly.'],
    ['Does clay soil cause problems for lighting systems?', 'Expansive clay can shift fixtures and strain buried splices over time. We use sturdy stakes, leave slack at each connection and use sealed splices so the system tolerates normal ground movement. An annual tune-up handles any re-aiming.'],
    ['What does landscape lighting cost in Dallas–Fort Worth?', 'Most residential projects fall in a planning range of $2,500–$12,000, with starter systems around $2,500–$5,000 and estate properties sometimes exceeding $20,000. Try our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a quick estimate.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('dallas-fort-worth'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your North Texas Home?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
