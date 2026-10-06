<?php defined('SLT') || exit;
add_schema(['@type' => 'AboutPage', 'name' => 'About Spring Landscape Lighting', 'url' => abs_url('/about-us/'), 'about' => ['@id' => SITE_URL . '/#business']]);
page_hero(['title' => 'About Spring Landscape Lighting', 'eyebrow' => 'Who we are', 'tall' => true, 'img' => 'Spring-Landscape-Lighting-BG-2.webp',
  'sub' => 'We believe a home should feel just as welcoming, comfortable and beautifully designed after sunset as it does during the day.', 'cta' => true, 'crumbs' => [['Home', '/'], ['About Us', null]]]);
?>
<section class="sec">
  <div class="wrap split">
    <div class="prose">
      <p class="lead">Spring Landscape Lighting provides custom landscape lighting design, installation, repair and system upgrades for homeowners in Spring, Texas and surrounding North Houston communities.</p>
      <p>Every lighting plan is created around the property itself, not pulled from a standard package or built around a fixed number of fixtures. That distinction matters. The best outdoor lighting reveals architectural details, makes walkways easier to navigate, brings mature trees to life and creates outdoor spaces people genuinely want to use.</p>
      <p>Our goal is to achieve all of that without making a home feel overlit, harsh or artificial.</p>
      <blockquote class="pull">Installing more fixtures does not automatically create a better result. Good lighting requires restraint.</blockquote>
    </div>
    <div data-reveal="right"><div class="frame"><img src="/assets/img/Spring-Landscape-Lighting-BG-1.webp" alt="Warm accent lighting on ornamental grasses at night" loading="lazy"><div class="frame__tag"><?= icon('moon') ?><span><strong>Designed for the night</strong>Every system is aimed and adjusted after dark.</span></div></div></div>
  </div>
</section>

<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('Lighting designed around your home', 'It starts with listening', 'No two properties in Spring are alike. Deep front yards, big oaks and pines, layered beds, brick and stone, pools, kitchens and long driveways all call for different answers.'); ?>
    <div class="grid-3">
      <?php foreach ([['house', 'Which areas you use most', 'Entries, patios, pool decks and paths you actually walk after dark.'], ['eye', 'What deserves attention', 'Architecture, specimen trees, textures and views worth revealing.'], ['footprints', 'Where visibility helps', 'Steps, grade changes, driveways and dark side yards.'], ['sparkles', 'How it should feel', 'Subtle accents, dramatic presentation or a balance of both.'], ['timer', 'How it should be controlled', 'Zones, schedules, dimming and app control that fit your evenings.'], ['moon', 'Where darkness should stay', 'Contrast, neighbors, wildlife and the night sky.']] as $i => [$ic, $t, $d]): ?>
      <div class="kv__item" data-reveal data-delay="<?= $i % 3 ?>"><?= icon($ic) ?><h3><?= e($t) ?></h3><p><?= e($d) ?></p></div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split split--rev">
    <div class="prose">
      <h2>Built for Spring, Texas conditions</h2>
      <p>Outdoor lighting in Southeast Texas has to survive more than the occasional storm. Heat, humidity, heavy rain, irrigation, insects, soil movement, fast-growing plants and severe weather all work against fixtures, wire, connections and transformers.</p>
      <p>A system that looks good on installation day is not enough. Our plans account for local conditions from the beginning: professional-grade low-voltage components, weather-conscious installation, secure connections, concealed wire and fixture placements that stay practical as the landscape grows.</p>
      <p>We also consider drainage, mowing patterns, sprinkler coverage, planting beds and tree roots, the details that decide whether a system still works well years from now.</p>
    </div>
    <div class="kv" style="grid-template-columns:1fr 1fr" data-reveal="left">
      <div class="kv__item"><?= icon('thermometer') ?><h3>Heat</h3><p>Components and connections chosen for long Texas summers.</p></div>
      <div class="kv__item"><?= icon('cloud-rain') ?><h3>Rain</h3><p>Placement and connections that respect drainage and storms.</p></div>
      <div class="kv__item"><?= icon('droplets') ?><h3>Irrigation</h3><p>Fixtures kept clear of spray to limit hard-water buildup.</p></div>
      <div class="kv__item"><?= icon('sprout') ?><h3>Growth</h3><p>Positions that still work as beds fill in and trees mature.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--light">
  <div class="wrap">
    <?php section_head('Why homeowners choose Spring Landscape Lighting', 'Six principles behind every project'); ?>
    <div class="kv">
      <div class="kv__item" data-reveal><?= icon('message-circle') ?><h3>We listen before we design</h3><p>The system should support the way you live, not force your property into a preset package.</p></div>
      <div class="kv__item" data-reveal data-delay="1"><?= icon('sparkles') ?><h3>We prioritize the finished effect</h3><p>Fixture count is not the goal. A comfortable, attractive and useful nighttime environment is.</p></div>
      <div class="kv__item" data-reveal data-delay="2"><?= icon('leaf') ?><h3>We respect the property</h3><p>Clean, careful installation planned around the landscaping, never treated as an afterthought.</p></div>
      <div class="kv__item" data-reveal><?= icon('eye') ?><h3>We use light with restraint</h3><p>Balance, contrast and appropriate brightness instead of flooding every surface.</p></div>
      <div class="kv__item" data-reveal data-delay="1"><?= icon('shield-check') ?><h3>We plan for long-term performance</h3><p>Fixtures, wiring, controls, drainage, plant growth and weather are part of the design.</p></div>
      <div class="kv__item" data-reveal data-delay="2"><?= icon('map-pin') ?><h3>We provide local service</h3><p>We know the home styles, vegetation, climate and outdoor living habits of North Houston.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <?php section_head('What we do', 'Complete outdoor lighting, new and existing', 'Spring Landscape Lighting designs new systems and improves existing ones.'); ?>
    <div class="grid-3"><?php $i = 0; foreach (SERVICES as $k => $s) echo service_card($k, $s, $i++); ?></div>
  </div>
</section>

<section class="sec sec--forest">
  <div class="wrap split">
    <div class="prose">
      <h2>See your home differently after dark</h2>
      <p>A successful landscape lighting system changes more than the appearance of a house. It makes the front entry feel welcoming, gives patios a reason to stay open longer, turns trees and gardens into part of the evening view, and makes moving around the property easier and safer.</p>
      <p>Most importantly, it creates an atmosphere that feels natural to the home. Spring Landscape Lighting is here to help you plan, install and maintain a system that is refined, reliable and designed specifically for your property.</p>
      <p>Call <a href="tel:<?= PHONE_TEL ?>"><?= PHONE ?></a> or email <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a> to get started, or <a href="/our-process/">see how our process works</a>.</p>
    </div>
    <div class="formcard" data-reveal="right"><h3>Request a complimentary consultation</h3><?php quote_form('about', true); ?></div>
  </div>
</section>
<?php cta_band(); ?>
