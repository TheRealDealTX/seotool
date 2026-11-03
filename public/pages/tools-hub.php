<?php
defined('SCC') || exit;
$tools = tools_meta();
page_head([
    'title' => 'Free Solar Camera Calculators & Planning Tools',
    'description' => 'Free solar security camera tools: panel angle by latitude, battery and panel sizing, 4G data use, coverage, camera count and solar vs wired cost.',
    'path' => '/tools/',
    'schema' => [
        breadcrumb_schema([['Home', '/'], ['Tools', '/tools/']]),
        ['@type' => 'CollectionPage', 'name' => 'Solar camera tools', 'url' => abs_url('/tools/'),
         'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_values(array_map(fn($t, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($t['path']), 'name' => $t['name']], $tools, range(0, count($tools) - 1)))]],
    ],
]);
?>
<section class="page-hero">
  <div class="hero-sky" aria-hidden="true"><span class="hero-sun"></span></div>
  <div class="wrap" style="position:relative">
    <?= breadcrumbs_html([['Home', '/'], ['Tools', '/tools/']]) ?>
    <h1>Free solar camera tools</h1>
    <p class="lede">Seven calculators that answer the questions spec sheets don’t: will this panel keep up in December, how many sunless days will the battery survive, how much 4G data will I burn, and is solar actually cheaper than running a cable? Everything runs in your browser; nothing is stored.</p>
  </div>
</section>
<section class="section" style="padding-top:50px">
  <div class="wrap">
    <div class="tool-grid">
<?php foreach ($tools as $t) echo tool_card($t); ?>
    </div>
    <div class="split" style="margin-top:70px">
      <div class="reveal">
        <span class="overline">Which tool first?</span>
        <h2>A five-minute sizing workflow</h2>
        <ol class="steps" style="padding:0">
          <li><strong>Plan the cameras</strong><p>Use the <a href="/tools/cctv-camera-planner/">CCTV Camera Planner</a> to decide how many cameras and which zones.</p></li>
          <li><strong>Check each spot</strong><p>Run the <a href="/tools/solar-camera-site-check/">Solar Site Check</a> for every location you intend to power with solar.</p></li>
          <li><strong>Aim the panel</strong><p>Get the tilt and direction for your latitude from the <a href="/tools/solar-panel-angle-calculator/">Panel Angle Calculator</a>.</p></li>
          <li><strong>Size panel &amp; battery</strong><p>Confirm the energy budget, including a cloudy week, with the <a href="/tools/solar-camera-battery-calculator/">Battery &amp; Power Calculator</a>.</p></li>
          <li><strong>Fine-tune</strong><p>Check plate/face detail with the <a href="/tools/camera-coverage-calculator/">Coverage Calculator</a>, estimate SIM data with the <a href="/tools/4g-data-and-storage-calculator/">4G Data Calculator</a>, and compare against wiring with the <a href="/tools/solar-vs-wired-cost-calculator/">cost calculator</a>.</p></li>
        </ol>
      </div>
      <div class="split-media reveal"><?= img('solar-camera-system', 'Solar powered outdoor security camera system on a pole', ['sizes' => '(max-width: 860px) 100vw, 560px']) ?></div>
    </div>
  </div>
</section>
<?php require_once ROOT . '/inc/article.php'; page_foot();
