<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['About Us', '/about-us/']];
$page = [
    'title' => 'About Austin Landscape Lighting | Outdoor Lighting Designers',
    'description' => 'Learn about Austin Landscape Lighting, Austin\'s trusted outdoor lighting company since 2020: design-first, licensed crews, brass LED systems, 2-year warranty.',
    'path' => '/about-us/',
    'active' => '/about-us/',
    'image' => 'landscape-lighting-company-austin-2',
    'schema' => [schema_webpage(['title' => 'About Austin Landscape Lighting', 'description' => 'About Austin Landscape Lighting.', 'path' => '/about-us/'], 'AboutPage'), schema_breadcrumb($crumbs)],
];
ob_start();
echo sub_hero(['eyebrow' => 'About us', 'h1' => 'Bringing Austin Properties to Life After Dark', 'intro' => 'Austin Landscape Lighting is a locally owned outdoor lighting design and installation company. Since 2020 we have lit more than 500 homes and businesses across Austin and the Hill Country with low-voltage LED systems that look like they belong.', 'image' => 'landscape-lighting-company-austin-2', 'image_alt' => 'Austin Landscape Lighting team reviewing a lighting design at dusk', 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container layout">
    <article class="prose" data-reveal>
      <h2>Outdoor lighting should do more than brighten a property</h2>
      <p>Every home, landscape and commercial property has architectural details, mature trees, gardens, pathways and outdoor living spaces that deserve to be appreciated long after the sun goes down. Our mission at Austin Landscape Lighting is to create custom landscape lighting systems that highlight those features while improving safety, security and curb appeal.</p>
      <p>As a locally focused Austin landscape lighting company, we specialize in designing, installing, maintaining and upgrading premium outdoor lighting systems for residential and commercial properties throughout Austin and the surrounding communities. Whether you want a welcoming front entrance, an illuminated backyard entertaining area, architectural details that stand out or better nighttime visibility, our team delivers lighting built specifically for your property.</p>
      <h2>Our passion for outdoor lighting</h2>
      <p>Landscape lighting is both an art and a science. It takes technical expertise, thoughtful design and an understanding of how light interacts with architecture, trees, stonework, water features and outdoor living spaces. Rather than relying on generic layouts, we create designs that complement the natural beauty of your property.</p>
      <p>Every project begins with listening. We take the time to understand your goals, evaluate your landscape, identify focal points and recommend techniques that produce dramatic yet natural-looking results. The goal is simple: an outdoor environment that looks as impressive at night as it does during the day.</p>
      <blockquote>We are not electricians with a box of fixtures. We are designers who understand how light shapes space, mood and perception, and we have spent six years learning how it behaves on Austin stone and live oaks.</blockquote>
      <h2>What we do</h2>
      <p>Austin Landscape Lighting provides complete outdoor lighting solutions from concept to completion: custom lighting design, installation, architectural uplighting, path and walkway lighting, garden and tree lighting, patio, deck and pool lighting, smart lighting systems, LED upgrades, low-voltage installation, repair, routine maintenance and system expansions. Every installation is planned to maximize beauty while minimizing energy consumption and maintenance.</p>
      <h2>How we are different</h2>
      <div class="values">
        <div class="card"><span class="card__icon"><?= icon('pencil') ?></span><h3>Design first</h3><p>A dusk walkthrough and a fixture-by-fixture plan before anything is sold. Techniques, beam spreads and color temperature are decided on paper, then proven at night.</p></div>
        <div class="card"><span class="card__icon"><?= icon('shield') ?></span><h3>Licensed and insured</h3><p>Background-checked technicians with full liability coverage. Clean installs, buried wire, beds left as we found them.</p></div>
        <div class="card"><span class="card__icon"><?= icon('warranty') ?></span><h3>Built to last</h3><p>Solid brass and copper fixtures, marine-grade connectors and a two-year workmanship warranty on every Austin Landscape Lighting install.</p></div>
      </div>
      <h2>Six years of Austin nights</h2>
      <ul class="timeline">
        <li><strong>2020</strong><p>Austin Landscape Lighting opens with a simple idea: treat outdoor lighting as design, not hardware. First projects in Tarrytown and Westlake.</p></li>
        <li><strong>2022</strong><p>Smart controls and app-based zoning become standard offerings. We pass 150 completed projects across Travis and Williamson counties.</p></li>
        <li><strong>2024</strong><p>LED retrofit program launches for the thousands of aging halogen systems around Austin. Commercial work expands to restaurants and retail.</p></li>
        <li><strong>2026</strong><p>More than 500 projects lit, a 4.9-star Google rating across 127 reviews, and a dozen cities served from Georgetown to Dripping Springs.</p></li>
      </ul>
      <h2>Serving Austin and the Hill Country</h2>
      <p>We are based in Austin and work across <?= implode(', ', array_map(fn($a) => '<a href="' . e($a['path']) . '">' . e($a['city']) . '</a>', array_values(areas()))) ?>. Consultations are free, scheduled at dusk when possible, and come with a written, itemized estimate.</p>
    </article>
    <?= sidebar(['links' => array_map(fn($s) => [$s['name'], $s['path']], array_slice(array_values(services()), 0, 6)), 'links_title' => 'Our services']) ?>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <?= section_head('By the numbers', 'Austin Landscape Lighting at a glance') ?>
    <?= stats_row() ?>
  </div>
</section>
<section class="section">
  <div class="container">
    <?= section_head('Reviews', 'What Austin says about us') ?>
    <div class="reviews-grid"><?php foreach (array_slice(REVIEWS, 0, 3) as $i => $r) echo review_card($r, $i); ?></div>
  </div>
</section>
<?= contact_section('Meet the team', 'Let\'s talk about your property') ?>
<?php
render_page($page, ob_get_clean());
